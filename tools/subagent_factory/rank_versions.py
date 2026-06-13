"""Rank subagent versions from pairwise judge outcomes (Phase 10 eval harness — deterministic).

The agent-benchmarking research (docs/enhancement-steps/agent-benchmarking-findings.md) requires
that a version comparison (e.g. 1-source vs 2-source) carry honest uncertainty: accept a ranking
only when the versions' intervals do not overlap, not on a bare win count. This is the deterministic
ranking math — it takes already-collected pairwise outcomes (the LLM judge ensemble produces those;
that part is not here) and returns Bradley-Terry strengths with bootstrap confidence intervals plus a
"top-two separated?" verdict. No LLM.

Input: pairwise outcomes as ``[{"winner": v, "loser": v}, ...]`` (a tie → pass both orderings, or
omit). Library: ``rank_versions(pairs, n_boot=1000, seed=0) -> dict``.
CLI: ``python -m tools.subagent_factory.rank_versions <outcomes.jsonl>``.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict

import numpy as np


def bradley_terry(
    pairs: list[tuple[str, str]], iters: int = 200, tol: float = 1e-9
) -> dict[str, float]:
    """Bradley-Terry strengths via MM iteration. ``pairs`` = (winner, loser). Normalised to sum 1."""
    versions = sorted({v for p in pairs for v in p})
    if not versions:
        return {}
    wins: dict[str, float] = defaultdict(float)
    games: dict[tuple[str, str], float] = defaultdict(float)
    for w, lo in pairs:
        wins[w] += 1
        games[(w, lo)] += 1
        games[(lo, w)] += 1
    p = dict.fromkeys(versions, 1.0)
    for _ in range(iters):
        new = {}
        for i in versions:
            denom = sum(
                games[(i, j)] / (p[i] + p[j]) for j in versions if j != i and games[(i, j)] > 0
            )
            new[i] = (wins[i] / denom) if denom > 0 else p[i]
        s = sum(new.values()) or 1.0
        new = {k: v / s for k, v in new.items()}
        if max(abs(new[k] - p[k]) for k in versions) < tol:
            p = new
            break
        p = new
    return p


def rank_versions(pairs: list[dict], n_boot: int = 1000, seed: int = 0) -> dict:
    """Rank versions with bootstrap CIs on Bradley-Terry strength + top-two separation verdict."""
    tuples = [(d["winner"], d["loser"]) for d in pairs if d.get("winner") and d.get("loser")]
    base = bradley_terry(tuples)
    if not base:
        return {"ranking": [], "n_outcomes": 0, "top2_separated": False}

    rng = np.random.default_rng(seed)
    versions = sorted(base)
    samples: dict[str, list[float]] = {v: [] for v in versions}
    n = len(tuples)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        bt = bradley_terry([tuples[i] for i in idx])
        for v in versions:
            samples[v].append(bt.get(v, 0.0))

    # typed (version, strength, ci_low, ci_high) tuples for the math; output dicts built last
    rows: list[tuple[str, float, float, float]] = []
    for v in versions:
        arr = np.array(samples[v])
        rows.append((v, base[v], float(np.percentile(arr, 5)), float(np.percentile(arr, 95))))
    rows.sort(key=lambda r: -r[1])

    top2_separated = len(rows) >= 2 and rows[0][2] > rows[1][3]
    ranking = [
        {"version": v, "strength": round(s, 4), "ci_low": round(lo, 4), "ci_high": round(hi, 4)}
        for v, s, lo, hi in rows
    ]
    return {
        "ranking": ranking,
        "n_outcomes": n,
        "n_boot": n_boot,
        "top2_separated": top2_separated,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.rank_versions <outcomes.jsonl>")
        sys.exit(1)
    pairs = [
        json.loads(line)
        for line in open(sys.argv[1], encoding="utf-8").read().splitlines()
        if line.strip()
    ]
    r = rank_versions(pairs)
    print(f"versions ranked from {r['n_outcomes']} pairwise outcomes (90% bootstrap CI):")
    for i, row in enumerate(r["ranking"], 1):
        print(
            f"  {i}. {row['version']:30} strength {row['strength']:.3f}  CI[{row['ci_low']:.3f},{row['ci_high']:.3f}]"
        )
    print(
        f"verdict: top-two {'SEPARATED (ranking trustworthy)' if r['top2_separated'] else 'OVERLAP — not a reliable win'}"
    )


if __name__ == "__main__":
    main()
