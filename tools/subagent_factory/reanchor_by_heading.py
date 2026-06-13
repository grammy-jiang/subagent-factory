"""Re-anchor concept-slug claim anchors to recovered heading anchors (deterministic).

When a package's claim ``source_anchors`` are conceptual *section slugs* (``ch1-tactical-empathy``,
``ch2-mirroring``) — the author's slugified label for a source section — and the source is
**re-converted with Docling** so its headings come back, the slug can be mapped to the heading it
names. That is faithful *recovery*, not fabrication: the slug already encodes which section it meant,
and we resolve it to that section's now-real heading anchor.

Matching is deterministic: strip the ``chN-`` / ``appendix-`` prefix, then pick the heading (in the
claim's own source) with the most shared concept tokens, **requiring ≥1 shared token** so a slug with
no matching heading (a sub-point that never had one) resolves to nothing rather than to a junk
heading. Such slugs are left for a separate fallback (surgical LLM / empty), never guessed here.

Evidence inherits its claim's anchors 1:1 by ``claim_id``. Deterministic, no LLM. Prerequisite: the
source has heading anchors (i.e. it was converted by a heading-aware converter such as Docling).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

_PREFIX_RE = re.compile(r"^(ch\d+|chapter\d+|appendix|app|sec\d+|section\d+)-")


def _slugify(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def _concept_tokens(slug: str) -> set[str]:
    return {t for t in _PREFIX_RE.sub("", slug.lower()).split("-") if len(t) > 2}


def _heading_anchors(base: Path) -> dict[str, list[tuple[set[str], str]]]:
    """``{source_id: [(heading_slug_tokens, anchor_id), ...]}`` for heading-type anchors only."""
    out: dict[str, list[tuple[set[str], str]]] = {}
    adir = base / "sources" / "anchors"
    if not adir.exists():
        return out
    for af in adir.glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("anchor_type") == "heading" and r.get("source_id") and r.get("anchor_id"):
                toks = {t for t in _slugify(r.get("text", "")).split("-") if len(t) > 2}
                out.setdefault(str(r["source_id"]), []).append((toks, str(r["anchor_id"])))
    return out


def match_slug_to_heading(slug: str, headings: list[tuple[set[str], str]]) -> str | None:
    """Best heading anchor for a concept slug (≥1 shared token), else None."""
    ct = _concept_tokens(slug)
    if not ct or not headings:
        return None
    best_score, best_id = 0, None
    for htoks, aid in headings:
        score = len(ct & htoks)
        if score > best_score:
            best_score, best_id = score, aid
    return best_id if best_score >= 1 else None


def reanchor_by_heading(subagent_dir: str | Path, *, write: bool = True) -> dict:
    """Resolve concept-slug claim anchors to heading anchors; propagate to evidence. Summary out."""
    base = Path(subagent_dir)
    headings = _heading_anchors(base)
    all_anchor_ids = _all_anchor_ids(base)

    claims_path = base / "analysis" / "claims.jsonl"
    claims = [
        json.loads(line)
        for line in claims_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    chosen_by_claim: dict[str, list[str]] = {}
    n_resolved = n_unresolved = 0
    for c in claims:
        sid = c.get("source_id", "")
        current = c.get("source_anchors") or []
        if current and all(a in all_anchor_ids for a in current):
            continue  # already resolves
        new: list[str] = []
        for a in current:
            if a in all_anchor_ids:
                new.append(a)
                continue
            m = match_slug_to_heading(str(a), headings.get(sid, []))
            if m:
                new.append(m)
                n_resolved += 1
            else:
                n_unresolved += 1
        c["source_anchors"] = list(dict.fromkeys(new))
        chosen_by_claim[c["claim_id"]] = c["source_anchors"]

    if write and chosen_by_claim:
        claims_path.write_text(
            "\n".join(json.dumps(c, ensure_ascii=False) for c in claims) + "\n", encoding="utf-8"
        )
        ev_path = base / "evidence" / "evidence-records.yaml"
        if ev_path.exists():
            ev = yaml.safe_load(ev_path.read_text(encoding="utf-8")) or {}
            for r in ev.get("evidence_records", []) or []:
                cid = r.get("claim_id")
                if cid in chosen_by_claim:
                    r["source_anchors"] = chosen_by_claim[cid]
            ev_path.write_text(
                yaml.safe_dump(ev, sort_keys=False, allow_unicode=True), encoding="utf-8"
            )
    n_claims_empty = sum(1 for v in chosen_by_claim.values() if not v)
    return {
        "n_resolved": n_resolved,
        "n_unresolved": n_unresolved,
        "n_claims_touched": len(chosen_by_claim),
        "n_claims_left_empty": n_claims_empty,
    }


def _all_anchor_ids(base: Path) -> set[str]:
    ids: set[str] = set()
    adir = base / "sources" / "anchors"
    if not adir.exists():
        return ids
    for af in adir.glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                ids.add(json.loads(line)["anchor_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.reanchor_by_heading subagents/<slug>")
        sys.exit(1)
    rep = reanchor_by_heading(sys.argv[1])
    print(
        f"heading re-anchor: {rep['n_resolved']} slug(s) resolved, {rep['n_unresolved']} unresolved; "
        f"{rep['n_claims_left_empty']}/{rep['n_claims_touched']} claims left empty"
    )


if __name__ == "__main__":
    main()
