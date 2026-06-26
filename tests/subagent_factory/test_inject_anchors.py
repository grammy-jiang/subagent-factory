"""Tests for inject_anchors."""

import json
import re
import tempfile
import textwrap
from pathlib import Path

from tools.subagent_factory.inject_anchors import _is_pdf_noise, inject_anchors

MD_CONTENT = """# Introduction

Some text here.

## Section One

More text.

### Subsection

![A figure](image.png)

```python
print("hello")
```

Final paragraph.
"""


def test_anchors_generated():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_CONTENT)
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name

    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "test-source")
    assert result["anchor_count"] > 0

    jsonl_text = Path(out_jsonl).read_text()
    lines = [ln for ln in jsonl_text.strip().splitlines() if ln]
    anchors = [json.loads(ln) for ln in lines]

    types = {a["anchor_type"] for a in anchors}
    assert "heading" in types

    for a in anchors:
        assert a["schema_version"] == "source_anchor_v1"
        assert a["source_id"] == "test-source"
        assert a["anchor_id"].startswith("test-source-")


def test_anchor_comments_injected():
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(MD_CONTENT)
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name

    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    inject_anchors(src, out_md, out_jsonl, "test-source")
    output = Path(out_md).read_text()
    assert "<!-- anchor:test-source-" in output


def test_paragraph_fallback_for_structureless_source():
    """A flat conversion (no headings/code/figures/pages) gets paragraph anchors.

    markitdown often flattens a PDF to one wall of text. Without a fallback the anchor
    index is empty and the Tier-1 evidence chain has nothing to ground to. Each
    word-bearing paragraph must yield one ``paragraph`` anchor; noise-only lines must not.
    """
    flat = "First real paragraph of prose.\n\n}\n\nSecond paragraph of prose here.\n"
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(flat)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "flat-source")
    # Two prose paragraphs anchored; the bare ``}`` line (no word chars) is skipped.
    assert result["anchor_count"] == 2
    anchors = [json.loads(ln) for ln in Path(out_jsonl).read_text().strip().splitlines() if ln]
    assert {a["anchor_type"] for a in anchors} == {"paragraph"}
    # Paragraph anchors use the distinct ``-g`` prefix (NOT ``-t``, which is reserved for tables).
    assert all(a["anchor_id"].startswith("flat-source-g") for a in anchors)
    assert not any("-t" in a["anchor_id"][len("flat-source") :] for a in anchors)
    assert "<!-- anchor:flat-source-g0000 -->" in Path(out_md).read_text()


def test_is_pdf_noise_classifies_conversion_artifacts():
    """The noise predicate flags running heads / page numbers / TOC rows, spares real prose."""
    noise = [
        "DeepDiveintoOAuthandOpenIDConnect 43",  # running head + page number
        "57",  # bare page number
        "| 5. Deep | Dive | into | OAuth |",  # pipe TOC / table row
        "CONTENTS",  # short all-caps label
        "}",  # punctuation only
        "IntroducingAPISecurityConcepts",  # single concatenated heading token
    ]
    prose = [
        "Identity is at the forefront of API security and you must verify the caller.",
        "Base API security on proven, peer-reviewed standards with market adoption.",
        "We build with the assumption that even private APIs become exposed.",
        "Use TLS 1.3 for transport so the data stream stays confidential.",  # digits in prose
    ]
    assert all(_is_pdf_noise(n) for n in noise)
    assert not any(_is_pdf_noise(p) for p in prose)


def test_paragraph_fallback_skips_noise_and_subchunks_page_wall():
    """Heading-less book PDF: blanks only at page breaks, prose hard-wrapped, running heads.

    The naive "anchor each blank-delimited block opener" tags one running-head per page and
    leaves the body unanchored. The fallback must instead skip noise and anchor real prose,
    sub-chunking a long unbroken run so several anchors land per page.
    """
    sentence = "This sentence states an operational rule about secure API design. "
    wrapped_prose = "\n".join(textwrap.wrap(sentence * 12, 60))  # ~780 chars > _MAX_SPAN_CHARS
    pages = []
    for p in range(1, 4):
        pages.append(f"SecuringTheAPIStronghold {p}")  # running head + page number -> noise
        pages.append(wrapped_prose)  # body prose (no inter-paragraph blanks)
        pages.append(str(p))  # trailing bare page number -> noise
    md = "\n\n".join(pages) + "\n"  # blank lines ONLY at these page boundaries

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(md)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    inject_anchors(src, out_md, out_jsonl, "book")
    anchors = [json.loads(ln) for ln in Path(out_jsonl).read_text().strip().splitlines() if ln]

    # Every anchor is a paragraph anchor landing on real prose, never a running head / number.
    assert anchors
    assert {a["anchor_type"] for a in anchors} == {"paragraph"}
    assert all("SecuringTheAPIStronghold" not in a["text"] for a in anchors)
    assert all(not re.fullmatch(r"\d+", a["text"]) for a in anchors)
    # Sub-chunking: 3 pages of >600-char prose yield more than one anchor per page.
    assert len(anchors) > 3


def test_paragraph_fallback_is_idempotent():
    """Re-anchoring a flat file (cache reuse) yields the same paragraph-anchor count."""
    flat = "Alpha paragraph text.\n\nBeta paragraph text.\n"
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(flat)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        jsonl1 = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        jsonl2 = f.name

    r1 = inject_anchors(src, md, jsonl1, "src-A")
    r2 = inject_anchors(md, md, jsonl2, "src-B")
    output = Path(md).read_text()
    assert r2["anchor_count"] == r1["anchor_count"] == 2
    assert "src-A" not in output  # stale anchors stripped before re-anchoring


def test_reinjection_is_idempotent():
    """A cache reuse re-anchors an already-anchored file with a new source_id.

    Injection must strip prior anchor comments first, so a second pass yields the
    same anchor count, no stale source_id comments, and preserved page markers —
    never a stacked second anchor above every heading.
    """
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write("# Title\n\ntext\n\n## Section\n\n<!-- page 2 -->\n\nmore\n")
        src = f.name

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        md = f.name

    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        jsonl1 = f.name

    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        jsonl2 = f.name

    # First pass writes anchored markdown back to the same file (as ingest does).
    r1 = inject_anchors(src, md, jsonl1, "src-A")
    comments_after_first = Path(md).read_text().count("<!-- anchor:")
    # Second pass simulates a cache hit: same anchored file, fresh source_id.
    r2 = inject_anchors(md, md, jsonl2, "src-B")
    output = Path(md).read_text()

    assert r2["anchor_count"] == r1["anchor_count"]
    assert "src-A" not in output  # stale anchors stripped
    # No stacking: comment count is stable across passes (page anchors emit no comment).
    assert output.count("<!-- anchor:") == comments_after_first
    assert "<!-- page 2 -->" in output  # page markers preserved, not stripped


def test_page_anchor_line_number_is_input_relative():
    """A page anchor's line_number must index the INPUT line, like every other anchor type.

    Regression: pages were scanned over the POST-injection output (which has extra anchor-comment
    lines), offsetting their line_number by the count of injected comments above the marker. Here a
    heading injects one comment line before the page marker; the page anchor must still report the
    marker's INPUT line, and that input line must actually contain the marker.
    """
    src_text = "# Title\n\nbody text\n\n<!-- page 7 -->\n\nmore body\n"
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(src_text)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "src")
    page_anchors = [a for a in result["anchors"] if a["anchor_type"] == "page"]
    assert len(page_anchors) == 1
    pa = page_anchors[0]
    assert pa["page_number"] == 7

    # line_number is 1-based and must point at the INPUT line holding the page marker.
    input_lines = src_text.splitlines()
    assert "<!-- page 7 -->" in input_lines[pa["line_number"] - 1]


def test_repeated_page_marker_yields_distinct_anchor_ids():
    """The SAME page number appearing twice (PDF running header/footer, repeated front-matter)
    must still produce TWO anchors with DISTINCT anchor_id values.

    Regression: page anchor ids were derived from the page NUMBER (``src-p0007``), so two
    ``<!-- page 7 -->`` markers collided on one id. Any downstream that keys anchors by anchor_id
    (the package_queries / corpus_health anchor-id sets, dedup, the faithfulness index) then
    silently dropped one page's line_number. Each duplicate must keep its own input line number.
    """
    src_text = "# Title\n\n<!-- page 7 -->\n\nbody text\n\nmore body\n\n<!-- page 7 -->\n\ntail\n"
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(src_text)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "src")
    page_anchors = [a for a in result["anchors"] if a["anchor_type"] == "page"]
    assert len(page_anchors) == 2

    ids = [a["anchor_id"] for a in page_anchors]
    assert len(set(ids)) == 2, f"page anchor ids collided: {ids}"

    # Both record page 7, and the page number must still be recoverable from the record field.
    assert all(a["page_number"] == 7 for a in page_anchors)

    # Each anchor keeps its own INPUT-relative line number, pointing at a real page-7 marker.
    input_lines = src_text.splitlines()
    line_nums = sorted(a["line_number"] for a in page_anchors)
    assert len(set(line_nums)) == 2
    for ln in line_nums:
        assert "<!-- page 7 -->" in input_lines[ln - 1]

    # Ids must still end in a single type-letter + digits (validate_faithfulness_report's
    # ``-[a-z]\\d{3,}$`` pattern) and carry the page ``-p`` type letter.
    for aid in ids:
        assert re.search(r"-[a-z]\d{3,}$", aid)
        assert aid[len("src") :].startswith("-p")
    # Sanity: a heading anchor exists above it and shares the same INPUT-relative scale.
    heading = [a for a in result["anchors"] if a["anchor_type"] == "heading"][0]
    assert input_lines[heading["line_number"] - 1].startswith("# Title")


def test_unclosed_table_still_finalizes_record_and_does_not_crash():
    """A <table> with no </table> (truncated/malformed) must still yield a valid table anchor.

    Before the fix, ``in_table`` stayed True for the rest of the file. The single open-table record
    must be finalized with fallback text rather than left empty, and injection must complete.
    """
    md = "# Heading\n\n<table>\n<tr><td>row one</td></tr>\n<tr><td>row two</td></tr>\n"
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(md)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "src")
    tables = [a for a in result["anchors"] if a["anchor_type"] == "table"]
    assert len(tables) == 1
    # Accumulated inner-row text is non-empty (so the empty-text branch isn't what we assert), but
    # the key guarantee is the record is finalized and valid — text is always a non-empty string.
    assert isinstance(tables[0]["text"], str) and tables[0]["text"]


def test_unclosed_empty_table_gets_fallback_text():
    """An unclosed table with no extractable text falls back to ``table at line N``."""
    md = "<table>\n<tr></tr>\n"  # opens, never closes, no word content
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        f.write(md)
        src = f.name
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
        out_md = f.name
    with tempfile.NamedTemporaryFile(
        suffix=".jsonl", mode="w", delete=False, encoding="utf-8"
    ) as f:
        out_jsonl = f.name

    result = inject_anchors(src, out_md, out_jsonl, "src")
    tables = [a for a in result["anchors"] if a["anchor_type"] == "table"]
    assert len(tables) == 1
    assert tables[0]["text"].startswith("table at line")
