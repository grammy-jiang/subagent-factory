"""Generate skill and reference stub files from a profile's knowledge_partition.

Phase 6 of the authoring cycle moves non-profile content into skills and
reference files. The deriver records what belongs there in
``knowledge_partition.skills[]`` and ``knowledge_partition.references[]``, but the
actual stub files were never scaffolded — leaving packages incomplete versus the
Plan §4 layout. This module creates the missing stubs (idempotently) so a package
has the expected ``skills/<name>/SKILL.md`` and ``references/<name>.md`` files,
each marked TODO until authored.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from tools.subagent_factory._common import atomic_write_text


def _stub_slug(text: str) -> str:
    """Derive a short kebab-case slug from the first words of a partition entry."""
    head = text.split(".")[0].split(":")[0].split("(")[0]
    slug = slugify(head, max_length=48, word_boundary=True)
    return slug or "item"


def planned_slugs(profile: dict) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Map ``knowledge_partition`` entries to their on-disk slugs (no I/O, no writes).

    Returns ``(skills, references)`` where each is a list of ``(entry, slug)`` pairs in
    declaration order, with the same kebab slug + collision-disambiguation rule the stub
    generator uses to choose ``skills/<slug>/SKILL.md`` / ``references/<slug>.md`` paths.
    This is the single source of truth for the entry→file mapping so the authoring
    validator (Step 8) and ``generate_stubs`` cannot drift apart.
    """
    kp = (profile or {}).get("knowledge_partition", {}) or {}

    def _resolve(entries: Any) -> list[tuple[str, str]]:
        out: list[tuple[str, str]] = []
        seen: set[str] = set()
        for entry in entries or []:
            if not isinstance(entry, str) or not entry.strip():
                continue
            slug = _stub_slug(entry)
            base, n = slug, 2
            while slug in seen:
                slug = f"{base}-{n}"
                n += 1
            seen.add(slug)
            out.append((entry, slug))
        return out

    return _resolve(kp.get("skills")), _resolve(kp.get("references"))


def _frontmatter(name: str, kind: str) -> str:
    """`authored-doc-v1` stub frontmatter: status stub + empty provenance."""
    return (
        f"---\nname: {name}\nkind: {kind}\nstatus: stub\n"
        f"provenance:\n  principles: []\n  claims: []\n  source_anchors: []\n---\n\n"
    )


def _skill_stub(slug: str, title: str, source_line: str) -> str:
    return (
        f"{_frontmatter(slug, 'skill')}"
        f"# {title.strip()[:80]}\n\n"
        f"> **STATUS: STUB — not yet authored.** Generated from "
        f"`profile.yaml knowledge_partition.skills`.\n\n"
        f"## Purpose\n\n{source_line.strip()}\n\n"
        f"## Procedure\n\nTODO: author the repeatable steps for this skill "
        f"(keep under 500 lines / 5,000 tokens).\n"
    )


def _reference_stub(slug: str, title: str, source_line: str) -> str:
    return (
        f"{_frontmatter(slug, 'reference')}"
        f"# {title.strip()[:80]}\n\n"
        f"> **STATUS: STUB — not yet authored.** Generated from "
        f"`profile.yaml knowledge_partition.references`.\n\n"
        f"{source_line.strip()}\n\n"
        f"TODO: author the table / taxonomy / checklist this reference should hold.\n"
    )


def generate_stubs(subagent_dir: str | Path) -> dict:
    """Create skill/reference stub files from the profile. Idempotent.

    Returns dict: skills_created, references_created, skills_existing,
    references_existing, skill_paths, reference_paths, error.
    """
    subagent_path = Path(subagent_dir)
    profile_path = subagent_path / "profile.yaml"
    result: dict[str, Any] = {
        "skills_created": 0,
        "references_created": 0,
        "skills_existing": 0,
        "references_existing": 0,
        "skill_paths": [],
        "reference_paths": [],
        "error": None,
    }
    if not profile_path.exists():
        result["error"] = f"profile.yaml not found at {profile_path}"
        return result

    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    skill_plan, ref_plan = planned_slugs(profile)

    for entry, slug in skill_plan:
        skill_dir = subagent_path / "skills" / slug
        skill_file = skill_dir / "SKILL.md"
        result["skill_paths"].append(str(skill_file))
        if skill_file.exists():
            result["skills_existing"] += 1
            continue
        skill_dir.mkdir(parents=True, exist_ok=True)
        # Atomic: exists()-only idempotency above means a torn write would persist as a truncated
        # stub and never be re-created; temp-file + os.replace makes a crash leave no file.
        atomic_write_text(skill_file, _skill_stub(slug, slug.replace("-", " "), entry))
        result["skills_created"] += 1

    refs_dir = subagent_path / "references"
    for entry, slug in ref_plan:
        ref_file = refs_dir / f"{slug}.md"
        result["reference_paths"].append(str(ref_file))
        if ref_file.exists():
            result["references_existing"] += 1
            continue
        refs_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_text(ref_file, _reference_stub(slug, slug.replace("-", " "), entry))
        result["references_created"] += 1

    return result
