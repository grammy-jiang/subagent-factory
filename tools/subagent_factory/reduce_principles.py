"""Recall-then-filter REDUCE over per-book principles (P3, productionized from the P0 prototype).

The cross-source merge, in three deterministic stages around one LLM stage:
  - recall_clusters(): embedding-cosine candidate clusters (high-recall, over-proposes — the C1 recall).
    The embedder is injected (Callable[[list[str]], list[list[float]]]); default `embed_minilm`.
  - <LLM precision filter>: per cluster decide confirm / split / conflict (run separately; passed in).
  - apply_decisions(): build merged multi-anchor principles from the decisions.
  - select_top(): rank by importance (cross-book strength -> evidence breadth -> confidence), keep N
    (the anti-bloat lever — dedup alone leaves too many; books are largely complementary).

Proven on software-architecture: 303 -> 289 true-distinct (filter rescued ~75 over-merges) -> 50.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path

import yaml

from tools.subagent_factory._common import confidence_rank
from tools.subagent_factory._common import cosine as _cosine

Embedder = Callable[[list[str]], list[list[float]]]


def recall_clusters(
    principles: list[dict], embedder: Embedder, cos: float = 0.55
) -> list[list[int]]:
    """Greedy single-pass cosine clustering of principle statements -> candidate index groups."""
    embs = embedder([str(p.get("statement", "")) for p in principles])
    reps: list[list[float]] = []
    groups: list[list[int]] = []
    for idx, e in enumerate(embs):
        best, best_c = -1, cos
        for gi, r in enumerate(reps):
            c = _cosine(e, r)
            if c >= best_c:
                best_c, best = c, gi
        if best >= 0:
            groups[best].append(idx)
        else:
            reps.append(e)
            groups.append([idx])
    return groups


def merge_group(principles: list[dict], idxs: list[int]) -> dict:
    """Fuse principles into one multi-anchor principle (union sources/claims/applies_when)."""
    members = [principles[i] for i in idxs]
    rep = max(members, key=lambda p: len(str(p.get("statement", ""))))
    sids = sorted({s for p in members for s in (p.get("source_ids") or [p.get("source_id")]) if s})
    derived = sorted({c for p in members for c in (p.get("derived_from_claims") or [])})
    applies: list[str] = []
    for p in members:
        for a in p.get("applies_when") or []:
            if a not in applies:
                applies.append(a)
    conf = max((p.get("confidence", "medium") for p in members), key=confidence_rank)
    return {
        "statement": rep.get("statement"),
        "source_ids": sids,
        "n_sources": len(sids),
        "derived_from_claims": derived,
        "confidence": conf,
        "applies_when": applies,
        "operational_mapping": rep.get("operational_mapping"),
    }


def apply_decisions(
    principles: list[dict], groups: list[list[int]], decisions: dict[int, dict] | None = None
) -> list[dict]:
    """Build merged principles from the LLM filter decisions (per group index): confirm/split/conflict.

    Singletons (groups of one) pass through. Missing decision defaults to confirm.
    """
    decisions = decisions or {}
    out: list[dict] = []
    for gi, idxs in enumerate(groups):
        if len(idxs) == 1:
            out.append(merge_group(principles, idxs))
            continue
        d = decisions.get(gi, {"action": "confirm"})
        action = d.get("action", "confirm")
        if action == "split":
            covered: set[int] = set()
            for sg in d.get("subgroups") or [[i] for i in idxs]:
                out.append(merge_group(principles, [i for i in sg if 0 <= i < len(principles)]))
                covered |= set(sg)
            out += [merge_group(principles, [i]) for i in idxs if i not in covered]
        elif action == "conflict":
            out += [merge_group(principles, [i]) for i in idxs]
        else:
            mp = merge_group(principles, idxs)
            if d.get("canonical"):
                mp["statement"] = d["canonical"]
            out.append(mp)
    return out


def importance(p: dict) -> tuple:
    return (
        p.get("n_sources", 1),
        len(p.get("derived_from_claims") or []),
        confidence_rank(p.get("confidence", "medium")),
    )


def select_top(principles: list[dict], limit: float) -> list[dict]:
    """Keep the importance-ranked top principles.

    ``limit`` is a count or a fraction:
    - ``0`` (or falsy)      → keep all.
    - ``0 < limit < 1``     → keep that FRACTION of the pool (e.g. 0.25 → top quarter), min 1.
    - ``limit >= 1``        → keep that many (count), capped at the pool size.
    """
    ranked = sorted(principles, key=importance, reverse=True)
    if not limit or limit <= 0:
        return ranked
    if limit < 1:
        k = max(1, round(len(ranked) * limit))
    else:
        k = int(limit)
    return ranked[:k]


def _embed_minilm(statements: list[str]) -> list[list[float]]:
    from tools.subagent_factory.seed_principle_clusters import embed_minilm

    return embed_minilm(statements)


def main() -> int:
    ap = argparse.ArgumentParser(description="Recall-then-filter REDUCE over per-book principles.")
    ap.add_argument(
        "principles_yaml", type=Path, help="combined principles.yaml (schema principles-v1)"
    )
    ap.add_argument("--cos", type=float, default=0.55)
    ap.add_argument("--select", type=int, default=0)
    ap.add_argument("--decisions", type=Path, help="optional decisions.json keyed by group index")
    args = ap.parse_args()
    ps = (yaml.safe_load(args.principles_yaml.read_text(encoding="utf-8")) or {}).get(
        "principles"
    ) or []
    groups = recall_clusters(ps, _embed_minilm, args.cos)
    decisions = (
        {int(k): v for k, v in json.loads(args.decisions.read_text()).items()}
        if args.decisions
        else None
    )
    merged = select_top(apply_decisions(ps, groups, decisions), args.select)
    print(f"{len(ps)} principles -> {len(groups)} clusters -> {len(merged)} merged/selected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
