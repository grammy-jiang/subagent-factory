"""Validate a faithfulness report (Step 1) — structural + referential.

Structural: ``schemas/faithfulness-report-v1.schema.json``.
Referential:
- each ``rule_ref`` names a field that exists in ``profile.yaml``;
- each ``source_anchors`` entry exists in the package anchor index;
- no ``CONTRADICTED`` finding is silently accepted (``action: accept_with_note``).

Signature is ``(path) -> list[str]`` so it plugs into the tier-gated artifact registry
in ``validate_generated_package``. Base dir is derived as ``<base>/reports/<file>``.
"""

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

_SCHEMA_PATH = (
    Path(__file__).parent.parent.parent / "schemas" / "faithfulness-report-v1.schema.json"
)
# An anchor id ends in a type letter + digits (``-h0007``, ``-t0042``, ``-p0003``). The
# faithfulness step occasionally emits a free-text section description ("ch4 Traps — RISC-V
# registers") instead of a real id; this pattern separates that generation defect from a
# merely-missing id so the error is self-explanatory.
_ANCHOR_ID_RE = re.compile(r"-[a-z]\d{3,}$")


def _profile_fields(base: Path) -> set[str]:
    pp = base / "profile.yaml"
    if not pp.exists():
        return set()
    try:
        prof = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return set(prof.keys()) if isinstance(prof, dict) else set()


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


def validate_faithfulness_report(report_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(report_path)
    base = path.parent.parent  # <base>/reports/faithfulness-report.yaml
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

    # Referential checks (only once structurally valid).
    fields = _profile_fields(base)
    anchors = _anchor_ids(base)
    for i, finding in enumerate(data.get("findings", [])):
        rule_ref = str(finding.get("rule_ref", ""))
        top = re.split(r"[.\[]", rule_ref, maxsplit=1)[0]
        if fields and top and top not in fields:
            errors.append(
                f"findings[{i}].rule_ref '{rule_ref}' has no field '{top}' in profile.yaml"
            )
        for a in finding.get("source_anchors", []) or []:
            if not _ANCHOR_ID_RE.search(str(a)):
                errors.append(
                    f"findings[{i}].source_anchors entry '{str(a)[:60]}' is not a valid anchor id "
                    "(looks like free text) — the faithfulness step must cite real anchor ids"
                )
            elif anchors and a not in anchors:
                errors.append(
                    f"findings[{i}].source_anchors entry '{a}' is not in the anchor index"
                )
        if finding.get("verdict") == "CONTRADICTED" and finding.get("action") == "accept_with_note":
            errors.append(
                f"findings[{i}] is CONTRADICTED but accepted with a note — must be resolved"
            )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_faithfulness_report <report.yaml>")
        sys.exit(1)
    errors = validate_faithfulness_report(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
