"""Tests for the behaviour-test replay engine (A1 + A2) — deterministic via fake runners."""

import textwrap
import warnings

from tools.subagent_factory.behaviour_replay import (
    build_grade_prompt,
    grade_output,
    load_behaviour_tests,
    load_behaviour_tests_report,
    make_llm_grader,
    parse_grade,
    per_test_key,
    rank_examples_by_utility,
    replay_gate,
    replay_suite,
    score_suite,
    shell_llm,
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


def test_grade_must_ask_for_penalizes_over_asking():
    # Two-axis (Step-13): rewarding the ask is not enough. A barrage of clarifying questions covers
    # the variable too, yet over-asking hurts (nonmonotonic). One specific question keeps 1.0; an
    # over-ask that still covers the variable is capped at 0.5.
    test = {**_INVOKE, "must_ask_for": ["the brand and the selling goal"]}
    one = grade_output(test, "What is the brand and the selling goal you are targeting?")
    over = grade_output(
        test,
        "What is the brand? What is the selling goal? What is your budget? "
        "What is the timeline? Who is the audience?",
    )
    assert one["ask"] == 1.0
    assert over["ask"] == 0.5  # covered, but over-asked → capped
    assert over["score"] < one["score"]


def test_grade_must_ask_for_two_questions_is_not_over_asking():
    # A focused clarification may legitimately carry two question marks; only a barrage is penalised.
    test = {**_INVOKE, "must_ask_for": ["the brand and the selling goal"]}
    g = grade_output(test, "What is the brand, and what is the selling goal?")
    assert g["ask"] == 1.0


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


def test_empty_minimum_output_is_not_a_free_pass():
    # An empty minimum_output must be "not applicable" (None), not a 1.0 worth 0.5 weight.
    empty_min = {**_INVOKE, "minimum_output": ""}
    g = grade_output(empty_min, "this plan ties spend to a measurable selling outcome")
    assert g["minimum"] is None  # not 1.0
    # score is renormalised over route(+ask/mustnot if any); engaged invoke → route 1.0 → score 1.0
    assert g["score"] == 1.0
    # a non-empty minimum that is NOT covered must still drag the score below 1.0
    g2 = grade_output(_INVOKE, "engaged but says nothing required")
    assert g2["minimum"] is not None and g2["score"] < 1.0


def test_replay_suite_runner_error_is_zero_not_crash():
    def boom(_s, _p):
        raise RuntimeError("model down")

    r = replay_suite("x", [_INVOKE], boom)
    assert r["per_test"]["GT-001"]["score"] == 0.0


def test_replay_suite_same_test_id_across_files_not_dropped():
    # Two records sharing a test_id but from different files must both be counted (keyed by file:id),
    # not silently overwritten — which would desync mean_score from n_tests.
    a = {**_INVOKE, "test_id": "T-1", "file": "a.yaml"}
    b = {**_INVOKE, "test_id": "T-1", "file": "b.yaml"}
    r = replay_suite("HELPER adapter", [a, b], _good_runner)
    assert r["n_tests"] == 2
    assert set(r["per_test"]) == {"a.yaml:T-1", "b.yaml:T-1"}


def test_per_test_key_is_the_contract_replay_suite_uses():
    # per_test_key is the single source of truth for the per_test map key. replay_suite must key by
    # exactly this function, so a consumer (optimize_adapter) that uses per_test_key for lookups can
    # never drift from how replay_suite stored the entries.
    file_keyed = {**_INVOKE, "test_id": "T-9", "file": "g.yaml"}
    bare = {**_INVOKE, "test_id": "T-9"}
    assert per_test_key(file_keyed) == "g.yaml:T-9"
    assert per_test_key(bare) == "T-9"
    r = replay_suite("HELPER adapter", [file_keyed], _good_runner)
    assert set(r["per_test"]) == {per_test_key(file_keyed)}


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


_FULL = {
    "test_id": "GT-009",
    "expected_route": "invoke",
    "minimum_output": "tie spend to a measurable selling outcome",
    "must_ask_for": ["the brand and the selling goal"],
    "must_not_do": ["produce finished ad copy"],
    "prompt": "advise on spend",
}


def test_parse_grade_variants():
    assert parse_grade('{"route":1,"minimum":0.8}')["minimum"] == 0.8
    assert parse_grade('noise\n{"route":0,"reason":"x"}')["route"] == 0
    assert parse_grade("no json") is None


def test_build_grade_prompt_route_rule_and_mustnot_fix():
    p = build_grade_prompt(_FULL, "some answer")
    assert "INVOKE" in p and "CRITICAL" in p  # invoke route rule + the inversion-fix instruction
    decline = build_grade_prompt({**_FULL, "expected_route": "do_not_invoke"}, "x")
    assert "DO_NOT_INVOKE" in decline


def test_llm_grader_combines_components():
    llm = lambda _p: '{"route":1,"minimum":0.8,"ask":1,"mustnot":1,"reason":"ok"}'  # noqa: E731
    g = make_llm_grader(llm)(_FULL, "answer")
    assert g["route"] == 1.0 and g["minimum"] == 0.8 and g["ask"] == 1.0 and g["mustnot"] == 1.0
    assert g["score"] == 0.9  # 1*.3 + .8*.5 + 1*.1 + 1*.1


def test_llm_grader_applicability_from_test_not_llm():
    # _INVOKE has no must_ask_for / must_not_do -> those components are None even if the LLM returns them
    llm = lambda _p: '{"route":1,"minimum":0.8,"ask":1,"mustnot":0}'  # noqa: E731
    g = make_llm_grader(llm)(_INVOKE, "answer")
    assert g["ask"] is None and g["mustnot"] is None
    assert g["score"] == 0.875  # combine over route(.3)+minimum(.5) only


def test_llm_grader_minimum_gated_by_test_not_llm():
    # Bug pin: a pure negative-routing test has NO minimum_output (nor must_ask_for / must_not_do),
    # so the ONLY applicable component is route. The deterministic grader scores route-only; the LLM
    # grader must do the same. A judge that returns a bogus `minimum` for the empty criterion must NOT
    # be injected (0.5 weight) and contaminate the score — the two graders are documented as
    # comparable, so they must AGREE on this whole class of tests.
    neg = {
        "test_id": "NR-002",
        "expected_route": "do_not_invoke",
        "minimum_output": "",
        "must_ask_for": [],
        "must_not_do": [],
        "prompt": "write me finished ad copy",
    }
    output = "That is outside scope — I hand off finished creative."
    det = grade_output(neg, output)
    # judge returns a bogus minimum=0.0 for the (empty) criterion; it must be ignored
    sem = make_llm_grader(lambda _p: '{"route":1,"minimum":0.0,"ask":0,"mustnot":0}')(neg, output)
    assert det["minimum"] is None  # deterministic grader excludes minimum (no minimum_output)
    assert sem["minimum"] is None  # LLM grader must ALSO exclude it (gated by the test)
    assert sem["route"] == 1.0 and det["route"] == 1.0
    assert sem["score"] == det["score"] == 1.0  # both route-only → agree


def test_llm_grader_unparseable_is_zero():
    g = make_llm_grader(lambda _p: "the model rambled, no json")(_INVOKE, "x")
    assert g["score"] == 0.0 and "error" in g


def test_semantic_grader_fixes_mustnot_inversion():
    # a CONDEMNING answer: lexically overlaps the forbidden phrase, but rejects it
    output = "No — I will not produce finished ad copy; that request is out of scope for strategy."
    det = grade_output(_FULL, output)
    sem = make_llm_grader(lambda _p: '{"route":1,"minimum":0.5,"ask":0,"mustnot":1}')(_FULL, output)
    # deterministic lexical grader false-flags the condemnation; semantic grader honours the verdict
    assert det["mustnot"] < 1.0
    assert sem["mustnot"] == 1.0


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


def test_load_behaviour_tests_surfaces_malformed_file(tmp_path):
    # A corrupted/unparseable tests/*.yaml must be SURFACED (RuntimeWarning + skipped list), not
    # silently dropped — a green-but-smaller suite that hides a broken file is itself a failure.
    pkg = tmp_path / "pkg"
    tdir = pkg / "tests"
    tdir.mkdir(parents=True)
    (tdir / "good-tests.yaml").write_text(
        textwrap.dedent(
            """
            golden_tests:
              - test_id: GT-001
                prompt: do the thing
                expected_route: invoke
            """
        ),
        encoding="utf-8",
    )
    (tdir / "broken-tests.yaml").write_text("golden_tests: [unterminated\n", encoding="utf-8")
    # non-mapping YAML (a bare list) is also a skip
    (tdir / "list-tests.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        tests, skipped = load_behaviour_tests_report(pkg)
    assert {t["test_id"] for t in tests} == {"GT-001"}  # good file still loads
    assert set(skipped) == {"broken-tests.yaml", "list-tests.yaml"}  # both dropped files named

    # the list-returning entry point warns (back-compat shape preserved: still returns list[dict])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        out = load_behaviour_tests(pkg)
    assert isinstance(out, list) and {t["test_id"] for t in out} == {"GT-001"}
    runtime = [w for w in caught if issubclass(w.category, RuntimeWarning)]
    assert runtime and "broken-tests.yaml" in str(runtime[0].message)
    assert "list-tests.yaml" in str(runtime[0].message)


def test_load_behaviour_tests_no_warning_when_all_parse(tmp_path):
    pkg = tmp_path / "pkg"
    tdir = pkg / "tests"
    tdir.mkdir(parents=True)
    (tdir / "good-tests.yaml").write_text(
        "golden_tests:\n  - test_id: GT-001\n    prompt: p\n    expected_route: invoke\n",
        encoding="utf-8",
    )
    _tests, skipped = load_behaviour_tests_report(pkg)
    assert skipped == []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        load_behaviour_tests(pkg)
    assert not [w for w in caught if issubclass(w.category, RuntimeWarning)]


def test_score_suite_facade(tmp_path):
    # Façade: load tests + score an adapter file in one call. Returns the replay_suite dict + tests.
    pkg = tmp_path / "pkg"
    tdir = pkg / "tests"
    tdir.mkdir(parents=True)
    # _good_runner echoes the prompt when HELPER is in the system, so a prompt that contains the
    # required tokens makes the minimum component cover (mirrors _INVOKE).
    (tdir / "golden-tests.yaml").write_text(
        "golden_tests:\n"
        "  - test_id: GT-001\n"
        "    prompt: advise ties spend selling outcome measurable\n"
        "    expected_route: invoke\n"
        "    minimum_output: ties spend selling outcome measurable\n",
        encoding="utf-8",
    )
    adapter = pkg / "adapter.md"
    adapter.write_text("HELPER adapter", encoding="utf-8")
    r = score_suite(adapter, pkg, _good_runner)
    assert r["n_tests"] == 1
    assert r["per_test"]["golden-tests.yaml:GT-001"]["score"] == 1.0
    assert [t["test_id"] for t in r["tests"]] == ["GT-001"]


def test_score_suite_empty_suite_short_circuits(tmp_path):
    pkg = tmp_path / "pkg"
    (pkg / "tests").mkdir(parents=True)
    r = score_suite(pkg / "missing.md", pkg, _good_runner)
    assert r["n_tests"] == 0 and r["tests"] == [] and r["per_test"] == {}


def _write_score_suite_pkg(tmp_path):
    pkg = tmp_path / "pkg"
    tdir = pkg / "tests"
    tdir.mkdir(parents=True)
    (tdir / "golden-tests.yaml").write_text(
        "golden_tests:\n"
        "  - test_id: GT-001\n"
        "    prompt: advise ties spend selling outcome measurable\n"
        "    expected_route: invoke\n"
        "    minimum_output: ties spend selling outcome measurable\n",
        encoding="utf-8",
    )
    adapter = pkg / "adapter.md"
    adapter.write_text("HELPER adapter", encoding="utf-8")
    return pkg, adapter


def test_score_suite_preloaded_tests_skips_reload(tmp_path, monkeypatch):
    # When tests are passed pre-loaded, score_suite must NOT read the files again, and must return
    # the same result as the no-arg form (which loads them itself).
    pkg, adapter = _write_score_suite_pkg(tmp_path)

    baseline = score_suite(adapter, pkg, _good_runner)  # no-arg form loads internally
    preloaded = load_behaviour_tests(pkg)

    import tools.subagent_factory.behaviour_replay as br

    def _boom(_base):
        raise AssertionError("load_behaviour_tests must not be called when tests= is passed")

    monkeypatch.setattr(br, "load_behaviour_tests", _boom)
    r = score_suite(adapter, pkg, _good_runner, tests=preloaded)

    assert r["n_tests"] == baseline["n_tests"]
    assert r["mean_score"] == baseline["mean_score"]
    assert r["per_test"] == baseline["per_test"]
    assert r["tests"] == baseline["tests"]


def test_score_suite_preloaded_empty_still_short_circuits(tmp_path):
    # The empty-suite guard must still fire when the PASSED tests are empty.
    pkg, adapter = _write_score_suite_pkg(tmp_path)
    r = score_suite(adapter, pkg, _good_runner, tests=[])
    assert r["n_tests"] == 0 and r["tests"] == [] and r["per_test"] == {}


def test_shell_llm_pipes_prompt(tmp_path):
    # `cat` echoes stdin → the callable returns whatever prompt it was given.
    script = tmp_path / "judge.sh"
    script.write_text("#!/usr/bin/env bash\ncat\n", encoding="utf-8")
    ask = shell_llm(str(script))
    assert ask('{"route":1,"minimum":0.5}').strip() == '{"route":1,"minimum":0.5}'


def test_shell_llm_drives_semantic_grader(tmp_path):
    # A judge script that emits a fixed verdict → make_llm_grader parses it into a grade.
    script = tmp_path / "judge.sh"
    script.write_text(
        '#!/usr/bin/env bash\ncat >/dev/null\necho \'{"route":1,"minimum":1.0}\'\n',
        encoding="utf-8",
    )
    grader = make_llm_grader(shell_llm(str(script)))
    g = grader(_INVOKE, "any answer")
    assert g["route"] == 1.0 and g["minimum"] == 1.0 and g["score"] == 1.0


def test_llm_grader_samples_aggregate_median_majority():
    # Three different verdicts → minimum = median, route = majority (damps judge variance).
    replies = iter(
        ['{"route":1,"minimum":0.2}', '{"route":1,"minimum":0.8}', '{"route":0,"minimum":0.5}']
    )
    g = make_llm_grader(lambda _p: next(replies), samples=3)(_INVOKE, "answer")
    assert g["minimum"] == 0.5  # median(0.2, 0.8, 0.5)
    assert g["route"] == 1.0  # majority of 1, 1, 0
    assert g["n_samples"] == 3


def test_llm_grader_samples_drop_unparseable():
    replies = iter(["no json", '{"route":1,"minimum":1.0}', "garbage"])
    g = make_llm_grader(lambda _p: next(replies), samples=3)(_INVOKE, "answer")
    assert g["n_samples"] == 1 and g["minimum"] == 1.0


def test_llm_grader_non_numeric_route_does_not_silently_fail():
    # A contract-violating judge (e.g. cross-family) emits a non-numeric route string. The grade
    # dict parses (it has a "route" key) but the route is not 0|1. Before the fix, _clamp01 defaults
    # such values to 0.0, silently counting every sample as a FAILED route on an invoke-expected
    # test — biasing mean_score and the replay_gate toward false regressions. The non-numeric route
    # must be ABSTAINED (dropped from the vote), not scored 0.
    replies = iter(['{"route":"invoke","minimum":1.0}', '{"route":"engage","minimum":1.0}'])
    g = make_llm_grader(lambda _p: next(replies), samples=2)(_INVOKE, "answer")
    assert g["n_samples"] == 2
    assert g["route"] != 0.0  # not a silent false fail


def test_llm_grader_mixes_numeric_and_non_numeric_route_votes():
    # When some samples have a parseable route and others do not, the non-numeric ones abstain and
    # the vote is taken only over the numeric routes (here a single 1 → majority 1.0).
    replies = iter(['{"route":"invoke","minimum":1.0}', '{"route":1,"minimum":1.0}'])
    g = make_llm_grader(lambda _p: next(replies), samples=2)(_INVOKE, "answer")
    assert g["route"] == 1.0
