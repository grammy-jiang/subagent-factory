"""Tests for the build checkpoint/resume substrate (P1)."""

from tools.subagent_factory.build_cache import atomic_write_text, is_done, mark_done, step_log


def test_atomic_write_creates_file_and_parents(tmp_path):
    target = tmp_path / "sub" / "out.txt"
    atomic_write_text(target, "hello")
    assert target.read_text() == "hello"
    assert not (tmp_path / "sub" / "out.txt.tmp").exists()  # tmp renamed away


def test_done_roundtrip(tmp_path):
    assert not is_done(tmp_path, "claims", ["a", "b"])
    mark_done(tmp_path, "claims", ["a", "b"])
    assert is_done(tmp_path, "claims", ["a", "b"])


def test_done_invalidated_when_inputs_change(tmp_path):
    mark_done(tmp_path, "claims", ["a", "b"])
    assert is_done(tmp_path, "claims", ["a", "b"])
    assert not is_done(tmp_path, "claims", ["a", "c"])  # upstream changed -> stale -> re-run


def test_step_log_appends_jsonl(tmp_path):
    log = tmp_path / "steps.log.jsonl"
    step_log(log, step="map", sha="abc", status="ok")
    step_log(log, step="reduce", status="ok")
    lines = log.read_text().strip().splitlines()
    assert len(lines) == 2
    import json

    assert json.loads(lines[0])["step"] == "map"
