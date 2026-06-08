"""Tests for detect_topic."""

import tempfile
from pathlib import Path

from tools.subagent_factory.detect_topic import detect_topic, _from_filename


def test_markdown_front_matter_title():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("---\ntitle: Clean Architecture Guide\n---\n\n# Body\n")
        path = f.name
    assert detect_topic(path) == "Clean Architecture Guide"


def test_markdown_h1_fallback():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Designing Reliable Systems\n\nContent here.\n")
        path = f.name
    assert detect_topic(path) == "Designing Reliable Systems"


def test_filename_fallback():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("No headings, no front matter.\n")
        path = f.name
    # result will be based on temp filename — just check it's a non-empty string
    result = detect_topic(path)
    assert isinstance(result, str)
    assert len(result) > 0


def test_filename_cleaner_strips_version():
    p = Path("/tmp/a_philosophy_of_software_design_v2.md")
    result = _from_filename(p)
    assert "V2" not in result
    assert "Philosophy" in result


def test_html_title_tag():
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False, encoding="utf-8") as f:
        f.write("<html><head><title>API Design Principles</title></head><body></body></html>")
        path = f.name
    assert detect_topic(path) == "API Design Principles"
