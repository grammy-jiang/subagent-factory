"""Tests for Step-11 behaviour-test generation + coverage validation."""

import json
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory.behaviour_replay import load_behaviour_tests
from tools.subagent_factory.gen_behaviour_tests import (
    gen_behaviour_tests,
    load_principles,
    write_suite,
)
from tools.subagent_factory.validate_behaviour_test_coverage import (
    validate_behaviour_test_coverage,
)

_REPO_ROOT = Path(__file__).parent.parent.parent
_SCHEMA = json.loads(
    (_REPO_ROOT / "schemas" / "golden-tests-v1.schema.json").read_text(encoding="utf-8")
)

_P_FULL = {
    "principle_id": "PRP-001",
    "statement": "Establish the identity model first before deciding access.",
    "confidence": "high",
    "applies_when": ["An API is being reviewed for how it controls access"],
    "does_not_apply_when": ["The question is purely about rendering performance"],
}
_P_STMT_ONLY = {
    "principle_id": "PRP-002",
    "statement": "Prefer standards-based security over home-grown schemes.",
    "confidence": "high",
}


def _pkg(tmp_path, principles, suite=None):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    if suite is not None:
        (base / "tests").mkdir(parents=True)
        (base / "tests" / "behaviour-tests.yaml").write_text(
            yaml.safe_dump(suite), encoding="utf-8"
        )
    return base


def _validate_schema(suite):
    jsonschema.Draft202012Validator(_SCHEMA).validate(suite)


# ── generator ────────────────────────────────────────────────────────────────


def test_full_principle_emits_all_three_sections():
    suite = gen_behaviour_tests([_P_FULL], "demo")
    assert len(suite["golden_tests"]) == 1
    assert len(suite["negative_routing_tests"]) == 1
    assert len(suite["missing_context_tests"]) == 1
    _validate_schema(suite)


def test_routes_and_oracles_per_section():
    suite = gen_behaviour_tests([_P_FULL], "demo")
    g = suite["golden_tests"][0]
    nr = suite["negative_routing_tests"][0]
    mc = suite["missing_context_tests"][0]
    assert g["expected_route"] == "invoke" and g["minimum_output"]
    assert nr["expected_route"] == "do_not_invoke" and nr["must_not_do"]
    assert mc["expected_route"] == "invoke" and mc["must_ask_for"]
    assert g["test_id"].startswith("GT-")
    assert nr["test_id"].startswith("NR-")
    assert mc["test_id"].startswith("MC-")


def test_golden_always_emitted_even_without_clauses():
    suite = gen_behaviour_tests([_P_STMT_ONLY], "demo")
    assert len(suite["golden_tests"]) == 1
    assert suite["negative_routing_tests"] == []  # no does_not_apply_when
    assert suite["missing_context_tests"] == []  # no applies_when


def test_principle_coverage_links_back():
    suite = gen_behaviour_tests([_P_FULL], "demo")
    for section in ("golden_tests", "negative_routing_tests", "missing_context_tests"):
        assert all(t["principle_coverage"] == ["PRP-001"] for t in suite[section])


def test_ideator_used_when_provided():
    def ideator(principle, cell_type):
        return f"CUSTOM {cell_type} for {principle['principle_id']}"

    suite = gen_behaviour_tests([_P_FULL], "demo", ideator=ideator)
    prompts = [t["prompt"] for s in _SCHEMA["properties"] if s.endswith("_tests") for t in suite[s]]
    assert prompts and all(p.startswith("CUSTOM ") for p in prompts)


def test_ideator_failure_falls_back_to_template():
    def boom(principle, cell_type):
        raise RuntimeError("model down")

    suite = gen_behaviour_tests([_P_FULL], "demo", ideator=boom)
    _validate_schema(suite)
    assert "CUSTOM" not in suite["golden_tests"][0]["prompt"]


def test_embedder_dedup_drops_near_duplicates():
    # Constant embedding → every prompt looks identical → only the first survives across all sections.
    suite = gen_behaviour_tests(
        [_P_FULL], "demo", embedder=lambda _t: [1.0, 0.0], cos_threshold=0.9
    )
    total = sum(
        len(suite[s]) for s in ("golden_tests", "negative_routing_tests", "missing_context_tests")
    )
    assert total == 1


def test_skips_malformed_principles():
    suite = gen_behaviour_tests([{"no_id": True}, _P_STMT_ONLY], "demo")
    assert [t["principle_coverage"] for t in suite["golden_tests"]] == [["PRP-002"]]


# ── round-trip: generator → behaviour_replay engine (proves "immediately runnable") ─


def test_behaviour_replay_reads_generated_suite(tmp_path):
    suite = gen_behaviour_tests([_P_FULL], "demo")
    base = _pkg(tmp_path, [_P_FULL])
    write_suite(base, suite)
    records = load_behaviour_tests(base)
    by_section = {r["section"]: r for r in records}
    assert by_section["golden_tests"]["expected_route"] == "invoke"
    assert by_section["negative_routing_tests"]["expected_route"] == "do_not_invoke"
    assert by_section["missing_context_tests"]["must_ask_for"]


# ── round-trip: generator → coverage validator ──────────────────────────────────


def test_generated_suite_passes_coverage_validator(tmp_path):
    suite = gen_behaviour_tests([_P_FULL, _P_STMT_ONLY], "demo")
    base = _pkg(tmp_path, [_P_FULL, _P_STMT_ONLY])
    out = write_suite(base, suite)
    assert validate_behaviour_test_coverage(out) == []


def test_load_principles_roundtrip(tmp_path):
    base = _pkg(tmp_path, [_P_FULL])
    assert [p["principle_id"] for p in load_principles(base)] == ["PRP-001"]


# ── validator ──────────────────────────────────────────────────────────────────


def test_validator_flags_missing_golden(tmp_path):
    # Suite covers PRP-001 but not high-confidence PRP-002.
    suite = gen_behaviour_tests([_P_FULL], "demo")
    base = _pkg(tmp_path, [_P_FULL, _P_STMT_ONLY], suite=suite)
    errs = validate_behaviour_test_coverage(base / "tests" / "behaviour-tests.yaml")
    assert any("PRP-002" in e and "no golden test" in e for e in errs)


def test_validator_flags_oracle_shape(tmp_path):
    bad = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": "demo",
        "negative_routing_tests": [
            {
                "test_id": "NR-001",
                "principle_coverage": ["PRP-001"],
                "prompt": "x",
                "expected_route": "invoke",  # wrong: must be do_not_invoke
            }
        ],
        "missing_context_tests": [
            {
                "test_id": "MC-001",
                "principle_coverage": ["PRP-001"],
                "prompt": "y",
                "expected_route": "invoke",  # missing must_ask_for
            }
        ],
        "golden_tests": [
            {
                "test_id": "GT-001",
                "principle_coverage": ["PRP-001"],
                "prompt": "z",
                "expected_route": "invoke",
            }
        ],
    }
    base = _pkg(tmp_path, [_P_FULL], suite=bad)
    errs = validate_behaviour_test_coverage(base / "tests" / "behaviour-tests.yaml")
    assert any("do_not_invoke" in e for e in errs)
    assert any("must populate must_ask_for" in e for e in errs)


def test_validator_flags_unknown_ref(tmp_path):
    suite = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": "demo",
        "golden_tests": [
            {
                "test_id": "GT-001",
                "principle_coverage": ["PRP-999"],
                "prompt": "x",
                "expected_route": "invoke",
            }
        ],
    }
    base = _pkg(tmp_path, [_P_FULL], suite=suite)
    errs = validate_behaviour_test_coverage(base / "tests" / "behaviour-tests.yaml")
    assert any("unknown principle id 'PRP-999'" in e for e in errs)


def test_validator_flags_schema_violation(tmp_path):
    bad = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": "demo",
        "golden_tests": [{"test_id": "GT-001"}],  # missing prompt
    }
    base = _pkg(tmp_path, [_P_FULL], suite=bad)
    errs = validate_behaviour_test_coverage(base / "tests" / "behaviour-tests.yaml")
    assert any(e.startswith("schema:") for e in errs)


# ── guard: the new schema accepts the engine's canonical format ─────────────────


def test_schema_matches_engine_sections():
    """The schema's test sections are exactly behaviour_replay._TEST_SECTIONS."""
    from tools.subagent_factory.behaviour_replay import _TEST_SECTIONS

    schema_sections = {k for k in _SCHEMA["properties"] if k.endswith("_tests")}
    assert schema_sections == set(_TEST_SECTIONS)
