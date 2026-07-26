"""Validate source-pack manifest YAML against schema."""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

_SCHEMA_PATH = (
    Path(__file__).parent.parent.parent / "schemas" / "source-pack-manifest-v1.schema.json"
)


def validate_manifest(manifest_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(manifest_path)
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        with open(_SCHEMA_PATH, encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.validate(data, schema)
        return []
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]
    except jsonschema.ValidationError as e:
        return [f"Schema validation: {e.message}"]
    except Exception as e:
        return [str(e)]


if __name__ == "__main__":
    errors = validate_manifest(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)
