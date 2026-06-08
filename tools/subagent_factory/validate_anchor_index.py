"""Validate anchor JSONL file line by line against schema."""

import json
import sys
from pathlib import Path

import jsonschema

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "source-anchor-index-v1.schema.json"


def validate_anchor_index(anchors_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(anchors_path)
    errors = []
    try:
        with open(_SCHEMA_PATH) as f:
            schema = json.load(f)
        with open(path) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    jsonschema.validate(record, schema)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: JSON parse error: {e}")
                except jsonschema.ValidationError as e:
                    errors.append(f"Line {line_num}: {e.message}")
    except Exception as e:
        errors.append(str(e))
    return errors


if __name__ == "__main__":
    errors = validate_anchor_index(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)
