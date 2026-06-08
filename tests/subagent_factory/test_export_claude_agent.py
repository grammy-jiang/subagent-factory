"""Regression tests for Claude Code adapter description composition.

Pins the fix for the Phase 9 export defect where the adapter `description`
was blindly char-truncated, producing a malformed string: the role was cut
mid-phrase to a dangling preposition ("...structures for"), pieces were glued
with a literal " | ", and the whole string was clipped mid-trigger
("...experiencing change").
"""

from tools.subagent_factory.export_claude_agent import (
    _clean_clause,
    _compose_description,
    _TRAILING_CONNECTORS,
)


# A profile whose role and triggers are all longer than their clause budgets,
# mirroring the real software-design-reviewer profile that exposed the bug.
SAMPLE_PROFILE = {
    "role": (
        "An expert reviewer who evaluates software designs and code structures "
        "for complexity, applying principles of modular design, information "
        "hiding, deep modules, and strategic programming to identify red flags "
        "and guide structural improvements."
    ),
    "when_to_use": [
        "A developer submits a class or module for design review before merging "
        "and wants to know whether its interface is deeper than its "
        "implementation or exposes too many details.",
        "A team is experiencing change amplification — a small feature requires "
        "modifications in many places — and needs a diagnosis of where "
        "information is leaking between modules.",
    ],
    "when_not_to_use": [
        "The request is solely to fix bugs, add features, or optimise "
        "performance without any design-structure question — that is "
        "implementation or debugging work, not a design review.",
    ],
}


def test_description_has_no_pipe_separator():
    desc = _compose_description(SAMPLE_PROFILE)
    assert " | " not in desc
    assert "Use when: |" not in desc


def test_description_role_not_truncated_to_dangling_preposition():
    desc = _compose_description(SAMPLE_PROFILE)
    role_part = desc.split(" — ")[0]
    # The original defect ended the role at "...code structures for" and glued
    # it to "| Use when". The role clause must end on a content word.
    assert not role_part.endswith(" for")
    assert role_part.split()[-1].lower() not in _TRAILING_CONNECTORS
    assert "for | " not in desc


def test_description_includes_role_trigger_and_exclusion():
    desc = _compose_description(SAMPLE_PROFILE)
    assert desc.startswith("An expert reviewer")
    assert "Use when:" in desc
    assert "Not for:" in desc


def test_description_within_budget():
    desc = _compose_description(SAMPLE_PROFILE, max_chars=320)
    assert len(desc) <= 320


def test_description_does_not_end_on_connector():
    desc = _compose_description(SAMPLE_PROFILE)
    last_word = desc.rstrip(" .;,—").split()[-1].lower()
    assert last_word not in _TRAILING_CONNECTORS


def test_description_role_ends_at_clause_boundary():
    desc = _compose_description(SAMPLE_PROFILE)
    role_part = desc.split(" — ")[0]
    # Clipped at the comma after "complexity", not mid-phrase.
    assert role_part.endswith("complexity")


def test_clean_clause_collapses_whitespace_and_strips_trailing_period():
    out = _clean_clause("  Hello   world.  ", 100)
    assert out == "Hello world"


def test_clean_clause_drops_dangling_connector():
    text = "An expert reviewer who evaluates software designs and code structures for complexity"
    # Budget forces a cut right after "...structures for"; the dangling
    # connector must be removed rather than left trailing.
    out = _clean_clause(text, 73)
    assert not out.endswith(" for")
    assert out.split()[-1].lower() not in _TRAILING_CONNECTORS


def test_clean_clause_takes_first_sentence_only():
    out = _clean_clause("First sentence here. Second sentence follows.", 200)
    assert out == "First sentence here"


def test_compose_drops_whole_pieces_when_over_budget():
    # A tiny budget must still yield a well-formed prefix, never a mid-clause cut.
    desc = _compose_description(SAMPLE_PROFILE, max_chars=90)
    assert len(desc) <= 90
    assert " | " not in desc
    assert desc.split()[-1].lower() not in _TRAILING_CONNECTORS
