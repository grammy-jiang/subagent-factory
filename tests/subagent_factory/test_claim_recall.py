"""Tests for the deterministic claim-recall harness (Step 10 G3, no-ML complement)."""

import yaml

from tools.subagent_factory.claim_recall import claim_f1, claim_recall, load_statements


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
