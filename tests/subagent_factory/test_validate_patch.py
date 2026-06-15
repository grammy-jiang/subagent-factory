"""Tests for the deterministic patch-validation ladder (Step-6 I-track)."""

import shutil
import subprocess

import pytest

from tools.subagent_factory.validate_patch import (
    FilePatch,
    RunResult,
    check_scope,
    parse_unified_diff,
    select_patch,
    shell_runner,
    validate_patch,
)

_GIT_DIFF = """\
diff --git a/src/calc.py b/src/calc.py
index 1111111..2222222 100644
--- a/src/calc.py
+++ b/src/calc.py
@@ -1,3 +1,3 @@
 def add(a, b):
-    return a - b
+    return a + b
"""

_TWO_FILE_DIFF = """\
diff --git a/a.py b/a.py
--- a/a.py
+++ b/a.py
@@ -1 +1 @@
-x
+y
diff --git a/b.py b/b.py
--- a/b.py
+++ b/b.py
@@ -1 +1,2 @@
 keep
+added
"""


# ── parse_unified_diff ──


def test_parse_single_file():
    fps = parse_unified_diff(_GIT_DIFF)
    assert fps == [FilePatch("src/calc.py", added=1, removed=1, hunks=1)]


def test_parse_two_files():
    fps = parse_unified_diff(_TWO_FILE_DIFF)
    assert [f.path for f in fps] == ["a.py", "b.py"]
    assert fps[1] == FilePatch("b.py", added=1, removed=0, hunks=1)


def test_parse_plain_diff_no_git_header():
    diff = "--- a/x.txt\n+++ b/x.txt\n@@ -1 +1 @@\n-old\n+new\n"
    assert parse_unified_diff(diff) == [FilePatch("x.txt", 1, 1, 1)]


def test_parse_file_creation_dev_null():
    diff = "--- /dev/null\n+++ b/new.py\n@@ -0,0 +1,2 @@\n+line1\n+line2\n"
    fps = parse_unified_diff(diff)
    assert fps[0].path == "new.py" and fps[0].added == 2 and fps[0].removed == 0


def test_parse_file_deletion_dev_null():
    diff = "--- a/gone.py\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-a\n-b\n"
    fps = parse_unified_diff(diff)
    assert fps[0].path == "gone.py" and fps[0].removed == 2


def test_parse_empty_raises():
    with pytest.raises(ValueError):
        parse_unified_diff("   \n")


def test_parse_headers_only_no_hunk_raises():
    with pytest.raises(ValueError):
        parse_unified_diff("diff --git a/x b/x\n--- a/x\n+++ b/x\n")


def test_parse_hunk_before_file_raises():
    with pytest.raises(ValueError):
        parse_unified_diff("@@ -1 +1 @@\n-a\n+b\n")


# ── check_scope (I5) ──

_FILES = [FilePatch("src/calc.py", 1, 1, 1)]


def test_scope_within_bounds():
    ok, detail = check_scope(_FILES, {"allow_paths": ["src/"], "max_files": 3})
    assert ok is True and "within bounds" in detail


def test_scope_deny_canonical_artifact():
    files = [FilePatch("subagents/foo/profile.yaml", 2, 0, 1)]
    ok, detail = check_scope(files, {"deny_paths": ["subagents/", ".claude/agents/generated/"]})
    assert ok is False and "denied" in detail


def test_scope_allow_miss():
    ok, detail = check_scope(_FILES, {"allow_paths": ["tests/"]})
    assert ok is False and "outside allow_paths" in detail


def test_scope_glob_allow():
    ok, _ = check_scope(_FILES, {"allow_paths": ["src/*.py"]})
    assert ok is True


def test_scope_max_files_exceeded():
    files = [FilePatch(f"f{i}.py", 1, 0, 1) for i in range(4)]
    ok, detail = check_scope(files, {"max_files": 2})
    assert ok is False and "files 4 exceeds max_files=2" in detail


def test_scope_max_changed_lines_exceeded():
    files = [FilePatch("big.py", 50, 60, 1)]
    ok, detail = check_scope(files, {"max_changed_lines": 100})
    assert ok is False and "changed lines 110 exceeds" in detail


# ── validate_patch verdicts ──


def _ok_runner(_phase):
    return RunResult(True, "ok")


def test_verdict_parse_fail():
    res = validate_patch("not a diff at all")
    assert res["verdict"] == "fail" and res["stopped_at"] == "parse"


def test_verdict_scope_fail_stops_before_execution():
    res = validate_patch(_GIT_DIFF, scope={"allow_paths": ["tests/"]}, runner=_ok_runner)
    assert res["verdict"] == "fail" and res["stopped_at"] == "scope"
    rungs = {r["rung"]: r["status"] for r in res["rungs"]}
    assert "reproduce" not in rungs  # short-circuit: execution rungs never recorded


def test_verdict_needs_human_without_runner():
    res = validate_patch(_GIT_DIFF, scope={"allow_paths": ["src/"]})
    assert res["verdict"] == "needs_human"  # scope passed but execution rungs skipped
    rungs = {r["rung"]: r["status"] for r in res["rungs"]}
    assert rungs["scope"] == "pass" and rungs["reproduce"] == "skip"


def test_verdict_needs_human_without_scope():
    res = validate_patch(_GIT_DIFF, runner=_ok_runner)
    assert res["verdict"] == "needs_human"  # reproduce/regress pass, but no scope bound
    assert any(r["rung"] == "scope" and r["status"] == "skip" for r in res["rungs"])


def test_verdict_pass_full_ladder():
    res = validate_patch(_GIT_DIFF, scope={"allow_paths": ["src/"]}, runner=_ok_runner)
    assert res["verdict"] == "pass" and res["stopped_at"] is None


def test_verdict_pass_when_ci_not_requested():
    res = validate_patch(
        _GIT_DIFF,
        scope={"allow_paths": ["src/"]},
        runner=_ok_runner,
        request=("reproduce", "regress"),
    )
    assert res["verdict"] == "pass"
    assert any(r["rung"] == "ci" and r["status"] == "skip" for r in res["rungs"])


def test_verdict_reproduce_fail():
    def runner(phase):
        return RunResult(phase != "reproduce", "boom" if phase == "reproduce" else "ok")

    res = validate_patch(_GIT_DIFF, scope={"allow_paths": ["src/"]}, runner=runner)
    assert res["verdict"] == "fail" and res["stopped_at"] == "reproduce"


def test_verdict_runner_exception_is_failure_not_crash():
    def runner(_phase):
        raise RuntimeError("harness died")

    res = validate_patch(_GIT_DIFF, scope={"allow_paths": ["src/"]}, runner=runner)
    assert res["verdict"] == "fail" and res["stopped_at"] == "reproduce"
    assert "harness died" in res["rungs"][-1]["detail"]


# ── select_patch (I3: deterministic gate decides, ranker only orders passing) ──


def test_select_skips_failing_keeps_passing():
    # candidate 0 fails scope (touches a denied path), candidate 1 passes
    bad = "--- a/subagents/x/profile.yaml\n+++ b/subagents/x/profile.yaml\n@@ -1 +1 @@\n-a\n+b\n"
    out = select_patch(
        [bad, _GIT_DIFF],
        scope={"allow_paths": ["src/", "subagents/"], "deny_paths": ["subagents/"]},
        runner_for=lambda _i: _ok_runner,
    )
    assert out["selected"] == 1 and out["passing"] == [1]
    assert out["verdict_per"][0] == "fail"


def test_select_ranker_cannot_pick_failing_candidate():
    bad = "garbage, not a diff"
    out = select_patch(
        [bad, _GIT_DIFF],
        scope={"allow_paths": ["src/"]},
        runner_for=lambda _i: _ok_runner,
        ranker=lambda _passing: 0,  # tries to pick the failed candidate 0
    )
    assert out["selected"] == 1  # ranker overruled — 0 never passed (I3 guarantee)
    assert "fell back" in out["reason"]


def test_select_ranker_orders_among_passing():
    out = select_patch(
        [_GIT_DIFF, _GIT_DIFF],
        scope={"allow_paths": ["src/"]},
        runner_for=lambda _i: _ok_runner,
        ranker=lambda passing: passing[-1],
    )
    assert out["selected"] == 1 and out["reason"] == "ranked among passing candidates"


def test_select_none_pass():
    out = select_patch(["junk", "also junk"], scope={"allow_paths": ["src/"]})
    assert out["selected"] is None and out["passing"] == []
    assert "no candidate passed" in out["reason"]


# ── shell_runner (real subprocess + git; the live adapter) ──

_HAVE_GIT = shutil.which("git") is not None


def _git(repo, *args):
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


# RED command keys its exit code off a data file (no import → no stale-pyc artifact): exit 0 iff
# the first line of val.txt is "2". Lets the test exercise shell_runner's apply/run/revert cleanly.
def _red(repo):
    import sys

    code = "import sys,pathlib;sys.exit(0 if pathlib.Path('val.txt').read_text().splitlines()[0]=='2' else 1)"
    return f'{sys.executable} -c "{code}"'


@pytest.mark.skipif(not _HAVE_GIT, reason="git not available")
def test_shell_runner_reproduce_and_autorevert(tmp_path):
    repo = tmp_path
    (repo / "val.txt").write_text("1\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")

    # produce a patch that flips 1 -> 2, then return the tree to baseline
    (repo / "val.txt").write_text("2\n", encoding="utf-8")
    diff = subprocess.run(["git", "diff"], cwd=repo, capture_output=True, text=True).stdout
    (repo / "fix.patch").write_text(diff, encoding="utf-8")
    _git(repo, "checkout", "--", "val.txt")

    red = _red(repo)
    runner = shell_runner(repo, patch_file=repo / "fix.patch", repro_cmd=red, regress_cmd=red)

    rep = runner("reproduce")
    assert rep.ok is True  # failed at baseline (1), passes after patch (2)
    # tree restored after the rung (auto-revert) → baseline value 1 is back
    assert (repo / "val.txt").read_text(encoding="utf-8").strip() == "1"

    # regress runs on the patched tree, then reverts too
    assert runner("regress").ok is True
    assert (repo / "val.txt").read_text(encoding="utf-8").strip() == "1"


@pytest.mark.skipif(not _HAVE_GIT, reason="git not available")
def test_shell_runner_reproduce_fails_when_bug_not_reproduced(tmp_path):
    repo = tmp_path
    (repo / "val.txt").write_text("2\n", encoding="utf-8")  # RED test already passes at baseline
    _git(repo, "init", "-q")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")
    (repo / "val.txt").write_text("2\nappended\n", encoding="utf-8")
    diff = subprocess.run(["git", "diff"], cwd=repo, capture_output=True, text=True).stdout
    (repo / "noop.patch").write_text(diff, encoding="utf-8")
    _git(repo, "checkout", "--", "val.txt")

    runner = shell_runner(repo, patch_file=repo / "noop.patch", repro_cmd=_red(repo))
    assert runner("reproduce").ok is False  # bug not reproduced pre-patch


def test_shell_runner_no_command_for_phase():
    r = shell_runner("/tmp", patch_file="/tmp/x.patch", repro_cmd="true")
    assert r("ci").ok is False  # ci_cmd not configured
