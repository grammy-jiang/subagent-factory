"""Tests for converter-agnostic scanned-PDF detection (convert_pdf._detect_scanned).

Regression guard for the finding that detection only fired on Docling's page
markers, so the default MarkItDown path never flagged a scanned PDF.
"""

from tools.subagent_factory.convert_pdf import _detect_scanned


def test_empty_text_is_scanned():
    assert _detect_scanned("") is True
    assert _detect_scanned("   \n\t ") is True


def test_real_page_count_flags_sparse_text_without_markers():
    # The fix: no Docling markers, but a real page count makes sparse text
    # (~0.5 chars/page) read as scanned. Old marker-only logic returned False.
    assert _detect_scanned("word " * 10, page_count=100) is True


def test_real_page_count_passes_rich_text():
    assert _detect_scanned("word " * 5000, page_count=2) is False


def test_docling_markers_still_detect_sparse_scan():
    text = "<!-- page 1 -->\n<!-- page 2 -->\n<!-- page 3 -->\n"
    assert _detect_scanned(text) is True


def test_no_page_signal_does_not_false_positive_on_real_text():
    # No markers, no page count, substantial text → born-digital, not scanned.
    assert _detect_scanned("word " * 100) is False


def test_no_page_signal_flags_near_empty_extraction():
    assert _detect_scanned("only a few words here") is True
