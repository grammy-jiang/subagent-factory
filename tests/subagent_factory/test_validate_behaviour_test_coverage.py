"""Tests for the Step-11 behaviour-test coverage validator.

Focus: the fail-closed behaviour of a COVERAGE gate. When principles.yaml is
absent or unparseable, the gate cannot read what it is meant to cover, so it must
FAIL rather than pass vacuously (the old `_high_confidence_principles` collapsed
missing / unparseable / genuinely-empty into the same (set(), set()) result).
"""

import yaml

from tools.subagent_factory.validate_behaviour_test_coverage import (
    validate_behaviour_test_coverage,
)


def _suite(golden=None, negative=None, missing=None):
    out = {"schema_version": "golden-tests-v1", "subagent_slug": "demo"}
    if golden is not None:
        out["golden_tests"] = golden
    if negative is not None:
        out["negative_routing_tests"] = negative
    if missing is not None:
        out["missing_context_tests"] = missing
    return out


def _pkg(tmp_path, suite, principles="__omit__"):
    """Write tests/behaviour-tests.yaml and optionally principles/principles.yaml.

    principles="__omit__" -> do not create principles.yaml (absent).
    principles=<str>      -> write the raw string verbatim (e.g. malformed YAML).
    principles=<dict>     -> dump as YAML.
    """
    base = tmp_path / "pkg"
    (base / "tests").mkdir(parents=True)
    sp = base / "tests" / "behaviour-tests.yaml"
    sp.write_text(yaml.safe_dump(suite), encoding="utf-8")
    if principles != "__omit__":
        (base / "principles").mkdir(parents=True)
        pp = base / "principles" / "principles.yaml"
        if isinstance(principles, str):
            pp.write_text(principles, encoding="utf-8")
        else:
            pp.write_text(yaml.safe_dump(principles), encoding="utf-8")
    return sp


# --- Fail-closed cases (the fix) ---


def test_principles_absent_fails(tmp_path):
    # A covering suite but no principles.yaml: cannot verify coverage -> FAIL.
    suite = _suite(golden=[{"test_id": "g1", "prompt": "do the thing"}])
    errs = validate_behaviour_test_coverage(_pkg(tmp_path, suite, principles="__omit__"))
    assert any("principles.yaml" in e for e in errs)


def test_principles_unparseable_fails(tmp_path):
    suite = _suite(golden=[{"test_id": "g1", "prompt": "do the thing"}])
    errs = validate_behaviour_test_coverage(
        _pkg(tmp_path, suite, principles="key: [unterminated\n")
    )
    assert any("principles.yaml" in e for e in errs)


# --- No false-FAIL: present principles file is readable ---


def test_present_zero_high_confidence_passes(tmp_path):
    # principles.yaml present with only non-high principles -> vacuous coverage is OK.
    suite = _suite(golden=[{"test_id": "g1", "prompt": "p"}])
    principles = {"principles": [{"principle_id": "P1", "confidence": "medium"}]}
    errs = validate_behaviour_test_coverage(_pkg(tmp_path, suite, principles=principles))
    assert errs == []


def test_high_confidence_covered_passes(tmp_path):
    suite = _suite(golden=[{"test_id": "g1", "prompt": "p", "principle_coverage": ["P1"]}])
    principles = {"principles": [{"principle_id": "P1", "confidence": "high"}]}
    errs = validate_behaviour_test_coverage(_pkg(tmp_path, suite, principles=principles))
    assert errs == []


def test_high_confidence_uncovered_fails(tmp_path):
    suite = _suite(golden=[{"test_id": "g1", "prompt": "p"}])
    principles = {"principles": [{"principle_id": "P1", "confidence": "high"}]}
    errs = validate_behaviour_test_coverage(_pkg(tmp_path, suite, principles=principles))
    assert any("no golden test" in e for e in errs)


def test_unknown_principle_ref_fails(tmp_path):
    suite = _suite(golden=[{"test_id": "g1", "prompt": "p", "principle_coverage": ["P-ghost"]}])
    principles = {"principles": [{"principle_id": "P1", "confidence": "high"}]}
    errs = validate_behaviour_test_coverage(_pkg(tmp_path, suite, principles=principles))
    assert any("unknown principle id" in e for e in errs)
