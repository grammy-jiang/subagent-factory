"""Re-ground a skill's ``provenance.source_anchors`` to real anchor ids by content overlap.

A Tier-0 package (no claims/principles distillation layer) can ship skills whose provenance lists
the **whole source id** (``kafka-best-practices-20260608223304``) instead of real anchor ids, which
fails ``validate_skill_authoring`` ("does not resolve to a real ID"). There is no claim→anchor chain
to rebuild from, but a skill is a *broad procedure*, and "which spans of the source does this skill
draw on" is answerable deterministically by **content overlap** — token overlap of the skill body
against each anchor's text. That is appropriate for *skill-level* provenance (it is not the
atomic-claim support judgement that needs an LLM): it cites the spans the skill actually covers.

For each skill, every bare/invalid ``source_anchors`` entry is replaced by the top-``k`` anchors of
the source it names (matched by id prefix), ranked by overlap and requiring a real shared-token
signal (``min_overlap``) so an irrelevant span is never cited. Entries that are already real anchor
ids are kept; bare ids whose source has no overlapping span are dropped (not guessed).

Deterministic, no LLM. Complements ``remap_faithfulness_anchors`` (faithfulness report) — this is the
skill-provenance counterpart for Tier-0 packages.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _content_tokens

_ANCHOR_ID_RE = re.compile(r"-[a-z]\d{3,}$")


def _source_anchor_text(base: Path) -> dict[str, list[tuple[str, set[str]]]]:
    """``{source_id: [(anchor_id, text_tokens), ...]}`` from the anchor index."""
    out: dict[str, list[tuple[str, set[str]]]] = {}
    adir = base / "sources" / "anchors"
    if not adir.exists():
        return out
    for af in adir.glob("*.anchors.jsonl"):
        for line in af.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid, aid = r.get("source_id"), r.get("anchor_id")
            if sid and aid:
                out.setdefault(str(sid), []).append((str(aid), _content_tokens(r.get("text", ""))))
    return out


def _split_frontmatter(text: str) -> tuple[dict, str, str] | None:
    """Return (frontmatter_dict, raw_frontmatter, body) for a ``---``-delimited markdown, else None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    raw = text[text.find("\n", 3) + 1 : end]
    body = text[end + 4 :]
    try:
        fm = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return None
    return (fm if isinstance(fm, dict) else {}), raw, body


def _best_anchors(body_tokens: set[str], anchors: list[tuple[str, set[str]]], k: int, min_overlap: int) -> list[str]:
    scored = sorted(
        ((len(body_tokens & at), aid) for aid, at in anchors), key=lambda x: x[0], reverse=True
    )
    return [aid for n, aid in scored[:k] if n >= min_overlap]


def reground_skill_anchors(
    subagent_dir: str | Path, *, top_k: int = 3, min_overlap: int = 2, write: bool = True
) -> dict:
    """Replace bare-source-id skill anchors with content-matched real anchor ids. Returns a summary."""
    base = Path(subagent_dir)
    src_anchors = _source_anchor_text(base)
    valid_ids = {aid for lst in src_anchors.values() for aid, _ in lst}
    source_ids = list(src_anchors)

    # Both authored-doc kinds carry the same provenance block and the same bare-source-id failure.
    docs = sorted((base / "skills").glob("*/SKILL.md")) + sorted((base / "references").glob("*.md"))
    results: list[dict] = []
    for sk in docs:
        text = sk.read_text(encoding="utf-8")
        parsed = _split_frontmatter(text)
        if not parsed:
            continue
        fm, raw, body = parsed
        prov = fm.get("provenance") or {}
        original = prov.get("source_anchors") or []
        if not isinstance(original, list):
            continue
        body_tokens = _content_tokens(body)
        new: list[str] = []
        n_regrounded = 0
        for ref in original:
            ref = str(ref)
            if ref in valid_ids:  # already a real anchor id
                new.append(ref)
                continue
            sid = next((s for s in source_ids if ref == s or s.startswith(ref) or ref.startswith(s)), None)
            if sid:
                matched = _best_anchors(body_tokens, src_anchors[sid], top_k, min_overlap)
                new.extend(matched)
                n_regrounded += len(matched)
            # else: unresolvable -> dropped (not guessed)
        new = list(dict.fromkeys(new))
        if new != original:
            prov["source_anchors"] = new
            fm["provenance"] = prov
            if write:
                new_fm = yaml.safe_dump(fm, sort_keys=False).rstrip("\n")
                sk.write_text(f"---\n{new_fm}\n---{body}", encoding="utf-8")
            label = sk.parent.name if sk.name == "SKILL.md" else sk.stem
            results.append({"doc": label, "before": original, "after": new})
    return {"n_skills_changed": len(results), "results": results}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.reground_skill_anchors subagents/<slug>")
        sys.exit(1)
    rep = reground_skill_anchors(sys.argv[1])
    print(f"re-grounded {rep['n_skills_changed']} authored doc(s)")
    for r in rep["results"]:
        print(f"  {r['doc']}: {len(r['before'])} -> {len(r['after'])} anchors")


if __name__ == "__main__":
    main()
