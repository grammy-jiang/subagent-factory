"""Deterministic GRADE-style confidence grading (Step 16 / K-track, K2).

Folds the systematic-review-evidence-synthesis research finding K2: a source's confidence is a
**GRADE-style start-then-up/down-grade** function — start at a baseline by source type, *down*-grade
for risk-of-bias-domain failures / inconsistency / conflict / indirectness, *up*-grade for replication
or large effect, then clamp to a level. This is the **deterministic arithmetic** half of the
semantic/arithmetic split (K1): the LLM supplies the *semantic* factors (which downgrades/upgrades
apply); this code owns *all* the scoring and clamping, so a grade is reproducible and auditable.

Two research-mandated shapes:
- **"medium" (and any grade the factors moved) is reported as a RANGE, not a point** (K6) — an unclear
  source should surface its uncertainty width.
- there is an explicit **"insufficient"** floor below "low" (K8) — prefer a calibrated abstention to a
  confident-wrong "low".

No model, no deps; pure function. The factory's existing ``confidence: high|medium|low`` becomes the
``level`` field of this function's output.
"""

from __future__ import annotations

# Ordered low→high; "insufficient" is the abstention floor (K8).
LEVELS = ("insufficient", "low", "medium", "high")

# Source-type → GRADE baseline level, aligned with the evidence-protocol confidence scale
# (high = official/peer-reviewed/replicated/classic; medium = expert book / strong essay / case study;
# low = anecdotal / weak secondary). Unknown source types fall back to ``default_baseline``.
_BASELINE: dict[str, str] = {
    "peer-reviewed": "high",
    "official": "high",
    "replicated": "high",
    "classic": "high",
    "standard": "high",
    "expert-book": "medium",
    "technical-essay": "medium",
    "case-study": "medium",
    "practitioner": "medium",
    "anecdotal": "low",
    "secondary": "low",
    "unsupported": "low",
    "blog": "low",
}

# Recognised GRADE down/up-grade reasons (advisory; the caller decides which apply). Free-form reasons
# are still counted — these sets are for documentation/validation, not a hard whitelist.
DOWNGRADE_REASONS = frozenset(
    {"risk-of-bias", "inconsistency", "conflict", "indirectness", "imprecision", "publication-bias"}
)
UPGRADE_REASONS = frozenset({"replication", "large-effect", "dose-response", "corroborated"})


def grade_confidence(
    source_type: str,
    downgrades: list[str] | tuple[str, ...] = (),
    upgrades: list[str] | tuple[str, ...] = (),
    *,
    default_baseline: str = "medium",
) -> dict:
    """Return a GRADE-style confidence grade.

    ``source_type`` sets the baseline level; each entry in ``downgrades`` lowers it one step and each
    in ``upgrades`` raises it one step; the result is clamped to ``LEVELS``. Returns ``level`` (a
    single ``LEVELS`` value), ``range`` (``[lo, hi]`` — widened to ±1 step whenever any factor was
    applied, so an adjusted grade surfaces its uncertainty per K6), ``baseline``, and the applied
    ``downgrades``/``upgrades`` for audit.
    """
    base = _BASELINE.get(source_type, default_baseline)
    if base not in LEVELS:
        base = default_baseline if default_baseline in LEVELS else "medium"

    n_down = len([d for d in downgrades if d])
    n_up = len([u for u in upgrades if u])
    idx = LEVELS.index(base) + n_up - n_down
    idx = max(0, min(idx, len(LEVELS) - 1))
    level = LEVELS[idx]

    # K6: any grade the factors moved (or a "medium") is uncertain → report a ±1-step range; a clean
    # baseline-only grade is a tight point range.
    moved = (n_down + n_up) > 0
    if moved or level == "medium":
        lo = LEVELS[max(0, idx - 1)]
        hi = LEVELS[min(len(LEVELS) - 1, idx + 1)]
    else:
        lo = hi = level

    return {
        "level": level,
        "range": [lo, hi],
        "baseline": base,
        "downgrades": [d for d in downgrades if d],
        "upgrades": [u for u in upgrades if u],
    }


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(description="GRADE-style confidence grade (deterministic).")
    ap.add_argument("source_type", help="e.g. peer-reviewed, expert-book, anecdotal")
    ap.add_argument("--down", action="append", default=[], help="downgrade reason (repeatable)")
    ap.add_argument("--up", action="append", default=[], help="upgrade reason (repeatable)")
    args = ap.parse_args()
    print(json.dumps(grade_confidence(args.source_type, args.down, args.up), indent=2))


if __name__ == "__main__":
    main()
