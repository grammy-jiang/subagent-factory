"""Render principles/conflict-log.md from the principle graph (Step 7 Phase B) — deterministic.

The cross-source ``conflicts`` edges (with their scoped ``resolution``) already live in
``principle-graph.json``; this renders them, plus each side's principle statement, into the
human-readable ``conflict-log.md`` the multi-source plan calls for. Unresolved conflicts (a
``conflicts`` edge with no ``resolution``) are surfaced at the top as **OPEN** — logged, never
dropped. No LLM.

Library: ``render_conflict_log(subagent_dir) -> str`` (also writes the file).
CLI: ``python -m tools.subagent_factory.render_conflict_log <subagents/slug>``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


def _principle_statements(base: Path) -> dict[str, str]:
    pp = base / "principles" / "principles.yaml"
    if not pp.exists():
        return {}
    data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    return {
        str(p.get("principle_id")): str(p.get("statement", ""))
        for p in (data.get("principles") or [])
        if p.get("principle_id")
    }


def render_conflict_log(subagent_dir: str | Path, *, write: bool = True) -> str:
    base = Path(subagent_dir)
    graph_path = base / "principles" / "principle-graph.json"
    if not graph_path.exists():
        return ""
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    stmt = _principle_statements(base)
    conflicts = [e for e in graph.get("edges", []) if e.get("relation") == "conflicts"]
    resolved = [e for e in conflicts if (e.get("resolution") or "").strip()]
    open_ = [e for e in conflicts if not (e.get("resolution") or "").strip()]

    lines = [
        f"# Cross-source conflict log — {base.name}",
        "",
        "Generated from `principle-graph.json` (Step 7). Cross-source `conflicts` edges are kept as "
        "**multi-truth**: both principles stay valid, scoped by the resolution. Never silently "
        "dropped.",
        "",
        f"- conflicts: {len(conflicts)} (resolved/scoped: {len(resolved)}, **OPEN: {len(open_)}**)",
        "",
    ]

    def block(e: dict) -> list[str]:
        s, t = e["source"], e["target"]
        return [
            f"### {s} ↔ {t}",
            f"- **{s}:** {stmt.get(s, '(statement missing)')}",
            f"- **{t}:** {stmt.get(t, '(statement missing)')}",
            f"- **Resolution:** {(e.get('resolution') or '_OPEN — needs scoping/human review_')}",
            "",
        ]

    if open_:
        lines.append("## OPEN conflicts (resolve before release)")
        lines.append("")
        for e in open_:
            lines += block(e)
    if resolved:
        lines.append("## Resolved / scoped (multi-truth)")
        lines.append("")
        for e in resolved:
            lines += block(e)
    if not conflicts:
        lines.append("_No cross-source conflicts recorded._")

    text = "\n".join(lines) + "\n"
    if write:
        (base / "principles" / "conflict-log.md").write_text(text, encoding="utf-8")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.render_conflict_log <subagents/slug>")
        sys.exit(1)
    out = render_conflict_log(sys.argv[1])
    if not out:
        print("no principle-graph.json — nothing to render")
        return
    n = out.count("### ")
    print(f"conflict-log.md written ({n} conflict block(s))")


if __name__ == "__main__":
    main()
