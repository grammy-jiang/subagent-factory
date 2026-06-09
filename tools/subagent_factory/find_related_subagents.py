"""
Search existing subagent packages for content similarity.

Query is built from TWO sources:
  topic          — inferred expert role string (e.g. "software design reviewer")
  domain_keywords — key domain terms extracted from content sample headings/body
                   (e.g. ["complexity", "abstraction", "modules", "interfaces"])

Both are tokenized and combined into one query set, then scored by overlap
coefficient (query coverage) against each profile's corpus. Each existing
subagent's profile is compared against the full query: display_name, role,
when_to_use, forbidden_behaviours, source titles, knowledge_partition always_on.

Overlap coefficient — not Jaccard — is used deliberately: the query (~15 tokens)
is tiny next to a profile corpus (hundreds of tokens), so symmetric Jaccard
(|A∩B|/|A∪B|) collapses toward zero even for a strong topical match and can never
reach the 0.55/0.80 routing thresholds.
"""

import re
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).parent.parent.parent


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
      "update"          — similarity >= 0.80  (default: update this subagent)
      "consider-update" — 0.55 <= sim < 0.80  (ask user)
      "create-new"      — sim < 0.55          (default: create new)
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
            with open(profile_path) as f:
                profile = yaml.safe_load(f) or {}
        except Exception:
            continue

        slug = profile.get("slug") or profile_path.parent.name
        corpus_tokens, corpus_text = _build_profile_corpus(profile)

        sim = _overlap_coefficient(query_tokens, corpus_tokens)
        matched = sorted(query_tokens & corpus_tokens)

        rec = "create-new"
        if sim >= 0.80:
            rec = "update"
        elif sim >= 0.55:
            rec = "consider-update"

        candidates.append(
            {
                "slug": slug,
                "profile_path": str(profile_path),
                "display_name": profile.get("display_name", slug),
                "role": profile.get("role", "")[:120],
                "similarity": round(sim, 3),
                "recommendation": rec,
                "matched_terms": matched[:15],
            }
        )

    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    return [c for c in candidates if c["similarity"] >= 0.10]


def _build_profile_corpus(profile: dict) -> tuple[set[str], str]:
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
    return _tokenize(text), text


def extract_domain_keywords(sample: dict, max_keywords: int = 40) -> list[str]:
    """
    Extract domain-specific keywords from a content sample dict
    (as returned by detect_topic.extract_content_sample).

    Returns list of meaningful single terms, suitable for passing to
    find_related_subagents() as domain_keywords.
    """
    text_parts = sample.get("headings", []) + [sample.get("body_excerpt", "")]
    text = " ".join(str(p) for p in text_parts)

    all_tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9]*", text)
    freq: dict[str, int] = {}
    for tok in all_tokens:
        t = tok.lower()
        if len(t) > 3 and t not in _STOP_WORDS:
            freq[t] = freq.get(t, 0) + 1

    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in ranked[:max_keywords]]


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in tokens if t not in _STOP_WORDS and len(t) > 2}


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union > 0 else 0.0


def _overlap_coefficient(a: set, b: set) -> float:
    """Szymkiewicz-Simpson overlap: |A∩B| / min(|A|, |B|).

    Fraction of the smaller set (the query) covered by the larger (the profile
    corpus). Used instead of Jaccard so a small query can still score high
    against a large profile when the topic genuinely matches.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


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
