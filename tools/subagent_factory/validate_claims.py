"""Validate ``analysis/claims.jsonl`` (Step 2) — structural + referential.

Structural: each line is one claim validated against ``schemas/claims-v1.schema.json``.
Referential (the teeth):
- ``claim_id`` is unique within the file;
- ``source_id`` exists in ``source-pack.manifest.yaml``;
- each ``source_anchors`` entry exists in the package anchor index;
- ``premise_type`` is set only when ``component_class == premise``.

Signature is ``(path) -> list[str]`` so it plugs into the tier-gated artifact registry
in ``validate_generated_package``. Base dir is ``<base>/analysis/claims.jsonl``.

Coverage (extracted vs claimable sentences) and heuristic type post-checks are the
``claim-extraction`` skill's responsibility, not this validator: they are LLM-judgement /
non-deterministic and must not hard-fail the gate.
"""

import json
from pathlib import Path

import jsonschema

from tools.subagent_factory._validator_cli import validator_main
from tools.subagent_factory.package_queries import (
    anchor_ids as _anchor_ids,
)
from tools.subagent_factory.package_queries import (
    manifest_source_ids as _manifest_source_ids,
)

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "claims-v1.schema.json"


def validate_claims(claims_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(claims_path)
    base = path.parent.parent  # <base>/analysis/claims.jsonl
    errors: list[str] = []

    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"Schema load error: {e}"]
    validator = jsonschema.Draft202012Validator(schema)

    source_ids = _manifest_source_ids(base)
    anchors = _anchor_ids(base)

    seen_ids: set[str] = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            claim = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"line {lineno}: JSON parse error: {e}")
            continue

        line_errors = [e.message for e in validator.iter_errors(claim)]
        if line_errors:
            errors.extend(f"line {lineno}: schema: {m}" for m in line_errors)
            continue  # referential checks assume a structurally valid claim

        cid = claim["claim_id"]
        if cid in seen_ids:
            errors.append(f"line {lineno}: duplicate claim_id '{cid}'")
        seen_ids.add(cid)

        if source_ids and claim["source_id"] not in source_ids:
            errors.append(
                f"line {lineno}: source_id '{claim['source_id']}' not in manifest "
                f"({', '.join(sorted(source_ids)) or 'none'})"
            )

        for a in claim.get("source_anchors", []) or []:
            if anchors and a not in anchors:
                errors.append(f"line {lineno}: source_anchor '{a}' not in the anchor index")

        if claim.get("premise_type") is not None and claim["component_class"] != "premise":
            errors.append(
                f"line {lineno}: premise_type set on a non-premise claim "
                f"(component_class='{claim['component_class']}')"
            )

    return errors


def main() -> None:
    validator_main(
        validate_claims,
        "Usage: python -m tools.subagent_factory.validate_claims <claims.jsonl>",
    )


if __name__ == "__main__":
    main()
