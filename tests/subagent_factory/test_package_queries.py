"""Contract tests for package_queries — the shared read-only query layer under nine referential
validators. Every function must return a set and NEVER raise on missing or garbled input (its own
docstring: "returns an empty set for a missing or garbled file")."""

from pathlib import Path

from tools.subagent_factory.package_queries import (
    anchor_ids,
    claim_ids,
    manifest_source_ids,
    principle_ids,
)

_GARBLED_YAML = "{[}"  # invalid flow mapping/sequence — yaml.safe_load raises YAMLError


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# --- anchor_ids -------------------------------------------------------------------------------
def test_anchor_ids_absent_dir_returns_empty(tmp_path):
    assert anchor_ids(tmp_path) == set()


def test_anchor_ids_collects_valid_skips_garbled(tmp_path):
    # Valid objects collected; blank / non-JSON / non-object / missing-key lines skipped, never raise.
    _write(
        tmp_path / "sources" / "anchors" / "s1.anchors.jsonl",
        '{"anchor_id": "a1"}\n\n{"anchor_id": "a2"}\nnot json\n{"no_id": 1}\n42\n[1, 2]\n',
    )
    assert anchor_ids(tmp_path) == {"a1", "a2"}


# --- claim_ids --------------------------------------------------------------------------------
def test_claim_ids_absent_file_returns_empty(tmp_path):
    assert claim_ids(tmp_path) == set()


def test_claim_ids_collects_valid_skips_garbled(tmp_path):
    _write(
        tmp_path / "analysis" / "claims.jsonl",
        '{"claim_id": "c1"}\ngarbage\n{"claim_id": "c2"}\n"bare string"\n{"x": 1}\n',
    )
    assert claim_ids(tmp_path) == {"c1", "c2"}


# --- manifest_source_ids ----------------------------------------------------------------------
def test_manifest_source_ids_absent_returns_empty(tmp_path):
    assert manifest_source_ids(tmp_path) == set()


def test_manifest_source_ids_collects_valid(tmp_path):
    _write(
        tmp_path / "source-pack.manifest.yaml",
        "sources:\n  - source_id: s1\n  - source_id: s2\n  - notes: no id here\n",
    )
    assert manifest_source_ids(tmp_path) == {"s1", "s2"}


def test_manifest_source_ids_garbled_yaml_no_raise(tmp_path):
    _write(tmp_path / "source-pack.manifest.yaml", _GARBLED_YAML)
    assert manifest_source_ids(tmp_path) == set()


def test_manifest_source_ids_non_dict_top_level_no_raise(tmp_path):
    _write(tmp_path / "source-pack.manifest.yaml", "- just\n- a\n- list\n")
    assert manifest_source_ids(tmp_path) == set()


# --- principle_ids ----------------------------------------------------------------------------
def test_principle_ids_absent_returns_empty(tmp_path):
    assert principle_ids(tmp_path) == set()


def test_principle_ids_collects_valid(tmp_path):
    _write(
        tmp_path / "principles.yaml",
        "principles:\n  - principle_id: P001\n  - principle_id: P002\n  - note: no id\n",
    )
    assert principle_ids(tmp_path) == {"P001", "P002"}


def test_principle_ids_garbled_yaml_no_raise(tmp_path):
    # Regression: principle_ids previously had no YAMLError guard and raised on garbled YAML,
    # violating the never-raise contract that manifest_source_ids already honored.
    _write(tmp_path / "principles.yaml", _GARBLED_YAML)
    assert principle_ids(tmp_path) == set()


def test_principle_ids_non_dict_element_no_raise(tmp_path):
    _write(tmp_path / "principles.yaml", "principles:\n  - just-a-string\n  - principle_id: P003\n")
    assert principle_ids(tmp_path) == {"P003"}
