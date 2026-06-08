"""Tests for validate_anchor_index."""

import json
import tempfile

from tools.subagent_factory.validate_anchor_index import validate_anchor_index

VALID_ANCHOR = {
    "schema_version": "source_anchor_v1",
    "anchor_id": "src-001-h0000",
    "source_id": "src-001",
    "anchor_type": "heading",
    "level": 1,
    "text": "Introduction",
    "line_number": 1,
    "page_number": None,
}


def test_valid_anchors():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
        f.write(json.dumps(VALID_ANCHOR) + "\n")
        path = f.name
    errors = validate_anchor_index(path)
    assert errors == []


def test_missing_required_field():
    bad = dict(VALID_ANCHOR)
    del bad["anchor_id"]
    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
        f.write(json.dumps(bad) + "\n")
        path = f.name
    errors = validate_anchor_index(path)
    assert len(errors) > 0


def test_invalid_anchor_type():
    bad = dict(VALID_ANCHOR)
    bad["anchor_type"] = "paragraph"
    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
        f.write(json.dumps(bad) + "\n")
        path = f.name
    errors = validate_anchor_index(path)
    assert len(errors) > 0


def test_empty_file_is_valid():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
        path = f.name
    errors = validate_anchor_index(path)
    assert errors == []
