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
import os
import re
import subprocess
import warnings
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

# Two-axis `must_ask_for` scoring (Step-13): reward ONE specific clarification question, cap the
# reward when the output over-asks. Up to this many question marks reads as a focused ask; beyond it
# is a barrage (over-asking hurts and is nonmonotonic — calibration finding #5).
_MAX_ASK_QUESTIONS = 2

# Token-overlap cutoffs (not score values): a clarification question counts as "covered" at or above
# _ASK_COVER_MIN recall of a must_ask_for item; a must_not_do item counts as "violated" at or above
# _MUSTNOT_OVERLAP_MIN recall. Both are heuristic thresholds, distinct from the partial-credit scores.
_ASK_COVER_MIN = 0.5
_MUSTNOT_OVERLAP_MIN = 0.6

Runner = Callable[[str, str], str]
Grader = Callable[[dict, str], dict]


def per_test_key(test: dict) -> str:
    """The single source of truth for a test's ``per_test`` map key.

    A test that carries a ``file`` (``load_behaviour_tests`` always sets it) keys as
    ``"<file>:<test_id>"`` so two records sharing a ``test_id`` across different YAML files do not
    silently overwrite each other; otherwise it falls back to the bare ``test_id``. ``replay_suite``
    uses this and so must any consumer that looks ``per_test`` up by key (e.g. ``optimize_adapter``),
    so the two cannot drift.
    """
    return f"{test['file']}:{test['test_id']}" if test.get("file") else test["test_id"]


def load_behaviour_tests(subagent_dir: str | Path) -> list[dict]:
    """Flatten every ``tests/*.yaml`` record into uniform behaviour-test dicts.

    Each record: ``test_id, section, prompt, expected_route, expected_mode, must_ask_for (list),
    minimum_output (str), must_not_do (list)``. Records without a prompt are skipped (nothing to
    replay).

    A ``tests/*.yaml`` that fails to parse (YAMLError) or is not a mapping is **skipped but
    surfaced**: a ``RuntimeWarning`` names every dropped file so a corrupted file cannot silently
    shrink the suite — a green-but-smaller run that hides a broken test file is itself a failure. The
    return type stays ``list[dict]`` (callers unchanged); use ``load_behaviour_tests_report`` when the
    explicit skipped-file list is needed.
    """
    out, _skipped = load_behaviour_tests_report(subagent_dir)
    return out


def load_behaviour_tests_report(subagent_dir: str | Path) -> tuple[list[dict], list[str]]:
    """Like ``load_behaviour_tests`` but also returns the list of skipped/unparseable file names.

    Same flattening and same ``RuntimeWarning`` on skips; this variant lets a caller assert on the
    skipped set without catching warnings. ``load_behaviour_tests`` delegates here.
    """
    base = Path(subagent_dir)
    tests_dir = base / "tests"
    out: list[dict] = []
    skipped: list[str] = []
    if not tests_dir.exists():
        return out, skipped
    for tf in sorted(tests_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            skipped.append(tf.name)
            continue
        if not isinstance(data, dict):
            skipped.append(tf.name)
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
    if skipped:
        warnings.warn(
            "load_behaviour_tests skipped "
            f"{len(skipped)} unparseable/non-mapping test file(s): {', '.join(sorted(skipped))}",
            RuntimeWarning,
            stacklevel=2,
        )
    return out, skipped


def load_gate_tests(subagent_dir: str | Path) -> tuple[list[dict], list[dict], list[str]]:
    """Missing-context tests + answerable twins for the Step-13 ask-gate, read from ``tests/*.yaml``.

    Reads the YAML directly because ``load_behaviour_tests`` flattens away ``twin_of``: each
    answerable twin (a golden test with ``twin_of``) inherits the ``must_ask_for`` of the
    missing-context test it twins, so the gate sees the same required-context with (twin → should
    answer) and without (missing-context → should ask) the answer present.

    Returns ``(missing_context, twins, problems)`` where each test dict is
    ``{test_id, prompt, must_ask_for}`` and ``problems`` names every skipped/unparseable file,
    duplicate ``test_id``, and dangling ``twin_of`` link. Nothing is dropped silently: a
    green-but-smaller ask-gate run that hides a broken test file is itself the silent-overconfidence
    failure the gate exists to catch, so the caller must surface ``problems``.
    """
    base = Path(subagent_dir)
    tests_dir = base / "tests"
    missing_context: list[dict] = []
    twin_src: list[tuple[dict, str]] = []
    problems: list[str] = []
    by_id: dict = {}
    if not tests_dir.exists():
        return missing_context, [], problems
    for tf in sorted(tests_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError) as e:
            problems.append(f"{tf.name}: unparseable ({e.__class__.__name__}) — skipped")
            continue
        if not isinstance(data, dict):
            problems.append(f"{tf.name}: not a mapping — skipped")
            continue
        for m in data.get("missing_context_tests") or []:
            if not isinstance(m, dict) or not m.get("prompt"):
                continue
            tid = m.get("test_id")
            if tid in by_id:
                problems.append(
                    f"duplicate test_id {tid!r} ({tf.name}) — twin inheritance keys on it, may be wrong"
                )
            rec = {
                "test_id": tid,
                "prompt": m.get("prompt"),
                "must_ask_for": m.get("must_ask_for") or [],
            }
            missing_context.append(rec)
            by_id[tid] = rec["must_ask_for"]
        for g in data.get("golden_tests") or []:
            if isinstance(g, dict) and g.get("twin_of") and g.get("prompt"):
                twin_src.append((g, tf.name))
    twins: list[dict] = []
    for g, fname in twin_src:
        tof = g.get("twin_of")
        if tof not in by_id:
            problems.append(
                f"twin {g.get('test_id')!r} ({fname}) references unknown twin_of {tof!r} → "
                "inherits no required-context, so the gate trivially 'answers' it (broken link)"
            )
        twins.append(
            {
                "test_id": g.get("test_id"),
                "prompt": g.get("prompt"),
                "must_ask_for": by_id.get(tof, g.get("must_ask_for") or []),
            }
        )
    return missing_context, twins, problems


def _declined(output: str) -> bool:
    low = output.lower()
    return len(output.strip()) < _DECLINE_MAX_CHARS and any(m in low for m in _DECLINE_MARKERS)


def _overlap_recall(reference: str, output: str) -> float:
    """Fraction of reference content tokens present in the output (0..1)."""
    ref = _content_tokens(reference)
    if not ref:
        return 1.0  # nothing required → trivially covered
    return len(ref & _content_tokens(output)) / len(ref)


def _applicable_components(test: dict) -> set[str]:
    """Which scoring components apply to this test — stated ONCE, consumed by both the deterministic
    grader (``grade_output``) and the semantic grader (``build_grade_prompt`` / ``make_llm_grader``).

    ``route`` always applies. ``minimum`` applies only when the test carries a ``minimum_output``
    (an empty one is "not applicable", not "trivially covered"). ``ask`` / ``mustnot`` apply only
    when ``must_ask_for`` / ``must_not_do`` are present.
    """
    comps = {"route"}
    if test.get("minimum_output"):
        comps.add("minimum")
    if test.get("must_ask_for"):
        comps.add("ask")
    if test.get("must_not_do"):
        comps.add("mustnot")
    return comps


def _score_route(test: dict, declined: bool) -> float:
    """route (always applies): did the output engage vs decline as ``expected_route`` demands."""
    if test["expected_route"] == "do_not_invoke":
        return 1.0 if declined else 0.0
    return 0.0 if declined else 1.0


def _score_minimum(test: dict, output: str) -> float | None:
    """minimum: content-token recall of ``minimum_output``; ``None`` when not applicable."""
    if not test["minimum_output"]:
        return None
    return _overlap_recall(test["minimum_output"], output)


def _score_ask(test: dict, output: str) -> float | None:
    """ask: rewards ONE specific covered clarification question; caps an over-ask barrage at 0.5.

    Two axes (Step-13): a single specific question naming the missing variable keeps the full 1.0;
    over-asking (a barrage of questions) is nonmonotonic and capped. ``None`` when not applicable.
    """
    if not test["must_ask_for"]:
        return None
    n_questions = output.count("?")
    asked = n_questions >= 1
    ask_cov = max((_overlap_recall(a, output) for a in test["must_ask_for"]), default=0.0)
    covered = ask_cov >= _ASK_COVER_MIN
    if asked and covered:
        return 1.0 if n_questions <= _MAX_ASK_QUESTIONS else 0.5
    return 0.5 if (asked or covered) else 0.0


def _score_mustnot(test: dict, output: str) -> float | None:
    """mustnot: weak heuristic — penalise outputs whose tokens strongly overlap a forbidden item.

    ``None`` when not applicable. See ``grade_output`` docstring for the measured inversion this
    component can suffer; a real adherence verdict needs the semantic grader.
    """
    if not test["must_not_do"]:
        return None
    violated = sum(
        1 for f in test["must_not_do"] if _overlap_recall(f, output) >= _MUSTNOT_OVERLAP_MIN
    )
    return 1.0 - violated / len(test["must_not_do"])


def grade_output(test: dict, output: str) -> dict:
    """Coarse deterministic score (0..1) of one output against one behaviour-test record.

    Components (weighted, then renormalised over the ones that apply to this test):
    - ``route`` (0.3): did it engage vs decline as the expected_route demands.
    - ``minimum`` (0.5): content-token recall of ``minimum_output`` (did it cover what's required).
    - ``ask`` (0.1, only if ``must_ask_for``): asked a question that overlaps the required ask. Two
      axes (Step-13): one specific covered question scores 1.0; an over-ask barrage that still covers
      the variable is capped at 0.5 (over-asking hurts, nonmonotonic).
    - ``mustnot`` (0.1): heuristic — penalise outputs whose tokens strongly overlap a forbidden
      item. Deterministic "did NOT do X" detection is unreliable; this is a weak signal, low weight.
      **Known inversion (measured):** an expert answer that *names and condemns* a forbidden pattern
      ("reject 'complexity now, fix later'") lexically overlaps the forbidden phrase and is scored as
      a violation — i.e. ``mustnot`` can move the *wrong way* for the *best* answers. Do not read
      ``mustnot`` as an adherence verdict; a real one needs a **semantic (LLM) grader** (inject one
      via ``grader=``). See ``docs/output-quality-eval.md`` (invariant-layer A/B finding).

    The number is a *proxy*: trust it for relative comparison (A1 deltas, A2 regressions), not as an
    absolute quality verdict. Returns the score plus its components for transparency.

    The four scoring policies live in ``_score_route`` / ``_score_minimum`` / ``_score_ask`` /
    ``_score_mustnot`` (each ``float | None``); the "which components apply" rule lives once in
    ``_applicable_components`` and is shared with the semantic grader path.
    """
    declined = _declined(output)
    applicable = _applicable_components(test)
    route = _score_route(test, declined)
    minimum = _score_minimum(test, output) if "minimum" in applicable else None
    ask = _score_ask(test, output) if "ask" in applicable else None
    mustnot = _score_mustnot(test, output) if "mustnot" in applicable else None

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
    route: float | None, minimum: float | None, ask: float | None, mustnot: float | None
) -> float:
    """Weighted score over the components that apply to this test (``None`` = not applicable).

    ``route`` is normally always present, but the semantic grader passes ``None`` when no sample
    returned a parseable route (every judged route abstained); it is dropped like any other ``None``.
    """
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
    applicable = _applicable_components(test)
    if "ask" in applicable:
        items = "; ".join(test["must_ask_for"])
        lines += [
            "",
            f'ASK — the response should ask the user for this missing input: "{items}". '
            "ask=1 if it asks ONE specific question naming the missing input, 0.5 if partial OR if it "
            "over-asks (a barrage of clarifying questions — over-asking hurts), 0 if it does not ask.",
        ]
    if "mustnot" in applicable:
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


def _route_vote(g: dict) -> float | None:
    """One sample's route vote, or ``None`` to abstain when the judge's ``route`` isn't numeric.

    The ``build_grade_prompt`` contract asks for ``route:0|1``. A contract-violating judge (e.g. a
    cross-family model) can return a non-numeric route (``"route":"invoke"``); ``_clamp01``'s
    default-on-failure (0.0) is correct for the 0..1 partial-credit components but would silently
    score such a sample as a FAILED route, systematically biasing the gate toward false regressions.
    Returning ``None`` here lets the aggregator drop the sample from the route vote instead.
    """
    try:
        return 1.0 if _clamp01(float(g.get("route"))) >= 0.5 else 0.0  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


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
        route_votes = [v for v in (_route_vote(g) for g in grades) if v is not None]
        if route_votes:
            # Majority/mean over samples whose route parses as a number; non-numeric routes abstain.
            route = 1.0 if (sum(route_votes) / len(route_votes)) >= 0.5 else 0.0
        else:
            # No sample had a parseable route at all: rather than silently scoring a false route
            # failure, abstain the route component (None drops it from _combine_components). This is
            # the only behavioural change vs. counting non-numeric routes as 0.
            route = None
        applicable = _applicable_components(test)
        minimum = (
            median(_clamp01(g.get("minimum")) for g in grades) if "minimum" in applicable else None
        )
        ask = median(_clamp01(g.get("ask")) for g in grades) if "ask" in applicable else None
        mustnot = (
            median(_clamp01(g.get("mustnot")) for g in grades) if "mustnot" in applicable else None
        )
        return {
            "score": _combine_components(route, minimum, ask, mustnot),
            "route": route,
            "minimum": round(minimum, 4) if minimum is not None else None,
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

    The ``per_test`` key is ``per_test_key(t)`` — ``"<file>:<test_id>"`` (falling back to ``test_id``)
    so two records that share a ``test_id`` across different YAML files do not silently overwrite each
    other — that would drop a test from the mean while ``n_tests`` still counted it, an internal
    inconsistency.
    """
    per_test: dict[str, dict] = {}
    for t in tests:
        try:
            output = runner(adapter_text, t["prompt"])
            g = grader(t, output)
        except Exception as e:  # a runner/grader blow-up is a 0, not a crash
            g = {"score": 0.0, "error": str(e)}
        per_test[per_test_key(t)] = g
    scores = [g["score"] for g in per_test.values()]
    # mean and n_tests over the SAME collection (per_test), so a key collision can't desync them.
    mean_score = round(sum(scores) / len(scores), 4) if scores else 0.0
    return {"mean_score": mean_score, "n_tests": len(per_test), "per_test": per_test}


def score_suite(
    adapter_path: str | Path,
    base: str | Path,
    runner: Runner,
    grader: Grader = grade_output,
    tests: list[dict] | None = None,
) -> dict:
    """Façade for the CLI: load a package's behaviour-tests, score ``adapter_path`` against them.

    One call instead of wiring ``load_behaviour_tests`` + ``replay_suite`` (+ ``shell_runner``) by
    hand. ``adapter_path`` is the adapter ``.md`` to score; ``base`` is the package dir whose
    ``tests/*.yaml`` supply the suite. Returns the ``replay_suite`` dict (``mean_score``, ``n_tests``,
    ``per_test``) plus ``tests`` (the flattened records, so the caller can short-circuit on an empty
    suite without re-loading). Skipped/unparseable test files are surfaced via ``load_behaviour_tests``
    ``RuntimeWarning``.

    ``tests`` may be passed pre-loaded (e.g. by a caller that already ran ``load_behaviour_tests``
    via the shared CLI preamble) to avoid a redundant second read of the same files; when ``None``
    (the default) the suite is loaded here, preserving the original single-call behaviour.
    """
    if tests is None:
        tests = load_behaviour_tests(base)
    if not tests:
        return {"mean_score": 0.0, "n_tests": 0, "per_test": {}, "tests": tests}
    adapter_text = Path(adapter_path).read_text(encoding="utf-8")
    result = replay_suite(adapter_text, tests, runner, grader)
    result["tests"] = tests
    return result


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


def _bash_stdout(script: str | Path, prompt: str, env: dict[str, str] | None, timeout: int) -> str:
    """Run ``bash <script>`` with ``prompt`` on stdin and return stdout.

    Shared by ``shell_runner`` and ``shell_llm`` (their only difference was an extra ``ADAPTER_TEXT``
    env var). ``check=True``: a non-zero exit (crashed model call, bad ARN, timeout-kill) must raise
    so the caller records an error — NOT return empty stdout that grades as a legitimate empty
    response and silently poisons utility deltas / the replay gate / the judge.
    """
    proc = subprocess.run(
        ["bash", str(script)],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
        check=True,
    )
    return proc.stdout


def shell_runner(script: str | Path, timeout: int = 300) -> Runner:
    """Build a real ``runner`` that shells out to a script (e.g. ``examples/replay-runner.sh``).

    The script receives the adapter/system text in env ``ADAPTER_TEXT`` and the user prompt on
    stdin, and prints the model's response on stdout. Used by the CLI for live replay; tests use a
    fake runner instead.
    """

    def _run(system: str, prompt: str) -> str:
        env = {**os.environ, "ADAPTER_TEXT": system}
        return _bash_stdout(script, prompt, env, timeout)

    return _run


def shell_llm(script: str | Path, timeout: int = 300) -> Callable[[str], str]:
    """Build an ``llm`` callable that shells to a judge script (e.g. ``examples/codex-judge.sh``).

    The script receives the prompt on stdin and prints the model's raw reply on stdout. Wire a live
    semantic grader with ``make_llm_grader(shell_llm(script))``; a cross-family judge (codex/gpt-5.5)
    avoids the same-family self-preference a Claude judge would carry when scoring Claude output.
    """

    def _ask(prompt: str) -> str:
        return _bash_stdout(script, prompt, None, timeout)

    return _ask
