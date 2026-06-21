#!/usr/bin/env python3
"""P1 build orchestrator — route -> chunk -> MAP -> anchors -> REDUCE, checkpointed + resumable.

Ties the per-book pipeline together with per-step `.done` markers (build_cache) under
`subagents/<slug>/.build/` + a `steps.log.jsonl` ledger, so an interrupted/capped build resumes
(skip-done) and a changed input invalidates the downstream marker. Deterministic steps run here; the
two LLM steps (per-book MAP, precision filter) are **gates** — if their artifact is missing the build
prints the exact command to run and stops, so this orchestrator never silently spends on an LLM.

Run: python3 campaign/build_p0.py <slug> --sources <dir|file> [--resume] [--select N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from tools.subagent_factory import chunk_source  # noqa: E402
from tools.subagent_factory.build_cache import (  # noqa: E402
    atomic_write_text,
    is_done,
    mark_done,
    step_log,
)
from tools.subagent_factory.route_books import _gather, route_books  # noqa: E402

CACHE = REPO / "cache" / "book-extracts"
REDUCE = REPO / "cache" / "p0-build" / "software-architecture-p0" / "reduce"


def _sha(p: str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _run(cmd: list[str]) -> bool:
    return subprocess.run(cmd, cwd=REPO).returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--sources", required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--threshold-tokens", type=int, default=100_000)
    ap.add_argument("--select", type=int, default=50)
    args = ap.parse_args()

    bdir = REPO / "subagents" / args.slug / ".build"
    bdir.mkdir(parents=True, exist_ok=True)
    log = bdir / "steps.log.jsonl"
    seen: dict[str, str] = {}
    for b in _gather(args.sources):
        seen.setdefault(_sha(b), b)
    books = list(seen.values())
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
        rows = route_books(books, args.threshold_tokens)
        atomic_write_text(bdir / "routing.json", json.dumps(rows, indent=1))
        n = sum(1 for r in rows if r["class"] == "small")
        print(f"      {len(rows)} books -> {n} copilot / {len(rows) - n} claude")
        return True

    def _chunk() -> bool:
        for b in books:
            chunk_source.write_book_module(Path(b), CACHE)
        return True

    def _map() -> bool:
        missing = [b for b, s in zip(books, shas, strict=False) if not (CACHE / s / "principles.yaml").exists()]
        if missing:
            print("      MAP incomplete — run, then re-run --resume:")
            for b in missing:
                print(f"        bash campaign/map_book.sh --book {b} --fg")
            return False
        print(f"      MAP complete for all {len(books)} books")
        return True

    def _filter() -> bool:
        if (REDUCE / "decisions.json").exists():
            print("      precision filter complete")
            return True
        print("      precision filter incomplete — run: bash campaign/precision_filter.sh --fg")
        return False

    do("route", books, _route)
    do("chunk", books, _chunk)
    if not do("map", shas, _map):
        print("BUILD GATED at MAP.")
        return 1
    do("anchors", shas, lambda: _run(["python3", "campaign/emit_anchors_p0.py"]))
    do("reduce-emit", shas, lambda: _run(["python3", "campaign/precision_filter_p0.py", "emit", "--cos", "0.55"]))
    if not do("filter", [str(REDUCE / "clusters.json")], _filter):
        print("BUILD GATED at precision-filter.")
        return 1
    do(
        "reduce-apply",
        [str(REDUCE / "decisions.json"), args.select],
        lambda: _run(["python3", "campaign/precision_filter_p0.py", "apply", "--select", str(args.select)]),
    )
    print(f"\nBUILD COMPLETE (slug={args.slug}).  checkpoints+log: {bdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
