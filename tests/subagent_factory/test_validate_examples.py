"""Tests for the optional examples slot (A4) — validator + template rendering."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from tools.subagent_factory.export_claude_agent import _build_template_context
from tools.subagent_factory.validate_examples import validate_examples

_REPO = Path(__file__).parent.parent.parent

_GOOD = [
    {
        "title": "Happy path",
        "kind": "happy-path",
        "scenario": "a clean in-scope request",
        "ideal_response": "engage and advise",
    },
    {
        "title": "Recovers from a bad ask",
        "kind": "failure-recovery",
        "scenario": "caller asks for an out-of-lane deliverable",
        "ideal_response": "decline, explain scope, hand off, then offer the in-scope help",
    },
]


def _write_profile(tmp_path, examples) -> Path:
    p = tmp_path / "profile.yaml"
    data = {"slug": "x", "role": "r"}
    if examples is not None:
        data["examples"] = examples
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_absent_examples_passes_trivially(tmp_path):
    assert validate_examples(_write_profile(tmp_path, None)) == []


def test_well_formed_with_recovery_passes(tmp_path):
    assert validate_examples(_write_profile(tmp_path, _GOOD)) == []


def test_happy_path_only_fails_a4(tmp_path):
    errs = validate_examples(_write_profile(tmp_path, [_GOOD[0]]))
    assert any("failure-recovery" in e for e in errs)


def test_missing_field_fails(tmp_path):
    bad = [{"title": "t", "kind": "failure-recovery", "scenario": "s"}]  # no ideal_response
    errs = validate_examples(_write_profile(tmp_path, bad))
    assert any("ideal_response" in e for e in errs)


def test_bad_kind_fails(tmp_path):
    bad = [{**_GOOD[1], "kind": "neither"}]
    errs = validate_examples(_write_profile(tmp_path, bad))
    assert any("not in" in e for e in errs)


def test_empty_examples_list_fails(tmp_path):
    errs = validate_examples(_write_profile(tmp_path, []))
    assert any("non-empty list" in e for e in errs)


# ---- template rendering ----------------------------------------------------------------------


def _render(profile: dict) -> str:
    ctx = _build_template_context(profile)
    env = Environment(loader=FileSystemLoader(str(_REPO / "templates")), autoescape=False)
    return env.get_template("claude-agent-adapter.md.j2").render(**ctx)


def test_examples_render_into_adapter():
    profile = {"slug": "x", "role": "r", "examples": _GOOD}
    out = _render(profile)
    assert "## Worked examples" in out
    assert "Recovers from a bad ask (`failure-recovery`)" in out
    assert "hand off" in out


def test_no_examples_section_when_absent():
    out = _render({"slug": "x", "role": "r"})
    assert "## Worked examples" not in out
