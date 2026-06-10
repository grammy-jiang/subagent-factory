"""Tests for the evidence-records validator (Step 3)."""

import json

import yaml

from tools.subagent_factory.validate_evidence_records import validate_evidence_records

_REC = {
    "evidence_id": "E-0001",
    "claim_id": "C-0001",
    "source_ids": ["s1"],
    "source_anchors": ["s1-h0001"],
    "support_granularity": "section",
    "evidence_type": "research",
    "evidence_strength": "moderate",
    "support_level": "partially_supported",
    "confidence": "medium",
    "quote_allowed": False,
    "limitations": "author gives rationale, no empirical data",
}


def _pkg(
    tmp_path,
    records,
    claim_ids=("C-0001",),
    source_ids=("s1",),
    anchors=("s1-h0001",),
    rights="distillation-only",
):
    base = tmp_path / "pkg"
    (base / "evidence").mkdir(parents=True)
    rp = base / "evidence" / "evidence-records.yaml"
    rp.write_text(
        yaml.safe_dump({"schema_version": "evidence-records-v1", "evidence_records": records}),
        encoding="utf-8",
    )
    if claim_ids is not None:
        (base / "analysis").mkdir(parents=True)
        (base / "analysis" / "claims.jsonl").write_text(
            "\n".join(
                json.dumps(
                    {
                        "claim_id": c,
                        "source_id": "s1",
                        "statement": "x",
                        "component_class": "claim",
                        "claim_type": "fact",
                    }
                )
                for c in claim_ids
            )
            + "\n",
            encoding="utf-8",
        )
    if source_ids is not None:
        (base / "sources" / "metadata").mkdir(parents=True)
        srcs = []
        for s in source_ids:
            rel = f"sources/metadata/{s}.metadata.json"
            (base / rel).write_text(
                json.dumps({"source_id": s, "rights_status": rights}), encoding="utf-8"
            )
            srcs.append({"source_id": s, "metadata_path": rel})
        (base / "source-pack.manifest.yaml").write_text(
            yaml.safe_dump({"schema_version": "source-pack-manifest-v1", "sources": srcs}),
            encoding="utf-8",
        )
    if anchors is not None:
        (base / "sources" / "anchors").mkdir(parents=True)
        (base / "sources" / "anchors" / "s1.anchors.jsonl").write_text(
            "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
        )
    return rp


def test_valid(tmp_path):
    assert validate_evidence_records(_pkg(tmp_path, [_REC])) == []


def test_bad_enum_is_schema_error(tmp_path):
    assert validate_evidence_records(_pkg(tmp_path, [{**_REC, "support_level": "nope"}]))


def test_unknown_claim_id(tmp_path):
    errs = validate_evidence_records(_pkg(tmp_path, [{**_REC, "claim_id": "C-999"}]))
    assert any("claims.jsonl" in e for e in errs)


def test_unknown_source_id(tmp_path):
    errs = validate_evidence_records(_pkg(tmp_path, [{**_REC, "source_ids": ["ghost"]}]))
    assert any("not in manifest" in e for e in errs)


def test_anchor_not_in_index(tmp_path):
    errs = validate_evidence_records(_pkg(tmp_path, [{**_REC, "source_anchors": ["ghost-h9"]}]))
    assert any("anchor index" in e for e in errs)


def test_quote_allowed_on_restricted_fails(tmp_path):
    errs = validate_evidence_records(
        _pkg(tmp_path, [{**_REC, "quote_allowed": True}], rights="distillation-only")
    )
    assert any("quote_allowed" in e for e in errs)


def test_quote_allowed_on_open_ok(tmp_path):
    assert (
        validate_evidence_records(_pkg(tmp_path, [{**_REC, "quote_allowed": True}], rights="open"))
        == []
    )


def test_duplicate_evidence_id(tmp_path):
    assert any("duplicate" in e for e in validate_evidence_records(_pkg(tmp_path, [_REC, _REC])))
