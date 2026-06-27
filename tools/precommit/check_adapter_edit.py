#!/usr/bin/env python3
"""Tier-1 pre-commit guard: generated adapters must stay generated.

pre-commit passes the staged adapter files (installed runtime adapters under
.claude/agents/generated/ and per-package adapters under subagents/*/adapters/).
Each must carry the DO-NOT-EDIT marker within its first lines — a file there
that lacks it was hand-written rather than produced by `cli export`, which
violates .claude/rules/generated-artifact-policy.md (rule 3).

This is a cheap shape check. Whether the adapter actually *matches* its
profile is verified by the full `cli validate` (adapter_policy_scan +
validate_adapter_quality) at pre-push / CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

MARKER = "GENERATED FILE. DO NOT EDIT DIRECTLY."
HEADER_LINES = 20
# Non-adapter files that legitimately live under the adapter dirs.
SKIP_NAMES = {"README.md"}


def main(argv: list[str]) -> int:
    offenders: list[str] = []
    for raw in argv:
        path = Path(raw)
        if path.name in SKIP_NAMES:
            continue
        if not path.is_file():
            # Deletion / rename — nothing to check.
            continue
        try:
            with path.open(encoding="utf-8", errors="replace") as fh:
                head = "".join(next(fh, "") for _ in range(HEADER_LINES))
        except OSError as exc:  # pragma: no cover - unreadable staged file
            offenders.append(f"{raw} (unreadable: {exc})")
            continue
        if MARKER not in head:
            offenders.append(raw)

    if offenders:
        print(
            "ERROR: generated adapter file(s) missing the DO-NOT-EDIT marker "
            f"in the first {HEADER_LINES} lines:",
            file=sys.stderr,
        )
        for o in offenders:
            print(f"  {o}", file=sys.stderr)
        print(
            "\nAdapters are derived artifacts. Do not hand-edit them — change\n"
            "subagents/<slug>/profile.yaml and re-run:  cli export <slug>\n"
            "\nEmergency bypass (discouraged): git commit --no-verify",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
