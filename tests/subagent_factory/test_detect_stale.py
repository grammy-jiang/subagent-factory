"""Tests for the stale-maintenance detector (Step 9)."""

import json

import yaml

from tools.subagent_factory.detect_stale import detect_stale


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
