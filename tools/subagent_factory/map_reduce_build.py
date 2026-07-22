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
import shutil
from collections.abc import Callable, Sequence
from pathlib import Path

import yaml

from tools.subagent_factory._common import atomic_write_text
from tools.subagent_factory.emit_chunk_anchors import emit_anchors
from tools.subagent_factory.generate_conversion_report import generate_conversion_report
from tools.subagent_factory.generate_manifest import generate_manifest
from tools.subagent_factory.generate_metadata import generate_metadata
from tools.subagent_factory.reduce_principles import (
    _embed_minilm,
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
                "source_id": json.loads((d / "module.json").read_text(encoding="utf-8"))[
                    "source_id"
                ],
                "claims": [
                    json.loads(x)
                    for x in (d / "claims.jsonl").read_text(encoding="utf-8").splitlines()
                    if x.strip()
                ],
                "principles": (
                    yaml.safe_load((d / "principles.yaml").read_text(encoding="utf-8")) or {}
                ).get("principles")
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


# --- Single-producer group-index contract -------------------------------------------------------
# The emit -> external-LLM-decisions -> assemble pipeline keys the `decisions` dict on a GROUP INDEX
# (the position of a cluster in `recall_clusters`' output). `recall_clusters` is a greedy, order- and
# float-sensitive single-pass clusterer (see reduce_principles.recall_clusters), so two independent
# calls can produce DIFFERENT groupings — which would silently land each decision on the wrong
# cluster. To make the contract sound, `recall_clusters` must be the SINGLE producer of `groups` for
# a given run: compute it once, then feed the SAME `groups` to both `emit_clusters` (which the LLM
# keys its decisions on) and `assemble` (which applies them). `build_groups` is that one producer;
# pass its result through both phases. `assemble` accepts an optional precomputed `groups` so an
# in-process caller can thread the identical object end-to-end; only when it is omitted does
# `assemble` recompute (and it then owns the single-producer call itself).


def build_groups(principles: list[dict], embedder: Embedder, cos: float = 0.55) -> list[list[int]]:
    """The single producer of the group-index contract: cluster `principles` ONCE.

    Both `emit_clusters` (which the external LLM decisions key on) and `assemble` (which applies
    those decisions) must consume the SAME list this returns — never recompute it independently —
    so `decisions[group_index]` always lands on the cluster the LLM actually saw.
    """
    return recall_clusters(principles, embedder, cos)


# --- Cross-process group persistence (single-producer contract, replayed) -----------------------
# `build_groups` produces a positional grouping (lists of indices into the principle list). When the
# emit and apply phases run in SEPARATE processes (the campaign driver), `assemble` cannot reuse the
# in-memory `groups` object — and re-running `build_groups` from scratch risks a reshuffle (greedy,
# float-sensitive clusterer + a re-invoked embedder), silently landing each LLM decision on a
# different cluster. So the emit phase serializes the grouping by a STABLE principle identity
# (positions are meaningless across processes), and the apply phase reloads it and rebuilds the
# positional `groups` against its own principle list — keeping `build_groups` the single producer and
# the persisted file merely its replayed output.


def principle_group_key(principle: dict) -> tuple[str, str, str]:
    """A stable, position-independent identity for a globalized principle.

    Built from fields that survive serialization and a fresh `globalize_principles` pass:
    `source_id`, `statement`, and the (global) `derived_from_claims`. Used to persist a grouping by
    identity rather than list position, so it can be replayed in another process.
    """
    return (
        str(principle.get("source_id", "")),
        str(principle.get("statement", "")),
        ",".join(map(str, principle.get("derived_from_claims") or [])),
    )


def _keyed_index(principles: list[dict]) -> dict[tuple[str, str, str, int], int]:
    """Map (stable key + per-key occurrence) -> position, so duplicate keys map deterministically."""
    out: dict[tuple[str, str, str, int], int] = {}
    seen: dict[tuple[str, str, str], int] = {}
    for i, p in enumerate(principles):
        k = principle_group_key(p)
        occ = seen.get(k, 0)
        seen[k] = occ + 1
        out[(*k, occ)] = i
    return out


def serialize_groups(principles: list[dict], groups: list[list[int]]) -> list[list[list[str]]]:
    """Render `groups` (positional) as lists of stable principle keys for cross-process persistence.

    Each member becomes a 3-tuple key `[source_id, statement, derived_from_claims_csv]`; duplicate
    keys keep their multiplicity by repetition, so `deserialize_groups` can reconstruct the exact
    positional grouping against a freshly globalized principle list.
    """
    return [[list(principle_group_key(principles[i])) for i in idxs] for idxs in groups]


def deserialize_groups(
    principles: list[dict], serialized: list[list[list[str]]]
) -> list[list[int]]:
    """Rebuild the positional `groups` for `principles` from a `serialize_groups` payload.

    Raises ValueError if a persisted member cannot be matched to a current principle (the set
    shrank) OR if the resulting groups do not cover every current principle (the set grew — a
    superset that would otherwise silently drop the new principles downstream) — fail loudly rather
    than silently mis-map or drop.
    """
    index = _keyed_index(principles)
    used: dict[tuple[str, str, str], int] = {}
    groups: list[list[int]] = []
    for grp in serialized:
        idxs: list[int] = []
        for key in grp:
            k = (str(key[0]), str(key[1]), str(key[2]))
            occ = used.get(k, 0)
            used[k] = occ + 1
            lookup = (*k, occ)
            if lookup not in index:
                raise ValueError(
                    f"persisted group member {k!r} (occurrence {occ}) has no match in the current "
                    "principle set — the principles changed since the grouping was persisted; "
                    "regenerate clusters before assembling"
                )
            idxs.append(index[lookup])
        groups.append(idxs)
    # Full-coverage check: every current principle must land in exactly one group. The per-member
    # lookup above only catches a SHRUNK set (a persisted key with no current match). It does NOT
    # catch a GROWN set (current principles are a superset of what was persisted) — every old key
    # still matches, but the newly-added principles appear in no group and would be silently dropped
    # by `apply_decisions` (which iterates groups only). Fail loudly with the same "regenerate
    # clusters" contract instead.
    covered = {i for grp in groups for i in grp}
    if covered != set(range(len(principles))):
        uncovered = len(principles) - len(covered)
        raise ValueError(
            f"persisted grouping covers only {len(covered)} of {len(principles)} current principles "
            f"({uncovered} uncovered) — the principle set grew since the grouping was persisted; "
            "regenerate clusters before assembling"
        )
    return groups


def emit_clusters(
    principles: list[dict],
    embedder: Embedder,
    cos: float = 0.55,
    *,
    groups: list[list[int]] | None = None,
) -> list[dict]:
    """Candidate multi-member clusters (with their group index) for the LLM precision filter.

    Pass `groups` (from `build_groups`) to bind the emitted group indices to the exact same
    grouping `assemble` will apply decisions against; when omitted, `build_groups` is called here
    and the caller is then responsible for reusing it in `assemble` (single-producer invariant).
    """
    if groups is None:
        groups = build_groups(principles, embedder, cos)
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


_SOURCE_SUBDIRS = ("markdown", "metadata", "anchors", "reports")


def _source_id_of(filename: str) -> str:
    """`<source_id>.<ext>` -> `<source_id>` for files under sources/{markdown,metadata,anchors,reports}."""
    for suffix in (".metadata.json", ".anchors.jsonl", ".conversion-report.md", ".md"):
        if filename.endswith(suffix):
            return filename[: -len(suffix)]
    return Path(filename).stem


def _sync_source_layer(
    slug: str, pkg: Path, modules: list[dict], source_paths: Sequence[str | Path]
) -> None:
    """Make sources/ + the manifest reflect EXACTLY the current modules' content-sha source ids.

    The map-reduce path assigns each book a CONTENT-sha source id (``<stem>-<sha8>``), which differs
    from the timestamp id a prior classic ingest used. Without this, rebuilding map-reduce *over an
    existing* package leaves a second, stale source identity (old markdown/metadata/anchors plus a
    profile.sources that points at it) that still validates but is incoherent. So assemble — the
    deterministic owner of the distilled layer — also owns the source layer: write each current id's
    markdown/metadata/report, prune any file whose id is not a current module, and rewrite the
    manifest to the current ids only. The LLM finish step then authors profile/skills/adapter against
    a single coherent identity instead of (unreliably) synthesising source files itself.

    Predecessor fields (title/author/year/rights/original_filename/file_type) are carried from an
    existing metadata file matched by source_id (the stable content-sha id), so re-MAPping over an
    existing package preserves provenance rather than degrading to stem-derived defaults.
    """
    import hashlib

    sources_root = pkg / "sources"
    for sub in _SOURCE_SUBDIRS:
        (sources_root / sub).mkdir(parents=True, exist_ok=True)

    # Snapshot predecessor metadata (keyed by input-markdown stem) BEFORE pruning, to carry provenance.
    sha_to_input = {
        hashlib.sha256(Path(sp).read_bytes()).hexdigest(): Path(sp) for sp in source_paths
    }
    predecessors: dict[str, dict] = {}
    for f in (sources_root / "metadata").glob("*.metadata.json"):
        try:
            predecessors[f.name[: -len(".metadata.json")]] = json.loads(
                f.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            continue

    cur_ids = {m["source_id"] for m in modules}
    records: list[dict] = []
    for m in modules:
        sid = m["source_id"]
        src_md = m["dir"] / "source.md"
        input_path = sha_to_input.get(m["dir"].name)
        # Match the predecessor by source_id — metadata files are named <source_id>.metadata.json,
        # and source_id is the stable content-sha id, so re-MAPping the same book carries its prior
        # provenance. (Keying on input_path.stem was wrong: the input file keeps its original name,
        # never equal to the truncated-slug+sha8 source_id, so the lookup always missed.)
        pred = predecessors.get(sid)
        text = src_md.read_text(encoding="utf-8") if src_md.exists() else ""

        if src_md.exists():
            atomic_write_text(sources_root / "markdown" / f"{sid}.md", text)

        anchors_file = sources_root / "anchors" / f"{sid}.anchors.jsonl"
        n_anchors = (
            sum(1 for ln in anchors_file.read_text(encoding="utf-8").splitlines() if ln.strip())
            if anchors_file.exists()
            else 0
        )
        mj = json.loads((m["dir"] / "module.json").read_text(encoding="utf-8"))
        meta = generate_metadata(
            original_path=src_md,
            source_id=sid,
            file_type=(pred or {}).get("file_type") or "md",
            conversion_result={
                "conversion_status": "ok",
                "stats": {
                    "word_count": len(text.split()) or None,
                    "page_count": (pred or {}).get("page_count"),
                },
                "converter_used": (pred or {}).get("converter_used"),
                "warnings": [],
            },
            output_path=sources_root / "metadata" / f"{sid}.metadata.json",
            title=(pred or {}).get("title") or mj.get("title"),
            author=(pred or {}).get("author"),
            year=(pred or {}).get("year"),
            original_url=(pred or {}).get("original_url"),
            authority=(pred or {}).get("authority", "secondary"),
            rights_status=(pred or {}).get("rights_status", "distillation-only"),
            anchor_count=n_anchors,
            notes=(pred or {}).get("notes"),
        )
        orig_fn = (pred or {}).get("original_filename") or (
            input_path.name if input_path else f"{sid}.md"
        )
        # DRY: write the conversion report through the shared writer (schema-conformant:
        # schema_version, warnings/errors, human-review, stats) instead of a hand-rolled Markdown
        # fragment that had drifted from it. sha256 + anchor_count live in the metadata JSON and the
        # anchors file, which the standard report format does not duplicate.
        generate_conversion_report(
            source_id=sid,
            original_filename=orig_fn,
            conversion_result={
                "conversion_status": "ok",
                "converter_used": (pred or {}).get("converter_used")
                or "map-reduce (pre-chunked markdown)",
                "warnings": [],
                "errors": [],
                "stats": {
                    "word_count": meta["word_count"],
                    "page_count": (pred or {}).get("page_count"),
                },
            },
            output_path=sources_root / "reports" / f"{sid}.conversion-report.md",
        )
        records.append(
            {
                "source_id": sid,
                "original_filename": orig_fn,
                "sha256": meta["sha256"],
                "conversion_status": "ok",
                "metadata_path": f"sources/metadata/{sid}.metadata.json",
                "markdown_path": f"sources/markdown/{sid}.md",
                "anchors_path": f"sources/anchors/{sid}.anchors.jsonl",
                "assets_path": None,
            }
        )

    # Prune any source file whose id is not a current module — the stale prior identity.
    for sub in _SOURCE_SUBDIRS:
        d = sources_root / sub
        if not d.exists():
            continue
        for f in d.iterdir():
            if f.is_file() and _source_id_of(f.name) not in cur_ids:
                f.unlink()

    # A map-reduce package does not carry classic-pipeline artifacts. When rebuilding over a classic
    # ingest these would otherwise linger keyed to the now-dead source id, so drop them.
    for vestige in ("interrogation-records.yaml", "analysis/claim-importance-scores.yaml"):
        (pkg / vestige).unlink(missing_ok=True)
    maps_dir = sources_root / "maps"
    if maps_dir.exists():
        shutil.rmtree(maps_dir)

    # Rewrite the manifest to exactly the current ids (generate_manifest merges -> start clean).
    manifest_path = pkg / "source-pack.manifest.yaml"
    manifest_path.unlink(missing_ok=True)
    generate_manifest(pkg, slug, records)


def assemble(
    slug: str,
    source_paths: Sequence[str | Path],
    *,
    repo: Path,
    embedder: Embedder,
    cos: float = 0.55,
    decisions: dict[int, dict] | None = None,
    select: float = 0,
    groups: list[list[int]] | None = None,
) -> dict:
    """Write the REDUCE'd distilled layer into subagents/<slug>/. Returns a counts summary.

    Pass `groups` (the same list produced by `build_groups` and fed to `emit_clusters`) to honour
    the single-producer group-index contract; when omitted, `assemble` becomes the single producer
    and clusters once here. Either way the SAME grouping backs both the emit and apply phases of a
    run, so `decisions[group_index]` cannot drift onto the wrong cluster.
    """
    cache_root = repo / "cache" / "book-extracts"
    pkg = repo / "subagents" / slug
    modules = load_modules(source_paths, cache_root)
    cmap, claims = build_claim_map(modules)
    claims_by_id = {c["claim_id"]: c for c in claims}
    gp = globalize_principles(modules, cmap)
    if groups is None:
        groups = build_groups(gp, embedder, cos)
    # Bound-check the GROUP KEYS (not just subgroup member indices, which apply_decisions already
    # guards): a decisions file built against a stale/different cluster set would otherwise have its
    # out-of-range keys silently ignored (apply_decisions falls back to `confirm`), swallowing author
    # intent. Fail loudly so the mismatch is fixed, not masked.
    if decisions:
        bad = sorted(gi for gi in decisions if not 0 <= gi < len(groups))
        if bad:
            raise ValueError(
                f"decisions reference out-of-range group keys {bad} for a cluster set of "
                f"{len(groups)} groups (valid 0..{len(groups) - 1}); the decisions were built "
                "against a different/stale grouping — regenerate clusters before assembling"
            )
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
    atomic_write_text(
        pkg / "analysis" / "claims.jsonl",
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in claims),
    )
    atomic_write_text(
        pkg / "principles" / "principles.yaml",
        yaml.safe_dump(
            {"schema_version": "principles-v1", "principles": merged},
            sort_keys=False,
            allow_unicode=True,
        ),
    )
    atomic_write_text(
        pkg / "evidence" / "evidence-records.yaml",
        yaml.safe_dump(
            {"schema_version": "evidence-records-v1", "evidence_records": evidence},
            sort_keys=False,
            allow_unicode=True,
        ),
    )
    for m in modules:
        # Ensure the per-module anchors.jsonl exists, THEN copy it. Don't gate the copy on
        # emit_anchors' truthiness: it returns the records list, which is [] (falsy) for a chunkless
        # module even after it writes the file — the old `exists() or emit_anchors()` then skipped a
        # written-but-empty anchors file, silently dropping that source's provenance.
        anchors = m["dir"] / "anchors.jsonl"
        if not anchors.exists():
            emit_anchors(m["dir"])
        if anchors.exists():
            atomic_write_text(
                pkg / "sources" / "anchors" / f"{m['source_id']}.anchors.jsonl",
                anchors.read_text(encoding="utf-8"),
            )
    # Own the source layer too: synth markdown/metadata/report for the current content-sha ids,
    # prune any stale prior identity, and rewrite the manifest — so the package has ONE coherent
    # source identity before the LLM finish step authors profile.sources against it.
    _sync_source_layer(slug, pkg, modules, source_paths)
    return {
        "books": len(modules),
        "claims": len(claims),
        "principles": len(merged),
        "evidence": len(evidence),
    }


# `_embed_minilm` is imported from reduce_principles (single definition; the two were byte-identical)
# and kept at module level here so `map_reduce_build._embed_minilm` remains a valid reference for
# existing callers (e.g. campaign/build_map_reduce.py).


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
            for ln in Path(args.sources).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
    )
    dec = (
        {int(k): v for k, v in json.loads(args.decisions.read_text(encoding="utf-8")).items()}
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
