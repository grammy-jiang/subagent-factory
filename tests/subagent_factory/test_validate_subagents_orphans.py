"""Tests for the repo-level adapter/package consistency gate.

Regression: on 2026-07-25, 14 installed adapters had no canonical package — 8 whose packages
lived only on an unmerged local branch, 6 whose packages were on no ref at all. Every one of them
was loadable by the runtime and invisible to CI, because `cli validate <slug>` runs per package
and a package that does not exist is never validated.
"""

import importlib.util
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "tools" / "precommit" / "validate_subagents.py"
_spec = importlib.util.spec_from_file_location("validate_subagents", _SRC)
vs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vs)


def _repo(tmp_path: Path, packages=(), adapters=()) -> Path:
    for slug in packages:
        pkg = tmp_path / "subagents" / slug
        pkg.mkdir(parents=True)
        (pkg / "profile.yaml").write_text(f"slug: {slug}\n", encoding="utf-8")
    gen = tmp_path / ".claude" / "agents" / "generated"
    gen.mkdir(parents=True)
    for slug in adapters:
        (gen / f"{slug}.md").write_text("---\nname: x\n---\n", encoding="utf-8")
    return tmp_path


def test_matched_adapter_and_package_is_clean(tmp_path):
    root = _repo(tmp_path, packages=["demo-advisor"], adapters=["demo-advisor"])
    assert vs.orphan_adapters(root) == []


def test_adapter_without_package_is_reported(tmp_path):
    root = _repo(tmp_path, packages=["demo-advisor"], adapters=["demo-advisor", "ghost-advisor"])
    assert vs.orphan_adapters(root) == ["ghost-advisor"]


def test_package_without_adapter_is_not_an_orphan(tmp_path):
    # The invariant is one-directional: a package may legitimately exist before its first export.
    root = _repo(
        tmp_path, packages=["demo-advisor", "unexported-advisor"], adapters=["demo-advisor"]
    )
    assert vs.orphan_adapters(root) == []


def test_readme_is_not_treated_as_an_adapter(tmp_path):
    root = _repo(tmp_path, packages=["demo-advisor"], adapters=["demo-advisor", "README"])
    assert vs.orphan_adapters(root) == []


def test_multiple_orphans_are_all_reported_sorted(tmp_path):
    root = _repo(tmp_path, packages=[], adapters=["zeta-advisor", "alpha-reviewer"])
    assert vs.orphan_adapters(root) == ["alpha-reviewer", "zeta-advisor"]


def test_missing_adapter_dir_is_not_an_error(tmp_path):
    (tmp_path / "subagents").mkdir()
    assert vs.orphan_adapters(tmp_path) == []


def test_main_fails_before_the_no_changes_early_return(tmp_path, monkeypatch, capsys):
    # An orphan adapter is precisely the case where NO package changed, so the check must run
    # ahead of main()'s "No subagent package changes to validate." early return.
    root = _repo(tmp_path, packages=["demo-advisor"], adapters=["demo-advisor", "ghost-advisor"])
    monkeypatch.setattr(vs, "repo_root", lambda: root)
    assert vs.main([]) == 1
    err = capsys.readouterr().err
    assert "ADAPTER/PACKAGE MISMATCH" in err
    assert "ghost-advisor" in err


def test_main_passes_when_consistent(tmp_path, monkeypatch):
    root = _repo(tmp_path, packages=["demo-advisor"], adapters=["demo-advisor"])
    monkeypatch.setattr(vs, "repo_root", lambda: root)
    assert vs.main([]) == 0
