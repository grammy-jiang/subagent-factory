"""Inject source_anchor_v1 anchors into Markdown and generate JSONL index."""

import json
import re
from pathlib import Path


def inject_anchors(
    markdown_path: str | Path,
    output_md_path: str | Path,
    anchors_jsonl_path: str | Path,
    source_id: str,
) -> dict:
    """
    Read Markdown, inject HTML anchor comments, write JSONL index.

    Returns dict: anchor_count, anchors list
    """
    src = Path(markdown_path)
    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()

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
            anchors.append({
                "schema_version": "source_anchor_v1",
                "anchor_id": anchor_id,
                "source_id": source_id,
                "anchor_type": "heading",
                "level": level,
                "text": text_content,
                "line_number": line_num,
                "page_number": None,
            })
            output_lines.append(f'<!-- anchor:{anchor_id} -->')
            output_lines.append(line)

        elif figure_match:
            alt_text = figure_match.group(1)
            anchor_id = f"{source_id}-f{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append({
                "schema_version": "source_anchor_v1",
                "anchor_id": anchor_id,
                "source_id": source_id,
                "anchor_type": "figure",
                "level": None,
                "text": alt_text or f"figure at line {line_num}",
                "line_number": line_num,
                "page_number": None,
            })
            output_lines.append(f'<!-- anchor:{anchor_id} -->')
            output_lines.append(line)

        elif code_fence:
            lang = code_fence.group(1) or "code"
            anchor_id = f"{source_id}-c{anchor_counter:04d}"
            anchor_counter += 1
            anchors.append({
                "schema_version": "source_anchor_v1",
                "anchor_id": anchor_id,
                "source_id": source_id,
                "anchor_type": "code_block",
                "level": None,
                "text": f"code block ({lang}) at line {line_num}",
                "line_number": line_num,
                "page_number": None,
            })
            output_lines.append(f'<!-- anchor:{anchor_id} -->')
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
            anchors.append({
                "schema_version": "source_anchor_v1",
                "anchor_id": anchor_id,
                "source_id": source_id,
                "anchor_type": "page",
                "level": None,
                "text": f"page {page_num}",
                "line_number": line_idx + 1,
                "page_number": page_num,
            })

    out_text = "\n".join(output_lines) + "\n"
    Path(output_md_path).write_text(out_text, encoding="utf-8")

    jsonl_lines = [json.dumps(a, ensure_ascii=False) for a in anchors]
    Path(anchors_jsonl_path).write_text("\n".join(jsonl_lines) + "\n", encoding="utf-8")

    return {"anchor_count": len(anchors), "anchors": anchors}
