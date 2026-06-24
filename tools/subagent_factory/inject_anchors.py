"""Inject source_anchor_v1 anchors into Markdown and generate JSONL index."""

import json
import re
from pathlib import Path

# Matches a previously injected anchor comment line, e.g. ``<!-- anchor:src-h0000 -->``.
# Page markers (``<!-- page 3 -->``) use a different prefix and are intentionally
# preserved — they are source content, not injected anchors.
_INJECTED_ANCHOR_RE = re.compile(r"^<!--\s*anchor:\S+\s*-->\s*$")

# Heading-less paragraph fallback tuning (see ``inject_anchors``).
# When a PDF→Markdown conversion flattens body prose into hard-wrapped lines with blank lines
# only at page boundaries, "anchor the opener of each blank-delimited block" degenerates to
# "anchor one running-head per page". The fallback therefore (a) skips conversion-noise lines
# and (b) sub-chunks a long unbroken prose run at sentence boundaries so anchors land on real
# body prose, evenly spaced, instead of page headers.
_MAX_SPAN_CHARS = 600  # soft target: open a new prose anchor past this, at the next sentence end
_HARD_CAP_CHARS = 1500  # hard cap: open one even with no sentence end in range
# A sentence terminator followed by whitespace or end-of-line. Detected anywhere in the line
# (not only at its end) because hard-wrapped PDF prose breaks lines mid-sentence, so sentence
# ends usually fall mid-line; requiring a line-final terminator would almost never sub-chunk.
_SENTENCE_BREAK_RE = re.compile(r'[.!?][")\'’”]?(\s|$)')


def _is_pdf_noise(stripped: str) -> bool:
    """True for a PDF-conversion noise line that must not receive a paragraph anchor.

    Targets the artifacts that dominate heading-less book conversions: running heads
    (``DeepDiveintoOAuth 43``), bare page numbers, pipe table-layout / TOC rows, short
    all-caps labels (``CONTENTS``), and near-empty lines. Deliberately conservative — real
    prose lines carry spaces and mixed punctuation, so the letters-then-digits and
    single-token tests cannot match them.
    """
    s = stripped.strip()
    if len(re.findall(r"[A-Za-z]", s)) < 3:
        return True  # blank / punctuation- or number-only line
    if "|" in s:
        return True  # pipe table-layout or TOC row
    nospace = re.sub(r"\s", "", s)
    if re.fullmatch(r"[A-Za-z]{2,}\d{1,4}", nospace):
        return True  # running head with a trailing page number
    if " " not in s and re.fullmatch(r"[A-Za-z]{12,}", nospace):
        return True  # single concatenated heading token (no body prose is one long word)
    if s.isupper() and len(s) < 30:
        return True  # short all-caps section label
    return False


_HTML_TAG_RE = re.compile(r"<[^>]+>")
# A caption line: "Table 3: ...", "Figure 12 ...", "Tbl. 2", "Fig 4 —" (proximity + reading order).
_CAPTION_RE = re.compile(r"^(table|figure|tbl|fig)\.?\s*\d+\b", re.IGNORECASE)


def _strip_html(s: str) -> str:
    """Drop HTML tags, collapse whitespace — for a table anchor's grounding text."""
    return " ".join(_HTML_TAG_RE.sub(" ", s).split())


def _table_caption(prior_lines: list[str]) -> str:
    """The immediately-preceding content line if it's a Table/Figure caption (Step-20 H2).

    Caption↔table association by proximity + reading order: scan back past blanks and injected
    anchor comments to the nearest real line; return it only if it looks like a caption. Empty
    otherwise. The forward case (caption *below* the table) is left to the follow-on.
    """
    for prev in reversed(prior_lines):
        s = prev.strip()
        if not s or s.startswith("<!-- anchor:"):
            continue
        return s if _CAPTION_RE.match(s) else ""
    return ""


def _make_anchor(
    anchor_id: str,
    source_id: str,
    anchor_type: str,
    text: str,
    line_number: int,
    *,
    level: int | None = None,
    page_number: int | None = None,
) -> dict:
    """One ``source_anchor_v1`` record. ``level`` is set for headings; ``page_number`` for pages."""
    return {
        "schema_version": "source_anchor_v1",
        "anchor_id": anchor_id,
        "source_id": source_id,
        "anchor_type": anchor_type,
        "level": level,
        "text": text,
        "line_number": line_number,
        "page_number": page_number,
    }


def inject_anchors(
    markdown_path: str | Path,
    output_md_path: str | Path,
    anchors_jsonl_path: str | Path,
    source_id: str,
) -> dict:
    """
    Read Markdown, inject HTML anchor comments, write JSONL index.

    Idempotent: any anchor comments left by a prior injection are stripped before
    re-anchoring. The markdown cache stores post-anchor Markdown, so a cache reuse
    feeds an already-anchored file back through this function with a new source_id;
    without stripping, each reuse would stack a second (stale-source_id) anchor above
    every heading and inflate line numbers.

    Returns dict: anchor_count, anchors list
    """
    src = Path(markdown_path)
    text = src.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not _INJECTED_ANCHOR_RE.match(ln)]

    anchors = []
    output_lines = []
    anchor_counter = 0
    in_table = False
    current_table: dict | None = None

    for line_idx, line in enumerate(lines):
        line_num = line_idx + 1

        # Table block (Step-20 H, part 3): an HTML <table> appears only when the Docling
        # table-structure flag was on. Anchor the whole block ONCE as a `-t` anchor (accumulating
        # its tag-stripped text for grounding) so claims can cite tabular facts; pass inner lines
        # through untouched. INERT when there is no <table> — current markdown has none, so default
        # behaviour is unchanged. Must run before the per-line heading/figure/code/noise logic so a
        # table's inner rows are never mis-anchored or skipped as pipe-noise.
        if in_table:
            output_lines.append(line)
            if current_table is not None:
                current_table["text"] = (current_table["text"] + " " + _strip_html(line)).strip()[
                    :600
                ]
            if "</table>" in line.lower():
                if current_table is not None and not current_table["text"]:
                    current_table["text"] = f"table at line {current_table['line_number']}"
                in_table, current_table = False, None
            continue
        if re.search(r"<table\b", line, re.IGNORECASE):
            caption = _table_caption(output_lines)  # H2: nearest preceding Table/Figure caption
            anchor_id = f"{source_id}-t{anchor_counter:04d}"
            anchor_counter += 1
            rec = _make_anchor(
                anchor_id,
                source_id,
                "table",
                f"{caption} {_strip_html(line)}".strip()[:600],
                line_num,
            )
            anchors.append(rec)
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)
            if "</table>" not in line.lower():
                in_table, current_table = True, rec  # multi-line: accumulate inner text
            elif not rec["text"]:
                rec["text"] = f"table at line {line_num}"  # single-line, empty
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        figure_match = re.match(r"^!\[([^\]]*)\]", line)
        code_fence = re.match(r"^```(\w*)", line)

        if heading_match:
            level = len(heading_match.group(1))
            text_content = heading_match.group(2).strip()
            anchor_id = f"{source_id}-h{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                _make_anchor(anchor_id, source_id, "heading", text_content, line_num, level=level)
            )
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)

        elif figure_match:
            alt_text = figure_match.group(1)
            anchor_id = f"{source_id}-f{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                _make_anchor(
                    anchor_id,
                    source_id,
                    "figure",
                    alt_text or f"figure at line {line_num}",
                    line_num,
                )
            )
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)

        elif code_fence:
            lang = code_fence.group(1) or "code"
            anchor_id = f"{source_id}-c{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                _make_anchor(
                    anchor_id,
                    source_id,
                    "code_block",
                    f"code block ({lang}) at line {line_num}",
                    line_num,
                )
            )
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)

        else:
            output_lines.append(line)

    # Page anchors from embedded page markers (e.g., from Docling)
    page_re = re.compile(r"<!-- page (\d+)", re.IGNORECASE)
    for line_idx, line in enumerate(output_lines):
        pm = page_re.search(line)
        if pm:
            page_num = int(pm.group(1))
            anchor_id = f"{source_id}-p{page_num:04d}"
            anchors.append(
                _make_anchor(
                    anchor_id,
                    source_id,
                    "page",
                    f"page {page_num}",
                    line_idx + 1,
                    page_number=page_num,
                )
            )

    # Paragraph fallback: a structureless conversion (e.g. markitdown flattening a PDF to
    # one wall of text with no ``#`` headings, code fences, figures, or page markers) yields
    # zero structural anchors, leaving the Tier-1 evidence chain nothing to ground to — claims,
    # evidence records, and faithfulness checks all reference ``source_anchors`` that must exist
    # in this index, and ``validate_claims`` silently skips its referential check when the index
    # is empty. Anchor real body prose so flat sources still carry referenceable spans. Only
    # fires when no structural/page anchor was found, so structured sources are unaffected.
    # Idempotent: prior anchor comments are stripped above.
    #
    # Two paragraph shapes occur and both must work:
    #   (a) blank-delimited paragraphs (markitdown wall-of-text) — anchor each block's opener;
    #   (b) hard-wrapped prose with blank lines only at PAGE boundaries (typical book PDF) —
    #       here "block opener" is the page running head, so naive anchoring tags ~one junk
    #       header per page and leaves the body unanchored. The fix: skip noise lines
    #       (``_is_pdf_noise``) and, within a long unbroken prose run, open a fresh anchor past
    #       ``_MAX_SPAN_CHARS`` at the next sentence end (or ``_HARD_CAP_CHARS`` regardless).
    if not anchors:
        output_lines = []
        pending_para = True  # True at a real paragraph start (after a blank, through any noise)
        chars_since = 0  # body chars accumulated since the last anchor (noise excluded)
        last_sentence_end = False
        for line_idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                pending_para = True
                output_lines.append(line)
                continue
            if _is_pdf_noise(stripped):
                output_lines.append(line)  # keep the line; never anchor noise
                continue
            anchor_here = (
                pending_para
                or (chars_since >= _MAX_SPAN_CHARS and last_sentence_end)
                or chars_since >= _HARD_CAP_CHARS
            )
            if anchor_here:
                anchor_id = f"{source_id}-t{anchor_counter:04d}"
                anchor_counter += 1
                anchors.append(
                    _make_anchor(anchor_id, source_id, "paragraph", stripped[:120], line_idx + 1)
                )
                output_lines.append(f"<!-- anchor:{anchor_id} -->")
                chars_since = 0
                pending_para = False
            output_lines.append(line)
            chars_since += len(stripped) + 1
            last_sentence_end = bool(_SENTENCE_BREAK_RE.search(stripped))

    out_text = "\n".join(output_lines) + "\n"
    Path(output_md_path).write_text(out_text, encoding="utf-8")

    jsonl_lines = [json.dumps(a, ensure_ascii=False) for a in anchors]
    Path(anchors_jsonl_path).write_text("\n".join(jsonl_lines) + "\n", encoding="utf-8")

    return {"anchor_count": len(anchors), "anchors": anchors}
