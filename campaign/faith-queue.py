#!/usr/bin/env python3
"""List ready packages still missing a *valid* faithfulness report (no LLM).

Eligible = profile ``status: ready`` and no ``reports/faithfulness-report.yaml`` that passes
``validate_faithfulness_report``. Prints one slug per line. Used by faith-run.sh.

Usage: faith-queue.py [--only slug,slug,...]
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
    only: set[str] = set()
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--only" and i + 1 < len(args):
            only = {s for s in args[i + 1].split(",") if s}
            i += 2
        else:
            i += 1

    from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report

    for p in sorted(SUB.glob("*/profile.yaml")):
        slug = p.parent.name
        if only and slug not in only:
            continue
        try:
            prof = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if str(prof.get("status", "")).lower() != "ready":
            continue
        rep = p.parent / "reports" / "faithfulness-report.yaml"
        if rep.exists():
            try:
                if not validate_faithfulness_report(rep):  # [] == valid → already covered
                    continue
            except Exception:
                pass  # unparseable/invalid → needs (re)generation
        print(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
