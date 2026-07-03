"""Repo-wide materials catalog + inbound duplication check.

Every source book/paper processed in this repo, keyed by ``sha256`` (the same content-address the
MAP cache and each package manifest already use). The catalog is DERIVED (DRY) from:
  - ``subagents/*/source-pack.manifest.yaml`` + ``sources/metadata/*.json``  (sources built into a package)
  - ``cache/book-extracts/*/module.json``                                     (books MAPped, maybe not yet built)

so it never drifts from the real provenance — regenerate any time.

CLI:
  python -m tools.subagent_factory.materials_catalog build
      -> regenerate catalog/materials.yaml + docs/materials-catalog.md
  python -m tools.subagent_factory.materials_catalog check <md-path | sha256 | title>
      -> report exact (sha) duplication + closest same-book/topic matches for inbound material

**Habit:** run ``check`` on every new book BEFORE converting/MAPping it (see CLAUDE.md).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SUBAGENTS = REPO / "subagents"
CACHE = REPO / "cache" / "book-extracts"
CAT_YAML = REPO / "catalog" / "materials.yaml"
CAT_MD = REPO / "docs" / "materials-catalog.md"


def _sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _norm(s: str | None) -> set[str]:
    """Title -> token set for same-book / topic overlap scoring."""
    if not s:
        return set()
    for ch in "-_./()[]":
        s = s.replace(ch, " ")
    return {t for t in s.lower().split() if len(t) > 2}


def collect() -> dict[str, dict]:
    """sha256 -> catalog entry, merged across package manifests and the MAP cache."""
    by_sha: dict[str, dict] = {}
    # 1) sources built into packages
    for man in sorted(SUBAGENTS.glob("*/source-pack.manifest.yaml")):
        pkg = man.parent
        try:
            m = yaml.safe_load(man.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        slug = m.get("subagent_slug", pkg.name)
        for s in m.get("sources", []) or []:
            sha = s.get("sha256")
            if not sha:
                continue
            md = _load_json(pkg / "sources" / "metadata" / f"{s.get('source_id', '')}.metadata.json")
            e = by_sha.setdefault(
                sha,
                {
                    "sha256": sha,
                    "title": md.get("title") or s.get("original_filename"),
                    "author": md.get("author"),
                    "year": md.get("year"),
                    "source_type": md.get("source_type"),
                    "word_count": md.get("word_count"),
                    "rights_status": md.get("rights_status"),
                    "feeds": [],
                    "map_principles": None,
                    "status": "built",
                },
            )
            if slug not in e["feeds"]:
                e["feeds"].append(slug)
    # 2) MAPped books (may not yet be built into any package)
    for mj in sorted(CACHE.glob("*/module.json")):
        d = _load_json(mj)
        sha = d.get("sha") or mj.parent.name
        e = by_sha.get(sha)
        if e is None:
            by_sha[sha] = {
                "sha256": sha,
                "title": d.get("title"),
                "author": None,
                "year": None,
                "source_type": "book",
                "word_count": None,
                "rights_status": None,
                "feeds": [],
                "map_principles": d.get("n_principles"),
                "status": "mapped-not-built",
            }
        else:
            e["map_principles"] = d.get("n_principles")
    return by_sha


def build() -> int:
    by_sha = collect()
    entries = sorted(by_sha.values(), key=lambda e: (not e["feeds"], (e["title"] or "").lower()))
    CAT_YAML.parent.mkdir(parents=True, exist_ok=True)
    CAT_YAML.write_text(
        yaml.safe_dump(
            {"schema_version": "materials-catalog-v1", "count": len(entries), "materials": entries},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Materials Catalog",
        "",
        f"Every source processed in this repo — **{len(entries)} items**, keyed by `sha256`.",
        "",
        "> **Generated file.** Refresh: `python -m tools.subagent_factory.materials_catalog build`",
        ">",
        "> **On a new book, FIRST check for duplication:**",
        "> `python -m tools.subagent_factory.materials_catalog check <md-path | sha256 | title>`",
        "",
        "| sha8 | title | type | words | rights | princ | feeds / status |",
        "|------|-------|------|-------|--------|-------|----------------|",
    ]
    for e in entries:
        feeds = ", ".join(e["feeds"]) if e["feeds"] else f"_{e['status']}_"
        lines.append(
            f"| `{e['sha256'][:8]}` | {e['title'] or '?'} | {e.get('source_type') or '?'} "
            f"| {e.get('word_count') or '-'} | {e.get('rights_status') or '-'} "
            f"| {e.get('map_principles') or '-'} | {feeds} |"
        )
    CAT_MD.parent.mkdir(parents=True, exist_ok=True)
    CAT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"catalog: {len(entries)} materials -> {CAT_YAML.relative_to(REPO)} + {CAT_MD.relative_to(REPO)}")
    return 0


def check(target: str) -> int:
    by_sha = collect()
    p = Path(target)
    sha: str | None = None
    title = target
    if p.exists():
        sha = _sha256_file(p)
        title = p.stem
    elif 8 <= len(target) <= 64 and all(c in "0123456789abcdef" for c in target.lower()):
        sha = target.lower()
    print(f"[check] target={target}  sha={(sha or '?')[:16]}")
    # exact content duplication
    if sha:
        for full, e in by_sha.items():
            if full == sha or full.startswith(sha) or (len(sha) == 64 and sha.startswith(full)):
                print(f"  ⛔ EXACT DUP (sha256) — already processed: '{e['title']}'  feeds={e['feeds'] or e['status']}")
                return 0
    # same-book / topic overlap by title tokens
    tt = _norm(title)
    scored = []
    for e in by_sha.values():
        et = _norm(e["title"])
        if tt and et:
            j = len(tt & et) / len(tt | et)
            if j > 0:
                scored.append((j, e))
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] >= 0.5:
        print("  ⚠ LIKELY SAME BOOK (high title overlap):")
    elif scored:
        print("  no exact dup. Closest existing materials (title tokens — judge topic overlap):")
    else:
        print("  ✅ no sha or title match — NEW material, no duplication")
        return 0
    for j, e in scored[:5]:
        print(f"    {j:.0%}  '{e['title']}'  feeds={e['feeds'] or e['status']}")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["build"]:
        return build()
    if argv[:1] == ["check"] and len(argv) >= 2:
        return check(argv[1])
    print("usage: materials_catalog build | check <md-path | sha256 | title>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
