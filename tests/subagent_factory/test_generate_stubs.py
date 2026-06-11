"""Tests for skill/reference stub generation."""

import yaml

from tools.subagent_factory.generate_stubs import _stub_slug, generate_stubs, planned_slugs


def _write_profile(tmp_path, skills, references):
    profile = {
        "slug": "demo-reviewer",
        "knowledge_partition": {"skills": skills, "references": references},
    }
    (tmp_path / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")


def test_stub_slug_shortens_long_entry():
    slug = _stub_slug(
        "Applying the guarded-suspension pattern: structure of the while-condition-wait loop"
    )
    assert slug.startswith("applying-the-guarded-suspension")
    assert " " not in slug and len(slug) <= 48


def test_generates_skill_and_reference_stubs(tmp_path):
    _write_profile(
        tmp_path,
        skills=[
            "Detecting deadlock and applying resource ordering.",
            "Structuring a BoundedBuffer with offer/poll variants.",
        ],
        references=["Lea's concurrency pattern taxonomy table.", "Thread API quick reference."],
    )
    r = generate_stubs(tmp_path)
    assert r["skills_created"] == 2
    assert r["references_created"] == 2
    assert (tmp_path / "skills").is_dir()
    assert (tmp_path / "references").is_dir()
    # every created skill file exists with a STUB marker (paths are absolute)
    for p in r["skill_paths"]:
        assert "STUB" in open(p).read()


def test_idempotent_does_not_overwrite(tmp_path):
    _write_profile(tmp_path, skills=["Detecting deadlock."], references=[])
    first = generate_stubs(tmp_path)
    assert first["skills_created"] == 1
    second = generate_stubs(tmp_path)
    assert second["skills_created"] == 0
    assert second["skills_existing"] == 1


def test_collision_disambiguation(tmp_path):
    # Two entries whose heads slugify identically must not collide.
    _write_profile(
        tmp_path, skills=["Naming things.", "Naming things differently later."], references=[]
    )
    r = generate_stubs(tmp_path)
    assert r["skills_created"] == 2
    assert len(set(r["skill_paths"])) == 2


def test_missing_profile_errors(tmp_path):
    r = generate_stubs(tmp_path)
    assert r["error"] is not None


def test_planned_slugs_disambiguates_collisions():
    profile = {"knowledge_partition": {"skills": ["Naming things.", "Naming things. Again later."]}}
    skills, refs = planned_slugs(profile)
    assert [s for _, s in skills] == ["naming-things", "naming-things-2"]
    assert refs == []


def test_stubs_carry_authored_doc_frontmatter(tmp_path):
    _write_profile(tmp_path, skills=["Detecting deadlock."], references=["A taxonomy table."])
    generate_stubs(tmp_path)
    skill = yaml.safe_load(
        (tmp_path / "skills" / "detecting-deadlock" / "SKILL.md").read_text().split("---")[1]
    )
    assert skill["kind"] == "skill" and skill["status"] == "stub"
    assert skill["provenance"] == {"principles": [], "claims": [], "source_anchors": []}
    ref = yaml.safe_load(
        (tmp_path / "references" / "a-taxonomy-table.md").read_text().split("---")[1]
    )
    assert ref["kind"] == "reference" and ref["status"] == "stub"
