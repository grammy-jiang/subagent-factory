"""Tests for the per-book over-extraction density guard (P3 #4)."""

import json

from tools.subagent_factory.extraction_density import density


def _mk(tmp_path, sid, n_claims, n_chunks):
    (tmp_path / "module.json").write_text(json.dumps({"source_id": sid}))
    (tmp_path / "claims.jsonl").write_text(
        "".join(json.dumps({"claim_id": f"C{i}"}) + "\n" for i in range(n_claims))
    )
    (tmp_path / "chunks.jsonl").write_text(
        "".join(json.dumps({"chunk_id": f"c{i}"}) + "\n" for i in range(n_chunks))
    )


def test_normal_density_ok(tmp_path):
    _mk(tmp_path, "book-1", n_claims=60, n_chunks=2)  # 30/chunk
    r = density(tmp_path, warn_per_chunk=80)
    assert r["per_chunk"] == 30.0 and r["over"] is False


def test_over_extraction_flagged(tmp_path):
    _mk(tmp_path, "book-2", n_claims=1428, n_chunks=4)  # 357/chunk (the sql-performance case)
    r = density(tmp_path, warn_per_chunk=80)
    assert r["per_chunk"] == 357.0 and r["over"] is True


def test_zero_chunks_does_not_crash(tmp_path):
    _mk(tmp_path, "book-3", n_claims=5, n_chunks=0)
    r = density(tmp_path, warn_per_chunk=80)
    assert r["chunks"] == 0 and r["over"] is False
