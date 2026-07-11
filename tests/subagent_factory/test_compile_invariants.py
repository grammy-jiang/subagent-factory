"""Tests for the must-hold invariant layer (A3 + A5) — compile, render, coverage gate."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from tools.subagent_factory.compile_invariants import (
    _to_invariant,
    compile_invariants,
    validate_invariant_coverage,
)
from tools.subagent_factory.export_claude_agent import _build_template_context

_REPO = Path(__file__).parent.parent.parent

_PRINCIPLES = [
    {
        "principle_id": "PRP-001",
        "statement": "Review the identity model first: because you cannot authorize before you "
        "authenticate.",
        "confidence": "high",
        "operational_mapping": {"profile_rule": True},
    },
    {
        "principle_id": "PRP-002",
        "statement": "Prefer short-lived tokens.",
        "confidence": "medium",  # not high -> excluded
        "operational_mapping": {"profile_rule": True},
    },
    {
        "principle_id": "PRP-003",
        "statement": "Log access decisions for audit.",
        "confidence": "high",
        "operational_mapping": {"profile_rule": False},  # not a profile rule -> excluded
    },
]


# ---- _to_invariant ---------------------------------------------------------------------------


def test_to_invariant_keeps_the_colon_tail():
    # The rule tail after a colon carries operative detail (a concrete rule, or a safety hedge);
    # it must survive — dropping it silently gutted P146's warning-severity caveat in the adapter.
    assert (
        _to_invariant("Apply the hierarchy: verify it against the governing standard")
        == "Apply the hierarchy: verify it against the governing standard"
    )


def test_to_invariant_first_sentence_when_multi_sentence():
    assert _to_invariant("Keep it simple. Other detail follows.") == "Keep it simple"


def test_to_invariant_never_truncates_mid_clause():
    # A long single sentence (no internal sentence break) renders in FULL — no "…" cut, so a
    # safety rule cannot lose its own conditions. P146's statement has no colon/period internally,
    # exactly the shape that previously fell through to a 160-char mid-clause cut.
    stmt = (
        "Translate warnings with particular care — it can be life or death — and verify the "
        "severity hierarchy against the governing standard rather than assuming any single ordering"
    )
    out = _to_invariant(stmt)
    assert "…" not in out and out == stmt


# ---- compile_invariants ----------------------------------------------------------------------


def test_compile_selects_only_high_confidence_profile_rules():
    invs = compile_invariants(_PRINCIPLES)
    assert [i["principle_id"] for i in invs] == ["PRP-001"]
    # First sentence in full (colon tail kept) — no head-before-colon reduction.
    assert (
        invs[0]["invariant"]
        == "Review the identity model first: because you cannot authorize before you authenticate"
    )


def test_compile_empty_when_none_qualify():
    assert compile_invariants([_PRINCIPLES[1], _PRINCIPLES[2]]) == []


# ---- template rendering ----------------------------------------------------------------------


def _render(profile: dict, invariants: list[dict]) -> str:
    ctx = _build_template_context(profile)
    ctx["invariants"] = invariants
    env = Environment(loader=FileSystemLoader(str(_REPO / "templates")), autoescape=False)
    return env.get_template("claude-agent-adapter.md.j2").render(**ctx)


def test_invariant_section_renders_with_ids():
    out = _render({"slug": "x", "role": "r"}, compile_invariants(_PRINCIPLES))
    assert "## Operating invariants (must hold)" in out
    assert "**[PRP-001]** Review the identity model first" in out


def test_no_invariant_section_when_empty():
    out = _render({"slug": "x", "role": "r"}, [])
    assert "## Operating invariants" not in out


# ---- validate_invariant_coverage -------------------------------------------------------------


def _pkg(tmp_path, principles, adapter_body: str | None) -> Path:
    base = tmp_path / "mypkg"
    (base / "principles").mkdir(parents=True)
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    if adapter_body is not None:
        adir = base / "adapters" / "claude-code"
        adir.mkdir(parents=True)
        (adir / "mypkg.md").write_text(adapter_body, encoding="utf-8")
    return base / "principles" / "principles.yaml"


def test_coverage_passes_when_no_must_hold(tmp_path):
    p = _pkg(tmp_path, [_PRINCIPLES[1]], "no invariant section here")
    assert validate_invariant_coverage(p) == []


def test_coverage_skips_pre_feature_adapter(tmp_path):
    # adapter has no invariant section -> not gated (non-breaking for the existing packages)
    p = _pkg(tmp_path, _PRINCIPLES, "## Role\nsome body, no invariants section")
    assert validate_invariant_coverage(p) == []


def test_coverage_passes_when_section_covers_all(tmp_path):
    body = "## Operating invariants (must hold)\n- **[PRP-001]** Review the identity model first"
    p = _pkg(tmp_path, _PRINCIPLES, body)
    assert validate_invariant_coverage(p) == []


def test_coverage_fails_on_stale_section(tmp_path):
    # section exists but is missing a must-hold principle -> stale adapter
    body = "## Operating invariants (must hold)\n- **[PRP-999]** something unrelated"
    p = _pkg(tmp_path, _PRINCIPLES, body)
    errs = validate_invariant_coverage(p)
    assert errs and "PRP-001" in errs[0]


def test_coverage_fails_on_truncated_invariant(tmp_path):
    # Every id is present, but an invariant was truncated mid-clause (trailing "…") — content did
    # not survive, so coverage-by-tag alone must not pass it (this is what shipped a gutted P146).
    body = (
        "## Operating invariants (must hold)\n"
        "- **[PRP-001]** Review the identity model first: because you cannot au…\n"
        "\n## When to use\n- always"
    )
    p = _pkg(tmp_path, _PRINCIPLES, body)
    errs = validate_invariant_coverage(p)
    assert errs and "truncates" in errs[0]
