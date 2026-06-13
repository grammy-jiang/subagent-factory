"""Tests for the converter-keyed markdown cache discriminator (_preferred_pdf_converter).

The cache key is tagged with the preferred available PDF converter so that installing a
higher-fidelity converter (Docling) auto-invalidates older lower-fidelity (MarkItDown) entries
instead of silently reusing them.
"""

import tools.subagent_factory.ingest_source as ing


def _only(*available):
    """find_spec stub: truthy spec only for the named modules."""
    return lambda name: object() if name in available else None


def test_prefers_docling(monkeypatch):
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only("docling", "markitdown", "fitz"))
    assert ing._preferred_pdf_converter() == "docling"


def test_falls_to_markitdown_without_docling(monkeypatch):
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only("markitdown", "fitz"))
    assert ing._preferred_pdf_converter() == "markitdown"


def test_falls_to_pymupdf_only(monkeypatch):
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only("fitz"))
    assert ing._preferred_pdf_converter() == "pymupdf"


def test_none_when_no_converter(monkeypatch):
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only())
    assert ing._preferred_pdf_converter() == "none"


def test_tag_changes_when_docling_installed(monkeypatch):
    # The invalidation property: the discriminator differs with vs without Docling, so the
    # cache filename differs and an old MarkItDown entry is missed (forcing a fresh convert).
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only("markitdown"))
    before = ing._preferred_pdf_converter()
    monkeypatch.setattr(ing.importlib.util, "find_spec", _only("docling", "markitdown"))
    after = ing._preferred_pdf_converter()
    assert before == "markitdown" and after == "docling" and before != after
