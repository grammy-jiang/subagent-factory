"""Export a generated subagent package to a Claude Code runtime adapter."""

import shutil
from datetime import datetime, timezone
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

    env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=False)
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


def _truncate_at_word(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(" ")
    return truncated[:last_space] if last_space > 0 else truncated


def _build_template_context(profile: dict) -> dict:
    modes = profile.get("outputs", {}).get("modes", [])
    tools = _determine_tools(profile)

    # Build description: role (first sentence) + top 2 triggers + top 1 exclusion
    role_first_sentence = profile.get("role", "").split(".")[0].strip()
    role_short = _truncate_at_word(role_first_sentence, 80)
    triggers = profile.get("when_to_use", [])[:2]
    exclusions = profile.get("when_not_to_use", [])[:1]
    desc_parts = [role_short]
    if triggers:
        desc_parts.append("Use when: " + "; ".join(triggers[:2]))
    if exclusions:
        desc_parts.append("Not when: " + exclusions[0])
    description = _truncate_at_word(" | ".join(desc_parts), 300)

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
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
    }


def _determine_tools(profile: dict) -> list[str]:
    kp = profile.get("knowledge_partition", {})
    mcp = kp.get("mcp", [])
    # Read-only roles default to Read, Grep, Glob
    base = ["Read", "Grep", "Glob"]
    modes = [m.get("name", "") for m in profile.get("outputs", {}).get("modes", [])]
    if "produce" in modes or "patch-suggest" in modes:
        base = ["Read", "Edit", "Write", "Grep", "Glob"]
    return base
