"""Tests for the deterministic Phase 8 profile self-check gate."""

import yaml

from tools.subagent_factory.profile_self_check import profile_self_check


def _valid_profile() -> dict:
    return {
        "schema_version": "portable-profile-v1",
        "slug": "demo-design-reviewer",
        "display_name": "Demo Design Reviewer",
        "agent_version": "0.1.0",
        "status": "draft",
        "role": "An expert reviewer who evaluates designs for complexity and guides "
        "structural improvements grounded in named principles.",
        "when_to_use": [
            "A module interface is submitted for a depth review before merging.",
            "A team needs a diagnosis of where information is leaking between modules.",
            "Two design alternatives are submitted to be compared for module depth.",
        ],
        "when_not_to_use": [
            "The request is solely a bug fix with no design-structure question.",
            "The task is technology or framework selection.",
        ],
        "inputs": {
            "required": [
                "The actual code or interface definition being reviewed.",
                "Enough context about the module purpose to judge interface depth.",
            ]
        },
        "outputs": {
            "primary_format": "annotated design critique with named findings",
            "modes": [
                {
                    "name": "review",
                    "trigger": "an existing artifact is submitted for evaluation",
                    "output": "named red flags with concrete recommendations",
                },
            ],
        },
        "quality_bar": [
            "Every finding cites a named design principle from the source.",
            "Recommendations reference specific evidence, not a style preference.",
            "Module depth is addressed with explicit reference to the principle.",
        ],
        "minimum_useful_output": "At least one named red flag with an explanation.",
        "forbidden_behaviours": [
            "Do not approve a design purely because tests pass.",
        ],
        "handoff_rules": ["Findings return to the module owner for the final decision."],
        "source_of_truth_policy": {
            "canonical_owner": "the developer who owns the module under review",
            "may_edit_canonical": False,
            "precedence": "The canonical source is the cited design book.",
        },
        "knowledge_partition": {
            "always_on": [],
            "skills": [],
            "references": [],
            "mcp": [],
            "caller_supplied": [],
        },
        "sources": [{"source_id": "s1", "title": "A Book", "sha256": "abc"}],
    }


def _golden_doc(golden: int = 3, negative: int = 1) -> dict:
    return {
        "schema_version": "golden-tests-v1",
        "golden_tests": [{"test_id": f"GT-{i:03d}", "description": "x"} for i in range(golden)],
        "negative_routing_tests": [
            {"test_id": f"NR-{i:03d}", "description": "x"} for i in range(negative)
        ],
    }


def _write_package(tmp_path, profile=None, golden=3, negative=1, ledger=True):
    pkg = tmp_path / "subagents" / "demo-design-reviewer"
    pkg.mkdir(parents=True)
    (pkg / "profile.yaml").write_text(yaml.safe_dump(profile or _valid_profile()), encoding="utf-8")
    if ledger:
        (pkg / "provenance-ledger.md").write_text(
            "# Provenance Ledger\n\n" + ("detail. " * 60), encoding="utf-8"
        )
    tests_dir = pkg / "tests"
    tests_dir.mkdir()
    (tests_dir / "golden-tests.yaml").write_text(
        yaml.safe_dump(_golden_doc(golden, negative)), encoding="utf-8"
    )
    return pkg


def _finding(result, num):
    return next(f for f in result["findings"] if f["num"] == num)


def test_valid_profile_passes(tmp_path):
    pkg = _write_package(tmp_path)
    result = profile_self_check(pkg)
    assert result["verdict"] == "PASS", [f for f in result["findings"] if f["level"] == "FAIL"]
    assert result["passed"] is True


def test_missing_profile_fails(tmp_path):
    pkg = tmp_path / "subagents" / "empty"
    pkg.mkdir(parents=True)
    result = profile_self_check(pkg)
    assert result["verdict"] == "FAIL"
    assert result["passed"] is False


def test_when_to_use_too_few_fails(tmp_path):
    p = _valid_profile()
    p["when_to_use"] = p["when_to_use"][:2]
    pkg = _write_package(tmp_path, profile=p)
    result = profile_self_check(pkg)
    assert _finding(result, 2)["level"] == "FAIL"
    assert result["passed"] is False


def test_when_not_to_use_too_few_fails(tmp_path):
    p = _valid_profile()
    p["when_not_to_use"] = p["when_not_to_use"][:1]
    pkg = _write_package(tmp_path, profile=p)
    assert _finding(profile_self_check(pkg), 3)["level"] == "FAIL"


def test_may_edit_canonical_true_fails(tmp_path):
    p = _valid_profile()
    p["source_of_truth_policy"]["may_edit_canonical"] = True
    pkg = _write_package(tmp_path, profile=p)
    assert _finding(profile_self_check(pkg), 10)["level"] == "FAIL"


def test_platform_token_in_core_fails(tmp_path):
    p = _valid_profile()
    p["role"] = p["role"] + " Always write to .claude/agents/generated/."
    pkg = _write_package(tmp_path, profile=p)
    assert _finding(profile_self_check(pkg), 15)["level"] == "FAIL"


def test_non_kebab_slug_fails(tmp_path):
    p = _valid_profile()
    p["slug"] = "Bad_Slug"
    pkg = _write_package(tmp_path, profile=p)
    assert _finding(profile_self_check(pkg), 1)["level"] == "FAIL"


def test_missing_provenance_ledger_fails(tmp_path):
    pkg = _write_package(tmp_path, ledger=False)
    assert _finding(profile_self_check(pkg), 16)["level"] == "FAIL"


def test_too_few_golden_tests_fails(tmp_path):
    pkg = _write_package(tmp_path, golden=2, negative=1)
    assert _finding(profile_self_check(pkg), 18)["level"] == "FAIL"


def test_no_negative_routing_test_fails(tmp_path):
    pkg = _write_package(tmp_path, golden=3, negative=0)
    assert _finding(profile_self_check(pkg), 18)["level"] == "FAIL"


def test_misplaced_test_schema_is_diagnosed(tmp_path):
    # A golden-tests file that parks its tests under a `tests:` list (instead of
    # the canonical golden_tests/negative_routing_tests keys) must FAIL check 18
    # with a diagnostic that names the unrecognized key and points at the
    # template — not a bare "found 0" that hides the schema mismatch.
    pkg = _write_package(tmp_path)
    (pkg / "tests" / "golden-tests.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "golden-tests-v1",
                "tests": [
                    {"test_id": "GT001", "mode": "advise", "routing_type": "positive"},
                    {"test_id": "GT002", "mode": "validate", "routing_type": "negative"},
                ],
            }
        ),
        encoding="utf-8",
    )
    finding = _finding(profile_self_check(pkg), 18)
    assert finding["level"] == "FAIL"
    assert "unrecognized key 'tests'" in finding["message"]
    assert "golden_tests" in finding["message"]
    assert "templates/golden-tests.yaml.j2" in finding["message"]


def test_canonical_test_schema_has_no_misplaced_hint(tmp_path):
    # A well-formed package must not trigger the misplaced-schema diagnostic.
    pkg = _write_package(tmp_path)
    finding = _finding(profile_self_check(pkg), 18)
    assert finding["level"] == "PASS"
    assert "misplaced" not in finding["message"]


def test_body_size_pass_has_plain_message_without_breakdown(tmp_path):
    # A within-budget profile keeps the compact "~N words" message and must NOT
    # carry the heaviest-sections breakdown (that is for over-budget profiles only).
    pkg = _write_package(tmp_path)
    finding = _finding(profile_self_check(pkg), 14)
    assert finding["level"] == "PASS"
    assert "heaviest" not in finding["message"]
    assert "words" in finding["message"]


def test_body_size_warning_names_heaviest_sections(tmp_path):
    # Push role just over the 800-word warn budget (but under the 1000 fail limit).
    p = _valid_profile()
    p["role"] = p["role"] + (" extra word" * 400)
    pkg = _write_package(tmp_path, profile=p)
    finding = _finding(profile_self_check(pkg), 14)
    assert finding["level"] == "WARNING"
    # The breakdown must point the author at the actual culprit section.
    assert "heaviest" in finding["message"]
    assert "role" in finding["message"]
    assert "over the 800-word budget" in finding["message"]


def test_body_size_fail_includes_breakdown(tmp_path):
    # Way over the 1000-word fail limit still reports the heaviest-section breakdown.
    p = _valid_profile()
    p["role"] = p["role"] + (" extra word" * 700)
    pkg = _write_package(tmp_path, profile=p)
    finding = _finding(profile_self_check(pkg), 14)
    assert finding["level"] == "FAIL"
    assert "heaviest" in finding["message"]
    assert "role" in finding["message"]
