"""Tests for detect_topic (content sample extraction)."""

import glob
import tempfile
from pathlib import Path

from tools.subagent_factory import detect_topic
from tools.subagent_factory.detect_topic import (
    _extract_body_excerpt,
    _extract_headings,
    _file_hint,
    extract_content_sample,
    format_sample_for_inference,
)

MD_WITH_FRONTMATTER = """\
---
title: Clean Architecture Guide
author: Test Author
---

# Introduction

This book covers software architecture principles.

## Chapter 1 — Boundaries

Code depends on abstractions, not concretions.

## Chapter 2 — Use Cases

Business rules live in the application layer.
"""

MD_NO_FRONTMATTER = """\
# Designing Reliable Systems

Systems fail. This book teaches fault tolerance and resilience patterns.

## Chapter 1 — Failure Modes

Every component will eventually fail.

## Chapter 2 — Redundancy

Replicate data and computation.
"""

MD_MINIMAL = "No headings, no front matter. Just a sentence."


def test_extracts_headings():
    sample = _extract_headings(MD_WITH_FRONTMATTER)
    assert "Introduction" in sample
    assert "Chapter 1 — Boundaries" in sample


def test_extracts_body_excerpt():
    body = _extract_body_excerpt(MD_WITH_FRONTMATTER)
    assert "software architecture" in body
    assert "Introduction" not in body  # headings excluded


def test_extract_content_sample_markdown():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_WITH_FRONTMATTER)
        path = f.name

    sample = extract_content_sample(path)
    assert len(sample["headings"]) >= 2
    assert "software architecture" in sample["body_excerpt"]
    assert isinstance(sample["file_hint"], str)


def test_extract_content_sample_no_front_matter():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_NO_FRONTMATTER)
        path = f.name

    sample = extract_content_sample(path)
    assert "Designing Reliable Systems" in sample["headings"]
    assert "fault tolerance" in sample["body_excerpt"]


def test_format_for_inference_contains_headings():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_WITH_FRONTMATTER)
        path = f.name

    sample = extract_content_sample(path)
    formatted = format_sample_for_inference(sample)
    assert "Headings" in formatted
    assert "Opening content" in formatted
    assert "Chapter 1" in formatted


def test_file_hint_strips_version():
    p = Path("/tmp/a_philosophy_of_software_design_v2.md")
    hint = _file_hint(p)
    assert "V2" not in hint
    assert "Philosophy" in hint


def test_nonexistent_file_returns_empty():
    sample = extract_content_sample("/tmp/does_not_exist_xyz.md")
    assert sample["headings"] == []
    assert sample["body_excerpt"] == ""
    assert sample["conversion_error"] is None


def test_markdown_path_has_no_conversion_error():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_WITH_FRONTMATTER)
        path = f.name

    sample = extract_content_sample(path)
    assert sample["conversion_error"] is None


def test_nonmarkdown_conversion_succeeds_without_leaking_tempfile(monkeypatch, tmp_path):
    """A non-Markdown source is converted without leaking the temp file."""
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.4 fake")

    monkeypatch.setattr(detect_topic, "detect_file_type", lambda p: "pdf")
    monkeypatch.setattr(
        detect_topic,
        "convert_document",
        lambda p, out: {
            "markdown_text": "# Converted Title\n\nReliable distributed systems content.",
            "errors": [],
        },
    )

    before = set(glob.glob(str(Path(tempfile.gettempdir()) / "*")))
    sample = extract_content_sample(str(src))
    after = set(glob.glob(str(Path(tempfile.gettempdir()) / "*")))

    assert "Converted Title" in sample["headings"]
    assert sample["conversion_error"] is None
    # No leftover temp artifacts created by the conversion path.
    assert after == before


def test_nonmarkdown_conversion_failure_is_surfaced(monkeypatch, tmp_path):
    """When convert_document raises, the dict carries a conversion_error signal."""
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.4 fake")

    monkeypatch.setattr(detect_topic, "detect_file_type", lambda p: "pdf")

    def _boom(p, out):
        raise RuntimeError("converter exploded")

    monkeypatch.setattr(detect_topic, "convert_document", _boom)

    sample = extract_content_sample(str(src))
    assert sample["body_excerpt"] == ""
    assert sample["conversion_error"] is not None
    assert "converter exploded" in sample["conversion_error"]


def test_nonmarkdown_empty_conversion_is_distinguished(monkeypatch, tmp_path):
    """An empty conversion is signalled, not silently degraded to text=''."""
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.4 fake")

    monkeypatch.setattr(detect_topic, "detect_file_type", lambda p: "pdf")
    monkeypatch.setattr(
        detect_topic,
        "convert_document",
        lambda p, out: {"markdown_text": "", "errors": ["no converter for file type: pdf"]},
    )

    sample = extract_content_sample(str(src))
    assert sample["body_excerpt"] == ""
    assert sample["conversion_error"] is not None
