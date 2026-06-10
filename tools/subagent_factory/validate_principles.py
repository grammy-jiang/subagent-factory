"""Validate ``principles/principles.yaml`` (Step 4) — structural + referential.

Structural: ``schemas/principles-v1.schema.json``.
Referential (the teeth):
- ``principle_id`` is unique within the file;
- every ``derived_from_claims`` entry exists in ``analysis/claims.jsonl`` (when present);
- **promotable coverage** (deferred from Step 3): every derived claim has ≥1 record in
  ``evidence/evidence-records.yaml`` (when present);
- ``operational_mapping.skill`` / ``reference`` (when non-null) exist in the profile's
  ``knowledge_partition``;
- ``operational_mapping.test_cases`` all exist in ``tests/*.yaml``.

Signature is ``(path) -> list[str]`` for the tier-gated artifact registry.
Base dir is ``<base>/principles/principles.yaml``.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "principles-v1.schema.json"


def _claim_ids(base: Path) -> set[str]:
    cp = base / "analysis" / "claims.jsonl"
    if not cp.exists():
        return set()
    ids: set[str] = set()
    for line in cp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ids.add(json.loads(line)["claim_id"])
        except (json.JSONDecodeError, KeyError):
            continue
    return ids


def _evidence_claim_ids(base: Path) -> set[str]:
    ep = base / "evidence" / "evidence-records.yaml"
    if not ep.exists():
        return set()
    try:
        data = yaml.safe_load(ep.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return {
        str(r.get("claim_id")) for r in (data.get("evidence_records") or []) if r.get("claim_id")
    }


def _knowledge(base: Path) -> tuple[set[str], set[str]]:
    pp = base / "profile.yaml"
    if not pp.exists():
        return set(), set()
    try:
        prof = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set(), set()
    kp = prof.get("knowledge_partition", {}) or {}
    return set(kp.get("skills") or []), set(kp.get("references") or [])


def _test_ids(base: Path) -> set[str]:
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
                    if isinstance(item, dict) and item.get("test_id"):
                        ids.add(str(item["test_id"]))
    return ids


def validate_principles(principles_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(principles_path)
    base = path.parent.parent  # <base>/principles/principles.yaml
    errors: list[str] = []

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        errors.extend(f"Schema: {e.message}" for e in validator.iter_errors(data))
    except (OSError, json.JSONDecodeError) as e:
        return [f"Schema load error: {e}"]
    if errors:
        return errors

    claim_ids = _claim_ids(base)
    evidence_claims = _evidence_claim_ids(base)
    skills, references = _knowledge(base)
    test_ids = _test_ids(base)

    seen: set[str] = set()
    for i, pr in enumerate(data.get("principles", [])):
        pid = pr["principle_id"]
        if pid in seen:
            errors.append(f"principles[{i}]: duplicate principle_id '{pid}'")
        seen.add(pid)

        for cid in pr["derived_from_claims"]:
            if claim_ids and cid not in claim_ids:
                errors.append(
                    f"principles[{i}]: derived_from_claims '{cid}' not in analysis/claims.jsonl"
                )
            elif evidence_claims and cid not in evidence_claims:
                errors.append(
                    f"principles[{i}]: claim '{cid}' has no evidence record (promotable coverage)"
                )

        om = pr.get("operational_mapping", {}) or {}
        skill = om.get("skill")
        if skill and skills and skill not in skills:
            errors.append(
                f"principles[{i}]: operational_mapping.skill '{skill}' not in knowledge_partition.skills"
            )
        reference = om.get("reference")
        if reference and references and reference not in references:
            errors.append(
                f"principles[{i}]: operational_mapping.reference '{reference}' not in knowledge_partition.references"
            )
        for tc in om.get("test_cases", []) or []:
            if test_ids and tc not in test_ids:
                errors.append(
                    f"principles[{i}]: operational_mapping.test_cases '{tc}' not found in tests/"
                )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_principles <principles.yaml>")
        sys.exit(1)
    errors = validate_principles(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
