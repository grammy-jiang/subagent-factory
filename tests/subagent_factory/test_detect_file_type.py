"""Tests for detect_file_type."""

import tempfile
from pathlib import Path

from tools.subagent_factory.detect_file_type import detect_file_type


def _write(path, content):
    Path(path).write_bytes(content if isinstance(content, bytes) else content.encode())


def test_pdf_extension():
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(b"%PDF-1.4 test")
        tmp = f.name
    assert detect_file_type(tmp) == "pdf"


def test_epub_extension():
    with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as f:
        f.write(b"PK\x03\x04 test epub data")
        tmp = f.name
    assert detect_file_type(tmp) == "epub"


def test_docx_extension():
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        f.write(b"PK\x03\x04 test docx data")
        tmp = f.name
    assert detect_file_type(tmp) == "docx"


def test_markdown_extension():
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(b"# Hello")
        tmp = f.name
    assert detect_file_type(tmp) == "markdown"


def test_html_extension():
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        f.write(b"<html><body>test</body></html>")
        tmp = f.name
    assert detect_file_type(tmp) == "html"


def test_pdf_by_magic():
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        f.write(b"%PDF-1.4 test content")
        tmp = f.name
    assert detect_file_type(tmp) == "pdf"


def test_non_zip_docx_not_trusted_as_docx():
    # A .docx whose bytes are NOT a ZIP (legacy OLE .doc renamed, or garbage) must not be trusted
    # as docx on extension alone — the magic-byte gate must apply to .docx too (C1).
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        f.write(b"\xd0\xcf\x11\xe0 legacy OLE compound doc, not a zip")
        tmp = f.name
    assert detect_file_type(tmp) != "docx"


def test_legacy_doc_not_trusted_as_docx():
    # .doc maps to the docx candidate but a real legacy .doc is an OLE container, not a ZIP — it
    # must not be dispatched to the docx/pandoc path as if it were OOXML.
    with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as f:
        f.write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1 OLE2 legacy word doc")
        tmp = f.name
    assert detect_file_type(tmp) != "docx"


def test_unknown():
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        f.write(b"\x00\x01\x02\x03 binary")
        tmp = f.name
    assert detect_file_type(tmp) == "unknown"
