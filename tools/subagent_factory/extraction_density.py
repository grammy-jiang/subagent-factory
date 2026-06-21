"""Detect runaway per-book claim over-extraction (P3 #4 density guard, verify-gated).

A book module whose claims/chunk is far above the norm (~15-50) is capturing trivia — a claim per
sentence or per example (observed: sql-performance, 1,428 claims ≈ 357/chunk) — rather than the
load-bearing principles, which bloats claims.jsonl + evidence. This deterministic check flags such
modules so the operator re-MAPs them with a tighter check-worthiness filter. NO LLM.

Lib: density(module_dir, warn_per_chunk=80) -> dict
CLI: python -m tools.subagent_factory.extraction_density <module_dir> [...] [--warn-per-chunk N]
     (exit 1 if any module exceeds the threshold, so it can gate a build).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

_DEFAULT_WARN = 100  # claims/chunk above this = likely trivia over-extraction (coarse metric)


def density(module_dir: str | Path, warn_per_chunk: int = _DEFAULT_WARN) -> dict:
    d = Path(module_dir)
    mj = d / "module.json"
    sid = (
        json.loads(mj.read_text(encoding="utf-8")).get("source_id", d.name[:12])
        if mj.exists()
        else d.name[:12]
    )
    claims = (
        sum(1 for x in (d / "claims.jsonl").read_text(encoding="utf-8").splitlines() if x.strip())
        if (d / "claims.jsonl").exists()
        else 0
    )
    chunks = (
        sum(1 for x in (d / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if x.strip())
        if (d / "chunks.jsonl").exists()
        else 0
    )
    per = round(claims / chunks, 1) if chunks else float(claims)
    return {
        "source_id": sid,
        "claims": claims,
        "chunks": chunks,
        "per_chunk": per,
        "over": bool(chunks) and per > warn_per_chunk,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag per-book claim over-extraction (claims/chunk).")
    ap.add_argument("module_dir", nargs="+", type=Path)
    ap.add_argument("--warn-per-chunk", type=int, default=_DEFAULT_WARN)
    args = ap.parse_args()
    over = 0
    for d in args.module_dir:
        r = density(d, args.warn_per_chunk)
        flag = "OVER-EXTRACTED (re-MAP with tighter check-worthiness)" if r["over"] else "ok"
        print(
            f"{r['source_id']}: {r['claims']} claims / {r['chunks']} chunks = {r['per_chunk']}/chunk  {flag}"
        )
        over += int(r["over"])
    return 1 if over else 0


if __name__ == "__main__":
    raise SystemExit(main())
