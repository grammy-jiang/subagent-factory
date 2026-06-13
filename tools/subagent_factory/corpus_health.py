"""One-shot structural health audit of every generated package (read-only, no LLM, fast).

Institutionalises the ad-hoc audits used during the Docling corpus migration: per package it
reports the source converter, anchor count + dominant type (and whether the index is empty or
PDF-noise), tier/status, claim count + dangling-anchor refs, and a derived health flag. Pure
filesystem read — does NOT run the full validator (use ``cli validate`` for that).
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

from tools.subagent_factory.inject_anchors import _is_pdf_noise


def _load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _anchor_stats(base: Path) -> dict:
    ids: set[str] = set()
    types: Counter = Counter()
    noise = 0
    for af in (base / "sources" / "anchors").glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            ids.add(r.get("anchor_id"))
            t = r.get("anchor_type", "?")
            types[t] += 1
            if t == "paragraph" and _is_pdf_noise(r.get("text", "")):
                noise += 1
    total = sum(types.values())
    dominant = types.most_common(1)[0][0] if types else "-"
    para = types.get("paragraph", 0)
    return {
        "total": total,
        "dominant": dominant,
        "types": dict(types),
        "ids": ids,
        "noise_ratio": round(noise / para, 2) if para else 0.0,
    }


def _claim_stats(base: Path, anchor_ids: set[str]) -> dict:
    cp = base / "analysis" / "claims.jsonl"
    if not cp.exists():
        return {"count": 0, "dead_refs": 0}
    count = dead = 0
    for line in cp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        count += 1
        for a in rec.get("source_anchors", []) or []:
            if anchor_ids and a not in anchor_ids:
                dead += 1
    return {"count": count, "dead_refs": dead}


def _converters(base: Path) -> str:
    used: set[str] = set()
    for mf in (base / "sources" / "metadata").glob("*.metadata.json"):
        try:
            used.add(json.loads(mf.read_text(encoding="utf-8")).get("converter_used") or "?")
        except (OSError, json.JSONDecodeError):
            continue
    return ",".join(sorted(used)) if used else "-"


def _health_flags(anchors: dict, claims: dict) -> list[str]:
    flags: list[str] = []
    if anchors["total"] == 0:
        flags.append("empty-anchors")
    elif anchors["dominant"] == "paragraph" and anchors["noise_ratio"] > 0.5:
        flags.append("junk-anchors")
    elif anchors["total"] and "heading" not in anchors["types"]:
        flags.append("no-headings")
    if claims["dead_refs"] > 0:
        flags.append("dead-refs")
    return flags or ["ok"]


def scan_package(pkg: Path) -> dict:
    profile = _load_yaml(pkg / "profile.yaml")
    anchors = _anchor_stats(pkg)
    claims = _claim_stats(pkg, anchors["ids"])
    return {
        "slug": pkg.name,
        "tier": profile.get("tier", "-"),
        "status": profile.get("status", "-"),
        "version": profile.get("agent_version", "-"),
        "converter": _converters(pkg),
        "anchors": anchors["total"],
        "anchor_type": anchors["dominant"],
        "noise_ratio": anchors["noise_ratio"],
        "claims": claims["count"],
        "dead_refs": claims["dead_refs"],
        "health": _health_flags(anchors, claims),
    }


def scan_corpus(root: str | Path) -> list[dict]:
    root = Path(root)
    if not root.exists():
        return []
    return [
        scan_package(p)
        for p in sorted(root.iterdir())
        if p.is_dir() and (p / "profile.yaml").exists()
    ]
