"""Regression tests for Claude Code adapter description composition.

Pins the fix for the Phase 9 export defect where the adapter `description`
was blindly char-truncated, producing a malformed string: the role was cut
mid-phrase to a dangling preposition ("...structures for"), pieces were glued
with a literal " | ", and the whole string was clipped mid-trigger
("...experiencing change").
"""

from tools.subagent_factory.export_claude_agent import (
    _TRAILING_CONNECTORS,
    _clean_clause,
    _compose_description,
    _drop_dangling_open_paren,
    _neutralize_inner_dashes,
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


def test_clean_clause_drops_truncated_colon_list():
    # A truncated "label: list" must drop back to before the colon, not end
    # mid-enumeration (e.g. "...strategy: pattern" from "...: pattern, eviction, …").
    text = (
        "Senior caching architect who guides engineering teams and technical decision-makers "
        "on caching strategy: pattern selection, eviction and TTL policy, consistency, scaling"
    )
    out = _clean_clause(text, 120)
    assert out.endswith("caching strategy")
    assert ":" not in out


def test_clean_clause_drops_dangling_relative_pronoun():
    text = "Latency is rising and the team must decide whether and where to cache and which pattern fits"
    out = _clean_clause(text, 85)
    assert out.split()[-1].lower() not in _TRAILING_CONNECTORS
    assert not out.endswith("which")


def test_clean_clause_takes_first_sentence_only():
    out = _clean_clause("First sentence here. Second sentence follows.", 200)
    assert out == "First sentence here"


def test_compose_drops_whole_pieces_when_over_budget():
    # A tiny budget must still yield a well-formed prefix, never a mid-clause cut.
    desc = _compose_description(SAMPLE_PROFILE, max_chars=90)
    assert len(desc) <= 90
    assert " | " not in desc
    assert desc.split()[-1].lower() not in _TRAILING_CONNECTORS


# A profile whose role and triggers carry parentheticals long enough that a
# clause-boundary clip can land inside a "(...)" group, mirroring the real
# microservice-patterns-advisor and kafka profiles that exposed the defect.
PAREN_PROFILE = {
    "role": (
        "An advisor who maps a microservice architecture concern onto the "
        "relevant patterns in the microservices pattern language and explains "
        "each candidate pattern's purpose and trade-offs."
    ),
    "when_to_use": [
        "The caller is deciding how to decompose an application into services "
        "(decompose by business capability, decompose by subdomain, "
        "self-contained service, service per team) and wants the applicable "
        "patterns.",
        "The caller is choosing an inter-service communication style (Messaging, "
        "Remote procedure invocation, API gateway, Circuit breaker) and wants "
        "the candidate patterns named.",
    ],
    "when_not_to_use": [
        "The caller wants implementation or configuration of a pattern in a "
        "specific language, framework, or product (Spring, Kubernetes, a "
        "particular broker) rather than a pattern recommendation.",
    ],
}


def test_clean_clause_drops_dangling_open_paren():
    # Clip lands right after an opening paren; the dangling "(decompose ..." must
    # be removed so the clause is paren-balanced, not a broken fragment.
    text = "The caller is deciding how to decompose an application into services (decompose by business capability)"
    out = _clean_clause(text, 70)
    assert out.count("(") == out.count(")")
    assert "(decompose" not in out
    assert not out.endswith("(")


def test_drop_dangling_open_paren_unit():
    assert _drop_dangling_open_paren("generations (e.g") == "generations"
    assert _drop_dangling_open_paren("concerns (CI/CD pipelines") == "concerns"
    # A balanced inner group followed by a dangling outer one keeps the balanced part.
    assert (
        _drop_dangling_open_paren("outer (inner) then dangling (oops")
        == "outer (inner) then dangling"
    )


def test_drop_dangling_open_paren_leaves_balanced_text_untouched():
    for s in ("no parens at all", "fully balanced (yes) text", "a (b) c (d) e"):
        assert _drop_dangling_open_paren(s) == s


def test_description_has_balanced_parentheses():
    # The composed router description must never contain an unmatched paren —
    # a dangling "(" reads as a broken, mid-clause fragment to the router.
    desc = _compose_description(PAREN_PROFILE)
    assert desc.count("(") == desc.count(")")
    assert "(decompose" not in desc
    assert desc.split()[-1].lower() not in _TRAILING_CONNECTORS


# A profile whose role and triggers use em/en dashes as appositive punctuation,
# mirroring the real xv6-kernel-internals-reviewer profile that exposed the
# defect: a content em dash inside a clipped trigger collides with the literal
# " — " section join, so the router cannot tell the boundary from punctuation.
EMDASH_PROFILE = {
    "role": (
        "An expert who explains and critiques the internals of a small "
        "Unix-like teaching operating-system kernel."
    ),
    "when_to_use": [
        "An engineer suspects a concurrency defect in kernel-style code — a "
        "race, a lock acquired out of order that risks deadlock, a missing "
        "memory barrier, or a lost wakeup — and wants it located.",
        "A reader studying the file system needs its layered design – buffer "
        "cache, logging layer, inodes – explained.",
    ],
    "when_not_to_use": [
        "Operating a production OS — kernel build flags, package management — "
        "rather than understanding the teaching kernel.",
    ],
}


def test_neutralize_inner_dashes_demotes_em_and_en_dashes_to_commas():
    assert _neutralize_inner_dashes("code — a race") == "code, a race"
    assert _neutralize_inner_dashes("design – buffer cache") == "design, buffer cache"
    # Tight (un-spaced) dashes are normalized too.
    assert _neutralize_inner_dashes("a—b") == "a, b"


def test_neutralize_inner_dashes_leaves_hyphens_and_slashes_untouched():
    for s in ("user/kernel boundary", "copy-on-write fork", "Unix-like kernel"):
        assert _neutralize_inner_dashes(s) == s


def test_clean_clause_demotes_inner_em_dash():
    # The clipped clause must not carry an em dash that would later be confused
    # with the structural " — " join in the composed description.
    out = _clean_clause(
        "An engineer suspects a concurrency defect in kernel-style code — a race", 200
    )
    assert "—" not in out
    assert "code, a race" in out


def test_description_em_dash_only_marks_section_boundaries():
    # Every em dash in the final description must be a structural section join
    # (" — Use when:" / " — Not for:"), never leftover content punctuation.
    desc = _compose_description(EMDASH_PROFILE)
    import re as _re

    total_em = desc.count("—")
    structural = len(_re.findall(r" — (?:Use when:|Not for:)", desc))
    assert total_em == structural, f"content em dash leaked into description: {desc!r}"
    # En dashes must not survive in the clauses either.
    assert "–" not in desc
