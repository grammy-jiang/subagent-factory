"""Dispatcher: route a file to the correct converter."""

from pathlib import Path

from tools.subagent_factory.convert_docx import convert_docx
from tools.subagent_factory.convert_epub import convert_epub
from tools.subagent_factory.convert_html import convert_html
from tools.subagent_factory.convert_pdf import convert_pdf
from tools.subagent_factory.detect_file_type import detect_file_type
from tools.subagent_factory.normalize_markdown import normalize_markdown


def convert_document(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Auto-detect and convert a document to Markdown.

    Returns converter result dict + file_type.
    """
    src = Path(source_path)
    file_type = detect_file_type(src)

    dispatch = {
        "pdf": convert_pdf,
        "epub": convert_epub,
        "docx": convert_docx,
        "html": convert_html,
    }

    if file_type == "markdown":
        result = normalize_markdown(src, output_path)
        result["file_type"] = "markdown"
        result["converter_used"] = "passthrough"
        return result

    if file_type in dispatch:
        result = dispatch[file_type](src, output_path)
        result["file_type"] = file_type
        return result

    return {
        "file_type": file_type,
        "markdown_text": "",
        "converter_used": "none",
        "warnings": [],
        "errors": [f"No converter for file type: {file_type}"],
        "stats": {},
    }
