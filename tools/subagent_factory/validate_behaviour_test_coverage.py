"""Validate a Step-11 generated behaviour-test suite (tests/behaviour-tests.yaml).

Three checks, all deterministic:

- **schema**: the suite validates against ``schemas/golden-tests-v1.schema.json``;
- **oracle shape**: every ``negative_routing_tests`` entry must set ``expected_route: do_not_invoke``;
  every ``missing_context_tests`` entry must populate ``must_ask_for`` (else the oracle cannot fire);
- **coverage**: every ``confidence: high`` principle is exercised by ≥1 ``golden_tests`` entry (via a
  matching ``principle_coverage`` id), and every referenced principle id resolves to a real principle.

Signature is ``(path) -> list[str]`` for the tier-gated artifact registry, keyed on
``tests/behaviour-tests.yaml`` (present-gated). The authored ``tests/golden-tests.yaml`` is
deliberately NOT keyed here, so the existing packages are untouched; this gate bites only once a
package ships a Step-11 generated suite. Base dir is ``<base>/tests/behaviour-tests.yaml``.
"""

import json
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory._validator_cli import validator_main

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "golden-tests-v1.schema.json"


def _high_confidence_principles(base: Path) -> tuple[set[str], set[str], bool]:
    """Return (all_principle_ids, high_confidence_principle_ids, readable).

    ``readable`` is False when principles.yaml is absent or unparseable — a coverage
    gate cannot verify coverage against a file it cannot read, so the caller fails
    closed. It is True when the file parsed (even if it declares zero principles, which
    is legitimately full coverage). This distinguishes the missing/unparseable case
    from the genuinely-empty case, which the prior (set(), set()) return collapsed.
    """
    pp = base / "principles" / "principles.yaml"
    if not pp.exists():
        return set(), set(), False
    try:
        data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set(), set(), False
    all_ids: set[str] = set()
    high: set[str] = set()
    for p in data.get("principles") or []:
        if not isinstance(p, dict) or not p.get("principle_id"):
            continue
        pid = str(p["principle_id"])
        all_ids.add(pid)
        if p.get("confidence") == "high":
            high.add(pid)
    return all_ids, high, True


def _refs(tests: list) -> set[str]:
    out: set[str] = set()
    for t in tests:
        if isinstance(t, dict):
            for pid in t.get("principle_coverage") or []:
                out.add(str(pid))
    return out


def validate_behaviour_test_coverage(suite_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid + covered."""
    path = Path(suite_path)
    base = path.parent.parent  # <base>/tests/behaviour-tests.yaml
    errors: list[str] = []

    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"Schema load error: {e}"]

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"schema: {loc}: {err.message}")
    if errors:
        # Shape is broken; skip semantic checks that assume a valid shape.
        return errors

    golden = [t for t in data.get("golden_tests", []) if isinstance(t, dict)]
    negative = [t for t in data.get("negative_routing_tests", []) if isinstance(t, dict)]
    missing = [t for t in data.get("missing_context_tests", []) if isinstance(t, dict)]

    # Oracle-shape checks.
    for t in negative:
        if t.get("expected_route") != "do_not_invoke":
            errors.append(
                f"oracle: negative-routing test '{t.get('test_id', '?')}' must set "
                "expected_route: do_not_invoke"
            )
    for t in missing:
        if not (t.get("must_ask_for") or []):
            errors.append(
                f"oracle: missing-context test '{t.get('test_id', '?')}' must populate must_ask_for"
            )

    # Coverage: each high-confidence principle needs ≥1 golden test; refs must resolve.
    all_ids, high, readable = _high_confidence_principles(base)
    # Fail-closed: a coverage gate that cannot read what it covers must FAIL, rather
    # than iterate an empty principle set and pass vacuously (fail-open). A present
    # file that declares zero principles is readable and legitimately full coverage.
    if not readable:
        errors.append("coverage: principles.yaml missing/unparseable — cannot verify coverage")
        return errors

    golden_refs = _refs(golden)
    all_refs = _refs(golden) | _refs(negative) | _refs(missing)

    for pid in sorted(high):
        if pid not in golden_refs:
            errors.append(f"coverage: high-confidence principle '{pid}' has no golden test")
    for ref in sorted(all_refs):
        if ref not in all_ids:
            errors.append(f"coverage: test references unknown principle id '{ref}'")

    return errors


def main() -> None:
    validator_main(
        validate_behaviour_test_coverage,
        "Usage: python -m tools.subagent_factory.validate_behaviour_test_coverage <tests/behaviour-tests.yaml>",
    )


if __name__ == "__main__":
    main()
