"""Tests for opt-in Docling table preservation (Step-20 H, parts 1 & 2)."""

from tools.subagent_factory.convert_pdf import _tables_enabled, _tables_to_html
from tools.subagent_factory.inject_anchors import inject_anchors


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


# ── _tables_to_html (part 2): replace pipe-table blocks with each table's HTML ──


class _FakeTable:
    def __init__(self, html):
        self._html = html

    def export_to_html(self, doc=None):
        return self._html


_PIPE = "| Region | Sales |\n| --- | --- |\n| EU | 120 |"


def test_pipe_block_replaced_with_html():
    md = f"# Returns\n\n{_PIPE}\n\nafter.\n"
    out = _tables_to_html(md, [_FakeTable("<table><tr><td>EU</td></tr></table>")])
    assert "<table>" in out and "| EU |" not in out  # pipe rows gone, HTML in
    assert "# Returns" in out and "after." in out  # surrounding text preserved


def test_two_blocks_two_tables_in_order():
    md = f"{_PIPE}\n\nmid\n\n{_PIPE}\n"
    out = _tables_to_html(md, [_FakeTable("<table>A</table>"), _FakeTable("<table>B</table>")])
    assert out.index("<table>A</table>") < out.index("mid") < out.index("<table>B</table>")


def test_stray_single_pipe_line_untouched():
    md = "a | b is not a table\n| just one row |\n"
    assert _tables_to_html(md, [_FakeTable("<table>X</table>")]) == md  # no ≥2 pipe block


def test_more_blocks_than_tables_extra_passthrough():
    md = f"{_PIPE}\n\n{_PIPE}\n"
    out = _tables_to_html(md, [_FakeTable("<table>only</table>")])
    assert (
        out.count("<table>only</table>") == 1 and "| EU | 120 |" in out
    )  # 2nd block left as pipes


def test_no_tables_verbatim():
    md = f"{_PIPE}\n"
    assert _tables_to_html(md, []) == md


# ── composition: part 2 output → part 3 anchoring (end-to-end, no PDF) ──


def test_html_table_then_anchored(tmp_path):
    md = f"# H\n\n{_PIPE}\n\nprose.\n"
    html_md = _tables_to_html(
        md, [_FakeTable("<table>\n<tr><td>EU</td><td>120</td></tr>\n</table>")]
    )
    inp = tmp_path / "in.md"
    inp.write_text(html_md, encoding="utf-8")
    res = inject_anchors(inp, tmp_path / "out.md", tmp_path / "a.jsonl", "s1")
    tabs = [a for a in res["anchors"] if a["anchor_type"] == "table"]
    assert len(tabs) == 1 and "EU" in tabs[0]["text"]  # part2 -> part3 composes
