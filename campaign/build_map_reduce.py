#!/usr/bin/env python3
"""Turnkey slug-agnostic map->reduce build (P3 #1) — one command, checkpointed + resumable.

Stitches the whole per-book pipeline for ANY package slug, using the verify-gated tools
(`route_books`, `chunk_source`, `emit_chunk_anchors`, `map_reduce_build`) for the deterministic work
and **gating** on the two LLM steps (per-book MAP, precision filter): if their artifact is missing the
build prints the exact command and stops, so it never silently spends on an LLM. Re-run with --resume
to continue (per-step `.done` + `steps.log.jsonl` under `subagents/<slug>/.build/`). Supersedes the
software-architecture-p0-specific `build_p0.py`.

Flow:  route -> chunk -> [MAP gate] -> anchors -> reduce-emit(clusters.json) -> [filter gate] -> assemble
Run:   python3 campaign/build_map_reduce.py <slug> --sources <dir|file> [--resume] [--select N] [--cos C]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from tools.subagent_factory import chunk_source, map_reduce_build  # noqa: E402
from tools.subagent_factory.build_cache import is_done, mark_done, step_log  # noqa: E402
from tools.subagent_factory.emit_chunk_anchors import emit_anchors  # noqa: E402
from tools.subagent_factory.route_books import _gather, route_books  # noqa: E402

CACHE = REPO / "cache" / "book-extracts"


def _sha(p: str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Turnkey slug-agnostic map->reduce build.")
    ap.add_argument("slug")
    ap.add_argument("--sources", required=True, help="newline file of md paths, or a dir of *.md")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument(
        "--select",
        type=float,
        default=0.25,
        help="principles to surface, importance-ranked. FRACTION (0<n<1, default 0.25 = top quarter "
        "of the pool — measured best grounding/size tradeoff over 6 external files), COUNT (>=1, e.g. "
        "50 focused / 150 comprehensive), or 0 = all merged/deduplicated principles.",
    )
    ap.add_argument("--cos", type=float, default=0.55)
    ap.add_argument("--threshold-tokens", type=int, default=100_000)
    args = ap.parse_args()

    bdir = REPO / "subagents" / args.slug / ".build"
    bdir.mkdir(parents=True, exist_ok=True)
    log = bdir / "steps.log.jsonl"
    seen: dict[str, str] = {}
    for s in _gather(args.sources):
        seen.setdefault(_sha(s), s)
    sources = list(seen.values())
    shas = list(seen.keys())

    def do(step: str, inputs: list, fn) -> bool:
        if args.resume and is_done(bdir, step, inputs):
            print(f"  [skip] {step}")
            step_log(log, step=step, status="skip")
            return True
        print(f"  [run ] {step}")
        ok = fn()
        step_log(log, step=step, status="ok" if ok else "gate")
        if ok:
            mark_done(bdir, step, inputs)
        return ok

    def _route() -> bool:
        rows = route_books(sources, args.threshold_tokens)
        (bdir / "routing.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
        n = sum(1 for r in rows if r["class"] == "small")
        print(f"      {len(rows)} books -> {n} copilot / {len(rows) - n} claude")
        return True

    def _chunk() -> bool:
        for s in sources:
            chunk_source.write_book_module(Path(s), CACHE)
        return True

    def _map() -> bool:
        missing = [
            s
            for s, sha in zip(sources, shas, strict=False)
            if not (CACHE / sha / "principles.yaml").exists()
        ]
        if missing:
            eng = {r["source"]: r["engine"] for r in route_books(missing, args.threshold_tokens)}
            print("      MAP incomplete — run these, then re-run --resume:")
            for s in missing:
                print(
                    f"        bash campaign/map_book.sh --book {s} --engine {eng.get(s, 'claude')} --fg"
                )
            return False
        from tools.subagent_factory.extraction_density import density

        for sha in shas:
            r = density(CACHE / sha)
            if r["over"]:
                print(
                    f"      WARN over-extraction: {r['source_id']} = {r['per_chunk']}/chunk"
                    " — consider re-MAP with a tighter check-worthiness filter"
                )
        print(f"      MAP complete for all {len(sources)} books")
        return True

    def _anchors() -> bool:
        for sha in shas:
            emit_anchors(CACHE / sha)
        return True

    def _reduce_emit() -> bool:
        mods = map_reduce_build.load_modules(sources, CACHE)
        cmap, _ = map_reduce_build.build_claim_map(mods)
        gp = map_reduce_build.globalize_principles(mods, cmap)
        clusters = map_reduce_build.emit_clusters(gp, map_reduce_build._embed_minilm, args.cos)
        (bdir / "clusters.json").write_text(
            json.dumps(clusters, indent=1, ensure_ascii=False), encoding="utf-8"
        )
        print(
            f"      {len(gp)} principles -> {len(clusters)} candidate clusters -> .build/clusters.json"
        )
        return True

    def _filter() -> bool:
        if (bdir / "decisions.json").exists():
            print("      precision filter complete (.build/decisions.json)")
            return True
        print("      precision filter incomplete — run the LLM filter over .build/clusters.json")
        print(
            "      -> write .build/decisions.json (group-index -> {action: confirm|split|conflict, ...}), then --resume"
        )
        return False

    def _assemble() -> bool:
        dec = {int(k): v for k, v in json.loads((bdir / "decisions.json").read_text()).items()}
        summary = map_reduce_build.assemble(
            args.slug,
            sources,
            repo=REPO,
            embedder=map_reduce_build._embed_minilm,
            cos=args.cos,
            decisions=dec,
            select=args.select,
        )
        print(f"      assembled distilled layer: {summary}")
        return True

    do("route", sources, _route)
    do("chunk", sources, _chunk)
    if not do("map", shas, _map):
        print("BUILD GATED at MAP.")
        return 1
    do("anchors", shas, _anchors)
    do("reduce-emit", shas, _reduce_emit)
    if not do("filter", [str(bdir / "clusters.json")], _filter):
        print("BUILD GATED at precision-filter.")
        return 1
    do("assemble", [str(bdir / "decisions.json"), args.select], _assemble)
    print(
        f"\nMAP->REDUCE distilled layer built for '{args.slug}'. Continue at author-subagent Step 7+."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
