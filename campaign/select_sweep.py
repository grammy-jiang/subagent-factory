#!/usr/bin/env python3
"""Measure how the distilled principle layer scales with --select, deterministically (no LLM, no
package clobber). For each select level it re-runs the REDUCE selection in memory and reports the
surfaced-principle count + the bytes those principle statements occupy (a proxy for the principle
contribution to adapter context).

CAVEAT printed in the output: the SHIPPED adapter's size is mostly LLM-authored prose
(Role/quality_bar/forbidden/examples) plus a compiled invariant layer whose membership the LLM sets
(confidence:high + profile_rule). This sweep measures the deterministic principle layer only; a true
end-to-end adapter-size comparison needs a finish run (p2b_finish) per level (LLM, expensive).

Usage: python3 campaign/select_sweep.py <slug> --sources campaign/<slug>.sources
       [--levels 0,0.25,0.5,0.75,1.0,50]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from tools.subagent_factory import map_reduce_build as mr  # noqa: E402
from tools.subagent_factory.reduce_principles import select_top  # noqa: E402

CACHE = REPO / "cache" / "book-extracts"


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic --select scaling sweep.")
    ap.add_argument("slug")
    ap.add_argument("--sources", required=True)
    ap.add_argument("--levels", default="0,0.25,0.5,0.75,1.0,50")
    ap.add_argument("--cos", type=float, default=0.55)
    args = ap.parse_args()

    srcs = [
        line.strip()
        for line in Path(args.sources).read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    mods = mr.load_modules(srcs, CACHE)
    cmap, claims = mr.build_claim_map(mods)
    gp = mr.globalize_principles(mods, cmap)
    groups = mr.recall_clusters(gp, mr._embed_minilm, args.cos)
    decisions = {i: {"action": "confirm"} for i in range(len(groups))}
    merged = mr.apply_decisions(gp, groups, decisions)
    pool = len(merged)

    print(
        f"\nslug={args.slug}  claims={len(claims)}  pre-merge principles={len(gp)}  pool(merged)={pool}\n"
    )
    print(f"{'level':>8} | {'surfaced':>8} | {'stmt_bytes':>10} | {'~stmt_tokens':>12}")
    print("-" * 48)
    levels = [float(x) for x in args.levels.split(",")]
    for lv in levels:
        sel = select_top(merged, lv)
        stmt_bytes = sum(len(str(p.get("statement", ""))) for p in sel)
        label = "all" if (not lv or lv <= 0) else (f"{lv:g}x" if lv < 1 else f"{int(lv)}")
        print(f"{label:>8} | {len(sel):>8} | {stmt_bytes:>10} | {stmt_bytes // 4:>12}")
    print(
        "\nNOTE: this is the deterministic principle layer only. The shipped adapter size is "
        "dominated by LLM-authored prose + a compiled invariant layer whose membership the finish "
        "step sets; a true adapter-byte comparison needs p2b_finish per level (LLM)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
