"""Tests for the converter-keyed markdown cache discriminator (preferred_pdf_converter).

The cache key is tagged with the preferred available PDF converter so that installing a
higher-fidelity converter (Docling) auto-invalidates older lower-fidelity (MarkItDown) entries
instead of silently reusing them. The helper lives in ``convert_pdf`` (it mirrors that module's
converter chain); ``ingest_source`` re-exports it as ``_preferred_pdf_converter`` for the cache key.
"""

import importlib.util

import tools.subagent_factory.convert_pdf as cp


def _only(*available):
    """find_spec stub: truthy spec only for the named modules."""
    return lambda name: object() if name in available else None


def test_prefers_docling(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", _only("docling", "markitdown", "fitz"))
    assert cp.preferred_pdf_converter() == "docling"


def test_falls_to_markitdown_without_docling(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", _only("markitdown", "fitz"))
    assert cp.preferred_pdf_converter() == "markitdown"


def test_falls_to_pymupdf_only(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", _only("fitz"))
    assert cp.preferred_pdf_converter() == "pymupdf"


def test_none_when_no_converter(monkeypatch):
    monkeypatch.setattr(importlib.util, "find_spec", _only())
    assert cp.preferred_pdf_converter() == "none"


def test_tag_changes_when_docling_installed(monkeypatch):
    # The invalidation property: the discriminator differs with vs without Docling, so the
    # cache filename differs and an old MarkItDown entry is missed (forcing a fresh convert).
    monkeypatch.setattr(importlib.util, "find_spec", _only("markitdown"))
    before = cp.preferred_pdf_converter()
    monkeypatch.setattr(importlib.util, "find_spec", _only("docling", "markitdown"))
    after = cp.preferred_pdf_converter()
    assert before == "markitdown" and after == "docling" and before != after


def test_ingest_source_reexports_the_helper():
    """The cache key (ingest_source) must stay wired to the convert_pdf helper."""
    import tools.subagent_factory.ingest_source as ing

    assert ing._preferred_pdf_converter is cp.preferred_pdf_converter
