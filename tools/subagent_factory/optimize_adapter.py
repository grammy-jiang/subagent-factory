"""Step 12 — optimize-adapter: tune an adapter against the behaviour-test objective.

The budgeted ``propose → score → keep-winner`` loop (see ``docs/enhancement-steps/
step-12-optimize-adapter.md``). The research finding is that this is **not a novel mechanism** — the
A-track already ships every primitive, so this module is a *driver* over them:

- scorer = ``behaviour_replay.replay_suite``;
- assess-before-merge = the same rule as ``behaviour_replay.replay_gate`` (merge a variant iff it
  flips ≥1 fail→pass with **zero** pass→fail), inlined here so the current best is scored once per
  round instead of once per candidate (cost = eval calls, the thing to minimise);
- propose = an injectable ``Proposer`` (the LLM in production, a fake in tests);
- hard pre-merge gate = an injectable ``AcceptGate`` (faithfulness / quote / adapter-policy in
  production — the load-bearing anti-reward-hacking control; ``None`` = permissive, for the unit loop).

Cost levers (finding #5): a minibatch screen prefilters candidates before the full-suite confirm, the
loop has a closed budget, and a no-improvement early stop. A small beam ``pool`` (finding #6) keeps
per-test winners rather than always editing the current best. Everything is deterministic given the
injected runner/grader/proposer, so the loop is unit-tested without a live model.
"""

from __future__ import annotations

from collections.abc import Callable

from tools.subagent_factory.behaviour_replay import Grader, Runner, grade_output, replay_suite

# (best_adapter_text, failing_tests, round_index) -> candidate adapter texts.
# Each failing entry is {"test": <behaviour-test dict>, "grade": <grade dict>}.
Proposer = Callable[[str, list[dict], int], list[str]]

# candidate_adapter_text -> list of violation strings (empty = accept). The production gate runs
# faithfulness-review + quote-scan + adapter-policy-scan; a variant that over-claims is rejected here
# BEFORE it can score higher, no matter its behaviour-test score.
AcceptGate = Callable[[str], list[str]]


def _assess(before: dict, after: dict, tol: float) -> tuple[list[dict], list[dict]]:
    """Per-test regressions/improvements between two ``per_test`` maps (the replay_gate rule)."""
    regressions: list[dict] = []
    improvements: list[dict] = []
    for tid, bg in before.items():
        ag = after.get(tid, {"score": 0.0})
        delta = round(ag["score"] - bg["score"], 4)
        if delta < -tol:
            regressions.append({"test_id": tid, "before": bg["score"], "after": ag["score"]})
        elif delta > tol:
            improvements.append({"test_id": tid, "before": bg["score"], "after": ag["score"]})
    return regressions, improvements


def _mean_on(per_test: dict, ids: list[str]) -> float:
    scores = [per_test[i]["score"] for i in ids if i in per_test]
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def optimize_adapter(
    base_adapter: str,
    tests: list[dict],
    runner: Runner,
    proposer: Proposer,
    *,
    grader: Grader = grade_output,
    budget: int = 4,
    minibatch: int | None = None,
    pool_size: int = 4,
    patience: int = 2,
    pass_bar: float = 1.0,
    accept_gate: AcceptGate | None = None,
    tol: float = 0.0,
) -> dict:
    """Run the propose→score→keep loop; return the winner (≥ baseline) and a full trace.

    Each round: take the pool's best, collect its failing tests (score < ``pass_bar``), ask the
    ``proposer`` for candidate adapter texts, drop any the ``accept_gate`` rejects, screen survivors
    on a ``minibatch`` prefix, full-confirm the promising ones, and merge a candidate iff it improves
    the mean with **zero** per-test regressions (assess-before-merge). Stop at ``budget`` rounds or
    after ``patience`` rounds with no improvement.

    Returns ``winner_text``, ``winner_mean``, ``baseline_mean``, ``improved`` (bool), ``rounds_used``,
    ``eval_calls`` (runner invocations, for cost accounting), and ``history``.
    """
    all_ids = [t["test_id"] for t in tests]
    eval_calls = 0

    baseline = replay_suite(base_adapter, tests, runner, grader)
    eval_calls += len(tests)
    pool: list[dict] = [{"text": base_adapter, "result": baseline}]
    history: list[dict] = [{"round": 0, "source": "baseline", "mean": baseline["mean_score"]}]

    mb = minibatch or 0
    use_screen = 0 < mb < len(tests)
    screen_ids = all_ids[:mb] if use_screen else all_ids
    no_improve = 0
    rounds_used = 0

    for r in range(1, budget + 1):
        rounds_used = r
        best = max(pool, key=lambda p: p["result"]["mean_score"])
        prev_best_mean = best["result"]["mean_score"]
        best_screen_mean = _mean_on(best["result"]["per_test"], screen_ids)

        failing = [
            {"test": t, "grade": best["result"]["per_test"].get(t["test_id"], {})}
            for t in tests
            if best["result"]["per_test"].get(t["test_id"], {}).get("score", 0.0) < pass_bar
        ]
        candidates = proposer(best["text"], failing, r) or []

        for cand in candidates:
            if accept_gate is not None:
                violations = accept_gate(cand)
                if violations:
                    history.append({"round": r, "rejected": "pre-merge-gate", "why": violations})
                    continue

            if use_screen:
                screen = replay_suite(cand, tests[:mb], runner, grader)
                eval_calls += mb
                if screen["mean_score"] < best_screen_mean - tol:
                    history.append({"round": r, "rejected": "minibatch-screen"})
                    continue

            cand_result = replay_suite(cand, tests, runner, grader)
            eval_calls += len(tests)
            regressions, _ = _assess(best["result"]["per_test"], cand_result["per_test"], tol)
            if not regressions and cand_result["mean_score"] > best["result"]["mean_score"] + tol:
                pool.append({"text": cand, "result": cand_result})
            else:
                history.append(
                    {
                        "round": r,
                        "rejected": "replay-gate" if regressions else "no-gain",
                        "regressions": regressions,
                    }
                )

        pool = sorted(pool, key=lambda p: p["result"]["mean_score"], reverse=True)[:pool_size]
        new_best_mean = pool[0]["result"]["mean_score"]
        history.append({"round": r, "mean": new_best_mean, "pool_size": len(pool)})

        if new_best_mean > prev_best_mean + tol:
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= patience:
                break

    winner = max(pool, key=lambda p: p["result"]["mean_score"])
    return {
        "winner_text": winner["text"],
        "winner_mean": winner["result"]["mean_score"],
        "baseline_mean": baseline["mean_score"],
        "improved": winner["result"]["mean_score"] > baseline["mean_score"],
        "rounds_used": rounds_used,
        "eval_calls": eval_calls,
        "n_tests": len(tests),
        "history": history,
    }
