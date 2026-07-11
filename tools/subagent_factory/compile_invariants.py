"""Compile must-hold principles into an adapter invariant layer (A3 + A5).

Instruction-induction research: an adapter reads better and is adhered to more when its
**non-negotiable, evidence-grounded rules** are a distinct enforced layer, separate from the softer
induced guidance (role, modes, examples). This module is the **deterministic** half:

- **A3 (compile must-hold → checks):** select the principles strong enough to be hard rules —
  ``confidence: high`` AND ``operational_mapping.profile_rule: true`` — and render each as a terse
  invariant line tagged with its ``principle_id`` (so every invariant is traceable to evidence).
- **A5 (layer the adapter):** these compiled invariants render into a dedicated
  ``## Operating invariants (must hold)`` section above the guidance.

The selection + text reduction are deterministic (no LLM): the invariant text is the rule *head*
(the clause before the first colon, else the first sentence) of the principle statement. An LLM
refinement pass over the wording is a documented follow-on, not required for the layer to be sound.

``validate_invariant_coverage`` is the **non-breaking** gate: it skips any adapter that predates the
feature (no invariant section) and only enforces coverage once the section exists, catching a *stale*
adapter (principles changed, export not re-run).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

INVARIANT_SECTION_HEADING = "## Operating invariants (must hold)"
_MAX_INVARIANT_CHARS = 160


def strip_invariant_section(adapter_text: str) -> str:
    """Remove the rendered ``## Operating invariants (must hold)`` block (up to the next ``## ``).

    Used to A/B an adapter with vs without its invariant layer (the baseline-gating measurement).
    """
    import re

    heading = re.escape(INVARIANT_SECTION_HEADING)
    return re.sub(rf"\n{heading}.*?(?=\n## )", "\n", adapter_text, flags=re.S)


def _to_invariant(statement: str, max_chars: int = _MAX_INVARIANT_CHARS) -> str:
    """Reduce a principle statement to a complete, self-sufficient rule line (deterministic).

    Renders the principle's **first sentence in full**. It never truncates mid-clause: an invariant
    that silently drops its own conditions or hedges is worse than a longer line — for a safety rule
    (e.g. the warning-severity caveat in P146) a mid-clause cut inverts the meaning, and the earlier
    ``head-before-colon`` + 160-char ``…`` reduction did exactly that (it also dropped the operative
    tail after a colon, e.g. every concrete style rule in P102). A principle whose whole rule must
    survive should therefore be written so its FIRST sentence is self-sufficient; the fuller
    elaboration lives in the skill body and the principles index. ``max_chars`` is retained for
    signature compatibility but no longer severs a sentence.
    """
    import re

    s = " ".join(str(statement).split())
    # First sentence, kept whole. Do NOT split on a colon: the tail after a colon routinely carries
    # the operative detail (the concrete rule, or a safety hedge), which head-only truncation drops.
    m = re.search(r"(?<=[a-z0-9\)])\.(?:\s|$)", s)
    head = (s[: m.start() + 1] if m else s).rstrip(" .;,")
    return head


def compile_invariants(principles: list[dict]) -> list[dict]:
    """Select must-hold principles and compile each to ``{principle_id, invariant, confidence}``.

    Must-hold = ``confidence: high`` AND ``operational_mapping.profile_rule: true`` — the principles
    promoted to hard adapter rules. Order is preserved from ``principles.yaml``.
    """
    out: list[dict] = []
    for p in principles:
        if not isinstance(p, dict):
            continue
        om = p.get("operational_mapping") or {}
        if p.get("confidence") == "high" and om.get("profile_rule") is True:
            pid = p.get("principle_id")
            stmt = p.get("statement")
            if pid and stmt:
                out.append(
                    {
                        "principle_id": str(pid),
                        "invariant": _to_invariant(stmt),
                        "confidence": "high",
                    }
                )
    return out


def load_principles(subagent_dir: str | Path) -> list[dict]:
    """Read ``principles/principles.yaml`` (``[]`` if absent/unreadable)."""
    path = Path(subagent_dir) / "principles" / "principles.yaml"
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    return [p for p in (data.get("principles") or []) if isinstance(p, dict)]


def validate_invariant_coverage(principles_path: str | Path) -> list[str]:
    """Gate: the adapter's invariant layer must cover every must-hold principle (non-breaking).

    Signature ``(path) -> list[str]`` for the tier-gated registry; ``path`` is principles.yaml.
    Returns ``[]`` (passes) when there are no must-hold principles, no adapter, or the adapter has
    **no invariant section** (a pre-feature adapter is not punished — re-export adopts the layer).
    Once the section exists, every must-hold ``principle_id`` must appear in the adapter.
    """
    path = Path(principles_path)
    base = path.parent.parent
    principles = load_principles(base)
    must_hold = compile_invariants(principles)
    if not must_hold:
        return []
    adapter = base / "adapters" / "claude-code" / f"{base.name}.md"
    if not adapter.exists():
        return []  # adapter existence is a separate, earlier check
    text = adapter.read_text(encoding="utf-8")
    if INVARIANT_SECTION_HEADING not in text:
        return []  # pre-feature adapter — not gated until it re-exports with the layer
    missing = [m["principle_id"] for m in must_hold if f"[{m['principle_id']}]" not in text]
    if missing:
        return [
            "adapter invariant layer is stale — missing must-hold principle(s) "
            f"{', '.join(missing)} (re-export the adapter)"
        ]
    # Content-survival, not just tag-presence: an invariant truncated mid-clause (trailing "…")
    # silently drops its rule tail — for safety-tier content this can invert meaning, and coverage
    # by tag alone cannot see it (this is what shipped a gutted P146 warning-severity rule).
    import re

    section = re.search(
        rf"{re.escape(INVARIANT_SECTION_HEADING)}(.*?)(?=\n## )", text, flags=re.S
    )
    if section and "…" in section.group(1):
        truncated = [ln.strip() for ln in section.group(1).splitlines() if "…" in ln]
        return [
            "adapter invariant layer truncates rule content (trailing '…') — a compiled invariant "
            "dropped its tail; fix compile_invariants and re-export: " + " | ".join(truncated[:3])
        ]
    return []


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.compile_invariants subagents/<slug>")
        sys.exit(1)
    invs = compile_invariants(load_principles(sys.argv[1]))
    for inv in invs:
        print(f"[{inv['principle_id']}] {inv['invariant']}")
    print(f"\n{len(invs)} must-hold invariant(s)")


if __name__ == "__main__":
    main()
