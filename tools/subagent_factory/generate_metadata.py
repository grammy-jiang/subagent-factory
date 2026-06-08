"""Generate source metadata JSON from ingestion results."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def generate_metadata(
    original_path: str | Path,
    source_id: str,
    file_type: str,
    conversion_result: dict,
    output_path: str | Path,
    **overrides,
) -> dict:
    """
    Build and write source metadata JSON.

    Returns metadata dict.
    """
    orig = Path(original_path)

    sha256 = _sha256(orig)
    file_size = orig.stat().st_size

    stats = conversion_result.get("stats", {})

    metadata = {
        "schema_version": "source-metadata-v1",
        "source_id": source_id,
        "title": overrides.get("title") or orig.stem.replace("-", " ").replace("_", " ").title(),
        "author": overrides.get("author"),
        "year": overrides.get("year"),
        "source_type": file_type,
        "file_type": file_type,
        "original_filename": orig.name,
        "original_url": overrides.get("original_url"),
        "sha256": sha256,
        "file_size_bytes": file_size,
        "authority": overrides.get("authority", "secondary"),
        "rights_status": overrides.get("rights_status", "distillation-only"),
        "volatility": overrides.get("volatility", "low"),
        "review_cadence": overrides.get("review_cadence", "annual"),
        "conversion_status": conversion_result.get("conversion_status", "ok"),
        "converter_used": conversion_result.get("converter_used"),
        "converter_warnings": conversion_result.get("warnings", []),
        "page_count": stats.get("page_count"),
        "word_count": stats.get("word_count"),
        "anchor_count": overrides.get("anchor_count"),
        "asset_count": overrides.get("asset_count"),
        "ingested_at": datetime.now(UTC).isoformat(),
        "notes": overrides.get("notes"),
    }

    Path(output_path).write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return metadata


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
