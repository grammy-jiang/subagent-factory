"""Deterministic distill-vs-retrieve routing for knowledge items (Step-14 / G-track, G1).

The rag-graphrag research answer to the factory's distill-vs-retrieve question: `knowledge_partition`
is a **deterministic routing rule**, not an either/or hand decision. Each knowledge item is routed by
four attributes — reuse, volatility, size, citation-need:

  - **distill** (carry in-prompt / `always_on`): stable + high-reuse + small + non-citable — the
    transferable rules the expert always applies.
  - **retrieve** (keep in a file / runtime store, read on demand): volatile OR long-tail (low-reuse)
    OR large OR citation-bearing — anything that ages, is rarely needed, is too big for the prompt, or
    must cite a real source passage.
  - **fine-tune** (transferable bulk skill): the research's third bucket — but the factory has **no
    training step**, so a fine-tune candidate degrades to *retrieve* (a reference file), flagged.

**Advisory, never a hard gate.** G1 is an open ACADEMIC question — no paper compares an agent's *own*
distilled principle store against runtime retrieval — so this routing ships **behind a per-package
measurement** (reuse the behaviour-test harness to A/B an item in-prompt vs in a file), never as a
global default that silently moves a package's content. The full retrieval spine (G2 hybrid
dense+BM25+rerank, G3 passage-grounded graph, G4 selective gate, G5 generate-then-cite, G6 index-time
distill) stays spec for the same reason — see `step-14-runtime-retrieval.md`.

Defaults skew conservative (unknown → *retrieve*): never silently bake volatile/uncertain content
into the prompt. Pure functions, no deps. Maps onto the existing profile `knowledge_partition`:
distill → `always_on`; retrieve → `skills` / `references`.
"""

import argparse
import json
import sys
from pathlib import Path

# Attribute vocabularies (case-insensitive). Anything not recognised as the distill-favouring value
# is treated conservatively (→ retrieve): an unknown volatility is volatile, an unknown reuse is
# long-tail. So a half-specified item is kept in a file, not baked into the prompt.
_STABLE = {"stable", "low"}
_LARGE = {"large", "big", "xl"}


def _norm(v: object) -> str:
    return str(v).strip().lower()


def _truthy(v: object) -> bool:
    if isinstance(v, bool):
        return v
    return _norm(v) in {"true", "yes", "y", "1", "required", "needed"}


def route_knowledge_item(
    name: str | None = None,
    *,
    reuse: str,
    volatility: str,
    size: str,
    citation_need: object = False,
) -> dict:
    """Route one knowledge item to ``distill`` or ``retrieve`` (G1 deterministic rule).

    ``reuse`` high|low, ``volatility`` stable|volatile, ``size`` small|large, ``citation_need`` bool.
    Returns ``{name, route, placement, reasons, fine_tune_candidate, note}``. ``placement`` maps to the
    profile's ``knowledge_partition`` buckets (``always_on`` for distill; ``skills/references`` for
    retrieve). Any retrieve trigger wins; only a stable + high-reuse + small + non-citable item distills.
    """
    high_reuse = _norm(reuse) == "high"
    volatile = _norm(volatility) not in _STABLE
    large = _norm(size) in _LARGE
    citable = _truthy(citation_need)

    retrieve_reasons: list[str] = []
    if volatile:
        retrieve_reasons.append("volatile")
    if not high_reuse:
        retrieve_reasons.append("long-tail (low reuse)")
    if large:
        retrieve_reasons.append("large")
    if citable:
        retrieve_reasons.append("citation-bearing")

    # The research's fine-tune bucket = transferable bulk (high-reuse, large, stable, non-citable).
    # The factory cannot fine-tune, so it degrades to retrieve, flagged for the human.
    fine_tune = high_reuse and large and not volatile and not citable

    if retrieve_reasons:
        note = (
            "transferable bulk: fine-tune is the research-ideal bucket, but the factory has no "
            "training step → keep as a retrieved reference"
            if fine_tune
            else ""
        )
        return {
            "name": name,
            "route": "retrieve",
            "placement": "skills/references",
            "reasons": retrieve_reasons,
            "fine_tune_candidate": fine_tune,
            "note": note,
        }
    return {
        "name": name,
        "route": "distill",
        "placement": "always_on",
        "reasons": ["stable", "high-reuse", "small", "non-citable"],
        "fine_tune_candidate": False,
        "note": "",
    }


def partition_plan(items: list[dict]) -> dict:
    """Route a list of knowledge items into distill / retrieve buckets (G1, advisory).

    Each item: ``{name?, reuse, volatility, size, citation_need?}``. Returns the per-item routes plus
    ``distill`` / ``retrieve`` name lists, ``fine_tune_candidates``, and ``measurement_required`` — a
    standing reminder that G1 is unproven, so the resulting partition must be A/B-measured on the
    package's behaviour-tests (in-prompt vs file) before it is trusted, not applied as a silent default.
    """
    routed = [
        route_knowledge_item(
            it.get("name"),
            reuse=it["reuse"],
            volatility=it["volatility"],
            size=it["size"],
            citation_need=it.get("citation_need", False),
        )
        for it in items
    ]
    return {
        "items": routed,
        "distill": [r["name"] for r in routed if r["route"] == "distill"],
        "retrieve": [r["name"] for r in routed if r["route"] == "retrieve"],
        "fine_tune_candidates": [r["name"] for r in routed if r["fine_tune_candidate"]],
        "measurement_required": bool(routed),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Distill-vs-retrieve knowledge routing (Step-14 G-track, G1 — advisory)."
    )
    ap.add_argument("--name", help="item name/label")
    ap.add_argument("--reuse", choices=["high", "low"], help="how often the item is needed")
    ap.add_argument("--volatility", choices=["stable", "volatile"], help="how fast it ages")
    ap.add_argument("--size", choices=["small", "large"], help="prompt-budget footprint")
    ap.add_argument("--citation-need", action="store_true", help="must cite a real source passage")
    ap.add_argument(
        "--plan", metavar="items.json", help="JSON list of items → a full partition plan"
    )
    args = ap.parse_args()

    if args.plan:
        items = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        print(json.dumps(partition_plan(items), indent=2))
    elif args.reuse and args.volatility and args.size:
        print(
            json.dumps(
                route_knowledge_item(
                    args.name,
                    reuse=args.reuse,
                    volatility=args.volatility,
                    size=args.size,
                    citation_need=args.citation_need,
                ),
                indent=2,
            )
        )
    else:
        ap.error("provide --plan FILE, or --reuse/--volatility/--size for a single item")
    sys.exit(0)


if __name__ == "__main__":
    main()
