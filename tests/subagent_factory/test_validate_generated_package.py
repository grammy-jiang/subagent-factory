"""Tests for the hardened package validation gating (GAP 4)."""

import yaml

import tools.subagent_factory.validate_generated_package as vgp


def _valid_profile() -> dict:
    return {
        "schema_version": "portable-profile-v1",
        "slug": "demo-design-reviewer",
        "display_name": "Demo Design Reviewer",
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
        "inputs": {"required": ["The actual code or interface definition being reviewed."]},
        "outputs": {
            "primary_format": "annotated design critique",
            "modes": [{"name": "review", "trigger": "an artifact is submitted",
                       "output": "named red flags with recommendations"}],
        },
        "quality_bar": [
            "Every finding cites a named design principle from the source.",
            "Recommendations reference specific evidence, not a style preference.",
            "Module depth is addressed with explicit reference to the principle.",
        ],
        "minimum_useful_output": "At least one named red flag with an explanation.",
        "forbidden_behaviours": ["Do not approve a design purely because tests pass."],
        "handoff_rules": ["Findings return to the module owner."],
        "source_of_truth_policy": {
            "canonical_owner": "the developer who owns the module",
            "may_edit_canonical": False,
            "precedence": "The canonical source is the cited design book.",
        },
        "knowledge_partition": {"always_on": [], "skills": [], "references": [], "mcp": [], "caller_supplied": []},
        "sources": [{"source_id": "s1", "title": "A Book", "sha256": "abc"}],
    }


def _build(tmp_path, monkeypatch, installed="match", with_test_results=True, with_tests=True):
    repo = tmp_path / "repo"
    monkeypatch.setattr(vgp, "_REPO_ROOT", repo)
    slug = "demo-design-reviewer"
    pkg = repo / "subagents" / slug
    pkg.mkdir(parents=True)

    (pkg / "profile.yaml").write_text(yaml.safe_dump(_valid_profile()), encoding="utf-8")
    (pkg / "provenance-ledger.md").write_text("# Provenance Ledger\n\n" + ("detail. " * 60), encoding="utf-8")
    (pkg / "source-pack.manifest.yaml").write_text(
        yaml.safe_dump({"schema_version": "source-pack-manifest-v1", "subagent_slug": slug, "sources": []}),
        encoding="utf-8",
    )
    (pkg / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")

    adapter_dir = pkg / "adapters" / "claude-code"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / f"{slug}.md").write_text("ADAPTER-CONTENT", encoding="utf-8")

    gen_dir = repo / ".claude" / "agents" / "generated"
    gen_dir.mkdir(parents=True)
    if installed == "match":
        (gen_dir / f"{slug}.md").write_text("ADAPTER-CONTENT", encoding="utf-8")
    elif installed == "mismatch":
        (gen_dir / f"{slug}.md").write_text("STALE-DIFFERENT-CONTENT", encoding="utf-8")
    # installed == "absent": create nothing

    if with_tests:
        tests_dir = pkg / "tests"
        tests_dir.mkdir()
        (tests_dir / "golden-tests.yaml").write_text(
            yaml.safe_dump({
                "golden_tests": [{"test_id": f"GT-{i:03d}"} for i in range(3)],
                "negative_routing_tests": [{"test_id": "NR-001"}],
            }),
            encoding="utf-8",
        )
        if with_test_results:
            (tests_dir / "test-results.md").write_text("# Test Results\n", encoding="utf-8")
    return pkg, slug


def _fail_checks(result):
    return {f["check"] for f in result["findings"] if f["level"] == "FAIL"}


def test_complete_package_passes(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch)
    result = vgp.validate_generated_package(pkg)
    assert result["passed"] is True, _fail_checks(result)


def test_missing_installed_adapter_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch, installed="absent")
    result = vgp.validate_generated_package(pkg)
    assert "adapter-installed" in _fail_checks(result)
    assert result["passed"] is False


def test_adapter_sync_mismatch_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch, installed="mismatch")
    result = vgp.validate_generated_package(pkg)
    assert "adapter-sync" in _fail_checks(result)
    assert result["passed"] is False


def test_missing_test_results_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch, with_test_results=False)
    result = vgp.validate_generated_package(pkg)
    assert "test-results" in _fail_checks(result)
    assert result["passed"] is False


def test_missing_tests_dir_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch, with_tests=False)
    result = vgp.validate_generated_package(pkg)
    assert "tests" in _fail_checks(result)
    assert result["passed"] is False


def test_phase8_fail_propagates_to_validation(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch)
    # Corrupt the profile so the Phase 8 gate fails (only 1 trigger).
    profile = _valid_profile()
    profile["when_to_use"] = profile["when_to_use"][:1]
    (pkg / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    result = vgp.validate_generated_package(pkg)
    assert "phase8" in _fail_checks(result)
    assert result["passed"] is False
