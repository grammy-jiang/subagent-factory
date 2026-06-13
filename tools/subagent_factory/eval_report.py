"""Consolidated version-comparison report (Phase 10 #1) — judge ranking + deterministic hedge + cost.

Combines the three signals the agent-benchmarking research says to report together, so a verdict is
diagnostic and not gameable by one axis:
- **advice quality** — `judge_ab` (position-swapped) → `rank_versions` (BT + CI + separation);
- **grounding** — `grounding_check` per version (deterministic, judge-independent hedge);
- **cost/compute parity** — review length per version + a parity flag, so a longer/pricier version
  is not credited a win it earned only by spending more.

The judge is injectable (real LLM in prod, mock in tests). The deterministic assembly is unit-tested.

Library: ``run_eval(versions, judge, doc_path, passes) -> dict`` ; helpers ``cost_stats``,
``parity_flag``, ``assemble``.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from tools.subagent_factory.grounding_check import grounding_check
from tools.subagent_factory.judge_ab import run_ab


def cost_stats(text: str) -> dict:
    return {"chars": len(text), "lines": text.count("\n") + 1}


def parity_flag(costs: dict[str, dict], tol: float = 0.4) -> str | None:
    """Flag if versions differ in size beyond ``tol`` (longest/shortest - 1), so a length lean is visible."""
    lines = [c["lines"] for c in costs.values() if c["lines"] > 0]
    if len(lines) < 2:
        return None
    ratio = max(lines) / max(min(lines), 1) - 1.0
    if ratio > tol:
        return f"length disparity {ratio:.0%} (longest/shortest lines) — a win may be partly length, not quality"
    return None


def assemble(ab: dict, grounding_by_version: dict[str, dict], costs: dict[str, dict]) -> dict:
    """Combine the judge ranking, per-version grounding, and cost stats into one verdict."""
    ranking = ab.get("ranking", {})
    return {
        "advice_quality": {
            "ranking": ranking.get("ranking", []),
            "separated": ranking.get("top2_separated", False),
            "decided": ab.get("n_decided", 0),
            "passes": ab.get("passes", 0),
        },
        "grounding": {
            v: {
                "coverage": g.get("coverage"),
                "cross_source_borrows": len(g.get("cross_source_terms", [])),
            }
            for v, g in grounding_by_version.items()
        },
        "cost": costs,
        "parity_flag": parity_flag(costs),
        "verdict": (
            "advice-quality: "
            + (
                f"{ranking['ranking'][0]['version']} (separated)"
                if ranking.get("top2_separated") and ranking.get("ranking")
                else "inconclusive (CIs overlap)"
            )
        ),
    }


def run_eval(
    versions: list[dict],
    judge: Callable[[str], str],
    doc_path: str | Path | None = None,
    passes: int = 12,
    seed: int = 0,
) -> dict:
    """``versions`` = exactly two ``{"slug_dir","label","review_path"}``. Runs the full comparison."""
    a, b = versions
    ta = Path(a["review_path"]).read_text(encoding="utf-8")
    tb = Path(b["review_path"]).read_text(encoding="utf-8")
    ab = run_ab(a["label"], ta, b["label"], tb, judge, passes=passes, seed=seed)
    grounding = {
        a["label"]: grounding_check(a["slug_dir"], a["review_path"], doc_path),
        b["label"]: grounding_check(b["slug_dir"], b["review_path"], doc_path),
    }
    costs = {a["label"]: cost_stats(ta), b["label"]: cost_stats(tb)}
    return assemble(ab, grounding, costs)
