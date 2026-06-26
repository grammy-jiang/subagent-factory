"""Tests for the stale-maintenance detector (Step 9)."""

import json

import yaml

from tools.subagent_factory.detect_stale import detect_stale
from tools.subagent_factory.validate_skill_authoring import _parse_frontmatter, split_frontmatter


def _body_after_frontmatter(text: str) -> str:
    return split_frontmatter(text)[1]


def _skill_md(slug, *, status="ready", principles=(), claims=(), digest=None, body="1. do x"):
    prov = {"principles": list(principles), "claims": list(claims), "source_anchors": []}
    if digest is not None:
        prov["authored_from_digest"] = digest
    fm = yaml.safe_dump(
        {"name": slug, "kind": "skill", "status": status, "provenance": prov}, sort_keys=False
    )
    return f"---\n{fm}---\n\n# {slug}\n\n## Procedure\n\n{body}\n\n## Provenance\n\nx\n"


def _pkg(tmp_path, *, skills, principles, claims, status="ready"):
    base = tmp_path / "pkg"
    base.mkdir(parents=True, exist_ok=True)
    (base / "profile.yaml").write_text(
        yaml.safe_dump(
            {"status": status, "knowledge_partition": {"skills": list(skills), "references": []}}
        ),
        encoding="utf-8",
    )
    (base / "principles").mkdir(parents=True, exist_ok=True)
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {
                        "principle_id": k,
                        "statement": v,
                        "derived_from_claims": ["C1"],
                        "confidence": "high",
                    }
                    for k, v in principles.items()
                ],
            }
        ),
        encoding="utf-8",
    )
    (base / "analysis").mkdir(parents=True, exist_ok=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(
            json.dumps(
                {
                    "claim_id": k,
                    "source_id": "s1",
                    "statement": v,
                    "component_class": "claim",
                    "claim_type": "fact",
                }
            )
            for k, v in claims.items()
        )
        + ("\n" if claims else ""),
        encoding="utf-8",
    )
    for slug, content in skills.items():
        d = base / "skills" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(content, encoding="utf-8")
    return base


def _doc_fm(base, slug):
    return yaml.safe_load((base / "skills" / slug / "SKILL.md").read_text().split("---")[1])


def test_no_baseline_is_info_not_stale(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=["C1"])},
        principles={"P1": "orig"},
        claims={"C1": "claim one"},
    )
    out = detect_stale(base)
    assert any(lvl == "INFO" and art == "skill:alpha" for lvl, art, _ in out)
    assert not any(lvl == "STALE" for lvl, _, _ in out)


def test_stamp_then_check_clean(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=["C1"])},
        principles={"P1": "orig"},
        claims={"C1": "claim one"},
    )
    detect_stale(base, stamp=True)
    assert "authored_from_digest" in _doc_fm(base, "alpha")["provenance"]
    out = detect_stale(base)
    assert not any(lvl == "STALE" for lvl, _, _ in out)
    assert any(lvl == "OK" and art == "skill:alpha" for lvl, art, _ in out)


def test_principle_change_marks_stale(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=[])},
        principles={"P1": "orig"},
        claims={},
    )
    detect_stale(base, stamp=True)
    pp = base / "principles" / "principles.yaml"
    data = yaml.safe_load(pp.read_text())
    data["principles"][0]["statement"] = "MATERIALLY CHANGED"
    pp.write_text(yaml.safe_dump(data), encoding="utf-8")
    out = detect_stale(base)
    assert any(lvl == "STALE" and art == "skill:alpha" for lvl, art, _ in out)


def test_missing_cited_id_marks_stale(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=[], claims=["C1"])},
        principles={},
        claims={"C1": "claim one"},
    )
    detect_stale(base, stamp=True)
    (base / "analysis" / "claims.jsonl").write_text("", encoding="utf-8")
    out = detect_stale(base)
    assert any(lvl == "STALE" and "no longer present" in reason for lvl, _, reason in out)


def test_empty_provenance_not_tracked(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=[], claims=[])},
        principles={},
        claims={},
    )
    out = detect_stale(base)
    assert any(lvl == "OK" and "not drift-tracked" in reason for lvl, _, reason in out)


def test_mark_flips_status_to_stale(tmp_path):
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=[])},
        principles={"P1": "orig"},
        claims={},
    )
    detect_stale(base, stamp=True)
    pp = base / "principles" / "principles.yaml"
    data = yaml.safe_load(pp.read_text())
    data["principles"][0]["statement"] = "CHANGED"
    pp.write_text(yaml.safe_dump(data), encoding="utf-8")
    detect_stale(base, mark=True)
    assert _doc_fm(base, "alpha")["status"] == "stale"


def test_stamp_preserves_body(tmp_path):
    base = _pkg(
        tmp_path,
        skills={
            "alpha": _skill_md("alpha", principles=["P1"], claims=[], body="UNIQUE_BODY_TOKEN")
        },
        principles={"P1": "orig"},
        claims={},
    )
    detect_stale(base, stamp=True)
    assert "UNIQUE_BODY_TOKEN" in (base / "skills" / "alpha" / "SKILL.md").read_text()


def test_no_profile_returns_empty(tmp_path):
    assert detect_stale(tmp_path / "nope") == []


def test_corrupt_frontmatter_does_not_crash_run(tmp_path):
    """A doc that opens a --- fence but never closes it must NOT abort the whole scan with an
    AttributeError on the _FRONTMATTER_CORRUPT sentinel; it is surfaced and the run continues."""
    good = _skill_md("alpha", principles=["P1"], claims=[], digest="x")
    base = _pkg(
        tmp_path,
        skills={"alpha": good, "broken": "---\nname: broken\nstatus: ready\nno close fence\n"},
        principles={"P1": "orig"},
        claims={},
    )
    # Both skills are declared in the profile partition.
    prof = base / "profile.yaml"
    data = yaml.safe_load(prof.read_text())
    data["knowledge_partition"]["skills"] = ["alpha", "broken"]
    prof.write_text(yaml.safe_dump(data), encoding="utf-8")
    findings = detect_stale(base)  # must not raise
    arts = {a for _, a, _ in findings}
    assert "skill:alpha" in arts  # the good doc still got checked
    assert any("broken" in a and lvl == "WARN" for lvl, a, _ in findings)


def test_stamp_preserves_body_containing_horizontal_rule(tmp_path):
    """--stamp must not truncate a body that itself contains a line of '---' (a Markdown
    horizontal rule / nested fence). The reader and rewriter share one anchored fence split."""
    body = "intro paragraph\n\n---\n\nsection after a horizontal rule TAILTOKEN"
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=[], body=body)},
        principles={"P1": "orig"},
        claims={},
    )
    detect_stale(base, stamp=True)
    written = (base / "skills" / "alpha" / "SKILL.md").read_text()
    assert "TAILTOKEN" in written
    assert "section after a horizontal rule" in written


def test_stamp_with_fence_line_inside_frontmatter_value(tmp_path):
    """The closing fence must be a FULL '---' line: a '---' embedded inside a multiline
    frontmatter value must not be mistaken for the close, or --stamp leaks frontmatter into the
    body. Reader and rewriter share one anchored split, so the body survives intact."""
    base = _pkg(
        tmp_path,
        skills={"alpha": _skill_md("alpha", principles=["P1"], claims=[], digest="x")},
        principles={"P1": "orig"},
        claims={},
    )
    # Hand-write a doc whose frontmatter has a block-scalar value containing a '---' line.
    doc = (
        "---\n"
        "name: alpha\n"
        "kind: skill\n"
        "status: ready\n"
        "note: |\n"
        "  first line of note\n"
        "  ---\n"
        "  second line after a dashed line\n"
        "provenance:\n"
        "  principles: [P1]\n"
        "  claims: []\n"
        "  source_anchors: []\n"
        "  authored_from_digest: x\n"
        "---\n\n"
        "# alpha\n\n## Procedure\n\nBODY_SENTINEL\n"
    )
    (base / "skills" / "alpha" / "SKILL.md").write_text(doc, encoding="utf-8")
    detect_stale(base, stamp=True)
    written = (base / "skills" / "alpha" / "SKILL.md").read_text()
    # Re-parse: the note value (incl. its embedded '---' line) must stay in the frontmatter, and
    # the body must be exactly the real body — no frontmatter leaked past the true closing fence.
    fm = _parse_frontmatter(written)
    assert isinstance(fm, dict)
    assert "second line after a dashed line" in fm["note"]
    body = written.split("\n---\n", 1)[-1] if False else _body_after_frontmatter(written)
    assert "BODY_SENTINEL" in body
    assert "note:" not in body and "second line after a dashed line" not in body
