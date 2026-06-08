"""Tests for generate_metadata."""

import json
import tempfile
from pathlib import Path

from tools.subagent_factory.generate_metadata import generate_metadata


def test_metadata_generated():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Test source\n\nContent here.\n")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
        out = f.name

    conversion_result = {
        "conversion_status": "ok",
        "converter_used": "passthrough",
        "warnings": [],
        "errors": [],
        "stats": {"word_count": 3, "heading_count": 1},
    }

    meta = generate_metadata(src, "test-src-001", "markdown", conversion_result, out, title="Test Source")

    assert meta["schema_version"] == "source-metadata-v1"
    assert meta["source_id"] == "test-src-001"
    assert meta["file_type"] == "markdown"
    assert len(meta["sha256"]) == 64
    assert meta["title"] == "Test Source"

    data = json.loads(Path(out).read_text())
    assert data["source_id"] == "test-src-001"


def test_sha256_stable():
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False, encoding="utf-8") as f:
        f.write("deterministic content")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
        out = f.name

    m1 = generate_metadata(src, "s1", "markdown", {"conversion_status": "ok", "warnings": [], "errors": [], "stats": {}}, out)
    m2 = generate_metadata(src, "s1", "markdown", {"conversion_status": "ok", "warnings": [], "errors": [], "stats": {}}, out)
    assert m1["sha256"] == m2["sha256"]
