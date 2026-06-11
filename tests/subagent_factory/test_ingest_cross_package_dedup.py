"""Tests for cross-package duplicate-source detection.

The per-slug manifest dedup only sees the current package, and the embedding-based
`search` is sha256-blind, so an identical source already authored under a *different*
slug can be silently re-authored as a redundant package. ``find_cross_package_duplicates``
surfaces that case so the caller can confirm a distinct role or update the existing package.
"""

import yaml

from tools.subagent_factory.ingest_source import find_cross_package_duplicates

SHA = "a" * 64
OTHER = "b" * 64


def _write_manifest(packages_root, slug, sources):
    pkg = packages_root / slug
    pkg.mkdir(parents=True)
    (pkg / "source-pack.manifest.yaml").write_text(
        yaml.safe_dump({"subagent_slug": slug, "sources": sources}),
        encoding="utf-8",
    )


def test_detects_identical_source_under_other_slug(tmp_path):
    _write_manifest(tmp_path, "existing-pkg", [{"source_id": "src-1", "sha256": SHA}])
    matches = find_cross_package_duplicates(tmp_path, SHA, current_slug="new-pkg")
    assert matches == [{"slug": "existing-pkg", "source_id": "src-1"}]


def test_excludes_current_slug(tmp_path):
    # A match inside the package being ingested into is handled by the per-slug dedup,
    # not reported here, so it must not be flagged as a cross-package duplicate.
    _write_manifest(tmp_path, "new-pkg", [{"source_id": "src-1", "sha256": SHA}])
    assert find_cross_package_duplicates(tmp_path, SHA, current_slug="new-pkg") == []


def test_no_match_for_different_sha(tmp_path):
    _write_manifest(tmp_path, "existing-pkg", [{"source_id": "src-1", "sha256": OTHER}])
    assert find_cross_package_duplicates(tmp_path, SHA, current_slug="new-pkg") == []


def test_reports_every_slug_sharing_the_source(tmp_path):
    _write_manifest(tmp_path, "pkg-a", [{"source_id": "a-1", "sha256": SHA}])
    _write_manifest(tmp_path, "pkg-b", [{"source_id": "b-1", "sha256": OTHER}])
    _write_manifest(tmp_path, "pkg-c", [{"source_id": "c-1", "sha256": SHA}])
    matches = find_cross_package_duplicates(tmp_path, SHA, current_slug="new-pkg")
    assert matches == [
        {"slug": "pkg-a", "source_id": "a-1"},
        {"slug": "pkg-c", "source_id": "c-1"},
    ]


def test_missing_packages_root_returns_empty(tmp_path):
    assert find_cross_package_duplicates(tmp_path / "nope", SHA, current_slug="x") == []


def test_malformed_manifest_is_skipped(tmp_path):
    pkg = tmp_path / "broken"
    pkg.mkdir()
    (pkg / "source-pack.manifest.yaml").write_text("{not: valid: yaml:", encoding="utf-8")
    _write_manifest(tmp_path, "good", [{"source_id": "g-1", "sha256": SHA}])
    matches = find_cross_package_duplicates(tmp_path, SHA, current_slug="new-pkg")
    assert matches == [{"slug": "good", "source_id": "g-1"}]
