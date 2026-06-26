"""Tests for the build checkpoint/resume substrate (P1)."""

from tools.subagent_factory.build_cache import atomic_write_text, is_done, mark_done, step_log


def test_atomic_write_lands_file_no_orphan(tmp_path):
    # atomic_write_text is now re-exported from _common (single owner, P010): it writes via a
    # unique sibling temp + os.replace and requires the parent dir to exist (caller's job).
    target = tmp_path / "out.txt"
    atomic_write_text(target, "hello")
    assert target.read_text() == "hello"
    assert list(tmp_path.glob("*.tmp")) == []  # unique sibling temp replaced away, no orphan


def test_mark_done_no_tmp_orphan_and_roundtrips(tmp_path):
    # mark_done creates the marker's parent and lands a .done that is_done parses back. After a
    # successful write no *.tmp sibling is left behind (the fixed-name collision bug is gone).
    step_dir = tmp_path / "steps"
    mark_done(step_dir, "claims", ["a", "b"])
    assert is_done(step_dir, "claims", ["a", "b"])
    assert (step_dir / "claims.done").exists()
    assert list(step_dir.glob("*.tmp")) == []


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
