"""Export a generated subagent package to a Claude Code runtime adapter."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from tools.subagent_factory._common import atomic_write_text

_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
_REPO_ROOT = Path(__file__).parent.parent.parent
GENERATOR_VERSION = "0.1.0"


def _yaml_scalar(value: str) -> str:
    """JSON-encode a string into a valid single-line YAML double-quoted scalar.

    JSON strings are valid YAML; this escapes embedded quotes/newlines and (unlike Jinja's
    ``tojson``) does not HTML-escape ``<>&``. Adapter frontmatter that fails to parse silently
    un-registers the agent (the tdd regression), so the description must always be well-formed.
    """
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def render_adapter(profile: dict, subagent_path: Path) -> str:
    """Render the Claude Code adapter Markdown from a loaded profile. Pure (no file I/O).

    Shared by export_claude_agent (the factory-installed adapter) and export_deployable
    (a self-contained bundle for another repo), so both render through one code path.
    """
    ctx = _build_template_context(profile)
    # A3/A5: compile must-hold principles into a distinct enforced invariant layer, traceable to
    # each principle_id. Baseline-gated: a profile may set `attach_invariants: false` to omit it.
    from tools.subagent_factory.compile_invariants import compile_invariants, load_principles

    if profile.get("attach_invariants", True):
        ctx["invariants"] = compile_invariants(load_principles(subagent_path))
    else:
        ctx["invariants"] = []

    # Markdown (not HTML) from trusted profile data; HTML autoescape would corrupt punctuation.
    env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=False)  # nosec B701
    return env.get_template("claude-agent-adapter.md.j2").render(**ctx)


def export_claude_agent(subagent_dir: str | Path) -> dict:
    """
    Read subagents/<slug>/profile.yaml and generate two adapter files:
      subagents/<slug>/adapters/claude-code/<slug>.md   (canonical)
      .claude/agents/generated/<slug>.md                (installed)

    Returns dict: slug, adapter_path, installed_path, error

    Error contract (intentionally dual; callers must handle both):
    - Missing-input failures (no profile.yaml, profile missing 'slug') are RETURNED as a result dict
      with a populated ``error`` field and ``None`` paths — callers branch on ``result["error"]``
      (see cli_pipeline.cmd_export). This stays a soft, recoverable signal for a missing/incomplete
      package.
    - Malformed-input failures further in (yaml parse, missing template, compile_invariants) RAISE.
      These are programmer/data-corruption errors, not the expected "package not ready yet" case.
    Kept dual deliberately: the cli caller (out of this change's scope) depends on the returned
    ``error`` field, so the missing-input branches must not be converted to raises here.
    """
    subagent_path = Path(subagent_dir)
    profile_path = subagent_path / "profile.yaml"

    result: dict[str, str | None] = {
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

    rendered = render_adapter(profile, subagent_path)

    # Write canonical adapter inside package (atomically — temp file + os.replace).
    adapter_dir = subagent_path / "adapters" / "claude-code"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    adapter_path = adapter_dir / f"{slug}.md"
    atomic_write_text(adapter_path, rendered)
    result["adapter_path"] = str(adapter_path)

    # Install to .claude/agents/generated/. Write the SAME rendered bytes atomically rather than
    # shutil.copy2-ing from the canonical file: copy2 is non-atomic, so a crash/error mid-copy left
    # the canonical adapter written but the installed one absent or truncated (a torn install) with
    # no rollback. atomic_write_text writes a sibling temp file then os.replace's it into place, so a
    # reader sees either the previous installed adapter or the complete new one — never a partial.
    # Writing `rendered` (not copying) keeps the installed file byte-identical to the canonical one.
    generated_dir = _REPO_ROOT / ".claude" / "agents" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    installed_path = generated_dir / f"{slug}.md"
    atomic_write_text(installed_path, rendered)
    result["installed_path"] = str(installed_path)

    return result


# FUTURE EXTRACTION (do not move now): the ~140 LOC description-cleaning cluster below
# (_TRAILING_CONNECTORS, _drop_dangling_open_paren, _neutralize_inner_dashes, _clean_clause,
# _compose_description) is router-description grammar logic, not adapter-export logic. It belongs in
# its own module (e.g. adapter_description.py) so export_claude_agent stays focused on read profile ->
# render template -> install. Deferred here because relocating it carries behaviour risk (the clause
# heuristics are pinned by a large regression suite); extract in a dedicated, test-backed pass.
_TRAILING_CONNECTORS = {
    "for",
    "to",
    "of",
    "and",
    "or",
    "the",
    "a",
    "an",
    "with",
    "in",
    "on",
    "that",
    "whether",
    "which",
    "where",
    "what",
    "whose",
    "whom",
    "its",
    "from",
    "by",
    "as",
    "before",
    "after",
    "into",
}


def _drop_dangling_open_paren(text: str) -> str:
    """Cut a clause back to before any unmatched opening parenthesis.

    Clipping at a clause/word boundary can land inside a parenthetical
    (``... into services (decompose``), leaving a dangling ``(`` with no close.
    An unbalanced paren reads as a broken, mid-clause fragment in the router
    description. When opens exceed closes, truncate at the last unmatched ``(``
    and re-trim trailing punctuation so the result is always paren-balanced.
    """
    if text.count("(") <= text.count(")"):
        return text
    depth = 0
    cut = None
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                cut = i  # position of an opening paren at top level
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
                if depth == 0:
                    cut = None  # this group closed; not the dangling one
    if cut is None:
        return text
    return text[:cut].rstrip(" .;,-")


def _neutralize_inner_dashes(text: str) -> str:
    """Replace em/en dashes inside a clause with commas.

    ``_compose_description`` joins its pieces with a literal em dash
    (``" — "``), so that separator must be reserved as the structural
    delimiter between the role, ``Use when:``, and ``Not for:`` sections. An
    em or en dash used *within* a clause (a common appositive in technical
    prose — e.g. ``a concurrency defect — a race``) renders identically to the
    join, so a reader or router cannot tell the section boundary from clause
    punctuation. Demoting the inner dash to a comma keeps the appositive
    readable while leaving the join unambiguous. Hyphens in compound words
    (``user/kernel``, ``copy-on-write``) are untouched.
    """
    # Collapse any spacing around an em/en dash, then emit a comma + space so
    # the result reads as ``code, a race`` rather than ``code , a race``.
    return re.sub(r"\s*[—–]\s*", ", ", text)


def _clean_clause(text: str, max_chars: int) -> str:
    """Collapse text to a single well-formed clause.

    Whitespace-collapsed, inner em/en dashes demoted to commas (so the
    structural em-dash join stays unambiguous), reduced to its first sentence,
    clipped at a clause or word boundary (never mid-word), with trailing
    punctuation and any dangling connector word removed. Never returns a
    fragment ending in a preposition or an unbalanced opening parenthesis.
    """
    text = " ".join(text.split())
    text = _neutralize_inner_dashes(text)
    text = text.split(". ")[0].rstrip(" .;,")
    if len(text) > max_chars:
        clipped = text[:max_chars]
        for sep in ("; ", ", ", " "):
            idx = clipped.rfind(sep)
            if idx > max_chars * 0.5:
                clipped = clipped[:idx]
                break
        # A truncated clause that still carries an inline ``label: list`` has a
        # necessarily incomplete list tail (the end was already lost), e.g.
        # ``caching strategy: pattern`` from ``…strategy: pattern selection, …``.
        # Drop back to before the colon so the description never ends mid-list.
        if ": " in clipped:
            clipped = clipped[: clipped.rfind(": ")]
        words = clipped.rstrip(" .;,").split()
        while words and words[-1].lower() in _TRAILING_CONNECTORS:
            words.pop()
        text = " ".join(words)
    text = _drop_dangling_open_paren(text)
    # Removing the paren fragment can re-expose a trailing connector word.
    words = text.split()
    while words and words[-1].lower() in _TRAILING_CONNECTORS:
        words.pop()
    return " ".join(words)


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

    # Build description: role + top triggers + top exclusion (Phase 9 rule), JSON-encoded into a
    # valid single-line YAML scalar so an embedded quote can't break the adapter frontmatter.
    description = _yaml_scalar(_compose_description(profile))

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
        "examples": profile.get("examples", []),
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
