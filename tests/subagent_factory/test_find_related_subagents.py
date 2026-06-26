"""Tests for find_related_subagents."""

import tempfile
from pathlib import Path

import yaml

from tools.subagent_factory.find_related_subagents import (
    _build_profile_corpus,
    _jaccard,
    _query_coverage,
    _tokenize,
    extract_domain_keywords,
    find_related_subagents,
)

# ── unit ───────────────────────────────────────────────────────────────────


def test_jaccard_identical():
    a = {"api", "security", "reviewer"}
    assert _jaccard(a, a) == 1.0


def test_jaccard_disjoint():
    assert _jaccard({"api", "security"}, {"database", "schema"}) == 0.0


def test_jaccard_partial():
    a = {"api", "security", "reviewer"}
    b = {"api", "security", "database"}
    assert 0 < _jaccard(a, b) < 1.0


def test_tokenize_strips_stop_words():
    tokens = _tokenize("The API and the security of a system")
    assert "the" not in tokens
    assert "and" not in tokens
    assert "api" in tokens
    assert "security" in tokens


def test_build_profile_corpus_uses_all_fields():
    profile = {
        "display_name": "API Security Auditor",
        "role": "Audits API authentication",
        "when_to_use": ["API exposes sensitive data"],
        "quality_bar": ["Every finding cites evidence"],
        "knowledge_partition": {"always_on": ["OAuth 2.0 flows"]},
        "sources": [{"title": "OWASP API Security Top 10"}],
    }
    tokens = _build_profile_corpus(profile)
    assert "auditor" in tokens
    assert "authentication" in tokens
    assert "owasp" in tokens
    assert "oauth" in tokens


# ── domain keyword extraction ─────────────────────────────────────────────


def test_extract_domain_keywords_returns_terms():
    sample = {
        "headings": [
            "The Nature of Complexity",
            "Information Hiding",
            "Deep Modules",
            "Shallow Modules",
            "Abstractions",
        ],
        "body_excerpt": "Complexity is anything that makes software hard to understand "
        "or modify. Abstraction hides implementation details. "
        "Modules should expose simple interfaces.",
        "toc_entries": [],
        "file_hint": "A Philosophy Of Software Design",
    }
    keywords = extract_domain_keywords(sample)
    assert isinstance(keywords, list)
    assert len(keywords) > 5
    # Domain terms should appear
    joined = " ".join(keywords)
    assert "complexity" in joined or "abstraction" in joined or "modules" in joined


# ── integration: search ───────────────────────────────────────────────────


def test_no_subagents_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        assert find_related_subagents("api security", subagents_dir=tmp) == []


def test_finds_match_with_keywords():
    with tempfile.TemporaryDirectory() as tmp:
        slug_dir = Path(tmp) / "software-design-reviewer"
        slug_dir.mkdir()
        profile = {
            "slug": "software-design-reviewer",
            "display_name": "Software Design Reviewer",
            "role": "Reviews software design for complexity and abstraction quality",
            "when_to_use": [
                "Code review needs design-level feedback",
                "Module interfaces need evaluation",
            ],
            "quality_bar": ["Every finding cites evidence"],
            "knowledge_partition": {
                "always_on": ["deep modules", "information hiding", "abstraction layers"]
            },
            "sources": [{"title": "A Philosophy of Software Design"}],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        # Topic alone (low lexical overlap with profile prose)
        results_topic_only = find_related_subagents("software design reviewer", subagents_dir=tmp)
        # Topic + domain keywords (richer overlap)
        results_with_keywords = find_related_subagents(
            "software design reviewer",
            domain_keywords=[
                "complexity",
                "abstraction",
                "modules",
                "interfaces",
                "information",
                "hiding",
            ],
            subagents_dir=tmp,
        )

        assert len(results_with_keywords) > 0
        assert results_with_keywords[0]["slug"] == "software-design-reviewer"
        # Keywords should improve similarity
        if results_topic_only:
            assert results_with_keywords[0]["similarity"] >= results_topic_only[0]["similarity"]


def test_recommendation_thresholds():
    with tempfile.TemporaryDirectory() as tmp:
        # Build a profile that will score very high against this query
        slug_dir = Path(tmp) / "test-reviewer"
        slug_dir.mkdir()
        # Mirror the query tokens heavily in the profile
        profile = {
            "slug": "test-reviewer",
            "display_name": "complexity abstraction reviewer",
            "role": "complexity abstraction reviewer modules interfaces",
            "when_to_use": ["complexity abstraction reviewer modules"],
            "quality_bar": [],
            "knowledge_partition": {"always_on": ["complexity abstraction modules"]},
            "sources": [],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        results = find_related_subagents(
            "complexity abstraction reviewer modules interfaces",
            subagents_dir=tmp,
        )
        assert len(results) > 0
        top = results[0]
        # With heavy overlap, should recommend update
        assert top["recommendation"] in ("update", "consider-update")


def test_query_coverage_covers_small_query_in_large_corpus():
    query = {"concurrency", "threads", "locks"}
    corpus = query | {f"filler{i}" for i in range(200)}
    # Query is fully covered → coverage 1.0, while Jaccard collapses to ~0.015.
    assert _query_coverage(query, corpus) == 1.0
    assert _jaccard(query, corpus) < 0.1


def test_small_query_large_corpus_reaches_update_threshold():
    # Regression: with Jaccard this scored ~0.05 and was filtered out, so the
    # Phase 7 update path was unreachable. Overlap coefficient must surface it.
    with tempfile.TemporaryDirectory() as tmp:
        slug_dir = Path(tmp) / "java-concurrency-reviewer"
        slug_dir.mkdir()
        filler = [f"unrelated filler clause number {i} alpha beta gamma delta" for i in range(40)]
        profile = {
            "slug": "java-concurrency-reviewer",
            "display_name": "Java Concurrency Reviewer",
            "role": "Reviews Java concurrent code for safety liveness and performance "
            "using synchronization locks monitor atomicity visibility threads deadlock",
            "when_to_use": ["synchronized code needs a deadlock and race audit"],
            "knowledge_partition": {"always_on": filler},
            "sources": [{"title": "Concurrent Programming in Java"}],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        results = find_related_subagents(
            "Java concurrency reviewer",
            domain_keywords=[
                "concurrency",
                "threads",
                "synchronization",
                "locks",
                "deadlock",
                "safety",
                "liveness",
                "monitor",
                "atomicity",
                "visibility",
            ],
            subagents_dir=tmp,
        )
        assert len(results) == 1
        top = results[0]
        assert top["slug"] == "java-concurrency-reviewer"
        assert top["similarity"] >= 0.55
        assert top["recommendation"] in ("update", "consider-update")


def test_overlap_coefficient_uses_query_denominator_not_min():
    # Coverage-of-query intent: a thin corpus SMALLER than the query must not
    # score 1.0 just because it is fully contained. Under min(|A|,|B|) this
    # scored 1.0 (corpus is the smaller set); under query-coverage it is 1/5.
    query = {"complexity", "abstraction", "modules", "interfaces", "hiding"}
    thin_corpus = {"complexity"}
    assert _query_coverage(query, thin_corpus) == 0.2


def test_thin_corpus_does_not_wrongly_recommend_update():
    # A stub profile with one matching token must not be promoted to "update"
    # against a richer query. Under the buggy min-denominator it scored 1.0.
    with tempfile.TemporaryDirectory() as tmp:
        slug_dir = Path(tmp) / "stub-reviewer"
        slug_dir.mkdir()
        profile = {
            "slug": "stub-reviewer",
            "display_name": "complexity",
            "role": "",
            "when_to_use": [],
            "sources": [],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        results = find_related_subagents(
            "complexity abstraction modules interfaces hiding",
            subagents_dir=tmp,
        )
        # 1 of 5 query tokens covered → 0.2, below the 0.10 floor it survives
        # but must never be "update" or "consider-update".
        assert len(results) == 1
        assert results[0]["similarity"] == 0.2
        assert results[0]["recommendation"] == "create-new"


def test_malformed_profile_is_surfaced_not_silently_dropped():
    # A dropped candidate can flip the verdict to "create-new" and cause a
    # duplicate subagent, so a skipped/unreadable profile must be surfaced.
    import io
    from contextlib import redirect_stderr

    with tempfile.TemporaryDirectory() as tmp:
        good_dir = Path(tmp) / "good-reviewer"
        good_dir.mkdir()
        (good_dir / "profile.yaml").write_text(
            yaml.dump(
                {
                    "slug": "good-reviewer",
                    "display_name": "API Security Reviewer",
                    "role": "Reviews API security",
                }
            )
        )

        bad_dir = Path(tmp) / "broken-reviewer"
        bad_dir.mkdir()
        # Invalid YAML that yaml.safe_load cannot parse.
        (bad_dir / "profile.yaml").write_text("display_name: [unclosed\n  : :")

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            results = find_related_subagents("api security reviewer", subagents_dir=tmp)

        # Good profile still found.
        assert any(r["slug"] == "good-reviewer" for r in results)
        # The skip is surfaced on stderr (not silently swallowed).
        assert "broken-reviewer" in stderr.getvalue()


def test_matched_terms_returned():
    with tempfile.TemporaryDirectory() as tmp:
        slug_dir = Path(tmp) / "security-reviewer"
        slug_dir.mkdir()
        profile = {
            "slug": "security-reviewer",
            "display_name": "API Security Reviewer",
            "role": "Reviews API security and authentication",
            "when_to_use": [],
            "sources": [],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        results = find_related_subagents("api security reviewer", subagents_dir=tmp)
        assert len(results) > 0
        assert "matched_terms" in results[0]
        assert isinstance(results[0]["matched_terms"], list)
