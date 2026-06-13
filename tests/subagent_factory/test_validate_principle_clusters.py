"""Tests for the principle-clusters validator (Step 7 Phase A)."""

import json

import yaml

from tools.subagent_factory.validate_principle_clusters import validate_principle_clusters

_GOOD = {
    "cluster_id": "pc000",
    "member_principle_ids": ["P1", "P2"],
    "sources": ["bookA", "bookB"],
    "method": "seed",
    "canonical_statement": None,
}


def _cl(tmp_path, clusters, pids=("P1", "P2", "P3")):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {
                        "principle_id": p,
                        "statement": "s",
                        "derived_from_claims": ["c"],
                        "confidence": "high",
                    }
                    for p in pids
                ],
            }
        ),
        encoding="utf-8",
    )
    f = base / "principles" / "principle-clusters.json"
    f.write_text(
        json.dumps(
            {"schema_version": "principle-clusters-v1", "subagent_slug": "d", "clusters": clusters}
        ),
        encoding="utf-8",
    )
    return f


def test_valid(tmp_path):
    assert validate_principle_clusters(_cl(tmp_path, [_GOOD])) == []


def test_dangling_principle_id(tmp_path):
    bad = {**_GOOD, "member_principle_ids": ["P1", "GHOST"]}
    assert any("not in principles" in e for e in validate_principle_clusters(_cl(tmp_path, [bad])))


def test_overlapping_clusters_fail(tmp_path):
    cls = [
        _GOOD,
        {
            "cluster_id": "pc001",
            "member_principle_ids": ["P2", "P3"],
            "sources": ["bookA", "bookB"],
            "method": "seed",
        },
    ]
    assert any("already in cluster" in e for e in validate_principle_clusters(_cl(tmp_path, cls)))


def test_single_source_cluster_fails(tmp_path):
    bad = {**_GOOD, "sources": ["bookA"]}
    assert any(">= 2 sources" in e for e in validate_principle_clusters(_cl(tmp_path, [bad])))


def test_llm_confirmed_requires_canonical(tmp_path):
    bad = {**_GOOD, "method": "llm-confirmed", "canonical_statement": ""}
    assert any(
        "canonical_statement" in e for e in validate_principle_clusters(_cl(tmp_path, [bad]))
    )


def test_schema_violation_min_members(tmp_path):
    bad = {**_GOOD, "member_principle_ids": ["P1"]}  # < 2
    assert any("Schema" in e for e in validate_principle_clusters(_cl(tmp_path, [bad])))
