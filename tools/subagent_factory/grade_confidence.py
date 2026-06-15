"""Deterministic GRADE-style confidence grading (Step 16 / K-track: K2 + K4 + K5).

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

Two more K-track functions live here because they are the same arithmetic-on-semantic-signals layer:
- **K4 `rob_weight`** — risk-of-bias as an **advisory weight, never a gate.** Automated RoB is weak
  (frontier LLMs ~42% Macro-F1; human ceiling κ=0.40), so RoB may only *lower confidence* at
  aggregation; it must not drop a source. Rolls per-domain signals up and maps them to at most one
  capped downgrade that feeds ``grade_confidence``.
- **K5 `conflict_label`** — resolve multiple judge verdicts by **reground + abstain, not averaging:**
  agree→high, one judge vindicated by reground→medium, both/all wrong or unresolved→withhold (human).
  The same multi-truth rule as Step-7.

No model, no deps; pure functions. The factory's existing ``confidence: high|medium|low`` becomes the
``level`` field of ``grade_confidence``.
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


# ── K4: risk-of-bias as an ADVISORY weight, never a gate ──

# RoB2-style per-domain assessment levels, worst→best. "unclear" is its own level — uncertainty is
# not penalised as "high" (that would conflate missing information with demonstrated bias).
_ROB_LEVELS = ("high", "some-concerns", "unclear", "low")


def rob_weight(domain_assessments: dict | list | tuple) -> dict:
    """Convert qualitative risk-of-bias domain signals into an ADVISORY downgrade — never a gate (K4).

    Automated RoB is weak (frontier LLMs ~42% Macro-F1; human ceiling κ=0.40), so RoB only ever
    *lowers confidence* at aggregation; it must **not** drop a source. Rolls per-domain assessments up
    (RoB2 rule: any ``high`` → overall ``high``; else any ``some-concerns`` → ``some-concerns``; else
    all ``low`` → ``low``; else ``unclear``), then maps overall to **at most one** ``risk-of-bias``
    downgrade — capped, so a weak signal cannot dominate the grade, and only a clear overall-``high``
    fires it. Feed the returned ``downgrades`` to ``grade_confidence``.

    ``domain_assessments`` may be a ``{domain: level}`` dict or a list/tuple of level strings.
    """
    raw = (
        domain_assessments.values() if isinstance(domain_assessments, dict) else domain_assessments
    )
    norm = [str(x).strip().lower() for x in raw if str(x).strip()]
    counts = {lv: norm.count(lv) for lv in _ROB_LEVELS}
    if counts["high"]:
        overall = "high"
    elif counts["some-concerns"]:
        overall = "some-concerns"
    elif norm and all(x == "low" for x in norm):
        overall = "low"
    else:
        overall = "unclear"
    return {
        "overall": overall,
        "downgrades": ["risk-of-bias"] if overall == "high" else [],
        "advisory": True,
        "is_gate": False,
        "counts": counts,
    }


def grade_with_rob(
    source_type: str,
    rob_domains: dict | list | tuple = (),
    downgrades: list[str] | tuple[str, ...] = (),
    upgrades: list[str] | tuple[str, ...] = (),
    *,
    default_baseline: str = "medium",
) -> dict:
    """``grade_confidence`` with risk-of-bias folded in as advisory downgrades (K2 + K4).

    Computes ``rob_weight(rob_domains)``, appends its (capped) downgrades to ``downgrades``, grades,
    and attaches the ``rob`` detail for audit. RoB never gates here — it can only move the grade.
    """
    rob = rob_weight(rob_domains)
    grade = grade_confidence(
        source_type, [*downgrades, *rob["downgrades"]], upgrades, default_baseline=default_baseline
    )
    grade["rob"] = rob
    return grade


# ── K5: conflict among judges → verification label by reground, not by averaging ──


def _modal_fraction(values: list[str]) -> float:
    return max((values.count(v) for v in set(values)), default=0) / len(values) if values else 0.0


def conflict_label(
    judgments: list | tuple,
    *,
    winner: object | None = None,
    both_wrong: bool = False,
) -> dict:
    """Resolve multiple judge verdicts into a verification label — reground + abstain, never average (K5).

    Dual (or more) judges; on disagreement you re-ground against the source instead of averaging the
    scores. ``agree`` → ``high``; one judge vindicated by the reground (``winner`` set) → ``one_wins`` /
    ``medium``; all wrong (``both_wrong``) or an unresolved disagreement (no reground yet) → ``withhold``
    (route to a human). ``winner`` is whatever the reground vindicated (an index or the verdict value);
    only its presence matters here. Returns ``label``, ``verification`` (high/medium/withhold),
    ``needs_human``, ``agreement`` (modal fraction), and the ``distinct`` verdicts seen.
    """
    verdicts = [str(j).strip().lower() for j in judgments]
    if not verdicts:
        return {
            "label": "no_judgments",
            "verification": "withhold",
            "needs_human": True,
            "agreement": 0.0,
            "distinct": [],
        }
    distinct = sorted(set(verdicts))
    agreement = _modal_fraction(verdicts)
    if len(distinct) == 1:
        return {
            "label": "agree",
            "verification": "high",
            "needs_human": False,
            "agreement": agreement,
            "distinct": distinct,
        }
    if both_wrong:
        label, verification, needs_human = "both_wrong", "withhold", True
    elif winner is not None:
        label, verification, needs_human = "one_wins", "medium", False
    else:
        label, verification, needs_human = "unresolved", "withhold", True
    return {
        "label": label,
        "verification": verification,
        "needs_human": needs_human,
        "agreement": agreement,
        "distinct": distinct,
    }


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(description="GRADE-style confidence grade (deterministic).")
    ap.add_argument("source_type", help="e.g. peer-reviewed, expert-book, anecdotal")
    ap.add_argument("--down", action="append", default=[], help="downgrade reason (repeatable)")
    ap.add_argument("--up", action="append", default=[], help="upgrade reason (repeatable)")
    ap.add_argument(
        "--rob-domain",
        action="append",
        default=[],
        help="risk-of-bias domain level (high|some-concerns|unclear|low), repeatable — advisory (K4)",
    )
    args = ap.parse_args()
    if args.rob_domain:
        print(
            json.dumps(
                grade_with_rob(args.source_type, args.rob_domain, args.down, args.up), indent=2
            )
        )
    else:
        print(json.dumps(grade_confidence(args.source_type, args.down, args.up), indent=2))


if __name__ == "__main__":
    main()
