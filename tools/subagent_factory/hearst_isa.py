"""Hybrid Hearst is-a extraction → candidate ``specializes`` edges (Step 7, C3).

Three signals, best-available wins, all deterministic:

1. **Hearst patterns (spaCy)** — "X such as Y", "X including Y", "Y and other X"… The spaCy parse
   snaps the hypernym/hyponym spans to real noun-chunk boundaries (clean heads), far better than raw
   string slicing. Falls back to a **flat regex** extractor when spaCy is absent (CI / light install)
   — higher precision, lower recall, zero dependency.
2. **WordNet (nltk)** — a general-English hypernym lexicon used to *confirm* a Hearst pair (is the
   claimed hypernym a transitive WordNet hypernym of the hyponym?). A confirmed pair is high
   confidence; a Hearst-only pair is low. This is the "hybrid with distributional/lexical" the plan
   calls for.

``hearst_pairs(text)`` is the reusable extractor. ``seed_specializes(principles)`` maps the is-a
pairs to candidate ``specializes`` edges (principle-graph-v1 fragment, ``method: seed``) for the
LLM-confirm step to decide. Measured caveat: on *distilled principle statements* the signal is thin
(principles are imperative rules, not enumerations) — the extractor's real yield is on enumerative
**source prose**, which callers can pass in. spaCy + nltk are the optional ``nlp`` extra; neither is
required for the flat path.
"""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path

import yaml

from tools.subagent_factory.prov import prov_record

_FUNCTION = {
    "a",
    "an",
    "the",
    "of",
    "to",
    "for",
    "so",
    "that",
    "and",
    "or",
    "but",
    "with",
    "in",
    "on",
    "by",
    "as",
    "is",
    "are",
    "be",
    "been",
    "being",
    "your",
    "their",
    "its",
    "this",
    "these",
    "those",
    "such",
    "other",
    "any",
    "all",
    "some",
    "more",
    "most",
    "than",
    "then",
    "it",
    "they",
    "we",
    "you",
    "use",
    "using",
    "used",
    "via",
    "into",
    "from",
    "at",
    "if",
    "when",
    "which",
}
_TRIGGERS_HL = (" such as ", " including ", ", especially ", " especially ")  # hypernym → list
_TRIGGERS_LH = (", and other ", " and other ", ", or other ", " or other ")  # list → hypernym
_NP = r"([A-Za-z][\w ’'\-]{2,45})"
_FLAT_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(_NP + r"\s+such as\s+(.+?)(?:[.;]|$)", re.I), "H_LIST"),
    (re.compile(r"such\s+" + _NP + r"\s+as\s+(.+?)(?:[.;]|$)", re.I), "H_LIST"),
    (re.compile(_NP + r"\s+including\s+(.+?)(?:[.;]|$)", re.I), "H_LIST"),
    (re.compile(_NP + r"\s*,?\s+especially\s+(.+?)(?:[.;]|$)", re.I), "H_LIST"),
    (re.compile(r"(.+?)\s*,?\s+and other\s+" + _NP, re.I), "LIST_H"),
    (re.compile(r"(.+?)\s*,?\s+or other\s+" + _NP, re.I), "LIST_H"),
]


# A noun phrase ends at the first clause-boundary word; cut there so a trailing prepositional /
# verb phrase ("SAML for service calls", "protocols are common") does not pollute the head.
_CLAUSE_CUT = re.compile(r"\b(for|to|in|on|of|that|which|are|is|was|were|with|when|by|as|will)\b")


def _np_head(phrase: str, *, lead: bool, n: int = 2) -> str:
    """Head of a noun phrase: cut at the first clause word, then take leading/trailing content words.

    ``lead=True`` (head noun at the front, e.g. a hyponym "SAML for…" → "saml") vs ``lead=False``
    (head at the end, e.g. the "such as" hypernym "an authentication method" → "authentication
    method").
    """
    phrase = _CLAUSE_CUT.split(phrase, maxsplit=1)[0]
    words = [w for w in re.findall(r"[a-z][a-z\-]+", phrase.lower()) if w not in _FUNCTION]
    return " ".join(words[:n] if lead else words[-n:]) if words else ""


def _list_heads(blob: str) -> list[str]:
    return [
        h
        for h in (_np_head(p, lead=True) for p in re.split(r",|\band\b|\bor\b", blob))
        if len(h) > 2
    ]


def _hearst_flat(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for rx, kind in _FLAT_PATTERNS:
        for m in rx.finditer(text):
            if kind == "H_LIST":
                hyper, lst = _np_head(m.group(1), lead=False), m.group(2)
            else:
                lst, hyper = m.group(1), _np_head(m.group(2), lead=True)
            if hyper:
                out += [(hypo, hyper) for hypo in _list_heads(lst) if hypo != hyper]
    return out


@lru_cache(maxsize=1)
def _nlp():  # pragma: no cover - exercised only when spaCy is installed
    import spacy

    return spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])


def _chunk_head(chunk) -> str:  # pragma: no cover - spaCy path
    words = [t.text.lower() for t in chunk if t.text.lower() not in _FUNCTION and t.is_alpha]
    return " ".join(words[-2:]) if words else ""


def _hearst_spacy(text: str) -> list[tuple[str, str]]:  # pragma: no cover - spaCy path
    """Hearst via spaCy: snap hypernym/hyponym spans to noun-chunk boundaries around each trigger."""
    out: list[tuple[str, str]] = []
    doc = _nlp()(text)
    for sent in doc.sents:
        chunks = list(sent.noun_chunks)
        if not chunks:
            continue
        low = sent.text.lower()
        for trig in _TRIGGERS_HL:
            i = low.find(trig)
            if i < 0:
                continue
            cut = sent.start_char + i
            before = [c for c in chunks if c.end_char <= cut]
            after = [c for c in chunks if c.start_char >= cut + len(trig)]
            if not before or not after:
                continue
            hyper = _chunk_head(before[-1])
            for c in after:
                hypo = _chunk_head(c)
                if hyper and hypo and hypo != hyper:
                    out.append((hypo, hyper))
        for trig in _TRIGGERS_LH:
            i = low.find(trig)
            if i < 0:
                continue
            cut = sent.start_char + i
            after = [c for c in chunks if c.start_char >= cut + len(trig)]
            before = [c for c in chunks if c.end_char <= cut]
            if not after or not before:
                continue
            hyper = _chunk_head(after[0])
            for c in before:
                hypo = _chunk_head(c)
                if hyper and hypo and hypo != hyper:
                    out.append((hypo, hyper))
    return out


def hearst_pairs(text: str, *, prefer_spacy: bool = True) -> list[tuple[str, str]]:
    """Extract ``(hyponym_head, hypernym_head)`` is-a pairs — spaCy parse if available, else flat."""
    pairs: list[tuple[str, str]] = []
    if prefer_spacy:
        try:
            pairs = _hearst_spacy(text)
        except Exception:
            pairs = []
    if not pairs:
        pairs = _hearst_flat(text)
    return list(dict.fromkeys(pairs))  # dedupe, preserve order


@lru_cache(maxsize=4096)
def wordnet_confirms(hypo: str, hyper: str) -> bool:
    """True if WordNet makes ``hyper`` a (transitive) hypernym of ``hypo`` (nltk). False if absent."""
    try:
        from nltk.corpus import wordnet as wn
    except Exception:
        return False
    hypo_key, hyper_key = hypo.split()[-1], hyper.split()[-1]  # head nouns
    try:
        syns = wn.synsets(hypo_key, pos=wn.NOUN)
    except Exception:
        return False
    targets = {hyper.lower(), hyper_key.lower()}
    for syn in syns:
        for path in syn.hypernym_paths():
            for s in path[:-1]:  # ancestors (exclude the synset itself)
                if targets & {n.lower().replace("_", " ") for n in s.lemma_names()}:
                    return True
    return False


def _content(text: str) -> set[str]:
    return {
        w for w in re.findall(r"[a-z][a-z\-]+", text.lower()) if w not in _FUNCTION and len(w) > 2
    }


def seed_specializes(
    principles: list[dict], *, source_texts: list[str] | None = None, require_wordnet: bool = False
) -> dict:
    """Candidate ``specializes`` edges from Hearst is-a (+ WordNet confidence). Graph-v1 fragment.

    Pairs are mined from ``source_texts`` if given (enumerative prose — the high-yield case), else
    from the principle statements (thin). A principle distinctively about the hyponym specializes the
    principle that enumerates / names the hypernym. WordNet-confirmed pairs are ``confidence: high``;
    ``require_wordnet=True`` keeps only those (high precision, near-zero recall on domain jargon
    WordNet does not cover).

    Precision guards (real factory source prose is noisy + domain-specific): a hyponym head that maps
    to **too many** principles is a common word, not a specializer, and is skipped — this stops the
    edge explosion a generic term like "security" otherwise causes.
    """
    pid_tokens = {p["principle_id"]: _content(str(p.get("statement", ""))) for p in principles}
    corpus = source_texts or [str(p.get("statement", "")) for p in principles]
    max_specs = max(2, len(principles) // 3)  # a real specializer is distinctive, not ubiquitous
    pairs: list[tuple[str, str]] = []
    seen_pair: set[tuple[str, str]] = set()
    for text in corpus:
        for pr in hearst_pairs(text):
            if pr not in seen_pair:
                seen_pair.add(pr)
                pairs.append(pr)

    edges: list[dict] = []
    seen_edge: set[tuple[str, str]] = set()
    for hypo, hyper in pairs:
        confirmed = wordnet_confirms(hypo, hyper)
        if require_wordnet and not confirmed:
            continue
        hypo_w, hyper_w = set(hypo.split()), set(hyper.split())
        specs = [pid for pid, toks in pid_tokens.items() if hypo_w & toks]
        gens = [pid for pid, toks in pid_tokens.items() if hyper_w & toks]
        if len(specs) > max_specs or len(gens) > max_specs:
            continue  # over-common term -> not a real specialiser/category; skip the explosion
        conf = "high" if confirmed else "low"
        for spec in specs:
            for gen in gens:
                if spec != gen and (spec, gen) not in seen_edge:
                    seen_edge.add((spec, gen))
                    edges.append(
                        {
                            "source": spec,
                            "target": gen,
                            "relation": "specializes",
                            "provenance": {
                                "cluster_id": None,
                                "method": "seed",
                                "confidence": conf,
                                # C2 PROV-O: derived from the two principles + the is-a term pair.
                                **prov_record("hearst-isa", [spec, gen, hypo, hyper]),
                            },
                            "note": f"Hearst is-a: '{hypo}' is-a '{hyper}'"
                            + ("; WordNet-confirmed" if conf == "high" else ""),
                        }
                    )
    return {"schema_version": "principle-graph-v1", "edges": edges}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.hearst_isa <subagents/slug> [--sources]")
        sys.exit(1)
    base = Path(sys.argv[1])
    pp = base / "principles" / "principles.yaml"
    principles = (
        (yaml.safe_load(pp.read_text(encoding="utf-8")) or {}).get("principles", [])
        if pp.exists()
        else []
    )
    source_texts = None
    if "--sources" in sys.argv:
        md = base / "sources" / "markdown"
        source_texts = (
            [f.read_text(encoding="utf-8") for f in md.glob("*.md")] if md.exists() else []
        )
    result = seed_specializes(principles, source_texts=source_texts)
    result["subagent_slug"] = base.name
    print(f"C3 Hearst is-a: {len(result['edges'])} candidate specializes edge(s)")
    for e in result["edges"][:20]:
        print(
            f"  {e['source']} specializes {e['target']}  [{e['provenance']['confidence']}] ({e['note']})"
        )


if __name__ == "__main__":
    main()
