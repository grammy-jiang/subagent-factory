"""Tests for the hardened package validation gating (GAP 4)."""

import json

import yaml

import tools.subagent_factory.validate_generated_package as vgp

# A substantive adapter body that passes the adapter-quality gate (header + load-bearing
# sections + length). Canonical and matching-installed adapters use this identical content.
_ADAPTER_BODY = (
    '---\nname: agent\ndescription: "Expert reviewer with real substance"\n'
    "tools: Read, Grep, Glob\nmodel: sonnet\n---\n"
    "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->\n\n# agent\n\n"
    "## Role\n\nExpert reviewer with real substance.\n\n"
    "## When to use\n\nWhen the user needs a review.\n\n"
    "## Supported modes and outputs\n\n### `review`\n\nReviews.\n\n"
    "## Quality bar\n\n- concrete\n- grounded\n- padding\n- padding\n- padding\n- padding\n"
)


def _write_metadata(pkg, source_id="s1", sha256="abc"):
    meta_dir = pkg / "sources" / "metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)
    (meta_dir / f"{source_id}.metadata.json").write_text(
        json.dumps({"source_id": source_id, "sha256": sha256}), encoding="utf-8"
    )


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
            "modes": [
                {
                    "name": "review",
                    "trigger": "an artifact is submitted",
                    "output": "named red flags with recommendations",
                }
            ],
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
        "knowledge_partition": {
            "always_on": [],
            "skills": [],
            "references": [],
            "mcp": [],
            "caller_supplied": [],
        },
        "sources": [{"source_id": "s1", "title": "A Book", "sha256": "abc"}],
    }


def _build(
    tmp_path,
    monkeypatch,
    installed="match",
    with_test_results=True,
    with_tests=True,
    with_faithfulness=True,
):
    repo = tmp_path / "repo"
    monkeypatch.setattr(vgp, "_REPO_ROOT", repo)
    slug = "demo-design-reviewer"
    pkg = repo / "subagents" / slug
    pkg.mkdir(parents=True)

    (pkg / "profile.yaml").write_text(yaml.safe_dump(_valid_profile()), encoding="utf-8")
    (pkg / "provenance-ledger.md").write_text(
        "# Provenance Ledger\n\n" + ("detail. " * 60), encoding="utf-8"
    )
    (pkg / "source-pack.manifest.yaml").write_text(
        yaml.safe_dump(
            {"schema_version": "source-pack-manifest-v1", "subagent_slug": slug, "sources": []}
        ),
        encoding="utf-8",
    )
    (pkg / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")

    if with_faithfulness:
        reports_dir = pkg / "reports"
        reports_dir.mkdir()
        (reports_dir / "faithfulness-report.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": "faithfulness-report-v1",
                    "subagent_slug": slug,
                    "findings": [
                        {
                            "rule_ref": "quality_bar[0]",
                            "verdict": "EXACT_SUPPORT",
                            "distortion": ["none"],
                            "support_granularity": "section",
                            "severity": "low",
                            "action": "accept_with_note",
                            "note": "matches source",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    adapter_dir = pkg / "adapters" / "claude-code"
    adapter_dir.mkdir(parents=True)
    (adapter_dir / f"{slug}.md").write_text(_ADAPTER_BODY, encoding="utf-8")

    gen_dir = repo / ".claude" / "agents" / "generated"
    gen_dir.mkdir(parents=True)
    if installed == "match":
        (gen_dir / f"{slug}.md").write_text(_ADAPTER_BODY, encoding="utf-8")
    elif installed == "mismatch":
        (gen_dir / f"{slug}.md").write_text("STALE-DIFFERENT-CONTENT", encoding="utf-8")
    # installed == "absent": create nothing

    if with_tests:
        tests_dir = pkg / "tests"
        tests_dir.mkdir()
        (tests_dir / "golden-tests.yaml").write_text(
            yaml.safe_dump(
                {
                    "golden_tests": [{"test_id": f"GT-{i:03d}"} for i in range(3)],
                    "negative_routing_tests": [{"test_id": "NR-001"}],
                }
            ),
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


def test_missing_faithfulness_report_fails(tmp_path, monkeypatch):
    # Faithfulness is required at all tiers (gate promoted from min_tier 99 -> 0).
    pkg, _ = _build(tmp_path, monkeypatch, with_faithfulness=False)
    result = vgp.validate_generated_package(pkg)
    assert not result["passed"]
    assert "tier-artifact" in _fail_checks(result)


def test_missing_tests_dir_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch, with_tests=False)
    result = vgp.validate_generated_package(pkg)
    assert "tests" in _fail_checks(result)
    assert result["passed"] is False


def test_source_provenance_match_ok(tmp_path, monkeypatch):
    # profile sha256 "abc" matches the ingested metadata → traceable.
    # (The minimal metadata fixture fails the separate schema check, so this
    # isolates the source-provenance finding rather than overall pass.)
    pkg, _ = _build(tmp_path, monkeypatch)
    _write_metadata(pkg, source_id="s1", sha256="abc")
    result = vgp.validate_generated_package(pkg)
    assert "source-provenance" not in _fail_checks(result)
    assert any(f["check"] == "source-provenance" and f["level"] == "OK" for f in result["findings"])


def test_source_provenance_sha_mismatch_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch)
    _write_metadata(pkg, source_id="s1", sha256="deadbeef")
    result = vgp.validate_generated_package(pkg)
    assert "source-provenance" in _fail_checks(result)
    assert result["passed"] is False


def test_source_provenance_unknown_source_id_fails(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch)
    _write_metadata(pkg, source_id="other-source", sha256="abc")
    result = vgp.validate_generated_package(pkg)
    assert "source-provenance" in _fail_checks(result)
    assert result["passed"] is False


def test_source_provenance_empty_sha_warns_not_fails(tmp_path, monkeypatch):
    profile = _valid_profile()
    profile["sources"] = [{"source_id": "s1", "title": "A Book", "sha256": ""}]
    pkg, _ = _build(tmp_path, monkeypatch)
    (pkg / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    _write_metadata(pkg, source_id="s1", sha256="abc")
    result = vgp.validate_generated_package(pkg)
    assert "source-provenance" not in _fail_checks(result)
    assert any(
        f["check"] == "source-provenance" and f["level"] == "WARN" for f in result["findings"]
    )


def _required_dir_warns(result):
    return [
        f["message"]
        for f in result["findings"]
        if f["check"] == "required-dirs" and f["level"] == "WARN"
    ]


def test_distillation_only_omits_verbatim_dirs_without_warning(tmp_path, monkeypatch):
    # distillation-only sources → sources/{original,markdown} hold copyrighted verbatim and are
    # withheld by the rights policy; their absence must NOT warn (rights-clean export).
    pkg, _ = _build(tmp_path, monkeypatch)
    md = pkg / "sources" / "metadata"
    md.mkdir(parents=True, exist_ok=True)
    (md / "s1.metadata.json").write_text(
        json.dumps({"source_id": "s1", "sha256": "abc", "rights_status": "distillation-only"}),
        encoding="utf-8",
    )
    warns = _required_dir_warns(vgp.validate_generated_package(pkg))
    assert not any("sources/original" in w or "sources/markdown" in w for w in warns)


def test_open_rights_still_warns_missing_verbatim_dirs(tmp_path, monkeypatch):
    # openly-licensed sources can be committed → absent verbatim dirs still warn.
    pkg, _ = _build(tmp_path, monkeypatch)
    md = pkg / "sources" / "metadata"
    md.mkdir(parents=True, exist_ok=True)
    (md / "s1.metadata.json").write_text(
        json.dumps({"source_id": "s1", "sha256": "abc", "rights_status": "open"}),
        encoding="utf-8",
    )
    warns = _required_dir_warns(vgp.validate_generated_package(pkg))
    assert any("sources/original" in w for w in warns)
    assert any("sources/markdown" in w for w in warns)


def _warn_checks(result):
    return {f["check"] for f in result["findings"] if f["level"] == "WARN"}


def test_tier_underdeclaration_warns_not_fails(tmp_path, monkeypatch):
    # Profile omits `tier:` (reads as Tier 0) but the manifest carries 2 sources, so
    # classify_tier computes Tier 2. The package under-declares its tier and would
    # silently dodge the evidence chain — validate must WARN, but still pass.
    pkg, slug = _build(tmp_path, monkeypatch)
    (pkg / "source-pack.manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "source-pack-manifest-v1",
                "subagent_slug": slug,
                "sources": [{"source_id": "s1"}, {"source_id": "s2"}],
            }
        ),
        encoding="utf-8",
    )
    result = vgp.validate_generated_package(pkg)
    assert "tier-consistency" in _warn_checks(result)
    assert "tier-consistency" not in _fail_checks(result)


def test_tier_consistency_ok_when_declared_matches(tmp_path, monkeypatch):
    # Profile declares tier 2 and the manifest has 2 sources → no drift, OK finding.
    pkg, slug = _build(tmp_path, monkeypatch)
    profile = _valid_profile()
    profile["tier"] = 2
    (pkg / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    (pkg / "source-pack.manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "source-pack-manifest-v1",
                "subagent_slug": slug,
                "sources": [{"source_id": "s1"}, {"source_id": "s2"}],
            }
        ),
        encoding="utf-8",
    )
    result = vgp.validate_generated_package(pkg)
    assert "tier-consistency" not in _warn_checks(result)
    assert any(f["check"] == "tier-consistency" and f["level"] == "OK" for f in result["findings"])


def test_phase8_fail_propagates_to_validation(tmp_path, monkeypatch):
    pkg, _ = _build(tmp_path, monkeypatch)
    # Corrupt the profile so the Phase 8 gate fails (only 1 trigger).
    profile = _valid_profile()
    profile["when_to_use"] = profile["when_to_use"][:1]
    (pkg / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    result = vgp.validate_generated_package(pkg)
    assert "phase8" in _fail_checks(result)
    assert result["passed"] is False
