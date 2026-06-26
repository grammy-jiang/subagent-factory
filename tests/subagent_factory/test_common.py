"""Tests for tools.subagent_factory._common.atomic_write_text.

Focus: the helper must land byte-identical content at the target and leave no temp orphan,
and it must use a *unique* sibling temp name (not a fixed ``<name>.tmp``) so concurrent
writers to the same target cannot share a temp file and tear each other's write.
"""

from __future__ import annotations

import os

import pytest

from tools.subagent_factory import _common
from tools.subagent_factory._common import atomic_write_text, cosine


def test_cosine_raises_on_length_mismatch():
    # Mismatched lengths are always an upstream bug (same-space embeddings), never ragged data:
    # strict=True must surface it loudly instead of silently truncating to the shorter vector.
    with pytest.raises(ValueError):
        cosine([1.0, 0.0], [1.0, 0.0, 0.0])


def test_cosine_zero_vector_returns_zero():
    # Zero-norm guard still holds for equal-length vectors under strict=True.
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0
    assert cosine([0.0, 0.0], [0.0, 0.0]) == 0.0


def test_atomic_write_lands_content(tmp_path):
    target = tmp_path / "out.txt"
    atomic_write_text(target, "hello world")
    assert target.read_text(encoding="utf-8") == "hello world"


def test_atomic_write_overwrites(tmp_path):
    target = tmp_path / "out.txt"
    atomic_write_text(target, "first")
    atomic_write_text(target, "second")
    assert target.read_text(encoding="utf-8") == "second"


def test_atomic_write_no_temp_orphan_after_sequential_calls(tmp_path):
    # Two sequential writes to the same target leave only the target, no .tmp orphan.
    target = tmp_path / "out.txt"
    atomic_write_text(target, "a")
    atomic_write_text(target, "b")
    assert target.read_text(encoding="utf-8") == "b"
    assert not list(tmp_path.glob("*.tmp"))
    assert list(tmp_path.iterdir()) == [target]


def test_temp_name_is_unique_not_fixed_suffix(tmp_path, monkeypatch):
    # Capture the temp path os.replace renames from; it must NOT be the fixed "<name>.tmp"
    # that two writers would collide on, and must differ across calls.
    target = tmp_path / "out.txt"
    fixed = tmp_path / "out.txt.tmp"
    seen: list[str] = []
    real_replace = os.replace

    def capturing_replace(src, dst):
        seen.append(str(src))
        return real_replace(src, dst)

    monkeypatch.setattr(_common.os, "replace", capturing_replace)
    atomic_write_text(target, "one")
    atomic_write_text(target, "two")

    assert len(seen) == 2
    assert str(fixed) not in seen  # not the collision-prone fixed name
    assert seen[0] != seen[1]  # unique per call
    # Each temp is still a sibling of the target (same filesystem for atomic rename).
    for src in seen:
        assert os.path.dirname(src) == str(tmp_path)


def test_no_temp_orphan_when_replace_fails(tmp_path, monkeypatch):
    # If os.replace raises, the temp file must be cleaned up (no orphan left behind).
    target = tmp_path / "out.txt"

    def boom(src, dst):
        raise OSError("simulated replace failure")

    monkeypatch.setattr(_common.os, "replace", boom)
    try:
        atomic_write_text(target, "data")
    except OSError:
        pass
    else:  # pragma: no cover - defensive
        raise AssertionError("expected os.replace failure to propagate")

    assert not list(tmp_path.glob("*.tmp"))
    assert not target.exists()
