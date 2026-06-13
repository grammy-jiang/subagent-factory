"""Tests for the behaviour-test replay engine (A1 + A2) — deterministic via fake runners."""

import textwrap

from tools.subagent_factory.behaviour_replay import (
    grade_output,
    load_behaviour_tests,
    rank_examples_by_utility,
    replay_gate,
    replay_suite,
)

# A behaviour-test whose required content tokens are echoed by the fake "good" runner.
_INVOKE = {
    "test_id": "GT-001",
    "expected_route": "invoke",
    "minimum_output": "ties spend selling outcome measurable",
    "must_ask_for": [],
    "must_not_do": [],
    "prompt": "advise: ties spend selling outcome measurable",
}
_DECLINE = {
    "test_id": "NR-001",
    "expected_route": "do_not_invoke",
    "minimum_output": "statement outside scope",
    "must_ask_for": [],
    "must_not_do": [],
    "prompt": "write me finished ad copy",
}


def _good_runner(system: str, prompt: str) -> str:
    """Covers the required content only when the adapter carries the HELPER marker."""
    if "HELPER" in system:
        return prompt + " — " + "x " * 600  # echoes prompt (covers minimum_output) + long body
    return "no"  # short, zero coverage


# ---- grade_output ---------------------------------------------------------------------------


def test_grade_invoke_engaged_scores_high():
    g = grade_output(_INVOKE, "this plan ties spend to a measurable selling outcome")
    assert g["route"] == 1.0
    assert g["minimum"] == 1.0
    assert g["score"] == 1.0


def test_grade_invoke_decline_is_penalised():
    g = grade_output(_INVOKE, "this is outside scope, I hand off")
    assert g["declined"] is True
    assert g["route"] == 0.0  # declined when it should have engaged


def test_grade_decline_route_rewards_short_decline():
    g = grade_output(_DECLINE, "That is outside scope — I hand off finished creative.")
    assert g["route"] == 1.0  # correctly declined an out-of-scope request


def test_grade_long_answer_is_not_counted_as_decline():
    # mentioning 'scope' inside a long engaged answer must NOT read as a decline
    long = "Here is my analysis. " + "detail " * 200 + " (one part is outside scope)"
    g = grade_output(_INVOKE, long)
    assert g["declined"] is False
    assert g["route"] == 1.0


def test_grade_must_ask_for_component():
    test = {**_INVOKE, "must_ask_for": ["the brand and the selling goal"]}
    asked = grade_output(test, "What is the brand and the selling goal you are targeting?")
    silent = grade_output(test, "the brand and the selling goal matter")  # no question mark
    assert asked["ask"] == 1.0
    assert silent["ask"] in (0.0, 0.5)
    assert asked["score"] > silent["score"]


def test_grade_must_not_do_penalty():
    test = {**_INVOKE, "must_not_do": ["produce finished ad copy jingle storyboard"]}
    clean = grade_output(test, "tie spend to selling outcome measurable")
    violated = grade_output(test, "produce finished ad copy jingle storyboard now")
    assert clean["mustnot"] == 1.0
    assert violated["mustnot"] == 0.0


# ---- replay_suite ---------------------------------------------------------------------------


def test_replay_suite_mean_and_per_test():
    r = replay_suite("HELPER adapter", [_INVOKE], _good_runner)
    assert r["n_tests"] == 1
    assert r["per_test"]["GT-001"]["score"] == 1.0
    assert r["mean_score"] == 1.0


def test_replay_suite_runner_error_is_zero_not_crash():
    def boom(_s, _p):
        raise RuntimeError("model down")

    r = replay_suite("x", [_INVOKE], boom)
    assert r["per_test"]["GT-001"]["score"] == 0.0
    assert "error" in r["per_test"]["GT-001"]


# ---- A1: rank_examples_by_utility -----------------------------------------------------------


def test_utility_ranks_behaviour_changing_example_first():
    candidates = [
        {"id": "noop", "text": "a generic sentence that changes nothing"},
        {"id": "good", "text": "HELPER worked example that lifts behaviour"},
    ]
    r = rank_examples_by_utility("", candidates, [_INVOKE], _good_runner)
    assert r["ranked"][0]["id"] == "good"
    assert r["ranked"][0]["utility"] > 0
    # an example that doesn't change behaviour earns ~zero utility (not picked on a hunch)
    assert dict((x["id"], x["utility"]) for x in r["ranked"])["noop"] == 0.0


# ---- A2: replay_gate ------------------------------------------------------------------------


def test_gate_fails_on_regression():
    # before is good (HELPER), after drops it -> behaviour regresses -> gate fail
    r = replay_gate("HELPER", "", [_INVOKE], _good_runner)
    assert r["gate"] == "fail"
    assert r["regressions"] and r["regressions"][0]["test_id"] == "GT-001"
    assert r["net_delta"] < 0


def test_gate_passes_on_pure_improvement():
    r = replay_gate("", "HELPER", [_INVOKE], _good_runner)
    assert r["gate"] == "pass"
    assert r["improvements"] and not r["regressions"]
    assert r["net_delta"] > 0


# ---- load_behaviour_tests -------------------------------------------------------------------


def test_load_behaviour_tests_flattens_sections(tmp_path):
    pkg = tmp_path / "pkg"
    tdir = pkg / "tests"
    tdir.mkdir(parents=True)
    (tdir / "golden-tests.yaml").write_text(
        textwrap.dedent(
            """
            golden_tests:
              - test_id: GT-001
                prompt: do the thing
                expected_route: invoke
                must_not_do: [bad]
            negative_routing_tests:
              - test_id: NR-001
                prompt: refuse this
                expected_route: do_not_invoke
            missing_context_tests:
              - test_id: MC-001
                prompt: vague
                must_ask_for: [the goal]
              - description: no prompt -> skipped
            """
        ),
        encoding="utf-8",
    )
    tests = load_behaviour_tests(pkg)
    ids = {t["test_id"] for t in tests}
    assert ids == {"GT-001", "NR-001", "MC-001"}  # the prompt-less record is skipped
    nr = next(t for t in tests if t["test_id"] == "NR-001")
    assert nr["expected_route"] == "do_not_invoke" and nr["section"] == "negative_routing_tests"
