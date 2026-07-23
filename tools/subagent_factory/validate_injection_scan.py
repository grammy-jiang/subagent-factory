"""Validate a book module's injection-scan.jsonl (one finding per line) against injection-scan-v1.

The artifact is written deterministically by chunk_source, so this is mainly a contract check (fits
the factory's "every artifact has a schema + validator" convention) and a guard against a
hand-edited / corrupted scan file being fed to triage.
"""

import json
import sys
from pathlib import Path

import jsonschema

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "injection-scan-v1.schema.json"


def validate_injection_scan(scan_path: str | Path) -> list[str]:
    """Return error strings for a book module's injection-scan.jsonl (empty = valid, or absent).

    Accepts the module dir or the injection-scan.jsonl path directly. Each non-blank line must be a
    JSON object conforming to injection-scan-v1.
    """
    path = Path(scan_path)
    if path.is_dir():
        path = path / "injection-scan.jsonl"
    if not path.exists():
        return []
    try:
        with open(_SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return [f"cannot load injection-scan-v1 schema: {e}"]
    errors: list[str] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {i}: invalid JSON ({e})")
            continue
        try:
            jsonschema.validate(record, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"line {i}: {e.message}")
    return errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_injection_scan <module|scan.jsonl>")
        sys.exit(1)
    errs = validate_injection_scan(sys.argv[1])
    for e in errs:
        print(f"ERROR: {e}")
    sys.exit(0 if not errs else 1)
