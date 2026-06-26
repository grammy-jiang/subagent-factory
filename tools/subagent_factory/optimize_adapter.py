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

import subprocess
import warnings
from collections.abc import Callable

from tools.subagent_factory.behaviour_replay import (
    Grader,
    Runner,
    grade_output,
    per_test_key,
    replay_suite,
)

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


def _merge_results(screen: dict, tail: dict) -> dict:
    """Combine a minibatch-screen result with a tail-only confirm into one full-suite result.

    The screen scored ``tests[:mb]`` and the tail scored ``tests[mb:]`` (disjoint), so their
    ``per_test`` maps union to the full suite. Mean and ``n_tests`` are recomputed over the merged
    map exactly as ``replay_suite`` does, so a merged result is indistinguishable from one produced
    by a single full ``replay_suite`` call — the screened+confirmed path stays behaviour-equivalent,
    it only avoids re-running the prefix tests.
    """
    per_test = {**screen["per_test"], **tail["per_test"]}
    # The slices are disjoint, so the union MUST have len(screen)+len(tail) entries. A shortfall means
    # two tests across the mb boundary collided on per_test_key (same "file:test_id", or two no-`file`
    # tests sharing a bare test_id): the union silently dropped one, shrinking n_tests and the mean
    # denominator while eval_calls still counts len(tests) — the exact n_tests/score desync per_test_key
    # exists to prevent. Fail loud instead of corrupting the gate's numbers.
    expected = len(screen["per_test"]) + len(tail["per_test"])
    if len(per_test) != expected:
        raise ValueError(
            f"merge-seam per_test_key collision: screen+tail = {expected} disjoint tests but merged "
            f"map has {len(per_test)} — a key collides across the minibatch boundary"
        )
    scores = [g["score"] for g in per_test.values()]
    mean_score = round(sum(scores) / len(scores), 4) if scores else 0.0
    return {"mean_score": mean_score, "n_tests": len(per_test), "per_test": per_test}


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
    all_ids = [per_test_key(t) for t in tests]
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
        best = min(pool, key=lambda p: (-p["result"]["mean_score"], p["text"]))
        prev_best_mean = best["result"]["mean_score"]
        best_screen_mean = _mean_on(best["result"]["per_test"], screen_ids)

        failing = [
            {"test": t, "grade": best["result"]["per_test"].get(per_test_key(t), {})}
            for t in tests
            if best["result"]["per_test"].get(per_test_key(t), {}).get("score", 0.0) < pass_bar
        ]
        try:
            candidates = proposer(best["text"], failing, r) or []
        except subprocess.SubprocessError as e:
            # The shell-backed proposer raises (check=True) on a crashed/timed-out model call. That is
            # infra failure, not "no candidate this round" — skip the round (best-so-far is still
            # returned) instead of aborting the whole optimization, and surface it. A non-subprocess
            # error (a real bug in an injected proposer) still propagates.
            warnings.warn(
                f"proposer failed in round {r} ({type(e).__name__}: {e}); skipping round",
                RuntimeWarning,
                stacklevel=2,
            )
            history.append({"round": r, "error": "proposer-failed", "detail": str(e)})
            candidates = []

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
                # Confirmed past the screen: score only the UNSEEN tail and reuse the screen's
                # per_test for the prefix, instead of re-running the prefix (the whole point of
                # screening is to NOT pay for the same tests twice).
                tail = replay_suite(cand, tests[mb:], runner, grader)
                eval_calls += len(tests) - mb
                cand_result = _merge_results(screen, tail)
            else:
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

        # Stable secondary key so equal-mean candidates order deterministically by text (not by
        # emission/list order). Sort ascending by text first, then stable-sort by mean descending →
        # higher mean wins, ties resolve to the lexicographically smaller text at pool[0].
        pool = sorted(pool, key=lambda p: p["text"])
        pool = sorted(pool, key=lambda p: p["result"]["mean_score"], reverse=True)[:pool_size]
        new_best_mean = pool[0]["result"]["mean_score"]
        history.append({"round": r, "mean": new_best_mean, "pool_size": len(pool)})

        if new_best_mean > prev_best_mean + tol:
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= patience:
                break

    winner = min(pool, key=lambda p: (-p["result"]["mean_score"], p["text"]))
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


def optimize_adapter_with_shell_proposer(
    base_text: str,
    tests: list[dict],
    runner: Runner,
    proposer_script: str,
    *,
    grader: Grader = grade_output,
    n_variants: int = 2,
    budget: int = 4,
    minibatch: int | None = None,
    pool_size: int = 4,
    patience: int = 2,
    tol: float = 0.0,
    proposer_timeout: int = 300,
) -> dict:
    """Façade for the CLI: run the optimize loop with the live shell-backed proposer + policy gate.

    Wraps the three pieces the CLI used to wire by hand — ``shell_proposer(proposer_script)``,
    ``make_policy_gate(base_text)``, and ``optimize_adapter(...)`` — into one call so the CLI stops
    reaching into module internals. Optimization behaviour is unchanged: it passes the same
    arguments through, with the policy gate always installed (as the live path always did).
    """
    return optimize_adapter(
        base_text,
        tests,
        runner,
        shell_proposer(proposer_script, n_variants=n_variants, timeout=proposer_timeout),
        grader=grader,
        budget=budget,
        minibatch=minibatch,
        pool_size=pool_size,
        patience=patience,
        tol=tol,
        accept_gate=make_policy_gate(base_text),
    )


# ── live wiring (D8): a shell-backed proposer + a text-level policy gate ─────────
#
# The live CLI uses these to run the loop against a real package with a real model. The proposer is
# *additive* in v1: the model emits short guidance blocks to APPEND (cheap + safe — it cannot rewrite
# or delete existing rules), and the driver scores base+block. Full-rewrite proposing is supported by
# the driver (it takes full texts) but is deferred for the live path (token cost + truncation risk).

_VARIANT_DELIM = "===VARIANT==="

# Tokens that must never appear in proposer-added text (instruction-injection / authority widening).
_ESCALATION_TOKENS = (
    "ignore previous",
    "ignore all previous",
    "disregard",
    "--dangerously-skip-permissions",
    "allowed-tools:",
    "bypass",
    "override the system",
)


def build_propose_prompt(best_text: str, failing: list[dict], n_variants: int) -> str:
    """Build the LLM proposer prompt: the failing tests + the additive, faithfulness-bound contract."""
    lines = [
        f"You improve a subagent by proposing {n_variants} ADDITIVE guidance blocks.",
        "The current adapter is your system prompt. It is FAILING the behaviour-tests below.",
        "Propose short blocks (a sharpened rule or a worked example) to APPEND to the adapter so it",
        "passes them — WITHOUT regressing anything it already does.",
        "",
        "HARD RULES:",
        "- Output ONLY the new blocks. Do not restate or rewrite the existing adapter.",
        f"- Begin EACH block with a line containing exactly: {_VARIANT_DELIM}",
        "- Make the blocks DIFFERENT from each other (vary the fix, not three near-identical edits).",
        "- Never claim anything the adapter's source does not support (a faithfulness gate will",
        "  reject an over-claim no matter its test score). Keep blocks human-readable.",
        "- Do not add tool grants, permissions, or instructions to ignore/override anything.",
        "",
        "FAILING BEHAVIOUR-TESTS:",
    ]
    for f in failing[:6]:
        t = f.get("test", {})
        g = f.get("grade", {})
        why = g.get("reason") or _why_failed(g)
        lines += [
            f"- [{t.get('test_id', '?')}] route={t.get('expected_route', 'invoke')} "
            f"score={g.get('score', 0)}",
            f"  prompt: {str(t.get('prompt', ''))[:240]}",
            f"  required: {str(t.get('minimum_output', ''))[:240]}"
            if t.get("minimum_output")
            else "",
            f"  weakness: {why}" if why else "",
        ]
    return "\n".join(line for line in lines if line != "")


def _why_failed(grade: dict) -> str:
    """Terse weakness summary from a deterministic grade's components."""
    bits = []
    if grade.get("route") == 0.0:
        bits.append("wrong route (engaged/declined incorrectly)")
    if isinstance(grade.get("minimum"), (int, float)) and grade["minimum"] < 0.5:
        bits.append("missed required content")
    if grade.get("ask") == 0.0:
        bits.append("did not ask for missing context")
    if isinstance(grade.get("mustnot"), (int, float)) and grade["mustnot"] < 1.0:
        bits.append("did a forbidden thing")
    return "; ".join(bits)


def parse_variants(raw: str, best_text: str, max_variants: int | None = None) -> list[str]:
    """Split a proposer reply into full candidate adapter texts (base + each additive block)."""
    if _VARIANT_DELIM in raw:
        chunks = raw.split(_VARIANT_DELIM)[1:]  # drop any preamble before the first delimiter
    else:
        chunks = [raw]
    blocks = [c.strip() for c in chunks if c.strip()]
    if max_variants is not None:
        blocks = blocks[:max_variants]
    base = best_text.rstrip()
    return [base + "\n\n" + b for b in blocks]


def shell_proposer(script: str, n_variants: int = 2, timeout: int = 300) -> Proposer:
    """Build a live ``Proposer`` that shells to a script (e.g. ``examples/optimize-proposer.sh``).

    The script receives the best adapter text in env ``ADAPTER_TEXT`` and the proposer prompt on
    stdin, and prints ``===VARIANT===``-delimited additive blocks on stdout.
    """
    import os
    import subprocess

    def _propose(best_text: str, failing: list[dict], round_idx: int) -> list[str]:
        prompt = build_propose_prompt(best_text, failing, n_variants)
        env = {**os.environ, "ADAPTER_TEXT": best_text}
        # check=True: a crashed proposer must raise, not return "" that parse_variants reads as
        # "no variants" — silently treating an infra failure as "no improvement found".
        out = subprocess.run(
            ["bash", script],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
            check=True,
        ).stdout
        return parse_variants(out, best_text, max_variants=n_variants)

    return _propose


def make_policy_gate(base_text: str) -> AcceptGate:
    """A text-level pre-merge gate: reject a candidate that widens tool grants or adds escalation text.

    Lightweight v1 backstop for the live loop (the full faithfulness + quote + adapter-policy scan
    runs when the human folds the winning edits into ``profile.yaml`` and re-exports). Assumes the
    additive proposer, so it scans the text added beyond the baseline.
    """
    from tools.subagent_factory.adapter_policy_scan import granted_tools

    base = base_text.rstrip()
    base_tools = granted_tools(base_text)

    def _gate(cand: str) -> list[str]:
        violations: list[str] = []
        if not granted_tools(cand) <= base_tools:
            violations.append("widens tool grants")
        added = (cand[len(base) :] if cand.startswith(base) else cand).lower()
        for tok in _ESCALATION_TOKENS:
            if tok in added:
                violations.append(f"escalation token in added text: {tok!r}")
        return violations

    return _gate
