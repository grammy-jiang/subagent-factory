"""Validate ``policy/patch-policy.yaml`` (Step 6) — schema + self-consistency.

Structural: ``schemas/patch-policy-v1.schema.json``.
Self-consistency:
- when ``default_mode: direct_patch``, ``direct_patch_allowed_when`` must include
  ``user_explicitly_requests_patch`` (no unconditional direct patching).

Signature is ``(path) -> list[str]``. Requiredness (a patch/produce mode ⇒ a policy must exist)
is enforced by a mode-conditional block in ``validate_generated_package``, not here.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "patch-policy-v1.schema.json"


def validate_patch_policy(policy_path: str | Path) -> list[str]:
    """Return list of error strings. Empty list = valid."""
    path = Path(policy_path)
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

    if data.get("default_mode") == "direct_patch":
        if "user_explicitly_requests_patch" not in (data.get("direct_patch_allowed_when") or []):
            errors.append(
                "default_mode 'direct_patch' requires 'user_explicitly_requests_patch' in "
                "direct_patch_allowed_when (no unconditional direct patching)"
            )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_patch_policy <patch-policy.yaml>")
        sys.exit(1)
    errors = validate_patch_policy(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
