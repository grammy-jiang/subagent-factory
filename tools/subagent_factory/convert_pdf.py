"""Convert PDF to Markdown. Primary: Docling. Fallback: MarkItDown (self-healed)."""

import re
from pathlib import Path

from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package

SCANNED_THRESHOLD = 0.15  # chars-per-page below this suggests scanned


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

    # Try Docling first (not auto-installed — heavy ML deps; use `bootstrap
    # --extra convert-full` to enable). Fall back to MarkItDown, which self-heals.
    text, used, warns, errs = _try_docling(src)
    if not text:
        text2, used2, warns2, errs2 = _try_markitdown(src)
        if text2:
            text, used = text2, used2
            warns = warns2 + ["Docling unavailable or failed; used MarkItDown fallback"]
            errs = errs2
        else:
            result["errors"] = errs + errs2
            result["errors"].append("All PDF converters failed")
            result["converter_used"] = "none"
            return result

    result["converter_used"] = used
    result["markdown_text"] = text
    result["is_scanned"] = _detect_scanned(text)
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    result["stats"] = _compute_stats(text)
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


def _detect_scanned(text: str) -> bool:
    if not text:
        return True
    page_markers = len(re.findall(r"<!-- page \d+", text, re.IGNORECASE))
    if page_markers == 0:
        return False
    chars_per_page = len(text) / max(page_markers, 1)
    return chars_per_page < SCANNED_THRESHOLD * 1000


def _compute_stats(text: str) -> dict:
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }
