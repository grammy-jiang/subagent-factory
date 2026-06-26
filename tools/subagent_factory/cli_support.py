"""Shared helpers for the subagent-factory CLI command modules."""

import re
from collections.abc import Iterable, Sequence
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

# Single source of truth for the status -> Rich-color palette used across the
# maintenance commands. Statuses not listed render uncolored ("white").
STATUS_COLORS: dict[str, str] = {
    "ready": "green",
    "draft": "yellow",
    "missing": "red",
}


def status_color(status: str) -> str:
    """Rich color for a package ``status`` (falls back to ``white``)."""
    return STATUS_COLORS.get(status, "white")


def render_table(
    title: str,
    columns: Sequence[str | tuple[str, dict]],
    rows: Iterable[Sequence[str]],
) -> None:
    """Build and print a Rich table from plain data.

    ``columns`` entries are either a header string or ``(header, kwargs)`` where
    ``kwargs`` is passed straight to :meth:`rich.table.Table.add_column` (e.g.
    ``{"justify": "right"}``). ``rows`` are sequences of pre-formatted cell
    strings (markup such as ``[green]ok[/green]`` is honored).
    """
    table = Table(title=title)
    for col in columns:
        if isinstance(col, tuple):
            header, kwargs = col
            table.add_column(header, **kwargs)
        else:
            table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


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
