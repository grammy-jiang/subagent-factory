"""Deterministic structural-degeneracy heuristic for extracted HTML tables (Step-20 H3).

This is **not** TEDS/GriTS. Those score a predicted table against a ground-truth table, which the
factory does not have at convert time — there is no reference grid to diff against. Instead this is
a cheap structural proxy: it flags tables whose *shape* looks like an extraction failure (no
rows/cells, header-only, single column, a mostly-empty grid) so a flag-on table-heavy convert can
route low-confidence tables to human review rather than silently grounding claims on a mangled grid.
A clean table returns ``ok=True`` with no reasons.

Pure stdlib (``html.parser``), deterministic, no ML — same contract as ``conversion_quality``.
"""

from html.parser import HTMLParser

# A grid this empty almost always means a borderless / dense-merged table that the parser could not
# segment — exactly the "route to review" case in the table-extraction research. Advisory, not a block.
_EMPTY_FRACTION = 0.6


class _TableShape(HTMLParser):
    """Walks one HTML table, tallying cells-per-row and empty cells. Tolerant of malformed markup."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[int] = []  # cells in each <tr>
        self.cells = 0
        self.empty = 0
        self._row_open = False
        self._row_count = 0
        self._cell_open = False
        self._cell_text = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        t = tag.lower()
        if t == "tr":
            self._flush_row()  # close an unterminated prior row
            self._row_open = True
            self._row_count = 0
        elif t in ("td", "th"):
            self._cell_open = True
            self._cell_text = ""
            self.cells += 1
            self._row_count += 1

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "tr":
            self._flush_row()
        elif t in ("td", "th"):
            if self._cell_open and not self._cell_text.strip():
                self.empty += 1
            self._cell_open = False

    def handle_data(self, data: str) -> None:
        if self._cell_open:
            self._cell_text += data

    def _flush_row(self) -> None:
        if self._row_open:
            self.rows.append(self._row_count)
            self._row_open = False


def table_quality(html: str) -> dict:
    """Structural-degeneracy verdict for one extracted table's HTML.

    Returns ``{ok, rows, cells, empty, max_cols, reasons}``. ``ok`` is True iff ``reasons`` is empty.
    Each reason names a shape that signals a likely extraction failure; the caller surfaces them as a
    WARN and routes the table to review. Never raises on ordinary markup.
    """
    p = _TableShape()
    p.feed(html or "")
    p._flush_row()  # close a trailing row with no </tr>
    rows = len(p.rows)
    cells = p.cells
    empty = p.empty
    max_cols = max(p.rows) if p.rows else 0
    reasons: list[str] = []
    if rows == 0:
        reasons.append("no rows")
    if cells == 0:
        reasons.append("no cells")
    if rows == 1:
        reasons.append("single row (header only, no data)")
    if cells and max_cols <= 1:
        reasons.append("single column (no tabular structure)")
    if cells and empty / cells >= _EMPTY_FRACTION:
        reasons.append(f"mostly empty ({empty}/{cells} cells)")
    return {
        "ok": not reasons,
        "rows": rows,
        "cells": cells,
        "empty": empty,
        "max_cols": max_cols,
        "reasons": reasons,
    }
