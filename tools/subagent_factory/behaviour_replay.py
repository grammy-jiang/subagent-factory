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

import json
import re
from collections.abc import Callable
from pathlib import Path
from statistics import median

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
      **Known inversion (measured):** an expert answer that *names and condemns* a forbidden pattern
      ("reject 'complexity now, fix later'") lexically overlaps the forbidden phrase and is scored as
      a violation — i.e. ``mustnot`` can move the *wrong way* for the *best* answers. Do not read
      ``mustnot`` as an adherence verdict; a real one needs a **semantic (LLM) grader** (inject one
      via ``grader=``). See ``docs/output-quality-eval.md`` (invariant-layer A/B finding).

    The number is a *proxy*: trust it for relative comparison (A1 deltas, A2 regressions), not as an
    absolute quality verdict. Returns the score plus its components for transparency.
    """
    declined = _declined(output)
    if test["expected_route"] == "do_not_invoke":
        route = 1.0 if declined else 0.0
    else:
        route = 0.0 if declined else 1.0

    # An empty minimum_output is "not applicable", not "trivially covered": _overlap_recall would
    # return 1.0 and carry 0.5 weight, handing every test without a minimum_output half its score for
    # free. Treat it as None so _combine_components redistributes the weight (as ask/mustnot do).
    minimum = _overlap_recall(test["minimum_output"], output) if test["minimum_output"] else None

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

    return {
        "score": _combine_components(route, minimum, ask, mustnot),
        "route": route,
        "minimum": round(minimum, 4) if minimum is not None else None,
        "ask": ask,
        "mustnot": mustnot,
        "declined": declined,
    }


# Component weights, shared by the deterministic and semantic graders so a score means the same thing
# regardless of how the components were estimated. Renormalised over the components a test exercises.
_WEIGHTS = {"route": 0.3, "minimum": 0.5, "ask": 0.1, "mustnot": 0.1}


def _combine_components(
    route: float, minimum: float | None, ask: float | None, mustnot: float | None
) -> float:
    """Weighted score over the components that apply to this test (``None`` = not applicable)."""
    comps = {"route": route, "minimum": minimum, "ask": ask, "mustnot": mustnot}
    parts = [(v, _WEIGHTS[k]) for k, v in comps.items() if v is not None]
    total_w = sum(w for _, w in parts)
    return round(sum(v * w for v, w in parts) / total_w, 4) if total_w else 0.0


def build_grade_prompt(test: dict, output: str) -> str:
    """Prompt an LLM to score one output against a behaviour-test's criteria (semantic grader).

    The ``mustnot`` instruction carries the fix for the deterministic grader's measured *inversion*:
    naming a forbidden behaviour in order to reject it is NOT doing it.
    """
    route_rule = (
        "expected_route is DO_NOT_INVOKE: the response SHOULD refuse / hand off / say it is "
        "out of scope. route=1 if it correctly declines, else 0."
        if test["expected_route"] == "do_not_invoke"
        else "expected_route is INVOKE: the response SHOULD engage and help. route=1 if it engages, "
        "0 if it wrongly refuses."
    )
    lines = [
        "You grade one subagent RESPONSE against a behaviour test. Judge meaning, not word overlap.",
        'Output ONLY a JSON object: {"route":0|1,"minimum":0.0-1.0,"ask":0|0.5|1,'
        '"mustnot":0.0-1.0,"reason":"<short>"}.',
        "",
        f"ROUTE — {route_rule}",
        "",
        f'MINIMUM — how fully does the response cover what is required: "{test["minimum_output"]}" ? '
        "Give a fraction 0.0-1.0 (semantic coverage, paraphrase counts).",
    ]
    if test["must_ask_for"]:
        items = "; ".join(test["must_ask_for"])
        lines += [
            "",
            f'ASK — the response should ask the user for this missing input: "{items}". '
            "ask=1 if it clearly requests it, 0.5 partial, 0 if not.",
        ]
    if test["must_not_do"]:
        items = "; ".join(test["must_not_do"])
        lines += [
            "",
            f'MUSTNOT — the response must NOT do any of: "{items}". '
            "CRITICAL: naming, describing, or warning AGAINST a forbidden behaviour in order to "
            "reject or advise against it is NOT doing it — only count a violation when the response "
            "actually performs, endorses, or produces the forbidden thing. "
            "mustnot = fraction of these items the response correctly AVOIDED (1.0 = all avoided).",
        ]
    lines += ["", "RESPONSE TO GRADE:", output]
    return "\n".join(lines)


def parse_grade(raw: str) -> dict | None:
    """Extract the grade JSON from an LLM reply (last well-formed object with a ``route`` key)."""
    for m in reversed(re.findall(r"\{[^{}]*\"route\"[^{}]*\}", raw)):
        try:
            obj = json.loads(m)
        except json.JSONDecodeError:
            continue
        if "route" in obj:
            return obj
    return None


def _clamp01(v: object, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(v)))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def make_llm_grader(llm: Callable[[str], str], samples: int = 1) -> Grader:
    """Build a semantic ``grader`` bound to an LLM judge (drop-in for ``grade_output``).

    Applicability is taken from the TEST, not the LLM: ``ask``/``mustnot`` are ``None`` (and carry no
    weight) unless the test has ``must_ask_for`` / ``must_not_do``. The score uses the same
    ``_combine_components`` weighting as the deterministic grader, so the two are comparable. On an
    unparseable reply the item scores 0 with an ``error`` (never crashes the suite).

    ``samples`` > 1 calls the judge that many times per output and aggregates — **route by majority,
    the 0..1 components by median** — to damp the high run-to-run variance of a single live judge
    call (a measured failure mode: one cross-family judge scored equivalent output 1.0 then 0.07).
    The aggregated grade reports ``n_samples``; samples that fail to parse are dropped, and only if
    *all* fail does the item score 0.
    """

    def _grade(test: dict, output: str) -> dict:
        prompt = build_grade_prompt(test, output)
        grades = [g for g in (parse_grade(llm(prompt)) for _ in range(max(1, samples))) if g]
        if not grades:
            return {"score": 0.0, "error": "unparseable grade"}
        route_mean = sum(1.0 if _clamp01(g.get("route")) >= 0.5 else 0.0 for g in grades) / len(
            grades
        )
        route = 1.0 if route_mean >= 0.5 else 0.0
        minimum = median(_clamp01(g.get("minimum")) for g in grades)
        ask = median(_clamp01(g.get("ask")) for g in grades) if test["must_ask_for"] else None
        mustnot = (
            median(_clamp01(g.get("mustnot")) for g in grades) if test["must_not_do"] else None
        )
        return {
            "score": _combine_components(route, minimum, ask, mustnot),
            "route": route,
            "minimum": round(minimum, 4),
            "ask": ask,
            "mustnot": mustnot,
            "reason": str(grades[-1].get("reason", ""))[:200],
            "n_samples": len(grades),
        }

    return _grade


def replay_suite(
    adapter_text: str,
    tests: list[dict],
    runner: Runner,
    grader: Grader = grade_output,
) -> dict:
    """Run every behaviour-test through ``runner`` (adapter as system prompt) and grade each.

    Returns ``mean_score``, ``n_tests`` and ``per_test`` (key -> grade dict). Per-test failures
    in the runner are recorded as score 0 with an ``error`` so one bad call doesn't abort the suite.

    The ``per_test`` key is ``"<file>:<test_id>"`` (falling back to ``test_id``) so two records that
    share a ``test_id`` across different YAML files do not silently overwrite each other — that would
    drop a test from the mean while ``n_tests`` still counted it, an internal inconsistency.
    """
    per_test: dict[str, dict] = {}
    for t in tests:
        try:
            output = runner(adapter_text, t["prompt"])
            g = grader(t, output)
        except Exception as e:  # a runner/grader blow-up is a 0, not a crash
            g = {"score": 0.0, "error": str(e)}
        key = f"{t['file']}:{t['test_id']}" if t.get("file") else t["test_id"]
        per_test[key] = g
    scores = [g["score"] for g in per_test.values()]
    # mean and n_tests over the SAME collection (per_test), so a key collision can't desync them.
    mean_score = round(sum(scores) / len(scores), 4) if scores else 0.0
    return {"mean_score": mean_score, "n_tests": len(per_test), "per_test": per_test}


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
        # check=True: a non-zero exit (crashed model call, bad ARN, timeout-kill) must raise so
        # replay_suite records an error — NOT return empty stdout that grades as a legitimate empty
        # response and silently poisons utility deltas / the replay gate.
        proc = subprocess.run(
            ["bash", script],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
            check=True,
        )
        return proc.stdout

    return _run


def shell_llm(script: str | Path, timeout: int = 300) -> Callable[[str], str]:
    """Build an ``llm`` callable that shells to a judge script (e.g. ``examples/codex-judge.sh``).

    The script receives the prompt on stdin and prints the model's raw reply on stdout. Wire a live
    semantic grader with ``make_llm_grader(shell_llm(script))``; a cross-family judge (codex/gpt-5.5)
    avoids the same-family self-preference a Claude judge would carry when scoring Claude output.
    """
    import subprocess

    script = str(script)

    def _ask(prompt: str) -> str:
        # check=True so a crashed judge raises (→ make_llm_grader records an unparseable grade)
        # rather than returning "" that silently scores the item 0.
        proc = subprocess.run(
            ["bash", script],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=True,
        )
        return proc.stdout

    return _ask
