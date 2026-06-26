"""Tests for the skill/reference authoring validator (Step 8) — status-gated."""

import yaml

from tools.subagent_factory.validate_skill_authoring import validate_skill_authoring

STUB_SKILL = (
    "---\nname: alpha-skill\nkind: skill\nstatus: stub\n"
    "provenance:\n  principles: []\n  claims: []\n  source_anchors: []\n---\n\n"
    "# Alpha\n\n> **STATUS: STUB — not yet authored.**\n\n## Purpose\n\nx\n\n"
    "## Procedure\n\nTODO: author the repeatable steps for this skill.\n"
)


def _authored_skill(principles=(), claims=(), anchors=(), evidence=()) -> str:
    prov = {
        "principles": list(principles),
        "claims": list(claims),
        "evidence": list(evidence),
        "source_anchors": list(anchors),
    }
    fm = yaml.safe_dump(
        {"name": "alpha-skill", "kind": "skill", "status": "ready", "provenance": prov}
    )
    return (
        f"---\n{fm}---\n\n# Alpha\n\n## Purpose\n\nReal purpose.\n\n"
        "## When to use\n\nWhen X.\n\n## Procedure\n\n1. Do the thing.\n\n"
        "## Inputs\n\ny\n\n## Output\n\nz\n\n## Provenance\n\nFrom the source.\n"
    )


def _pkg(
    tmp_path, status="draft", skills=None, refs=None, files=None, principles=None, evidence=None
):
    """Build a package dir. ``skills``/``refs`` are slug lists (== knowledge_partition entries);
    ``files`` maps a relative path under base to file content (the authored/stub bodies)."""
    base = tmp_path / "pkg"
    base.mkdir(parents=True, exist_ok=True)
    profile = {
        "status": status,
        "knowledge_partition": {"skills": list(skills or []), "references": list(refs or [])},
    }
    (base / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    if evidence is not None:
        (base / "evidence").mkdir(parents=True, exist_ok=True)
        (base / "evidence" / "evidence-records.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": "evidence-records-v1",
                    "evidence_records": [
                        {"evidence_id": e, "claim_id": "c1", "source_ids": ["s1"]} for e in evidence
                    ],
                }
            ),
            encoding="utf-8",
        )
    if principles is not None:
        (base / "principles").mkdir(parents=True, exist_ok=True)
        (base / "principles" / "principles.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": "principles-v1",
                    "principles": [
                        {
                            "principle_id": p,
                            "statement": "s",
                            "derived_from_claims": ["C-1"],
                            "confidence": "high",
                        }
                        for p in principles
                    ],
                }
            ),
            encoding="utf-8",
        )
    for rel, content in (files or {}).items():
        f = base / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    return base


def _levels(findings):
    return {lvl for lvl, _ in findings}


def test_no_profile_returns_empty(tmp_path):
    assert validate_skill_authoring(tmp_path / "nope") == []


def test_no_partition_returns_empty(tmp_path):
    assert validate_skill_authoring(_pkg(tmp_path)) == []


def test_draft_with_stubs_warns_never_fails(tmp_path):
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": STUB_SKILL},
    )
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings)
    assert any(lvl == "WARN" and "0/1" in msg for lvl, msg in findings)


def test_draft_missing_file_warns_never_fails(tmp_path):
    # declared skill, no file on disk → draft = WARN, not FAIL (non-breaking for the 15 pkgs).
    base = _pkg(tmp_path, status="draft", skills=["alpha-skill"])
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings)
    assert any(lvl == "WARN" for lvl, _ in findings)


def test_ready_with_stub_fails(tmp_path):
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": STUB_SKILL},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "still a stub" in msg for lvl, msg in findings)


def test_ready_missing_file_fails(tmp_path):
    base = _pkg(tmp_path, status="ready", skills=["alpha-skill"])
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "no file" in msg for lvl, msg in findings)


def test_ready_all_authored_passes(tmp_path):
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill()},
    )
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings)


def test_authored_invalid_fails_even_in_draft(tmp_path):
    # A file claiming status: ready with a dangling provenance id must FAIL regardless of pkg status.
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(principles=["P-999"])},
        principles=["P-001"],
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "does not resolve" in msg for lvl, msg in findings)


def test_authored_resolving_provenance_passes(tmp_path):
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(principles=["P-001"])},
        principles=["P-001"],
    )
    assert "FAIL" not in _levels(validate_skill_authoring(base))


def test_authored_evidence_provenance_resolves_passes(tmp_path):
    # evidence is a valid provenance field (claim -> evidence -> principle chain); resolving ids pass.
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(evidence=["e001", "e002"])},
        evidence=["e001", "e002", "e003"],
    )
    assert "FAIL" not in _levels(validate_skill_authoring(base))


def test_authored_dangling_evidence_id_fails(tmp_path):
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(evidence=["e999"])},
        evidence=["e001"],
    )
    findings = validate_skill_authoring(base)
    assert any(
        lvl == "FAIL" and "evidence" in msg and "does not resolve" in msg for lvl, msg in findings
    )


def test_authored_skill_missing_procedure_fails(tmp_path):
    body = _authored_skill().replace("## Procedure\n\n1. Do the thing.\n\n", "")
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": body},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "Procedure" in msg for lvl, msg in findings)


def test_ready_status_with_residual_todo_marker_fails(tmp_path):
    body = _authored_skill() + "\nTODO: author the rest.\n"
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": body},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "TODO: author" in msg for lvl, msg in findings)


# ── Fail-closed regression tests (defects 5–7) ────────────────────────────────


def test_corrupt_frontmatter_declaring_authored_fails(tmp_path):
    """A doc that opens a frontmatter fence but whose YAML is unparseable must FAIL,
    not silently demote to 'stub' and skip all content checks (defect 5)."""
    # Tabs after a mapping value make this invalid YAML; a status hint is present.
    corrupt = (
        "---\n"
        "name: alpha-skill\n"
        "kind: skill\n"
        "status: ready\n"
        "provenance:\n"
        "\t- bad indentation with tab\n"
        ": : :\n"
        "---\n\n# Alpha\n\nGarbage authored body, no Procedure section.\n"
    )
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": corrupt},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" for lvl, _ in findings), findings


def test_frontmatter_close_must_be_full_line(tmp_path):
    """A '---' embedded mid-line in the frontmatter must not truncate parsing early so that a
    later-declared authored status is missed (defect 5)."""
    # An inline '---' inside a value should not be treated as the closing fence.
    body = (
        "---\n"
        "name: alpha-skill\n"
        "kind: skill\n"
        "description: a value with --- inline dashes\n"
        "status: ready\n"
        "provenance:\n  principles: []\n  claims: []\n  source_anchors: []\n"
        "---\n\n# Alpha\n\nNo Procedure here.\n"
    )
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": body},
    )
    findings = validate_skill_authoring(base)
    # status: ready was correctly read → missing Procedure must FAIL.
    assert any(lvl == "FAIL" and "Procedure" in msg for lvl, msg in findings), findings


def test_legit_stub_without_frontmatter_still_stub(tmp_path):
    """A doc with no frontmatter at all is a legitimate stub (behaviour-preserving)."""
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": "# Alpha\n\nplain body, no frontmatter.\n"},
    )
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings)
    assert any(lvl == "WARN" and "0/1" in msg for lvl, msg in findings)


def test_provenance_universe_unparseable_source_fails(tmp_path):
    """If a doc cites provenance of a kind whose SOURCE file is present-but-unparseable, the
    reference must FAIL rather than pass unchecked against an empty universe (defect 6)."""
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(principles=["P-001"])},
    )
    # Write a corrupt principles.yaml so principle_ids() yields an empty universe.
    (base / "principles").mkdir(parents=True, exist_ok=True)
    (base / "principles" / "principles.yaml").write_text(
        "principles: [ : : unbalanced\n", encoding="utf-8"
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "principles" in msg for lvl, msg in findings), findings


def test_provenance_no_source_file_fails_when_cited(tmp_path):
    """Citing principle provenance when no principles.yaml exists at all must FAIL (defect 6)."""
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(principles=["P-001"])},
    )
    # No principles dir/file created → cited provenance cannot be resolved.
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "principles" in msg for lvl, msg in findings), findings


def test_no_provenance_cited_with_missing_source_passes(tmp_path):
    """A doc that cites NO provenance of a kind must not FAIL just because that source is
    absent (behaviour-preserving for legit packages)."""
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill()},  # empty provenance lists
    )
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings), findings


# ── Round-2 fail-closed regression tests (defects F5/F9, F7) ──────────────────


def test_bom_prefixed_corrupt_frontmatter_fails(tmp_path):
    """A doc whose frontmatter fence is preceded by a UTF-8 BOM must not be misread as
    'no frontmatter' → stub. With corrupt YAML inside, it must FAIL (defects F5/F9)."""
    corrupt = (
        "﻿---\n"
        "name: alpha-skill\n"
        "kind: skill\n"
        "status: ready\n"
        "provenance:\n"
        "\t- bad indentation with tab\n"
        ": : :\n"
        "---\n\n# Alpha\n\nGarbage authored body, no Procedure.\n"
    )
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": corrupt},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" for lvl, _ in findings), findings


def test_leading_blank_line_corrupt_frontmatter_fails(tmp_path):
    """Leading whitespace/blank lines before the opening '---' must not demote a corrupt
    frontmatter to a stub; it must still FAIL closed (defects F5/F9)."""
    corrupt = (
        "\n  \n---\n"
        "name: alpha-skill\n"
        "status: ready\n"
        "\t- bad tab indentation\n"
        ": : :\n"
        "---\n\n# Alpha\n\nNo Procedure.\n"
    )
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": corrupt},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" for lvl, _ in findings), findings


def test_opening_fence_without_close_fails(tmp_path):
    """A doc that OPENS a frontmatter fence but is truncated (no closing '---') must FAIL
    closed rather than silently demote to a stub and skip content checks (defects F5/F9)."""
    truncated = (
        "---\n"
        "name: alpha-skill\n"
        "kind: skill\n"
        "status: ready\n"
        "provenance:\n  principles: []\n"
        "# never closes the fence\n\n# Alpha\n\nNo closing fence here.\n"
    )
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": truncated},
    )
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" for lvl, _ in findings), findings


def test_fenceless_plaintext_with_leading_blank_still_stub(tmp_path):
    """A genuinely fence-less plain-text doc (even with leading blank lines) stays a stub —
    only docs that actually OPEN a fence move to fail-closed (behaviour-preserving)."""
    base = _pkg(
        tmp_path,
        status="draft",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": "\n\n# Alpha\n\nplain body, no frontmatter fence.\n"},
    )
    findings = validate_skill_authoring(base)
    assert "FAIL" not in _levels(findings), findings
    assert any(lvl == "WARN" and "0/1" in msg for lvl, msg in findings)


def test_principles_source_non_mapping_list_fails_cleanly(tmp_path):
    """A principles.yaml that parses to a top-level LIST (non-mapping) makes principle_ids()
    raise on .get — _safe_ids must catch it, the universe is empty + source non-loadable, and a
    doc citing a principle must FAIL cleanly without crashing the validator (defect F7)."""
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": _authored_skill(principles=["P-001"])},
    )
    (base / "principles").mkdir(parents=True, exist_ok=True)
    (base / "principles" / "principles.yaml").write_text("- P-001\n- P-002\n", encoding="utf-8")
    # Must not raise; must FAIL closed because the source is not a usable mapping.
    findings = validate_skill_authoring(base)
    assert any(lvl == "FAIL" and "principles" in msg for lvl, msg in findings), findings


def test_body_line_count_excludes_frontmatter(tmp_path):
    """The skill-body line limit must count the BODY, not the whole file incl frontmatter
    (defect 7). A body within the limit must pass even when body+frontmatter exceeds it."""
    from tools.subagent_factory import validate_skill_authoring as mod

    limit = mod._MAX_SKILL_LINES
    # A large frontmatter (many provenance refs) so the FILE total exceeds the limit ...
    fm_principles = [f"P-{i:03d}" for i in range(80)]
    authored = _authored_skill(principles=fm_principles)
    fm_lines = authored.count("\n") + 1  # includes the big frontmatter
    # ... while the BODY itself sits just under the limit.
    body_marker = "## Provenance\n\nFrom the source.\n"
    # Filler sized so the body is comfortably under the limit but body+frontmatter exceeds it.
    filler = "\n".join(f"line {i}" for i in range(limit - 60))
    big = authored.replace(body_marker, body_marker + "\n" + filler + "\n")
    # Whole-file count is over the limit; body count stays under.
    assert big.count("\n") + 1 > limit
    base = _pkg(
        tmp_path,
        status="ready",
        skills=["alpha-skill"],
        files={"skills/alpha-skill/SKILL.md": big},
        principles=fm_principles,
    )
    findings = validate_skill_authoring(base)
    over = [m for lvl, m in findings if lvl == "FAIL" and "lines" in m]
    assert not over, (over, fm_lines)
