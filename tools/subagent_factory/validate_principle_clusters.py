"""Validate ``principles/principle-clusters.json`` (Step 7 Phase A) — structural + referential.

Structural: ``schemas/principle-clusters-v1.schema.json``.
Referential (the teeth):
- every ``member_principle_ids`` entry exists in ``principles.yaml``;
- no principle belongs to more than one cluster (clusters partition, not overlap);
- each cluster spans ≥ 2 distinct sources (a cross-source cluster by definition);
- an ``llm-confirmed`` cluster must carry a non-empty ``canonical_statement`` (a ``seed`` cluster
  need not — that is what confirmation adds).

Signature ``(path) -> list[str]`` for the tier-gated artifact registry. The clusters file sits at
``<base>/principles/principle-clusters.json``; ``principles.yaml`` is its sibling.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

from tools.subagent_factory.package_queries import principle_ids as _principle_ids

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "principle-clusters-v1.schema.json"


def validate_principle_clusters(clusters_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(clusters_path)
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"parse error: {e}"]

    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        errors.extend(f"Schema: {e.message}" for e in validator.iter_errors(data))
    except (OSError, json.JSONDecodeError) as e:
        return [f"Schema load error: {e}"]
    if errors:
        return errors

    known = _principle_ids(path.parent)
    seen: dict[str, str] = {}  # principle_id -> cluster_id (overlap detection)
    for c in data.get("clusters", []):
        cid = c["cluster_id"]
        for pid in c["member_principle_ids"]:
            if known and pid not in known:
                errors.append(f"cluster {cid}: principle '{pid}' not in principles.yaml")
            if pid in seen:
                errors.append(
                    f"cluster {cid}: principle '{pid}' already in cluster '{seen[pid]}' "
                    "(clusters must not overlap)"
                )
            else:
                seen[pid] = cid
        if len(set(c.get("sources") or [])) < 2:
            errors.append(
                f"cluster {cid}: must span >= 2 sources (cross-source), got {c.get('sources')}"
            )
        if c.get("method") == "llm-confirmed" and not (c.get("canonical_statement") or "").strip():
            errors.append(f"cluster {cid}: llm-confirmed but has no canonical_statement")
    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_principle_clusters <clusters.json>")
        sys.exit(1)
    errs = validate_principle_clusters(sys.argv[1])
    for e in errs:
        print(f"ERROR: {e}")
    print("OK" if not errs else f"{len(errs)} error(s)")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
