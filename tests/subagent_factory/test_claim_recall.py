"""Tests for the deterministic claim-recall harness (Step 10 G3, no-ML complement)."""

import subprocess
import sys

import pytest
import yaml

from tools.subagent_factory import claim_recall as cr
from tools.subagent_factory.claim_recall import (
    STOPWORDS,
    claim_f1,
    claim_recall,
    content_tokens,
    load_statements,
)


def test_f1_identical_is_one():
    assert claim_f1("cache invalidation is hard", "cache invalidation is hard") == 1.0


def test_f1_disjoint_is_zero():
    assert claim_f1("redis cluster sharding", "negotiation tactical empathy") == 0.0


def test_f1_partial_is_between():
    s = claim_f1(
        "use a write-through cache for consistency",
        "a write-through cache improves consistency",
    )
    assert 0.0 < s < 1.0


def test_recall_full_when_candidate_covers():
    ref = ["write-through cache keeps data consistent", "ttl expiry bounds staleness"]
    cand = [*ref, "an extra unrelated note about migratory birds"]
    r = claim_recall(ref, cand, threshold=0.5)
    assert r["recall"] == 1.0 and r["n_matched"] == 2


def test_recall_partial_lists_unmatched():
    ref = ["redis sorted sets rank leaderboards", "pipelining reduces network round trips"]
    cand = ["redis sorted sets rank leaderboards"]
    r = claim_recall(ref, cand)
    assert r["recall"] == 0.5
    assert any("pipelining" in m for m in r["unmatched_reference"])


def test_precision_flags_noise_candidate():
    ref = ["cache aside pattern loads data on a miss"]
    cand = ["cache aside pattern loads data on a miss", "totally unrelated llamas graze meadows"]
    r = claim_recall(ref, cand)
    assert r["recall"] == 1.0 and r["precision"] == 0.5


def test_empty_inputs_are_zero():
    assert claim_recall([], [])["recall"] == 0.0
    assert claim_recall(["a real claim here"], [])["recall"] == 0.0


def test_load_statements_jsonl(tmp_path):
    f = tmp_path / "c.jsonl"
    f.write_text('{"statement": "alpha claim"}\n\n{"statement": "beta claim"}\n', encoding="utf-8")
    assert load_statements(f) == ["alpha claim", "beta claim"]


def test_load_statements_source_map(tmp_path):
    f = tmp_path / "m.source-map.yaml"
    f.write_text(
        yaml.safe_dump({"candidate_units": [{"statement": "unit one"}, {"statement": "unit two"}]}),
        encoding="utf-8",
    )
    assert load_statements(f) == ["unit one", "unit two"]


# --- Finding 1: shared tokenizer is a PUBLIC contract -----------------------------------------


def test_public_names_are_exported():
    """The tokenizer is a load-bearing contract imported by 7 modules; it must be public."""
    assert callable(content_tokens)
    assert isinstance(STOPWORDS, (set, frozenset))


def test_private_aliases_are_the_public_names():
    """Backward-compat aliases keep the 7 existing importers working without edits."""
    assert cr._content_tokens is cr.content_tokens
    assert cr._STOPWORDS is cr.STOPWORDS


def test_content_tokens_drops_stopwords_and_short_tokens():
    toks = content_tokens("The cache invalidation IS hard to do")
    assert "cache" in toks and "invalidation" in toks and "hard" in toks
    assert "the" not in toks  # stopword
    assert "is" not in toks  # stopword
    assert "to" not in toks  # stopword + length<=2


# --- Finding 2: recall matching semantics (per-reference independent matching) -----------------


def test_one_candidate_recalls_multiple_references():
    """Documented semantics: a reference is recalled if ANY candidate clears threshold; the same
    candidate may recall several references. ref=[a, b], cand=[c] where c matches both => recall 1.0."""
    ref = [
        "write-through cache keeps stored data consistent",
        "write-through cache keeps data consistent on stores",
    ]
    cand = ["write-through cache keeps data consistent"]
    # The single candidate clears threshold against BOTH references.
    assert claim_f1(cand[0], ref[0]) >= 0.5
    assert claim_f1(cand[0], ref[1]) >= 0.5
    r = claim_recall(ref, cand, threshold=0.5)
    assert r["recall"] == 1.0
    assert r["n_matched"] == 2
    assert r["precision"] == 1.0  # the lone candidate is on-topic, not noise


# --- Finding 3: CLI threshold validation -------------------------------------------------------


def _run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "tools.subagent_factory.claim_recall", *args],
        capture_output=True,
        text=True,
    )


def test_cli_non_numeric_threshold_shows_usage(tmp_path):
    f = tmp_path / "c.jsonl"
    f.write_text('{"statement": "alpha claim"}\n', encoding="utf-8")
    res = _run_cli(str(f), str(f), "notanumber")
    assert res.returncode != 0
    assert "Usage:" in (res.stdout + res.stderr)
    assert "Traceback" not in res.stderr


@pytest.mark.parametrize("bad", ["5.0", "-1"])
def test_cli_out_of_range_threshold_rejected(tmp_path, bad):
    f = tmp_path / "c.jsonl"
    f.write_text('{"statement": "alpha claim"}\n', encoding="utf-8")
    res = _run_cli(str(f), str(f), bad)
    assert res.returncode != 0
    assert "Usage:" in (res.stdout + res.stderr)
    assert "Traceback" not in res.stderr
