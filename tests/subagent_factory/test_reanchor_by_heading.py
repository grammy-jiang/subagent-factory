"""Tests for deterministic concept-slug -> heading-anchor re-anchoring."""

import json

import yaml

from tools.subagent_factory.reanchor_by_heading import (
    match_slug_to_heading,
    reanchor_by_heading,
)

_SID = "the-book-20260101"


def _build(tmp_path):
    base = tmp_path / "pkg"
    (base / "analysis").mkdir(parents=True)
    (base / "evidence").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    anchors = [
        {"anchor_id": f"{_SID}-h0001", "source_id": _SID, "anchor_type": "heading", "text": "TACTICAL EMPATHY"},
        {"anchor_id": f"{_SID}-h0002", "source_id": _SID, "anchor_type": "heading", "text": "MIRRORING"},
        {"anchor_id": f"{_SID}-t0050", "source_id": _SID, "anchor_type": "text", "text": "some prose"},
    ]
    (base / "sources" / "anchors" / f"{_SID}.anchors.jsonl").write_text(
        "\n".join(json.dumps(a) for a in anchors), encoding="utf-8"
    )
    claims = [
        {"schema_version": "claims-v1", "claim_id": "CL001", "source_id": _SID,
         "source_anchors": ["ch1-tactical-empathy"], "statement": "s", "component_class": "major_claim", "claim_type": "value"},
        {"schema_version": "claims-v1", "claim_id": "CL002", "source_id": _SID,
         "source_anchors": ["ch2-mirroring"], "statement": "s", "component_class": "major_claim", "claim_type": "fact"},
        {"schema_version": "claims-v1", "claim_id": "CL003", "source_id": _SID,
         "source_anchors": ["ch7-7-38-55"], "statement": "s", "component_class": "major_claim", "claim_type": "fact"},
    ]
    (base / "analysis" / "claims.jsonl").write_text("\n".join(json.dumps(c) for c in claims), encoding="utf-8")
    ev = {"schema_version": "evidence-records-v1", "evidence_records": [
        {"evidence_id": "EV001", "claim_id": "CL001", "source_ids": [_SID], "source_anchors": ["ch1-tactical-empathy"]},
    ]}
    (base / "evidence" / "evidence-records.yaml").write_text(yaml.safe_dump(ev), encoding="utf-8")
    return base


def test_match_slug_strips_prefix_and_requires_shared_token():
    heads = [({"tactical", "empathy"}, "a-h0001"), ({"mirroring"}, "a-h0002")]
    assert match_slug_to_heading("ch1-tactical-empathy", heads) == "a-h0001"
    assert match_slug_to_heading("ch2-mirroring", heads) == "a-h0002"
    assert match_slug_to_heading("ch7-7-38-55", heads) is None  # no shared token -> None


def test_reanchor_resolves_matching_slugs(tmp_path):
    base = _build(tmp_path)
    rep = reanchor_by_heading(base)
    assert rep["n_resolved"] == 2 and rep["n_unresolved"] == 1
    recs = {json.loads(line)["claim_id"]: json.loads(line)["source_anchors"]
            for line in (base / "analysis/claims.jsonl").read_text().splitlines() if line.strip()}
    assert recs["CL001"] == [f"{_SID}-h0001"]
    assert recs["CL002"] == [f"{_SID}-h0002"]
    assert recs["CL003"] == []  # no heading -> left empty, not guessed


def test_evidence_inherits_heading_anchor(tmp_path):
    base = _build(tmp_path)
    reanchor_by_heading(base)
    ev = yaml.safe_load((base / "evidence" / "evidence-records.yaml").read_text())
    assert ev["evidence_records"][0]["source_anchors"] == [f"{_SID}-h0001"]


def test_only_heading_anchors_are_targets(tmp_path):
    # a text anchor must never be chosen even if it shares a token
    base = _build(tmp_path)
    reanchor_by_heading(base)
    recs = [json.loads(line) for line in (base / "analysis/claims.jsonl").read_text().splitlines() if line.strip()]
    chosen = {a for r in recs for a in r["source_anchors"]}
    assert all("-h" in a for a in chosen)
