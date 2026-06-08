"""Tests for find_related_subagents."""

import tempfile
from pathlib import Path

import yaml

from tools.subagent_factory.find_related_subagents import find_related_subagents, _jaccard, _tokenize


def test_jaccard_identical():
    a = {"api", "security", "reviewer"}
    assert _jaccard(a, a) == 1.0


def test_jaccard_disjoint():
    a = {"api", "security"}
    b = {"database", "schema"}
    assert _jaccard(a, b) == 0.0


def test_jaccard_partial():
    a = {"api", "security", "reviewer"}
    b = {"api", "security", "database"}
    assert 0 < _jaccard(a, b) < 1.0


def test_tokenize():
    tokens = _tokenize("API Security Reviewer")
    assert "api" in tokens
    assert "security" in tokens
    assert "reviewer" in tokens


def test_no_subagents_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        result = find_related_subagents("api security", tmp)
        assert result == []


def test_finds_high_similarity():
    with tempfile.TemporaryDirectory() as tmp:
        slug_dir = Path(tmp) / "api-security-reviewer"
        slug_dir.mkdir()
        # Minimal corpus so Jaccard stays high: same 3 core tokens, minimal extras
        profile = {
            "slug": "api-security-reviewer",
            "display_name": "API Security Reviewer",
            "role": "API security reviewer",
            "when_to_use": ["API security reviewer needed"],
            "sources": [],
        }
        (slug_dir / "profile.yaml").write_text(yaml.dump(profile))

        results = find_related_subagents("api security reviewer", tmp)
        assert len(results) > 0
        assert results[0]["slug"] == "api-security-reviewer"
        # With focused corpus, similarity should be high
        assert results[0]["similarity"] >= 0.55
