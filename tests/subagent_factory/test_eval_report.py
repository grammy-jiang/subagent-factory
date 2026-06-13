"""Tests for the consolidated eval report's deterministic assembly (Phase 10 #1)."""

from tools.subagent_factory.eval_report import assemble, cost_stats, parity_flag


def test_cost_stats():
    s = cost_stats("a\nb\nc")
    assert s["lines"] == 3 and s["chars"] == 5


def test_parity_flag_none_when_similar():
    assert parity_flag({"A": {"lines": 100}, "B": {"lines": 110}}) is None


def test_parity_flag_set_when_disparate():
    assert parity_flag({"A": {"lines": 100}, "B": {"lines": 220}}) is not None


def test_assemble_separated_verdict():
    ab = {
        "ranking": {
            "ranking": [{"version": "B", "strength": 0.8}, {"version": "A", "strength": 0.2}],
            "top2_separated": True,
        },
        "n_decided": 20,
        "passes": 20,
    }
    grounding = {
        "A": {"coverage": 0.2, "cross_source_terms": [1, 2]},
        "B": {"coverage": 0.3, "cross_source_terms": []},
    }
    r = assemble(ab, grounding, {"A": {"lines": 100}, "B": {"lines": 110}})
    assert r["advice_quality"]["separated"] is True
    assert "B (separated)" in r["verdict"]
    assert r["grounding"]["A"]["cross_source_borrows"] == 2
    assert r["parity_flag"] is None


def test_assemble_inconclusive_with_parity_flag():
    ab = {
        "ranking": {
            "ranking": [{"version": "B"}, {"version": "A"}],
            "top2_separated": False,
        },
        "n_decided": 6,
        "passes": 6,
    }
    r = assemble(ab, {"A": {}, "B": {}}, {"A": {"lines": 100}, "B": {"lines": 220}})
    assert "inconclusive" in r["verdict"]
    assert r["parity_flag"] is not None
