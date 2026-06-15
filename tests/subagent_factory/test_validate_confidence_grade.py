"""Tests for GRADE-consistency of principle confidence (Step 16 / K2 wiring)."""

import yaml

from tools.subagent_factory.validate_confidence_grade import validate_confidence_grade


def _pf(tmp_path, principles):
    p = tmp_path / "principles.yaml"
    p.write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    return p


def _prin(confidence, grade=None):
    p = {
        "principle_id": "P1",
        "statement": "x",
        "derived_from_claims": ["c1"],
        "confidence": confidence,
    }
    if grade is not None:
        p["grade"] = grade
    return p


def test_matching_grade_passes(tmp_path):
    # peer-reviewed(high) − 1 downgrade → medium; confidence medium → consistent
    pr = [_prin("medium", {"source_type": "peer-reviewed", "downgrades": ["risk-of-bias"]})]
    assert validate_confidence_grade(_pf(tmp_path, pr)) == []


def test_mismatch_flagged(tmp_path):
    # peer-reviewed, no factors → high; confidence low → mismatch
    pr = [_prin("low", {"source_type": "peer-reviewed"})]
    errs = validate_confidence_grade(_pf(tmp_path, pr))
    assert any("GRADE-computed 'high'" in e for e in errs)


def test_insufficient_flagged(tmp_path):
    # anecdotal(low) − 1 downgrade → insufficient → should not be promoted
    pr = [_prin("low", {"source_type": "anecdotal", "downgrades": ["conflict"]})]
    errs = validate_confidence_grade(_pf(tmp_path, pr))
    assert any("insufficient" in e for e in errs)


def test_no_grade_block_passes(tmp_path):
    # validate-if-present: a principle without a grade block is untouched
    assert validate_confidence_grade(_pf(tmp_path, [_prin("low")])) == []
