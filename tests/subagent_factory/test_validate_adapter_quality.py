"""Tests for the adapter output-quality gate."""

from tools.subagent_factory.validate_adapter_quality import validate_adapter_quality

_HEADER = "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->\n"
_FRONT = (
    '---\nname: demo\ndescription: "Expert reviewer of demo things"\n'
    "tools: Read, Grep, Glob\nmodel: sonnet\n---\n"
)
_GOOD = (
    _FRONT
    + _HEADER
    + "\n# demo\n\n## Role\n\nExpert reviewer of demo things with real substance.\n\n"
    + "## When to use\n\nWhen the user needs a demo review of their work.\n\n"
    + "## Supported modes and outputs\n\n### `review`\n\nReviews stuff.\n\n"
    + "## Quality bar\n\n- be concrete\n- cite sources\n- avoid vagueness\n- more\n- padding\n"
)


def _adapter(tmp_path, body, slug="demo"):
    base = tmp_path / slug
    (base / "adapters" / "claude-code").mkdir(parents=True)
    (base / "adapters" / "claude-code" / f"{slug}.md").write_text(body, encoding="utf-8")
    return base


def _levels(out):
    return {lvl for lvl, _ in out}


def test_good_adapter_passes(tmp_path):
    assert "FAIL" not in _levels(validate_adapter_quality(_adapter(tmp_path, _GOOD)))


def test_no_adapter_returns_empty(tmp_path):
    (tmp_path / "demo").mkdir()
    assert validate_adapter_quality(tmp_path / "demo") == []


def test_missing_header_fails(tmp_path):
    base = _adapter(tmp_path, _GOOD.replace(_HEADER, ""))
    assert any(lvl == "FAIL" and "DO NOT EDIT" in m for lvl, m in validate_adapter_quality(base))


def test_placeholder_token_fails(tmp_path):
    base = _adapter(tmp_path, _GOOD + "\n## Notes\n\nTODO: finish this section.\n")
    assert any(lvl == "FAIL" and "TODO" in m for lvl, m in validate_adapter_quality(base))


def test_uppercase_placeholder_token_fails(tmp_path):
    base = _adapter(tmp_path, _GOOD + "\n## Notes\n\nReplace PLACEHOLDER with the real value.\n")
    assert any(lvl == "FAIL" and "PLACEHOLDER" in m for lvl, m in validate_adapter_quality(base))


def test_template_placeholder_marker_fails(tmp_path):
    base = _adapter(tmp_path, _GOOD + "\n## Notes\n\nSee <placeholder> for details.\n")
    assert any(lvl == "FAIL" and "placeholder" in m for lvl, m in validate_adapter_quality(base))


def test_lowercase_placeholder_word_in_prose_passes(tmp_path):
    # A real English word in distilled prose is not a stub token (the ``:`` null utility is a
    # "do-nothing placeholder"). Case-sensitive PLACEHOLDER must not false-positive on it.
    body = (
        _GOOD + "\n## Notes\n\nUse `:` as a do-nothing placeholder where a command is required.\n"
    )
    assert not any(
        lvl == "FAIL" and "PLACEHOLDER" in m
        for lvl, m in validate_adapter_quality(_adapter(tmp_path, body))
    )


def test_stub_token_inside_compiled_invariant_line_passes(tmp_path):
    # Compiled ``- **[Pxxx]** …`` lines are rendered verbatim from an already-validated spine, so a
    # stub token there is grounded source content, not an unfinished profile field. Regression:
    # mcp-quality-advisor's P167 legitimately reads "leaving TODO rows for ambiguity", and failing
    # on it drove the package to set ``attach_invariants: false``, dropping its whole must-hold layer.
    body = (
        _GOOD
        + "\n## Operating invariants (must hold)\n\n"
        + "- **[P167]** Author traceability YAML mapping each normative sentence to a check, "
        + "leaving TODO rows for ambiguity\n"
    )
    assert not any(
        lvl == "FAIL" and "TODO" in m
        for lvl, m in validate_adapter_quality(_adapter(tmp_path, body))
    )


def test_stub_token_in_invariant_section_prose_still_fails(tmp_path):
    # Only the compiled ``- **[Pxxx]** …`` lines are exempt — prose inside the same section is not.
    body = (
        _GOOD
        + "\n## Operating invariants (must hold)\n\nTODO: write the invariant preamble.\n\n"
        + "- **[P001]** Do the grounded thing\n"
    )
    assert any(
        lvl == "FAIL" and "TODO" in m
        for lvl, m in validate_adapter_quality(_adapter(tmp_path, body))
    )


def test_stub_status_marker_fails(tmp_path):
    base = _adapter(tmp_path, _GOOD + "\n> **STATUS: STUB**\n")
    assert any(lvl == "FAIL" and "STATUS: STUB" in m for lvl, m in validate_adapter_quality(base))


def test_missing_required_section_fails(tmp_path):
    base = _adapter(
        tmp_path,
        _GOOD.replace("## Role\n\nExpert reviewer of demo things with real substance.\n\n", ""),
    )
    assert any(lvl == "FAIL" and "## Role" in m for lvl, m in validate_adapter_quality(base))


def test_empty_required_section_warns(tmp_path):
    body = _HEADER + "\n## Role\n\n## When to use\n\nw\n" + "padding line\n" * 20
    out = validate_adapter_quality(_adapter(tmp_path, body))
    assert any(lvl == "WARN" and "## Role" in m and "empty" in m for lvl, m in out)


def test_too_short_warns(tmp_path):
    body = _HEADER + "## Role\n\nr\n\n## When to use\n\nw\n"
    out = validate_adapter_quality(_adapter(tmp_path, body))
    assert any(lvl == "WARN" and "stub" in m for lvl, m in out)
