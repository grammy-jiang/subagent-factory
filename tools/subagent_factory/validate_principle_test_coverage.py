"""Validate principle-to-behaviour test coverage (Step 5).

Reads ``principles/principles.yaml`` + every ``tests/*.yaml`` and checks:
- **coverage**: each principle with ``confidence: high`` is referenced by ≥1 test (any
  ``tests/*.yaml`` list-item carrying a matching ``principle_id``);
- **dangling**: every ``principle_id`` referenced by a test exists in ``principles.yaml``.

Signature is ``(path) -> list[str]`` for the tier-gated artifact registry; it is keyed on
``principles/principles.yaml`` (present-gated) so coverage is checked whenever principles exist.
Base dir is ``<base>/principles/principles.yaml``.
"""

from pathlib import Path

import yaml

from tools.subagent_factory._validator_cli import validator_main


def _referenced_principle_ids(base: Path) -> set[str]:
    """Principle IDs referenced by any test entry under tests/."""
    ids: set[str] = set()
    tests_dir = base / "tests"
    if not tests_dir.exists():
        return ids
    for tf in tests_dir.glob("*.yaml"):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        for value in data.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and item.get("principle_id"):
                        ids.add(str(item["principle_id"]))
    return ids


def validate_principle_test_coverage(principles_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = covered."""
    path = Path(principles_path)
    base = path.parent.parent  # <base>/principles/principles.yaml
    errors: list[str] = []

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    principles = [p for p in (data.get("principles") or []) if isinstance(p, dict)]
    principle_ids = {str(p.get("principle_id")) for p in principles if p.get("principle_id")}
    referenced = _referenced_principle_ids(base)

    for p in principles:
        pid = str(p.get("principle_id"))
        if p.get("confidence") == "high" and pid not in referenced:
            errors.append(
                f"high-confidence principle '{pid}' has no behavioural test referencing it"
            )

    for rid in sorted(referenced):
        if rid not in principle_ids:
            errors.append(f"test references unknown principle_id '{rid}'")

    return errors


def main() -> None:
    validator_main(
        validate_principle_test_coverage,
        "Usage: python -m tools.subagent_factory.validate_principle_test_coverage <principles.yaml>",
    )


if __name__ == "__main__":
    main()
