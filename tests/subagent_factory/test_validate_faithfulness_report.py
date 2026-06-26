"""Tests for the faithfulness-report validator (Step 1)."""

import json

import yaml

from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report

_GOOD = {
    "schema_version": "faithfulness-report-v1",
    "subagent_slug": "demo",
    "findings": [
        {
            "rule_ref": "quality_bar[2]",
            "verdict": "SCOPE_BROADENED",
            "action": "downgrade",
            "source_anchors": ["src-1-h0001"],
            "severity": "high",
        }
    ],
}


def _pkg(tmp_path, report, profile=None, anchors=None):
    base = tmp_path / "pkg"
    (base / "reports").mkdir(parents=True)
    rp = base / "reports" / "faithfulness-report.yaml"
    rp.write_text(yaml.safe_dump(report), encoding="utf-8")
    if profile is not None:
        (base / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    if anchors is not None:
        (base / "sources" / "anchors").mkdir(parents=True)
        (base / "sources" / "anchors" / "src-1.anchors.jsonl").write_text(
            "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
        )
    return rp


def test_valid_report(tmp_path):
    rp = _pkg(tmp_path, _GOOD, profile={"quality_bar": ["a", "b", "c"]}, anchors=["src-1-h0001"])
    assert validate_faithfulness_report(rp) == []


def test_bad_enum_is_schema_error(tmp_path):
    rep = {
        **_GOOD,
        "findings": [{"rule_ref": "quality_bar", "verdict": "NOPE", "action": "downgrade"}],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": []})
    assert validate_faithfulness_report(rp)


def test_unknown_rule_ref_field(tmp_path):
    rep = {
        **_GOOD,
        "findings": [
            {"rule_ref": "nonexistent[0]", "verdict": "WITHIN_SCOPE", "action": "accept_with_note"}
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": []}, anchors=["src-1-h0001"])
    assert any("no field" in e for e in validate_faithfulness_report(rp))


def test_rule_ref_index_out_of_range(tmp_path):
    # quality_bar has 1 element; [5] is a coverage hole the report must not claim.
    rep = {
        **_GOOD,
        "findings": [
            {"rule_ref": "quality_bar[5]", "verdict": "WITHIN_SCOPE", "action": "accept_with_note"}
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": ["only-one"]}, anchors=["src-1-h0001"])
    assert any("does not resolve" in e for e in validate_faithfulness_report(rp))


def test_rule_ref_unknown_mode_name(tmp_path):
    rep = {
        **_GOOD,
        "findings": [
            {
                "rule_ref": "outputs.modes[ghost].trigger",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
            }
        ],
    }
    profile = {"outputs": {"modes": [{"name": "review", "trigger": "t"}]}}
    rp = _pkg(tmp_path, rep, profile=profile, anchors=["src-1-h0001"])
    assert any("does not resolve" in e for e in validate_faithfulness_report(rp))


def test_rule_ref_named_mode_resolves_both_forms(tmp_path):
    profile = {"outputs": {"modes": [{"name": "review", "trigger": "t", "output": "o"}]}}
    for ref in ("outputs.modes[review].trigger", "outputs.modes.review.output"):
        rep = {
            **_GOOD,
            "findings": [
                {"rule_ref": ref, "verdict": "EXACT_SUPPORT", "action": "accept_with_note"}
            ],
        }
        rp = _pkg(
            tmp_path / ref.replace(".", "_").replace("[", "_").replace("]", "_"),
            rep,
            profile=profile,
        )
        assert validate_faithfulness_report(rp) == [], ref


def test_rule_ref_in_range_index_ok(tmp_path):
    rep = {
        **_GOOD,
        "findings": [
            {"rule_ref": "quality_bar[2]", "verdict": "WITHIN_SCOPE", "action": "accept_with_note"}
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": ["a", "b", "c"]}, anchors=["src-1-h0001"])
    assert validate_faithfulness_report(rp) == []


def test_anchor_not_in_index(tmp_path):
    rep = {
        **_GOOD,
        "findings": [
            {
                "rule_ref": "quality_bar",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
                "source_anchors": ["ghost-h9999"],
            }
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": []}, anchors=["src-1-h0001"])
    assert any("anchor index" in e for e in validate_faithfulness_report(rp))


def test_unresolved_contradiction(tmp_path):
    rep = {
        **_GOOD,
        "findings": [
            {"rule_ref": "quality_bar", "verdict": "CONTRADICTED", "action": "accept_with_note"}
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": []})
    assert any("CONTRADICTED" in e for e in validate_faithfulness_report(rp))


def test_contradicted_with_add_condition_fails(tmp_path):
    # A CONTRADICTED rule conflicts with its source; adding a condition does not make it true.
    # Only an actual resolution (remove/downgrade) is acceptable — accept_with_note AND add_condition
    # must both FAIL (they don't resolve the contradiction).
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": "demo",
        "findings": [
            {"rule_ref": "quality_bar", "verdict": "CONTRADICTED", "action": "add_condition"}
        ],
    }
    rp = _pkg(tmp_path, report, profile={"quality_bar": ["a"]})
    assert any("CONTRADICTED" in e for e in validate_faithfulness_report(rp))


def test_contradicted_with_downgrade_passes(tmp_path):
    # A CONTRADICTED finding resolved by an actual fix (downgrade/remove) is the legitimate path.
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": "demo",
        "findings": [{"rule_ref": "quality_bar", "verdict": "CONTRADICTED", "action": "downgrade"}],
    }
    rp = _pkg(tmp_path, report, profile={"quality_bar": ["a"]})
    assert not any("CONTRADICTED" in e for e in validate_faithfulness_report(rp))


def test_scope_broadened_accept_with_note_fails(tmp_path):
    # SCOPE_BROADENED / HEDGING_REMOVED are over-claims (the rule says more than the source). A bare
    # note does not correct the drift — it must be downgraded/removed/conditioned. accept_with_note
    # must FAIL for these verdicts, same class as CONTRADICTED one rung up the ladder.
    for verdict in ("SCOPE_BROADENED", "HEDGING_REMOVED"):
        report = {
            "schema_version": "faithfulness-report-v1",
            "subagent_slug": "demo",
            "findings": [
                {"rule_ref": "quality_bar[0]", "verdict": verdict, "action": "accept_with_note"}
            ],
        }
        rp = _pkg(tmp_path / verdict, report, profile={"quality_bar": ["a", "b", "c"]})
        assert any(verdict in e for e in validate_faithfulness_report(rp)), (
            f"{verdict} over-claim accepted with only a note must FAIL"
        )


def test_scope_broadened_add_condition_passes(tmp_path):
    # Unlike CONTRADICTED, a SCOPE_BROADENED claim CAN be legitimately re-scoped by a condition.
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": "demo",
        "findings": [
            {"rule_ref": "quality_bar[0]", "verdict": "SCOPE_BROADENED", "action": "add_condition"}
        ],
    }
    rp = _pkg(tmp_path, report, profile={"quality_bar": ["a", "b", "c"]})
    assert not any("SCOPE_BROADENED" in e for e in validate_faithfulness_report(rp))


def test_empty_findings_on_nontrivial_profile_fails(tmp_path):
    # A report with zero findings on a profile that has gradable rules means the faithfulness step
    # graded NOTHING — the gate must not report "faithful" by vacuous omission.
    report = {"schema_version": "faithfulness-report-v1", "subagent_slug": "demo", "findings": []}
    rp = _pkg(tmp_path, report, profile={"quality_bar": ["a", "b", "c"]})
    assert validate_faithfulness_report(rp), "empty findings on a non-trivial profile must FAIL"


def test_empty_findings_on_empty_profile_passes(tmp_path):
    # No gradable rules → nothing to grade → empty findings is legitimately fine (no false-FAIL).
    report = {"schema_version": "faithfulness-report-v1", "subagent_slug": "demo", "findings": []}
    rp = _pkg(tmp_path, report, profile={"slug": "demo"})
    assert validate_faithfulness_report(rp) == []


def test_freetext_anchor_flagged_as_invalid(tmp_path):
    # The faithfulness step sometimes emits a section description instead of an anchor id; it must
    # be flagged distinctly (free text), not as a merely-missing index entry.
    rep = {
        **_GOOD,
        "findings": [
            {
                "rule_ref": "quality_bar",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
                "source_anchors": ["whole book — explanatory commentary style"],
            }
        ],
    }
    rp = _pkg(tmp_path, rep, profile={"quality_bar": []}, anchors=["src-1-h0001"])
    assert any("not a valid anchor id" in e for e in validate_faithfulness_report(rp))
