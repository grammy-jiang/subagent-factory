"""Remap stale faithfulness ``source_anchors`` to real anchor ids (deterministic repair).

A package authored under an older anchor convention can carry faithfulness ``source_anchors`` that
are not real anchor ids — line references (``<source_id>:L148``, ``kafka-best-practices L753-757``),
or conceptual section slugs (``ch6-never-split``, ``the-struggle``). These fail
``validate_faithfulness_report`` (shape ``-[a-z]\\d{3,}$``). This tool repairs them **without
fabricating provenance**:

1. **Regenerate** the anchor index from the surviving source markdown if it is empty/missing
   (``inject_anchors``), giving real ``anchor_id`` + ``line_number`` per source.
2. **Line-remap** any entry that carries a line number resolvable to a single source: route by the
   entry's source hint (``<sid>:L`` prefix, or a leading source-name token; a single-source package
   needs no hint), then map the line to the anchor whose span starts at or before it.
3. **Quarantine the rest** (slugs, or bare ``L<n>`` ambiguous across multiple sources) to
   ``reports/faithfulness-repair.yaml`` — fuzzy slug→heading matching would *invent* an evidence
   link, the exact thing the faithfulness step exists to prevent, so the honest action is to drop +
   record, not guess.

Deterministic, no LLM. The complement to ``repair_faithfulness_report`` (which only strips): this
*recovers* line-anchored provenance first, then strips what genuinely cannot be resolved.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

from tools.subagent_factory.inject_anchors import inject_anchors

_LINE_RE = re.compile(r"L(\d+)")
_LEAD_TOKEN_RE = re.compile(r"^([a-z0-9][a-z0-9-]{2,})")


def _source_ids(base: Path) -> list[str]:
    md_dir = base / "sources" / "markdown"
    return [p.stem for p in sorted(md_dir.glob("*.md"))] if md_dir.exists() else []


def _ensure_anchors(base: Path, sid: str) -> Path:
    """Anchor-index path for ``sid``; regenerate from markdown if empty/missing."""
    aj = base / "sources" / "anchors" / f"{sid}.anchors.jsonl"
    if aj.exists() and aj.stat().st_size > 1:
        return aj
    md = base / "sources" / "markdown" / f"{sid}.md"
    if md.exists():
        aj.parent.mkdir(parents=True, exist_ok=True)
        inject_anchors(md, md, aj, sid)
    return aj


def _load_lines(aj: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    if not aj.exists():
        return out
    for line in aj.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "anchor_id" in r and "line_number" in r:
            out.append((int(r["line_number"]), str(r["anchor_id"])))
    out.sort()
    return out


def _route_source(entry: str, source_ids: list[str]) -> str | None:
    """Pick the source an entry refers to: ``<sid>:L`` prefix, leading name token, or sole source."""
    entry = entry.strip()
    if ":L" in entry:
        pref = entry.split(":L", 1)[0].strip()
        for sid in source_ids:
            if sid.startswith(pref) or pref.startswith(sid):
                return sid
    lead = _LEAD_TOKEN_RE.match(entry)
    if lead:
        tok = lead.group(1)
        for sid in source_ids:
            # name hint (``kafka-best-practices`` ⊂ sid) OR a full anchor id (sid ⊂ ``…-t0056``)
            if sid.startswith(tok) or tok.startswith(sid):
                return sid
    return source_ids[0] if len(source_ids) == 1 else None


def _finding_source(original: list, source_ids: list[str]) -> str | None:
    """The single source a finding's *hinted* anchors agree on (else None — mixed/none).

    A faithfulness finding usually cites one source. When some of its anchors carry an explicit
    source hint and they all point to the same source, a bare ``L<n>`` sibling in that finding can be
    routed there too — recovering provenance that is otherwise ambiguous in a multi-source package.
    """
    if len(source_ids) == 1:
        return source_ids[0]
    hinted = set()
    for a in original:
        a = str(a)
        if ":L" in a or _LEAD_TOKEN_RE.match(a.strip()):
            sid = _route_source(a, source_ids)
            if sid:
                hinted.add(sid)
    return next(iter(hinted)) if len(hinted) == 1 else None


def _remap_one(
    entry: str,
    maps: dict[str, list[tuple[int, str]]],
    source_ids: list[str],
    default_sid: str | None = None,
) -> str | None:
    """Return a real anchor_id for an entry carrying a resolvable line number, else None."""
    m = _LINE_RE.search(entry)
    if not m:
        return None  # no line number -> not line-anchored (slug); cannot remap honestly
    sid = _route_source(entry, source_ids) or default_sid
    if not sid or not maps.get(sid):
        return None  # ambiguous source (bare line, no finding-level source agreement)
    n = int(m.group(1))
    byline = maps[sid]
    covering = [a for ln, a in byline if ln <= n]
    return covering[-1] if covering else byline[0][1]


def remap_faithfulness_anchors(report_path: str | Path, *, write: bool = True) -> dict:
    """Remap line-anchored entries to real ids; quarantine the unresolvable. Returns a summary."""
    path = Path(report_path)
    base = path.parents[1]  # <base>/reports/faithfulness-report.yaml
    source_ids = _source_ids(base)
    maps = {sid: _load_lines(_ensure_anchors(base, sid)) for sid in source_ids}
    valid_ids = {a for bl in maps.values() for _, a in bl}

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    n_remapped = 0
    quarantined: list[dict] = []
    for i, finding in enumerate(data.get("findings", []) or []):
        original = finding.get("source_anchors", []) or []
        default_sid = _finding_source(original, source_ids)
        new: list[str] = []
        for a in original:
            a = str(a)
            if a in valid_ids:  # already a real anchor id — keep
                new.append(a)
                continue
            mapped = _remap_one(a, maps, source_ids, default_sid)
            if mapped:
                new.append(mapped)
                n_remapped += 1
            else:
                quarantined.append(
                    {"finding": i, "rule_ref": finding.get("rule_ref", ""), "dropped": a}
                )
        finding["source_anchors"] = list(dict.fromkeys(new))  # dedupe, preserve order

    changed = n_remapped > 0 or bool(quarantined)
    if write and changed:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        if quarantined:
            (base / "reports" / "faithfulness-repair.yaml").write_text(
                yaml.safe_dump({"quarantined": quarantined}, sort_keys=False), encoding="utf-8"
            )
    return {
        "n_remapped": n_remapped,
        "n_quarantined": len(quarantined),
        "quarantined": quarantined,
        "changed": changed,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.remap_faithfulness_anchors <report.yaml>")
        sys.exit(1)
    rep = remap_faithfulness_anchors(sys.argv[1])
    print(
        f"remap: {rep['n_remapped']} anchor(s) recovered to real ids, "
        f"{rep['n_quarantined']} quarantined (no resolvable line)"
    )
    for q in rep["quarantined"][:15]:
        print(f"  finding[{q['finding']}] {q['rule_ref']}: {q['dropped'][:60]}")


if __name__ == "__main__":
    main()
