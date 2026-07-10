"""Adapter output-quality gate — the exported adapter must be substantive, not a stub.

Complements the existing adapter checks (existence, canonical==installed, and the *security*
adapter-policy scan) with a *quality* gate on the canonical adapter
``adapters/claude-code/<slug>.md``:

- the ``GENERATED FILE. DO NOT EDIT`` header is present (generated-artifact-policy rule #3 — was
  enforced nowhere);
- no stub/placeholder tokens leaked from an unfinished profile (TODO, STATUS: STUB, PLACEHOLDER…);
- the load-bearing sections (``## Role``, ``## When to use``) exist and are non-empty;
- the body is not implausibly short.

Signature ``(base) -> list[(level, msg)]`` with ``level ∈ {FAIL, WARN, OK}`` to match the other
check blocks in ``validate_generated_package``. Returns ``[]`` when no adapter is present (its
existence is a separate, earlier check).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Clear stub markers; deliberately omits ambiguous ones (XXX/TBD) to avoid false positives in
# synthesized prose. Each entry is (regex, human label).
# ``PLACEHOLDER`` is matched case-SENSITIVELY (like TODO/FIXME): the stub-token convention is the
# upper-case word, whereas the lower-case "placeholder" is an ordinary English term that legitimately
# appears in distilled prose (e.g. a bash principle: the ``:`` null utility is a "do-nothing
# placeholder where the grammar needs a command"). The template-marker form ``<placeholder…`` is still
# caught case-insensitively by its own entry below, so real placeholders do not slip through.
_PLACEHOLDERS = [
    (re.compile(r"\bTODO\b"), "TODO"),
    (re.compile(r"\bFIXME\b"), "FIXME"),
    (re.compile(r"STATUS:\s*STUB", re.IGNORECASE), "STATUS: STUB"),
    (re.compile(r"\bPLACEHOLDER\b"), "PLACEHOLDER"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "lorem ipsum"),
    (re.compile(r"\bTKTK\b", re.IGNORECASE), "TKTK"),
    (re.compile(r"to be (?:authored|written|filled)", re.IGNORECASE), "to be authored/written"),
    (re.compile(r"<\s*placeholder", re.IGNORECASE), "<placeholder"),
]
_REQUIRED_SECTIONS = ("## Role", "## When to use")
_MIN_LINES = 20  # a real templated adapter is ~130 lines; below this it is a stub


def _parse_frontmatter(text: str) -> tuple[str, object]:
    """Parse the leading ``---``-delimited YAML frontmatter block.

    Returns ``("ok", mapping)`` on success, ``("missing", None)`` if there is no delimited
    block, or ``("invalid", message)`` if the block is not valid YAML or not a mapping. A
    Claude Code adapter whose frontmatter does not parse is silently un-loadable by the
    runtime (the agent never registers), so this must be a hard failure — not a stub check.
    """
    if not text.startswith("---"):
        return ("missing", None)
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ("missing", None)
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return ("invalid", str(exc).splitlines()[0])
    if not isinstance(data, dict):
        return ("invalid", "frontmatter is not a mapping")
    return ("ok", data)


def _section_nonempty(text: str, heading: str) -> tuple[bool, bool]:
    """Return (present, non_empty) for a ``## Heading`` block (content up to the next ``## ``)."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == heading:
            for body in lines[i + 1 :]:
                if body.startswith("## "):
                    break
                if body.strip() and not body.startswith("#"):
                    return True, True
            return True, False
    return False, False


def validate_adapter_quality(subagent_dir: str | Path) -> list[tuple[str, str]]:
    base = Path(subagent_dir)
    adapter = base / "adapters" / "claude-code" / f"{base.name}.md"
    if not adapter.exists():
        return []  # existence is a separate, earlier check
    text = adapter.read_text(encoding="utf-8")
    out: list[tuple[str, str]] = []

    head = "\n".join(text.splitlines()[:20]).upper()
    if "DO NOT EDIT" not in head:
        out.append(
            ("FAIL", "adapter missing 'GENERATED FILE. DO NOT EDIT' header in first 20 lines")
        )

    # Frontmatter must be loadable YAML, else the runtime silently drops the agent (the tdd
    # regression: an unescaped quote in `description` broke the block and the agent never
    # registered, yet every other quality check passed).
    fm_status, fm_payload = _parse_frontmatter(text)
    if fm_status == "missing":
        out.append(("FAIL", "adapter has no '---' delimited YAML frontmatter block"))
    elif fm_status == "invalid":
        out.append(("FAIL", f"adapter frontmatter is not valid YAML: {fm_payload}"))
    else:
        for key in ("name", "description"):
            if not (isinstance(fm_payload, dict) and fm_payload.get(key)):
                out.append(("FAIL", f"adapter frontmatter missing required key '{key}'"))

    for pattern, label in _PLACEHOLDERS:
        if pattern.search(text):
            out.append(("FAIL", f"adapter contains stub/placeholder token: {label}"))

    for sec in _REQUIRED_SECTIONS:
        present, nonempty = _section_nonempty(text, sec)
        if not present:
            out.append(("FAIL", f"adapter missing required section '{sec}'"))
        elif not nonempty:
            out.append(("WARN", f"adapter section '{sec}' is empty"))

    n_lines = len(text.splitlines())
    if n_lines < _MIN_LINES:
        out.append(("WARN", f"adapter is only {n_lines} lines — likely a stub"))

    if not out:
        out.append(("OK", "adapter quality checks passed"))
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_adapter_quality subagents/<slug>")
        sys.exit(1)
    findings = validate_adapter_quality(sys.argv[1])
    for level, msg in findings:
        print(f"[{level:4s}] {msg}")
    sys.exit(1 if any(lvl == "FAIL" for lvl, _ in findings) else 0)


if __name__ == "__main__":
    main()
