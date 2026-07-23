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
    base_resolved = base.resolve()
    for source in manifest.get("sources", []):
        meta_path = (base / source.get("metadata_path", "")).resolve()
        sid = source.get("source_id")
        # Traversal guard: a manifest-supplied metadata_path that escapes the package tree is
        # untrusted — never read the out-of-tree file (inconsistent with redact_injection_spans' own
        # basename guard otherwise).
        if not meta_path.is_relative_to(base_resolved):
            continue
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
        # Basename the id before joining it into a path — a manifest-supplied source_id like
        # "../../etc/passwd" must not read outside sources/markdown/ (matches redact's guard).
        md_path = markdown_dir / f"{Path(source_id).name}.md"
        if md_path.exists():
            try:
                texts[source_id] = normalize_ws(md_path.read_text(encoding="utf-8"))
            except Exception:
                pass
    return texts


_DEFAULT_CACHE_ROOT = Path(__file__).parent.parent.parent / "cache" / "book-extracts"


def _manifest_sha_by_id(base: Path) -> dict[str, str]:
    """``source_id -> sha256`` from the package's ``source-pack.manifest.yaml`` (``{}`` if absent).

    A malformed manifest returns ``{}`` rather than raising: the cache loader is a *fallback* used
    only when ``sources/markdown/`` is empty, and a broken manifest already fails the dedicated
    manifest validator — here it just means "no cache linkage available", not a rights bypass (the
    caller then reports "could not scan", which fails no more open than the empty-source status quo)."""
    mf = base / "source-pack.manifest.yaml"
    if not mf.exists():
        return {}
    try:
        data = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError):
        return {}
    out: dict[str, str] = {}
    if isinstance(data, dict):
        for s in data.get("sources") or []:
            if isinstance(s, dict) and s.get("source_id") and s.get("sha256"):
                out[str(s["source_id"])] = str(s["sha256"])
    return out


def _find_book_module(sha: str, cache_root: Path) -> Path | None:
    """Locate ``<cache_root>/<sha>/`` for a manifest source sha, tolerating the sha12/sha64 prefix
    invariant (mirrors ``materials_catalog``'s matching). ``None`` when the cache is cold/absent."""
    if not sha or not cache_root.is_dir():
        return None
    direct = cache_root / sha
    if direct.is_dir():
        return direct
    for d in sorted(cache_root.glob("*/")):
        name = d.name
        if name == sha or name.startswith(sha) or (len(sha) == 64 and sha.startswith(name)):
            return d
    return None


def load_book_module_texts(
    base: str | Path, source_ids: set[str] | None = None, cache_root: str | Path | None = None
) -> dict[str, str]:
    """Whitespace-normalized source text from the map-reduce CACHE modules a package was built from.

    The map-reduce (Tier-1+) path never populates per-package ``sources/markdown/`` — distillation-only
    sources are withheld rights-clean — so ``load_source_texts`` is empty on the real corpus and the
    verbatim-quote gate is vacuous there. The untrusted book text still lives, content-addressed, in
    ``cache/book-extracts/<sha>/source.md`` (the sha is the package manifest's ``sources[].sha256``,
    which equals the cache dir for map-reduce packages). This loads it so the quote scan can actually
    run. ``source_ids`` restricts to a subset (e.g. the rights-restricted ids); ``None`` loads every
    manifest source. The pristine ``source.md.raw`` is preferred when present (injection redaction
    blanks whole lines, which would hide a verbatim quote on such a line). Returns ``{source_id: text}``;
    a source whose cache module is absent (cold cache) is simply omitted, so the caller can tell
    "scanned" from "could not scan" by whether any text came back.

    Rights note (same as ``load_source_texts``): rights restrict *emitted* quotation, not internal
    comparison — reading the cache source for the scan is allowed exactly as reading sources/markdown/ was."""
    base = Path(base)
    root = Path(cache_root) if cache_root is not None else _DEFAULT_CACHE_ROOT
    sha_by_id = _manifest_sha_by_id(base)
    ids = list(sha_by_id) if source_ids is None else list(source_ids)
    texts: dict[str, str] = {}
    for sid in ids:
        mod = _find_book_module(sha_by_id.get(sid, ""), root)
        if mod is None:
            continue
        src = mod / "source.md.raw"
        if not src.exists():
            src = mod / "source.md"
        if src.exists():
            try:
                texts[sid] = normalize_ws(src.read_text(encoding="utf-8"))
            except OSError:
                pass
    return texts


def contains_span(probe: str, source_texts: dict[str, str]) -> bool:
    """True if ``probe`` (already lowercased) is a substring of any source text."""
    return any(probe in src for src in source_texts.values())
