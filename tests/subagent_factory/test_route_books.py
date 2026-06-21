"""Tests for the deterministic per-book engine router (P1)."""

from pathlib import Path

from tools.subagent_factory.route_books import classify, route_books


def _mk(tmp_path: Path, name: str, nbytes: int) -> Path:
    p = tmp_path / name
    p.write_text("x" * nbytes, encoding="utf-8")
    return p


def test_small_routes_to_copilot(tmp_path):
    p = _mk(tmp_path, "small.md", 80_000)  # 20k tok
    r = classify(p, threshold_tokens=100_000)
    assert r["class"] == "small"
    assert r["engine"] == "copilot"


def test_large_routes_to_claude(tmp_path):
    p = _mk(tmp_path, "big.md", 1_200_000)  # 300k tok
    r = classify(p, threshold_tokens=100_000)
    assert r["class"] == "large"
    assert r["engine"] == "claude"


def test_threshold_is_inclusive_small(tmp_path):
    p = _mk(tmp_path, "edge.md", 400_000)  # exactly 100k tok
    assert classify(p, threshold_tokens=100_000)["class"] == "small"


def test_route_books_over_dir_files(tmp_path):
    _mk(tmp_path, "a.md", 40_000)
    _mk(tmp_path, "b.md", 800_000)
    rows = route_books([str(tmp_path / "a.md"), str(tmp_path / "b.md")], threshold_tokens=100_000)
    engines = {Path(r["source"]).name: r["engine"] for r in rows}
    assert engines == {"a.md": "copilot", "b.md": "claude"}
