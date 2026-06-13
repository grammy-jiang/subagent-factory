"""Tests for skill/reference anchor re-grounding by content overlap (Tier-0 repair)."""

import json

from tools.subagent_factory.reground_skill_anchors import (
    _split_frontmatter,
    reground_skill_anchors,
)

_SID = "the-book-20260101"


def _build(tmp_path):
    base = tmp_path / "pkg"
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "skills" / "batching").mkdir(parents=True)
    (base / "references").mkdir(parents=True)
    anchors = [
        {
            "anchor_id": f"{_SID}-t0001",
            "source_id": _SID,
            "line_number": 1,
            "text": "tune batch size and linger ms for producer throughput",
        },
        {
            "anchor_id": f"{_SID}-t0002",
            "source_id": _SID,
            "line_number": 9,
            "text": "completely unrelated avocado banana orchard content",
        },
        {
            "anchor_id": f"{_SID}-t0003",
            "source_id": _SID,
            "line_number": 20,
            "text": "batch size throughput producer compression tuning guide",
        },
    ]
    (base / "sources" / "anchors" / f"{_SID}.anchors.jsonl").write_text(
        "\n".join(json.dumps(a) for a in anchors), encoding="utf-8"
    )
    return base


def _doc(prov_anchors, body="configure batch size and linger for producer throughput tuning"):
    fm = "name: x\nkind: skill\nstatus: ready\nprovenance:\n  principles: []\n  claims: []\n"
    fm += "  source_anchors:\n" + "".join(f"    - {a}\n" for a in prov_anchors)
    return f"---\n{fm}---\n\n# Body\n\n{body}\n"


def test_split_frontmatter_roundtrip():
    fm, raw, body = _split_frontmatter(_doc([f"{_SID}-t0001"]))
    assert fm["kind"] == "skill"
    assert "# Body" in body


def test_bare_source_id_regrounded_to_overlapping_anchors(tmp_path):
    base = _build(tmp_path)
    (base / "skills" / "batching" / "SKILL.md").write_text(_doc([_SID]), encoding="utf-8")
    rep = reground_skill_anchors(base)
    after = rep["results"][0]["after"]
    # the two batching anchors (overlap) are cited; the avocado one (no overlap) is not
    assert f"{_SID}-t0001" in after and f"{_SID}-t0003" in after
    assert f"{_SID}-t0002" not in after


def test_existing_valid_anchor_is_kept(tmp_path):
    base = _build(tmp_path)
    (base / "skills" / "batching" / "SKILL.md").write_text(
        _doc([f"{_SID}-t0003"]), encoding="utf-8"
    )
    rep = reground_skill_anchors(base)
    # already valid -> unchanged, nothing to do
    assert rep["n_skills_changed"] == 0


def test_references_are_also_regrounded(tmp_path):
    base = _build(tmp_path)
    (base / "references" / "catalogue.md").write_text(_doc([_SID]), encoding="utf-8")
    rep = reground_skill_anchors(base)
    docs = {r["doc"] for r in rep["results"]}
    assert "catalogue" in docs


def test_no_overlap_drops_rather_than_guesses(tmp_path):
    base = _build(tmp_path)
    # body shares no tokens with any anchor -> nothing cited (not guessed)
    (base / "skills" / "batching" / "SKILL.md").write_text(
        _doc([_SID], body="xylophone zeppelin quokka"), encoding="utf-8"
    )
    rep = reground_skill_anchors(base)
    assert rep["results"][0]["after"] == []
