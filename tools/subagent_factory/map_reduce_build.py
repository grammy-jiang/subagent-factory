"""Slug-agnostic map->reduce assembly of a package's distilled layer (P3 polish, verify-gated).

Ties the generic cores (`chunk_source`, `emit_chunk_anchors`, `reduce_principles`) into one tool that,
given a package slug + its per-book MAP modules (each `cache/book-extracts/<sha>/` with claims.jsonl +
principles.yaml, produced by `map_book.sh`), writes the REDUCE'd distilled layer into
`subagents/<slug>/`:
  - `analysis/claims.jsonl`        — all per-book claims, GLOBALLY renumbered (C#####);
  - `principles/principles.yaml`   — recall->filter->selected, derived_from_claims rewritten to globals;
  - `evidence/evidence-records.yaml` — one record per claim backing a kept principle;
  - `sources/anchors/<sid>.anchors.jsonl` — chunk (paragraph) anchors.
No baseline copy: a real author-subagent run already has `sources/` + manifest from Step-5 ingest, and
Step 7+ (profile/faithfulness/skills/tests/adapter) run unchanged afterwards.

The LLM precision filter is external: `emit_clusters()` writes candidate clusters for it; `assemble()`
consumes the returned per-group decisions (confirm/split/conflict). Embedder is injected (default
`embed_minilm`).
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Sequence
from pathlib import Path

import yaml

from tools.subagent_factory.emit_chunk_anchors import emit_anchors
from tools.subagent_factory.reduce_principles import (
    apply_decisions,
    recall_clusters,
    select_top,
)

Embedder = Callable[[list[str]], list[list[float]]]

# principles-v1 is additionalProperties:false — strip the merge working-fields (source_ids / n_sources)
# before writing principles.yaml; multi-source provenance stays recoverable via derived_from_claims.
_ALLOWED_PRINCIPLE_FIELDS = frozenset(
    {
        "statement",
        "derived_from_claims",
        "confidence",
        "applies_when",
        "does_not_apply_when",
        "operational_mapping",
        "grade",
    }
)


def load_modules(source_paths: Sequence[str | Path], cache_root: Path) -> list[dict]:
    """Resolve each source md -> its content-addressed MAP module; dedup by sha; require completeness."""
    import hashlib

    out: list[dict] = []
    seen: set[str] = set()
    for sp in source_paths:
        sha = hashlib.sha256(Path(sp).read_bytes()).hexdigest()
        if sha in seen:
            continue
        seen.add(sha)
        d = cache_root / sha
        if not (d / "principles.yaml").exists() or not (d / "module.json").exists():
            raise FileNotFoundError(f"MAP module incomplete for {sp} ({d}) — run map_book first")
        out.append(
            {
                "dir": d,
                "source_id": json.loads((d / "module.json").read_text())["source_id"],
                "claims": [
                    json.loads(x)
                    for x in (d / "claims.jsonl").read_text().splitlines()
                    if x.strip()
                ],
                "principles": (yaml.safe_load((d / "principles.yaml").read_text()) or {}).get(
                    "principles"
                )
                or [],
            }
        )
    return out


def build_claim_map(modules: list[dict]) -> tuple[dict[tuple[str, str], str], list[dict]]:
    """(source_id, per-book claim_id) -> global C##### ; all claims renumbered globally."""
    cmap: dict[tuple[str, str], str] = {}
    claims: list[dict] = []
    for m in modules:
        for c in m["claims"]:
            gid = f"C{len(claims) + 1:05d}"
            cmap[(m["source_id"], c["claim_id"])] = gid
            claims.append({**c, "claim_id": gid})
    return cmap, claims


def globalize_principles(modules: list[dict], cmap: dict[tuple[str, str], str]) -> list[dict]:
    """Each book's principles, tagged with source_id, derived_from_claims rewritten to global ids."""
    out: list[dict] = []
    for m in modules:
        for p in m["principles"]:
            out.append(
                {
                    **p,
                    "source_id": m["source_id"],
                    "derived_from_claims": [
                        cmap[(m["source_id"], c)]
                        for c in (p.get("derived_from_claims") or [])
                        if (m["source_id"], c) in cmap
                    ],
                }
            )
    return out


def emit_clusters(principles: list[dict], embedder: Embedder, cos: float = 0.55) -> list[dict]:
    """Candidate multi-member clusters (with their group index) for the LLM precision filter."""
    groups = recall_clusters(principles, embedder, cos)
    return [
        {
            "group": gi,
            "members": [{"idx": i, "statement": principles[i].get("statement", "")} for i in idxs],
        }
        for gi, idxs in enumerate(groups)
        if len(idxs) > 1
    ]


def evidence_records(principles: list[dict], claims_by_id: dict[str, dict]) -> list[dict]:
    wanted = sorted({c for p in principles for c in (p.get("derived_from_claims") or [])})
    recs = []
    for i, cid in enumerate(wanted, 1):
        c = claims_by_id.get(cid)
        if not c:
            continue
        recs.append(
            {
                "evidence_id": f"E{i:05d}",
                "claim_id": cid,
                "source_ids": [c["source_id"]],
                "source_anchors": c.get("source_anchors") or [],
                "support_granularity": c.get("support_granularity") or "paragraph",
                "evidence_type": c.get("evidence_type") or "expert",
                "evidence_strength": "moderate",
                "support_level": "entailed",
                "confidence": c.get("confidence_initial") or "medium",
                "quote_allowed": False,
                "limitations": "Distilled paraphrase; bound to a chunk-level (paragraph) anchor.",
            }
        )
    return recs


def assemble(
    slug: str,
    source_paths: Sequence[str | Path],
    *,
    repo: Path,
    embedder: Embedder,
    cos: float = 0.55,
    decisions: dict[int, dict] | None = None,
    select: int = 0,
) -> dict:
    """Write the REDUCE'd distilled layer into subagents/<slug>/. Returns a counts summary."""
    cache_root = repo / "cache" / "book-extracts"
    pkg = repo / "subagents" / slug
    modules = load_modules(source_paths, cache_root)
    cmap, claims = build_claim_map(modules)
    claims_by_id = {c["claim_id"]: c for c in claims}
    gp = globalize_principles(modules, cmap)
    groups = recall_clusters(gp, embedder, cos)
    merged = select_top(apply_decisions(gp, groups, decisions), select)
    merged = [
        {
            "principle_id": f"P{i:03d}",
            **{k: v for k, v in p.items() if k in _ALLOWED_PRINCIPLE_FIELDS},
        }
        for i, p in enumerate(merged, 1)
    ]
    evidence = evidence_records(merged, claims_by_id)

    (pkg / "analysis").mkdir(parents=True, exist_ok=True)
    (pkg / "principles").mkdir(parents=True, exist_ok=True)
    (pkg / "evidence").mkdir(parents=True, exist_ok=True)
    (pkg / "sources" / "anchors").mkdir(parents=True, exist_ok=True)
    with open(pkg / "analysis" / "claims.jsonl", "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    (pkg / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "principles-v1", "principles": merged},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    (pkg / "evidence" / "evidence-records.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "evidence-records-v1", "evidence_records": evidence},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    for m in modules:
        if (m["dir"] / "anchors.jsonl").exists() or emit_anchors(m["dir"]):
            (pkg / "sources" / "anchors" / f"{m['source_id']}.anchors.jsonl").write_text(
                (m["dir"] / "anchors.jsonl").read_text(encoding="utf-8"), encoding="utf-8"
            )
    return {
        "books": len(modules),
        "claims": len(claims),
        "principles": len(merged),
        "evidence": len(evidence),
    }


def _embed_minilm(statements: list[str]) -> list[list[float]]:
    from tools.subagent_factory.seed_principle_clusters import embed_minilm

    return embed_minilm(statements)


def main() -> int:
    ap = argparse.ArgumentParser(description="Slug-agnostic map->reduce distilled-layer assembly.")
    ap.add_argument("slug")
    ap.add_argument(
        "--sources", required=True, help="newline file of source md paths, or a dir of *.md"
    )
    ap.add_argument(
        "--decisions", type=Path, help="precision-filter decisions.json (group-index keyed)"
    )
    ap.add_argument("--select", type=int, default=0)
    ap.add_argument("--cos", type=float, default=0.55)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args()
    sp = (
        sorted(str(x) for x in Path(args.sources).glob("*.md"))
        if Path(args.sources).is_dir()
        else [
            ln.strip()
            for ln in Path(args.sources).read_text().splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
    )
    dec = (
        {int(k): v for k, v in json.loads(args.decisions.read_text()).items()}
        if args.decisions
        else None
    )
    summary = assemble(
        args.slug,
        sp,
        repo=args.repo,
        embedder=_embed_minilm,
        cos=args.cos,
        decisions=dec,
        select=args.select,
    )
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
