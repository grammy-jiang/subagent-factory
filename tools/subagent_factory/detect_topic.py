"""
Extract a content sample from a source file for expert-role inference.

The TOPIC of a source is not its title — it is the expert role that a
subagent built from this material would perform. That requires semantic
reasoning over content, which Claude does in the skill after receiving
the sample produced here.

This script's job: extract a compact, representative text sample:
  - All headings (H1–H3) to reveal structure
  - First ~1500 words of body text to reveal domain and intent
  - Table of contents entries when present

The skill reads this sample and answers:
  "What expert reviewer or advisor role would someone trained on this
   material become? (e.g. 'software design reviewer', 'API security
   auditor', 'distributed systems architect')"
"""

import re
from pathlib import Path

from tools.subagent_factory.convert_document import convert_document
from tools.subagent_factory.detect_file_type import detect_file_type

SAMPLE_WORDS = 1500
MAX_HEADINGS = 60


def extract_content_sample(source_path: str | Path) -> dict:
    """
    Extract a content sample for expert-role inference.

    Returns dict:
      headings      list[str]   — all H1–H3 heading texts, in order
      body_excerpt  str         — first ~1500 words of body text
      toc_entries   list[str]   — table of contents entries if found
      file_hint     str         — raw title/filename (lowest-priority hint only)
    """
    p = Path(source_path)
    if not p.exists():
        return _empty_sample(p)

    file_type = detect_file_type(p)

    conversion_error: str | None = None

    # For non-Markdown files, convert to Markdown first (in temp location)
    if file_type == "markdown":
        text = p.read_text(encoding="utf-8", errors="replace")
        text = _strip_front_matter(text)
    else:
        import tempfile

        # TemporaryDirectory removes the delete=False footgun structurally:
        # the temp file is always cleaned up when the context exits, even if
        # convert_document raises.
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = str(Path(tmp_dir) / "converted.md")
            try:
                result = convert_document(p, tmp_path)
            except Exception as exc:  # surface conversion failure to caller
                text = ""
                conversion_error = f"conversion raised: {type(exc).__name__}: {exc}"
            else:
                text = result.get("markdown_text", "")
                if not text:
                    text = (
                        Path(tmp_path).read_text(encoding="utf-8", errors="replace")
                        if Path(tmp_path).exists()
                        else ""
                    )
                if not text:
                    # Empty conversion is distinct from a genuinely empty source:
                    # signal it so role-inference does not silently degrade.
                    errors = result.get("errors") or []
                    conversion_error = (
                        "; ".join(errors) if errors else "conversion produced empty markdown"
                    )

    headings = _extract_headings(text)
    toc = _extract_toc(text)
    body = _extract_body_excerpt(text)
    file_hint = _file_hint(p)

    return {
        "headings": headings[:MAX_HEADINGS],
        "body_excerpt": body,
        "toc_entries": toc,
        "file_hint": file_hint,
        "conversion_error": conversion_error,
    }


def format_sample_for_inference(sample: dict) -> str:
    """
    Format a content sample as text Claude can read to infer expert role.
    """
    parts = []

    if sample.get("file_hint"):
        parts.append(f"[Source title hint: {sample['file_hint']}]")

    if sample.get("toc_entries"):
        parts.append("## Table of Contents\n" + "\n".join(sample["toc_entries"][:30]))

    if sample.get("headings"):
        parts.append("## Headings (structure)\n" + "\n".join(f"- {h}" for h in sample["headings"]))

    if sample.get("body_excerpt"):
        parts.append("## Opening content\n" + sample["body_excerpt"])

    return "\n\n".join(parts)


# ── extractors ─────────────────────────────────────────────────────────────


def _strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def _extract_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            headings.append(m.group(2).strip())
    return headings


def _extract_toc(text: str) -> list[str]:
    """Find a TOC block — lines that look like numbered or bulleted chapter listings."""
    toc_entries = []
    in_toc = False
    toc_re = re.compile(r"^(\d+[\.\)]|[-*])\s+.{5,80}$")

    for line in text.splitlines():
        low = line.lower().strip()
        if low in ("table of contents", "contents", "## table of contents", "# contents"):
            in_toc = True
            continue
        if in_toc:
            if toc_re.match(line.strip()):
                toc_entries.append(line.strip())
                if len(toc_entries) >= 40:
                    break
            elif line.strip() == "" and len(toc_entries) > 5:
                # blank line after some entries likely ends the TOC
                break
    return toc_entries


def _extract_body_excerpt(text: str) -> str:
    """
    Skip headings and blank lines, return first SAMPLE_WORDS words of body prose.
    """
    lines = []
    word_count = 0
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            continue
        if not line.strip():
            continue
        lines.append(line)
        word_count += len(line.split())
        if word_count >= SAMPLE_WORDS:
            break
    return "\n".join(lines)


def _file_hint(p: Path) -> str:
    stem = re.sub(r"[_\-]+", " ", p.stem)
    stem = re.sub(r"\bv\d+(\.\d+)*\b", "", stem, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", stem).strip().title()


def _empty_sample(p: Path) -> dict:
    return {
        "headings": [],
        "body_excerpt": "",
        "toc_entries": [],
        "file_hint": _file_hint(p),
        "conversion_error": None,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    sample = extract_content_sample(sys.argv[1])
    print(format_sample_for_inference(sample))
