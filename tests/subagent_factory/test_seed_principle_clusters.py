"""Tests for the deterministic cross-source principle-cluster seeder (Step 7 Phase A)."""

import json

import yaml

from tools.subagent_factory.seed_principle_clusters import _cosine, seed_clusters

_OVERLAP = "deep modules reduce complexity through information hiding"


def _pkg(tmp_path, principles, claims):
    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "analysis").mkdir(parents=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c) for c in claims) + "\n", encoding="utf-8"
    )
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump({"schema_version": "principles-v1", "principles": principles}),
        encoding="utf-8",
    )
    return base


def test_seeds_cross_source_cluster(tmp_path):
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
        {"claim_id": "c3", "source_id": "bookA", "statement": "z"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": _OVERLAP,
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": _OVERLAP + " always",
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
        {
            "principle_id": "P3",
            "statement": "prefer cats over dogs in quiet gardens",
            "derived_from_claims": ["c3"],
            "confidence": "high",
        },
    ]
    r = seed_clusters(_pkg(tmp_path, principles, claims), 0.15)
    assert len(r["clusters"]) == 1
    c = r["clusters"][0]
    assert set(c["member_principle_ids"]) == {"P1", "P2"}
    assert set(c["sources"]) == {"bookA", "bookB"}
    assert c["method"] == "seed" and c["canonical_statement"] is None


def test_same_source_not_clustered(tmp_path):
    # identical statements but BOTH from one source → not cross-source → no cluster.
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookA", "statement": "y"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": _OVERLAP,
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": _OVERLAP,
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
    ]
    assert seed_clusters(_pkg(tmp_path, principles, claims), 0.15)["clusters"] == []


def test_below_threshold_no_cluster(tmp_path):
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": "deep modules hide implementation complexity",
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": "prefer cats over dogs in gardens",
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
    ]
    assert seed_clusters(_pkg(tmp_path, principles, claims), 0.5)["clusters"] == []


# ---- C1: embedding-cosine augmentation (fake embedder, CI-safe) ------------------------------

# Two cross-source paraphrases that share NO content tokens (token-F1 = 0) but mean the same thing.
_P1_STMT = "understand the counterpart perspective"
_P2_STMT = "grasp how the other party feels"
_P3_STMT = "prefer cats over dogs in gardens"
# cosine(P1,P2) = 0.8 (above the 0.6 default, below a 0.99 bar); P3 orthogonal.
_VECS = {_P1_STMT: [1.0, 0.0, 0.0], _P2_STMT: [0.8, 0.6, 0.0], _P3_STMT: [0.0, 0.0, 1.0]}


def _fake_embedder(statements):
    return [_VECS[s] for s in statements]


def _paraphrase_pkg(tmp_path):
    claims = [
        {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
        {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
        {"claim_id": "c3", "source_id": "bookB", "statement": "z"},
    ]
    principles = [
        {
            "principle_id": "P1",
            "statement": _P1_STMT,
            "derived_from_claims": ["c1"],
            "confidence": "high",
        },
        {
            "principle_id": "P2",
            "statement": _P2_STMT,
            "derived_from_claims": ["c2"],
            "confidence": "high",
        },
        {
            "principle_id": "P3",
            "statement": _P3_STMT,
            "derived_from_claims": ["c3"],
            "confidence": "high",
        },
    ]
    return _pkg(tmp_path, principles, claims)


def test_cosine_basic():
    assert _cosine([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert _cosine([1.0, 0.0], [0.0, 1.0]) == 0.0
    assert _cosine([0.0, 0.0], [1.0, 1.0]) == 0.0  # zero vector -> 0, no div error


def test_lexical_only_misses_paraphrase(tmp_path):
    # P1/P2 share no content tokens -> lexical seeder finds nothing
    assert seed_clusters(_paraphrase_pkg(tmp_path), 0.15)["clusters"] == []


def test_embedding_pairs_paraphrase_token_f1_misses(tmp_path):
    r = seed_clusters(_paraphrase_pkg(tmp_path), 0.15, embedder=_fake_embedder)
    assert len(r["clusters"]) == 1
    c = r["clusters"][0]
    assert set(c["member_principle_ids"]) == {"P1", "P2"}  # P3 (orthogonal) not merged
    assert set(c["sources"]) == {"bookA", "bookB"}
    assert c["method"] == "seed"  # schema unchanged
    assert c["mean_overlap"] == 0.0  # joined by embedding, not lexical overlap


def test_embedding_respects_cos_threshold(tmp_path):
    # raise the absolute floor above the pair's 0.8 cosine -> no merge
    assert (
        seed_clusters(_paraphrase_pkg(tmp_path), 0.15, embedder=_fake_embedder, cos_threshold=0.99)[
            "clusters"
        ]
        == []
    )


# ---- C1(c): margin-above-baseline structural discrimination (fixes the over-merge) -----------


def _clusters_pkg(tmp_path, vecs, sources):
    """Build a package from {statement: vector} + {statement: source}; statements share no tokens."""
    claims, principles, embmap = [], [], {}
    for i, (stmt, vec) in enumerate(vecs.items(), 1):
        cid, pid = f"c{i}", f"P{i}"
        claims.append({"claim_id": cid, "source_id": sources[stmt], "statement": "x"})
        principles.append(
            {
                "principle_id": pid,
                "statement": stmt,
                "derived_from_claims": [cid],
                "confidence": "high",
            }
        )
        embmap[stmt] = vec
    base = _pkg(tmp_path, principles, claims)
    return base, (lambda stmts: [embmap[s] for s in stmts])


def test_margin_rejects_same_topic_blob(tmp_path):
    # X,Y,Z all pairwise cosine 0.5 across sources: each clears the 0.5 floor but none STANDS OUT
    # above its peers' mean -> margin blocks the over-merge.
    vecs = {
        "alpha apple": [1.0, 0.0],
        "bravo banana": [0.5, 0.866],
        "charlie cherry": [0.5, -0.866],
    }
    src = {"alpha apple": "A", "bravo banana": "B", "charlie cherry": "B"}
    base, emb = _clusters_pkg(tmp_path, vecs, src)
    assert seed_clusters(base, 0.99, embedder=emb, cos_threshold=0.5)["clusters"] == []


def test_margin_keeps_standout_pair(tmp_path):
    # P~Q cosine 0.85 (a real paraphrase) well above P's other peer (R at 0.3) -> stands out -> merge
    vecs = {"delta date": [1.0, 0.0], "echo fig": [0.85, 0.527], "foxtrot grape": [0.3, 0.954]}
    src = {"delta date": "A", "echo fig": "B", "foxtrot grape": "B"}
    base, emb = _clusters_pkg(tmp_path, vecs, src)
    r = seed_clusters(base, 0.99, embedder=emb, cos_threshold=0.5)
    assert len(r["clusters"]) == 1
    assert set(r["clusters"][0]["member_principle_ids"]) == {"P1", "P2"}  # P/Q, not R
