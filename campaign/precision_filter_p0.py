#!/usr/bin/env python3
"""P0 REDUCE precision filter — the LLM 'filter' half of recall-then-filter.

Embedding recall over-groups (similarity != equivalence). This adds the precision step the C1 design
intends (seed -> LLM confirm):

  emit  : deterministic embedding recall -> candidate MULTI-member clusters (reduce/clusters.json)
          + the full assembled principle list (reduce/principles_all.json).
  <LLM> : reads clusters.json, writes reduce/decisions.json — per cluster: confirm (+canonical) /
          split (+subgroups) / conflict.  (campaign/precision_filter.sh)
  apply : deterministic — rebuild the merged set from decisions (confirm->one multi-anchor;
          split->separate; conflict->keep both, tagged) + singletons -> importance-select -> measure.

Throwaway P0 harness (campaign/, outside the verify gate).

Run:
  python3 campaign/precision_filter_p0.py emit --cos 0.55
  bash    campaign/precision_filter.sh                       # LLM: clusters.json -> decisions.json
  python3 campaign/precision_filter_p0.py apply --select 50
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from tools.subagent_factory.grounding_check import grounding_richness

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "cache" / "book-extracts"
OUT = REPO / "cache" / "p0-build" / "software-architecture-p0"
WORK = OUT / "reduce"
_CONF = {"low": 0, "medium": 1, "high": 2}


def load_all_principles() -> list[dict]:
    ps: list[dict] = []
    for d in sorted(p for p in CACHE.iterdir() if p.is_dir() and not p.name.endswith("-copilot")):
        pp, mj = d / "principles.yaml", d / "module.json"
        if not pp.exists():
            continue
        sid = (json.loads(mj.read_text()) if mj.exists() else {}).get("source_id", d.name[:12])
        for p in (yaml.safe_load(pp.read_text()) or {}).get("principles") or []:
            ps.append(
                {
                    "pid": f"G{len(ps) + 1:04d}",
                    "source_id": sid,
                    "statement": str(p.get("statement", "")),
                    "derived_from_claims": p.get("derived_from_claims") or [],
                    "confidence": p.get("confidence", "medium"),
                    "applies_when": p.get("applies_when") or [],
                    "operational_mapping": p.get("operational_mapping"),
                }
            )
    return ps


def _greedy(embs: list[list[float]], cos: float) -> list[list[int]]:
    from tools.subagent_factory.seed_principle_clusters import _cosine

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


def _merge(members: list[dict]) -> dict:
    rep = max(members, key=lambda p: len(p["statement"]))
    sids = sorted({p["source_id"] for p in members})
    derived = sorted({c for p in members for c in p["derived_from_claims"]})
    applies: list[str] = []
    for p in members:
        for a in p["applies_when"]:
            if a not in applies:
                applies.append(a)
    conf = max((p["confidence"] for p in members), key=lambda c: _CONF.get(c, 1))
    return {
        "statement": rep["statement"],
        "source_ids": sids,
        "n_sources": len(sids),
        "derived_from_claims": derived,
        "confidence": conf,
        "applies_when": applies,
        "operational_mapping": rep["operational_mapping"],
    }


def _importance(p: dict) -> tuple:
    return (p["n_sources"], len(p["derived_from_claims"]), _CONF.get(p["confidence"], 1))


def emit(cos: float) -> None:
    from tools.subagent_factory.seed_principle_clusters import embed_minilm

    ps = load_all_principles()
    groups = _greedy(embed_minilm([p["statement"] for p in ps]), cos)
    multi = [g for g in groups if len(g) > 1]
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "principles_all.json").write_text(json.dumps(ps), encoding="utf-8")
    clusters = [
        {
            "cluster_id": f"K{i:02d}",
            "members": [
                {"pid": ps[idx]["pid"], "source_id": ps[idx]["source_id"], "statement": ps[idx]["statement"]}
                for idx in g
            ],
        }
        for i, g in enumerate(multi, 1)
    ]
    (WORK / "clusters.json").write_text(json.dumps(clusters, indent=1, ensure_ascii=False), encoding="utf-8")
    nmem = sum(len(c["members"]) for c in clusters)
    print(f"emit: {len(ps)} principles -> {len(clusters)} candidate clusters ({nmem} members) -> {WORK}/clusters.json")


def apply(select: int, baseline: str) -> None:
    ps = {p["pid"]: p for p in json.loads((WORK / "principles_all.json").read_text())}
    clusters = json.loads((WORK / "clusters.json").read_text())
    dpath = WORK / "decisions.json"
    decisions = (
        {d["cluster_id"]: d for d in json.loads(dpath.read_text())} if dpath.exists() else {}
    )
    if not dpath.exists():
        print(f"WARN: no {dpath} — every cluster treated as confirm (no precision filter applied)")
    clustered = {m["pid"] for c in clusters for m in c["members"]}
    stats = {"confirm": 0, "split": 0, "conflict": 0}
    final: list[dict] = [_merge([p]) for pid, p in ps.items() if pid not in clustered]
    for c in clusters:
        d = decisions.get(c["cluster_id"], {"action": "confirm"})
        act = d.get("action", "confirm")
        members = [ps[m["pid"]] for m in c["members"]]
        if act == "split":
            stats["split"] += 1
            covered: set[str] = set()
            for sg in d.get("subgroups") or [[m["pid"]] for m in c["members"]]:
                final.append(_merge([ps[p] for p in sg if p in ps]))
                covered |= set(sg)
            final += [_merge([ps[m["pid"]]]) for m in c["members"] if m["pid"] not in covered]
        elif act == "conflict":
            stats["conflict"] += 1
            for m in c["members"]:
                mp = _merge([ps[m["pid"]]])
                mp["conflict_cluster"] = c["cluster_id"]
                final.append(mp)
        else:
            stats["confirm"] += 1
            mp = _merge(members)
            if d.get("canonical"):
                mp["statement"] = d["canonical"]
            final.append(mp)

    final.sort(key=_importance, reverse=True)
    deduped = len(final)
    if select > 0:
        final = final[:select]
    final = [{"principle_id": f"P{i:03d}", **p} for i, p in enumerate(final, 1)]

    (OUT / "principles").mkdir(parents=True, exist_ok=True)
    (OUT / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "principles-v1", "principles": final}, sort_keys=False, allow_unicode=True
        ),
        encoding="utf-8",
    )
    multi = sum(1 for p in final if p["n_sources"] > 1)
    print(f"decisions: {stats}   deduped {deduped} -> selected {len(final)} ({multi} multi-source)")
    base = grounding_richness(str(REPO / baseline))
    p0 = grounding_richness(OUT)
    print("\n=== grounding-richness:  baseline v0.3.0  ->  P0 (filtered+selected) ===")
    for k in ("principles", "grounded_unigrams", "grounded_bigrams"):
        print(f"  {k:18s} {base[k]:6d}  ->  {p0[k]:6d}   ({p0[k] - base[k]:+d})")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("emit")
    e.add_argument("--cos", type=float, default=0.55)
    a = sub.add_parser("apply")
    a.add_argument("--select", type=int, default=50)
    a.add_argument("--baseline", default="subagents/software-architecture")
    args = ap.parse_args()
    if args.cmd == "emit":
        emit(args.cos)
    else:
        apply(args.select, args.baseline)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
