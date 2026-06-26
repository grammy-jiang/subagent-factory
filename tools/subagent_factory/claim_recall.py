"""Deterministic claim-recall harness (Step 10 G3, the no-ML complement).

The source-structure-mapping skill's claim-recall is an LLM self-check (FActScore/KPA style).
This is its deterministic, dependency-free counterpart: it measures how many of a *reference*
claim set are recalled by a *candidate* claim set by lexical content-token overlap — so an A/B
(flat extraction vs structure-mapped) can be scored on claim CONTENT, not just anchor position,
without an embedding model.

Matching is token-set F1 over content tokens (lowercased word tokens, stopwords and length<=2
dropped). A reference claim is "recalled" if some candidate scores >= ``threshold`` (per-reference
independent matching — one candidate may recall several references; see ``claim_recall`` for the
precise semantics). This is a paraphrase-blind lower bound — lexical overlap under-counts true semantic matches — so treat the
numbers as a conservative floor, useful for *relative* arm comparison rather than an absolute truth.

Library: ``claim_recall(reference, candidate, threshold) -> dict``.
CLI: ``python -m tools.subagent_factory.claim_recall <ref> <cand>`` where each path is a
claims.jsonl (``statement`` per line) or a ``*.source-map.yaml`` (``candidate_units[].statement``).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

# --- Shared tokenizer (PUBLIC contract) -------------------------------------------------------
# ``STOPWORDS`` and ``content_tokens`` are the single source of truth for lexical content-token
# extraction across the factory. They are imported by seven other modules (grounding_check,
# ask_gate, reground_skill_anchors, behaviour_replay, reanchor_claims, retrieval_ab,
# seed_principle_clusters). Treat any change here as a contract change: it shifts recall/grounding
# numbers in every importer at once. ``test_claim_recall.py`` pins this contract.

# Small, deliberately generic stopword set — domain terms must survive so matching stays meaningful.
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "if",
    "then",
    "else",
    "for",
    "of",
    "to",
    "in",
    "on",
    "at",
    "by",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "as",
    "with",
    "from",
    "into",
    "than",
    "can",
    "should",
    "must",
    "may",
    "will",
    "you",
    "your",
    "we",
    "our",
    "they",
    "their",
    "not",
    "no",
    "do",
    "does",
    "when",
    "which",
    "who",
    "what",
    "how",
    "why",
    "use",
    "used",
    "using",
    "via",
    "per",
    "also",
    "such",
    "more",
    "most",
}


def content_tokens(text: str) -> set[str]:
    """Lowercased word tokens with stopwords and length<=2 dropped — the shared tokenizer."""
    return {
        t
        for t in re.findall(r"[a-z][a-z0-9]+", str(text).lower())
        if len(t) > 2 and t not in STOPWORDS
    }


# Backward-compat aliases: the seven importers reference these private names. Keep them bound to
# the public names so the contract stays single-source without churning 7 files.
_STOPWORDS = STOPWORDS
_content_tokens = content_tokens


def claim_f1(a: str, b: str) -> float:
    """Token-set F1 between two claim statements (0..1)."""
    ta, tb = content_tokens(a), content_tokens(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    if not inter:
        return 0.0
    precision = inter / len(tb)
    recall = inter / len(ta)
    return 2 * precision * recall / (precision + recall)


def claim_recall(reference: list[str], candidate: list[str], threshold: float = 0.5) -> dict:
    """Score how many ``reference`` claims are recalled by ``candidate`` claims.

    Matching semantics — PER-REFERENCE INDEPENDENT MATCHING (not a 1:1 assignment):

    * A reference claim is "recalled" if ANY candidate scores ``>= threshold`` against it. A
      single candidate may therefore recall several references; recall is the fraction of
      reference claims with at least one above-threshold candidate. This is deliberate: a
      structure-mapped candidate that subsumes two narrow reference claims should count for both.
    * ``precision`` is the fraction of DISTINCT candidates that recall at least one reference (a
      duplication/noise signal): candidates that match nothing are noise. Because matching is
      independent per reference, precision is order-independent — it counts the set of candidates
      that ever cleared threshold, with no first-candidate tie-break.

    Returns recall, precision, f1, counts, and the unmatched reference statements (recall gaps).
    """
    matched_ref: list[str] = []
    unmatched_ref: list[str] = []
    matching_candidates: set[int] = set()
    for r in reference:
        # Per-reference: every candidate that clears threshold counts (no greedy first-best pick).
        hits = [j for j, c in enumerate(candidate) if claim_f1(r, c) >= threshold]
        if hits:
            matched_ref.append(r)
            matching_candidates.update(hits)
        else:
            unmatched_ref.append(r)
    used_candidate = matching_candidates
    n_ref, n_cand = len(reference), len(candidate)
    recall = len(matched_ref) / n_ref if n_ref else 0.0
    precision = len(used_candidate) / n_cand if n_cand else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "recall": round(recall, 3),
        "precision": round(precision, 3),
        "f1": round(f1, 3),
        "n_reference": n_ref,
        "n_candidate": n_cand,
        "n_matched": len(matched_ref),
        "threshold": threshold,
        "unmatched_reference": unmatched_ref,
    }


def load_statements(path: str | Path) -> list[str]:
    """Read claim statements from a claims.jsonl or a *.source-map.yaml candidate_units block."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        data = yaml.safe_load(text) or {}
        units = data.get("candidate_units") or []
        return [str(u.get("statement", "")) for u in units if u.get("statement")]
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        stmt = rec.get("statement")
        if stmt:
            out.append(str(stmt))
    return out


_USAGE = (
    "Usage: python -m tools.subagent_factory.claim_recall <reference> <candidate> "
    "[threshold]\n  each path: claims.jsonl or *.source-map.yaml; threshold in [0, 1]"
)


def main() -> None:
    if len(sys.argv) < 3:
        print(_USAGE)
        sys.exit(1)
    threshold = 0.5
    if len(sys.argv) > 3:
        try:
            threshold = float(sys.argv[3])
        except ValueError:
            print(f"error: threshold must be a number in [0, 1], got {sys.argv[3]!r}\n{_USAGE}")
            sys.exit(1)
        if not 0.0 <= threshold <= 1.0:
            print(f"error: threshold must be in [0, 1], got {threshold}\n{_USAGE}")
            sys.exit(1)
    reference = load_statements(sys.argv[1])
    candidate = load_statements(sys.argv[2])
    rep = claim_recall(reference, candidate, threshold)
    print(
        f"claim-recall (threshold {rep['threshold']}): "
        f"recall {rep['recall']:.0%} ({rep['n_matched']}/{rep['n_reference']}) | "
        f"precision {rep['precision']:.0%} | f1 {rep['f1']:.0%} | candidate {rep['n_candidate']}"
    )
    for s in rep["unmatched_reference"][:15]:
        print(f"  MISS: {s[:90]}")
    if len(rep["unmatched_reference"]) > 15:
        print(f"  … +{len(rep['unmatched_reference']) - 15} more misses")


if __name__ == "__main__":
    main()
