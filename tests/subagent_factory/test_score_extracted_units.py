"""Tests for Phase 2.5 importance ranking (score_extracted_units)."""

import tempfile

import yaml

from tools.subagent_factory.score_extracted_units import (
    DIMENSIONS,
    format_worksheet,
    score_unit,
    score_units,
    score_units_file,
)


def _scores(value=3, **overrides):
    s = {d: value for d in DIMENSIONS}
    s.update(overrides)
    return s


def test_keep_by_total():
    # all 4s -> total 36 >= 32
    r = score_unit({"id": "U1", "scores": _scores(4)})
    assert r["verdict"] == "keep"
    assert r["total"] == 36


def test_keep_by_risk_override_below_total_threshold():
    # mostly 1s but risk_impact=5 and actionability=4 -> keep despite total < 32
    r = score_unit({"id": "U2", "scores": _scores(1, risk_impact=5, actionability=4)})
    assert r["verdict"] == "keep"
    assert r["total"] < 32


def test_keep_by_authority_override():
    r = score_unit({"id": "U3", "scores": _scores(1, authority=5, operational_fit=4)})
    assert r["verdict"] == "keep"


def test_discard_low_and_weak():
    # all 1s -> total 9 < 20, no strong dimension
    r = score_unit({"id": "U4", "scores": _scores(1)})
    assert r["verdict"] == "discard"


def test_review_band():
    # all 3s -> total 27, no keep rule, not a clear discard
    r = score_unit({"id": "U5", "scores": _scores(3)})
    assert r["verdict"] == "review"


def test_low_total_but_strong_is_review_not_discard():
    # total 12 (<20) but uniqueness=4 is "strong" -> review, not discard
    s = _scores(1, uniqueness=4)
    r = score_unit({"id": "U6", "scores": s})
    assert r["total"] < 20
    assert r["verdict"] == "review"


def test_importance_score_key_alias():
    r = score_unit({"id": "U7", "importance_score": _scores(4)})
    assert r["verdict"] == "keep"


def test_invalid_missing_dimension():
    s = _scores(4)
    del s["uniqueness"]
    r = score_unit({"id": "U8", "scores": s})
    assert r["verdict"] == "invalid"
    assert any("uniqueness" in e for e in r["errors"])


def test_invalid_out_of_range():
    r = score_unit({"id": "U9", "scores": _scores(4, authority=7)})
    assert r["verdict"] == "invalid"


def test_invalid_missing_scores_block():
    r = score_unit({"id": "U10"})
    assert r["verdict"] == "invalid"


def test_invalid_unknown_dimension():
    s = _scores(4)
    s["made_up"] = 3
    r = score_unit({"id": "U11", "scores": s})
    assert r["verdict"] == "invalid"


def test_score_units_buckets_and_validity():
    units = [
        {"id": "K", "scores": _scores(4)},
        {"id": "D", "scores": _scores(1)},
        {"id": "R", "scores": _scores(3)},
    ]
    result = score_units(units)
    assert result["summary"] == {"keep": 1, "review": 1, "discard": 1, "invalid": 0}
    assert result["valid"] is True
    assert result["kept"] == ["K"]


def test_score_units_file_and_worksheet(tmp_path=None):
    units = {"candidate_units": [{"id": "U1", "summary": "x", "scores": _scores(4)}]}
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False, encoding="utf-8") as f:
        yaml.safe_dump(units, f)
        path = f.name
    result = score_units_file(path)
    assert result["valid"]
    md = format_worksheet(result)
    assert "Importance-Scored Unit Shortlist" in md
    assert "U1" in md


def test_bare_list_input():
    units = [{"id": "U1", "scores": _scores(4)}]
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False, encoding="utf-8") as f:
        yaml.safe_dump(units, f)
        path = f.name
    result = score_units_file(path)
    assert result["summary"]["keep"] == 1
