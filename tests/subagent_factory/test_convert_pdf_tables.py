"""Tests for the opt-in Docling table-structure flag (Step-20 H, increment 1)."""

from tools.subagent_factory.convert_pdf import _tables_enabled


def test_tables_flag_default_off(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_DOCLING_TABLES", raising=False)
    assert _tables_enabled() is False


def test_tables_flag_truthy_values(monkeypatch):
    for v in ("1", "true", "TRUE", "yes", "on"):
        monkeypatch.setenv("SUBAGENT_FACTORY_DOCLING_TABLES", v)
        assert _tables_enabled() is True


def test_tables_flag_falsy_values(monkeypatch):
    for v in ("0", "false", "no", "", "off"):
        monkeypatch.setenv("SUBAGENT_FACTORY_DOCLING_TABLES", v)
        assert _tables_enabled() is False
