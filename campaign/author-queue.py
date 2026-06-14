#!/usr/bin/env python3
"""List draft packages eligible for the authoring campaign (no LLM).

Eligible = profile ``status: draft``, ``tier >= TIER_MIN``, and the package
currently **validates** — so incomplete/broken packages (e.g. an interrupted
build leaving no adapter) are skipped: they need repair, not authoring. Ordered
tier-desc then name (richest grounding first). Prints one slug per line.

Usage: author-queue.py [TIER_MIN] [--only slug,slug,...]
       (--only is explicit selection and bypasses TIER_MIN — a named Tier-0 draft still lists.)
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SUB = REPO / "subagents"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def main() -> int:
    tier_min = 1
    only: set[str] = set()
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--only" and i + 1 < len(args):
            only = {s for s in args[i + 1].split(",") if s}
            i += 2
        elif a.isdigit():
            tier_min = int(a)
            i += 1
        else:
            i += 1

    from tools.subagent_factory.validate_generated_package import validate_generated_package

    rows: list[tuple[int, str]] = []
    for p in sorted(SUB.glob("*/profile.yaml")):
        slug = p.parent.name
        if only and slug not in only:
            continue
        try:
            prof = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if str(prof.get("status", "")).lower() != "draft":
            continue
        try:
            tier = int(prof.get("tier", 0) or 0)
        except (TypeError, ValueError):
            tier = 0
        # --only is explicit selection: honour it regardless of tier_min (so a Tier-0 draft named
        # by --only is not silently dropped). tier_min only filters the unfiltered "all" queue.
        if not only and tier < tier_min:
            continue
        try:
            if not validate_generated_package(p.parent).get("passed"):
                continue  # incomplete/broken → repair, don't author
        except Exception:
            continue
        rows.append((tier, slug))

    rows.sort(key=lambda r: (-r[0], r[1]))
    for _tier, slug in rows:
        print(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
