"""Tests for the pairwise A/B judging harness (Phase 10) — deterministic via mock judges."""

from tools.subagent_factory.judge_ab import (
    build_judge_prompt,
    parse_winner,
    run_ab,
    run_ab_ensemble,
)


def _content_judge(prompt: str) -> str:
    """Mock judge: picks whichever review block contains 'EXCELLENT' (content, not position)."""
    r1 = prompt.split("REVIEW Review-1:")[1].split("REVIEW Review-2:")[0]
    win = "Review-1" if "EXCELLENT" in r1 else "Review-2"
    return f'{{"winner": "{win}", "reason": "content"}}'


def _content_loser_judge(prompt: str) -> str:
    """Adversarial mock: picks the block WITHOUT 'EXCELLENT' (disagrees with _content_judge)."""
    r1 = prompt.split("REVIEW Review-1:")[1].split("REVIEW Review-2:")[0]
    win = "Review-2" if "EXCELLENT" in r1 else "Review-1"
    return f'{{"winner": "{win}"}}'


def _position1_judge(prompt: str) -> str:
    return '{"winner": "Review-1", "reason": "always first"}'


def test_parse_winner_variants():
    assert parse_winner('{"winner": "Review-1"}') == "Review-1"
    assert parse_winner('preamble\n{"winner": "Review-2", "reason": "x"}') == "Review-2"
    assert parse_winner("no json here") is None


def test_build_prompt_anonymizes_with_labels():
    p = build_judge_prompt("Review-1", "alpha body", "Review-2", "beta body")
    assert "REVIEW Review-1:" in p and "alpha body" in p and "beta body" in p


def test_better_version_wins_regardless_of_position():
    r = run_ab("A", "EXCELLENT sharp findings", "B", "vague filler", _content_judge, passes=6)
    rk = r["ranking"]
    assert rk["ranking"][0]["version"] == "A"
    assert rk["top2_separated"] is True
    assert r["n_decided"] == 6


def test_position_bias_cancelled_by_swapping():
    # a judge that always picks position 1 should NOT yield a separated winner once swapped.
    r = run_ab("A", "ta", "B", "tb", _position1_judge, passes=6)
    assert r["ranking"]["top2_separated"] is False


def test_unparseable_verdicts_skipped():
    r = run_ab("A", "ta", "B", "tb", lambda _p: "garbage no json", passes=4)
    assert r["n_decided"] == 0 and r["ranking"]["ranking"] == []


def test_ensemble_unanimous_is_stable():
    r = run_ab_ensemble("A", "EXCELLENT findings", "B", "vague", [_content_judge] * 3, passes=6)
    assert r["mean_judge_agreement"] == 1.0 and r["stable"] is True
    assert r["ranking"]["ranking"][0]["version"] == "A"


def test_ensemble_majority_with_partial_agreement():
    judges = [_content_judge, _content_judge, _content_loser_judge]  # 2 say A, 1 says B
    r = run_ab_ensemble("A", "EXCELLENT", "B", "vague", judges, passes=4)
    assert 0.5 < r["mean_judge_agreement"] < 1.0  # ~0.667
    assert r["ranking"]["ranking"][0]["version"] == "A"  # majority still A


def test_ensemble_fully_split_is_unstable():
    judges = [_content_judge, _content_loser_judge]  # 1-1 every pass
    r = run_ab_ensemble("A", "EXCELLENT", "B", "vague", judges, passes=4)
    assert r["mean_judge_agreement"] == 0.5 and r["stable"] is False
