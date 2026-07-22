"""Validate anchor JSONL file line by line against schema."""

import json
import sys
from pathlib import Path

import jsonschema

_SCHEMA_PATH = (
    Path(__file__).parent.parent.parent / "schemas" / "source-anchor-index-v1.schema.json"
)


def validate_anchor_index(anchors_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(anchors_path)
    errors = []
    record_count = 0
    file_read = False
    try:
        with open(_SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
        with open(path, encoding="utf-8") as f:
            file_read = True
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                record_count += 1
                try:
                    record = json.loads(line)
                    jsonschema.validate(record, schema)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: JSON parse error: {e}")
                except jsonschema.ValidationError as e:
                    errors.append(f"Line {line_num}: {e.message}")
    except Exception as e:
        errors.append(str(e))
    # Fail-closed: an existing-but-recordless file is an invalid anchor index.
    # An empty (or all-blank) file silently passed before (fail-open); reject it.
    if file_read and record_count == 0:
        errors.append("anchor index is empty (no anchor records)")
    return errors


if __name__ == "__main__":
    errors = validate_anchor_index(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)
