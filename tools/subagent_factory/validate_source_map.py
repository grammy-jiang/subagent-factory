"""Validate ``sources/maps/<source_id>.source-map.yaml`` (Step 10) — structural + referential.

Structural: ``schemas/source-map-v1.schema.json``.
Referential (the teeth):
- ``node_id`` unique; ``parent_id`` is null or an existing ``node_id``; the parent graph is a
  forest (no cycles);
- every node/unit ``source_anchors`` entry exists in the package anchor index;
- every candidate unit's ``node_id`` exists in ``nodes``; ``unit_id`` unique.

**Coverage is intentionally NOT enforced here yet.** A claim/principle-level recall metric is
research gap G3 (open until research round 3); until then the coverage gate would be a guess, so
the validator restricts itself to the *stable* checks (schema + tree integrity + anchor
referential). Coverage lands when Step 10 is promoted to full.

Signature is ``(path) -> list[str]`` for the gate. Base dir is ``<base>/sources/maps/<id>.source-map.yaml``.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "source-map-v1.schema.json"


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


def _has_cycle(node_id: str, parents: dict[str, str | None]) -> bool:
    seen: set[str] = set()
    cur: str | None = node_id
    while cur is not None:
        if cur in seen:
            return True
        seen.add(cur)
        cur = parents.get(cur)
    return False


def validate_source_map(map_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(map_path)
    base = path.parents[2]  # <base>/sources/maps/<id>.source-map.yaml
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

    anchors = _anchor_ids(base)
    nodes = data.get("nodes") or []
    node_ids: set[str] = set()
    parents: dict[str, str | None] = {}

    for i, n in enumerate(nodes):
        nid = n["node_id"]
        if nid in node_ids:
            errors.append(f"nodes[{i}]: duplicate node_id '{nid}'")
        node_ids.add(nid)
        parents[nid] = n.get("parent_id")
        for a in n.get("source_anchors", []) or []:
            if anchors and a not in anchors:
                errors.append(f"nodes[{i}] ({nid}): source_anchor '{a}' not in the anchor index")

    for nid, pid in parents.items():
        if pid is not None and pid not in node_ids:
            errors.append(f"node '{nid}': parent_id '{pid}' is not an existing node_id")
    for nid in node_ids:
        if _has_cycle(nid, parents):
            errors.append(f"node '{nid}': parent chain contains a cycle")
            break

    seen_units: set[str] = set()
    for i, u in enumerate(data.get("candidate_units") or []):
        uid = u["unit_id"]
        if uid in seen_units:
            errors.append(f"candidate_units[{i}]: duplicate unit_id '{uid}'")
        seen_units.add(uid)
        if u["node_id"] not in node_ids:
            errors.append(f"candidate_units[{i}] ({uid}): node_id '{u['node_id']}' not in nodes")
        for a in u.get("source_anchors", []) or []:
            if anchors and a not in anchors:
                errors.append(
                    f"candidate_units[{i}] ({uid}): source_anchor '{a}' not in the anchor index"
                )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_source_map <source-map.yaml>")
        sys.exit(1)
    errs = validate_source_map(sys.argv[1])
    for e in errs:
        print(f"ERROR: {e}")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
