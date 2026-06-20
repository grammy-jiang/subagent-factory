#!/usr/bin/env python3
"""P2 spike: emit a chunk-level anchor index for each per-book MAP module + prove resolution.

The anchor reconciliation unknown: P0 claims anchor to chunk_ids (`<sha12>-c0001`); the factory's
provenance system needs a `source-anchor-index-v1` JSONL whose records the claims resolve against.
`anchor_type` allows "paragraph", so each chunk becomes a paragraph-anchor (coarser than the baseline's
heading anchors, but a valid, resolvable provenance unit). Emits one anchors.jsonl per module, runs
validate_anchor_index, and checks every claim's source_anchors resolve.

Run: python3 campaign/emit_anchors_p0.py
"""
from __future__ import annotations

import json
from pathlib import Path

from tools.subagent_factory.validate_anchor_index import validate_anchor_index

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "cache" / "book-extracts"


def emit_for_module(d: Path) -> tuple[str, set[str], list[str]]:
    meta = json.loads((d / "module.json").read_text())
    sid = meta["source_id"]
    src = (d / "source.md").read_text(encoding="utf-8")
    chunks = [json.loads(x) for x in (d / "chunks.jsonl").read_text().splitlines() if x.strip()]
    out = d / "anchors.jsonl"
    ids: set[str] = set()
    with open(out, "w", encoding="utf-8") as f:
        for c in chunks:
            line_no = src[: c["char_start"]].count("\n") + 1
            rec = {
                "schema_version": "source_anchor_v1",
                "anchor_id": c["chunk_id"],
                "source_id": sid,
                "anchor_type": "paragraph",
                "level": None,
                "text": (c.get("heading_path") or "(chunk)")[:280],
                "line_number": line_no,
                "page_number": None,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            ids.add(c["chunk_id"])
    errs = validate_anchor_index(out)
    return sid, ids, errs


def main() -> int:
    mods = [
        d
        for d in sorted(CACHE.iterdir())
        if d.is_dir() and not d.name.endswith("-copilot") and (d / "module.json").exists()
    ]
    all_ids: set[str] = set()
    total_err = 0
    for d in mods:
        sid, ids, errs = emit_for_module(d)
        all_ids |= ids
        total_err += len(errs)
        flag = "OK" if not errs else f"{len(errs)} ERR"
        print(f"  {sid:28s} {len(ids):3d} anchors  validate:{flag}")
        for e in errs[:2]:
            print("     ", e[:100])
    # resolution: every claim's source_anchors must be an emitted anchor_id
    miss = 0
    nclaims = 0
    for d in mods:
        cl = d / "claims.jsonl"
        if not cl.exists():
            continue
        for line in cl.read_text().splitlines():
            if not line.strip():
                continue
            nclaims += 1
            for a in json.loads(line).get("source_anchors") or []:
                if a not in all_ids:
                    miss += 1
    print(f"\nanchor-index validate errors: {total_err}")
    print(f"claims: {nclaims}  unresolved source_anchors: {miss}")
    print("ANCHOR RECONCILIATION:", "PASS" if (total_err == 0 and miss == 0) else "FAIL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
