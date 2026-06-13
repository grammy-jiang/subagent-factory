"""Tests for the deterministic cross-source principle-cluster seeder (Step 7 Phase A)."""

import json

import yaml

from tools.subagent_factory.seed_principle_clusters import seed_clusters

_OVERLAP = "deep modules reduce complexity through information hiding"


def _pkg(tmp_path, principles, claims):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "analysis").mkdir(parents=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c) for c in claims) + "\n", encoding="utf-8"
    )
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    return base


def test_seeds_cross_source_cluster(tmp_path):
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
        {"claim_id": "c3", "source_id": "bookA", "statement": "z"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": _OVERLAP,
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": _OVERLAP + " always",
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
        {
            "principle_id": "P3",
            "statement": "prefer cats over dogs in quiet gardens",
            "derived_from_claims": ["c3"],
            "confidence": "high",
        },
    ]
    r = seed_clusters(_pkg(tmp_path, principles, claims), 0.15)
    assert len(r["clusters"]) == 1
    c = r["clusters"][0]
    assert set(c["member_principle_ids"]) == {"P1", "P2"}
    assert set(c["sources"]) == {"bookA", "bookB"}
    assert c["method"] == "seed" and c["canonical_statement"] is None


def test_same_source_not_clustered(tmp_path):
    # identical statements but BOTH from one source → not cross-source → no cluster.
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookA", "statement": "y"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": _OVERLAP,
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": _OVERLAP,
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
    ]
    assert seed_clusters(_pkg(tmp_path, principles, claims), 0.15)["clusters"] == []


def test_below_threshold_no_cluster(tmp_path):
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": "deep modules hide implementation complexity",
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": "prefer cats over dogs in gardens",
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
    ]
    assert seed_clusters(_pkg(tmp_path, principles, claims), 0.5)["clusters"] == []
