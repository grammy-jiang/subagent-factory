"""Tests for judge↔gold agreement (Phase 10 B4)."""

from tools.subagent_factory.gold_eval import cohens_kappa, judge_vs_gold, load_gold


def test_kappa_perfect_agreement():
    assert cohens_kappa(["A", "B", "A", "B"], ["A", "B", "A", "B"]) == 1.0


def test_kappa_total_disagreement_is_negative():
    assert cohens_kappa(["A", "A", "B", "B"], ["B", "B", "A", "A"]) < 0


def test_kappa_empty():
    assert cohens_kappa([], []) == 0.0


def test_judge_vs_gold_perfect_is_trusted():
    judge = {"i1": "A", "i2": "B", "i3": "A", "i4": "B"}
    gold = {"i1": "A", "i2": "B", "i3": "A", "i4": "B"}
    r = judge_vs_gold(judge, gold)
    assert r["n_overlap"] == 4 and r["cohens_kappa"] == 1.0
    assert r["trust_judge"] is True and r["interpretation"] == "almost-perfect"


def test_judge_vs_gold_chance_not_trusted():
    judge = {"i1": "A", "i2": "A", "i3": "A", "i4": "A"}  # judge always A
    gold = {"i1": "A", "i2": "B", "i3": "A", "i4": "B"}  # gold 50/50
    r = judge_vs_gold(judge, gold)
    assert r["trust_judge"] is False  # kappa ~0


def test_judge_vs_gold_overlap_only():
    judge = {"i1": "A", "i2": "B", "extra": "A"}
    gold = {"i1": "A", "i2": "B", "other": "B"}
    assert judge_vs_gold(judge, gold)["n_overlap"] == 2


def test_load_gold(tmp_path):
    f = tmp_path / "gold.jsonl"
    f.write_text(
        '{"item": "i1", "winner": "A", "annotator": "h"}\n\n{"item": "i2", "winner": "B"}\n',
        encoding="utf-8",
    )
    assert load_gold(str(f)) == {"i1": "A", "i2": "B"}
