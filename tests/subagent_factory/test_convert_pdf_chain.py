"""Tests for the PDF converter fallback chain: Docling → MarkItDown → PyMuPDF.

Guards finding 1 (Docling-enable hint surfaced on any fallback) and finding 2
(PyMuPDF wired as the final fallback tier).
"""

import sys
import types
from pathlib import Path

import tools.subagent_factory.convert_pdf as cp


def _pdf(tmp_path: Path) -> tuple[Path, Path]:
    src = tmp_path / "in.pdf"
    src.write_bytes(b"%PDF-1.4\n")
    return src, tmp_path / "out.md"


def test_chain_falls_through_to_pymupdf(monkeypatch, tmp_path):
    monkeypatch.setattr(
        cp, "_try_docling", lambda s: cp.ConvertAttempt(None, None, [], ["no docling"])
    )
    monkeypatch.setattr(
        cp, "_try_markitdown", lambda s: cp.ConvertAttempt(None, None, [], ["no markitdown"])
    )
    monkeypatch.setattr(
        cp, "_try_pymupdf", lambda s: cp.ConvertAttempt("body text " * 50, "pymupdf", [], [])
    )
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 1)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert r["converter_used"] == "pymupdf"
    assert any("convert-full" in w for w in r["warnings"])  # finding 1: hint surfaced
    assert out.read_text()


def test_docling_success_emits_no_fallback_hint(monkeypatch, tmp_path):
    monkeypatch.setattr(
        cp, "_try_docling", lambda s: cp.ConvertAttempt("body " * 50, "docling", [], [])
    )
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 1)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert r["converter_used"] == "docling"
    assert not any("convert-full" in w for w in r["warnings"])


def test_all_converters_fail(monkeypatch, tmp_path):
    for fn in ("_try_docling", "_try_markitdown", "_try_pymupdf"):
        monkeypatch.setattr(cp, fn, lambda s: cp.ConvertAttempt(None, None, [], ["nope"]))
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


def test_zero_heading_pdf_warns(monkeypatch, tmp_path):
    # A multi-page PDF that converts with no headings → flattened/scanned warning.
    monkeypatch.setattr(cp, "_try_docling", lambda s: cp.ConvertAttempt(None, None, [], ["x"]))
    monkeypatch.setattr(
        cp,
        "_try_markitdown",
        lambda s: cp.ConvertAttempt("plain body text " * 200, "markitdown", [], []),
    )
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 10)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert any("0 headings recovered" in w for w in r["warnings"])


def test_headings_present_no_zero_heading_warn(monkeypatch, tmp_path):
    monkeypatch.setattr(
        cp,
        "_try_docling",
        lambda s: cp.ConvertAttempt("# A\n\nbody text\n\n" * 200, "docling", [], []),
    )
    monkeypatch.setattr(cp, "_pdf_page_count", lambda s: 10)
    src, out = _pdf(tmp_path)
    r = cp.convert_pdf(src, out)
    assert not any("0 headings recovered" in w for w in r["warnings"])


def test_docling_fast_path_disables_ocr_and_tables(monkeypatch):
    """The born-digital fast path must build Docling with OCR and table-structure off."""
    captured = {}

    class PdfPipelineOptions:
        def __init__(self):
            self.do_ocr = True  # docling defaults; the fast path must flip both to False
            self.do_table_structure = True

    class PdfFormatOption:
        def __init__(self, pipeline_options=None):
            self.pipeline_options = pipeline_options

    class InputFormat:
        PDF = "pdf"

    class _Doc:
        def export_to_markdown(self):
            return "# Heading\n\nbody text here\n"

    class _Result:
        document = _Doc()

    class DocumentConverter:
        def __init__(self, format_options=None):
            captured["fmt"] = format_options

        def convert(self, _src):
            captured["opts"] = captured["fmt"][InputFormat.PDF].pipeline_options
            return _Result()

    base = types.ModuleType("docling.datamodel.base_models")
    base.InputFormat = InputFormat
    popt = types.ModuleType("docling.datamodel.pipeline_options")
    popt.PdfPipelineOptions = PdfPipelineOptions
    dconv = types.ModuleType("docling.document_converter")
    dconv.DocumentConverter = DocumentConverter
    dconv.PdfFormatOption = PdfFormatOption
    for name, mod in [
        ("docling", types.ModuleType("docling")),
        ("docling.datamodel", types.ModuleType("docling.datamodel")),
        ("docling.datamodel.base_models", base),
        ("docling.datamodel.pipeline_options", popt),
        ("docling.document_converter", dconv),
    ]:
        monkeypatch.setitem(sys.modules, name, mod)

    text, used, _warns, errs = cp._try_docling(Path("x.pdf"))
    assert used == "docling" and text and not errs
    assert captured["opts"].do_ocr is False
    assert captured["opts"].do_table_structure is False


def test_docling_postprocess_failure_does_not_retry_default(monkeypatch):
    """A failure during table post-processing must surface, not trigger the slow default retry.

    The fast path's converter.convert() succeeds, but _finish_docling raises (e.g. a table
    export bug). That is NOT a construction/API failure, so the chain must not silently rebuild
    a full OCR+table default converter and re-run the same doomed post-processing (~20x slower).
    The convert() call must happen exactly once and the real error must surface.
    """
    convert_calls = {"n": 0}

    class PdfPipelineOptions:
        def __init__(self):
            self.do_ocr = True
            self.do_table_structure = True

    class PdfFormatOption:
        def __init__(self, pipeline_options=None):
            self.pipeline_options = pipeline_options

    class InputFormat:
        PDF = "pdf"

    class _Doc:
        def export_to_markdown(self):
            return "# Heading\n\nbody text here\n"

    class _Result:
        document = _Doc()

    class DocumentConverter:
        def __init__(self, format_options=None):
            pass

        def convert(self, _src):
            convert_calls["n"] += 1
            return _Result()

    base = types.ModuleType("docling.datamodel.base_models")
    base.InputFormat = InputFormat
    popt = types.ModuleType("docling.datamodel.pipeline_options")
    popt.PdfPipelineOptions = PdfPipelineOptions
    dconv = types.ModuleType("docling.document_converter")
    dconv.DocumentConverter = DocumentConverter
    dconv.PdfFormatOption = PdfFormatOption
    for name, mod in [
        ("docling", types.ModuleType("docling")),
        ("docling.datamodel", types.ModuleType("docling.datamodel")),
        ("docling.datamodel.base_models", base),
        ("docling.datamodel.pipeline_options", popt),
        ("docling.document_converter", dconv),
    ]:
        monkeypatch.setitem(sys.modules, name, mod)

    # _finish_docling blows up (simulates a table post-processing defect).
    def _boom(_document, _tables_on):
        raise RuntimeError("table post-processing exploded")

    monkeypatch.setattr(cp, "_finish_docling", _boom)

    text, used, _warns, errs = cp._try_docling(Path("x.pdf"))

    assert convert_calls["n"] == 1  # NO silent slow retry with the default converter
    assert text is None and used is None
    assert errs and any("table post-processing exploded" in e for e in errs)  # real error surfaces
