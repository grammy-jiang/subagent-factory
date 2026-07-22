"""Tests for baseline-gating the operating-invariant layer (A3/A5 follow-on)."""

from pathlib import Path

import yaml

from tools.subagent_factory.compile_invariants import strip_invariant_section
from tools.subagent_factory.export_claude_agent import export_claude_agent
from tools.subagent_factory.invariant_policy import (
    recommend_invariants,
    should_attach_invariants,
)

_REPO = Path(__file__).parent.parent.parent

_ADAPTER = """---
name: x
---
## Role

r

## Operating invariants (must hold)

Non-negotiable rules.

- **[PRP-001]** Do the thing first

## When to use

- always
"""


# ---- decision rule (fits the n=3 data) -------------------------------------------------------


def test_decision_rule_matches_observed_data():
    # mysql 0.366 and software-design 0.774 improved -> attach; DDD 0.880 regressed -> skip
    assert should_attach_invariants(0.366)["attach"] is True
    assert should_attach_invariants(0.774)["attach"] is True
    assert should_attach_invariants(0.880)["attach"] is False


def test_decision_rule_boundary():
    assert should_attach_invariants(0.80)["attach"] is False  # >= threshold
    assert should_attach_invariants(0.799)["attach"] is True
    assert should_attach_invariants(0.5, threshold=0.4)["attach"] is False  # custom threshold


# ---- strip ----------------------------------------------------------------------------------


def test_strip_invariant_section_removes_block_keeps_rest():
    out = strip_invariant_section(_ADAPTER)
    assert "## Operating invariants" not in out
    assert "## Role" in out and "## When to use" in out and "always" in out


# ---- recommend (fake runner + grader) --------------------------------------------------------


def _pkg_with_adapter(tmp_path):
    base = tmp_path / "pkg"
    adir = base / "adapters" / "claude-code"
    adir.mkdir(parents=True)
    (adir / "pkg.md").write_text(_ADAPTER, encoding="utf-8")
    tdir = base / "tests"
    tdir.mkdir()
    (tdir / "golden-tests.yaml").write_text(
        yaml.safe_dump(
            {"golden_tests": [{"test_id": "GT-1", "prompt": "p", "expected_route": "invoke"}]}
        ),
        encoding="utf-8",
    )
    return base


def test_recommend_attaches_when_baseline_weak(tmp_path):
    base = _pkg_with_adapter(tmp_path)
    r = recommend_invariants(
        base, runner=lambda _s, _p: "out", grader=lambda _t, _o: {"score": 0.4}
    )
    assert r["attach"] is True and r["baseline"] == 0.4 and r["n_tests"] == 1


def test_recommend_skips_when_baseline_strong(tmp_path):
    base = _pkg_with_adapter(tmp_path)
    r = recommend_invariants(
        base, runner=lambda _s, _p: "out", grader=lambda _t, _o: {"score": 0.95}
    )
    assert r["attach"] is False and r["baseline"] == 0.95


def test_recommend_no_section_to_gate(tmp_path):
    base = tmp_path / "pkg"
    adir = base / "adapters" / "claude-code"
    adir.mkdir(parents=True)
    (adir / "pkg.md").write_text("## Role\nr\n", encoding="utf-8")
    r = recommend_invariants(base, runner=lambda _s, _p: "out")
    assert "error" in r and r["attach"] is False


# ---- export honours the flag -----------------------------------------------------------------


def _export_pkg(tmp_path, attach: bool | None):
    # dir name must equal the profile slug (export's path-traversal guard requires it)
    base = tmp_path / "sdpkg-test-xyz"
    (base / "principles").mkdir(parents=True)
    profile = {
        "slug": "sdpkg-test-xyz",
        "role": "r",
        "when_to_use": ["w"],
        "when_not_to_use": ["n"],
    }
    if attach is not None:
        profile["attach_invariants"] = attach
    (base / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {
                        "principle_id": "PRP-001",
                        "statement": "Do the thing first: because reasons",
                        "derived_from_claims": ["c1"],
                        "confidence": "high",
                        "operational_mapping": {"profile_rule": True},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return base, profile["slug"]


def _run_export(tmp_path, attach):
    base, slug = _export_pkg(tmp_path, attach)
    installed = _REPO / ".claude" / "agents" / "generated" / f"{slug}.md"
    try:
        export_claude_agent(base)
        return (base / "adapters" / "claude-code" / f"{slug}.md").read_text()
    finally:
        installed.unlink(missing_ok=True)  # don't pollute the real generated dir


def test_export_includes_invariants_by_default(tmp_path):
    assert "## Operating invariants" in _run_export(tmp_path, attach=None)


def test_export_omits_invariants_when_flag_false(tmp_path):
    assert "## Operating invariants" not in _run_export(tmp_path, attach=False)
