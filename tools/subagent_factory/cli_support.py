"""Shared helpers for the subagent-factory CLI command modules."""

from pathlib import Path

from rich.console import Console

console = Console()


def repo_root() -> Path:
    """Repository root (three levels up from tools/subagent_factory/)."""
    return Path(__file__).parent.parent.parent


def subagent_path(slug: str) -> Path:
    """Path to a generated package: <repo>/subagents/<slug>."""
    return repo_root() / "subagents" / slug
