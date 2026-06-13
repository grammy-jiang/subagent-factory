"""Tests for the faithfulness anchor remapper — deterministic, tmp packages."""

import json

import yaml

from tools.subagent_factory.remap_faithfulness_anchors import (
    _finding_source,
    _remap_one,
    _route_source,
    remap_faithfulness_anchors,
)
from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report


def _pkg(tmp_path, sources: dict[str, list[tuple[int, str]]], findings: list[list[str]]):
    """Build a package: ``sources`` = {source_id: [(line_number, anchor_id), ...]}."""
    base = tmp_path / "pkg"
    (base / "sources" / "markdown").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "reports").mkdir(parents=True)
    (base / "profile.yaml").write_text("slug: pkg\nrole: r\n", encoding="utf-8")
    for sid, anchors in sources.items():
        (base / "sources" / "markdown" / f"{sid}.md").write_text("x\n" * 50, encoding="utf-8")
        lines = "\n".join(
            json.dumps({"anchor_id": aid, "line_number": ln, "source_id": sid})
            for ln, aid in anchors
        )
        (base / "sources" / "anchors" / f"{sid}.anchors.jsonl").write_text(lines, encoding="utf-8")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": "pkg",
        "findings": [
            {
                "rule_ref": "role",
                "verdict": "WITHIN_SCOPE",
                "action": "accept_with_note",
                "source_anchors": sa,
            }
            for sa in findings
        ],
    }
    rp = base / "reports" / "faithfulness-report.yaml"
    rp.write_text(yaml.safe_dump(report), encoding="utf-8")
    return rp


_SRC = "the-book-20260101"
_ANCHORS = [(1, f"{_SRC}-t0000"), (100, f"{_SRC}-t0010"), (200, f"{_SRC}-t0020")]


# ---- routing + single remap ------------------------------------------------------------------


def test_route_explicit_sid_prefix():
    assert _route_source(f"{_SRC}:L148", [_SRC]) == _SRC


def test_route_name_token_and_full_anchor_id():
    sids = ["kafka-best-practices-2026", "optimizing-2026"]
    assert _route_source("kafka-best-practices L753", sids) == "kafka-best-practices-2026"
    # a recovered real anchor id is LONGER than the sid -> tok.startswith(sid) branch
    assert _route_source("kafka-best-practices-2026-t0005", sids) == "kafka-best-practices-2026"


def test_route_bare_line_ambiguous_is_none():
    assert _route_source("L1082-1084", ["a-1", "b-2"]) is None
    assert _route_source("L1082", ["only-1"]) == "only-1"  # single source -> unambiguous


def test_remap_one_maps_to_covering_anchor():
    maps = {_SRC: _ANCHORS}
    # line 150 -> last anchor with line<=150 == the one at line 100
    assert _remap_one(f"{_SRC}:L150", maps, [_SRC]) == f"{_SRC}-t0010"
    assert _remap_one("a slug with no line", maps, [_SRC]) is None


def test_finding_source_inference():
    sids = ["kafka-2026", "opt-2026"]
    # a finding whose only hinted anchor points to kafka -> bare-L routes there
    assert _finding_source(["kafka-2026-t0005", "L1082"], sids) == "kafka-2026"
    # mixed hints -> ambiguous -> None
    assert _finding_source(["kafka-2026-t0005", "opt-2026-t0003", "L1082"], sids) is None


# ---- end-to-end repair -----------------------------------------------------------------------


def test_single_source_line_refs_recovered_and_validate(tmp_path):
    rp = _pkg(tmp_path, {_SRC: _ANCHORS}, [[f"{_SRC}:L148", f"{_SRC}:L5"]])
    r = remap_faithfulness_anchors(rp)
    assert r["n_remapped"] == 2 and r["n_quarantined"] == 0
    assert validate_faithfulness_report(rp) == []


def test_slug_refs_quarantined_but_report_validates(tmp_path):
    rp = _pkg(tmp_path, {_SRC: _ANCHORS}, [["ch1-tactical-empathy", "the-struggle"]])
    r = remap_faithfulness_anchors(rp)
    assert r["n_remapped"] == 0 and r["n_quarantined"] == 2
    assert validate_faithfulness_report(rp) == []  # empty source_anchors is valid
    side = rp.parent / "faithfulness-repair.yaml"
    assert side.exists()  # dropped refs preserved for review


def test_multisource_finding_inference_recovers_bare_line(tmp_path):
    a = "kafka-best-2026"
    b = "opt-2026"
    rp = _pkg(
        tmp_path,
        {a: [(1, f"{a}-t0000"), (50, f"{a}-t0005")], b: [(1, f"{b}-t0000")]},
        [[f"{a} L60", "L55"]],  # one hinted (->a) + one bare; bare should route to a
    )
    r = remap_faithfulness_anchors(rp)
    assert r["n_remapped"] == 2 and r["n_quarantined"] == 0
    assert validate_faithfulness_report(rp) == []
