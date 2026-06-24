"""Small shared leaf-level constants and helpers for the factory.

Single source of truth for values/maths that were previously copy-pasted across modules.
This module imports nothing from the rest of the package, so it is safe to import from any
factory module without risking an import cycle.
"""

from __future__ import annotations

# Rough char -> token estimate, used by the chunker and the size router. Kept identical so a
# book's size class and its chunk token estimates agree.
CHARS_PER_TOKEN = 4

# Confidence levels, ordered weakest -> strongest. "insufficient" is the abstention floor (K8).
# One ordering shared by the GRADE grader and the principle-importance ranker, so they cannot drift.
CONFIDENCE_LEVELS: tuple[str, ...] = ("insufficient", "low", "medium", "high")


def confidence_rank(level: str, *, default: str = "medium") -> int:
    """Ordinal rank of a confidence level (higher = stronger). Unknown level -> rank of ``default``."""
    if level in CONFIDENCE_LEVELS:
        return CONFIDENCE_LEVELS.index(level)
    return CONFIDENCE_LEVELS.index(default)


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors; 0.0 if either vector has zero norm."""
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0
