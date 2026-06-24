"""Main source ingestion entry point — Phase 1.5 of the authoring cycle."""

import hashlib
import shutil
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from tools.subagent_factory.convert_document import convert_document
from tools.subagent_factory.convert_pdf import preferred_pdf_converter as _preferred_pdf_converter
from tools.subagent_factory.detect_file_type import detect_file_type
from tools.subagent_factory.extract_assets import extract_assets
from tools.subagent_factory.fetch_url import fetch_url
from tools.subagent_factory.generate_conversion_report import generate_conversion_report
from tools.subagent_factory.generate_manifest import generate_manifest
from tools.subagent_factory.generate_metadata import generate_metadata
from tools.subagent_factory.inject_anchors import inject_anchors

# Canonical rights classifications (see .claude/rules/rights-and-quotation-policy.md).
VALID_RIGHTS_STATUSES = ("open", "distillation-only", "proprietary/restricted", "unknown")
# `unknown` is a blocking state: it must be resolved to a concrete status before a
# source may enter distillation. Per policy, never ingest with rights_status=unknown.
INGESTIBLE_RIGHTS_STATUSES = ("open", "distillation-only", "proprietary/restricted")


def _content_source_id(source_file: Path, sha256: str) -> str:
    """Deterministic, content-addressed source id: ``<slugified-stem>-<sha8>``.

    Stable across re-ingests of identical content, so a re-author reuses the same id and overwrites
    artifacts in place — rather than minting a fresh (formerly timestamped) id that orphans the
    prior profile / faithfulness / source-map references whenever a run is interrupted partway.
    The sha prefix is collision-safe (identical prefix ⇒ identical content).
    """
    stem = slugify(source_file.stem, max_length=20) or "source"
    return f"{stem}-{sha256[:8]}"


def _validate_rights(rights_status: str) -> str | None:
    """Error message if the rights classification blocks ingestion, else None.

    A typo here silently corrupts the rights gate that governs all downstream quotation, so the
    caller rejects it before any conversion work happens.
    """
    if rights_status not in VALID_RIGHTS_STATUSES:
        return (
            f"Invalid rights_status {rights_status!r}. "
            f"Must be one of: {', '.join(VALID_RIGHTS_STATUSES)}."
        )
    if rights_status not in INGESTIBLE_RIGHTS_STATUSES:
        return (
            "rights_status 'unknown' blocks distillation and must be resolved to a "
            "concrete status before ingestion (see rights-and-quotation-policy.md). "
            "For an authored work, the conservative floor is 'distillation-only'."
        )
    return None


def _resolve_source_file(
    source_input: str, subagent_path: Path, metadata_overrides: dict
) -> tuple[Path | None, dict[str, Any]]:
    """Resolve the input to a local source file.

    Returns ``(source_file, {})`` on success, or ``(None, abort)`` where ``abort`` carries the
    ``error`` (and ``needs_auth``) to merge into the result. A URL is fetched into
    ``sources/snapshots/`` and records its ``original_url`` override.
    """
    is_url = source_input.startswith("http://") or source_input.startswith("https://")
    if is_url:
        snapshots_dir = subagent_path / "sources" / "snapshots"
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        fetch_result = fetch_url(source_input, snapshots_dir)
        if fetch_result.get("needs_auth"):
            return None, {"needs_auth": True, "error": fetch_result["error"]}
        if fetch_result.get("error"):
            return None, {"error": fetch_result["error"]}
        metadata_overrides.setdefault("original_url", source_input)
        return Path(fetch_result["local_path"]), {}
    source_file = Path(source_input)
    if not source_file.exists():
        return None, {"error": f"Source file not found: {source_file}"}
    return source_file, {}


def _create_source_dirs(subagent_path: Path, source_id: str) -> dict[str, Path]:
    """Create + return the per-source directory layout under ``sources/``."""
    dirs = {
        "original": subagent_path / "sources" / "original" / source_id,
        "markdown": subagent_path / "sources" / "markdown",
        "assets": subagent_path / "sources" / "assets" / source_id,
        "anchors": subagent_path / "sources" / "anchors",
        "metadata": subagent_path / "sources" / "metadata",
        "reports": subagent_path / "sources" / "reports",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def _convert_or_restore(
    original_dest: Path, md_path: Path, cache_md: Path, file_type: str
) -> dict[str, Any]:
    """Convert the original to Markdown, or restore a cache hit (a synthetic ``converter='cache'``)."""
    if cache_md.exists():
        shutil.copy2(cache_md, md_path)
        cached_size = cache_md.stat().st_size
        return {
            "file_type": file_type,
            "markdown_text": "",  # not re-read from cache; emptiness is judged via cached_bytes
            "converter_used": "cache",
            "warnings": [],
            "errors": [],
            "stats": {"cached_bytes": cached_size},
            "from_cache": True,
        }
    return convert_document(original_dest, md_path)


def ingest_source(
    source_input: str,
    subagent_dir: str | Path,
    subagent_slug: str,
    source_id: str | None = None,
    **metadata_overrides,
) -> dict:
    """
    Full Phase 1.5 ingestion for one source (file path or URL).

    Creates:
      subagent_dir/sources/original/<source_id>/original.<ext>
      subagent_dir/sources/markdown/<source_id>.md
      subagent_dir/sources/assets/<source_id>/
      subagent_dir/sources/anchors/<source_id>.anchors.jsonl
      subagent_dir/sources/metadata/<source_id>.metadata.json
      subagent_dir/sources/reports/<source_id>.conversion-report.md

    Returns result dict.
    """
    subagent_path = Path(subagent_dir)
    result: dict[str, Any] = {
        "source_id": None,
        "original_path": None,
        "markdown_path": None,
        "metadata": None,
        "conversion_result": None,
        "anchor_count": 0,
        "asset_count": 0,
        "needs_auth": False,
        "already_ingested": False,
        "duplicate_source_slugs": [],
        "error": None,
    }

    # Fail fast on an invalid or non-ingestible rights classification, before any conversion work.
    rights_status = metadata_overrides.get("rights_status", "distillation-only")
    rights_error = _validate_rights(rights_status)
    if rights_error:
        result["error"] = rights_error
        return result

    # Resolve the input (URL fetch or local file) to a source file on disk.
    source_file, abort = _resolve_source_file(source_input, subagent_path, metadata_overrides)
    if source_file is None:
        result.update(abort)
        return result

    # sha256 dedup: skip if same content already ingested in THIS package
    sha256 = _sha256_file(source_file)
    manifest_path = subagent_path / "source-pack.manifest.yaml"
    if manifest_path.exists():
        existing_manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        for existing_source in existing_manifest.get("sources", []):
            if existing_source.get("sha256") == sha256:
                result["source_id"] = existing_source["source_id"]
                result["already_ingested"] = True
                return result

    # Cross-package duplicate detection. The per-slug dedup above only sees THIS
    # package's manifest; the embedding-based `search` is sha256-blind. An identical
    # source already authored under a *different* slug is therefore invisible, and an
    # already-distilled book can be silently re-authored as a redundant package.
    # Surface the match so the caller can confirm a genuinely distinct role (or update
    # the existing package) before proceeding. This warns, never blocks — distinct
    # subagents may legitimately share one source (see untrusted-source-policy WARN/triage).
    result["duplicate_source_slugs"] = find_cross_package_duplicates(
        subagent_path.parent, sha256, subagent_slug
    )

    file_type = detect_file_type(source_file)

    # Markdown cache: inputs/markdown-cache/<sha256>.<converter>.md
    # Avoids re-converting the same source across packages / rounds. The key is converter-keyed:
    # a PDF's entry is tagged with the *preferred available* PDF converter (docling > markitdown >
    # pymupdf), so installing Docling on top of a MarkItDown-cached corpus misses the old
    # `<sha>.markitdown.md` and forces a fresh, higher-fidelity Docling convert — no manual cache
    # purge. Non-PDF types key on the stable file_type. (Legacy bare `<sha>.md` entries are simply
    # never hit and ignored.)
    cache_dir = subagent_path.parent.parent / "inputs" / "markdown-cache"
    conv_tag = _preferred_pdf_converter() if file_type == "pdf" else file_type
    cache_md = cache_dir / f"{sha256}.{conv_tag}.md"

    if source_id is None:
        source_id = _content_source_id(source_file, sha256)
    result["source_id"] = source_id

    dirs = _create_source_dirs(subagent_path, source_id)

    # Preserve immutable original
    ext = source_file.suffix or f".{file_type}"
    original_dest = dirs["original"] / f"original{ext}"
    shutil.copy2(source_file, original_dest)
    result["original_path"] = str(original_dest)

    # Convert to Markdown (or restore from cache), then derive its status
    md_path = dirs["markdown"] / f"{source_id}.md"
    conversion_result = _convert_or_restore(original_dest, md_path, cache_md, file_type)
    conversion_result["conversion_status"] = _derive_status(conversion_result)
    result["conversion_result"] = conversion_result

    # Extract assets
    asset_result = extract_assets(md_path, dirs["assets"], source_id)
    result["asset_count"] = asset_result["asset_count"]

    # Inject anchors
    anchored_md = dirs["markdown"] / f"{source_id}.md"
    anchors_path = dirs["anchors"] / f"{source_id}.anchors.jsonl"
    anchor_result = inject_anchors(md_path, anchored_md, anchors_path, source_id)
    result["anchor_count"] = anchor_result["anchor_count"]
    result["markdown_path"] = str(anchored_md)

    # Populate markdown cache on fresh conversion
    if not conversion_result.get("from_cache") and conversion_result["conversion_status"] == "ok":
        cache_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(anchored_md, cache_md)

    # Generate metadata
    meta_path = dirs["metadata"] / f"{source_id}.metadata.json"
    metadata = generate_metadata(
        original_dest,
        source_id,
        file_type,
        conversion_result,
        meta_path,
        anchor_count=result["anchor_count"],
        asset_count=result["asset_count"],
        **metadata_overrides,
    )
    result["metadata"] = metadata

    # Generate conversion report
    report_path = dirs["reports"] / f"{source_id}.conversion-report.md"
    generate_conversion_report(
        source_id,
        source_file.name,
        conversion_result,
        report_path,
    )

    # Generate human-review queue entry if needed
    if conversion_result.get("conversion_status") in ("needs-human-review", "needs-ocr", "failed"):
        _append_human_review_queue(dirs["reports"], source_id, conversion_result)

    # Update manifest
    manifest_source = {
        "source_id": source_id,
        "original_filename": source_file.name,
        "sha256": metadata["sha256"],
        "conversion_status": conversion_result["conversion_status"],
        "metadata_path": f"sources/metadata/{source_id}.metadata.json",
        "markdown_path": f"sources/markdown/{source_id}.md",
        "anchors_path": f"sources/anchors/{source_id}.anchors.jsonl",
        "assets_path": f"sources/assets/{source_id}/",
    }
    generate_manifest(subagent_path, subagent_slug, [manifest_source])

    return result


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_cross_package_duplicates(
    packages_root: Path, sha256: str, current_slug: str
) -> list[dict[str, str]]:
    """Find sources in OTHER packages that share this sha256.

    Scans every ``<packages_root>/<slug>/source-pack.manifest.yaml`` except the
    current slug's, returning one ``{"slug", "source_id"}`` entry per match. Used
    to warn when an identical source has already been ingested under a different
    slug — a duplicate the per-slug dedup and the embedding-based search both miss.
    """
    matches: list[dict[str, str]] = []
    if not packages_root.is_dir():
        return matches
    for manifest_path in sorted(packages_root.glob("*/source-pack.manifest.yaml")):
        if manifest_path.parent.name == current_slug:
            continue
        try:
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            continue
        for src in data.get("sources", []):
            if src.get("sha256") == sha256:
                matches.append(
                    {
                        "slug": str(data.get("subagent_slug") or manifest_path.parent.name),
                        "source_id": str(src.get("source_id", "?")),
                    }
                )
    return matches


def _derive_status(conversion_result: dict) -> str:
    if conversion_result.get("errors"):
        if conversion_result.get("is_scanned"):
            return "needs-ocr"
        return "failed"
    if conversion_result.get("is_scanned"):
        return "needs-human-review"
    # One emptiness rule for both paths: a fresh convert is empty if its markdown_text is blank; a
    # cache hit is empty if it restored zero bytes. (No "_" sentinel faking non-empty for the cache.)
    if conversion_result.get("from_cache"):
        is_empty = conversion_result.get("stats", {}).get("cached_bytes", 0) == 0
    else:
        is_empty = not conversion_result.get("markdown_text", "").strip()
    if is_empty:
        return "failed"
    if conversion_result.get("low_quality"):
        return "needs-human-review"
    return "ok"


def _append_human_review_queue(reports_dir: Path, source_id: str, conversion_result: dict) -> None:
    queue_path = reports_dir / "human-review-queue.md"
    # Idempotent: re-ingesting a still-failing source must not append a duplicate block for the same
    # source_id (the ingest is designed to be re-run-safe).
    if queue_path.exists() and f"\n## {source_id}\n" in (
        "\n" + queue_path.read_text(encoding="utf-8")
    ):
        return
    reasons = conversion_result.get("errors", []) or ["Conversion quality requires review"]
    entry = f"\n## {source_id}\n\n"
    for r in reasons:
        entry += f"- {r}\n"
    with open(queue_path, "a", encoding="utf-8") as f:
        if queue_path.stat().st_size == 0:
            f.write("# Human Review Queue\n\n")
        f.write(entry)
