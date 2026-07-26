"""Branch coverage for the two schema-gate validators on the release path (both were untested).
Each has four outcomes — clean pass, parse error, schema violation, and the catch-all Exception
(e.g. a missing file). A regression that made either silently return [] would let a structurally
broken package pass release validation, so each branch is pinned by its error-string prefix."""

import json

from tools.subagent_factory.validate_manifest import validate_manifest
from tools.subagent_factory.validate_metadata import validate_metadata

_VALID_METADATA = {
    "schema_version": "source-metadata-v1",
    "source_id": "s1",
    "title": "t",
    "file_type": "markdown",
    "sha256": "a" * 64,
    "conversion_status": "ok",
}


def test_metadata_valid_returns_empty(tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps(_VALID_METADATA), encoding="utf-8")
    assert validate_metadata(p) == []


def test_metadata_invalid_json_reports_parse_error(tmp_path):
    p = tmp_path / "m.json"
    p.write_text("{not valid json", encoding="utf-8")
    errs = validate_metadata(p)
    assert errs and errs[0].startswith("JSON parse error:")


def test_metadata_schema_violation_reported(tmp_path):
    p = tmp_path / "m.json"
    p.write_text("{}", encoding="utf-8")  # missing every required field
    errs = validate_metadata(p)
    assert errs and errs[0].startswith("Schema validation:")


def test_metadata_missing_file_is_error_not_silent_pass(tmp_path):
    assert validate_metadata(tmp_path / "absent.json")  # catch-all Exception branch — non-empty


def test_manifest_valid_returns_empty(tmp_path):
    p = tmp_path / "m.yaml"
    p.write_text(
        "schema_version: source-pack-manifest-v1\nsubagent_slug: demo\nsources: []\n",
        encoding="utf-8",
    )
    assert validate_manifest(p) == []


def test_manifest_invalid_yaml_reports_parse_error(tmp_path):
    p = tmp_path / "m.yaml"
    p.write_text("{[}", encoding="utf-8")
    errs = validate_manifest(p)
    assert errs and errs[0].startswith("YAML parse error:")


def test_manifest_schema_violation_reported(tmp_path):
    p = tmp_path / "m.yaml"
    p.write_text("schema_version: source-pack-manifest-v1\n", encoding="utf-8")  # missing required
    errs = validate_manifest(p)
    assert errs and errs[0].startswith("Schema validation:")


def test_manifest_missing_file_is_error_not_silent_pass(tmp_path):
    assert validate_manifest(tmp_path / "absent.yaml")  # catch-all Exception branch — non-empty
