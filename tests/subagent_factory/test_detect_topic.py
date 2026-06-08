"""Tests for detect_topic (content sample extraction)."""

import tempfile
from pathlib import Path

from tools.subagent_factory.detect_topic import (
    extract_content_sample,
    format_sample_for_inference,
    _file_hint,
    _extract_headings,
    _extract_toc,
    _extract_body_excerpt,
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
