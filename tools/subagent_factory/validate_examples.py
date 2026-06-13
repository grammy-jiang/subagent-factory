"""Validate the optional ``examples`` slot in a profile (Phase 9 — instruction-induction A4).

Worked examples in an adapter teach behaviour few-shot. The instruction-induction research: a
happy-path-only example set leaves the agent untrained on the hard case — so **A4 requires at least
one failure-and-recovery example** whenever a package ships examples at all.

Design choice (does not mass-break the example-less packages): this is **validate-if-present**. A
package with no ``examples`` key passes trivially (adoption is encouraged, not forced). But the
moment a package adds examples, the A4 rule bites — each example must be well-formed and **≥1 must be
``kind: failure-recovery``** (not only ``happy-path``). "If you ship examples, ship a recovery one."

Signature ``(profile_path) -> list[str]`` for the tier-gated artifact registry; base is the
profile.yaml itself (examples live inside it). Empty list = valid.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_REQUIRED_FIELDS = ("title", "scenario", "ideal_response", "kind")
_KINDS = {"happy-path", "failure-recovery"}


def validate_examples(profile_path: str | Path) -> list[str]:
    """Return error strings for the ``examples`` block (empty list = valid / absent)."""
    path = Path(profile_path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]
    if not isinstance(data, dict):
        return ["profile is not a mapping"]

    examples = data.get("examples")
    if examples is None:
        return []  # absent → nothing to gate (adoption encouraged elsewhere, not required here)
    if not isinstance(examples, list) or not examples:
        return ["'examples' must be a non-empty list when present"]

    errors: list[str] = []
    kinds_seen: list[str] = []
    for i, ex in enumerate(examples):
        where = f"examples[{i}]"
        if not isinstance(ex, dict):
            errors.append(f"{where} must be a mapping")
            continue
        for field in _REQUIRED_FIELDS:
            val = ex.get(field)
            if not (isinstance(val, str) and val.strip()):
                errors.append(f"{where} missing non-empty '{field}'")
        kind = ex.get("kind")
        if isinstance(kind, str):
            kinds_seen.append(kind)
            if kind not in _KINDS:
                errors.append(f"{where} kind '{kind}' not in {sorted(_KINDS)}")

    # A4: a package that ships examples must include at least one failure-and-recovery example.
    if "failure-recovery" not in kinds_seen:
        errors.append(
            "A4: examples present but none with kind 'failure-recovery' "
            "(require ≥1 failure-and-recovery example, not only happy-path)"
        )
    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_examples <profile.yaml>")
        sys.exit(1)
    errors = validate_examples(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
