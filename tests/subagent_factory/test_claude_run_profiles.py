"""Least-privilege session profiles in campaign/_claude_run.sh (item #1, leg B + the review guard).

build_claude_argv assembles the headless `claude -p` argv per CLAUDE_PERM_PROFILE. These tests drive
the bash builder and assert the permission flags, so a regression that widens a session's authority
(e.g. dropping the author network-tool deny) fails here rather than silently in production.
"""

import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_HELPER = _REPO / "campaign" / "_claude_run.sh"


def _argv(profile: str) -> str:
    script = f"""
      set -euo pipefail
      source {_HELPER}
      CLAUDE_PERM_PROFILE={profile} build_claude_argv argv "" ""
      printf '%s' "$(claude_argv_str "${{argv[@]}}")"
    """
    r = subprocess.run(["bash", "-c", script], cwd=_REPO, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


@pytest.mark.skipif(not _HELPER.exists(), reason="_claude_run.sh not present")
def test_author_profile_denies_agent_network_tools():
    argv = _argv("author")
    # Leg B of the lethal-trifecta fix: the author session keeps write/exec authority but loses its
    # own reach to the network (URL sources are prefetched; in-session ingest runs offline).
    assert "--disallowedTools 'WebFetch WebSearch'" in argv
    assert "--dangerously-skip-permissions" in argv


@pytest.mark.skipif(not _HELPER.exists(), reason="_claude_run.sh not present")
def test_review_profile_denies_edit():
    argv = _argv("review")
    assert "--disallowedTools Edit" in argv
    # The review profile must NOT carry the author network deny (distinct role, distinct flags).
    assert "WebFetch" not in argv


@pytest.mark.skipif(not _HELPER.exists(), reason="_claude_run.sh not present")
def test_default_profile_is_author():
    # An unset/unknown profile falls through to author (the default branch).
    assert "--disallowedTools 'WebFetch WebSearch'" in _argv("")
