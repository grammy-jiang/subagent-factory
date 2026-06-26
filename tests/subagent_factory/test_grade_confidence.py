"""Tests for the deterministic GRADE-style confidence function (Step 16 / K2 + K4 + K5)."""

from tools.subagent_factory.grade_confidence import (
    conflict_label,
    grade_confidence,
    grade_with_rob,
    rob_weight,
)


def test_baseline_by_source_type():
    assert grade_confidence("peer-reviewed")["level"] == "high"
    assert grade_confidence("expert-book")["level"] == "medium"
    assert grade_confidence("anecdotal")["level"] == "low"
    assert grade_confidence("unknown-xyz")["level"] == "medium"  # default baseline


def test_downgrade_lowers_one_step_each():
    assert grade_confidence("peer-reviewed", downgrades=["risk-of-bias"])["level"] == "medium"
    assert (
        grade_confidence("expert-book", downgrades=["conflict", "inconsistency"])["level"]
        == "insufficient"
    )


def test_upgrade_raises():
    assert grade_confidence("anecdotal", upgrades=["replication"])["level"] == "medium"


def test_clamp_floor_and_ceiling():
    # below "low" floors at the abstention level; above "high" clamps at "high"
    assert (
        grade_confidence("anecdotal", downgrades=["risk-of-bias", "conflict"])["level"]
        == "insufficient"
    )
    assert (
        grade_confidence("peer-reviewed", upgrades=["replication", "large-effect"])["level"]
        == "high"
    )


def test_net_up_and_down():
    # high(3) − 2 + 1 = 2 → medium
    g = grade_confidence("peer-reviewed", downgrades=["a", "b"], upgrades=["c"])
    assert g["level"] == "medium"


def test_medium_is_reported_as_a_range():
    g = grade_confidence("expert-book")  # medium baseline, no factors
    assert g["level"] == "medium"
    assert g["range"] == ["low", "high"]


def test_clean_baseline_extreme_is_tight():
    assert grade_confidence("peer-reviewed")["range"] == ["high", "high"]


def test_adjusted_grade_surfaces_uncertainty_range():
    g = grade_confidence("peer-reviewed", downgrades=["risk-of-bias"])  # → medium, factors applied
    assert g["level"] == "medium" and g["range"] == ["low", "high"]


def test_insufficient_floor_below_low():
    assert grade_confidence("anecdotal", downgrades=["risk-of-bias"])["level"] == "insufficient"


def test_audit_fields_preserved():
    g = grade_confidence("peer-reviewed", downgrades=["conflict"])
    assert g["baseline"] == "high" and g["downgrades"] == ["conflict"] and g["upgrades"] == []


def test_range_is_fixed_pm1_adjacency_flag_not_magnitude():
    # HONESTY (K6): `range` is a FIXED ±1 adjacency flag ("this grade was adjusted"), NOT a
    # magnitude — one downgrade and five downgrades that land on the same level report the same
    # ±1-step range. Pin that documented behaviour so the docstring stays honest.
    one = grade_confidence("peer-reviewed", downgrades=["a"])  # high -> medium
    many = grade_confidence(
        "peer-reviewed", downgrades=["a", "b", "c", "d", "e"]
    )  # clamps to floor
    # both moved, both report a ±1-step window around their (clamped) level; width is not scaled
    assert one["range"] == ["low", "high"]  # around medium
    assert many["level"] == "insufficient"
    assert many["range"] == ["insufficient", "low"]  # ±1 around the floor, still width 1, not 5


def test_saturated_flag_when_clamped():
    # ROBUSTNESS: when the raw index was clamped (factors pushed past the LEVELS span) the grade is
    # `saturated`; an unclamped grade is not.
    assert grade_confidence("peer-reviewed")["saturated"] is False
    g = grade_confidence("anecdotal", downgrades=["a", "b", "c"])  # low - 3 → clamped to floor
    assert g["level"] == "insufficient" and g["saturated"] is True
    hi = grade_confidence("peer-reviewed", upgrades=["a", "b"])  # high + 2 → clamped to ceiling
    assert hi["level"] == "high" and hi["saturated"] is True


# ── K4: risk-of-bias as advisory weight, never a gate ──


def test_rob_overall_high_when_any_domain_high():
    r = rob_weight(["low", "high", "some-concerns"])
    assert r["overall"] == "high"
    assert r["downgrades"] == ["risk-of-bias"]  # capped at one
    assert r["is_gate"] is False and r["advisory"] is True


def test_rob_some_concerns_does_not_auto_downgrade():
    # weak signal: some-concerns is surfaced but does not lower the grade (only a clear high does)
    r = rob_weight(["low", "some-concerns", "low"])
    assert r["overall"] == "some-concerns" and r["downgrades"] == []


def test_rob_all_low():
    r = rob_weight(["low", "low"])
    assert r["overall"] == "low" and r["downgrades"] == []


def test_rob_unclear_not_treated_as_high():
    # uncertainty is not bias: an unclear-only assessment must not fire a downgrade
    r = rob_weight(["unclear", "low"])
    assert r["overall"] == "unclear" and r["downgrades"] == []


def test_rob_accepts_dict():
    r = rob_weight({"randomization": "low", "missing-data": "high"})
    assert r["overall"] == "high" and r["counts"]["high"] == 1


def test_rob_empty():
    r = rob_weight([])
    assert r["overall"] == "unclear" and r["downgrades"] == []


def test_rob_unrecognized_level_routes_to_unclear_not_vanish():
    # ROB rollup: a level outside the RoB2 vocabulary ("n/a", "weird") must not silently vanish
    # from the rollup — it routes to `unclear` (uncertainty), and the count is surfaced.
    r = rob_weight(["weird", "n/a"])
    assert r["overall"] == "unclear" and r["downgrades"] == []
    # the unrecognized inputs are surfaced, not dropped
    assert r["counts"].get("unclear", 0) >= 1 or r["unrecognized"]


def test_rob_unrecognized_does_not_block_a_real_high():
    # a genuine `high` still rolls up to high even when an unrecognized level is present
    r = rob_weight(["high", "bogus"])
    assert r["overall"] == "high" and r["downgrades"] == ["risk-of-bias"]


def test_grade_with_rob_lowers_but_never_drops():
    # high baseline + an overall-high RoB → one step down to medium; RoB cannot drop the source
    g = grade_with_rob("peer-reviewed", ["high"])
    assert g["level"] == "medium"
    assert "risk-of-bias" in g["downgrades"]
    assert g["rob"]["overall"] == "high" and g["rob"]["is_gate"] is False


def test_grade_with_rob_clean_rob_no_change():
    g = grade_with_rob("peer-reviewed", ["low", "low"])
    assert g["level"] == "high" and g["rob"]["downgrades"] == []


# ── K5: dual-judge conflict → verification label (reground, not average) ──


def test_conflict_all_agree_high():
    r = conflict_label(["accept", "accept"])
    assert r["label"] == "agree" and r["verification"] == "high" and r["needs_human"] is False
    assert r["agreement"] == 1.0


def test_conflict_unresolved_withholds_for_human():
    r = conflict_label(["accept", "reject"])  # disagree, no reground supplied
    assert (
        r["label"] == "unresolved" and r["verification"] == "withhold" and r["needs_human"] is True
    )


def test_conflict_one_wins_after_reground_medium():
    r = conflict_label(["accept", "reject"], winner=0)
    assert r["label"] == "one_wins" and r["verification"] == "medium" and r["needs_human"] is False


def test_conflict_both_wrong_withholds():
    r = conflict_label(["accept", "reject"], both_wrong=True)
    assert (
        r["label"] == "both_wrong" and r["verification"] == "withhold" and r["needs_human"] is True
    )


def test_conflict_both_wrong_precedence_over_winner():
    r = conflict_label(["a", "b"], winner=0, both_wrong=True)
    assert r["label"] == "both_wrong"


def test_conflict_never_averages_three_judges():
    # 2 accept / 1 reject must NOT become a majority "accept" — disagreement → withhold, not average
    r = conflict_label(["accept", "accept", "reject"])
    assert r["verification"] == "withhold" and round(r["agreement"], 2) == 0.67


def test_conflict_empty():
    r = conflict_label([])
    assert r["label"] == "no_judgments" and r["needs_human"] is True
