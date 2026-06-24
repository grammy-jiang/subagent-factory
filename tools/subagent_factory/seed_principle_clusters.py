"""Deterministic seeder for cross-source principle clusters (Step 7 multi-source synthesis, Phase A).

Proposes candidate clusters of co-expressed principles across sources, for the LLM-confirm step to
accept/label. NO LLM here: it pairs principles whose statements overlap (token-set F1) AND that come
from DIFFERENT sources, then takes connected components spanning ≥2 sources. Output is
``principle-clusters-v1`` with ``method: seed`` and no ``canonical_statement`` (the LLM sets that on
confirmation). Single-source packages produce no clusters.

A principle's source set = the source_ids of the claims in its ``derived_from_claims``. Reuses the
``claim_recall`` token-F1 so the overlap metric matches the rest of the factory's tooling.

By default this is a **weak candidate generator**: token-F1 is paraphrase-blind, so lexical-only mode
catches only cross-source principles that share surface wording. Threshold is sensitive: too high →
nothing; too low → one over-merged component. ~0.15 surfaced clean 2-member candidates on the first
real package; treat output as a starting set for the LLM, never as the final clustering.

**C1 (embedding cosine):** pass an ``embedder`` to *also* pair cross-source paraphrases token-F1
misses (the common case — *why* multi-source synthesis is hard). It is still a candidate generator
(the LLM-confirm step decides). The embedder is **injectable** (``Callable[[list[str]],
list[list[float]]]``), mirroring how the eval harness injects its LLM judge — unit tests use a fake.
``embed_minilm`` is the provided, **validated** reference (cached, pinned all-MiniLM-L6-v2; clear
paraphrases ~0.5 vs unrelated ~0.0); the CLI ``--embeddings`` flag uses it. Library:
``seed_clusters(subagent_dir, threshold=0.15, embedder=None, cos_threshold=0.6) -> dict``.

Library: ``seed_clusters(subagent_dir, threshold=0.15) -> dict`` (principle-clusters-v1).
CLI: ``python -m tools.subagent_factory.seed_principle_clusters <subagents/slug> [threshold]``.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _content_tokens, claim_f1
from tools.subagent_factory.prov import prov_record

_DEFAULT_THRESHOLD = 0.15
# Absolute cosine floor for an embedding pair. On a single-topic package raw cosine over-merges (all
# principles ~0.4–0.5), so the floor alone is NOT enough — see _DEFAULT_MARGIN.
_DEFAULT_COS_THRESHOLD = 0.5
# C1(c) structural discrimination: an embedding pair must also stand out this far ABOVE each
# principle's MEAN cosine to its cross-source peers. Subtracting that "same-topic floor" is what
# separates "same concept" (a standout pair) from "same topic" (the whole blob sits near its mean),
# fixing the raw-cosine over-merge measured in C1(b). 0 disables the margin (pure absolute floor).
_DEFAULT_MARGIN = 0.15

Embedder = Callable[[list[str]], list[list[float]]]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


_MINILM = "sentence-transformers/all-MiniLM-L6-v2"
# Pinned commit (the locally-cached snapshot): reproducible + satisfies the unsafe-download check.
# Public HF model revision, not a credential.
_MINILM_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"  # pragma: allowlist secret


def embed_minilm(statements: list[str]) -> list[list[float]]:
    """Reference embedder for C1: cached all-MiniLM-L6-v2, mean-pooled + L2-normalised.

    Validated (``docs/output-quality-eval.md``): identical strings → cosine 1.0; clear paraphrases
    separate (~0.5) from unrelated (~0.0). It is *one* usable embedder, not the only one — the
    ``seed_clusters`` ``embedder`` arg takes any ``Callable[[list[str]], list[list[float]]]``. Lazy
    torch+transformers import + pinned, locally-cached model, so the seeder stays dependency-light
    unless embeddings are requested.
    """
    import torch
    from transformers import AutoModel, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(_MINILM, revision=_MINILM_REVISION)
    model = AutoModel.from_pretrained(_MINILM, revision=_MINILM_REVISION)
    model.eval()
    enc = tok(list(statements), padding=True, truncation=True, max_length=256, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc)
    mask = enc["attention_mask"].unsqueeze(-1).float()
    emb = (out.last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    return emb.tolist()


def _claim_sources(base: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    cp = base / "analysis" / "claims.jsonl"
    if not cp.exists():
        return out
    for line in cp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
        except json.JSONDecodeError:
            continue
        if c.get("claim_id"):
            out[c["claim_id"]] = str(c.get("source_id", "?"))
    return out


def _load_principles(base: Path) -> list[dict]:
    pp = base / "principles" / "principles.yaml"
    if not pp.exists():
        return []
    data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    return data.get("principles") or []


class _UnionFind:
    """Disjoint-set with path compression; clusters principle ids by transitive similarity."""

    def __init__(self) -> None:
        self._parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        self._parent[self.find(a)] = self.find(b)


def seed_clusters(
    subagent_dir: str | Path,
    threshold: float = _DEFAULT_THRESHOLD,
    *,
    embedder: Embedder | None = None,
    cos_threshold: float = _DEFAULT_COS_THRESHOLD,
    margin: float = _DEFAULT_MARGIN,
) -> dict:
    """Seed candidate cross-source clusters by lexical token-F1, optionally + embedding cosine (C1).

    Default (``embedder=None``) is the original lexical-only seeder. Pass ``embedder=embed_minilm`` to
    *also* pair cross-source paraphrases that share too few words to clear ``threshold``.

    **C1(c) structural discrimination (fixes the C1(b) over-merge):** an embedding pair is accepted
    only when its cosine is both ≥ ``cos_threshold`` (absolute floor) AND ≥ each principle's mean
    cross-source cosine + ``margin`` (it *stands out* from that principle's same-topic peers). On a
    single-topic package every pair sits near the mean, so nothing merges; a genuine paraphrase pair
    rises above the floor and merges. Set ``margin=0`` for the old raw-absolute behaviour.

    Output stays ``principle-clusters-v1`` (``method: seed``); ``mean_overlap`` remains the *lexical*
    overlap, so a low value on a populated cluster signals an embedding-driven merge.
    """
    base = Path(subagent_dir)
    claim_src = _claim_sources(base)
    principles = _load_principles(base)
    pid_stmt = {p["principle_id"]: str(p.get("statement", "")) for p in principles}
    pid_sources = {
        p["principle_id"]: {claim_src.get(c, "?") for c in (p.get("derived_from_claims") or [])}
        for p in principles
    }

    emb: dict[str, list[float]] | None = None
    cos: dict[tuple[str, str], float] = {}
    peer_sum: dict[str, float] = {}
    peer_n: dict[str, int] = {}
    if embedder is not None and pid_stmt:
        pids = list(pid_stmt)
        emb = dict(zip(pids, embedder([pid_stmt[p] for p in pids]), strict=False))
        peer_sum = {p: 0.0 for p in pids}
        peer_n = {p: 0 for p in pids}
        for a, b in combinations(pids, 2):
            if pid_sources[a].isdisjoint(pid_sources[b]):  # cross-source
                c = _cosine(emb[a], emb[b])
                cos[(a, b)] = c
                peer_sum[a] += c
                peer_sum[b] += c
                peer_n[a] += 1
                peer_n[b] += 1

    def _baseline(p: str, exclude: float) -> float:
        # leave-one-out mean of p's cross-source cosines, excluding the pair under test (so a
        # principle with only this one peer has no "floor" to clear — avoids a degenerate small-set
        # self-comparison). 0.0 when p has no other cross-source peer.
        n = peer_n.get(p, 0)
        return (peer_sum[p] - exclude) / (n - 1) if n > 1 else 0.0

    def _embedding_pair(a: str, b: str) -> bool:
        c = cos.get((a, b))
        if c is None or c < cos_threshold:
            return False
        return c >= _baseline(a, c) + margin and c >= _baseline(b, c) + margin

    uf = _UnionFind()
    pair_score: dict[tuple[str, str], float] = {}  # lexical overlap, drives mean_overlap
    edges: list[tuple[str, str]] = []
    for a, b in combinations(pid_stmt, 2):
        if not pid_sources[a].isdisjoint(pid_sources[b]):  # cross-source only
            continue
        s = claim_f1(pid_stmt[a], pid_stmt[b])
        accept = s >= threshold or (emb is not None and _embedding_pair(a, b))
        if accept:
            uf.union(a, b)
            edges.append((a, b))
            pair_score[(a, b)] = s  # lexical s (may be < threshold when joined only by embedding)

    groups: dict[str, list[str]] = {}
    for pid in {x for e in edges for x in e}:
        groups.setdefault(uf.find(pid), []).append(pid)

    clusters = []
    for i, members in enumerate(sorted(groups.values(), key=len, reverse=True)):
        sources = sorted({s for m in members for s in pid_sources[m] if s != "?"})
        if len(sources) < 2:
            continue
        scores = [
            pair_score[(a, b)] for a, b in combinations(sorted(members), 2) if (a, b) in pair_score
        ]
        shared = (
            set.intersection(*[_content_tokens(pid_stmt[m]) for m in members]) if members else set()
        )
        clusters.append(
            {
                "cluster_id": f"pc{i:03d}",
                "member_principle_ids": sorted(members),
                "sources": sources,
                "canonical_statement": None,
                "method": "seed",
                "shared_terms": sorted(shared)[:12],
                "mean_overlap": round(sum(scores) / len(scores), 3) if scores else 0.0,
                # C2: full PROV-O — this cluster was derived from its member principles + sources.
                "provenance": prov_record("cluster-seed", sorted(members) + sources),
            }
        )

    return {
        "schema_version": "principle-clusters-v1",
        "subagent_slug": base.name,
        "clusters": clusters,
    }


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    use_embeddings = "--embeddings" in sys.argv
    if not args:
        print(
            "Usage: python -m tools.subagent_factory.seed_principle_clusters "
            "<subagents/slug> [threshold] [--embeddings]   # --embeddings: add C1 cosine via MiniLM"
        )
        sys.exit(1)
    threshold = float(args[1]) if len(args) > 1 else _DEFAULT_THRESHOLD
    result = seed_clusters(args[0], threshold, embedder=embed_minilm if use_embeddings else None)
    n = len(result["clusters"])
    print(f"seeded {n} candidate cross-source cluster(s) (threshold {threshold}):")
    for c in result["clusters"]:
        print(
            f"  {c['cluster_id']}: {len(c['member_principle_ids'])} principles "
            f"across {c['sources']} (overlap {c['mean_overlap']}); shared: {c['shared_terms'][:6]}"
        )
    out = Path(args[0]) / "principles" / "principle-clusters.seed.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
