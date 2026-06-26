"""Checkpoint / resume substrate for the per-book build (P1, per-book-authoring-upgrade.md).

Per-step completion markers with **input-fingerprinting** + **atomic writes**, so a capped/interrupted
build resumes (skip done steps) and a changed upstream invalidates the downstream marker (no stale
resume). NO LLM.

  atomic_write_text(path, text)        : re-exported from _common (single owner; unique sibling temp + os.replace).
  mark_done(step_dir, step, inputs)    : write <step>.done carrying the inputs' fingerprint + ts.
  is_done(step_dir, step, inputs)      : True iff <step>.done exists AND its fingerprint matches inputs.
  step_log(log_path, **fields)         : append one JSON line to a steps.log.jsonl run ledger.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterable
from pathlib import Path

# Single owner of the atomic-write pattern (P010). Re-exported so existing
# `from build_cache import atomic_write_text` call sites keep working.
from tools.subagent_factory._common import atomic_write_text

__all__ = ["atomic_write_text", "fingerprint", "is_done", "mark_done", "step_log"]


def fingerprint(inputs: Iterable[object]) -> str:
    h = hashlib.sha256()
    for x in inputs:
        h.update(str(x).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def mark_done(step_dir: str | Path, step: str, inputs: Iterable[object] = ()) -> None:
    target = Path(step_dir) / f"{step}.done"
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(
        target,
        json.dumps({"step": step, "fp": fingerprint(inputs), "ts": time.time()}),
    )


def is_done(step_dir: str | Path, step: str, inputs: Iterable[object] = ()) -> bool:
    p = Path(step_dir) / f"{step}.done"
    if not p.exists():
        return False
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("fp") == fingerprint(inputs)
    except (OSError, json.JSONDecodeError):
        return False


def step_log(log_path: str | Path, **fields: object) -> None:
    fields.setdefault("ts", time.time())
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(fields) + "\n")
