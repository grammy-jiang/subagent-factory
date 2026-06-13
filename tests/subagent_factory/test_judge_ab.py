"""Tests for the pairwise A/B judging harness (Phase 10) — deterministic via mock judges."""

from tools.subagent_factory.judge_ab import build_judge_prompt, parse_winner, run_ab


def _content_judge(prompt: str) -> str:
    """Mock judge: picks whichever review block contains 'EXCELLENT' (content, not position)."""
    r1 = prompt.split("REVIEW Review-1:")[1].split("REVIEW Review-2:")[0]
    win = "Review-1" if "EXCELLENT" in r1 else "Review-2"
    return f'{{"winner": "{win}", "reason": "content"}}'


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
