#!/usr/bin/env python3
"""P0 REDUCE prototype: merge per-book MAP modules -> deduped principle set + measure vs baseline.

This is the DETERMINISTIC RECALL stage of the recall-then-filter merge (per-book-authoring-upgrade.md):
cluster per-book principles by token-F1 statement similarity (claim_recall.claim_f1) into multi-anchor
principles, assemble a pseudo-package (claims.jsonl + principles.yaml), and compare grounding-richness
to the current batch baseline. The LLM PRECISION FILTER (confirm/split near-duplicate clusters) is the
next refinement; this prototype reports the deterministic-recall merge so we can see whether the
per-book MAP wins on richness BEFORE investing in the filter.

Throwaway P0 harness (lives in campaign/, outside the make-verify gate). Reads every module under
cache/book-extracts/ that has a principles.yaml (currently only the software-architecture run).

Run: python3 campaign/merge_principles_p0.py [--threshold 0.6] [--baseline subagents/software-architecture]
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
    for d in sorted(p for p in CACHE.iterdir() if p.is_dir()):
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


def cluster(principles: list[tuple[str, dict]], threshold: float) -> list[dict]:
    """Greedy single-pass clustering of (source_id, principle) by statement token-F1 (recall stage)."""
    clusters: list[dict] = []
    for sid, p in principles:
        stmt = str(p.get("statement", ""))
        best, best_s = None, 0.0
        for c in clusters:
            s = claim_f1(stmt, c["rep"])
            if s > best_s:
                best_s, best = s, c
        if best is not None and best_s >= threshold:
            best["members"].append((sid, p))
        else:
            clusters.append({"rep": stmt, "members": [(sid, p)]})
    return clusters


def merge_cluster(c: dict) -> dict:
    members = c["members"]
    _, rep = max(members, key=lambda m: len(str(m[1].get("statement", ""))))
    sids = sorted({sid for sid, _ in members})
    derived = sorted({cid for _, p in members for cid in (p.get("derived_from_claims") or [])})
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


def assemble(threshold: float) -> tuple[list[dict], list[tuple[str, dict]], list[dict], list[dict]]:
    mods = load_modules()
    all_p = [(m["sid"], p) for m in mods for p in m["prins"]]
    all_c = [c for m in mods for c in m["claims"]]
    merged = [merge_cluster(c) for c in cluster(all_p, threshold)]
    merged.sort(key=lambda p: (-p["n_sources"], -len(p["derived_from_claims"])))
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
    return mods, all_p, all_c, merged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.6)
    ap.add_argument("--baseline", default="subagents/software-architecture")
    args = ap.parse_args()
    mods, all_p, all_c, merged = assemble(args.threshold)
    print("=== per-book MAP modules ===")
    for m in sorted(mods, key=lambda m: -len(m["claims"])):
        print(f"  {len(m['claims']):4d} claims  {len(m['prins']):3d} prin  {m['title'][:50]}")
    multi = sum(1 for p in merged if p["n_sources"] > 1)
    print(f"\npre-merge: {len(all_c)} claims, {len(all_p)} principles across {len(mods)} books")
    print(
        f"merged @F1>={args.threshold}: {len(merged)} principles "
        f"({multi} multi-source = cross-book / strengthened)"
    )
    base = grounding_richness(str(REPO / args.baseline))
    p0 = grounding_richness(OUT)
    print("\n=== grounding-richness:  baseline v0.3.0  ->  P0 map-reduce ===")
    for k in ("claims", "principles", "grounded_unigrams", "grounded_bigrams"):
        print(f"  {k:18s} {base[k]:6d}  ->  {p0[k]:6d}   ({p0[k] - base[k]:+d})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
