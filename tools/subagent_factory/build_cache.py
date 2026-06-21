"""Checkpoint / resume substrate for the per-book build (P1, per-book-authoring-upgrade.md).

Per-step completion markers with **input-fingerprinting** + **atomic writes**, so a capped/interrupted
build resumes (skip done steps) and a changed upstream invalidates the downstream marker (no stale
resume). NO LLM.

  atomic_write_text(path, text)        : write via tmp -> fsync -> rename (never a torn/half file).
  mark_done(step_dir, step, inputs)    : write <step>.done carrying the inputs' fingerprint + ts.
  is_done(step_dir, step, inputs)      : True iff <step>.done exists AND its fingerprint matches inputs.
  step_log(log_path, **fields)         : append one JSON line to a steps.log.jsonl run ledger.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from collections.abc import Iterable
from pathlib import Path


def fingerprint(inputs: Iterable[object]) -> str:
    h = hashlib.sha256()
    for x in inputs:
        h.update(str(x).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def atomic_write_text(path: str | Path, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    tmp.rename(p)


def mark_done(step_dir: str | Path, step: str, inputs: Iterable[object] = ()) -> None:
    atomic_write_text(
        Path(step_dir) / f"{step}.done",
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
