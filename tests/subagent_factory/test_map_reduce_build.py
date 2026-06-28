"""Tests for the slug-agnostic map->reduce distilled-layer assembler (P3 polish)."""

import hashlib
import json

import pytest
import yaml

from tools.subagent_factory.map_reduce_build import (
    assemble,
    build_claim_map,
    build_groups,
    deserialize_groups,
    emit_clusters,
    globalize_principles,
    load_modules,
    serialize_groups,
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
    assert len(prins) == 1
    assert (
        "n_sources" not in prins[0] and "source_ids" not in prins[0]
    )  # principles-v1 is additionalProperties:false
    assert set(prins[0]["derived_from_claims"]) == {
        "C00001",
        "C00002",
    }  # both books merged into one
    assert set(prins[0]["derived_from_claims"]) <= claim_ids
    ev = yaml.safe_load((pkg / "evidence" / "evidence-records.yaml").read_text())[
        "evidence_records"
    ]
    assert {e["claim_id"] for e in ev} == {"C00001", "C00002"}
    assert (pkg / "sources" / "anchors" / "alpha-0001.anchors.jsonl").exists()


# --- source-layer ownership: coherent single identity, prune stale, carry provenance --------------


def _assemble_demo(repo, slug, sources):
    return assemble(
        slug,
        sources,
        repo=repo,
        embedder=_fake_embedder,
        cos=0.5,
        decisions={0: {"action": "confirm"}},
        select=0,
    )


def test_assemble_writes_full_source_layer(tmp_path):
    # assemble owns the source layer: each current id gets markdown + metadata + anchors + report,
    # and the manifest lists exactly those ids — so the LLM finish step never has to synth them.
    sources = _fixture(tmp_path)
    _assemble_demo(tmp_path, "demo-src", sources)
    pkg = tmp_path / "subagents" / "demo-src"
    for sid in ("alpha-0001", "beta-0002"):
        assert (pkg / "sources" / "markdown" / f"{sid}.md").exists()
        assert (pkg / "sources" / "metadata" / f"{sid}.metadata.json").exists()
        assert (pkg / "sources" / "anchors" / f"{sid}.anchors.jsonl").exists()
        assert (pkg / "sources" / "reports" / f"{sid}.conversion-report.md").exists()
        meta = json.loads((pkg / "sources" / "metadata" / f"{sid}.metadata.json").read_text())
        assert meta["schema_version"] == "source-metadata-v1"
        assert meta["source_id"] == sid
    manifest = yaml.safe_load((pkg / "source-pack.manifest.yaml").read_text())
    assert {s["source_id"] for s in manifest["sources"]} == {"alpha-0001", "beta-0002"}


def test_assemble_prunes_stale_source_identity(tmp_path):
    # Rebuilding map-reduce OVER an existing package must not leave a second, stale source identity.
    # Pre-seed the package with a foreign id's source files + manifest; assemble must purge them.
    sources = _fixture(tmp_path)
    pkg = tmp_path / "subagents" / "demo-stale-src"
    for sub in ("markdown", "metadata", "anchors", "reports"):
        (pkg / "sources" / sub).mkdir(parents=True, exist_ok=True)
    stale = "caching-old-20260612101948"
    (pkg / "sources" / "markdown" / f"{stale}.md").write_text("stale")
    (pkg / "sources" / "metadata" / f"{stale}.metadata.json").write_text("{}")
    (pkg / "sources" / "anchors" / f"{stale}.anchors.jsonl").write_text("{}\n")
    (pkg / "sources" / "reports" / f"{stale}.conversion-report.md").write_text("# stale")

    _assemble_demo(tmp_path, "demo-stale-src", sources)

    # The stale identity is gone from every subdir...
    for sub, ext in (
        ("markdown", ".md"),
        ("metadata", ".metadata.json"),
        ("anchors", ".anchors.jsonl"),
        ("reports", ".conversion-report.md"),
    ):
        assert not (pkg / "sources" / sub / f"{stale}{ext}").exists()
    # ...and only the current ids remain, in the manifest too.
    manifest = yaml.safe_load((pkg / "source-pack.manifest.yaml").read_text())
    assert {s["source_id"] for s in manifest["sources"]} == {"alpha-0001", "beta-0002"}


def test_assemble_drops_classic_vestiges(tmp_path):
    # A map-reduce package carries none of the classic-pipeline artifacts; rebuilding over a classic
    # ingest must drop them rather than leave them keyed to the now-dead source id.
    sources = _fixture(tmp_path)
    pkg = tmp_path / "subagents" / "demo-vestige"
    (pkg / "analysis").mkdir(parents=True, exist_ok=True)
    (pkg / "sources" / "maps").mkdir(parents=True, exist_ok=True)
    (pkg / "interrogation-records.yaml").write_text("q1: stale")
    (pkg / "analysis" / "claim-importance-scores.yaml").write_text("old-id: 0.5")
    (pkg / "sources" / "maps" / "caching-old.source-map.yaml").write_text("stale: map")

    _assemble_demo(tmp_path, "demo-vestige", sources)

    assert not (pkg / "interrogation-records.yaml").exists()
    assert not (pkg / "analysis" / "claim-importance-scores.yaml").exists()
    assert not (pkg / "sources" / "maps").exists()
    # the real distilled layer is untouched
    assert (pkg / "analysis" / "claims.jsonl").exists()


def test_assemble_carries_predecessor_metadata(tmp_path):
    # A prior ingest's metadata (matched by the input markdown stem) is carried onto the new id,
    # so re-MAPping preserves title/rights/author instead of degrading to stem-derived defaults.
    sources = _fixture(tmp_path)
    pkg = tmp_path / "subagents" / "demo-carry"
    md_dir = pkg / "sources" / "metadata"
    md_dir.mkdir(parents=True, exist_ok=True)
    (md_dir / "alpha-0001.metadata.json").write_text(
        json.dumps(
            {
                "source_id": "alpha-0001",
                "title": "The Real Caching Book",
                "author": "A. Author",
                "rights_status": "open",
                "file_type": "pdf",
                "original_filename": "real-caching.pdf",
            }
        )
    )
    _assemble_demo(tmp_path, "demo-carry", sources)
    meta = json.loads((md_dir / "alpha-0001.metadata.json").read_text())
    assert meta["title"] == "The Real Caching Book"
    assert meta["author"] == "A. Author"
    assert meta["rights_status"] == "open"
    assert meta["file_type"] == "pdf"
    manifest = yaml.safe_load((pkg / "source-pack.manifest.yaml").read_text())
    rec = next(s for s in manifest["sources"] if s["source_id"] == "alpha-0001")
    assert rec["original_filename"] == "real-caching.pdf"


# --- single-producer group-index contract (fix #1) + group-key validation (fix #2) ----------------


def test_emit_and_assemble_share_one_grouping(tmp_path):
    # build_groups is the single producer; emit_clusters keys the LLM decisions on it and assemble
    # applies them against the SAME grouping (threaded via the optional `groups` arg) — no recompute.
    sources = _fixture(tmp_path)
    mods = load_modules(sources, tmp_path / "cache" / "book-extracts")
    cmap, _ = build_claim_map(mods)
    gp = globalize_principles(mods, cmap)
    groups = build_groups(gp, _fake_embedder, cos=0.5)
    clusters = emit_clusters(gp, _fake_embedder, cos=0.5, groups=groups)
    # The two example principles cluster into one multi-member group at this threshold.
    assert clusters and clusters[0]["group"] == 0
    summary = assemble(
        "demo-shared",
        sources,
        repo=tmp_path,
        embedder=_fake_embedder,
        cos=0.5,
        decisions={clusters[0]["group"]: {"action": "confirm"}},
        select=0,
        groups=groups,  # identical object the emit phase keyed its decisions on
    )
    assert summary["principles"] == 1  # confirm merged the shared cluster


def test_assemble_rejects_out_of_range_group_key(tmp_path):
    # A decisions file built against a stale/different cluster set has an out-of-range GROUP KEY.
    # apply_decisions would silently default it to confirm; assemble must instead fail loudly.
    sources = _fixture(tmp_path)
    with pytest.raises(ValueError, match="out-of-range group keys"):
        assemble(
            "demo-stale",
            sources,
            repo=tmp_path,
            embedder=_fake_embedder,
            cos=0.5,
            decisions={99: {"action": "confirm"}},
            select=0,
        )


# --- cross-process group persistence + replay (fix: silent reshuffle hazard) ----------------------


def _gp(sid, statement, claims):
    return {"source_id": sid, "statement": statement, "derived_from_claims": list(claims)}


def test_serialize_then_deserialize_roundtrips_positions():
    principles = [
        _gp("a", "alpha", ["C1"]),
        _gp("b", "beta", ["C2"]),
        _gp("a", "gamma", ["C3"]),
    ]
    groups = [[0, 2], [1]]
    serialized = serialize_groups(principles, groups)
    assert deserialize_groups(principles, serialized) == groups


def test_persisted_groups_replay_to_same_principles_under_reshuffle():
    # The emit phase produced this grouping on the ORIGINAL order; the LLM keyed decisions on it.
    emit_order = [
        _gp("a", "prefer caching", ["C1"]),
        _gp("b", "prefer caching strongly", ["C2"]),
        _gp("c", "use a bulkhead to isolate failures", ["C3"]),
    ]
    # group 0 = the two cache principles (identities a/prefer caching + b/prefer caching strongly).
    emit_groups = [[0, 1], [2]]
    serialized = serialize_groups(emit_order, emit_groups)

    # A second process re-globalizes principles in a DIFFERENT order (the reshuffle hazard).
    assemble_order = [emit_order[2], emit_order[0], emit_order[1]]  # c, a, b

    # Replaying the persisted grouping maps group 0 to the SAME principle identities, NOT positions.
    replayed = deserialize_groups(assemble_order, serialized)
    replayed_keys = [
        {(assemble_order[i]["source_id"], assemble_order[i]["statement"]) for i in grp}
        for grp in replayed
    ]
    assert replayed_keys[0] == {("a", "prefer caching"), ("b", "prefer caching strongly")}
    assert replayed_keys[1] == {("c", "use a bulkhead to isolate failures")}
    # Position 0 in assemble_order is the bulkhead principle — a naive position-keyed reuse of
    # emit_groups would have wrongly merged it; the identity replay does not.
    assert 0 not in replayed[0]


def test_deserialize_rejects_changed_principle_set():
    emit_order = [_gp("a", "alpha", ["C1"]), _gp("b", "beta", ["C2"])]
    serialized = serialize_groups(emit_order, [[0, 1]])
    changed = [_gp("a", "alpha", ["C1"]), _gp("b", "DIFFERENT", ["C2"])]
    with pytest.raises(ValueError, match="no match in the current principle set"):
        deserialize_groups(changed, serialized)


def test_deserialize_rejects_grown_principle_set_superset():
    # The persisted payload covers only a SUBSET of the current principles: a module was re-MAP'd
    # and GAINED a principle between emit and assemble. Every old key still matches, so the existing
    # missing-member check never fires — but the new principle (index 2) is in NO group and would be
    # SILENTLY DROPPED from the distilled layer. deserialize_groups must instead fail loudly.
    emit_order = [_gp("a", "alpha", ["C1"]), _gp("b", "beta", ["C2"])]
    serialized = serialize_groups(emit_order, [[0, 1]])
    grown = [
        _gp("a", "alpha", ["C1"]),
        _gp("b", "beta", ["C2"]),
        _gp("c", "newly added principle", ["C3"]),  # gained after the grouping was persisted
    ]
    with pytest.raises(ValueError, match="uncovered"):
        deserialize_groups(grown, serialized)


def test_emit_persist_assemble_applies_decision_to_original_cluster(tmp_path):
    # End-to-end of the two-phase contract: emit produces a grouping, it is persisted by stable
    # identity, and assemble loading the persisted groups applies the decision to the SAME cluster
    # even when fed a DIFFERENT principle order than emit saw.
    sources = _fixture(tmp_path)
    mods = load_modules(sources, tmp_path / "cache" / "book-extracts")
    cmap, _ = build_claim_map(mods)
    gp = globalize_principles(mods, cmap)
    groups = build_groups(gp, _fake_embedder, cos=0.5)
    clusters = emit_clusters(gp, _fake_embedder, cos=0.5, groups=groups)
    assert clusters and clusters[0]["group"] == 0
    serialized = serialize_groups(gp, groups)

    # Simulate the assemble process re-globalizing in a different order, then replaying the groups.
    reshuffled = list(reversed(gp))
    replayed = deserialize_groups(reshuffled, serialized)
    # Replayed group 0 still contains exactly the two original cache-principle identities.
    keys = {(reshuffled[i]["source_id"], reshuffled[i]["statement"]) for i in replayed[0]}
    assert keys == {("alpha-0001", "prefer caching"), ("beta-0002", "prefer caching strongly")}

    # assemble with the persisted (replayed) groups confirms the shared cluster -> 1 merged principle.
    summary = assemble(
        "demo-persist",
        sources,
        repo=tmp_path,
        embedder=_fake_embedder,
        cos=0.5,
        decisions={clusters[0]["group"]: {"action": "confirm"}},
        select=0,
        groups=build_groups(gp, _fake_embedder, cos=0.5),
    )
    assert summary["principles"] == 1
