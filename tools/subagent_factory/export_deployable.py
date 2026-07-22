"""Export a generated subagent package as a self-contained *deployable* bundle for another repo.

`export_claude_agent` produces a factory-installed adapter whose body references factory-relative
paths (``subagents/<slug>/...``) — those resolve only inside the factory. To *run* a generated
subagent inside a different project you need a self-contained bundle. This module emits one in the
proven **layout A** (see the ``deploy-subagent-self-contained`` memory):

- ``<dest>/.claude/agents/<slug>.md`` — a lean adapter with a ``skills:`` frontmatter field, the
  factory-relative "Canonical package" section stripped, the generated-file header rewritten for a
  deployed copy, and the package's references inlined into the body.
- ``<dest>/.claude/skills/<name>/`` — each knowledge skill dir copied verbatim (auto-discovered by
  Claude Code, so the subagent's ``skills:`` frontmatter resolves).

References are inlined into the adapter body rather than copied: they have no ``.claude/skills/``
home (only ``SKILL.md`` is auto-loaded), and the body is the subagent's private system prompt.
"""

import re
import shutil
from pathlib import Path

import yaml

from tools.subagent_factory._common import atomic_write_text
from tools.subagent_factory.export_claude_agent import render_adapter

_CANONICAL_MARKER = "\n## Canonical package"

# A knowledge skill/reference name is a single path segment (no separators, no traversal). It is
# joined into rmtree/copytree/read paths on a target repo, so a name like "../../x" would delete or
# read outside the bundle. Reject anything that is not a bare identifier segment before use.
_SAFE_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def _strip_canonical_section(md: str) -> str:
    """Drop the factory-relative '## Canonical package' section (its paths resolve only in the factory)."""
    idx = md.find(_CANONICAL_MARKER)
    return md if idx == -1 else md[:idx].rstrip() + "\n"


def _rewrite_header(md: str, slug: str) -> str:
    """Rewrite the generated-file header so a deployed copy points back at the factory exporter."""
    return md.replace(
        f"Regenerate with: /author-subagent --update {slug}",
        f"Deployed copy — do not edit. Re-export from the factory: "
        f"cli export-deployable {slug} --dest <this repo root>",
    )


def _inject_skills_frontmatter(md: str, skills: list[str]) -> str:
    """Insert a ``skills:`` list into the YAML frontmatter (before its closing ``---``).

    Claude Code preloads the named skills into the subagent when it runs. No-op when there are
    no skills. Only the first ``---``-delimited frontmatter block is touched.
    """
    if not skills:
        return md
    lines = md.split("\n")
    if not lines or lines[0].strip() != "---":
        return md  # no frontmatter to extend; leave untouched
    out = [lines[0]]
    injected = False
    for ln in lines[1:]:
        if ln.strip() == "---" and not injected:
            out.append("skills:")
            out.extend(f"  - {s}" for s in skills)
            injected = True
        out.append(ln)
    return "\n".join(out)


def _inline_references(md: str, subagent_path: Path, refs: list[str]) -> tuple[str, list[str]]:
    """Append each existing reference's body as a private '## Reference — <name>' section."""
    blocks: list[str] = []
    inlined: list[str] = []
    for ref in refs:
        ref_path = subagent_path / "references" / f"{ref}.md"
        if not ref_path.exists():
            continue
        blocks.append(f"## Reference — {ref}\n\n{ref_path.read_text().strip()}\n")
        inlined.append(ref)
    if not blocks:
        return md, inlined
    return md.rstrip() + "\n\n" + "\n\n".join(blocks) + "\n", inlined


def export_deployable(subagent_dir: str | Path, dest_root: str | Path) -> dict:
    """Export ``<slug>`` as a self-contained deployable bundle into ``dest_root`` (a target repo root).

    Writes ``<dest_root>/.claude/agents/<slug>.md`` and copies each knowledge skill dir to
    ``<dest_root>/.claude/skills/<name>/``. Returns a result dict:
    ``{slug, adapter_path, skills_copied, references_inlined, error}``.

    Missing-input failures (no profile.yaml, no slug) are returned as a soft ``error`` — the same
    contract as :func:`export_claude_agent`, so callers branch on ``result["error"]``.
    """
    subagent_path = Path(subagent_dir)
    dest = Path(dest_root)
    result: dict = {
        "slug": None,
        "adapter_path": None,
        "skills_copied": [],
        "references_inlined": [],
        "error": None,
    }

    profile_path = subagent_path / "profile.yaml"
    if not profile_path.exists():
        result["error"] = f"profile.yaml not found at {profile_path}"
        return result

    # `or {}`: an empty / comment-only profile.yaml yields None; guard so `.get` follows the
    # soft-error contract (matches export_claude_agent) instead of raising AttributeError.
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    slug = profile.get("slug")
    if not slug:
        result["error"] = "profile.yaml missing 'slug' field"
        return result
    # Path-traversal guard (see export_claude_agent): the slug is joined into the bundle write path,
    # so require it equal the (already-validated) package directory name; fail closed on divergence.
    if str(slug) != subagent_path.name:
        result["error"] = (
            f"profile.yaml slug {slug!r} does not match package directory "
            f"{subagent_path.name!r} — refusing to export"
        )
        return result
    result["slug"] = slug

    kp = profile.get("knowledge_partition", {})
    # Drop any skill/reference name that is not a bare path segment before it reaches rmtree /
    # copytree / read — a "../.." name would otherwise delete or disclose files outside the bundle.
    skills = [s for s in kp.get("skills", []) if _SAFE_SEGMENT.match(str(s))]
    refs = [r for r in kp.get("references", []) if _SAFE_SEGMENT.match(str(r))]

    md = render_adapter(profile, subagent_path)
    md = _strip_canonical_section(md)
    md = _rewrite_header(md, slug)
    md = _inject_skills_frontmatter(md, skills)
    md, inlined = _inline_references(md, subagent_path, refs)
    result["references_inlined"] = inlined

    agents_dir = dest / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    adapter_path = agents_dir / f"{slug}.md"
    atomic_write_text(adapter_path, md)
    result["adapter_path"] = str(adapter_path)

    skills_root = dest / ".claude" / "skills"
    for s in skills:
        src = subagent_path / "skills" / s
        if not src.is_dir():
            continue
        dst = skills_root / s
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        result["skills_copied"].append(s)

    return result
