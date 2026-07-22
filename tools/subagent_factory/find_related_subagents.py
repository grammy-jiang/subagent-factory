"""
Search existing subagent packages for content similarity.

Query is built from TWO sources:
  topic          — inferred expert role string (e.g. "software design reviewer")
  domain_keywords — key domain terms extracted from content sample headings/body
                   (e.g. ["complexity", "abstraction", "modules", "interfaces"])

Both are tokenized and combined into one query set, then scored by the
fraction of the query covered by each profile's corpus (|query ∩ corpus| /
|query|). Each existing subagent's profile is compared against the full query:
display_name, role, when_to_use, forbidden_behaviours, source titles,
knowledge_partition always_on.

Query-coverage — not symmetric Jaccard — is used deliberately: the query
(~15 tokens) is tiny next to a profile corpus (hundreds of tokens), so symmetric
Jaccard (|A∩B|/|A∪B|) collapses toward zero even for a strong topical match and
can never reach the 0.55/0.80 routing thresholds. The denominator is the query
token count (not min(|query|,|corpus|)) so a sparse/stub profile that happens to
be smaller than the query cannot score a misleading 1.0.

Results below ``_DROP_BELOW`` (0.10) are dropped from the returned list: such a
weak lexical overlap is noise, not a candidate worth showing to the routing step.
Recommendation bands: similarity >= ``_UPDATE`` (0.80) → "update";
>= ``_CONSIDER`` (0.55) → "consider-update"; otherwise "create-new".
"""

import re
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).parent.parent.parent

# Routing thresholds and result floor (documented in the module docstring).
_DROP_BELOW = 0.10  # similarity below this is noise; drop from results
_CONSIDER = 0.55  # >= this → "consider-update" (ask the user)
_UPDATE = 0.80  # >= this → "update" (default: update this subagent)

# Output truncations.
_ROLE_MAX_CHARS = 120  # role string truncated for display
_MATCHED_TERMS_MAX = 15  # matched terms truncated for display


def find_related_subagents(
    topic: str,
    domain_keywords: list[str] | None = None,
    subagents_dir: str | Path | None = None,
) -> list[dict]:
    """
    Search subagents/<slug>/profile.yaml for candidates related to topic + keywords.

    Returns list sorted by similarity desc:
      slug, similarity, display_name, role, recommendation, matched_terms

    recommendation:
      "update"          — similarity >= _UPDATE (0.80)   (default: update this subagent)
      "consider-update" — _CONSIDER <= sim < _UPDATE      (ask user)
      "create-new"      — sim < _CONSIDER (0.55)          (default: create new)

    Profiles that cannot be read or parsed are skipped and a warning naming the
    path is written to stderr — a silently dropped candidate can flip the verdict
    to "create-new" and cause a duplicate subagent.
    """
    base = Path(subagents_dir) if subagents_dir else _REPO_ROOT / "subagents"
    if not base.exists():
        return []

    # Build query token set from topic + domain keywords
    query_tokens = _tokenize(topic)
    for kw in domain_keywords or []:
        query_tokens |= _tokenize(kw)

    if not query_tokens:
        return []

    candidates = []

    for profile_path in base.glob("*/profile.yaml"):
        try:
            with open(profile_path, encoding="utf-8") as f:
                profile = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError) as exc:
            # Surface the skip: a silently dropped candidate can flip the
            # verdict to "create-new" and cause a duplicate subagent.
            print(
                f"find_related_subagents: skipped unreadable profile {profile_path}: {exc}",
                file=sys.stderr,
            )
            continue

        slug = profile.get("slug") or profile_path.parent.name
        corpus_tokens = _build_profile_corpus(profile)

        sim = _query_coverage(query_tokens, corpus_tokens)
        matched = sorted(query_tokens & corpus_tokens)

        rec = "create-new"
        if sim >= _UPDATE:
            rec = "update"
        elif sim >= _CONSIDER:
            rec = "consider-update"

        candidates.append(
            {
                "slug": slug,
                "profile_path": str(profile_path),
                "display_name": profile.get("display_name", slug),
                "role": profile.get("role", "")[:_ROLE_MAX_CHARS],
                "similarity": round(sim, 3),
                "recommendation": rec,
                "matched_terms": matched[:_MATCHED_TERMS_MAX],
            }
        )

    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    return [c for c in candidates if c["similarity"] >= _DROP_BELOW]


def _build_profile_corpus(profile: dict) -> set[str]:
    """Build a rich token set from all meaningful profile fields."""
    parts = [
        profile.get("display_name", ""),
        profile.get("role", ""),
    ]
    parts += profile.get("when_to_use", [])
    parts += profile.get("when_not_to_use", [])
    parts += profile.get("quality_bar", [])
    parts += profile.get("forbidden_behaviours", [])

    kp = profile.get("knowledge_partition", {})
    parts += kp.get("always_on", [])
    parts += kp.get("skills", [])
    parts += kp.get("references", [])

    for source in profile.get("sources", []):
        parts.append(source.get("title", ""))

    text = " ".join(str(p) for p in parts if p)
    return _tokenize(text)


def extract_domain_keywords(sample: dict, max_keywords: int = 40) -> list[str]:
    """
    Extract domain-specific keywords from a content sample dict
    (as returned by detect_topic.extract_content_sample).

    Returns list of meaningful single terms, suitable for passing to
    find_related_subagents() as domain_keywords.
    """
    text_parts = sample.get("headings", []) + [sample.get("body_excerpt", "")]
    text = " ".join(str(p) for p in text_parts)

    # Build the frequency map over _terms() so the "meaningful term" rule
    # (regex + length + stop-word filter) lives in exactly one place.
    freq: dict[str, int] = {}
    for t in _terms(text):
        freq[t] = freq.get(t, 0) + 1

    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in ranked[:max_keywords]]


def _terms(text: str) -> list[str]:
    """Yield meaningful terms from text, in order, with duplicates kept.

    Single definition of "meaningful term": lowercase [a-z0-9]+ runs longer
    than two characters that are not stop words. Both _tokenize (set) and
    extract_domain_keywords (frequency map) build on this.
    """
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]


def _tokenize(text: str) -> set[str]:
    return set(_terms(text))


def _jaccard(a: set, b: set) -> float:
    # Retained only as the documented baseline for the query-coverage choice
    # (see module docstring); not used in production, exercised by tests.
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union > 0 else 0.0


def _query_coverage(query: set, corpus: set) -> float:
    """Fraction of the query covered by the corpus: |query ∩ corpus| / |query|.

    Denominator is the query token count (the documented "coverage of query"
    intent), NOT min(|query|,|corpus|): a sparse/stub profile that happens to be
    smaller than the query must not score a misleading 1.0.
    """
    if not query or not corpus:
        return 0.0
    return len(query & corpus) / len(query)


_STOP_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "of",
    "in",
    "to",
    "for",
    "is",
    "are",
    "be",
    "that",
    "this",
    "it",
    "its",
    "with",
    "from",
    "by",
    "as",
    "on",
    "at",
    "not",
    "but",
    "if",
    "was",
    "has",
    "have",
    "had",
    "will",
    "would",
    "can",
    "could",
    "should",
    "may",
    "might",
    "must",
    "than",
    "then",
    "when",
    "which",
    "who",
    "what",
    "how",
    "all",
    "any",
    "both",
    "each",
    "more",
    "also",
    "into",
    "about",
    "after",
    "before",
    "between",
    "such",
    "these",
    "those",
    "there",
    "their",
    "them",
    "they",
    "been",
    "being",
    "chapter",
    "section",
    "figure",
    "table",
    "page",
    "see",
    "note",
    "example",
}
