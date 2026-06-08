"""Search existing subagent packages for topic similarity."""

import re
from pathlib import Path

import yaml


_REPO_ROOT = Path(__file__).parent.parent.parent


def find_related_subagents(topic: str, subagents_dir: str | Path | None = None) -> list[dict]:
    """
    Search subagents/<slug>/profile.yaml for candidates related to topic.

    Returns list of dicts: slug, similarity, display_name, role, recommendation
      recommendation: "update" | "consider-update" | "create-new"
    """
    base = Path(subagents_dir) if subagents_dir else _REPO_ROOT / "subagents"
    if not base.exists():
        return []

    candidates = []
    topic_tokens = _tokenize(topic)

    for profile_path in base.glob("*/profile.yaml"):
        try:
            with open(profile_path) as f:
                profile = yaml.safe_load(f) or {}
        except Exception:
            continue

        slug = profile.get("slug") or profile_path.parent.name
        display_name = profile.get("display_name", slug)
        role = profile.get("role", "")
        when_to_use = profile.get("when_to_use", [])
        sources = profile.get("sources", [])
        source_titles = [s.get("title", "") for s in sources]

        corpus = " ".join([display_name, role] + when_to_use + source_titles)
        corpus_tokens = _tokenize(corpus)

        sim = _jaccard(topic_tokens, corpus_tokens)

        rec = "create-new"
        if sim >= 0.80:
            rec = "update"
        elif sim >= 0.55:
            rec = "consider-update"

        candidates.append({
            "slug": slug,
            "profile_path": str(profile_path),
            "display_name": display_name,
            "role": role[:120],
            "similarity": round(sim, 3),
            "recommendation": rec,
        })

    candidates.sort(key=lambda x: x["similarity"], reverse=True)
    return [c for c in candidates if c["similarity"] >= 0.15]


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"a", "an", "the", "and", "or", "of", "in", "to", "for", "is", "are", "be", "that", "this"}
    return {t for t in tokens if t not in stop and len(t) > 2}


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union > 0 else 0.0
