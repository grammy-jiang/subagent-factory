"""Tests for the source-map validator (Step 10)."""

import json

import yaml

from tools.subagent_factory.validate_source_map import (
    claim_recall_findings,
    coverage_findings,
    validate_source_map,
)

_GOOD = {
    "schema_version": "source-map-v1",
    "source_id": "s1",
    "nodes": [
        {"node_id": "n1", "parent_id": None, "level": "chapter", "source_anchors": ["a1"]},
        {"node_id": "n2", "parent_id": "n1", "level": "section", "source_anchors": ["a2"]},
    ],
    "candidate_units": [
        {"unit_id": "u1", "node_id": "n2", "statement": "x", "source_anchors": ["a2"]},
    ],
}


def _pkg(tmp_path, data, anchors=("a1", "a2")):
    base = tmp_path / "pkg"
    (base / "sources" / "maps").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "anchors" / "s1.anchors.jsonl").write_text(
        "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
    )
    mp = base / "sources" / "maps" / "s1.source-map.yaml"
    mp.write_text(yaml.safe_dump(data), encoding="utf-8")
    return mp


def test_valid(tmp_path):
    assert validate_source_map(_pkg(tmp_path, _GOOD)) == []


def test_bad_level_is_schema_error(tmp_path):
    bad = {**_GOOD, "nodes": [{"node_id": "n1", "parent_id": None, "level": "page"}]}
    assert validate_source_map(_pkg(tmp_path, bad))


def test_dangling_parent(tmp_path):
    bad = {**_GOOD, "nodes": [{"node_id": "n1", "parent_id": "ghost", "level": "section"}]}
    errs = validate_source_map(_pkg(tmp_path, bad))
    assert any("not an existing node_id" in e for e in errs)


def test_cycle(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": "n2", "level": "section"},
            {"node_id": "n2", "parent_id": "n1", "level": "section"},
        ],
        "candidate_units": [],
    }
    assert any("cycle" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_dangling_anchor(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section", "source_anchors": ["ghost"]}
        ],
        "candidate_units": [],
    }
    assert any("anchor index" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_unit_dangling_node(tmp_path):
    bad = {
        **_GOOD,
        "candidate_units": [{"unit_id": "u1", "node_id": "ghost", "statement": "x"}],
    }
    assert any("not in nodes" in e for e in validate_source_map(_pkg(tmp_path, bad)))


def test_coverage_clean_when_section_has_unit(tmp_path):
    # _GOOD: section n2 has unit u1 → no coverage warning.
    assert coverage_findings(_pkg(tmp_path, _GOOD)) == []


def test_coverage_flags_uncovered_substantive_section(tmp_path):
    m = {
        "schema_version": "source-map-v1",
        "source_id": "s1",
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section", "role_class": "method"},
        ],
        "candidate_units": [],
    }
    out = coverage_findings(_pkg(tmp_path, m))
    assert any("no candidate unit" in w for w in out)


def test_coverage_ignores_background_sections(tmp_path):
    m = {
        "schema_version": "source-map-v1",
        "source_id": "s1",
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section", "role_class": "background"},
        ],
        "candidate_units": [],
    }
    assert coverage_findings(_pkg(tmp_path, m)) == []


def test_coverage_covered_via_descendant(tmp_path):
    m = {
        "schema_version": "source-map-v1",
        "source_id": "s1",
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section", "role_class": "method"},
            {"node_id": "n2", "parent_id": "n1", "level": "passage"},
        ],
        "candidate_units": [{"unit_id": "u1", "node_id": "n2", "statement": "x"}],
    }
    assert coverage_findings(_pkg(tmp_path, m)) == []


def test_duplicate_node_id(tmp_path):
    bad = {
        **_GOOD,
        "nodes": [
            {"node_id": "n1", "parent_id": None, "level": "section"},
            {"node_id": "n1", "parent_id": None, "level": "section"},
        ],
        "candidate_units": [],
    }
    assert any("duplicate node_id" in e for e in validate_source_map(_pkg(tmp_path, bad)))


# ── claim-recall (Step 10 G3 deterministic counterpart) ─────────────────────────


def _write_claims(mp, anchors_per_claim):
    base = mp.parents[2]
    (base / "analysis").mkdir(parents=True, exist_ok=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(
            json.dumps({"claim_id": f"c{i}", "source_anchors": a})
            for i, a in enumerate(anchors_per_claim)
        )
        + "\n",
        encoding="utf-8",
    )


def test_claim_recall_full_no_warn(tmp_path):
    mp = _pkg(tmp_path, _GOOD)
    _write_claims(mp, [["a2"]])  # covers u1's anchor
    assert claim_recall_findings(mp) == []


def test_claim_recall_low_warns(tmp_path):
    data = {
        **_GOOD,
        "candidate_units": [
            {"unit_id": f"u{i}", "node_id": "n2", "statement": "x", "source_anchors": [f"a{i}"]}
            for i in range(5)
        ],
    }
    mp = _pkg(tmp_path, data, anchors=tuple(f"a{i}" for i in range(5)))
    _write_claims(mp, [["a0"]])  # 1/5 = 20% < 25% threshold
    w = claim_recall_findings(mp)
    assert w and "claim recall" in w[0]


def test_claim_recall_no_claims_skips(tmp_path):
    assert claim_recall_findings(_pkg(tmp_path, _GOOD)) == []  # no analysis/claims.jsonl


def test_claim_recall_no_units_skips(tmp_path):
    data = {**_GOOD, "candidate_units": []}
    mp = _pkg(tmp_path, data)
    _write_claims(mp, [["a2"]])
    assert claim_recall_findings(mp) == []
