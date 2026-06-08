"""Export a generated subagent package to a Claude Code runtime adapter."""

import shutil
from datetime import UTC, datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
_REPO_ROOT = Path(__file__).parent.parent.parent
GENERATOR_VERSION = "0.1.0"


def export_claude_agent(subagent_dir: str | Path) -> dict:
    """
    Read subagents/<slug>/profile.yaml and generate two adapter files:
      subagents/<slug>/adapters/claude-code/<slug>.md   (canonical)
      .claude/agents/generated/<slug>.md                (installed)

    Returns dict: slug, adapter_path, installed_path, error
    """
    subagent_path = Path(subagent_dir)
    profile_path = subagent_path / "profile.yaml"

    result = {
        "slug": None,
        "adapter_path": None,
        "installed_path": None,
        "error": None,
    }

    if not profile_path.exists():
        result["error"] = f"profile.yaml not found at {profile_path}"
        return result

    with open(profile_path) as f:
        profile = yaml.safe_load(f)

    slug = profile.get("slug")
    if not slug:
        result["error"] = "profile.yaml missing 'slug' field"
        return result

    result["slug"] = slug

    ctx = _build_template_context(profile)

    # Renders a Markdown adapter (not HTML) from trusted profile data;
    # HTML autoescape would corrupt Markdown punctuation in the output.
    env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=False)  # nosec B701
    tmpl = env.get_template("claude-agent-adapter.md.j2")
    rendered = tmpl.render(**ctx)

    # Write canonical adapter inside package
    adapter_dir = subagent_path / "adapters" / "claude-code"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    adapter_path = adapter_dir / f"{slug}.md"
    adapter_path.write_text(rendered, encoding="utf-8")
    result["adapter_path"] = str(adapter_path)

    # Install to .claude/agents/generated/
    generated_dir = _REPO_ROOT / ".claude" / "agents" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    installed_path = generated_dir / f"{slug}.md"
    shutil.copy2(adapter_path, installed_path)
    result["installed_path"] = str(installed_path)

    return result


_TRAILING_CONNECTORS = {
    "for", "to", "of", "and", "or", "the", "a", "an", "with", "in", "on",
    "that", "whether", "its", "from", "by", "as", "before", "after", "into",
}


def _clean_clause(text: str, max_chars: int) -> str:
    """Collapse text to a single well-formed clause.

    Whitespace-collapsed, reduced to its first sentence, clipped at a clause or
    word boundary (never mid-word), with trailing punctuation and any dangling
    connector word removed. Never returns a fragment ending in a preposition.
    """
    text = " ".join(text.split())
    text = text.split(". ")[0].rstrip(" .;,")
    if len(text) > max_chars:
        clipped = text[:max_chars]
        for sep in ("; ", ", ", " "):
            idx = clipped.rfind(sep)
            if idx > max_chars * 0.5:
                clipped = clipped[:idx]
                break
        words = clipped.rstrip(" .;,").split()
        while words and words[-1].lower() in _TRAILING_CONNECTORS:
            words.pop()
        text = " ".join(words)
    return text


def _compose_description(profile: dict, max_chars: int = 320) -> str:
    """Build a routing description: role + top triggers + top exclusion.

    Assembles from already-clipped clauses joined with em dashes. If the full
    form exceeds the budget, whole pieces are dropped (second trigger first,
    then the exclusion) so the result is never a mid-clause truncation.
    """
    role = _clean_clause(profile.get("role", ""), 120)
    triggers = [_clean_clause(t, 85) for t in profile.get("when_to_use", [])[:2]]
    triggers = [t for t in triggers if t]
    exclusions = [_clean_clause(e, 85) for e in profile.get("when_not_to_use", [])[:1]]
    exclusion = next((e for e in exclusions if e), "")

    def assemble(n_triggers: int, with_exclusion: bool) -> str:
        parts = [role] if role else []
        used = triggers[:n_triggers]
        if used:
            parts.append("Use when: " + "; ".join(used))
        if with_exclusion and exclusion:
            parts.append("Not for: " + exclusion)
        return " — ".join(parts)

    for n_triggers, with_exclusion in ((2, True), (1, True), (2, False), (1, False)):
        candidate = assemble(n_triggers, with_exclusion)
        if len(candidate) <= max_chars:
            return candidate
    # Last resort (budget smaller than role + one trigger): role alone,
    # clause-clipped to the budget so the result is always well-formed.
    return _clean_clause(role, max_chars)


def _build_template_context(profile: dict) -> dict:
    modes = profile.get("outputs", {}).get("modes", [])
    tools = _determine_tools(profile)

    # Build description: role + top triggers + top exclusion (Phase 9 rule).
    description = _compose_description(profile)

    kp = profile.get("knowledge_partition", {})
    sot = profile.get("source_of_truth_policy", {})
    sources = profile.get("sources", [])

    return {
        "slug": profile["slug"],
        "description": description,
        "tools": tools,
        "model": profile.get("model", "sonnet"),
        "role": profile.get("role", ""),
        "when_to_use": profile.get("when_to_use", []),
        "when_not_to_use": profile.get("when_not_to_use", []),
        "inputs_required": profile.get("inputs", {}).get("required", []),
        "primary_format": profile.get("outputs", {}).get("primary_format", ""),
        "modes": modes,
        "quality_bar": profile.get("quality_bar", []),
        "minimum_useful_output": profile.get("minimum_useful_output", ""),
        "forbidden_behaviours": profile.get("forbidden_behaviours", []),
        "handoff_rules": profile.get("handoff_rules", []),
        "canonical_owner": sot.get("canonical_owner", ""),
        "may_edit_canonical": sot.get("may_edit_canonical", False),
        "precedence": sot.get("precedence", ""),
        "knowledge_skills": kp.get("skills", []),
        "knowledge_references": kp.get("references", []),
        "agent_version": profile.get("agent_version", "0.1.0"),
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "sources": sources,
    }


def _determine_tools(profile: dict) -> list[str]:
    # Read-only roles default to Read, Grep, Glob
    base = ["Read", "Grep", "Glob"]
    modes = [m.get("name", "") for m in profile.get("outputs", {}).get("modes", [])]
    if "produce" in modes or "patch-suggest" in modes:
        base = ["Read", "Edit", "Write", "Grep", "Glob"]
    return base
