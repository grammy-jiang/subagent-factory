"""Tests for the corpus-health structural audit."""

import json

import yaml

from tools.subagent_factory.corpus_health import scan_corpus, scan_package


def _pkg(
    tmp_path, name="p", tier=1, status="ready", anchors=None, claims=None, converter="docling"
):
    base = tmp_path / name
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "metadata").mkdir(parents=True)
    (base / "profile.yaml").write_text(
        yaml.safe_dump({"tier": tier, "status": status, "agent_version": "1.0.0"}), encoding="utf-8"
    )
    (base / "sources" / "metadata" / "s.metadata.json").write_text(
        json.dumps({"converter_used": converter}), encoding="utf-8"
    )
    if anchors:
        (base / "sources" / "anchors" / "s.anchors.jsonl").write_text(
            "\n".join(json.dumps(a) for a in anchors) + "\n", encoding="utf-8"
        )
    if claims is not None:
        (base / "analysis").mkdir(parents=True)
        (base / "analysis" / "claims.jsonl").write_text(
            "\n".join(json.dumps(c) for c in claims) + "\n", encoding="utf-8"
        )
    return base


def _h(i, text="Real section heading about the topic"):
    return {"anchor_id": f"s-h{i:04d}", "anchor_type": "heading", "text": text}


def test_healthy_package_is_ok(tmp_path):
    base = _pkg(
        tmp_path,
        anchors=[_h(0), _h(1)],
        claims=[{"claim_id": "c1", "source_anchors": ["s-h0000"], "statement": "x"}],
    )
    r = scan_package(base)
    assert r["health"] == ["ok"]
    assert r["converter"] == "docling" and r["anchor_type"] == "heading" and r["claims"] == 1


def test_empty_anchors_flagged(tmp_path):
    base = _pkg(tmp_path, anchors=None, claims=[])
    assert "empty-anchors" in scan_package(base)["health"]


def test_dead_refs_flagged(tmp_path):
    base = _pkg(
        tmp_path,
        anchors=[_h(0)],
        claims=[{"claim_id": "c1", "source_anchors": ["s-h9999"], "statement": "x"}],
    )
    r = scan_package(base)
    assert r["dead_refs"] == 1 and "dead-refs" in r["health"]


def test_no_headings_flagged(tmp_path):
    base = _pkg(
        tmp_path,
        anchors=[
            {"anchor_id": "s-t0000", "anchor_type": "paragraph", "text": "real prose line here"}
        ],
        claims=[],
    )
    assert "no-headings" in scan_package(base)["health"]


def test_junk_paragraph_anchors_flagged(tmp_path):
    noise = [
        {"anchor_id": f"s-t{i:04d}", "anchor_type": "paragraph", "text": f"DeepDiveIntoOAuth {i}"}
        for i in range(4)
    ]
    base = _pkg(tmp_path, anchors=noise, claims=[])
    assert "junk-anchors" in scan_package(base)["health"]


def test_scan_corpus_skips_non_packages(tmp_path):
    _pkg(tmp_path, name="real", anchors=[_h(0)], claims=[])
    (tmp_path / "not-a-package").mkdir()  # no profile.yaml → skipped
    rows = scan_corpus(tmp_path)
    assert [r["slug"] for r in rows] == ["real"]
