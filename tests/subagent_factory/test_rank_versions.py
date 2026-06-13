"""Tests for the deterministic version-ranking tool (Phase 10: BT + bootstrap CI)."""

from tools.subagent_factory.rank_versions import bradley_terry, rank_versions


def _pairs(seq):
    return [{"winner": w, "loser": lo} for w, lo in seq]


def test_clear_winner_is_separated(tmp_path=None):
    r = rank_versions(_pairs([("A", "B")] * 12), n_boot=300, seed=0)
    assert r["ranking"][0]["version"] == "A"
    assert r["top2_separated"] is True


def test_close_contest_not_separated():
    r = rank_versions(_pairs([("A", "B")] * 6 + [("B", "A")] * 5), n_boot=300, seed=0)
    assert r["top2_separated"] is False  # overlapping CIs → not a reliable win


def test_transitive_ordering():
    r = rank_versions(
        _pairs([("A", "B")] * 8 + [("B", "C")] * 8 + [("A", "C")] * 8), n_boot=200, seed=0
    )
    assert [x["version"] for x in r["ranking"]] == ["A", "B", "C"]


def test_deterministic_under_seed():
    pairs = _pairs([("A", "B")] * 7 + [("B", "A")] * 3)
    assert rank_versions(pairs, n_boot=200, seed=1) == rank_versions(pairs, n_boot=200, seed=1)


def test_empty_outcomes():
    r = rank_versions([])
    assert r["ranking"] == [] and r["top2_separated"] is False


def test_bradley_terry_orders_by_strength():
    p = bradley_terry([("A", "B")] * 5 + [("B", "C")] * 5)
    assert p["A"] > p["C"]
