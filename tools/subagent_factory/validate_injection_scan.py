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
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"cannot load injection-scan-v1 schema: {e}"]
    # Read defensively: this validator exists to guard a HAND-EDITED / corrupted scan, so a non-UTF-8
    # byte must be reported (UnicodeDecodeError is a ValueError, not OSError) — never an uncaught raise
    # that kills the CLI with a traceback and breaks the "always return a list[str]" contract.
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"cannot read {path}: {e}"]
    errors: list[str] = []
    # Split on "\n" only (the writer's delimiter), NOT str.splitlines(): splitlines() also breaks on
    # U+2028/U+2029/U+0085/… which ensure_ascii=False output can carry inside a string value, which
    # would shatter one well-formed record into "invalid JSON" fragments. The blank guard below
    # absorbs the trailing empty element.
    for i, line in enumerate(text.split("\n"), 1):
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
