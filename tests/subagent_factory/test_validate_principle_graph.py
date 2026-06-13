"""Tests for the principle-graph validator (Step 7 Phase C)."""

import json

import yaml

from tools.subagent_factory.validate_principle_graph import validate_principle_graph


def _g(tmp_path, edges, pids=("P1", "P2", "P3")):
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
    f = base / "principles" / "principle-graph.json"
    f.write_text(
        json.dumps({"schema_version": "principle-graph-v1", "subagent_slug": "d", "edges": edges}),
        encoding="utf-8",
    )
    return f


def test_valid(tmp_path):
    assert (
        validate_principle_graph(
            _g(tmp_path, [{"source": "P1", "target": "P2", "relation": "alias"}])
        )
        == []
    )


def test_dangling_target(tmp_path):
    bad = [{"source": "P1", "target": "GHOST", "relation": "refines"}]
    assert any("not in principles" in e for e in validate_principle_graph(_g(tmp_path, bad)))


def test_self_loop(tmp_path):
    bad = [{"source": "P1", "target": "P1", "relation": "alias"}]
    assert any("self-loop" in e for e in validate_principle_graph(_g(tmp_path, bad)))


def test_duplicate_edge(tmp_path):
    e = {"source": "P1", "target": "P2", "relation": "supports"}
    assert any("duplicate" in x for x in validate_principle_graph(_g(tmp_path, [e, dict(e)])))


def test_hierarchy_cycle(tmp_path):
    edges = [
        {"source": "P1", "target": "P2", "relation": "refines"},
        {"source": "P2", "target": "P1", "relation": "refines"},
    ]
    assert any("cycle" in e for e in validate_principle_graph(_g(tmp_path, edges)))


def test_unresolved_conflict_is_not_a_structural_error(tmp_path):
    # a conflicts edge with no resolution is valid here (the gate WARNs / logs it, not the validator).
    edges = [{"source": "P1", "target": "P2", "relation": "conflicts"}]
    assert validate_principle_graph(_g(tmp_path, edges)) == []


def test_bad_relation_is_schema_error(tmp_path):
    bad = [{"source": "P1", "target": "P2", "relation": "bogus"}]
    assert any("Schema" in e for e in validate_principle_graph(_g(tmp_path, bad)))
