"""Validate ``principles/principle-graph.json`` (Step 7 Phase C) — structural + referential.

Structural: ``schemas/principle-graph-v1.schema.json``.
Referential (the teeth):
- every edge ``source``/``target`` exists in ``principles.yaml``;
- no self-loop (``source != target``);
- no duplicate edge (same ``source``, ``target``, ``relation``);
- the hierarchy sub-graph (``refines`` + ``specializes`` edges) is acyclic — A refines B refines A
  is incoherent.

Conflict *resolution* is intentionally NOT failed here: an unresolved ``conflicts`` edge (no
``resolution``) is a policy WARN surfaced to ``conflict-log.md`` by the gate, not a structural error
(per the multi-source plan: conflicts are logged, never silently dropped or hard-blocked).

Signature ``(path) -> list[str]`` for the tier-gated artifact registry. The graph sits at
``<base>/principles/principle-graph.json``; ``principles.yaml`` is its sibling.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

from tools.subagent_factory.package_queries import principle_ids as _principle_ids

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "principle-graph-v1.schema.json"
_HIERARCHY = {"refines", "specializes"}


def _has_cycle(adj: dict[str, list[str]]) -> bool:
    """DFS cycle detection over a directed graph (white/grey/black colouring)."""
    color: dict[str, int] = {}

    def visit(n: str) -> bool:
        color[n] = 1  # grey
        for m in adj.get(n, []):
            c = color.get(m, 0)
            if c == 1 or (c == 0 and visit(m)):
                return True
        color[n] = 2  # black
        return False

    return any(color.get(n, 0) == 0 and visit(n) for n in adj)


def validate_principle_graph(graph_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(graph_path)
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"parse error: {e}"]

    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        errors.extend(f"Schema: {e.message}" for e in validator.iter_errors(data))
    except (OSError, json.JSONDecodeError) as e:
        return [f"Schema load error: {e}"]
    if errors:
        return errors

    known = _principle_ids(path.parent)
    seen: set[tuple[str, str, str]] = set()
    hier_adj: dict[str, list[str]] = {}
    for i, edge in enumerate(data.get("edges", [])):
        src, tgt, rel = edge["source"], edge["target"], edge["relation"]
        if known and src not in known:
            errors.append(f"edges[{i}]: source '{src}' not in principles.yaml")
        if known and tgt not in known:
            errors.append(f"edges[{i}]: target '{tgt}' not in principles.yaml")
        if src == tgt:
            errors.append(f"edges[{i}]: self-loop on '{src}' ({rel})")
        key = (src, tgt, rel)
        if key in seen:
            errors.append(f"edges[{i}]: duplicate edge {src} -{rel}-> {tgt}")
        seen.add(key)
        if rel in _HIERARCHY:
            hier_adj.setdefault(src, []).append(tgt)

    if _has_cycle(hier_adj):
        errors.append("hierarchy edges (refines/specializes) contain a cycle")
    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_principle_graph <graph.json>")
        sys.exit(1)
    errs = validate_principle_graph(sys.argv[1])
    for e in errs:
        print(f"ERROR: {e}")
    print("OK" if not errs else f"{len(errs)} error(s)")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
