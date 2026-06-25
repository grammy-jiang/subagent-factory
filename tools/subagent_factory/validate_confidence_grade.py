"""Validate GRADE-consistency of principle confidence (Step 16 / K2 wiring).

When a principle carries an optional ``grade`` block (``source_type`` + ``downgrades``/``upgrades`` —
the semantic GRADE factors the LLM emitted during promotion), its ``confidence`` must equal the
deterministic ``grade_confidence(...)`` level. This closes the K1 split: the LLM proposes the factors,
the deterministic function owns the level, and this gate enforces they agree — so a confidence value
can't drift from its stated evidence basis.

Validate-if-present: principles without a ``grade`` block (all current ones) pass trivially, so the
gate is non-breaking. A principle that GRADE-grades to ``insufficient`` is flagged — it should be
dropped (abstain), not promoted with a high/medium/low confidence.

Signature ``(path) -> list[str]`` for the tier-gated registry, keyed on ``principles/principles.yaml``.
"""

from pathlib import Path

import yaml

from tools.subagent_factory._validator_cli import validator_main
from tools.subagent_factory.grade_confidence import grade_confidence


def validate_confidence_grade(principles_path: str | Path) -> list[str]:
    """Return error strings. Empty = consistent (or no grade blocks present)."""
    path = Path(principles_path)
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    for p in data.get("principles") or []:
        if not isinstance(p, dict):
            continue
        grade = p.get("grade")
        if not isinstance(grade, dict) or not grade.get("source_type"):
            continue  # validate-if-present
        pid = str(p.get("principle_id", "?"))
        declared = p.get("confidence")
        computed = grade_confidence(
            str(grade["source_type"]),
            [str(x) for x in (grade.get("downgrades") or [])],
            [str(x) for x in (grade.get("upgrades") or [])],
        )["level"]
        if computed == "insufficient":
            errors.append(
                f"principle '{pid}': GRADE factors yield 'insufficient' — drop/abstain, "
                f"do not promote with confidence '{declared}'"
            )
        elif computed != declared:
            errors.append(
                f"principle '{pid}': confidence '{declared}' != GRADE-computed '{computed}' "
                f"(source_type={grade['source_type']}, "
                f"down={list(grade.get('downgrades') or [])}, up={list(grade.get('upgrades') or [])})"
            )
    return errors


def main() -> None:
    validator_main(
        validate_confidence_grade,
        "Usage: python -m tools.subagent_factory.validate_confidence_grade <principles.yaml>",
    )


if __name__ == "__main__":
    main()
