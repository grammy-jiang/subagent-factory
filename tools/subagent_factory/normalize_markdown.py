"""Normalize a Markdown file: front matter, heading hierarchy, whitespace."""

import re
from pathlib import Path

import yaml


def normalize_markdown(source_path: str | Path, output_path: str | Path, metadata: dict | None = None) -> dict:
    """
    Read Markdown, normalize it, write to output_path.

    Returns dict: markdown_text, warnings, front_matter
    """
    src = Path(source_path)
    text = src.read_text(encoding="utf-8", errors="replace")
    warnings = []

    front_matter, body = _split_front_matter(text)

    if metadata:
        front_matter.update({
            k: v for k, v in metadata.items()
            if v is not None and k not in front_matter
        })

    body = _normalize_headings(body)
    body = _normalize_whitespace(body)
    body = _normalize_code_fences(body)

    fm_block = ""
    if front_matter:
        fm_block = "---\n" + yaml.dump(front_matter, allow_unicode=True, sort_keys=False) + "---\n\n"

    normalized = fm_block + body
    Path(output_path).write_text(normalized, encoding="utf-8")

    return {
        "markdown_text": normalized,
        "warnings": warnings,
        "front_matter": front_matter,
        "word_count": len(body.split()),
    }


def _split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


def _normalize_headings(text: str) -> str:
    lines = text.splitlines()
    result = []
    for line in lines:
        m = re.match(r"^(#{1,6})(#{0,})(\s+.*)", line)
        if m:
            hashes = m.group(1)
            line = hashes + m.group(3)
        result.append(line)
    return "\n".join(result)


def _normalize_whitespace(text: str) -> str:
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def _normalize_code_fences(text: str) -> str:
    return re.sub(r"^(`{3,})(?!\n)", r"\1\n", text, flags=re.MULTILINE)
