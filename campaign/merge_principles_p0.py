#!/usr/bin/env python3
"""P0 REDUCE prototype: merge per-book MAP modules -> dedup -> select -> measure vs baseline.

Recall-then-filter merge (per-book-authoring-upgrade.md), deterministic stages:
  - RECALL: cluster per-book principles by similarity. Lexical token-F1 (default) is paraphrase-blind
    and finds ~0 cross-book dups (proven); --embeddings uses MiniLM cosine (the C1 recall) which finds
    the real paraphrased duplicates.
  - MERGE: each cluster -> one multi-anchor principle (union sources/claims/applies_when).
  - SELECT (--select N): rank merged principles by importance (cross-book strength, evidence breadth,
    confidence) and keep the best N -> the anti-bloat step (dedup alone leaves ~215-260 principles).
The LLM PRECISION FILTER (confirm/split clusters) is the next refinement, run on top of RECALL.

Throwaway P0 harness (campaign/, outside the make-verify gate). Reads every cache/book-extracts/<sha>/
module with a principles.yaml.

Run:
  python3 campaign/merge_principles_p0.py                         # lexical token-F1 (baseline behaviour)
  python3 campaign/merge_principles_p0.py --embeddings --cos 0.55 --select 50
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import claim_f1
from tools.subagent_factory.grounding_check import grounding_richness

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "cache" / "book-extracts"
OUT = REPO / "cache" / "p0-build" / "software-architecture-p0"
_CONF = {"low": 0, "medium": 1, "high": 2}


def load_modules() -> list[dict]:
    mods = []
    for d in sorted(p for p in CACHE.iterdir() if p.is_dir() and not p.name.endswith("-copilot")):
        pp, mj, cl = d / "principles.yaml", d / "module.json", d / "claims.jsonl"
        if not pp.exists():
            continue
        meta = json.loads(mj.read_text()) if mj.exists() else {}
        prins = (yaml.safe_load(pp.read_text()) or {}).get("principles") or []
        claims = (
            [json.loads(x) for x in cl.read_text().splitlines() if x.strip()] if cl.exists() else []
        )
        mods.append(
            {
                "sid": meta.get("source_id", d.name[:12]),
                "title": meta.get("title", d.name[:12]),
                "prins": prins,
                "claims": claims,
            }
        )
    return mods


def cluster_lexical(principles: list[tuple[str, dict]], threshold: float) -> list[list[int]]:
    reps: list[str] = []
    groups: list[list[int]] = []
    for idx, (_sid, p) in enumerate(principles):
        stmt = str(p.get("statement", ""))
        best, best_s = -1, threshold
        for gi, r in enumerate(reps):
            s = claim_f1(stmt, r)
            if s >= best_s:
                best_s, best = s, gi
        if best >= 0:
            groups[best].append(idx)
        else:
            reps.append(stmt)
            groups.append([idx])
    return groups


def cluster_embedding(principles: list[tuple[str, dict]], cos: float) -> list[list[int]]:
    from tools.subagent_factory.seed_principle_clusters import _cosine, embed_minilm

    embs = embed_minilm([str(p.get("statement", "")) for _sid, p in principles])
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


def merge_group(principles: list[tuple[str, dict]], idxs: list[int]) -> dict:
    members = [principles[i] for i in idxs]
    _, rep = max(members, key=lambda m: len(str(m[1].get("statement", ""))))
    sids = sorted({sid for sid, _ in members})
    derived = sorted({c for _, p in members for c in (p.get("derived_from_claims") or [])})
    applies: list[str] = []
    for _, p in members:
        for a in p.get("applies_when") or []:
            if a not in applies:
                applies.append(a)
    conf = max((p.get("confidence", "medium") for _, p in members), key=lambda c: _CONF.get(c, 1))
    return {
        "statement": rep.get("statement"),
        "source_ids": sids,
        "n_sources": len(sids),
        "derived_from_claims": derived,
        "confidence": conf,
        "applies_when": applies,
        "operational_mapping": rep.get("operational_mapping"),
    }


def importance(p: dict) -> tuple:
    # cross-book strength first, then evidence breadth, then confidence.
    return (p["n_sources"], len(p["derived_from_claims"]), _CONF.get(p["confidence"], 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.6, help="lexical token-F1 cutoff")
    ap.add_argument("--embeddings", action="store_true", help="use MiniLM cosine recall (C1)")
    ap.add_argument("--cos", type=float, default=0.55, help="embedding cosine cutoff")
    ap.add_argument("--select", type=int, default=0, help="keep top-N by importance (0=all)")
    ap.add_argument("--baseline", default="subagents/software-architecture")
    args = ap.parse_args()

    mods = load_modules()
    all_p = [(m["sid"], p) for m in mods for p in m["prins"]]
    all_c = [c for m in mods for c in m["claims"]]
    groups = (
        cluster_embedding(all_p, args.cos) if args.embeddings else cluster_lexical(all_p, args.threshold)
    )
    merged = [merge_group(all_p, g) for g in groups]
    merged.sort(key=importance, reverse=True)
    deduped_n = len(merged)
    if args.select > 0:
        merged = merged[: args.select]
    merged = [{"principle_id": f"P{i:03d}", **p} for i, p in enumerate(merged, 1)]

    (OUT / "analysis").mkdir(parents=True, exist_ok=True)
    (OUT / "principles").mkdir(parents=True, exist_ok=True)
    with open(OUT / "analysis" / "claims.jsonl", "w", encoding="utf-8") as f:
        for j, c in enumerate(all_c, 1):
            f.write(json.dumps({**c, "claim_id": f"C{j:05d}"}, ensure_ascii=False) + "\n")
    (OUT / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "principles-v1", "principles": merged},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    recall = f"embeddings cos>={args.cos}" if args.embeddings else f"token-F1>={args.threshold}"
    multi = sum(1 for p in merged if p["n_sources"] > 1)
    print(f"recall: {recall}   books: {len(mods)}")
    print(f"pre-merge: {len(all_c)} claims, {len(all_p)} principles")
    print(f"deduped:   {deduped_n} principles   selected: {len(merged)} ({multi} multi-source kept)")
    base = grounding_richness(str(REPO / args.baseline))
    p0 = grounding_richness(OUT)
    print("\n=== grounding-richness:  baseline v0.3.0  ->  P0 (deduped+selected) ===")
    for k in ("claims", "principles", "grounded_unigrams", "grounded_bigrams"):
        print(f"  {k:18s} {base[k]:6d}  ->  {p0[k]:6d}   ({p0[k] - base[k]:+d})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
