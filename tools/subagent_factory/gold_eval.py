"""Judge↔gold agreement (Phase 10 B4) — break circular evaluation with a human authority set.

The agent-benchmarking research: a self-judged eval inflates scores (silver Micro-F1 ~0.54 → gold
~0.03); trust a judge only after measuring its agreement with an INDEPENDENT gold set, reported as
inter-annotator agreement (Cohen's κ). This module is the deterministic agreement math + the
comparison; the **gold labels must be human-provided** — generating them with an LLM reproduces the
exact circularity B4 exists to break, so this module never creates gold, only scores against it.

Gold-set format (human-authored), one JSON object per line:
    {"item": "<comparison id>", "winner": "<version label>", "annotator": "<who>"}
Judge labels are the per-item majority winners from ``judge_ab.run_ab_ensemble``.

Rule of thumb: κ ≥ 0.6 (substantial) → the judge tracks human judgement well enough to trust its
verdicts; below that, the judge (or rubric) needs work before its rankings mean anything.
"""

from __future__ import annotations

from collections import Counter


def cohens_kappa(rater_a: list[str], rater_b: list[str]) -> float:
    """Cohen's κ for two raters over categorical labels (paired, same length)."""
    n = len(rater_a)
    if n == 0:
        return 0.0
    po = sum(x == y for x, y in zip(rater_a, rater_b, strict=False)) / n
    ca, cb = Counter(rater_a), Counter(rater_b)
    cats = set(rater_a) | set(rater_b)
    pe = sum((ca.get(c, 0) / n) * (cb.get(c, 0) / n) for c in cats)
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def _kappa_band(k: float) -> str:
    if k < 0:
        return "poor"
    if k < 0.2:
        return "slight"
    if k < 0.4:
        return "fair"
    if k < 0.6:
        return "moderate"
    if k < 0.8:
        return "substantial"
    return "almost-perfect"


def judge_vs_gold(judge_labels: dict[str, str], gold_labels: dict[str, str]) -> dict:
    """Compare a judge's per-item winners against the gold set over their overlapping items."""
    items = sorted(set(judge_labels) & set(gold_labels))
    a = [judge_labels[i] for i in items]
    b = [gold_labels[i] for i in items]
    n = len(items)
    raw = sum(x == y for x, y in zip(a, b, strict=False)) / n if n else 0.0
    kappa = round(cohens_kappa(a, b), 3)
    return {
        "n_overlap": n,
        "raw_agreement": round(raw, 3),
        "cohens_kappa": kappa,
        "interpretation": _kappa_band(kappa),
        "trust_judge": kappa >= 0.6,
    }


def load_gold(path: str) -> dict[str, str]:
    """Read a human gold-label jsonl into ``{item: winner}`` (last label per item wins)."""
    import json
    from pathlib import Path

    out: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("item") and rec.get("winner"):
            out[str(rec["item"])] = str(rec["winner"])
    return out
