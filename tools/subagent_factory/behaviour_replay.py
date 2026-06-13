"""Behaviour-test replay engine (Phase 5/9 — instruction-induction A1 + A2).

``run_tests`` validates that behaviour-test *records* are well-formed (structural, no model).
This module is the complementary **execution** path: actually run a candidate adapter against the
package's behaviour-tests and score the result, so adapter changes can be selected and gated by
*measured behaviour* instead of by similarity or by eye.

Two research items lean on one engine:

- **A1 — example selection by utility.** When choosing which worked examples to put in an adapter,
  prefer the ones that *measurably raise* the behaviour-test score, not the ones an embedding
  thinks are similar. ``rank_examples_by_utility`` scores ``base`` vs ``base + candidate`` and
  ranks candidates by the marginal delta.
- **A2 — replay gate (SkillCAT assess-before-merge).** Before merging a generated rule/example,
  re-run the behaviour-tests; reject the change if it regresses any test that previously passed.
  ``replay_gate`` compares a before/after adapter and FAILs on any per-test regression.

Two things are injected so the orchestration is deterministic and unit-testable (the same pattern
as ``judge_ab``):

- ``runner: Callable[[system, prompt], output]`` — runs the adapter (as system prompt) on a test
  prompt and returns the model's text. Real impl shells out to ``examples/replay-runner.sh``
  (``claude -p``); tests pass a fake.
- ``grader: Callable[[test, output], dict]`` — scores one output against one behaviour-test record.
  The default ``grade_output`` is a **coarse deterministic proxy**: its value is *relative
  consistency* (so utility-deltas and regressions are meaningful), not absolute truth. Swap in an
  LLM grader for production-grade absolute scoring.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _content_tokens

# Sections of a tests/*.yaml that hold behaviour-test records (mirrors run_tests).
_TEST_SECTIONS = ("golden_tests", "negative_routing_tests", "missing_context_tests")

# Phrases that signal the agent declined / handed off (route = do_not_invoke is supposed to;
# route = invoke is not). Lower-cased substring match.
_DECLINE_MARKERS = (
    "outside scope",
    "out of scope",
    "out of my scope",
    "outside my scope",
    "beyond my scope",
    "beyond the scope",
    "not the right",
    "not something i",
    "isn't something i",
    "not in scope",
    "hand off",
    "handoff",
    "hand this off",
    "decline",
    "i can't help with",
    "i cannot help with",
    "won't produce",
    "will not produce",
    "do not produce",
)
# A long answer that merely *mentions* scope is still an engagement; only a short, decline-dominated
# reply counts as an actual decline.
_DECLINE_MAX_CHARS = 600

Runner = Callable[[str, str], str]
Grader = Callable[[dict, str], dict]


def load_behaviour_tests(subagent_dir: str | Path) -> list[dict]:
    """Flatten every ``tests/*.yaml`` record into uniform behaviour-test dicts.

    Each record: ``test_id, section, prompt, expected_route, expected_mode, must_ask_for (list),
    minimum_output (str), must_not_do (list)``. Records without a prompt are skipped (nothing to
    replay).
    """
    base = Path(subagent_dir)
    tests_dir = base / "tests"
    out: list[dict] = []
    if not tests_dir.exists():
        return out
    for tf in sorted(tests_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        for section in _TEST_SECTIONS:
            for rec in data.get(section, []) or []:
                if not isinstance(rec, dict) or not rec.get("prompt"):
                    continue
                out.append(
                    {
                        "test_id": str(rec.get("test_id", f"T{len(out) + 1:03d}")),
                        "section": section,
                        "prompt": str(rec.get("prompt", "")),
                        "expected_route": str(rec.get("expected_route", "invoke")),
                        "expected_mode": rec.get("expected_mode"),
                        "must_ask_for": [str(x) for x in (rec.get("must_ask_for") or [])],
                        "minimum_output": str(rec.get("minimum_output", "")),
                        "must_not_do": [str(x) for x in (rec.get("must_not_do") or [])],
                        "file": tf.name,
                    }
                )
    return out


def _declined(output: str) -> bool:
    low = output.lower()
    return len(output.strip()) < _DECLINE_MAX_CHARS and any(m in low for m in _DECLINE_MARKERS)


def _overlap_recall(reference: str, output: str) -> float:
    """Fraction of reference content tokens present in the output (0..1)."""
    ref = _content_tokens(reference)
    if not ref:
        return 1.0  # nothing required → trivially covered
    return len(ref & _content_tokens(output)) / len(ref)


def grade_output(test: dict, output: str) -> dict:
    """Coarse deterministic score (0..1) of one output against one behaviour-test record.

    Components (weighted, then renormalised over the ones that apply to this test):
    - ``route`` (0.3): did it engage vs decline as the expected_route demands.
    - ``minimum`` (0.5): content-token recall of ``minimum_output`` (did it cover what's required).
    - ``ask`` (0.1, only if ``must_ask_for``): asked a question that overlaps the required ask.
    - ``mustnot`` (0.1): heuristic — penalise outputs whose tokens strongly overlap a forbidden
      item. Deterministic "did NOT do X" detection is unreliable; this is a weak signal, low weight.

    The number is a *proxy*: trust it for relative comparison (A1 deltas, A2 regressions), not as an
    absolute quality verdict. Returns the score plus its components for transparency.
    """
    declined = _declined(output)
    if test["expected_route"] == "do_not_invoke":
        route = 1.0 if declined else 0.0
    else:
        route = 0.0 if declined else 1.0

    minimum = _overlap_recall(test["minimum_output"], output)

    ask_applicable = bool(test["must_ask_for"])
    if ask_applicable:
        asked = "?" in output
        ask_cov = max((_overlap_recall(a, output) for a in test["must_ask_for"]), default=0.0)
        ask = 1.0 if (asked and ask_cov >= 0.5) else (0.5 if asked or ask_cov >= 0.5 else 0.0)
    else:
        ask = None

    if test["must_not_do"]:
        violated = sum(1 for f in test["must_not_do"] if _overlap_recall(f, output) >= 0.6)
        mustnot = 1.0 - violated / len(test["must_not_do"])
    else:
        mustnot = None

    parts = [("route", route, 0.3), ("minimum", minimum, 0.5)]
    if ask is not None:
        parts.append(("ask", ask, 0.1))
    if mustnot is not None:
        parts.append(("mustnot", mustnot, 0.1))
    total_w = sum(w for _, _, w in parts)
    score = sum(v * w for _, v, w in parts) / total_w if total_w else 0.0

    return {
        "score": round(score, 4),
        "route": route,
        "minimum": round(minimum, 4),
        "ask": ask,
        "mustnot": mustnot,
        "declined": declined,
    }


def replay_suite(
    adapter_text: str,
    tests: list[dict],
    runner: Runner,
    grader: Grader = grade_output,
) -> dict:
    """Run every behaviour-test through ``runner`` (adapter as system prompt) and grade each.

    Returns ``mean_score``, ``n_tests`` and ``per_test`` (test_id -> grade dict). Per-test failures
    in the runner are recorded as score 0 with an ``error`` so one bad call doesn't abort the suite.
    """
    per_test: dict[str, dict] = {}
    for t in tests:
        try:
            output = runner(adapter_text, t["prompt"])
            g = grader(t, output)
        except Exception as e:  # a runner/grader blow-up is a 0, not a crash
            g = {"score": 0.0, "error": str(e)}
        per_test[t["test_id"]] = g
    scores = [g["score"] for g in per_test.values()]
    mean_score = round(sum(scores) / len(scores), 4) if scores else 0.0
    return {"mean_score": mean_score, "n_tests": len(tests), "per_test": per_test}


def rank_examples_by_utility(
    base_adapter: str,
    candidates: list[dict],
    tests: list[dict],
    runner: Runner,
    grader: Grader = grade_output,
) -> dict:
    """A1: rank candidate examples by *measured* marginal utility, not similarity.

    ``candidates`` is a list of ``{"id": str, "text": str}`` example blocks. Each is appended to the
    base adapter and re-scored; ``utility = score(base + candidate) - score(base)``. The ranking is
    by utility descending — pick the top-k for the adapter. A non-positive utility means the example
    does not measurably improve behaviour and should not be added on a similarity hunch.
    """
    base = replay_suite(base_adapter, tests, runner, grader)
    base_mean = base["mean_score"]
    ranked: list[dict] = []
    for c in candidates:
        aug = base_adapter.rstrip() + "\n\n" + c["text"]
        s = replay_suite(aug, tests, runner, grader)
        ranked.append(
            {
                "id": c["id"],
                "utility": round(s["mean_score"] - base_mean, 4),
                "augmented_mean": s["mean_score"],
            }
        )
    ranked.sort(key=lambda r: r["utility"], reverse=True)
    return {"base_mean": base_mean, "n_tests": base["n_tests"], "ranked": ranked}


def replay_gate(
    before_adapter: str,
    after_adapter: str,
    tests: list[dict],
    runner: Runner,
    grader: Grader = grade_output,
    tol: float = 0.0,
) -> dict:
    """A2: SkillCAT assess-before-merge gate. FAIL if the change regresses any behaviour-test.

    Scores ``before`` and ``after``, then per test: a **regression** is ``after < before - tol`` and
    an **improvement** is ``after > before + tol``. The gate is ``fail`` if any regression exists
    (a change must not trade a passing behaviour for a new one), else ``pass``. ``net_delta`` reports
    the mean change for context.
    """
    b = replay_suite(before_adapter, tests, runner, grader)
    a = replay_suite(after_adapter, tests, runner, grader)
    regressions: list[dict] = []
    improvements: list[dict] = []
    for tid, bg in b["per_test"].items():
        ag = a["per_test"].get(tid, {"score": 0.0})
        delta = round(ag["score"] - bg["score"], 4)
        if delta < -tol:
            regressions.append({"test_id": tid, "before": bg["score"], "after": ag["score"]})
        elif delta > tol:
            improvements.append({"test_id": tid, "before": bg["score"], "after": ag["score"]})
    return {
        "gate": "fail" if regressions else "pass",
        "before_mean": b["mean_score"],
        "after_mean": a["mean_score"],
        "net_delta": round(a["mean_score"] - b["mean_score"], 4),
        "regressions": regressions,
        "improvements": improvements,
        "n_tests": b["n_tests"],
    }


def shell_runner(script: str | Path, timeout: int = 300) -> Runner:
    """Build a real ``runner`` that shells out to a script (e.g. ``examples/replay-runner.sh``).

    The script receives the adapter/system text in env ``ADAPTER_TEXT`` and the user prompt on
    stdin, and prints the model's response on stdout. Used by the CLI for live replay; tests use a
    fake runner instead.
    """
    import os
    import subprocess

    script = str(script)

    def _run(system: str, prompt: str) -> str:
        env = {**os.environ, "ADAPTER_TEXT": system}
        return subprocess.run(
            ["bash", script],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        ).stdout

    return _run
