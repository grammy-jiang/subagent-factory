"""Deterministic grounding-leak scorer for a subagent's review output (no LLM).

Automates the manual check from the output-quality eval (see docs/output-quality-eval.md): does a
review lean on domain vocabulary that is actually grounded in the subagent's distilled source, or
on terms the base model supplied ("leak")? Compares the review's salient multi-word domain terms
against the subagent's grounded vocabulary (principles.yaml + claims.jsonl).

A review necessarily quotes the reviewed document's own nouns (component names, file names) — those
are subject matter, not the reviewer's expertise, so they must be excluded first. Pass the reviewed
doc: any salient review bigram that also appears in the doc is dropped as quoted subject matter. The
remainder is the reviewer's **own concept vocabulary**. Of that, a bigram is **grounded** if the
exact bigram is in the subagent's grounded vocabulary OR both its content tokens are; a salient one
that is neither is a **leak candidate** (the reviewer reached for a concept outside its source).
``coverage`` = grounded / (grounded + leak) over the reviewer's own concept vocabulary.

Library: ``grounding_check(subagent_dir, review_path, doc_path=None) -> dict``.
CLI: ``python -m tools.subagent_factory.grounding_check <subagents/slug> <review.md> [<doc.md>]``.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _STOPWORDS, _content_tokens

_MIN_SALIENCE = 2  # a review bigram must appear at least this many times to be "leaned on"
_TOP_LEAK = 15


def _token_seq(text: str) -> list[str]:
    """Ordered content tokens (lowercased, >2 chars, stopwords dropped)."""
    return [
        t
        for t in re.findall(r"[a-z][a-z0-9]+", str(text).lower())
        if len(t) > 2 and t not in _STOPWORDS
    ]


def _bigrams(text: str) -> list[str]:
    toks = _token_seq(text)
    return [f"{a} {b}" for a, b in zip(toks, toks[1:], strict=False)]


def _grounded_vocab(base: Path) -> tuple[set[str], set[str]]:
    """(grounded_unigrams, grounded_bigrams) from principles.yaml + claims.jsonl statements."""
    text_parts: list[str] = []
    pp = base / "principles" / "principles.yaml"
    if pp.exists():
        data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
        text_parts += [str(p.get("statement", "")) for p in (data.get("principles") or [])]
    cp = base / "analysis" / "claims.jsonl"
    if cp.exists():
        for line in cp.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                text_parts.append(str(json.loads(line).get("statement", "")))
            except json.JSONDecodeError:
                continue
    blob = "\n".join(text_parts)
    return set(_content_tokens(blob)), set(_bigrams(blob))


def _sibling_concept_index(root: Path, exclude: str) -> dict[str, list[str]]:
    """{bigram -> [sibling slug whose source contains that exact bigram]} across the corpus.

    Exact-bigram match (not the lenient both-token rule) so the cross-source signal is precise: a
    leak term found here is a named expert concept that *another* distilled source actually uses —
    high-confidence borrow, and it names the source to add (the eval-driven multi-source recipe).
    """
    index: dict[str, list[str]] = {}
    if not root.exists():
        return index
    for pkg in sorted(root.iterdir()):
        if not pkg.is_dir() or pkg.name == exclude or not (pkg / "profile.yaml").exists():
            continue
        _, sib_bi = _grounded_vocab(pkg)
        for bg in sib_bi:
            index.setdefault(bg, []).append(pkg.name)
    return index


def grounding_check(
    subagent_dir: str | Path,
    review_path: str | Path,
    doc_path: str | Path | None = None,
    cross_source: bool = True,
) -> dict:
    base = Path(subagent_dir)
    uni, bi = _grounded_vocab(base)
    review = Path(review_path).read_text(encoding="utf-8")
    freq = Counter(_bigrams(review))
    salient = {bg: n for bg, n in freq.items() if n >= _MIN_SALIENCE}

    # Drop bigrams quoted from the reviewed doc — that's subject matter, not the reviewer's lens.
    doc_bigrams: set[str] = set()
    if doc_path:
        doc_bigrams = set(_bigrams(Path(doc_path).read_text(encoding="utf-8")))
    concept = {bg: n for bg, n in salient.items() if bg not in doc_bigrams}

    def grounded(bg: str) -> bool:
        if bg in bi:
            return True
        a, b = bg.split(" ", 1)
        return a in uni and b in uni

    grounded_terms = {bg for bg in concept if grounded(bg)}
    leak = sorted(
        ((bg, n) for bg, n in concept.items() if bg not in grounded_terms),
        key=lambda kv: -kv[1],
    )
    coverage = len(grounded_terms) / len(concept) if concept else 1.0

    # Cross-source: which leak terms are named concepts in ANOTHER subagent's source (precise,
    # actionable borrows — they name the source to add). Aggregated by sibling for the recipe.
    cross_terms: list[tuple[str, int, list[str]]] = []
    add_source: Counter = Counter()
    if cross_source:
        idx = _sibling_concept_index(base.parent, base.name)
        for bg, n in leak:
            sibs = idx.get(bg)
            if sibs:
                cross_terms.append((bg, n, sibs))
                for s in sibs:
                    add_source[s] += n
    return {
        "coverage": round(coverage, 3),
        "n_concept_terms": len(concept),
        "n_grounded": len(grounded_terms),
        "n_leak": len(leak),
        "n_doc_quoted_dropped": len(salient) - len(concept),
        "grounded_vocab_size": len(uni),
        "leak_terms": leak[:_TOP_LEAK],
        "cross_source_terms": cross_terms[:_TOP_LEAK],
        "suggested_sources": add_source.most_common(3),
    }


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: python -m tools.subagent_factory.grounding_check "
            "<subagents/slug> <review.md> [<doc.md>]"
        )
        sys.exit(1)
    doc = sys.argv[3] if len(sys.argv) > 3 else None
    r = grounding_check(sys.argv[1], sys.argv[2], doc)
    print(
        f"grounding coverage {r['coverage']:.0%} "
        f"({r['n_grounded']}/{r['n_concept_terms']} reviewer-concept bigrams grounded; "
        f"{r['n_leak']} leak candidates; {r['n_doc_quoted_dropped']} doc-quoted dropped; "
        f"grounded-vocab {r['grounded_vocab_size']} tokens)"
    )
    if r["cross_source_terms"]:
        print("cross-source borrows (concept is in another subagent's source — high-confidence):")
        for bg, n, sibs in r["cross_source_terms"]:
            print(f"  x{n:<3d} {bg:<28s} <- {', '.join(sibs)}")
        if r["suggested_sources"]:
            print(
                "suggested source(s) to add (multi-source grounding):",
                ", ".join(f"{s}(+{w})" for s, w in r["suggested_sources"]),
            )
    else:
        print("no cross-source borrows found; top leak candidates (human-confirm):")
        for bg, n in r["leak_terms"][:8]:
            print(f"  x{n:<3d} {bg}")


if __name__ == "__main__":
    main()
