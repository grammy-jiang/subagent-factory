"""Tests for the patch-safety policy validator + the mode-conditional gate block (Step 6)."""

import yaml

import tools.subagent_factory.validate_generated_package as vgp
from tools.subagent_factory.validate_patch_policy import validate_patch_policy

_GOOD_POL = {
    "schema_version": "patch-policy-v1",
    "default_mode": "patch_suggest_only",
    "direct_patch_allowed_when": ["user_explicitly_requests_patch", "patch_scope_is_bounded"],
    "must_not": ["silently_edit_canonical_artifacts", "patch_without_risk_explanation"],
}


def _policy(tmp_path, data):
    p = tmp_path / "patch-policy.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


# ── validator unit tests ──────────────────────────────────────────────────────
def test_valid_policy(tmp_path):
    assert validate_patch_policy(_policy(tmp_path, _GOOD_POL)) == []


def test_bad_default_mode_is_schema_error(tmp_path):
    assert validate_patch_policy(_policy(tmp_path, {**_GOOD_POL, "default_mode": "yolo"}))


def test_direct_patch_requires_explicit_request(tmp_path):
    bad = {
        **_GOOD_POL,
        "default_mode": "direct_patch",
        "direct_patch_allowed_when": ["target_files_are_supplied"],
    }
    assert any(
        "user_explicitly_requests_patch" in e for e in validate_patch_policy(_policy(tmp_path, bad))
    )


# ── gate block: mode-conditional requiredness ────────────────────────────────
def _min_pkg(tmp_path, modes, policy=None):
    base = tmp_path / "pkg"
    base.mkdir()
    profile = {"slug": "demo", "outputs": {"modes": [{"name": n} for n in modes]}}
    (base / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    if policy is not None:
        (base / "policy").mkdir()
        (base / "policy" / "patch-policy.yaml").write_text(yaml.safe_dump(policy), encoding="utf-8")
    return base


def _fail_checks(result):
    return {f["check"] for f in result["findings"] if f["level"] == "FAIL"}


def test_patch_mode_without_policy_fails(tmp_path):
    res = vgp.validate_generated_package(_min_pkg(tmp_path, ["produce"]))
    assert "patch-policy" in _fail_checks(res)


def test_readonly_mode_needs_no_policy(tmp_path):
    res = vgp.validate_generated_package(_min_pkg(tmp_path, ["review"]))
    assert "patch-policy" not in _fail_checks(res)


def test_valid_policy_present_passes_patch_check(tmp_path):
    res = vgp.validate_generated_package(_min_pkg(tmp_path, ["patch-suggest"], policy=_GOOD_POL))
    assert "patch-policy" not in _fail_checks(res)
