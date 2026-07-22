"""Shared access to ingested source text.

Extracted from ``quote_scan`` so other gates (the prompt-injection scan and the
faithfulness checks added in enhancement Steps 1/3) reuse the exact loader and
whitespace normaliser the rights gate already uses. The functions here are the
originals moved verbatim, so ``quote_scan`` behaviour is preserved.

Rights note: the source markdown is stored in-repo regardless of licence; rights
restrict *emitted* quotation, not internal comparison. ``load_restricted_source_ids``
selects the rights-restricted subset for the verbatim-quote gate; the injection /
faithfulness gates pass ``source_ids=None`` to load every source.
"""

import json
import re
from pathlib import Path

import yaml


def normalize_ws(text: str) -> str:
    """Lowercase and collapse every run of whitespace to a single space.

    The verbatim probe is built with ``str.split()`` + single-space ``join``, so it
    is whitespace-normalized. The source side must be normalized the same way or the
    substring match fails on the most common PDF-conversion artifacts — line-wrap
    newlines and the double spaces converters emit between words.
    """
    return re.sub(r"\s+", " ", text.lower())


def load_restricted_source_ids(base: str | Path) -> set[str]:
    """Source IDs whose rights forbid verbatim quotation (restricted / distillation-only)."""
    base = Path(base)
    restricted: set[str] = set()
    manifest_path = base / "source-pack.manifest.yaml"
    if not manifest_path.exists():
        return restricted
    # This set drives quote_scan's rights enforcement: silently returning an empty set on a read
    # error would FAIL OPEN (a restricted source goes unflagged, allowing verbatim quotation). So a
    # manifest-level failure propagates; only a single unreadable/malformed per-source meta is skipped
    # (treated as "rights unknown" — and an unknown source is conservatively flagged restricted).
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}
    for source in manifest.get("sources", []):
        meta_path = base / source.get("metadata_path", "")
        sid = source.get("source_id")
        if not meta_path.exists():
            continue
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, json.JSONDecodeError):
            # rights unknown for this source → conservative floor: treat as restricted, don't skip it.
            if sid:
                restricted.add(sid)
            continue
        rights = meta.get("rights_status", "")
        if "restricted" in rights.lower() or "distillation-only" in rights.lower():
            restricted.add(sid)
    return restricted


def load_source_texts(base: str | Path, source_ids: set[str] | None = None) -> dict[str, str]:
    """Whitespace-normalized text of ``sources/markdown/<id>.md``.

    ``source_ids=None`` loads every markdown source; pass a set to restrict (e.g. the
    rights-restricted subset for the quote gate).
    """
    base = Path(base)
    texts: dict[str, str] = {}
    markdown_dir = base / "sources" / "markdown"
    if not markdown_dir.exists():
        return texts
    ids = [p.stem for p in markdown_dir.glob("*.md")] if source_ids is None else list(source_ids)
    for source_id in ids:
        md_path = markdown_dir / f"{source_id}.md"
        if md_path.exists():
            try:
                texts[source_id] = normalize_ws(md_path.read_text(encoding="utf-8"))
            except Exception:
                pass
    return texts


def contains_span(probe: str, source_texts: dict[str, str]) -> bool:
    """True if ``probe`` (already lowercased) is a substring of any source text."""
    return any(probe in src for src in source_texts.values())
