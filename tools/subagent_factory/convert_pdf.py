"""Convert PDF to Markdown. Chain: Docling → MarkItDown (self-heals) → PyMuPDF."""

import re
from pathlib import Path

from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package

SCANNED_THRESHOLD = 0.15  # chars-per-page (×1000) below this suggests scanned
_MIN_WORDS_BORN_DIGITAL = 30  # below this, with no page signal, suspect a failed scan


def convert_pdf(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert PDF to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors,
                  is_scanned, low_quality, quality, page_count, stats
    """
    src = Path(source_path)
    result = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "is_scanned": False,
        "low_quality": False,
        "quality": {},
        "page_count": None,
        "stats": {},
    }

    # Ordered converter chain. Docling (best layout/table fidelity) is the
    # intended primary but is not auto-installed (heavy ML deps). MarkItDown
    # self-heals; PyMuPDF is a pure-extraction last resort. Docling and PyMuPDF
    # are soft deps — enable Docling with `bootstrap --extra convert-full`.
    text: str | None = None
    used: str | None = None
    warns: list[str] = []
    attempt_errors: list[str] = []
    for name, fn in (("docling", _try_docling), ("markitdown", _try_markitdown), ("pymupdf", _try_pymupdf)):
        t, u, w, e = fn(src)
        if t:
            text, used, warns = t, u, w
            if name != "docling":
                warns = list(warns) + [
                    f"Docling unavailable or failed; used {u} fallback. Enable Docling "
                    "for best layout/table fidelity: `bootstrap --extra convert-full`."
                ]
            break
        attempt_errors += e
    else:
        result["errors"] = attempt_errors + ["All PDF converters failed"]
        result["converter_used"] = "none"
        return result

    result["converter_used"] = used
    result["markdown_text"] = text
    page_count = _pdf_page_count(src)
    result["page_count"] = page_count
    result["is_scanned"] = _detect_scanned(text, page_count)
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    stats = _compute_stats(text)
    stats["page_count"] = page_count
    result["stats"] = stats
    Path(output_path).write_text(text, encoding="utf-8")
    return result


def _try_docling(src: Path):
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        return None, None, [], ["docling not installed"]
    try:
        converter = DocumentConverter()
        doc = converter.convert(str(src))
        text = doc.document.export_to_markdown()
        return text, "docling", [], []
    except Exception as e:
        return None, None, [], [f"docling error: {e}"]


def _try_markitdown(src: Path):
    md_mod = ensure_package("markitdown", purpose="PDF conversion")
    if md_mod is None:
        return None, None, [], ["markitdown not installed and could not be auto-installed"]
    try:
        md = md_mod.MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
    except Exception as e:
        return None, None, [], [f"markitdown error: {e}"]


def _try_pymupdf(src: Path):
    """Last-resort plain-text extraction (PyMuPDF / fitz). Optional soft dep."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None, None, [], ["pymupdf not installed"]
    try:
        with fitz.open(str(src)) as doc:
            text = "\n\n".join(page.get_text() for page in doc)
        return text, "pymupdf", [], []
    except Exception as e:
        return None, None, [], [f"pymupdf error: {e}"]


def _pdf_page_count(src: Path) -> int | None:
    """Real page count straight from the PDF page tree (converter-agnostic).

    Uses pdfminer when available — a soft dependency that MarkItDown's PDF path
    already pulls in, so it is present exactly on the fallback path that needs it.
    Returns None when pdfminer is absent or the PDF cannot be parsed.
    """
    try:
        from pdfminer.pdfpage import PDFPage
    except ImportError:
        return None
    try:
        with open(src, "rb") as fh:
            return sum(1 for _ in PDFPage.get_pages(fh)) or None
    except Exception:
        return None


def _detect_scanned(text: str, page_count: int | None = None) -> bool:
    """Detect a scanned/image-only PDF independent of which converter ran.

    Density signal, in priority order:
      1. real page count from the PDF (works for any converter),
      2. Docling's ``<!-- page N -->`` markers if no count is available,
      3. no page signal at all → flag only near-empty extraction as a suspected scan.
    """
    if not text or not text.strip():
        return True
    pages = page_count
    if not pages:
        markers = len(re.findall(r"<!-- page \d+", text, re.IGNORECASE))
        pages = markers or None
    if not pages:
        return len(text.split()) < _MIN_WORDS_BORN_DIGITAL
    chars_per_page = len(text) / pages
    return chars_per_page < SCANNED_THRESHOLD * 1000


def _compute_stats(text: str) -> dict:
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }
