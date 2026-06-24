"""Shared read-only queries over a generated package's on-disk artifacts.

Single source of truth for the small "collect the ids declared in <file>" helpers that the
referential validators each used to re-implement verbatim. Pure reads: every function returns an
empty set for a missing or garbled file, so callers can run referential checks without first
guarding for existence. Imports nothing from the rest of the package (safe from any module).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


def anchor_ids(base: Path) -> set[str]:
    """Anchor ids declared in ``<base>/sources/anchors/*.anchors.jsonl``."""
    ids: set[str] = set()
    anchors_dir = base / "sources" / "anchors"
    if not anchors_dir.exists():
        return ids
    for af in anchors_dir.glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(json.loads(line)["anchor_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def claim_ids(base: Path) -> set[str]:
    """Claim ids declared in ``<base>/analysis/claims.jsonl``."""
    cp = base / "analysis" / "claims.jsonl"
    if not cp.exists():
        return set()
    ids: set[str] = set()
    for line in cp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ids.add(json.loads(line)["claim_id"])
        except (json.JSONDecodeError, KeyError):
            continue
    return ids


def manifest_source_ids(base: Path) -> set[str]:
    """Source ids declared in ``<base>/source-pack.manifest.yaml``."""
    mp = base / "source-pack.manifest.yaml"
    if not mp.exists():
        return set()
    try:
        manifest = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return {str(s.get("source_id")) for s in (manifest.get("sources") or []) if s.get("source_id")}


def principle_ids(principles_dir: Path) -> set[str]:
    """Principle ids declared in ``<principles_dir>/principles.yaml``."""
    pp = principles_dir / "principles.yaml"
    if not pp.exists():
        return set()
    data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    return {
        str(p.get("principle_id")) for p in (data.get("principles") or []) if p.get("principle_id")
    }
