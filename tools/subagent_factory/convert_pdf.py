"""Convert PDF to Markdown. Primary: Docling. Fallback: MarkItDown."""

import re
import subprocess
import sys
from pathlib import Path


SCANNED_THRESHOLD = 0.15  # chars-per-page below this suggests scanned


def convert_pdf(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert PDF to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors,
                  is_scanned, page_count, stats
    """
    src = Path(source_path)
    result = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "is_scanned": False,
        "page_count": None,
        "stats": {},
    }

    # Try Docling first
    text, used, warns, errs = _try_docling(src)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns
        result["errors"] = errs
        result["markdown_text"] = text
        result["is_scanned"] = _detect_scanned(text)
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    # Fallback: MarkItDown
    text, used, warns, errs = _try_markitdown(src)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns + ["Docling unavailable or failed; used MarkItDown fallback"]
        result["errors"] = errs
        result["markdown_text"] = text
        result["is_scanned"] = _detect_scanned(text)
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    result["errors"].append("All PDF converters failed")
    result["converter_used"] = "none"
    return result


def _try_docling(src: Path):
    try:
        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        doc = converter.convert(str(src))
        text = doc.document.export_to_markdown()
        return text, "docling", [], []
    except ImportError:
        return None, None, [], ["docling not installed"]
    except Exception as e:
        return None, None, [], [f"docling error: {e}"]


def _try_markitdown(src: Path):
    try:
        from markitdown import MarkItDown

        md = MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
    except ImportError:
        return None, None, [], ["markitdown not installed"]
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
