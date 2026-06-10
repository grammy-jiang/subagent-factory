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
from tools.subagent_factory.prompt_injection_scan import _denylist_hits

_REPO_ROOT = Path(__file__).parent.parent.parent

_ESCALATION = (
    "mcpservers",
    "permissionmode",
    "disallowedtools",
    "bypasspermissions",
    "dangerously-skip-permissions",
)
_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---", re.S)
_TOOLS_LINE = re.compile(r"^tools:\s*(.+)$", re.M)


def _granted_tools(text: str) -> set[str]:
    m = _FRONT_MATTER.search(text)
    fm = m.group(1) if m else text
    tm = _TOOLS_LINE.search(fm)
    if not tm:
        return set()
    return {t.strip() for t in tm.group(1).split(",") if t.strip()}


def _body(text: str) -> str:
    m = _FRONT_MATTER.search(text)
    return text[m.end() :] if m else text


def adapter_policy_scan(subagent_dir: str | Path) -> list[dict]:
    """Scan exported adapter(s). Returns findings ``{file, level, kind, issue}``.

    ``level`` is ``FAIL`` (tool-grant / escalation) or ``WARN`` (body injection).
    """
    base = Path(subagent_dir)
    findings: list[dict] = []
    profile_path = base / "profile.yaml"
    if not profile_path.exists():
        return findings
    try:
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return findings

    slug = str(profile.get("slug") or base.name)
    allowed = set(_determine_tools(profile))
    candidates = [
        base / "adapters" / "claude-code" / f"{slug}.md",
        _REPO_ROOT / ".claude" / "agents" / "generated" / f"{slug}.md",
    ]
    for ad in candidates:
        if not ad.exists():
            continue
        text = ad.read_text(encoding="utf-8", errors="replace")

        extra = _granted_tools(text) - allowed
        if extra:
            findings.append(
                {
                    "file": str(ad),
                    "level": "FAIL",
                    "kind": "tool-grant",
                    "issue": f"adapter grants tools beyond profile modes: {sorted(extra)} "
                    f"(allowed: {sorted(allowed)})",
                }
            )

        low = text.lower()
        esc = [t for t in _ESCALATION if t in low]
        if esc:
            findings.append(
                {
                    "file": str(ad),
                    "level": "FAIL",
                    "kind": "escalation",
                    "issue": f"permission-escalation tokens in adapter: {esc}",
                }
            )

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
