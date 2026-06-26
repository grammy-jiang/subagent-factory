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
import statistics
import sys
import warnings
from collections import Counter
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _STOPWORDS

_MIN_SALIENCE = 2  # a review bigram must appear at least this many times to be "leaned on"
_TOP_LEAK = 15

# Denoise: a concept bigram is "generic" (common engineering vocab, not a distinctive borrow) when
# it is grounded in >= _GENERIC_DF packages' sources, OR both its tokens are universal qualifiers.
# Generic bigrams are excluded from coverage, leaks, and cross-source attribution so the score
# reflects *distinctive* concept grounding and borrows name a real source, not a phrase collision
# (e.g. "correctness performance" was falsely attributed to xv6-kernel-internals-reviewer).
_GENERIC_DF = 3
_GENERIC_TOKENS = frozenset(
    {
        "correctness",
        "performance",
        "quality",
        "issue",
        "issues",
        "error",
        "errors",
        "result",
        "results",
        "impact",
        "before",
        "after",
        "apply",
        "applying",
        "applied",
        "highest",
        "lowest",
        "overall",
        "general",
        "various",
        "multiple",
        "several",
        "important",
        "simple",
        "complex",
        "good",
        "better",
        "best",
        "proper",
        "common",
        "clear",
        "strong",
        "high",
        "low",
        "large",
        "small",
        "main",
        "core",
        "key",
    }
)


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
    # Derive unigrams and bigrams from the SAME tokenizer (_token_seq). Previously unigrams came from
    # claim_recall._content_tokens while bigrams came from _token_seq; if the two ever drifted,
    # grounded() (which checks a bigram's two halves against the unigram set) would mismatch on
    # tokenization rather than on actual grounding. One tokenizer → the check is leak-driven.
    toks = _token_seq(blob)
    return set(toks), set(_bigrams(blob))


def _corpus_bigram_map(
    root: Path, self_bigrams: tuple[str, set[str]] | None = None
) -> dict[str, set[str]]:
    """{bigram -> {package slugs whose grounded source contains that exact bigram}} (incl self).

    One pass over the corpus serves two jobs: document-frequency (genericness — a bigram in many
    sources is common vocab) and cross-source attribution (a distinctive leak found in exactly one
    *other* source names the source to add — the eval-driven multi-source recipe). Exact-bigram
    match keeps the borrow signal precise.

    ``self_bigrams`` lets the caller inject the package-under-review's already-computed
    ``(slug, bigrams)`` so we skip re-parsing it here (the package's vocab was derived once in
    ``grounding_check``). The package is matched by directory name and its precomputed bigrams are
    folded in instead of re-deriving them from disk — the resulting map is identical, just without
    the redundant YAML+JSONL parse fan-out over the package under review.
    """
    index: dict[str, set[str]] = {}
    self_slug: str | None = None
    if self_bigrams is not None:
        self_slug = self_bigrams[0]
        for bg in self_bigrams[1]:
            index.setdefault(bg, set()).add(self_slug)
    if not root.exists():
        return index
    for pkg in sorted(root.iterdir()):
        if not pkg.is_dir() or not (pkg / "profile.yaml").exists():
            continue
        if pkg.name == self_slug:
            continue  # already injected via self_bigrams — avoid the redundant re-parse
        _, pkg_bi = _grounded_vocab(pkg)
        for bg in pkg_bi:
            index.setdefault(bg, set()).add(pkg.name)
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

    cmap = _corpus_bigram_map(base.parent, (base.name, bi)) if cross_source else {}

    def is_generic(bg: str) -> bool:
        if len(cmap.get(bg, ())) >= _GENERIC_DF:
            return True
        a, b = bg.split(" ", 1)
        return a in _GENERIC_TOKENS and b in _GENERIC_TOKENS

    # Distinctive concept vocab = the reviewer's own concept bigrams minus common/corpus-generic
    # ones, so coverage measures *distinctive* concept grounding and leaks/borrows are meaningful.
    distinctive = {bg: n for bg, n in concept.items() if not is_generic(bg)}
    n_generic_dropped = len(concept) - len(distinctive)

    grounded_terms = {bg for bg in distinctive if grounded(bg)}
    leak = sorted(
        ((bg, n) for bg, n in distinctive.items() if bg not in grounded_terms),
        key=lambda kv: -kv[1],
    )
    # Empty distinctive vocab (empty/trivial reviewer output, or all terms dropped as generic/quoted)
    # is "nothing to assess", NOT "perfectly grounded". Returning 1.0 here let a degenerate review
    # silently score as a perfect pass on the gate it informs. Report coverage=None + scored=False so
    # a consumer treats it as not-applicable rather than a ceiling.
    scored = bool(distinctive)
    coverage = (len(grounded_terms) / len(distinctive)) if scored else None

    # Cross-source: a distinctive leak that ANOTHER source grounds names that source to add
    # (precise, actionable — the eval-driven multi-source recipe).
    cross_terms: list[tuple[str, int, list[str]]] = []
    src_bigrams: dict[str, set[str]] = {}
    for bg, n in leak:
        sibs = sorted(cmap.get(bg, set()) - {base.name})
        if sibs:
            cross_terms.append((bg, n, sibs))
            for s in sibs:
                src_bigrams.setdefault(s, set()).add(bg)
    # Suggest a source only when >= 2 DISTINCT distinctive borrows point to it — a single shared
    # phrase is a collision (e.g. "architecture review"), not evidence the source is missing.
    suggested = sorted(
        ((s, len(bgs)) for s, bgs in src_bigrams.items() if len(bgs) >= 2),
        key=lambda kv: (-kv[1], kv[0]),
    )[:3]
    return {
        "coverage": round(coverage, 3) if coverage is not None else None,
        "scored": scored,
        "n_concept_terms": len(distinctive),
        "n_grounded": len(grounded_terms),
        "n_leak": len(leak),
        "n_generic_dropped": n_generic_dropped,
        "n_doc_quoted_dropped": len(salient) - len(concept),
        "grounded_vocab_size": len(uni),
        "leak_terms": leak[:_TOP_LEAK],
        "cross_source_terms": cross_terms[:_TOP_LEAK],
        "suggested_sources": suggested,
    }


_BASELINE_PATH = Path(__file__).with_name("grounding_baseline.json")


def load_baseline(path: Path | None = None) -> list[dict]:
    """Recorded (slug, doc, coverage) calibration points. Absolute coverage is only interpretable
    relative to this distribution — the *rank* is the signal, not the raw %."""
    p = path or _BASELINE_PATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        # Genuinely absent baseline is normal on first run — silent, no signal needed.
        return []
    except (OSError, json.JSONDecodeError) as exc:
        # A present-but-corrupt baseline must NOT silently degrade a calibration gate to no-signal.
        # Warn (naming the path) so the corruption is visible, then fall back to no baseline.
        warnings.warn(
            f"grounding baseline at {p} is unreadable/corrupt ({exc}); ignoring it",
            RuntimeWarning,
            stacklevel=2,
        )
        return []
    return data if isinstance(data, list) else []


def _baseline_is_corrupt(p: Path) -> bool:
    """True iff the file EXISTS and is non-empty but cannot be parsed as JSON — i.e. corruption
    (a torn/truncated file), distinct from genuinely absent (FileNotFoundError) or legitimately
    empty (``[]`` / whitespace). Used to refuse a read-modify-write that would clobber recoverable
    history. Relies on json.JSONDecodeError directly rather than load_baseline's lossy [] so a
    corrupt file is never mistaken for an empty one."""
    try:
        raw = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False  # absent → first run, not corruption
    except OSError:
        return True  # exists but unreadable (permissions, torn inode) → treat as corrupt
    if not raw.strip():
        return False  # legitimately empty file → safe to append
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        return True  # present, non-empty, unparseable → corruption
    return False


def baseline_band(
    coverage: float, records: list[dict] | None = None, path: Path | None = None
) -> dict | None:
    """Where a coverage sits in the recorded baseline: floor / median / ceiling + percentile."""
    recs = records if records is not None else load_baseline(path)
    covs = sorted(float(r["coverage"]) for r in recs if "coverage" in r)
    if not covs:
        return None
    return {
        "n": len(covs),
        "floor": covs[0],
        "median": statistics.median(covs),
        "ceiling": covs[-1],
        "percentile": round(100 * sum(1 for c in covs if c <= coverage) / len(covs)),
    }


def record_baseline(
    slug: str, coverage: float, doc: str | None = None, path: Path | None = None
) -> None:
    """Append a measured coverage point so the calibration baseline grows with each eval.

    Refuses to write over a present-but-corrupt baseline: load_baseline returns [] for a corrupt
    file (after warning), so a naive append+overwrite would convert visible corruption into silent
    TOTAL loss of all prior recoverable points. An absent file (first run) or a legitimately-empty
    ``[]`` baseline still appends normally.
    """
    p = path or _BASELINE_PATH
    if _baseline_is_corrupt(p):
        raise ValueError(
            f"refusing to record baseline: existing baseline at {p} is non-empty but corrupt "
            f"(unparseable JSON). Overwriting it would destroy prior recoverable points. "
            f"Inspect/repair or remove the file, then retry."
        )
    recs = load_baseline(p)
    recs.append({"slug": slug, "doc": doc or "", "coverage": round(float(coverage), 3)})
    p.write_text(json.dumps(recs, indent=2) + "\n", encoding="utf-8")


def grounding_richness(subagent_dir: str | Path) -> dict:
    """Deterministic, run-independent grounding size of a package: claim + principle counts plus
    grounded vocabulary (unigrams/bigrams from principles + claims). Unlike review-coverage this
    needs no LLM review or reviewed doc, so it is the reliable before/after gate for a strengthen:
    adding a source must GROW these, never shrink them (the Round-4 full-reauthor shrank devops
    72->50 claims under Copilot's cap — this measure caught it cleanly).
    """
    base = Path(subagent_dir)
    uni, bi = _grounded_vocab(base)
    cl = base / "analysis" / "claims.jsonl"
    nclaims = (
        sum(1 for ln in cl.read_text(encoding="utf-8").splitlines() if ln.strip())
        if cl.exists()
        else 0
    )
    nprin = 0
    pp = base / "principles" / "principles.yaml"
    if pp.exists():
        try:
            data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
            nprin = len(data.get("principles") or [])
        except yaml.YAMLError:
            nprin = 0
    return {
        "claims": nclaims,
        "principles": nprin,
        "grounded_unigrams": len(uni),
        "grounded_bigrams": len(bi),
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
    cov = f"{r['coverage']:.0%}" if r["coverage"] is not None else "n/a (no distinctive vocab)"
    print(
        f"grounding coverage {cov} "
        f"({r['n_grounded']}/{r['n_concept_terms']} distinctive concept bigrams grounded; "
        f"{r['n_leak']} leak candidates; {r['n_generic_dropped']} generic dropped; "
        f"{r['n_doc_quoted_dropped']} doc-quoted dropped; grounded-vocab {r['grounded_vocab_size']} tokens)"
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
