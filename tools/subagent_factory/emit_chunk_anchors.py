"""Emit a `source-anchor-index-v1` index from a per-book chunk module (P3, productionized).

Each chunk becomes one `paragraph` anchor (`anchor_id = chunk_id`) so claims anchored to chunk_ids
resolve against `validate_anchor_index` — the P2-spike reconciliation, now a first-class tool.
Deterministic, NO LLM.

Lib: emit_anchors(module_dir) -> list[dict]   (also writes <module_dir>/anchors.jsonl)
CLI: python -m tools.subagent_factory.emit_chunk_anchors <module_dir> [<module_dir> ...]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.subagent_factory._common import atomic_write_text


def emit_anchors(module_dir: str | Path) -> list[dict]:
    d = Path(module_dir)
    sid = json.loads((d / "module.json").read_text(encoding="utf-8"))["source_id"]
    # Decode source.md exactly as chunk_source built char offsets (raw bytes, errors="replace"),
    # so char_start indexes the SAME text. A plain strict read_text would raise on invalid UTF-8 and,
    # if it differed, would slice at the wrong char position → wrong line_number.
    src = (d / "source.md").read_bytes().decode("utf-8", errors="replace")
    records: list[dict] = []
    for line in (d / "chunks.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        # char_start must index into src; a stale/wrong-revision module would silently mis-slice.
        start = c["char_start"]
        if not (0 <= start <= len(src)):
            raise ValueError(
                f"{d.name}: chunk {c['chunk_id']} char_start={start} out of range "
                f"[0, {len(src)}] — chunks.jsonl and source.md are inconsistent (re-chunk the module)"
            )
        records.append(
            {
                "schema_version": "source_anchor_v1",
                "anchor_id": c["chunk_id"],
                "source_id": sid,
                "anchor_type": "paragraph",
                "level": None,
                "text": (c.get("heading_path") or "(chunk)")[:280],
                "line_number": src[:start].count("\n") + 1,
                "page_number": None,
            }
        )
    atomic_write_text(
        d / "anchors.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    )
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit paragraph anchors from chunk module(s).")
    ap.add_argument("module_dir", nargs="+", type=Path)
    args = ap.parse_args()
    for d in args.module_dir:
        recs = emit_anchors(d)
        print(f"{json.loads((d / 'module.json').read_text())['source_id']}: {len(recs)} anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
