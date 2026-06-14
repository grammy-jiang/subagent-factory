"""Validate ``sources/maps/<source_id>.source-map.yaml`` (Step 10) — structural + referential.

Structural: ``schemas/source-map-v1.schema.json``.
Referential (the teeth):
- ``node_id`` unique; ``parent_id`` is null or an existing ``node_id``; the parent graph is a
  forest (no cycles);
- every node/unit ``source_anchors`` entry exists in the package anchor index;
- every candidate unit's ``node_id`` exists in ``nodes``; ``unit_id`` unique.

**`validate_source_map` FAILs only on structural/referential errors.** Two **WARN-level** advisory
signals live alongside it (never FAIL): ``coverage_findings`` (deterministic *section* coverage) and
``claim_recall_findings`` (deterministic *claim* recall — the G3 counterpart, anchor-overlap join
between the map and ``claims.jsonl``). Both are the deterministic halves of Step-10 G3; the LLM
self-check in the source-structure-mapping skill remains the richer (FActScore/Claimify-style) view.

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


_BACKGROUND_ROLES = {
    "background",
    "intro",
    "introduction",
    "overview",
    "motivation",
    "why",
    "summary",
    "preface",
    "conclusion",
}


def coverage_findings(map_path: str | Path) -> list[str]:
    """WARN-level section-coverage signals (Step 10 G3 — the deterministic part).

    A substantive section node (``level: section``, ``role_class`` not background-ish) is "covered"
    if it, or any descendant, has ≥1 candidate unit. Reports uncovered substantive sections + the
    coverage ratio. This is the deterministic *section*-coverage proxy; ``claim_recall_findings`` is
    its *claim*-recall counterpart. The richer FActScore/Claimify + KPA metric is the
    source-structure-mapping skill's LLM self-check. Advisory (the gate emits these as WARN, never FAIL).
    """
    path = Path(map_path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []
    nodes = data.get("nodes") or []
    units = data.get("candidate_units") or []
    children: dict[str | None, list[str]] = {}
    for n in nodes:
        children.setdefault(n.get("parent_id"), []).append(n["node_id"])
    covered = {u.get("node_id") for u in units if u.get("node_id")}

    def has_unit(nid: str) -> bool:
        stack = [nid]
        while stack:
            c = stack.pop()
            if c in covered:
                return True
            stack.extend(children.get(c, []))
        return False

    sections = [
        n
        for n in nodes
        if n.get("level") == "section"
        and str(n.get("role_class", "")).lower() not in _BACKGROUND_ROLES
    ]
    if not sections:
        return []
    uncovered = [n["node_id"] for n in sections if not has_unit(n["node_id"])]
    if not uncovered:
        return []
    ratio = 1 - len(uncovered) / len(sections)
    return [
        f"section coverage {ratio:.0%}: {len(uncovered)}/{len(sections)} substantive sections "
        f"have no candidate unit ({', '.join(uncovered[:8])}{'…' if len(uncovered) > 8 else ''})"
    ]


def _claim_anchor_set(base: Path) -> set[str]:
    """All ``source_anchors`` referenced by any extracted claim (analysis/claims.jsonl)."""
    cj = base / "analysis" / "claims.jsonl"
    anchors: set[str] = set()
    if not cj.exists():
        return anchors
    for line in cj.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        for a in rec.get("source_anchors", []) or []:
            anchors.add(str(a))
    return anchors


def claim_recall_findings(map_path: str | Path, threshold: float = 0.25) -> list[str]:
    """WARN-level **claim-recall** signal (Step 10 G3 — the deterministic counterpart to section
    coverage).

    A source-map candidate unit is "recalled" if ≥1 extracted claim shares one of its
    ``source_anchors`` (the deterministic anchor-overlap join between the map and ``claims.jsonl``).
    Recall = recalled / total candidate units. WARN when recall falls below ``threshold`` — a signal
    that claim extraction missed a lot of the mapped content. Advisory (never FAIL); skipped when
    there are no claims (Tier-0 / pre-extraction) or no candidate units. NB: anchors are matched
    exactly, so a claim anchored to a finer sub-span than its unit under-counts — read this as a
    *floor* on recall, not an exact figure.
    """
    path = Path(map_path)
    base = path.parents[2]  # <base>/sources/maps/<id>.source-map.yaml
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []
    units = data.get("candidate_units") or []
    claim_anchors = _claim_anchor_set(base)
    if not units or not claim_anchors:
        return []
    recalled = [
        u for u in units if any(str(a) in claim_anchors for a in (u.get("source_anchors") or []))
    ]
    ratio = len(recalled) / len(units)
    if ratio >= threshold:
        return []
    missed = [str(u.get("unit_id")) for u in units if u not in recalled]
    return [
        f"claim recall {ratio:.0%}: only {len(recalled)}/{len(units)} mapped candidate units have an "
        f"extracted claim ({', '.join(missed[:8])}{'…' if len(missed) > 8 else ''})"
    ]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_source_map <source-map.yaml>")
        sys.exit(1)
    errs = validate_source_map(sys.argv[1])
    for e in errs:
        print(f"ERROR: {e}")
    for w in coverage_findings(sys.argv[1]) + claim_recall_findings(sys.argv[1]):
        print(f"WARN: {w}")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
