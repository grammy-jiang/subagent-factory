"""Tests for the slug-agnostic map->reduce distilled-layer assembler (P3 polish)."""

import hashlib
import json

import yaml

from tools.subagent_factory.map_reduce_build import (
    assemble,
    build_claim_map,
    globalize_principles,
    load_modules,
)


def _fake_embedder(stmts):
    vocab = sorted({w for s in stmts for w in s.split()})
    return [[1.0 if w in s.split() else 0.0 for w in vocab] for s in stmts]


def _mk_module(repo, sid, text, claims, principles):
    sp = repo / "src" / f"{sid}.md"
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(text, encoding="utf-8")
    sha = hashlib.sha256(sp.read_bytes()).hexdigest()
    d = repo / "cache" / "book-extracts" / sha
    d.mkdir(parents=True)
    (d / "module.json").write_text(json.dumps({"source_id": sid}))
    (d / "source.md").write_text(text)
    (d / "chunks.jsonl").write_text(
        json.dumps({"chunk_id": f"{sid}-c0000", "char_start": 0, "heading_path": "H"}) + "\n"
    )
    (d / "claims.jsonl").write_text("\n".join(json.dumps(c) for c in claims))
    (d / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles})
    )
    return str(sp)


def _fixture(repo):
    c1 = {
        "claim_id": "C001",
        "source_id": "alpha-0001",
        "statement": "cache is hard",
        "source_anchors": ["alpha-0001-c0000"],
    }
    c2 = {
        "claim_id": "C001",
        "source_id": "beta-0002",
        "statement": "cache is also hard",
        "source_anchors": ["beta-0002-c0000"],
    }
    p1 = {
        "principle_id": "P001",
        "statement": "prefer caching",
        "derived_from_claims": ["C001"],
        "confidence": "medium",
        "applies_when": ["x"],
        "operational_mapping": {},
    }
    p2 = {
        "principle_id": "P001",
        "statement": "prefer caching strongly",
        "derived_from_claims": ["C001"],
        "confidence": "high",
        "applies_when": ["y"],
        "operational_mapping": {},
    }
    s1 = _mk_module(repo, "alpha-0001", "Alpha body text", [c1], [p1])
    s2 = _mk_module(repo, "beta-0002", "Beta body text", [c2], [p2])
    return [s1, s2]


def test_claim_map_global_renumber(tmp_path):
    sources = _fixture(tmp_path)
    mods = load_modules(sources, tmp_path / "cache" / "book-extracts")
    cmap, claims = build_claim_map(mods)
    assert [c["claim_id"] for c in claims] == ["C00001", "C00002"]
    assert cmap[("alpha-0001", "C001")] == "C00001"
    assert cmap[("beta-0002", "C001")] == "C00002"


def test_globalize_principles_rewrites_derived(tmp_path):
    sources = _fixture(tmp_path)
    mods = load_modules(sources, tmp_path / "cache" / "book-extracts")
    cmap, _ = build_claim_map(mods)
    gp = globalize_principles(mods, cmap)
    assert {d for p in gp for d in p["derived_from_claims"]} == {"C00001", "C00002"}


def test_assemble_merges_and_resolves(tmp_path):
    sources = _fixture(tmp_path)
    summary = assemble(
        "demo-p0",
        sources,
        repo=tmp_path,
        embedder=_fake_embedder,
        cos=0.5,
        decisions={0: {"action": "confirm"}},
        select=0,
    )
    assert summary == {"books": 2, "claims": 2, "principles": 1, "evidence": 2}
    pkg = tmp_path / "subagents" / "demo-p0"
    claim_ids = {
        json.loads(ln)["claim_id"]
        for ln in (pkg / "analysis" / "claims.jsonl").read_text().splitlines()
        if ln.strip()
    }
    assert claim_ids == {"C00001", "C00002"}
    prins = yaml.safe_load((pkg / "principles" / "principles.yaml").read_text())["principles"]
    assert len(prins) == 1 and prins[0]["n_sources"] == 2
    # every derived claim resolves into the assembled claims.jsonl
    assert set(prins[0]["derived_from_claims"]) <= claim_ids
    ev = yaml.safe_load((pkg / "evidence" / "evidence-records.yaml").read_text())[
        "evidence_records"
    ]
    assert {e["claim_id"] for e in ev} == {"C00001", "C00002"}
    assert (pkg / "sources" / "anchors" / "alpha-0001.anchors.jsonl").exists()
