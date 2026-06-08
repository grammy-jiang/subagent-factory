"""Tests for detect_file_type."""

import tempfile
from pathlib import Path

import pytest

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


def test_unknown():
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        f.write(b"\x00\x01\x02\x03 binary")
        tmp = f.name
    assert detect_file_type(tmp) == "unknown"
