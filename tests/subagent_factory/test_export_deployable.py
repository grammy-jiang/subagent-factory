"""Tests for export_deployable — the self-contained deployable-bundle exporter (layout A)."""

from pathlib import Path

import pytest

from tools.subagent_factory.export_deployable import (
    _inject_skills_frontmatter,
    _inline_references,
    _rewrite_header,
    _strip_canonical_section,
    export_deployable,
)


def _make_pkg(root: Path, slug: str = "testdep") -> Path:
    """Write a minimal renderable package: profile + two skills + two references."""
    pkg = root / "subagents" / slug
    (pkg / "skills" / "skill-a").mkdir(parents=True)
    (pkg / "skills" / "skill-b").mkdir(parents=True)
    (pkg / "references").mkdir(parents=True)
    (pkg / "skills" / "skill-a" / "SKILL.md").write_text("# Skill A\n\nProcedure A.\n")
    (pkg / "skills" / "skill-b" / "SKILL.md").write_text("# Skill B\n\nProcedure B.\n")
    (pkg / "references" / "ref-one.md").write_text("# Ref One\n\nRubric one.\n")
    (pkg / "references" / "ref-two.md").write_text("# Ref Two\n\nChecklist two.\n")
    (pkg / "profile.yaml").write_text(
        f"slug: {slug}\n"
        "role: A test advisor for the deployable exporter.\n"
        "attach_invariants: false\n"
        "knowledge_partition:\n"
        "  skills: [skill-a, skill-b]\n"
        "  references: [ref-one, ref-two]\n"
    )
    return pkg


# --- pure helpers ---------------------------------------------------------------------------


def test_strip_canonical_section_removes_tail():
    md = "## Role\n\nbody\n\n## Canonical package\n\nFull source at: `subagents/x/`\n"
    out = _strip_canonical_section(md)
    assert "## Canonical package" not in out
    assert out.rstrip().endswith("body")


def test_strip_canonical_section_noop_when_absent():
    md = "## Role\n\nbody only\n"
    assert _strip_canonical_section(md) == md


def test_inject_skills_frontmatter_inserts_before_close():
    md = "---\nname: x\nmodel: sonnet\n---\n\n## Role\n"
    out = _inject_skills_frontmatter(md, ["a", "b"])
    fm = out.split("---")[1]
    assert "skills:" in fm and "  - a" in fm and "  - b" in fm
    # body untouched, exactly one frontmatter block
    assert out.count("\n---\n") >= 1
    assert "## Role" in out


def test_inject_skills_frontmatter_noop_without_skills_or_frontmatter():
    md = "---\nname: x\n---\nbody\n"
    assert _inject_skills_frontmatter(md, []) == md
    assert _inject_skills_frontmatter("no frontmatter here", ["a"]) == "no frontmatter here"


def test_rewrite_header_points_at_factory_exporter():
    md = "Regenerate with: /author-subagent --update foo\n"
    out = _rewrite_header(md, "foo")
    assert "/author-subagent --update foo" not in out
    assert "export-deployable foo --dest" in out


def test_inline_references_appends_existing_only(tmp_path):
    pkg = _make_pkg(tmp_path)
    md, inlined = _inline_references("## Role\n\nbody\n", pkg, ["ref-one", "missing", "ref-two"])
    assert inlined == ["ref-one", "ref-two"]
    assert "## Reference — ref-one" in md and "Rubric one." in md
    assert "## Reference — ref-two" in md and "Checklist two." in md
    assert "missing" not in md


# --- full export ----------------------------------------------------------------------------


def test_export_deployable_builds_layout_a(tmp_path):
    pkg = _make_pkg(tmp_path)
    dest = tmp_path / "target-repo"
    result = export_deployable(pkg, dest)

    assert result["error"] is None
    assert result["slug"] == "testdep"
    assert sorted(result["skills_copied"]) == ["skill-a", "skill-b"]
    assert sorted(result["references_inlined"]) == ["ref-one", "ref-two"]

    adapter = Path(result["adapter_path"])
    assert adapter == dest / ".claude" / "agents" / "testdep.md"
    text = adapter.read_text()
    # skills frontmatter present
    assert "skills:" in text.split("---")[1]
    assert "  - skill-a" in text and "  - skill-b" in text
    # canonical section stripped, references inlined, header rewritten
    assert "## Canonical package" not in text
    assert "## Reference — ref-one" in text and "## Reference — ref-two" in text
    assert "export-deployable testdep --dest" in text
    # skill dirs copied
    assert (
        (dest / ".claude" / "skills" / "skill-a" / "SKILL.md").read_text().startswith("# Skill A")
    )
    assert (dest / ".claude" / "skills" / "skill-b" / "SKILL.md").exists()


def test_export_deployable_overwrites_existing_skill_dir(tmp_path):
    pkg = _make_pkg(tmp_path)
    dest = tmp_path / "target-repo"
    stale = dest / ".claude" / "skills" / "skill-a"
    stale.mkdir(parents=True)
    (stale / "OLD.md").write_text("stale\n")

    export_deployable(pkg, dest)

    # stale file gone (dir was replaced), fresh SKILL.md present
    assert not (stale / "OLD.md").exists()
    assert (stale / "SKILL.md").exists()


def test_export_deployable_missing_profile_returns_error(tmp_path):
    result = export_deployable(tmp_path / "nope", tmp_path / "dest")
    assert result["error"] and "profile.yaml not found" in result["error"]
    assert result["adapter_path"] is None


def test_export_deployable_missing_slug_returns_error(tmp_path):
    pkg = tmp_path / "subagents" / "x"
    pkg.mkdir(parents=True)
    (pkg / "profile.yaml").write_text("role: no slug here\n")
    result = export_deployable(pkg, tmp_path / "dest")
    assert result["error"] == "profile.yaml missing 'slug' field"


@pytest.mark.parametrize("skills", [[], ["only-one"]])
def test_inject_skills_frontmatter_shapes(skills):
    md = "---\nname: x\n---\nbody\n"
    out = _inject_skills_frontmatter(md, skills)
    if skills:
        assert "skills:" in out
    else:
        assert out == md
