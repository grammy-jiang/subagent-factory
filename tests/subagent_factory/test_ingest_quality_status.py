"""Tests for ingest conversion-status derivation, incl. the low-quality gate."""

from tools.subagent_factory.ingest_source import _derive_status


def test_clean_conversion_is_ok():
    assert _derive_status({"markdown_text": "real content here", "low_quality": False}) == "ok"


def test_low_quality_routes_to_human_review():
    assert _derive_status({"markdown_text": "x" * 20, "low_quality": True}) == "needs-human-review"


def test_scanned_routes_to_human_review():
    assert _derive_status({"markdown_text": "x", "is_scanned": True}) == "needs-human-review"


def test_errors_with_scanned_is_needs_ocr():
    assert _derive_status({"errors": ["e"], "is_scanned": True, "markdown_text": ""}) == "needs-ocr"


def test_errors_without_text_is_failed():
    assert _derive_status({"errors": ["boom"], "markdown_text": ""}) == "failed"


def test_empty_text_is_failed():
    assert _derive_status({"markdown_text": "   "}) == "failed"
