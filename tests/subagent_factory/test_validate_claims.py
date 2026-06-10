"""Tests for the claims validator (Step 2) — structural + referential."""

import json

import yaml

from tools.subagent_factory.validate_claims import validate_claims

_GOOD_CLAIM = {
    "claim_id": "C-0001",
    "source_id": "s1",
    "statement": "Explicit module boundaries reduce hidden coupling.",
    "component_class": "claim",
    "claim_type": "value",
    "source_anchors": ["s1-h0001"],
    "support_granularity": "section",
    "certainty": "asserted",
}


def _pkg(tmp_path, claims, source_ids=("s1",), anchors=("s1-h0001",)):
    base = tmp_path / "pkg"
    (base / "analysis").mkdir(parents=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c) for c in claims) + "\n", encoding="utf-8"
    )
    if source_ids is not None:
        (base / "source-pack.manifest.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": "source-pack-manifest-v1",
                    "sources": [{"source_id": s} for s in source_ids],
                }
            ),
            encoding="utf-8",
        )
    if anchors is not None:
        (base / "sources" / "anchors").mkdir(parents=True)
        (base / "sources" / "anchors" / "s1.anchors.jsonl").write_text(
            "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
        )
    return base / "analysis" / "claims.jsonl"


def test_valid_claims(tmp_path):
    assert validate_claims(_pkg(tmp_path, [_GOOD_CLAIM])) == []


def test_bad_enum_is_schema_error(tmp_path):
    assert validate_claims(_pkg(tmp_path, [{**_GOOD_CLAIM, "claim_type": "nope"}]))


def test_unknown_source_id(tmp_path):
    errs = validate_claims(_pkg(tmp_path, [{**_GOOD_CLAIM, "source_id": "ghost"}]))
    assert any("not in manifest" in e for e in errs)


def test_anchor_not_in_index(tmp_path):
    errs = validate_claims(_pkg(tmp_path, [{**_GOOD_CLAIM, "source_anchors": ["ghost-h9"]}]))
    assert any("anchor index" in e for e in errs)


def test_premise_type_on_non_premise_fails(tmp_path):
    errs = validate_claims(_pkg(tmp_path, [{**_GOOD_CLAIM, "premise_type": "statistics"}]))
    assert any("non-premise" in e for e in errs)


def test_premise_type_on_premise_ok(tmp_path):
    claim = {**_GOOD_CLAIM, "component_class": "premise", "premise_type": "statistics"}
    assert validate_claims(_pkg(tmp_path, [claim])) == []


def test_duplicate_claim_id(tmp_path):
    errs = validate_claims(_pkg(tmp_path, [_GOOD_CLAIM, _GOOD_CLAIM]))
    assert any("duplicate" in e for e in errs)


def test_bad_json_line(tmp_path):
    base = tmp_path / "pkg"
    (base / "analysis").mkdir(parents=True)
    cp = base / "analysis" / "claims.jsonl"
    cp.write_text("{not json}\n", encoding="utf-8")
    assert any("JSON parse" in e for e in validate_claims(cp))
