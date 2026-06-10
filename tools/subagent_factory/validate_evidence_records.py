"""Validate ``evidence/evidence-records.yaml`` (Step 3) — structural + referential.

Structural: ``schemas/evidence-records-v1.schema.json``.
Referential (the teeth):
- ``evidence_id`` is unique within the file;
- ``claim_id`` exists in ``analysis/claims.jsonl`` (when present);
- every ``source_ids`` entry exists in the manifest;
- every ``source_anchors`` entry exists in the anchor index;
- ``quote_allowed`` is never true for a rights-restricted source.

Signature is ``(path) -> list[str]`` so it plugs into the tier-gated artifact registry.
Base dir is ``<base>/evidence/evidence-records.yaml``.

Promotable-claim coverage ("every promotable claim has ≥1 evidence record") depends on the
importance scores + promotion threshold, so it lives in the principle-promotion step (Step 4),
not this deterministic validator.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory.source_text import load_restricted_source_ids

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "evidence-records-v1.schema.json"


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


def _manifest_source_ids(base: Path) -> set[str]:
    mp = base / "source-pack.manifest.yaml"
    if not mp.exists():
        return set()
    try:
        manifest = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return {str(s.get("source_id")) for s in (manifest.get("sources") or []) if s.get("source_id")}


def _anchor_ids(base: Path) -> set[str]:
    ids: set[str] = set()
    anchors_dir = base / "sources" / "anchors"
    if not anchors_dir.exists():
        return ids
    for af in anchors_dir.glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(json.loads(line)["anchor_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def validate_evidence_records(records_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(records_path)
    base = path.parent.parent  # <base>/evidence/evidence-records.yaml
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
    source_ids = _manifest_source_ids(base)
    anchors = _anchor_ids(base)
    restricted = load_restricted_source_ids(base)

    seen: set[str] = set()
    for i, rec in enumerate(data.get("evidence_records", [])):
        eid = rec["evidence_id"]
        if eid in seen:
            errors.append(f"evidence_records[{i}]: duplicate evidence_id '{eid}'")
        seen.add(eid)

        if claim_ids and rec["claim_id"] not in claim_ids:
            errors.append(
                f"evidence_records[{i}]: claim_id '{rec['claim_id']}' not in analysis/claims.jsonl"
            )
        for sid in rec.get("source_ids", []):
            if source_ids and sid not in source_ids:
                errors.append(f"evidence_records[{i}]: source_id '{sid}' not in manifest")
        for a in rec.get("source_anchors", []) or []:
            if anchors and a not in anchors:
                errors.append(f"evidence_records[{i}]: source_anchor '{a}' not in the anchor index")

        if rec.get("quote_allowed") is True:
            bad = [s for s in rec.get("source_ids", []) if s in restricted]
            if bad:
                errors.append(
                    f"evidence_records[{i}]: quote_allowed=true for rights-restricted source(s) {bad}"
                )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python -m tools.subagent_factory.validate_evidence_records <evidence-records.yaml>"
        )
        sys.exit(1)
    errors = validate_evidence_records(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
