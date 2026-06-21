#!/usr/bin/env python3
"""P2a deterministic package assembly — focused P0 set -> an installable package scaffold.

Reuses the baseline package's scaffold (sources/, manifest, provenance, profile, tests, skills,
adapter — the 9 source_ids are identical because same book -> same sha -> same id) and OVERWRITES the
distilled layer with the P0 map->reduce output:
  - analysis/claims.jsonl : all per-book claims, GLOBALLY renumbered (C00001..), source-attributed;
  - principles/principles.yaml : the focused 50 (precision-filtered + selected), with
    derived_from_claims rewritten to the global ids (the renumber-consistency fix);
  - evidence/evidence-records.yaml : one record per claim backing a kept principle;
  - sources/anchors/<sid>.anchors.jsonl : the chunk (paragraph) anchors the claims resolve against.
Then runs validate_generated_package to expose the remaining P2b gaps (faithfulness/profile/tests/skills).

Run: python3 campaign/assemble_package_p0.py [--slug software-architecture-p0] [--select 50]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "campaign"))
import precision_filter_p0 as pf  # noqa: E402  (reuse _merge/_importance + cluster apply)

CACHE = REPO / "cache" / "book-extracts"
REDUCE = REPO / "cache" / "p0-build" / "software-architecture-p0" / "reduce"
BASE = REPO / "subagents" / "software-architecture"


def _modules() -> list[Path]:
    return [
        d
        for d in sorted(CACHE.iterdir())
        if d.is_dir() and not d.name.endswith("-copilot") and (d / "module.json").exists()
    ]


def build_claim_map() -> tuple[dict[tuple[str, str], str], list[dict]]:
    """(source_id, per-book claim_id) -> global C##### ; plus all claims renumbered globally."""
    cmap: dict[tuple[str, str], str] = {}
    claims: list[dict] = []
    for d in _modules():
        sid = json.loads((d / "module.json").read_text())["source_id"]
        for line in (d / "claims.jsonl").read_text().splitlines():
            if not line.strip():
                continue
            c = json.loads(line)
            gid = f"C{len(claims) + 1:05d}"
            cmap[(sid, c["claim_id"])] = gid
            c["claim_id"] = gid
            claims.append(c)
    return cmap, claims


def globalize_and_merge(cmap: dict, select: int) -> list[dict]:
    ps = json.loads((REDUCE / "principles_all.json").read_text())
    for p in ps:
        p["derived_from_claims"] = [
            cmap[(p["source_id"], c)] for c in p["derived_from_claims"] if (p["source_id"], c) in cmap
        ]
    by_pid = {p["pid"]: p for p in ps}
    clusters = json.loads((REDUCE / "clusters.json").read_text())
    decisions = {d["cluster_id"]: d for d in json.loads((REDUCE / "decisions.json").read_text())}
    clustered = {m["pid"] for c in clusters for m in c["members"]}
    final = [pf._merge([p]) for pid, p in by_pid.items() if pid not in clustered]
    for c in clusters:
        d = decisions.get(c["cluster_id"], {"action": "confirm"})
        members = [by_pid[m["pid"]] for m in c["members"]]
        act = d.get("action", "confirm")
        if act == "split":
            covered: set[str] = set()
            for sg in d.get("subgroups") or [[m["pid"]] for m in c["members"]]:
                final.append(pf._merge([by_pid[p] for p in sg if p in by_pid]))
                covered |= set(sg)
            final += [pf._merge([by_pid[m["pid"]]]) for m in c["members"] if m["pid"] not in covered]
        elif act == "conflict":
            final += [pf._merge([by_pid[m["pid"]]]) for m in c["members"]]
        else:
            mp = pf._merge(members)
            if d.get("canonical"):
                mp["statement"] = d["canonical"]
            final.append(mp)
    final.sort(key=pf._importance, reverse=True)
    final = final[:select] if select > 0 else final
    out = []
    for i, p in enumerate(final, 1):
        out.append(
            {
                "principle_id": f"P{i:03d}",
                "statement": p["statement"],
                "derived_from_claims": p["derived_from_claims"],
                "confidence": p["confidence"],
                "applies_when": p["applies_when"] or ["Architecture review or decision in scope"],
                "operational_mapping": p["operational_mapping"] or {"profile_rule": True},
            }
        )
    return out


def evidence_for(principles: list[dict], claims_by_id: dict[str, dict]) -> list[dict]:
    wanted = sorted({c for p in principles for c in p["derived_from_claims"]})
    recs = []
    for i, cid in enumerate(wanted, 1):
        c = claims_by_id.get(cid)
        if not c:
            continue
        recs.append(
            {
                "evidence_id": f"E{i:05d}",
                "claim_id": cid,
                "source_ids": [c["source_id"]],
                "source_anchors": c.get("source_anchors") or [],
                "support_granularity": c.get("support_granularity") or "paragraph",
                "evidence_type": c.get("evidence_type") or "expert",
                "evidence_strength": "moderate",
                "support_level": "entailed",
                "confidence": c.get("confidence_initial") or "medium",
                "quote_allowed": False,
                "limitations": "Distilled paraphrase; bound to a chunk-level (paragraph) anchor.",
            }
        )
    return recs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="software-architecture-p0")
    ap.add_argument("--select", type=int, default=50)
    args = ap.parse_args()
    pkg = REPO / "subagents" / args.slug

    cmap, claims = build_claim_map()
    claims_by_id = {c["claim_id"]: c for c in claims}
    principles = globalize_and_merge(cmap, args.select)
    evidence = evidence_for(principles, claims_by_id)

    if pkg.exists():
        shutil.rmtree(pkg)
    shutil.copytree(BASE, pkg)  # scaffold: sources/, manifest, provenance, profile, tests, skills, adapter

    (pkg / "analysis").mkdir(exist_ok=True)
    with open(pkg / "analysis" / "claims.jsonl", "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    (pkg / "principles" / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (pkg / "evidence" / "evidence-records.yaml").write_text(
        yaml.safe_dump({"schema_version": "evidence-records-v1", "evidence_records": evidence}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    # swap in the chunk-anchor indices (claims resolve against these)
    for d in _modules():
        sid = json.loads((d / "module.json").read_text())["source_id"]
        if (d / "anchors.jsonl").exists():
            shutil.copyfile(d / "anchors.jsonl", pkg / "sources" / "anchors" / f"{sid}.anchors.jsonl")
    # retarget slug in manifest/provenance/profile
    for rel in ("source-pack.manifest.yaml", "provenance-ledger.md", "profile.yaml"):
        p = pkg / rel
        p.write_text(p.read_text(encoding="utf-8").replace("software-architecture", args.slug), encoding="utf-8")

    print(f"assembled: {len(claims)} claims, {len(principles)} principles, {len(evidence)} evidence -> {pkg}")
    print("=== validate_generated_package (expect P2b gaps: faithfulness/profile/tests/skills) ===")
    subprocess.run([sys.executable, "-m", "tools.subagent_factory.validate_generated_package", str(pkg)], cwd=REPO)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
