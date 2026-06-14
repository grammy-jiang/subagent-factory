"""Tests for Step-11 behaviour-test generation + coverage validation."""

import json
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory.behaviour_replay import load_behaviour_tests
from tools.subagent_factory.gen_behaviour_tests import (
    _choose_prompt,
    build_ideate_prompt,
    gen_behaviour_tests,
    load_principles,
    shell_ideator,
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
    # golden_tests = the golden cell + the answerable twin paired with the missing-context cell.
    assert len(suite["golden_tests"]) == 2
    assert len(suite["negative_routing_tests"]) == 1
    assert len(suite["missing_context_tests"]) == 1
    _validate_schema(suite)


def test_answerable_twin_paired_with_missing_context():
    suite = gen_behaviour_tests([_P_FULL], "demo")
    mc = suite["missing_context_tests"][0]
    twins = [t for t in suite["golden_tests"] if t.get("twin_of")]
    assert len(twins) == 1
    assert twins[0]["twin_of"] == mc["test_id"]
    assert twins[0]["expected_route"] == "invoke"  # the twin should answer
    assert twins[0]["must_not_do"]  # ... and explicitly not over-ask
    assert not twins[0].get("must_ask_for")  # the twin must NOT require asking


def test_no_twins_when_disabled():
    suite = gen_behaviour_tests([_P_FULL], "demo", answerable_twins=False)
    assert not any(t.get("twin_of") for t in suite["golden_tests"])
    assert len(suite["golden_tests"]) == 1


# ── multi-candidate generation + rare-weighting (#2 follow-on) ──────────────────


def test_choose_prompt_rare_weighted_picks_most_novel():
    accepted = [[1.0, 0.0]]
    vecs = {"NEAR": [0.9, 0.44], "FAR": [0.5, 0.87]}  # NEAR cos≈0.9, FAR cos≈0.5 to accepted
    seq = iter(["NEAR", "FAR"])
    chosen = _choose_prompt(
        _P_FULL, "golden", lambda p, c: next(seq), lambda t: vecs[t], accepted, 2, 0.95
    )
    assert chosen == "FAR"  # lowest max-cosine to the accepted set = most novel
    assert len(accepted) == 2  # chosen vector appended


def test_choose_prompt_all_duplicates_returns_none():
    accepted = [[1.0, 0.0]]
    chosen = _choose_prompt(
        _P_FULL, "golden", lambda p, c: "X", lambda t: [1.0, 0.02], accepted, 2, 0.9
    )
    assert chosen is None  # the only candidate is a near-duplicate of an accepted prompt


def test_multi_candidate_calls_ideator_n_times():
    calls = []

    def ideator(principle, cell_type):
        calls.append(cell_type)
        return f"{cell_type}-{len(calls)}"

    # _P_STMT_ONLY → only the golden cell; n_candidates=3 → 3 ideator calls for it.
    gen_behaviour_tests([_P_STMT_ONLY], "demo", ideator=ideator, n_candidates=3)
    assert calls.count("golden") == 3


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


# ── LLM ideator (E follow-on) ──────────────────────────────────────────────────


def test_build_ideate_prompt_per_cell():
    p = build_ideate_prompt(_P_FULL, "negative-routing")
    assert "Output ONLY" in p
    assert _P_FULL["statement"].rstrip(".") in p
    assert "out-of-scope" in p.lower() or "out of scope" in p.lower()


def test_shell_ideator_feeds_generator(tmp_path):
    # A script that ignores stdin and echoes a fixed message → that becomes the test prompt.
    script = tmp_path / "ideator.sh"
    script.write_text(
        "#!/usr/bin/env bash\ncat >/dev/null\necho 'A crafted realistic message.'\n",
        encoding="utf-8",
    )
    suite = gen_behaviour_tests([_P_FULL], "demo", ideator=shell_ideator(str(script)))
    assert suite["golden_tests"][0]["prompt"] == "A crafted realistic message."
    assert suite["negative_routing_tests"][0]["prompt"] == "A crafted realistic message."
