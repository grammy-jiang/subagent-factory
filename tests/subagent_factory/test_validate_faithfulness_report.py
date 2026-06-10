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
