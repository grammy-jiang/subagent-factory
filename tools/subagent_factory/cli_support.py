"""Shared helpers for the subagent-factory CLI command modules."""

import re
from pathlib import Path

import click
from rich.console import Console

console = Console()

# Generated-package slugs are kebab-case. Enforcing that where the path is built keeps a stray or
# malicious slug (absolute path, ".." traversal, or an embedded "/") from escaping subagents/.
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def repo_root() -> Path:
    """Repository root (three levels up from tools/subagent_factory/)."""
    return Path(__file__).parent.parent.parent


def subagent_path(slug: str) -> Path:
    """Path to a generated package: ``<repo>/subagents/<slug>``.

    ``slug`` must be kebab-case (``[a-z0-9-]``); this rejects absolute paths and ``..`` traversal so
    a slug cannot escape ``subagents/``.
    """
    if not _SLUG_RE.match(slug):
        raise click.BadParameter(f"invalid slug {slug!r}: must be kebab-case [a-z0-9-]")
    return repo_root() / "subagents" / slug
