"""Generate or update source-pack manifest YAML."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from tools.subagent_factory._common import atomic_write_text


def generate_manifest(
    subagent_dir: str | Path,
    subagent_slug: str,
    sources: list[dict],
) -> dict:
    """
    Write source-pack.manifest.yaml under subagent_dir.

    sources: list of dicts with keys matching manifest schema.
    Returns manifest dict.
    """
    subagent_path = Path(subagent_dir)
    manifest_path = subagent_path / "source-pack.manifest.yaml"

    now = datetime.now(UTC).isoformat()

    existing: dict[str, Any] = {}
    if manifest_path.exists():
        with open(manifest_path, encoding="utf-8") as f:
            existing = yaml.safe_load(f) or {}

    existing_sources = {s["source_id"]: s for s in existing.get("sources", [])}
    for source in sources:
        existing_sources[source["source_id"]] = source

    manifest = {
        "schema_version": "source-pack-manifest-v1",
        "subagent_slug": subagent_slug,
        "created_at": existing.get("created_at", now),
        "updated_at": now,
        "sources": list(existing_sources.values()),
    }

    # Atomic: the manifest is a REQUIRED_FILES entry aggregating every prior source — a torn write
    # would corrupt it and break all future ingests. temp file + os.replace makes the swap atomic.
    atomic_write_text(manifest_path, yaml.dump(manifest, allow_unicode=True, sort_keys=False))
    return manifest
