"""Phase 2.5 importance ranking — score extracted candidate units before triage.

Phase 2 interrogation finds *what* a source says; this phase decides *what is
worth keeping*. See ``docs/subagent-authoring-process-cycle.md`` (Phase 2.5).

The dimension scores (1–5) are a judgement call made by the interrogating agent
and recorded per candidate unit. This module is the *deterministic* half: it
validates those scores and applies the fixed decision rule, so the keep/discard
boundary is reproducible rather than re-argued each run.

Decision rule (from Phase 2.5):
  keep    — total >= 32, OR (risk_impact >= 5 AND actionability >= 4),
            OR (authority >= 5 AND operational_fit >= 4)
  discard — total < 20 AND no strong actionability/risk/uniqueness (none >= 4)
  review  — everything in between (human decides keep-for-reference vs drop)

Input is a YAML file::

    schema_version: importance-scores-v1
    candidate_units:
      - id: U1
        source_id: <source_id>
        summary: "one-line description of the unit"
        scores:                 # 'importance_score:' is also accepted
          authority: 5
          actionability: 4
          reusability: 4
          risk_impact: 5
          evidence_strength: 4
          uniqueness: 3
          transferability: 4
          stability: 4
          operational_fit: 4

High-value units (``keep``) proceed to Phase 4 triage; ``discard`` units route to
the provenance ledger only; ``review`` units need a human decision.
"""

import sys
from pathlib import Path

import yaml

DIMENSIONS = (
    "authority",
    "actionability",
    "reusability",
    "risk_impact",
    "evidence_strength",
    "uniqueness",
    "transferability",
    "stability",
    "operational_fit",
)

MAX_TOTAL = len(DIMENSIONS) * 5  # 45
_STRONG = 4  # threshold for "strong" actionability/risk/uniqueness


def score_unit(unit: dict) -> dict:
    """Validate one candidate unit's scores and apply the decision rule.

    Returns a dict with ``id``, ``total``, ``verdict``
    (keep/review/discard/invalid), ``reasons``, and ``errors``.
    """
    unit_id = str(unit.get("id") or unit.get("unit_id") or "?")
    raw = unit.get("scores")
    if raw is None:
        raw = unit.get("importance_score")
    errors: list[str] = []

    if not isinstance(raw, dict):
        return {
            "id": unit_id,
            "total": 0,
            "verdict": "invalid",
            "reasons": [],
            "errors": ["missing 'scores' (or 'importance_score') mapping"],
        }

    s: dict[str, int] = {}
    for dim in DIMENSIONS:
        if dim not in raw:
            errors.append(f"missing dimension '{dim}'")
            continue
        val = raw[dim]
        if not isinstance(val, int) or isinstance(val, bool) or not 1 <= val <= 5:
            errors.append(f"dimension '{dim}'={val!r} is not an integer in 1–5")
            continue
        s[dim] = val

    extra = sorted(set(raw) - set(DIMENSIONS))
    if extra:
        errors.append(f"unknown dimension(s): {', '.join(extra)}")

    if errors:
        return {"id": unit_id, "total": 0, "verdict": "invalid", "reasons": [], "errors": errors}

    total = sum(s.values())
    reasons: list[str] = []

    keep = False
    if total >= 32:
        keep = True
        reasons.append(f"total {total} >= 32")
    if s["risk_impact"] >= 5 and s["actionability"] >= 4:
        keep = True
        reasons.append("risk_impact>=5 and actionability>=4")
    if s["authority"] >= 5 and s["operational_fit"] >= 4:
        keep = True
        reasons.append("authority>=5 and operational_fit>=4")

    if keep:
        verdict = "keep"
    else:
        strong = (
            s["actionability"] >= _STRONG
            or s["risk_impact"] >= _STRONG
            or s["uniqueness"] >= _STRONG
        )
        if total < 20 and not strong:
            verdict = "discard"
            reasons.append(f"total {total} < 20 and no strong actionability/risk/uniqueness")
        else:
            verdict = "review"
            reasons.append(f"total {total}; no keep rule met and not a clear discard")

    return {"id": unit_id, "total": total, "verdict": verdict, "reasons": reasons, "errors": []}


def score_units(units: list[dict]) -> dict:
    """Score a list of candidate units and bucket them by verdict."""
    scored = [score_unit(u) for u in units]
    buckets = {"keep": [], "review": [], "discard": [], "invalid": []}
    for r in scored:
        buckets[r["verdict"]].append(r["id"])
    return {
        "units": scored,
        "summary": {k: len(v) for k, v in buckets.items()},
        "kept": buckets["keep"],
        "review": buckets["review"],
        "discarded": buckets["discard"],
        "invalid": buckets["invalid"],
        "valid": not buckets["invalid"],
    }


def load_units(path: str | Path) -> list[dict]:
    """Load candidate units from a YAML file.

    Accepts a top-level ``candidate_units:`` list or a bare list of units.
    """
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if isinstance(data, list):
        return data
    return data.get("candidate_units", []) or []


def score_units_file(path: str | Path) -> dict:
    """Load and score a candidate-unit YAML file."""
    return score_units(load_units(path))


def format_worksheet(result: dict) -> str:
    """Render the importance-scored shortlist as a Markdown table for Phase 4."""
    lines = [
        "# Importance-Scored Unit Shortlist (Phase 2.5)",
        "",
        f"keep={result['summary']['keep']}  review={result['summary']['review']}  "
        f"discard={result['summary']['discard']}  invalid={result['summary']['invalid']}",
        "",
        "| Unit ID | Total /45 | Verdict | Reason |",
        "|---------|-----------|---------|--------|",
    ]
    for r in result["units"]:
        detail = "; ".join(r["reasons"] or r["errors"])
        lines.append(f"| {r['id']} | {r['total']} | {r['verdict']} | {detail} |")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.score_extracted_units <units.yaml>")
        sys.exit(1)

    result = score_units_file(sys.argv[1])
    print(format_worksheet(result), end="")
    if not result["valid"]:
        print(f"\nINVALID: {len(result['invalid'])} unit(s) have malformed scores.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
