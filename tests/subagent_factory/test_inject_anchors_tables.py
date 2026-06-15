"""Tests for HTML-table anchoring (Step-20 H, part 3).

Synthetic markdown only — no Docling/PDF. The table branch is additive + inert: it triggers only on
an HTML <table> block (which the converter emits only under the table-structure flag), so table-free
markdown is unaffected.
"""

from tools.subagent_factory.inject_anchors import inject_anchors


def _run(tmp_path, md, sid="s1"):
    inp = tmp_path / "in.md"
    inp.write_text(md, encoding="utf-8")
    out = tmp_path / "out.md"
    res = inject_anchors(inp, out, tmp_path / "a.jsonl", sid)
    return res["anchors"], out.read_text(encoding="utf-8")


def _tables(anchors):
    return [a for a in anchors if a["anchor_type"] == "table"]


def test_multiline_table_one_anchor_with_text(tmp_path):
    md = (
        "# Returns\n\n"
        "<table>\n"
        "<tr><td>Region</td><td>Sales</td></tr>\n"
        "<tr><td>EU</td><td>120</td></tr>\n"
        "</table>\n\n"
        "prose after the table.\n"
    )
    anchors, out = _run(tmp_path, md)
    tabs = _tables(anchors)
    assert len(tabs) == 1
    assert "EU" in tabs[0]["text"] and "Sales" in tabs[0]["text"]  # accumulated, tag-stripped
    assert f"<!-- anchor:{tabs[0]['anchor_id']} -->" in out  # anchor comment injected
    assert tabs[0]["anchor_id"].startswith("s1-t")


def test_single_line_table(tmp_path):
    anchors, _ = _run(tmp_path, "<table><tr><td>a</td><td>b</td></tr></table>\n")
    tabs = _tables(anchors)
    assert len(tabs) == 1 and "a" in tabs[0]["text"]


def test_no_table_is_inert_and_headings_still_anchor(tmp_path):
    # pipe-rows are NOT html tables → no table anchor; headings still anchored (unchanged behaviour)
    md = "# Heading\n\nsome prose here.\n\n| a | b |\n| 1 | 2 |\n"
    anchors, _ = _run(tmp_path, md)
    assert _tables(anchors) == []
    assert any(a["anchor_type"] == "heading" for a in anchors)


def test_table_inner_lines_not_misanchored(tmp_path):
    # a heading-looking line inside the table must not become a heading anchor
    md = "<table>\n# not a heading\n<tr><td>x</td></tr>\n</table>\n"
    anchors, _ = _run(tmp_path, md)
    assert len(_tables(anchors)) == 1
    assert not any(a["anchor_type"] == "heading" for a in anchors)


def test_multiple_tables_each_anchored(tmp_path):
    md = "<table><tr><td>1</td></tr></table>\n\nbetween\n\n<table>\n<tr><td>2</td></tr>\n</table>\n"
    anchors, _ = _run(tmp_path, md)
    assert len(_tables(anchors)) == 2


# ── H2: caption↔table association (caption above the table, by proximity + reading order) ──


def test_caption_directly_above_table_captured(tmp_path):
    md = "Table 3: Quarterly sales\n<table><tr><td>EU</td><td>120</td></tr></table>\n"
    tabs = _tables(_run(tmp_path, md)[0])
    assert len(tabs) == 1
    assert tabs[0]["text"].startswith("Table 3: Quarterly sales")  # caption seeded into text
    assert "EU" in tabs[0]["text"]  # plus the table content


def test_caption_with_blank_line_between_captured(tmp_path):
    # the helper scans back past blanks/anchor-comments to the nearest content line
    md = "Figure 2 — pipeline stages\n\n<table>\n<tr><td>x</td></tr>\n</table>\n"
    tabs = _tables(_run(tmp_path, md)[0])
    assert tabs[0]["text"].startswith("Figure 2 — pipeline stages")


def test_non_caption_prose_above_table_not_captured(tmp_path):
    # an ordinary sentence is not a caption → text must NOT start with it
    md = "Here is the data we collected.\n<table><tr><td>x</td></tr></table>\n"
    tabs = _tables(_run(tmp_path, md)[0])
    assert not tabs[0]["text"].startswith("Here is the data")


def test_caption_above_earlier_heading_not_crossed(tmp_path):
    # nearest content line is the heading, not a caption → no caption seeded
    md = "## Section\n<table><tr><td>x</td></tr></table>\n"
    tabs = _tables(_run(tmp_path, md)[0])
    assert not tabs[0]["text"].startswith("## Section")
    assert not tabs[0]["text"].startswith("Section")
