"""Tests for the source-map validator (Step 10)."""

import json

import yaml

from tools.subagent_factory.validate_source_map import validate_source_map

_GOOD = {
    "schema_version": "source-map-v1",
    "source_id": "s1",
    "nodes": [
        {"node_id": "n1", "parent_id": None, "level": "chapter", "source_anchors": ["a1"]},
        {"node_id": "n2", "parent_id": "n1", "level": "section", "source_anchors": ["a2"]},
    ],
    "candidate_units": [
        {"unit_id": "u1", "node_id": "n2", "statement": "x", "source_anchors": ["a2"]},
    ],
}


def _pkg(tmp_path, data, anchors=("a1", "a2")):
    base = tmp_path / "pkg"
    (base / "sources" / "maps").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "anchors" / "s1.anchors.jsonl").write_text(
        "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
    )
    mp = base / "sources" / "maps" / "s1.source-map.yaml"
    mp.write_text(yaml.safe_dump(data), encoding="utf-8")
    return mp


def test_valid(tmp_path):
    assert validate_source_map(_pkg(tmp_path, _GOOD)) == []


def test_bad_level_is_schema_error(tmp_path):
    bad = {**_GOOD, "nodes": [{"node_id": "n1", "parent_id": None, "level": "page"}]}
    assert validate_source_map(_pkg(tmp_path, bad))


def test_dangling_parent(tmp_path):
    bad = {**_GOOD, "nodes": [{"node_id": "n1", "parent_id": "ghost", "level": "section"}]}
    errs = validate_source_map(_pkg(tmp_path, bad))
    assert any("not an existing node_id" in e for e in errs)


def test_cycle(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": "n2", "level": "section"},
            {"node_id": "n2", "parent_id": "n1", "level": "section"},
        ],
        "candidate_units": [],
    }
    assert any("cycle" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_dangling_anchor(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section", "source_anchors": ["ghost"]}
        ],
        "candidate_units": [],
    }
    assert any("anchor index" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_unit_dangling_node(tmp_path):
    bad = {
        **_GOOD,
        "candidate_units": [{"unit_id": "u1", "node_id": "ghost", "statement": "x"}],
    }
    assert any("not in nodes" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_duplicate_node_id(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section"},
            {"node_id": "n1", "parent_id": None, "level": "section"},
        ],
        "candidate_units": [],
    }
    assert any("duplicate node_id" in e for e in validate_source_map(_pkg(tmp_path, bad)))
