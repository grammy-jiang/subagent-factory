"""Tests for C3 Hearst is-a extraction + specializes seeding.

The flat-regex path runs everywhere (CI-safe). The spaCy parse path and the WordNet (nltk) path are
skip-guarded so the suite never needs the optional `nlp` extra on CI.
"""

import pytest

from tools.subagent_factory.hearst_isa import (
    _hearst_flat,
    hearst_pairs,
    seed_specializes,
    wordnet_confirms,
)

# ---- flat extractor (always) ----------------------------------------------------------------


def test_flat_such_as():
    pairs = _hearst_flat("Use an authentication method such as OAuth and SAML for service calls")
    hypos = {h for h, _ in pairs}
    assert "oauth" in hypos and "saml" in hypos
    assert all(hyper.endswith("method") for _, hyper in pairs)


def test_flat_and_other():
    pairs = _hearst_flat("OAuth and other delegation protocols are common")
    assert ("oauth", "delegation protocols") in pairs or ("oauth", "protocols") in pairs


def test_hearst_pairs_falls_back_to_flat_when_spacy_off():
    pairs = hearst_pairs("metrics such as latency and throughput", prefer_spacy=False)
    assert ("latency", _hearst_flat("metrics such as latency")[0][1]) in pairs


def test_hearst_pairs_dedupes():
    txt = "tools such as ruff; linters such as ruff"
    assert len(hearst_pairs(txt, prefer_spacy=False)) == len(
        set(hearst_pairs(txt, prefer_spacy=False))
    )


# ---- seed_specializes (flat-backed, env-agnostic) -------------------------------------------


def test_seed_specializes_links_hyponym_principle_to_enumerator():
    principles = [
        {"principle_id": "P1", "statement": "Use an authentication method such as OAuth for calls"},
        {"principle_id": "P2", "statement": "Configure OAuth tokens carefully for delegation"},
        {"principle_id": "P3", "statement": "Prefer cats over dogs in quiet gardens"},
    ]
    edges = seed_specializes(principles)["edges"]
    e = {(x["source"], x["target"], x["relation"]) for x in edges}
    assert ("P2", "P1", "specializes") in e  # P2 (about OAuth) specializes P1 (enumerates it)
    assert all(x["target"] != "P3" and x["source"] != "P3" for x in edges)  # unrelated untouched
    assert all(x["provenance"]["method"] == "seed" for x in edges)


def test_seed_specializes_empty_when_no_enumeration():
    principles = [
        {"principle_id": "P1", "statement": "Keep modules small and focused"},
        {"principle_id": "P2", "statement": "Write clear comments"},
    ]
    assert seed_specializes(principles)["edges"] == []


# ---- spaCy parse path (skip-guarded) --------------------------------------------------------


def test_spacy_hearst_extracts_clean_heads():
    pytest.importorskip("spacy")
    try:
        from tools.subagent_factory.hearst_isa import _nlp

        _nlp()
    except Exception:
        pytest.skip("en_core_web_sm not available")
    pairs = hearst_pairs("Several authentication methods, such as OAuth and SAML, are supported.")
    hypos = {h for h, _ in pairs}
    assert "oauth" in hypos and "saml" in hypos


# ---- WordNet hybrid (skip-guarded) ----------------------------------------------------------


def test_wordnet_confirms_general_isa():
    wn = pytest.importorskip("nltk.corpus").wordnet
    try:
        wn.synsets("dog")
    except LookupError:
        pytest.skip("WordNet data not downloaded")
    assert wordnet_confirms("dog", "animal") is True
    assert wordnet_confirms("dog", "vehicle") is False
