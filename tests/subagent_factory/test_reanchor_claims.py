"""Tests for surgical LLM claim re-anchoring — deterministic via a fake LLM."""

import json
import re

import yaml

from tools.subagent_factory.inject_anchors import inject_anchors
from tools.subagent_factory.reanchor_claims import (
    _load_source,
    build_reanchor_prompt,
    parse_reanchor,
    reanchor_claims,
)

_SID = "the-book-20260101"


def _build(tmp_path):
    base = tmp_path / "pkg"
    (base / "analysis").mkdir(parents=True)
    (base / "evidence").mkdir(parents=True)
    (base / "sources" / "anchors").mkdir(parents=True)
    (base / "sources" / "markdown").mkdir(parents=True)
    anchors = [
        {
            "anchor_id": f"{_SID}-t0001",
            "source_id": _SID,
            "line_number": 1,
            "text": "mirroring repeat last critical words",
        },
        {
            "anchor_id": f"{_SID}-t0002",
            "source_id": _SID,
            "line_number": 3,
            "text": "tactical empathy understand counterpart feelings",
        },
        {
            "anchor_id": f"{_SID}-t0003",
            "source_id": _SID,
            "line_number": 5,
            "text": "unrelated filler content here",
        },
    ]
    (base / "sources" / "anchors" / f"{_SID}.anchors.jsonl").write_text(
        "\n".join(json.dumps(a) for a in anchors), encoding="utf-8"
    )
    (base / "sources" / "markdown" / f"{_SID}.md").write_text(
        "mirroring is repeating the last critical words\n\nx\ntactical empathy means understanding\n\nfiller\n",
        encoding="utf-8",
    )
    claims = [
        {
            "schema_version": "claims-v1",
            "claim_id": "CL001",
            "source_id": _SID,
            "source_anchors": ["ch2-mirroring"],
            "statement": "Mirroring is repeating the last critical words",
            "component_class": "major_claim",
            "claim_type": "fact",
        },
        {
            "schema_version": "claims-v1",
            "claim_id": "CL002",
            "source_id": _SID,
            "source_anchors": ["ch1-empathy"],
            "statement": "Tactical empathy means understanding the counterpart",
            "component_class": "major_claim",
            "claim_type": "value",
        },
    ]
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c) for c in claims), encoding="utf-8"
    )
    ev = {
        "schema_version": "evidence-records-v1",
        "evidence_records": [
            {
                "evidence_id": "EV001",
                "claim_id": "CL001",
                "source_ids": [_SID],
                "source_anchors": ["ch2-mirroring"],
            },
            {
                "evidence_id": "EV002",
                "claim_id": "CL002",
                "source_ids": [_SID],
                "source_anchors": ["ch1-empathy"],
            },
        ],
    }
    (base / "evidence" / "evidence-records.yaml").write_text(yaml.safe_dump(ev), encoding="utf-8")
    return base


def _keyword_llm(prompt: str) -> str:
    """Fake LLM: pick the candidate whose snippet best shares words with the CLAIM line."""
    claim = re.search(r"CLAIM: (.+)", prompt).group(1).lower()
    best, best_id = -1, None
    for aid, snip in re.findall(r"- (\S+): (.*)", prompt):
        overlap = len(set(claim.split()) & set(snip.lower().split()))
        if overlap > best:
            best, best_id = overlap, aid
    return json.dumps({"anchors": [best_id] if best_id else []})


def test_load_source_window_aligns_with_injected_anchor_comments(tmp_path):
    """_load_source must slice windows from the SAME coordinate system the anchor line_numbers use.

    inject_anchors records line_number against the anchor-comment-free input, then writes the
    markdown with a `<!-- anchor:... -->` line inserted before each anchored line. _load_source reads
    that on-disk (comment-laden) file; if it slices by the raw line_number it drifts by the count of
    preceding comments, so an anchor's window shows a NEIGHBOR's passage — the LLM then judges support
    against the wrong text and silently re-anchors a claim to the wrong span. Build the source via the
    REAL inject_anchors (so the comment shift is present) and assert each anchor's window contains its
    OWN paragraph, not a neighbor's.
    """
    base = tmp_path / "pkg"
    md_dir = base / "sources" / "markdown"
    an_dir = base / "sources" / "anchors"
    md_dir.mkdir(parents=True)
    an_dir.mkdir(parents=True)
    sid = "doc-1"
    doc = (
        "# Alpha\n\nAlpha para about mirroring and tactical empathy.\n\n"
        "# Beta\n\nBeta para about resource ordering and deadlock.\n\n"
        "# Gamma\n\nGamma para about the closing concept here.\n"
    )
    src = md_dir / f"{sid}.md"
    src.write_text(doc, encoding="utf-8")
    inject_anchors(src, src, an_dir / f"{sid}.anchors.jsonl", sid)

    _, window = _load_source(base, sid)
    a, b, g = f"{sid}-h0000", f"{sid}-h0001", f"{sid}-h0002"
    # Each heading anchor's window must carry its own section's paragraph, not a neighbor's.
    assert "mirroring" in window[a] and "deadlock" not in window[a]
    assert "deadlock" in window[b] and "closing concept" not in window[b]
    assert "closing concept" in window[g]
    # And the injected comment markers must not leak into the windows shown to the LLM.
    assert "<!-- anchor:" not in window[a]


def test_parse_reanchor_rejects_invented_ids():
    allowed = {"a-t0001", "a-t0002"}
    assert parse_reanchor('{"anchors": ["a-t0001", "a-t9999"]}', allowed) == ["a-t0001"]
    assert parse_reanchor("no json", allowed) == []


def test_build_prompt_lists_candidates():
    p = build_reanchor_prompt("the claim", ["x-t0001"], {"x-t0001": "passage text"})
    assert "CLAIM: the claim" in p and "- x-t0001: passage text" in p


def test_reanchor_resolves_slugs_to_real_anchors(tmp_path):
    base = _build(tmp_path)
    rep = reanchor_claims(base, _keyword_llm)
    assert rep["n_fixed"] == 2 and rep["n_empty"] == 0
    # CL001 -> mirroring anchor, CL002 -> empathy anchor (content-correct)
    assert rep["chosen"]["CL001"] == [f"{_SID}-t0001"]
    assert rep["chosen"]["CL002"] == [f"{_SID}-t0002"]


def test_evidence_inherits_claim_anchors(tmp_path):
    base = _build(tmp_path)
    reanchor_claims(base, _keyword_llm)
    ev = yaml.safe_load((base / "evidence" / "evidence-records.yaml").read_text())
    by_id = {r["evidence_id"]: r["source_anchors"] for r in ev["evidence_records"]}
    assert by_id["EV001"] == [f"{_SID}-t0001"]
    assert by_id["EV002"] == [f"{_SID}-t0002"]


def test_claims_written_with_real_anchors(tmp_path):
    base = _build(tmp_path)
    reanchor_claims(base, _keyword_llm)
    lines = (base / "analysis" / "claims.jsonl").read_text().splitlines()
    recs = [json.loads(line) for line in lines if line.strip()]
    assert all(
        a.endswith(tuple(f"-t000{i}" for i in range(1, 4))) or a == []
        for r in recs
        for a in r["source_anchors"]
    )
    assert recs[0]["source_anchors"] == [f"{_SID}-t0001"]


def test_llm_no_support_leaves_empty(tmp_path):
    base = _build(tmp_path)
    rep = reanchor_claims(base, lambda _p: '{"anchors": []}')
    assert rep["n_fixed"] == 0 and rep["n_empty"] == 2
    assert rep["chosen"]["CL001"] == []


def test_reanchor_llm_subprocess_failure_is_resilient(tmp_path, recwarn):
    # The shell-backed _claude_llm raises subprocess.SubprocessError (check=True) on a crashed/timed-out
    # call. A crash is NOT "no anchor found": the run must not abort, the claim's existing anchors must
    # be left intact (not wiped to []), and the failure must be counted + surfaced.
    import subprocess

    def crashing_llm(_prompt):
        raise subprocess.CalledProcessError(1, ["claude", "-p"])

    rep = reanchor_claims(base := _build(tmp_path), crashing_llm)
    assert rep["n_errors"] == 2  # both claims hit the crash
    assert rep["n_fixed"] == 0
    assert rep["chosen"] == {}
    # original (unresolved) anchors preserved on disk, NOT overwritten with []
    recs = [
        json.loads(line)
        for line in (base / "analysis" / "claims.jsonl").read_text().splitlines()
        if line.strip()
    ]
    assert recs[0]["source_anchors"] == ["ch2-mirroring"]
    assert any(issubclass(w.category, RuntimeWarning) for w in recwarn.list)


def test_reanchor_llm_non_subprocess_error_propagates(tmp_path):
    # Guard: only subprocess failures are absorbed; a real bug in the injected llm still propagates.
    import pytest

    def buggy_llm(_prompt):
        raise ValueError("real bug")

    with pytest.raises(ValueError):
        reanchor_claims(_build(tmp_path), buggy_llm)
