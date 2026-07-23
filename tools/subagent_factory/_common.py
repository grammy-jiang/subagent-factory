"""Small shared leaf-level constants and helpers for the factory.

Single source of truth for values/maths that were previously copy-pasted across modules.
This module imports nothing from the rest of the package, so it is safe to import from any
factory module without risking an import cycle.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

# Rough char -> token estimate, used by the chunker and the size router. Kept identical so a
# book's size class and its chunk token estimates agree.
CHARS_PER_TOKEN = 4


def iter_jsonl_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield ``(1-indexed line number, stripped non-blank line)`` for a JSONL body.

    Splits on ``"\\n"`` ONLY — NOT ``str.splitlines()``, which also breaks on U+2028/U+2029/U+0085
    that ``ensure_ascii=False`` output can carry inside a string value, shattering one well-formed
    record into "invalid JSON" fragments. Blank lines are skipped. Shared by every reader of the
    injection-scan.jsonl artifact so a corrupted-line policy cannot drift between them (the loader and
    the validator must agree)."""
    for i, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        if stripped:
            yield i, stripped


def atomic_write_text(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` via a sibling temp file + ``os.replace`` so a crash mid-write
    can never leave a truncated artifact behind.

    ``os.replace`` is atomic on the same filesystem, so a reader (or a content-addressed re-run
    that would otherwise trust a partially written file) sees either the old file or the complete
    new one. The temp file is a *unique* sibling of the target (``mkstemp`` in ``path.parent``): a
    per-writer name means two concurrent writers to the same target never share a temp file, so one
    writer's ``os.replace`` can never fire on a temp the other is still filling (the torn-write
    window a shared ``<name>.tmp`` reintroduced). The temp stays a sibling so the rename stays on one
    filesystem. Single owner for the pattern; see map_reduce_build and export_claude_agent.
    """
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        # No orphan temp left behind if writing or replacing fails.
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


# Confidence levels, ordered weakest -> strongest. "insufficient" is the abstention floor (K8).
# One ordering shared by the GRADE grader and the principle-importance ranker, so they cannot drift.
CONFIDENCE_LEVELS: tuple[str, ...] = ("insufficient", "low", "medium", "high")


def confidence_rank(level: str, *, default: str = "medium") -> int:
    """Ordinal rank of a confidence level (higher = stronger). Unknown level -> rank of ``default``."""
    if level in CONFIDENCE_LEVELS:
        return CONFIDENCE_LEVELS.index(level)
    return CONFIDENCE_LEVELS.index(default)


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors; 0.0 if either vector has zero norm.

    ``strict=True``: a length mismatch raises ``ValueError`` instead of silently truncating to
    the shorter vector. Cosine here is always over same-space embeddings from one embedder, so a
    differing length is always an upstream bug (it would otherwise corrupt clustering with a
    plausible-but-wrong score and no signal), never valid ragged data.
    """
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0
