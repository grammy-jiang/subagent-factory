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
