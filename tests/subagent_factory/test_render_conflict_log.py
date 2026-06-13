"""Tests for the deterministic conflict-log renderer (Step 7 Phase B)."""

import json

import yaml

from tools.subagent_factory.render_conflict_log import render_conflict_log


def _pkg(tmp_path, edges, pids=("P1", "P2", "P3")):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {
                        "principle_id": p,
                        "statement": f"stmt {p}",
                        "derived_from_claims": ["c"],
                        "confidence": "high",
                    }
                    for p in pids
                ],
            }
        ),
        encoding="utf-8",
    )
    (base / "principles" / "principle-graph.json").write_text(
        json.dumps({"schema_version": "principle-graph-v1", "subagent_slug": "d", "edges": edges}),
        encoding="utf-8",
    )
    return base


def test_resolved_conflict_rendered_as_scoped(tmp_path):
    base = _pkg(
        tmp_path,
        [
            {
                "source": "P1",
                "target": "P2",
                "relation": "conflicts",
                "resolution": "co-valid, scoped by context",
            }
        ],
    )
    out = render_conflict_log(base)
    assert "Resolved / scoped" in out and "co-valid, scoped by context" in out
    assert "**OPEN: 0**" in out
    assert (base / "principles" / "conflict-log.md").exists()


def test_open_conflict_flagged(tmp_path):
    base = _pkg(tmp_path, [{"source": "P1", "target": "P2", "relation": "conflicts"}])
    out = render_conflict_log(base)
    assert "OPEN conflicts" in out and "OPEN: 1" in out


def test_non_conflict_edges_ignored(tmp_path):
    base = _pkg(tmp_path, [{"source": "P1", "target": "P2", "relation": "alias"}])
    out = render_conflict_log(base)
    assert "No cross-source conflicts recorded" in out


def test_no_graph_returns_empty(tmp_path):
    base = tmp_path / "empty"
    (base / "principles").mkdir(parents=True)
    assert render_conflict_log(base) == ""
