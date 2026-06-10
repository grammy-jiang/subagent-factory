"""Tests for the shared source-text loader (enhancement Step 0).

These functions were extracted verbatim from ``quote_scan`` so the prompt-injection
and faithfulness gates reuse the exact loader/normaliser the rights gate uses. The
parity test pins that the extracted loader returns what ``quote_scan`` relies on.
"""

import json

from tools.subagent_factory.source_text import (
    contains_span,
    load_restricted_source_ids,
    load_source_texts,
    normalize_ws,
)


def _pkg(tmp_path, text: str, rights: str = "distillation-only"):
    base = tmp_path / "pkg"
    (base / "sources" / "markdown").mkdir(parents=True)
    sid = "src-1"
    (base / "sources" / "markdown" / f"{sid}.md").write_text(text, encoding="utf-8")
    meta = {"schema_version": "source-metadata-v1", "source_id": sid, "rights_status": rights}
    rel = f"sources/metadata/{sid}.metadata.json"
    (base / "sources" / "metadata").mkdir(parents=True)
    (base / rel).write_text(json.dumps(meta), encoding="utf-8")
    (base / "source-pack.manifest.yaml").write_text(
        "schema_version: source-pack-manifest-v1\n"
        "sources:\n"
        f"  - source_id: {sid}\n"
        f"    metadata_path: {rel}\n",
        encoding="utf-8",
    )
    return base, sid


def test_normalize_ws_lowercases_and_collapses():
    assert normalize_ws("A  B\nC\tD") == "a b c d"


def test_restricted_ids_include_distillation_only(tmp_path):
    base, sid = _pkg(tmp_path, "hello world")
    assert load_restricted_source_ids(base) == {sid}


def test_restricted_ids_exclude_open(tmp_path):
    base, _ = _pkg(tmp_path, "hello world", rights="open")
    assert load_restricted_source_ids(base) == set()


def test_load_source_texts_normalizes(tmp_path):
    base, sid = _pkg(tmp_path, "Hello   World")
    assert load_source_texts(base, {sid}) == {sid: "hello world"}


def test_load_source_texts_none_loads_all(tmp_path):
    base, sid = _pkg(tmp_path, "x")
    assert set(load_source_texts(base)) == {sid}


def test_contains_span():
    texts = {"s": "the quick brown fox"}
    assert contains_span("quick brown", texts)
    assert not contains_span("lazy dog", texts)


def test_missing_markdown_dir_returns_empty(tmp_path):
    base = tmp_path / "empty"
    base.mkdir()
    assert load_source_texts(base) == {}
