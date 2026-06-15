"""Tests for the structural-degeneracy heuristic (Step-20 H3) and its convert-time wiring."""

from tools.subagent_factory.convert_pdf import _table_warnings
from tools.subagent_factory.table_quality import table_quality

_CLEAN = (
    "<table>"
    "<tr><th>Region</th><th>Q1</th><th>Q2</th></tr>"
    "<tr><td>EU</td><td>120</td><td>130</td></tr>"
    "<tr><td>US</td><td>200</td><td>210</td></tr>"
    "</table>"
)


def test_clean_table_ok():
    q = table_quality(_CLEAN)
    assert q["ok"] is True
    assert q["reasons"] == []
    assert q["rows"] == 3 and q["cells"] == 9 and q["max_cols"] == 3


def test_empty_string_no_rows():
    q = table_quality("")
    assert q["ok"] is False and "no rows" in q["reasons"]


def test_empty_table_element():
    q = table_quality("<table></table>")
    assert q["ok"] is False and "no rows" in q["reasons"]


def test_header_only_single_row_flagged():
    q = table_quality("<table><tr><th>A</th><th>B</th></tr></table>")
    assert q["ok"] is False
    assert any("single row" in r for r in q["reasons"])


def test_single_column_flagged():
    html = "<table><tr><td>a</td></tr><tr><td>b</td></tr><tr><td>c</td></tr></table>"
    q = table_quality(html)
    assert q["ok"] is False
    assert any("single column" in r for r in q["reasons"])
    assert q["max_cols"] == 1


def test_mostly_empty_flagged():
    # 2x3 grid, only 1 of 6 cells has content → ≥0.6 empty
    html = (
        "<table><tr><td>x</td><td></td><td>  </td></tr><tr><td></td><td></td><td></td></tr></table>"
    )
    q = table_quality(html)
    assert q["ok"] is False
    assert any("mostly empty" in r for r in q["reasons"])
    assert q["empty"] == 5 and q["cells"] == 6


def test_whitespace_cells_count_as_empty():
    q = table_quality("<table><tr><td>   </td><td>\n\t</td></tr></table>")
    assert q["empty"] == 2


def test_ragged_table_uses_widest_row_for_max_cols():
    # a wide data row keeps max_cols > 1 even if another row is short → not "single column"
    html = "<table><tr><td>a</td><td>b</td><td>c</td></tr><tr><td>d</td></tr></table>"
    q = table_quality(html)
    assert q["max_cols"] == 3
    assert not any("single column" in r for r in q["reasons"])


# ── _table_warnings: convert-time wiring (advisory, swallows errors) ──


class _FakeTable:
    def __init__(self, html):
        self._html = html

    def export_to_html(self, doc=None):
        return self._html


class _BoomTable:
    def export_to_html(self, doc=None):
        raise RuntimeError("export blew up")


def test_table_warnings_only_for_degenerate():
    tables = [_FakeTable(_CLEAN), _FakeTable("<table><tr><th>only header</th></tr></table>")]
    warns = _table_warnings(tables)
    assert len(warns) == 1
    assert warns[0].startswith("Table 1:")  # index 1 is the degenerate one
    assert "single row" in warns[0]


def test_table_warnings_clean_is_silent():
    assert _table_warnings([_FakeTable(_CLEAN), _FakeTable(_CLEAN)]) == []


def test_table_warnings_swallows_export_errors():
    # a table that raises on export must not break the convert — it is skipped, not reported
    assert _table_warnings([_BoomTable(), _FakeTable(_CLEAN)]) == []


def test_table_warnings_empty_list():
    assert _table_warnings([]) == []
