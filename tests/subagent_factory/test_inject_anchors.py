"""Tests for inject_anchors."""

import json
import tempfile
from pathlib import Path

from tools.subagent_factory.inject_anchors import inject_anchors

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
