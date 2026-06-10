"""Inject source_anchor_v1 anchors into Markdown and generate JSONL index."""

import json
import re
from pathlib import Path

# Matches a previously injected anchor comment line, e.g. ``<!-- anchor:src-h0000 -->``.
# Page markers (``<!-- page 3 -->``) use a different prefix and are intentionally
# preserved — they are source content, not injected anchors.
_INJECTED_ANCHOR_RE = re.compile(r"^<!--\s*anchor:\S+\s*-->\s*$")


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

    for line_idx, line in enumerate(lines):
        line_num = line_idx + 1

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        figure_match = re.match(r"^!\[([^\]]*)\]", line)
        code_fence = re.match(r"^```(\w*)", line)

        if heading_match:
            level = len(heading_match.group(1))
            text_content = heading_match.group(2).strip()
            anchor_id = f"{source_id}-h{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                {
                    "schema_version": "source_anchor_v1",
                    "anchor_id": anchor_id,
                    "source_id": source_id,
                    "anchor_type": "heading",
                    "level": level,
                    "text": text_content,
                    "line_number": line_num,
                    "page_number": None,
                }
            )
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)

        elif figure_match:
            alt_text = figure_match.group(1)
            anchor_id = f"{source_id}-f{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                {
                    "schema_version": "source_anchor_v1",
                    "anchor_id": anchor_id,
                    "source_id": source_id,
                    "anchor_type": "figure",
                    "level": None,
                    "text": alt_text or f"figure at line {line_num}",
                    "line_number": line_num,
                    "page_number": None,
                }
            )
            output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)

        elif code_fence:
            lang = code_fence.group(1) or "code"
            anchor_id = f"{source_id}-c{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append(
                {
                    "schema_version": "source_anchor_v1",
                    "anchor_id": anchor_id,
                    "source_id": source_id,
                    "anchor_type": "code_block",
                    "level": None,
                    "text": f"code block ({lang}) at line {line_num}",
                    "line_number": line_num,
                    "page_number": None,
                }
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
                {
                    "schema_version": "source_anchor_v1",
                    "anchor_id": anchor_id,
                    "source_id": source_id,
                    "anchor_type": "page",
                    "level": None,
                    "text": f"page {page_num}",
                    "line_number": line_idx + 1,
                    "page_number": page_num,
                }
            )

    # Paragraph fallback: a structureless conversion (e.g. markitdown flattening a PDF to
    # one wall of text with no ``#`` headings, code fences, figures, or page markers) yields
    # zero anchors, leaving the Tier-1 evidence chain nothing to ground to — claims, evidence
    # records, and faithfulness checks all reference ``source_anchors`` that must exist in this
    # index, and ``validate_claims`` silently skips its referential check when the index is
    # empty. Anchor each paragraph (a word-bearing line opening a block) so flat sources still
    # carry real, referenceable spans. Only fires when no structural/page anchor was found, so
    # structured sources are unaffected. Idempotent: prior anchor comments are stripped above.
    if not anchors:
        output_lines = []
        prev_blank = True
        for line_idx, line in enumerate(lines):
            stripped = line.strip()
            is_blank = not stripped
            if prev_blank and not is_blank and len(re.findall(r"[A-Za-z]", stripped)) >= 3:
                anchor_id = f"{source_id}-t{anchor_counter:04d}"
                anchor_counter += 1
                anchors.append(
                    {
                        "schema_version": "source_anchor_v1",
                        "anchor_id": anchor_id,
                        "source_id": source_id,
                        "anchor_type": "paragraph",
                        "level": None,
                        "text": stripped[:120],
                        "line_number": line_idx + 1,
                        "page_number": None,
                    }
                )
                output_lines.append(f"<!-- anchor:{anchor_id} -->")
            output_lines.append(line)
            prev_blank = is_blank

    out_text = "\n".join(output_lines) + "\n"
    Path(output_md_path).write_text(out_text, encoding="utf-8")

    jsonl_lines = [json.dumps(a, ensure_ascii=False) for a in anchors]
    Path(anchors_jsonl_path).write_text("\n".join(jsonl_lines) + "\n", encoding="utf-8")

    return {"anchor_count": len(anchors), "anchors": anchors}
