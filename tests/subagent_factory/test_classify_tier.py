"""Tests for deterministic tier classification (enhancement Step 0)."""

from tools.subagent_factory.classify_tier import classify_tier


def _pkg(tmp_path, n_sources: int = 1, words: int = 10):
    base = tmp_path / "pkg"
    (base / "sources" / "markdown").mkdir(parents=True)
    sids = []
    for i in range(n_sources):
        sid = f"src-{i}"
        sids.append(sid)
        (base / "sources" / "markdown" / f"{sid}.md").write_text(
            " ".join(["word"] * words), encoding="utf-8"
        )
    manifest = "schema_version: source-pack-manifest-v1\nsources:\n" + "".join(
        f"  - source_id: {s}\n    metadata_path: m\n" for s in sids
    )
    (base / "source-pack.manifest.yaml").write_text(manifest, encoding="utf-8")
    return base


def test_short_single_source_is_tier0(tmp_path):
    assert classify_tier(_pkg(tmp_path, n_sources=1, words=100)) == 0


def test_long_single_source_is_tier1(tmp_path):
    assert classify_tier(_pkg(tmp_path, n_sources=1, words=20000)) == 1


def test_multi_source_is_tier2(tmp_path):
    assert classify_tier(_pkg(tmp_path, n_sources=2, words=100)) == 2


def test_missing_manifest_is_tier0(tmp_path):
    base = tmp_path / "empty"
    base.mkdir()
    assert classify_tier(base) == 0
