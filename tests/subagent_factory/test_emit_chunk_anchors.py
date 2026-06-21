"""Tests for the productionized chunk-anchor emitter (P3)."""

import json

from tools.subagent_factory.emit_chunk_anchors import emit_anchors
from tools.subagent_factory.validate_anchor_index import validate_anchor_index


def test_emit_anchors_shape_and_validate(tmp_path):
    (tmp_path / "module.json").write_text(json.dumps({"source_id": "foo-12345678"}))
    (tmp_path / "source.md").write_text("line1\nline2\nline3\nbody\n")
    (tmp_path / "chunks.jsonl").write_text(
        json.dumps({"chunk_id": "abc-c0000", "char_start": 0, "heading_path": "Intro"})
        + "\n"
        + json.dumps({"chunk_id": "abc-c0001", "char_start": 12, "heading_path": "Ch1 > S2"})
        + "\n"
    )
    recs = emit_anchors(tmp_path)
    assert len(recs) == 2
    assert recs[0]["anchor_type"] == "paragraph"
    assert recs[0]["anchor_id"] == "abc-c0000"
    assert recs[0]["source_id"] == "foo-12345678"
    assert recs[1]["text"] == "Ch1 > S2"
    assert recs[1]["line_number"] >= 1
    assert validate_anchor_index(tmp_path / "anchors.jsonl") == []  # passes the v1 schema
