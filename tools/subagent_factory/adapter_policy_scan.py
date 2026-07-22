"""Adapter-policy scan (Step 1): the exported adapter must not silently widen authority.

Additive to ``profile_self_check`` #15 (which guards the *neutral core*). This scans the
*exported adapter* file(s) — ``adapters/claude-code/<slug>.md`` and the installed
``.claude/agents/generated/<slug>.md`` — for:

- **tool-grant widening** (FAIL): tools beyond what the profile's modes authorize
  (``export_claude_agent._determine_tools``). An effect-side / least-privilege control —
  the adapter must not grant more authority than the profile earns.
- **permission-escalation tokens** (FAIL): ``mcpServers`` / ``permissionMode`` /
  ``disallowedTools`` / ``bypassPermissions`` etc. — never legitimate in a generated adapter.
- **instruction-injection patterns** in the adapter body (WARN): a source payload that
  leaked through into the adapter. WARN, not FAIL, because the body is synthesized prose and
  a denylist phrase there can be a legitimate quote; a reviewer triages it.
"""

import re
import sys
from pathlib import Path

import yaml

from tools.subagent_factory.export_claude_agent import _determine_tools
from tools.subagent_factory.prompt_injection_scan import _denylist_hits, _norm
from tools.subagent_factory.validate_skill_authoring import (
    _FRONTMATTER_CORRUPT,
    _parse_frontmatter,
    split_frontmatter,
)

_REPO_ROOT = Path(__file__).parent.parent.parent

# A grant value the parser cannot reduce to a clean name-set (corrupt frontmatter, or a `tools`
# value that is a mapping / nested structure) yields this sentinel instead of an empty set. It can
# never be in the allowed baseline, so `granted_tools(text) - allowed` is non-empty → tool-grant
# FAIL. This makes "a tools shape I can't model" fail CLOSED, not open (the recurring seam: every
# unmodelled shape used to collapse to set() and PASS).
_UNPARSEABLE_GRANT = "\x00UNPARSEABLE-TOOLS"

# Permission-escalation tokens never legitimate in a generated adapter. Matched case-folded after
# normalization (zero-width strip / confusable fold) so an obfuscated key can't slip past, and
# de-hyphenated so ``allowed-tools`` and ``allowedTools`` collapse to the same token. Includes the
# authority-widening keys (``allowedtools`` widens the tool grant outside the profile basis;
# ``additionaldirectories`` widens filesystem reach) alongside the permission-mode escapes.
_ESCALATION = (
    "mcpservers",
    "permissionmode",
    "disallowedtools",
    "allowedtools",
    "additionaldirectories",
    "bypasspermissions",
    "dangerouslyskippermissions",
)

# Allowlist of the ONLY legitimate Claude Code adapter frontmatter keys (normalized: lowercased,
# hyphens/underscores dropped). Any other key present is an escalation FAIL — strictly stronger than
# enumerating known-bad tokens, which can only catch shapes already on the list. _ESCALATION is
# retained to enrich the message when an unexpected key is a recognized escalation token.
_ALLOWED_FRONTMATTER_KEYS = frozenset({"name", "description", "tools", "model"})


def granted_tools(text: str) -> set[str]:
    """Public: the set of tool names an adapter's front-matter ``tools:`` grants (empty if none).

    Parses the frontmatter via the shared ``_parse_frontmatter`` (BOM/blank-line/CRLF-tolerant —
    the same fence recognition the rest of the factory uses, so this can't diverge from how the
    doc is otherwise read), then reads the ``tools`` value as YAML. BOTH supported Claude Code
    forms are covered: the inline scalar (``tools: Read, Grep``) and the block list
    (``tools:\\n  - Read\\n  - Bash``). The earlier line-regex (a) only read the inline form and
    (b) fell back to parsing the whole body when its strict ``^---\\n`` fence missed a BOM/CRLF
    opening — both let a Bash/Write grant bypass the load-bearing tool-grant FAIL path. Used by
    this scan and by ``optimize_adapter.make_policy_gate``, so the parsing rule lives in one place.
    """
    fm = _parse_frontmatter(text)
    if fm is _FRONTMATTER_CORRUPT:
        # Present-but-unparseable adapter frontmatter: cannot be assessed → fail closed (a hidden
        # `tools: Bash` inside malformed frontmatter must not read as "grants nothing").
        return {_UNPARSEABLE_GRANT}
    if not isinstance(fm, dict):
        return set()  # no frontmatter at all → no grant
    val = fm.get("tools")
    if val is None:
        return set()
    if isinstance(val, str):
        return {t.strip() for t in val.split(",") if t.strip()}
    if isinstance(val, (list, tuple)):
        # Names must be scalars; a non-scalar element (list of mappings, nested) is unmodellable.
        if all(isinstance(t, (str, int, float)) for t in val):
            return {str(t).strip() for t in val if str(t).strip()}
        return {_UNPARSEABLE_GRANT}
    # dict or any other shape: cannot reduce to a name-set → fail closed.
    return {_UNPARSEABLE_GRANT}


def _escalation_keys(fm: object) -> set[str]:
    """All mapping KEYS in the frontmatter, recursively, normalized (zero-width strip / confusable
    fold, lowercased, hyphens+underscores dropped) so allowed-tools / allowed_tools / allowedTools
    collapse to one token. Escalation is a frontmatter-KEY control — Claude Code honors these as
    keys, not as words in body prose — so matching keys (not a whole-text substring sweep) catches
    the real attack while not false-FAILing a reviewer adapter whose prose merely names the concept.
    """
    keys: set[str] = set()
    if isinstance(fm, dict):
        for k, v in fm.items():
            keys.add(re.sub(r"[-_]", "", _norm(str(k)).lower()))
            keys |= _escalation_keys(v)
    elif isinstance(fm, (list, tuple)):
        for item in fm:
            keys |= _escalation_keys(item)
    return keys


def _toolgrant_issue(text: str, allowed: set[str]) -> str | None:
    """Tool-grant widening issue for an adapter string, or None. ``allowed`` = _determine_tools()."""
    extra = granted_tools(text) - allowed
    if extra:
        return f"adapter grants tools beyond profile modes: {sorted(extra)} (allowed: {sorted(allowed)})"
    return None


def _escalation_issue(text: str) -> str | None:
    """Escalation issue for an adapter string, or None: any frontmatter key outside the allowlist."""
    keys = _escalation_keys(_parse_frontmatter(text))
    unexpected = sorted(k for k in keys if k not in _ALLOWED_FRONTMATTER_KEYS)
    if not unexpected:
        return None
    known = [k for k in unexpected if any(t in k for t in _ESCALATION)]
    detail = f"; incl. known escalation token(s): {known}" if known else ""
    return (
        "unexpected adapter frontmatter key(s) — allowlist is name/description/tools/model: "
        f"{unexpected}{detail}"
    )


def scan_rendered_adapter(text: str, allowed: set[str]) -> list[dict]:
    """FAIL findings (tool-grant widening + escalation keys) for a RENDERED adapter string, checkable
    BEFORE it is written. Lets export gate the write (reference-monitor placement) rather than relying
    on a later validate pass to catch a widened adapter already at the live path. ``allowed`` =
    ``set(_determine_tools(profile))``. Body-injection is excluded here — it is WARN-tier, and export
    must not fail-closed on a WARN."""
    out: list[dict] = []
    if (iss := _toolgrant_issue(text, allowed)) is not None:
        out.append({"level": "FAIL", "kind": "tool-grant", "issue": iss})
    if (iss := _escalation_issue(text)) is not None:
        out.append({"level": "FAIL", "kind": "escalation", "issue": iss})
    return out


def _body(text: str) -> str:
    # Shared (BOM/blank/CRLF-tolerant) split. With no frontmatter at all the whole text is body;
    # with frontmatter present the split's body is authoritative (even if empty).
    result, body = split_frontmatter(text)
    return text if result is None else body


def adapter_policy_scan(subagent_dir: str | Path) -> list[dict]:
    """Scan exported adapter(s). Returns findings ``{file, level, kind, issue}``.

    ``level`` is ``FAIL`` (tool-grant / escalation) or ``WARN`` (body injection).
    """
    base = Path(subagent_dir)
    findings: list[dict] = []
    profile_path = base / "profile.yaml"

    # The profile is the policy BASIS (which tools the modes earn). If it is missing or corrupt we
    # cannot derive `allowed`, so the gate must FAIL CLOSED whenever an adapter is nonetheless
    # present — returning [] (PASS) would let a tampered package that also removed/corrupted its
    # profile disable this control entirely. With no adapter present there is nothing to gate, so
    # an absent profile is a benign no-op (preserves the empty-package PASS).
    cc_dir = base / "adapters" / "claude-code"
    adapter_present = cc_dir.is_dir() and any(cc_dir.glob("*.md"))
    # A profile that loads but is NOT a mapping (top-level list/scalar) is not a usable policy
    # basis — treat it like a parse failure (None) and fail closed below, rather than coercing it
    # to {} (which would silently pass a read-only adapter on a garbage profile).
    profile: dict | None = None
    if profile_path.exists():
        try:
            loaded = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            profile = loaded if isinstance(loaded, dict) else None
        except yaml.YAMLError:
            profile = None
    if profile is None:
        if adapter_present:
            findings.append(
                {
                    "file": str(profile_path),
                    "level": "FAIL",
                    "kind": "scan-error",
                    "issue": "cannot load profile.yaml to derive the allowed-tool basis; "
                    "failing closed (adapter present, policy basis unavailable)",
                }
            )
        return findings

    slug = str(profile.get("slug") or base.name)
    allowed = set(_determine_tools(profile))
    # Scan EVERY adapter file in the package's claude-code dir, not only {slug}.md: a file whose
    # name drifted from the slug (rename not propagated) must not escape the FAIL path. Plus the
    # installed adapter at the canonical {slug}.md path. Dedup by resolved path, stable order.
    candidates: list[Path] = sorted(cc_dir.glob("*.md")) if cc_dir.is_dir() else []
    candidates.append(_REPO_ROOT / ".claude" / "agents" / "generated" / f"{slug}.md")
    seen: set[Path] = set()
    for ad in candidates:
        if not ad.exists():
            continue
        rp = ad.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        text = ad.read_text(encoding="utf-8", errors="replace")

        # Tool-grant widening + escalation-key checks, shared with scan_rendered_adapter (export's
        # pre-write gate). Escalation is now an ALLOWLIST over the parsed frontmatter KEYS (Claude
        # Code honors these as keys, not as body prose), so a reviewer adapter whose prose merely
        # names "allowedTools" is not flagged, while ANY unexpected real key fails closed — stronger
        # than the former known-bad-token denylist. A corrupt/parseless adapter yields no keys here;
        # its grant is already failed closed by granted_tools' sentinel.
        for iss in scan_rendered_adapter(text, allowed):
            findings.append({"file": str(ad), **iss})

        for fam in _denylist_hits(_body(text)):
            findings.append(
                {
                    "file": str(ad),
                    "level": "WARN",
                    "kind": "injection",
                    "issue": f"instruction-injection pattern in adapter body: {fam}",
                }
            )
    return findings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.adapter_policy_scan subagents/<slug>")
        sys.exit(1)
    findings = adapter_policy_scan(sys.argv[1])
    for f in findings:
        print(f"{f['level']} [{f['kind']}] {f['file']}: {f['issue']}")
    if not findings:
        print("adapter-policy-scan PASS")
    sys.exit(1 if any(f["level"] == "FAIL" for f in findings) else 0)


if __name__ == "__main__":
    main()
