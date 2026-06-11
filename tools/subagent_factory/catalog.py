"""Build a directory of generated subagent packages (deterministic; no LLM).

The generated packages (``subagents/<slug>/``) and their installed adapters
(``.claude/agents/generated/<slug>.md``) are **gitignored output** — invisible from
the tracked repo. This builds an in-memory catalog from the profiles so ``cli catalog``
can print it on demand: a local discovery / testing aid that **writes no file**, so the
experts stay uncommitted while remaining easy to find and exercise.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).parent.parent.parent
SUB = REPO / "subagents"
ADAPTERS = REPO / ".claude" / "agents" / "generated"


def _src(profile: dict) -> str:
    srcs = profile.get("sources") or []
    if not srcs:
        return ""
    s = srcs[0] or {}
    title = s.get("title") or s.get("source_id") or ""
    return " ".join(str(title).split())[:70]


def build_catalog(ready_only: bool = False) -> list[dict[str, Any]]:
    """Read every ``subagents/*/profile.yaml`` into a catalog row. Sorted tier-desc, slug."""
    out: list[dict[str, Any]] = []
    for p in sorted(SUB.glob("*/profile.yaml")):
        slug = p.parent.name
        try:
            prof = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        status = str(prof.get("status", "")).lower()
        if ready_only and status != "ready":
            continue
        modes = [
            m.get("name")
            for m in (prof.get("outputs", {}) or {}).get("modes", []) or []
            if m.get("name")
        ]
        skills_dir, refs_dir = p.parent / "skills", p.parent / "references"
        out.append(
            {
                "slug": slug,
                "tier": prof.get("tier", 0),
                "status": status,
                "role": " ".join(str(prof.get("role", "")).split()),
                "when_to_use": [
                    " ".join(str(x).split()) for x in (prof.get("when_to_use") or [])[:3]
                ],
                "when_not_to_use": [
                    " ".join(str(x).split()) for x in (prof.get("when_not_to_use") or [])[:1]
                ],
                "modes": modes,
                "source": _src(prof),
                "adapter_installed": (ADAPTERS / f"{slug}.md").exists(),
                "skills": len(list(skills_dir.glob("*"))) if skills_dir.exists() else 0,
                "references": len(list(refs_dir.glob("*.md"))) if refs_dir.exists() else 0,
            }
        )
    out.sort(key=lambda r: (-int(r["tier"] or 0), r["slug"]))
    return out


def format_markdown(cat: list[dict[str, Any]]) -> str:
    """Copy-pasteable Markdown directory (for piping to a throwaway file if wanted)."""
    lines = [
        "# Generated Subagent Catalog (local — not committed)",
        "",
        f"{len(cat)} experts · regenerate with `python -m tools.subagent_factory.cli catalog --md`. "
        "Packages + adapters are gitignored output; this is a local discovery/testing aid.",
        "",
        "| Expert | Tier | Status | Modes | Sk/Rf | Adapter | Source |",
        "|--------|-----:|--------|-------|------:|:-------:|--------|",
    ]
    for e in cat:
        lines.append(
            f"| `{e['slug']}` | {e['tier']} | {e['status']} | {', '.join(e['modes'])} "
            f"| {e['skills']}/{e['references']} | {'OK' if e['adapter_installed'] else 'MISSING'} "
            f"| {e['source']} |"
        )
    lines.append("")
    for e in cat:
        lines.append(f"## {e['slug']}  ·  tier {e['tier']}  ·  {e['status']}")
        lines.append(e["role"])
        if e["when_to_use"]:
            lines.append("- **Use when:** " + " ; ".join(e["when_to_use"]))
        if e["when_not_to_use"]:
            lines.append("- **Not for:** " + " ; ".join(e["when_not_to_use"]))
        lines.append(f"- **Modes:** {', '.join(e['modes'])}   **Source:** {e['source']}")
        lines.append(
            f'- **Test it:** `Agent(subagent_type="{e["slug"]}")`, or prompt Claude Code with a matching task.'
        )
        lines.append("")
    return "\n".join(lines)
