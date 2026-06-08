"""Validate source metadata JSON against schema."""

import json
import sys
from pathlib import Path

import jsonschema


_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "source-metadata-v1.schema.json"


def validate_metadata(metadata_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(metadata_path)
    try:
        with open(path) as f:
            data = json.load(f)
        with open(_SCHEMA_PATH) as f:
            schema = json.load(f)
        jsonschema.validate(data, schema)
        return []
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]
    except jsonschema.ValidationError as e:
        return [f"Schema validation: {e.message}"]
    except Exception as e:
        return [str(e)]


if __name__ == "__main__":
    errors = validate_metadata(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)
