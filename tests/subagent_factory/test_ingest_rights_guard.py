"""Tests for the ingest rights-classification guard.

The rights gate governs all downstream quotation behaviour, so an invalid or
non-ingestible rights_status must be rejected before any conversion work runs.
"""

from tools.subagent_factory.ingest_source import (
    INGESTIBLE_RIGHTS_STATUSES,
    VALID_RIGHTS_STATUSES,
    ingest_source,
)


def test_typo_rights_status_is_rejected(tmp_path):
    result = ingest_source("/nonexistent/file.pdf", tmp_path, "demo", rights_status="restricted")
    assert result["error"]
    assert "Invalid rights_status" in result["error"]


def test_unknown_rights_status_blocks_ingestion(tmp_path):
    result = ingest_source("/nonexistent/file.pdf", tmp_path, "demo", rights_status="unknown")
    assert result["error"]
    assert "blocks distillation" in result["error"]


def test_valid_rights_passes_guard(tmp_path):
    # A canonical rights value clears the guard; failure now comes from the missing
    # source file, not from the rights check.
    result = ingest_source(
        "/nonexistent/file.pdf", tmp_path, "demo", rights_status="distillation-only"
    )
    assert result["error"]
    assert "rights_status" not in result["error"]
    assert "Source file not found" in result["error"]


def test_unknown_is_valid_but_not_ingestible():
    assert "unknown" in VALID_RIGHTS_STATUSES
    assert "unknown" not in INGESTIBLE_RIGHTS_STATUSES
