"""Tests for the PDF converter fallback chain: Docling → MarkItDown → PyMuPDF.

Guards finding 1 (Docling-enable hint surfaced on any fallback) and finding 2
(PyMuPDF wired as the final fallback tier).
"""

from pathlib import Path

import tools.subagent_factory.convert_pdf as cp


def _pdf(tmp_path: Path) -> tuple[Path, Path]:
    src = tmp_path / "in.pdf"
    src.write_bytes(b"%PDF-1.4\n")
    return src, tmp_path / "out.md"


def test_chain_falls_through_to_pymupdf(monkeypatch, tmp_path):
    monkeypatch.setattr(cp, "_try_docling", lambda s: (None, None, [], ["no docling"]))
    monkeypatch.setattr(cp, "_try_markitdown", lambda s: (None, None, [], ["no markitdown"]))
    monkeypatch.setattr(cp, "_try_pymupdf", lambda s: ("body text " * 50, "pymupdf", [], []))
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 1)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert r["converter_used"] == "pymupdf"
    assert any("convert-full" in w for w in r["warnings"])  # finding 1: hint surfaced
    assert out.read_text()


def test_docling_success_emits_no_fallback_hint(monkeypatch, tmp_path):
    monkeypatch.setattr(cp, "_try_docling", lambda s: ("body " * 50, "docling", [], []))
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 1)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert r["converter_used"] == "docling"
    assert not any("convert-full" in w for w in r["warnings"])


def test_all_converters_fail(monkeypatch, tmp_path):
    for fn in ("_try_docling", "_try_markitdown", "_try_pymupdf"):
        monkeypatch.setattr(cp, fn, lambda s: (None, None, [], ["nope"]))
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert r["converter_used"] == "none"
    assert any("All PDF converters failed" in e for e in r["errors"])


def test_pymupdf_absent_soft_fails():
    # fitz not installed (or target file invalid) → soft error, never raises.
    text, used, _warns, errs = cp._try_pymupdf(Path("does-not-exist.pdf"))
    assert text is None
    assert used is None
    assert errs
