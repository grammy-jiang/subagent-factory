"""Tests for surgical LLM claim re-anchoring — deterministic via a fake LLM."""

import json
import re

import yaml

from tools.subagent_factory.reanchor_claims import (
    build_reanchor_prompt,
    parse_reanchor,
    reanchor_claims,
)

_SID = "the-book-20260101"


def _build(tmp_path):
    base = tmp_path / "pkg"
    (base / "analysis").mkdir(parents=True)
    (base / "evidence").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "markdown").mkdir(parents=True)
    anchors = [
        {
            "anchor_id": f"{_SID}-t0001",
            "source_id": _SID,
            "line_number": 1,
            "text": "mirroring repeat last critical words",
        },
        {
            "anchor_id": f"{_SID}-t0002",
            "source_id": _SID,
            "line_number": 3,
            "text": "tactical empathy understand counterpart feelings",
        },
        {
            "anchor_id": f"{_SID}-t0003",
            "source_id": _SID,
            "line_number": 5,
            "text": "unrelated filler content here",
        },
    ]
    (base / "sources" / "anchors" / f"{_SID}.anchors.jsonl").write_text(
        "\n".join(json.dumps(a) for a in anchors), encoding="utf-8"
    )
    (base / "sources" / "markdown" / f"{_SID}.md").write_text(
        "mirroring is repeating the last critical words\n\nx\ntactical empathy means understanding\n\nfiller\n",
        encoding="utf-8",
    )
    claims = [
        {
            "schema_version": "claims-v1",
            "claim_id": "CL001",
            "source_id": _SID,
            "source_anchors": ["ch2-mirroring"],
            "statement": "Mirroring is repeating the last critical words",
            "component_class": "major_claim",
            "claim_type": "fact",
        },
        {
            "schema_version": "claims-v1",
            "claim_id": "CL002",
            "source_id": _SID,
            "source_anchors": ["ch1-empathy"],
            "statement": "Tactical empathy means understanding the counterpart",
            "component_class": "major_claim",
            "claim_type": "value",
        },
    ]
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c) for c in claims), encoding="utf-8"
    )
    ev = {
        "schema_version": "evidence-records-v1",
        "evidence_records": [
            {
                "evidence_id": "EV001",
                "claim_id": "CL001",
                "source_ids": [_SID],
                "source_anchors": ["ch2-mirroring"],
            },
            {
                "evidence_id": "EV002",
                "claim_id": "CL002",
                "source_ids": [_SID],
                "source_anchors": ["ch1-empathy"],
            },
        ],
    }
    (base / "evidence" / "evidence-records.yaml").write_text(yaml.safe_dump(ev), encoding="utf-8")
    return base


def _keyword_llm(prompt: str) -> str:
    """Fake LLM: pick the candidate whose snippet best shares words with the CLAIM line."""
    claim = re.search(r"CLAIM: (.+)", prompt).group(1).lower()
    best, best_id = -1, None
    for aid, snip in re.findall(r"- (\S+): (.*)", prompt):
        overlap = len(set(claim.split()) & set(snip.lower().split()))
        if overlap > best:
            best, best_id = overlap, aid
    return json.dumps({"anchors": [best_id] if best_id else []})


def test_parse_reanchor_rejects_invented_ids():
    allowed = {"a-t0001", "a-t0002"}
    assert parse_reanchor('{"anchors": ["a-t0001", "a-t9999"]}', allowed) == ["a-t0001"]
    assert parse_reanchor("no json", allowed) == []


def test_build_prompt_lists_candidates():
    p = build_reanchor_prompt("the claim", ["x-t0001"], {"x-t0001": "passage text"})
    assert "CLAIM: the claim" in p and "- x-t0001: passage text" in p


def test_reanchor_resolves_slugs_to_real_anchors(tmp_path):
    base = _build(tmp_path)
    rep = reanchor_claims(base, _keyword_llm)
    assert rep["n_fixed"] == 2 and rep["n_empty"] == 0
    # CL001 -> mirroring anchor, CL002 -> empathy anchor (content-correct)
    assert rep["chosen"]["CL001"] == [f"{_SID}-t0001"]
    assert rep["chosen"]["CL002"] == [f"{_SID}-t0002"]


def test_evidence_inherits_claim_anchors(tmp_path):
    base = _build(tmp_path)
    reanchor_claims(base, _keyword_llm)
    ev = yaml.safe_load((base / "evidence" / "evidence-records.yaml").read_text())
    by_id = {r["evidence_id"]: r["source_anchors"] for r in ev["evidence_records"]}
    assert by_id["EV001"] == [f"{_SID}-t0001"]
    assert by_id["EV002"] == [f"{_SID}-t0002"]


def test_claims_written_with_real_anchors(tmp_path):
    base = _build(tmp_path)
    reanchor_claims(base, _keyword_llm)
    lines = (base / "analysis" / "claims.jsonl").read_text().splitlines()
    recs = [json.loads(line) for line in lines if line.strip()]
    assert all(
        a.endswith(tuple(f"-t000{i}" for i in range(1, 4))) or a == []
        for r in recs
        for a in r["source_anchors"]
    )
    assert recs[0]["source_anchors"] == [f"{_SID}-t0001"]


def test_llm_no_support_leaves_empty(tmp_path):
    base = _build(tmp_path)
    rep = reanchor_claims(base, lambda _p: '{"anchors": []}')
    assert rep["n_fixed"] == 0 and rep["n_empty"] == 2
    assert rep["chosen"]["CL001"] == []
