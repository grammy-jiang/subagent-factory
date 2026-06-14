"""Tests for Step-12 optimize-adapter driver (fakes only — no live model)."""

from tools.subagent_factory.optimize_adapter import optimize_adapter


def _test(tid, minimum):
    """A golden behaviour-test record in load_behaviour_tests shape."""
    return {
        "test_id": tid,
        "section": "golden_tests",
        "prompt": f"prompt-{tid}",
        "expected_route": "invoke",
        "expected_mode": None,
        "must_ask_for": [],
        "minimum_output": minimum,
        "must_not_do": [],
    }


# Runner returns the adapter text itself, so grade_output's `minimum` component = whether the adapter
# text contains the required tokens. An adapter "knows" a token iff the token is in its text.
def _runner(system: str, prompt: str) -> str:
    return system


TESTS2 = [_test("GT-001", "alpha"), _test("GT-002", "beta")]


def test_improving_variant_is_kept():
    # Baseline knows neither token; the proposed variant knows both → strictly better, no regression.
    def proposer(best_text, failing, rnd):
        return [best_text + " alpha beta"]

    res = optimize_adapter("base", TESTS2, _runner, proposer, budget=3, patience=1)
    assert res["baseline_mean"] < res["winner_mean"]
    assert res["improved"] is True
    assert "alpha" in res["winner_text"] and "beta" in res["winner_text"]


def test_regressing_variant_is_rejected():
    # Baseline already knows both; the variant drops 'beta' → one test regresses → gate rejects it.
    def proposer(best_text, failing, rnd):
        return ["base alpha zzz"]

    res = optimize_adapter("base alpha beta", TESTS2, _runner, proposer, budget=2, patience=1)
    assert res["improved"] is False
    assert res["winner_text"] == "base alpha beta"
    assert any(h.get("rejected") == "replay-gate" for h in res["history"])


def test_pre_merge_gate_rejects_before_scoring():
    # A high-scoring variant that fails the hard pre-merge gate (e.g. faithfulness) never lands.
    def proposer(best_text, failing, rnd):
        return ["base alpha beta OVERCLAIM"]

    def gate(text):
        return ["over-claim"] if "OVERCLAIM" in text else []

    res = optimize_adapter(
        "base", TESTS2, _runner, proposer, accept_gate=gate, budget=2, patience=1
    )
    assert res["improved"] is False
    assert any(h.get("rejected") == "pre-merge-gate" for h in res["history"])
    # Only the baseline suite was scored — the gated candidate cost zero eval calls.
    assert res["eval_calls"] == len(TESTS2)


def test_no_candidates_returns_baseline():
    res = optimize_adapter("base", TESTS2, _runner, lambda *_: [], budget=3, patience=1)
    assert res["improved"] is False
    assert res["winner_text"] == "base"
    assert res["rounds_used"] == 1  # early-stops after the first no-improvement round


def test_minibatch_screen_prefilters_cheaply():
    tests4 = [
        _test("GT-001", "alpha"),
        _test("GT-002", "beta"),
        _test("GT-003", "gamma"),
        _test("GT-004", "delta"),
    ]

    # Baseline is strong on the minibatch prefix (alpha,beta) but weak on the tail (gamma,delta).
    # The candidate trades the prefix for the tail → it loses on the minibatch screen and is dropped
    # before the expensive full-suite confirm.
    def proposer(best_text, failing, rnd):
        return ["base gamma delta"]

    res = optimize_adapter(
        "base alpha beta", tests4, _runner, proposer, minibatch=2, budget=2, patience=1
    )
    assert any(h.get("rejected") == "minibatch-screen" for h in res["history"])
    # Cost: baseline (4) + one minibatch screen (2) = 6; no full-confirm for the screened candidate.
    assert res["eval_calls"] == len(tests4) + 2


def test_early_stop_on_patience():
    # Proposer keeps offering the same already-best text → no improvement → patience stops the loop
    # well before the budget is exhausted.
    def proposer(best_text, failing, rnd):
        return ["base alpha beta"]

    res = optimize_adapter("base", TESTS2, _runner, proposer, budget=10, patience=2)
    assert res["rounds_used"] < 10
    assert res["improved"] is True


def test_result_shape():
    res = optimize_adapter("base", TESTS2, _runner, lambda *_: [], budget=1)
    for key in (
        "winner_text",
        "winner_mean",
        "baseline_mean",
        "improved",
        "rounds_used",
        "eval_calls",
        "n_tests",
        "history",
    ):
        assert key in res
