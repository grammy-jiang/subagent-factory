"""Convert DOCX to Markdown. Primary: Pandoc. Fallback: MarkItDown (self-healed)."""

from pathlib import Path
from typing import Any

from tools.subagent_factory._converter_common import (
    finalize,
    try_markitdown,
    try_pandoc,
)


def convert_docx(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert DOCX to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors,
                  low_quality, quality, stats
    """
    src = Path(source_path)
    result: dict[str, Any] = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "low_quality": False,
        "quality": {},
        "stats": {},
    }

    text, used, warns, errs = try_pandoc(src, "docx")
    if not text:
        text2, used2, warns2, errs2 = try_markitdown(src, "DOCX conversion")
        if text2:
            text, used = text2, used2
            warns = warns2 + ["Pandoc unavailable or failed; used MarkItDown fallback"]
            errs = errs2
        else:
            result["errors"] = errs + errs2
            result["errors"].append("All DOCX converters failed")
            result["converter_used"] = "none"
            return result

    return finalize(result, text, used, warns, errs, output_path)
