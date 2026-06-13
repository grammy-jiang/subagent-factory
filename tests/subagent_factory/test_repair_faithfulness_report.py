"""Tests for the deterministic faithfulness-report repair (anchor quarantine)."""

import json

import yaml

from tools.subagent_factory.repair_faithfulness_report import repair_faithfulness_report
from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report


def _pkg(tmp_path, findings, anchors=("s-1-h0001",), profile=None):
    base = tmp_path / "pkg"
    (base / "reports").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "anchors" / "s-1.anchors.jsonl").write_text(
        "\n".join(json.dumps({"anchor_id": a}) for a in anchors) + "\n", encoding="utf-8"
    )
    if profile is not None:
        (base / "profile.yaml").write_text(yaml.safe_dump(profile), encoding="utf-8")
    rp = base / "reports" / "faithfulness-report.yaml"
    rp.write_text(
        yaml.safe_dump(
            {"schema_version": "faithfulness-report-v1", "subagent_slug": "d", "findings": findings}
        ),
        encoding="utf-8",
    )
    return rp


def test_drops_freetext_keeps_valid_and_quarantines(tmp_path):
    rp = _pkg(
        tmp_path,
        [
            {
                "rule_ref": "r",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
                "source_anchors": ["s-1-h0001", "whole book — explanatory commentary"],
            }
        ],
    )
    res = repair_faithfulness_report(rp)
    assert res["n_dropped"] == 1 and res["changed"]
    d = yaml.safe_load(rp.read_text())
    assert d["findings"][0]["source_anchors"] == ["s-1-h0001"]
    assert d["findings"][0]["verdict"] == "WITHIN_SCOPE"  # verdict untouched
    side = yaml.safe_load((rp.parent / "faithfulness-repair.yaml").read_text())
    assert any("whole book" in q["dropped"] for q in side["quarantined"])


def test_drops_dangling_shaped_id(tmp_path):
    rp = _pkg(
        tmp_path,
        [
            {
                "rule_ref": "r",
                "verdict": "EXACT_SUPPORT",
                "action": "accept",
                "source_anchors": ["s-1-h9999"],
            }
        ],
    )
    res = repair_faithfulness_report(rp)
    assert res["n_dropped"] == 1
    assert yaml.safe_load(rp.read_text())["findings"][0]["source_anchors"] == []


def test_clean_report_unchanged_no_sidecar(tmp_path):
    rp = _pkg(
        tmp_path,
        [
            {
                "rule_ref": "r",
                "verdict": "EXACT_SUPPORT",
                "action": "accept",
                "source_anchors": ["s-1-h0001"],
            }
        ],
    )
    res = repair_faithfulness_report(rp)
    assert res["changed"] is False and res["n_dropped"] == 0
    assert not (rp.parent / "faithfulness-repair.yaml").exists()


def test_repaired_report_then_passes_validation(tmp_path):
    rp = _pkg(
        tmp_path,
        [
            {
                "rule_ref": "quality_bar",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
                "source_anchors": ["s-1-h0001", "a free-text section description"],
            }
        ],
        profile={"quality_bar": ["a"]},
    )
    assert validate_faithfulness_report(rp)  # free-text → fails before repair
    repair_faithfulness_report(rp)
    assert validate_faithfulness_report(rp) == []  # clean after repair
