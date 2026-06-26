"""Tests for the recall-then-filter REDUCE (P3); fake embedder keeps MiniLM out of the suite."""

from tools.subagent_factory.reduce_principles import (
    _cosine,
    apply_decisions,
    merge_group,
    recall_clusters,
    select_top,
)


def _fake_embedder(stmts):
    vocab = sorted({w for s in stmts for w in s.split()})
    return [[1.0 if w in s.split() else 0.0 for w in vocab] for s in stmts]


def test_cosine_basics():
    assert _cosine([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert _cosine([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_recall_clusters_groups_similar():
    ps = [
        {"statement": "cache invalidation hard"},
        {"statement": "cache invalidation hard tricky"},
        {"statement": "event driven messaging bus"},
    ]
    groups = recall_clusters(ps, _fake_embedder, cos=0.5)
    assert sorted(len(g) for g in groups) == [1, 2]  # first two cluster, third stands alone


def test_merge_group_unions_and_picks_longest():
    ps = [
        {
            "statement": "a",
            "source_id": "s1",
            "derived_from_claims": ["C1"],
            "confidence": "medium",
            "applies_when": ["x"],
        },
        {
            "statement": "aa longer",
            "source_id": "s2",
            "derived_from_claims": ["C2"],
            "confidence": "high",
            "applies_when": ["y"],
        },
    ]
    m = merge_group(ps, [0, 1])
    assert m["n_sources"] == 2
    assert m["derived_from_claims"] == ["C1", "C2"]
    assert m["confidence"] == "high"
    assert m["statement"] == "aa longer"


def test_apply_decisions_confirm_split_conflict():
    ps = [{"statement": f"p{i}", "source_id": f"s{i}", "derived_from_claims": []} for i in range(3)]
    groups = [[0, 1, 2]]
    assert len(apply_decisions(ps, groups, {0: {"action": "confirm"}})) == 1
    assert (
        len(apply_decisions(ps, groups, {0: {"action": "split", "subgroups": [[0], [1, 2]]}})) == 2
    )
    assert len(apply_decisions(ps, groups, {0: {"action": "conflict"}})) == 3


def test_select_top_by_importance():
    a = {"n_sources": 3, "derived_from_claims": ["C1"], "confidence": "high"}
    b = {"n_sources": 1, "derived_from_claims": [], "confidence": "low"}
    assert select_top([b, a], 1) == [a]


def test_select_top_fraction_keeps_top_fraction():
    # 0<limit<1 keeps that FRACTION (rounded, min 1) of the importance-ranked pool. This path is
    # only reachable from the CLI once --select is type=float (was type=int, which truncated it).
    ps = [{"n_sources": n, "derived_from_claims": [], "confidence": "low"} for n in range(1, 5)]
    kept = select_top(ps, 0.5)  # 4 principles -> top half = 2
    assert [p["n_sources"] for p in kept] == [4, 3]


def test_select_top_fraction_rounds_to_min_one():
    ps = [{"n_sources": n, "derived_from_claims": [], "confidence": "low"} for n in range(1, 4)]
    # 3 * 0.1 = 0.3 -> round -> 0, floored to min 1.
    assert len(select_top(ps, 0.1)) == 1
