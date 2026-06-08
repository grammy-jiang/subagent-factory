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

    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
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

    with tempfile.NamedTemporaryFile(suffix=".jsonl", mode="w", delete=False, encoding="utf-8") as f:
        out_jsonl = f.name

    inject_anchors(src, out_md, out_jsonl, "test-source")
    output = Path(out_md).read_text()
    assert "<!-- anchor:test-source-" in output
