"""Shared CLI entry point for the leaf validators.

Most ``validate_*`` modules expose a ``validate_X(path) -> list[str]`` function and a near-identical
``main()``: check the single path arg, print one ``ERROR:`` line per error, exit 0 (clean) or 1.
``validator_main`` is that one harness, so each module's ``main`` is a one-line call.
"""

import sys
from collections.abc import Callable
from pathlib import Path

ValidateFn = Callable[[str | Path], list[str]]


def validator_main(validate_fn: ValidateFn, usage: str) -> None:
    """Run a leaf validator from the CLI: validate ``sys.argv[1]``, print each error, exit 0/1."""
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)
    errors = validate_fn(sys.argv[1])
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(0 if not errors else 1)
