#!/usr/bin/env python3
"""Per-run extraction-dilution experiment on software-architecture books (throwaway slugs).

A — initial batch size: author from scratch over 1 / 3 / 5 books, measure claims/book.
B — increment size: from a fixed [B1] base, add 1 / 3 / 5 books, measure Δclaims/book-added.
Metric: grounding-richness (deterministic). All runs on Claude (no Copilot cap). Slugs ax-* are
throwaway — delete after with: rm -rf subagents/ax-* .claude/agents/generated/ax-*.md
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from tools.subagent_factory.grounding_check import grounding_richness

REPO = Path(__file__).resolve().parent.parent
STAGE = REPO / "campaign" / "staging" / "software-architecture"
CAMP = REPO / "campaign"
TOPIC = "software architecture reviewer"

# Ordered pool B1..B6 (substring -> staged md), so a count maps to a deterministic subset.
WANT = [
    "fundamentals-of-software-architecture",
    "clean-architecture",
    "hard-parts",
    "patterns-of-enterprise-application",
    "software-architecture-patterns",
    "designing-event-driven",
]


def pool() -> list[Path]:
    md = list(STAGE.glob("*.md"))
    out = []
    for key in WANT:
        m = [p for p in md if key in p.name]
        if not m:
            print(f"MISSING staged md for '{key}'", file=sys.stderr)
            sys.exit(3)
        out.append(m[0])
    return out


def write_sources(name: str, paths: list[Path]) -> Path:
    f = CAMP / f"{name}.sources"
    f.write_text("".join(f"{p}\n" for p in paths), encoding="utf-8")
    return f


def sh(cmd: list[str]) -> int:
    print("  $", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=REPO).returncode


def richness(slug: str) -> dict:
    return grounding_richness(REPO / "subagents" / slug)


def main() -> int:
    B = pool()
    results: list[tuple[str, int, dict]] = []  # (label, n_books, richness)

    # --- Experiment A: batch size 1 / 3 / 5 ---
    for n in (1, 3, 5):
        slug = f"ax-b{n}"
        write_sources(slug, B[:n])
        print(f"\n=== A batch-{n}: author {slug} from scratch ({n} books) ===", flush=True)
        sh(["bash", str(CAMP / "generate-subagent.sh"), "--fg", "--slug", slug,
            "--topic", TOPIC, "--sources-file", str(CAMP / f"{slug}.sources")])
        r = richness(slug)
        results.append((f"A batch-{n}", n, r))
        print(f"   -> claims={r['claims']} ({r['claims']/n:.1f}/book) bigrams={r['grounded_bigrams']}", flush=True)

    # base for B = ax-b1 ([B1]); snapshot it so each increment arm starts identical.
    snap = Path("/tmp/ax-base-snap")
    if snap.exists():
        shutil.rmtree(snap)
    shutil.copytree(REPO / "subagents" / "ax-b1", snap)
    base_claims = richness("ax-b1")["claims"]

    # --- Experiment B: increment size 1 / 3 / 5 (restore base each time) ---
    for n in (1, 3, 5):
        # restore base
        shutil.rmtree(REPO / "subagents" / "ax-b1")
        shutil.copytree(snap, REPO / "subagents" / "ax-b1")
        write_sources("ax-b1-new", B[1 : 1 + n])  # add B2..B(1+n)
        print(f"\n=== B add-{n}: base[B1] + add {n} books ===", flush=True)
        sh(["bash", str(CAMP / "add-source.sh"), "--fg", "--slug", "ax-b1",
            "--sources-file", str(CAMP / "ax-b1-new.sources")])
        r = richness("ax-b1")
        delta = r["claims"] - base_claims
        results.append((f"B add-{n}", n, r))
        print(f"   -> claims={r['claims']} (+{delta}, {delta/n:.1f}/book-added) bigrams={r['grounded_bigrams']}", flush=True)

    print("\n===DILUTION_RESULTS===")
    print(f"base[B1] claims = {base_claims}")
    for label, n, r in results:
        per = (r["claims"] / n) if label.startswith("A") else ((r["claims"] - base_claims) / n)
        print(f"{label:12s} books={n} claims={r['claims']:4d} prin={r['principles']:3d} bi={r['grounded_bigrams']:4d} per-book={per:.1f}")
    print("===END===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
