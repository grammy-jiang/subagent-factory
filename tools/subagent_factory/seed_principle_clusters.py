"""Deterministic seeder for cross-source principle clusters (Step 7 multi-source synthesis, Phase A).

Proposes candidate clusters of co-expressed principles across sources, for the LLM-confirm step to
accept/label. NO LLM here: it pairs principles whose statements overlap (token-set F1) AND that come
from DIFFERENT sources, then takes connected components spanning ≥2 sources. Output is
``principle-clusters-v1`` with ``method: seed`` and no ``canonical_statement`` (the LLM sets that on
confirmation). Single-source packages produce no clusters.

A principle's source set = the source_ids of the claims in its ``derived_from_claims``. Reuses the
``claim_recall`` token-F1 so the overlap metric matches the rest of the factory's tooling.

This seed is intentionally a **weak candidate generator**: token-F1 is paraphrase-blind, so it only
catches cross-source principles that share surface wording. Differently-worded equivalents (the
common case — that is *why* multi-source synthesis is hard) are missed here and are the LLM-confirm
step's job to add. Threshold is sensitive: too high → nothing; too low → one over-merged component.
~0.15 surfaced clean 2-member candidates on the first real package; treat output as a starting set
for the LLM, never as the final clustering.

Library: ``seed_clusters(subagent_dir, threshold=0.15) -> dict`` (principle-clusters-v1).
CLI: ``python -m tools.subagent_factory.seed_principle_clusters <subagents/slug> [threshold]``.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _content_tokens, claim_f1

_DEFAULT_THRESHOLD = 0.15


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


class _UF:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        self.p[self.find(a)] = self.find(b)


def seed_clusters(subagent_dir: str | Path, threshold: float = _DEFAULT_THRESHOLD) -> dict:
    base = Path(subagent_dir)
    claim_src = _claim_sources(base)
    principles = _load_principles(base)
    pid_stmt = {p["principle_id"]: str(p.get("statement", "")) for p in principles}
    pid_sources = {
        p["principle_id"]: {claim_src.get(c, "?") for c in (p.get("derived_from_claims") or [])}
        for p in principles
    }

    uf = _UF()
    pair_score: dict[tuple[str, str], float] = {}
    for a, b in combinations(pid_stmt, 2):
        if pid_sources[a].isdisjoint(pid_sources[b]):  # cross-source only
            s = claim_f1(pid_stmt[a], pid_stmt[b])
            if s >= threshold:
                uf.union(a, b)
                pair_score[(a, b)] = s

    groups: dict[str, list[str]] = {}
    for pid in {x for pair in pair_score for x in pair}:
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
            }
        )

    return {
        "schema_version": "principle-clusters-v1",
        "subagent_slug": base.name,
        "clusters": clusters,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python -m tools.subagent_factory.seed_principle_clusters "
            "<subagents/slug> [threshold]"
        )
        sys.exit(1)
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else _DEFAULT_THRESHOLD
    result = seed_clusters(sys.argv[1], threshold)
    n = len(result["clusters"])
    print(f"seeded {n} candidate cross-source cluster(s) (threshold {threshold}):")
    for c in result["clusters"]:
        print(
            f"  {c['cluster_id']}: {len(c['member_principle_ids'])} principles "
            f"across {c['sources']} (overlap {c['mean_overlap']}); shared: {c['shared_terms'][:6]}"
        )
    out = Path(sys.argv[1]) / "principles" / "principle-clusters.seed.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    main()
