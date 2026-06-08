"""Main source ingestion entry point — Phase 1.5 of the authoring cycle."""

import hashlib
import shutil
from datetime import UTC, datetime
from pathlib import Path

import yaml
from slugify import slugify

from tools.subagent_factory.convert_document import convert_document
from tools.subagent_factory.detect_file_type import detect_file_type
from tools.subagent_factory.extract_assets import extract_assets
from tools.subagent_factory.fetch_url import fetch_url
from tools.subagent_factory.generate_conversion_report import generate_conversion_report
from tools.subagent_factory.generate_manifest import generate_manifest
from tools.subagent_factory.generate_metadata import generate_metadata
from tools.subagent_factory.inject_anchors import inject_anchors


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
    result = {
        "source_id": None,
        "original_path": None,
        "markdown_path": None,
        "metadata": None,
        "conversion_result": None,
        "anchor_count": 0,
        "asset_count": 0,
        "needs_auth": False,
        "already_ingested": False,
        "error": None,
    }

    # Handle URL
    is_url = source_input.startswith("http://") or source_input.startswith("https://")
    if is_url:
        snapshots_dir = subagent_path / "sources" / "snapshots"
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        fetch_result = fetch_url(source_input, snapshots_dir)
        if fetch_result.get("needs_auth"):
            result["needs_auth"] = True
            result["error"] = fetch_result["error"]
            return result
        if fetch_result.get("error"):
            result["error"] = fetch_result["error"]
            return result
        source_file = Path(fetch_result["local_path"])
        metadata_overrides.setdefault("original_url", source_input)
    else:
        source_file = Path(source_input)
        if not source_file.exists():
            result["error"] = f"Source file not found: {source_file}"
            return result

    # sha256 dedup: skip if same content already ingested
    sha256 = _sha256_file(source_file)
    manifest_path = subagent_path / "source-pack.manifest.yaml"
    if manifest_path.exists():
        existing_manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        for existing_source in existing_manifest.get("sources", []):
            if existing_source.get("sha256") == sha256:
                result["source_id"] = existing_source["source_id"]
                result["already_ingested"] = True
                return result

    file_type = detect_file_type(source_file)

    if source_id is None:
        stem = slugify(source_file.stem, max_length=20) or "source"
        ts = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        source_id = f"{stem}-{ts}"

    result["source_id"] = source_id

    # Create directory layout
    original_dir = subagent_path / "sources" / "original" / source_id
    markdown_dir = subagent_path / "sources" / "markdown"
    assets_dir = subagent_path / "sources" / "assets" / source_id
    anchors_dir = subagent_path / "sources" / "anchors"
    metadata_dir = subagent_path / "sources" / "metadata"
    reports_dir = subagent_path / "sources" / "reports"

    for d in [original_dir, markdown_dir, assets_dir, anchors_dir, metadata_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Preserve immutable original
    ext = source_file.suffix or f".{file_type}"
    original_dest = original_dir / f"original{ext}"
    shutil.copy2(source_file, original_dest)
    result["original_path"] = str(original_dest)

    # Convert to Markdown
    md_path = markdown_dir / f"{source_id}.md"
    conversion_result = convert_document(original_dest, md_path)
    conversion_result["conversion_status"] = _derive_status(conversion_result)
    result["conversion_result"] = conversion_result

    # Extract assets
    asset_result = extract_assets(md_path, assets_dir, source_id)
    result["asset_count"] = asset_result["asset_count"]

    # Inject anchors
    anchored_md = markdown_dir / f"{source_id}.md"
    anchors_path = anchors_dir / f"{source_id}.anchors.jsonl"
    anchor_result = inject_anchors(md_path, anchored_md, anchors_path, source_id)
    result["anchor_count"] = anchor_result["anchor_count"]
    result["markdown_path"] = str(anchored_md)

    # Generate metadata
    meta_path = metadata_dir / f"{source_id}.metadata.json"
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
    report_path = reports_dir / f"{source_id}.conversion-report.md"
    generate_conversion_report(
        source_id,
        source_file.name,
        conversion_result,
        report_path,
    )

    # Generate human-review queue entry if needed
    if conversion_result.get("conversion_status") in ("needs-human-review", "needs-ocr", "failed"):
        _append_human_review_queue(reports_dir, source_id, conversion_result)

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


def _derive_status(conversion_result: dict) -> str:
    if conversion_result.get("errors"):
        if conversion_result.get("is_scanned"):
            return "needs-ocr"
        return "failed"
    if conversion_result.get("is_scanned"):
        return "needs-human-review"
    if not conversion_result.get("markdown_text", "").strip():
        return "failed"
    if conversion_result.get("low_quality"):
        return "needs-human-review"
    return "ok"


def _append_human_review_queue(reports_dir: Path, source_id: str, conversion_result: dict) -> None:
    queue_path = reports_dir / "human-review-queue.md"
    reasons = conversion_result.get("errors", []) or ["Conversion quality requires review"]
    entry = f"\n## {source_id}\n\n"
    for r in reasons:
        entry += f"- {r}\n"
    with open(queue_path, "a", encoding="utf-8") as f:
        if queue_path.stat().st_size == 0:
            f.write("# Human Review Queue\n\n")
        f.write(entry)
