"""Baseline-gate the operating-invariant layer (A3/A5 follow-on).

The invariant-layer A/B (3 packages, 2 graders — see ``docs/output-quality-eval.md``) found the
layer's benefit is **package-dependent, ≈ inverse to baseline strength**: a large lift on a weak
adapter (mysql-at-scale baseline 0.366 → ~0.9), mild mid-range (software-design 0.774 → +0.084), and a
slight *regression* on an already-strong one (DDD 0.880). So "attach invariants to every package" is
wrong — attach them where a package's behaviour-test baseline is weak.

This module turns that into a rule:

- ``should_attach_invariants(baseline, threshold=0.80)`` — the deterministic decision. The default
  0.80 is the crossover the n=3 data implies (attach mysql 0.366 ✓ and software-design 0.774 ✓ which
  both improved; skip DDD 0.880 ✗ which regressed). Treat it as a starting threshold, refine as N
  grows.
- ``recommend_invariants(subagent_dir, runner, grader, threshold)`` — measures the baseline by
  replaying the adapter **without** its invariant section (model-cost; runner/grader injected, same as
  the rest of the eval harness) and applies the rule. It only *recommends* — set the profile's
  ``attach_invariants`` flag (honoured by ``export_claude_agent``) from the result; nothing is
  auto-edited.
"""

from __future__ import annotations

from pathlib import Path

from tools.subagent_factory.behaviour_replay import (
    Grader,
    Runner,
    grade_output,
    load_behaviour_tests,
    replay_suite,
)
from tools.subagent_factory.compile_invariants import (
    INVARIANT_SECTION_HEADING,
    strip_invariant_section,
)

_DEFAULT_THRESHOLD = 0.80


def should_attach_invariants(baseline: float, threshold: float = _DEFAULT_THRESHOLD) -> dict:
    """Decide whether the invariant layer is worth attaching, given the no-invariant baseline."""
    attach = baseline < threshold
    return {
        "attach": attach,
        "baseline": round(baseline, 4),
        "threshold": threshold,
        "reason": (
            f"baseline {baseline:.3f} < {threshold} → weak adapter, invariants likely help"
            if attach
            else f"baseline {baseline:.3f} ≥ {threshold} → strong adapter, invariants may not help"
        ),
    }


def recommend_invariants(
    subagent_dir: str | Path,
    runner: Runner,
    grader: Grader = grade_output,
    threshold: float = _DEFAULT_THRESHOLD,
) -> dict:
    """Measure the no-invariant baseline (replay) and recommend whether to attach the layer.

    Returns the ``should_attach_invariants`` decision plus ``n_tests``. ``error`` when the package has
    no behaviour-tests or no invariant section to strip (nothing to gate). Model-cost via ``runner``;
    use a semantic ``grader`` (``make_llm_grader``) for a trustworthy baseline.
    """
    base = Path(subagent_dir)
    adapter = base / "adapters" / "claude-code" / f"{base.name}.md"
    if not adapter.exists():
        return {"error": "no adapter", "attach": True}
    text = adapter.read_text(encoding="utf-8")
    if INVARIANT_SECTION_HEADING not in text:
        return {"error": "no invariant section to gate", "attach": False}
    tests = load_behaviour_tests(base)
    if not tests:
        return {"error": "no behaviour-tests", "attach": True}
    stripped = strip_invariant_section(text)
    baseline = replay_suite(stripped, tests, runner, grader)["mean_score"]
    return {**should_attach_invariants(baseline, threshold), "n_tests": len(tests)}
