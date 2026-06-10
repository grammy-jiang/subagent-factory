"""Tests for principle-to-behaviour test coverage (Step 5)."""

import yaml

from tools.subagent_factory.validate_principle_test_coverage import validate_principle_test_coverage

_P_HIGH = {
    "principle_id": "P-001",
    "statement": "x",
    "derived_from_claims": ["C-1"],
    "confidence": "high",
}
_P_MED = {
    "principle_id": "P-002",
    "statement": "y",
    "derived_from_claims": ["C-2"],
    "confidence": "medium",
}


def _pkg(tmp_path, principles, tests=None, tests_filename="principle-behaviour-tests.yaml"):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    pp = base / "principles" / "principles.yaml"
    pp.write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    if tests is not None:
        (base / "tests").mkdir(parents=True)
        (base / "tests" / tests_filename).write_text(yaml.safe_dump(tests), encoding="utf-8")
    return pp


def test_high_principle_covered(tmp_path):
    tests = {"principle_behaviour_tests": [{"test_id": "PB-1", "principle_id": "P-001"}]}
    assert validate_principle_test_coverage(_pkg(tmp_path, [_P_HIGH], tests)) == []


def test_high_principle_uncovered(tmp_path):
    errs = validate_principle_test_coverage(
        _pkg(tmp_path, [_P_HIGH], tests={"principle_behaviour_tests": []})
    )
    assert any("no behavioural test" in e for e in errs)


def test_medium_principle_not_required(tmp_path):
    assert (
        validate_principle_test_coverage(
            _pkg(tmp_path, [_P_MED], tests={"principle_behaviour_tests": []})
        )
        == []
    )


def test_dangling_principle_ref(tmp_path):
    tests = {"principle_behaviour_tests": [{"test_id": "PB-1", "principle_id": "P-999"}]}
    errs = validate_principle_test_coverage(_pkg(tmp_path, [_P_HIGH], tests=tests))
    assert any("unknown principle_id" in e for e in errs)


def test_coverage_via_golden_tests(tmp_path):
    pp = _pkg(
        tmp_path,
        [_P_HIGH],
        tests={"golden_tests": [{"test_id": "GT-1", "principle_id": "P-001"}]},
        tests_filename="golden-tests.yaml",
    )
    assert validate_principle_test_coverage(pp) == []
