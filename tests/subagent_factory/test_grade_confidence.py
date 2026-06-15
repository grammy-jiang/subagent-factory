"""Tests for the deterministic GRADE-style confidence function (Step 16 / K2)."""

from tools.subagent_factory.grade_confidence import grade_confidence


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
