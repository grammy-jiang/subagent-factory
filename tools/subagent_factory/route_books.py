"""Deterministic engine router for per-book MAP (P1, per-book-authoring-upgrade.md).

Classifies each staged book by size and assigns an engine for its whole-book MAP session:
small (<= threshold) -> **copilot** (the whole session fits its ~200k window with headroom, and a
small book is one cheap premium-request unit); large (> threshold) -> **claude** (~1M, no compaction).
The ~100k-token threshold is conservative (leaves room for the accumulating extraction output so a
Copilot session never compacts). NO LLM.

CLI:  python -m tools.subagent_factory.route_books <sources-file|dir> [--threshold-tokens N] [--json]
Lib:  route_books(paths, threshold_tokens=100_000) -> list[dict]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

_CHARS_PER_TOKEN = 4
_DEFAULT_THRESHOLD = 100_000  # tokens; <= -> copilot, > -> claude


def classify(md_path: Path, threshold_tokens: int = _DEFAULT_THRESHOLD) -> dict:
    tokens = md_path.stat().st_size // _CHARS_PER_TOKEN  # bytes ~ chars; ample for a size class
    klass = "small" if tokens <= threshold_tokens else "large"
    return {
        "source": str(md_path),
        "title": md_path.stem,
        "est_tokens": tokens,
        "class": klass,
        "engine": "copilot" if klass == "small" else "claude",
    }


def route_books(
    paths: Sequence[str | Path], threshold_tokens: int = _DEFAULT_THRESHOLD
) -> list[dict]:
    return [classify(Path(p), threshold_tokens) for p in paths]


def _gather(arg: str) -> list[str]:
    p = Path(arg)
    if p.is_dir():
        return sorted(str(x) for x in p.glob("*.md"))
    return [
        ln.strip()
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic small/large -> engine router.")
    ap.add_argument("src", help="sources file (newline md paths) or a directory of *.md")
    ap.add_argument("--threshold-tokens", type=int, default=_DEFAULT_THRESHOLD)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = route_books(_gather(args.src), args.threshold_tokens)
    if args.json:
        print(json.dumps(rows, indent=1))
        return 0
    for r in sorted(rows, key=lambda r: -r["est_tokens"]):
        print(
            f"  ~{r['est_tokens']:7d} tok  {r['class']:5s} -> {r['engine']:7s}  {Path(r['source']).name[:50]}"
        )
    n_small = sum(1 for r in rows if r["class"] == "small")
    print(f"{len(rows)} books: {n_small} small->copilot, {len(rows) - n_small} large->claude")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
