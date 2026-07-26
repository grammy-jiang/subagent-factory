"""Tests for the shared converter engine (_converter_common): attempt-function soft-fail behaviour
and Markdown stats counting. The soft-fail contract — return a (None, None, [], [errs]) tuple, never
raise — is what lets the per-format chains aggregate errors instead of crashing mid-ingest."""

from pathlib import Path

import tools.subagent_factory._converter_common as cc


def test_try_pandoc_soft_fails_on_bad_input():
    # pandoc missing, or pandoc run against a nonexistent file → soft error tuple, never raises.
    text, used, _warns, errs = cc.try_pandoc(Path("does-not-exist.docx"), "docx")
    assert text is None and used is None and errs


def test_try_markitdown_soft_fails_when_unavailable(monkeypatch):
    # Simulate markitdown absent AND un-installable — mock ensure_package so no real self-heal pip
    # install is triggered by the test.
    monkeypatch.setattr(cc, "ensure_package", lambda name, purpose="": None)
    text, used, _warns, errs = cc.try_markitdown(Path("x.docx"), "DOCX conversion")
    assert text is None and used is None
    assert errs and "markitdown" in errs[0].lower()


def test_compute_stats_counts_markdown_elements():
    md = (
        "# Heading\n\nfive plain words here now\n\n```\ncode\n```\n\n"
        "| a | b |\n| - | - |\n\n![f](p.png)\n"
    )
    s = cc.compute_stats(md)
    assert s["heading_count"] == 1
    assert s["code_block_count"] == 1
    assert s["figure_count"] == 1
    assert s["table_count"] >= 1
    assert s["word_count"] > 0
