"""Tests for the principles validator (Step 4)."""

import json

import yaml

from tools.subagent_factory.validate_principles import validate_principles

_PRIN = {
    "principle_id": "P-001",
    "statement": "Prefer explicit interfaces at stable module boundaries.",
    "derived_from_claims": ["C-0001"],
    "confidence": "high",
    "applies_when": ["public API design"],
    "does_not_apply_when": ["throwaway prototype"],
    "operational_mapping": {
        "profile_rule": True,
        "skill": "api-boundary-review",
        "reference": None,
        "test_cases": ["GT-003"],
    },
}


def _pkg(
    tmp_path,
    principles,
    claims=("C-0001",),
    evidence_claims=("C-0001",),
    skills=("api-boundary-review",),
    refs=(),
    test_ids=("GT-003",),
):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    pp = base / "principles" / "principles.yaml"
    pp.write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    if claims is not None:
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
                for c in claims
            )
            + "\n",
            encoding="utf-8",
        )
    if evidence_claims is not None:
        (base / "evidence").mkdir(parents=True)
        recs = [
            {"evidence_id": f"E-{i}", "claim_id": c, "source_ids": ["s1"]}
            for i, c in enumerate(evidence_claims)
        ]
        (base / "evidence" / "evidence-records.yaml").write_text(
            yaml.safe_dump({"schema_version": "evidence-records-v1", "evidence_records": recs}),
            encoding="utf-8",
        )
    if skills is not None or refs is not None:
        (base / "profile.yaml").write_text(
            yaml.safe_dump(
                {
                    "knowledge_partition": {
                        "skills": list(skills or []),
                        "references": list(refs or []),
                    }
                }
            ),
            encoding="utf-8",
        )
    if test_ids is not None:
        (base / "tests").mkdir(parents=True)
        (base / "tests" / "golden-tests.yaml").write_text(
            yaml.safe_dump({"golden_tests": [{"test_id": t} for t in test_ids]}), encoding="utf-8"
        )
    return pp


def test_valid(tmp_path):
    assert validate_principles(_pkg(tmp_path, [_PRIN])) == []


def test_bad_enum_is_schema_error(tmp_path):
    assert validate_principles(_pkg(tmp_path, [{**_PRIN, "confidence": "nope"}]))


def test_unknown_claim(tmp_path):
    errs = validate_principles(_pkg(tmp_path, [{**_PRIN, "derived_from_claims": ["C-999"]}]))
    assert any("claims.jsonl" in e for e in errs)


def test_missing_evidence_coverage(tmp_path):
    errs = validate_principles(
        _pkg(tmp_path, [_PRIN], claims=("C-0001",), evidence_claims=("C-0002",))
    )
    assert any("evidence record" in e for e in errs)


def test_unknown_skill(tmp_path):
    bad = {**_PRIN, "operational_mapping": {**_PRIN["operational_mapping"], "skill": "ghost-skill"}}
    errs = validate_principles(_pkg(tmp_path, [bad], skills=("api-boundary-review",)))
    assert any("knowledge_partition.skills" in e for e in errs)


def test_unknown_test_case(tmp_path):
    bad = {
        **_PRIN,
        "operational_mapping": {**_PRIN["operational_mapping"], "test_cases": ["GT-999"]},
    }
    errs = validate_principles(_pkg(tmp_path, [bad], test_ids=("GT-003",)))
    assert any("tests/" in e for e in errs)


def test_duplicate_principle_id(tmp_path):
    assert any("duplicate" in e for e in validate_principles(_pkg(tmp_path, [_PRIN, _PRIN])))
