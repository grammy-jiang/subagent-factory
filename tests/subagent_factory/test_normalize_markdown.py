"""Tests for normalize_markdown."""

import tempfile
from pathlib import Path

from tools.subagent_factory.normalize_markdown import normalize_markdown


def test_basic_normalization():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Title\n\n\n\n\nSome text.\n")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        dst = f.name

    result = normalize_markdown(src, dst)
    output = Path(dst).read_text()
    assert "# Title" in output
    assert "\n\n\n\n\n" not in output
    assert result["word_count"] > 0


def test_front_matter_preserved():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("---\ntitle: Test\n---\n\n# Body\n")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        dst = f.name

    result = normalize_markdown(src, dst)
    assert result["front_matter"].get("title") == "Test"
    assert "# Body" in Path(dst).read_text()


def test_metadata_injection():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Plain doc\n\nNo front matter.\n")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        dst = f.name

    result = normalize_markdown(src, dst, metadata={"author": "Test Author"})
    assert result["front_matter"].get("author") == "Test Author"
