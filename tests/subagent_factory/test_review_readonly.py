"""Corrective read-only guard for review sessions (campaign/_review_readonly.sh).

Write cannot be permission-scoped in this claude version (see _claude_run.sh), so the review loop
reverts any NON-report file a review session writes to the package it reviews. These tests drive the
bash helper (snapshot → simulate a review → enforce) against a throwaway git repo. The load-bearing
case is that the guard reverts only THIS review's writes and never wipes an uncommitted prior fix.
"""

import subprocess
from pathlib import Path

import pytest

_HELPER = Path(__file__).resolve().parents[2] / "campaign" / "_review_readonly.sh"


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _repo_with_package(tmp_path):
    repo = tmp_path / "repo"
    pkg = repo / "subagents" / "x"
    (pkg / "reports").mkdir(parents=True)
    (pkg / "profile.yaml").write_text("slug: x\n")
    (pkg / "skill.md").write_text("original skill\n")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "init")
    return repo, pkg


def _run(repo, simulate):
    """snapshot -> run `simulate` (bash simulating the review session) -> enforce; return the count."""
    script = f"""
      set -euo pipefail
      cd {repo}
      source {_HELPER}
      before_ut=$(mktemp)
      pre=$(review_readonly_snapshot subagents/x "$before_ut")
      {simulate}
      review_readonly_enforce subagents/x "$pre" "$before_ut"
    """
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


@pytest.mark.skipif(not _HELPER.exists(), reason="review-readonly helper not present")
def test_reverts_stray_writes_keeps_report(tmp_path):
    repo, pkg = _repo_with_package(tmp_path)
    n = _run(
        repo,
        """
          echo 'INJECTED' >> subagents/x/profile.yaml     # stray tracked modification
          echo 'new' > subagents/x/STRAY.md               # stray new file
          echo 'the report' > subagents/x/reports/r1.md   # legitimate report output
        """,
    )
    assert (pkg / "profile.yaml").read_text() == "slug: x\n"  # stray mod reverted
    assert not (pkg / "STRAY.md").exists()  # stray new file deleted
    assert (pkg / "reports" / "r1.md").read_text() == "the report\n"  # report kept
    assert n == "2"


@pytest.mark.skipif(not _HELPER.exists(), reason="review-readonly helper not present")
def test_preserves_uncommitted_prior_fix(tmp_path):
    repo, pkg = _repo_with_package(tmp_path)
    # A prior failed fix left uncommitted changes: a tracked modification + a new untracked file.
    (pkg / "skill.md").write_text("FIXED skill\n")
    (pkg / "new_ref.md").write_text("prior fix new ref\n")
    n = _run(
        repo,
        """
          echo 'INJECTED' >> subagents/x/profile.yaml     # THIS review's stray write
          echo 'the report' > subagents/x/reports/r1.md   # legitimate report output
        """,
    )
    # This review's stray is reverted:
    assert (pkg / "profile.yaml").read_text() == "slug: x\n"
    assert (pkg / "reports" / "r1.md").read_text() == "the report\n"
    # ...but the uncommitted prior fix must be PRESERVED (not wiped by the guard):
    assert (pkg / "skill.md").read_text() == "FIXED skill\n"
    assert (pkg / "new_ref.md").read_text() == "prior fix new ref\n"
    assert n == "1"


@pytest.mark.skipif(not _HELPER.exists(), reason="review-readonly helper not present")
def test_clean_review_reverts_nothing(tmp_path):
    repo, pkg = _repo_with_package(tmp_path)
    n = _run(repo, "echo 'the report' > subagents/x/reports/r1.md")
    assert (pkg / "reports" / "r1.md").read_text() == "the report\n"
    assert (pkg / "profile.yaml").read_text() == "slug: x\n"
    assert n == "0"
