"""Heuristic quality assessment for converted Markdown.

A converter can return text yet still produce unusable output — e.g. a PDF with a
decorative vertical spine watermark that extracts as thousands of single-character
lines, or a near-empty extraction. The scanned-PDF detector does not catch these,
so a noisy conversion was previously marked ``ok``. ``assess_quality`` flags such
output as ``low_quality`` so ingestion can route it to the human-review queue.
"""

from __future__ import annotations

# Fraction of non-empty lines that are <=2 chars above which we suspect
# watermark / fragmentation noise.
NOISE_RATIO_THRESHOLD = 0.40
# Minimum words we expect from a real document source.
MIN_WORDS = 500


def assess_quality(text: str) -> dict:
    """Return a quality report for converted Markdown.

    Keys: ``low_quality`` (bool), ``noise_ratio`` (float), ``word_count`` (int),
    ``short_line_count`` (int), ``reasons`` (list[str]).
    """
    lines = text.splitlines()
    nonempty = [ln for ln in lines if ln.strip()]
    word_count = len(text.split())
    reasons: list[str] = []

    if not nonempty:
        return {
            "low_quality": True,
            "noise_ratio": 1.0,
            "word_count": 0,
            "short_line_count": 0,
            "reasons": ["conversion produced no non-empty lines"],
        }

    short = sum(1 for ln in nonempty if len(ln.strip()) <= 2)
    noise_ratio = short / len(nonempty)

    low_quality = False
    if noise_ratio > NOISE_RATIO_THRESHOLD:
        low_quality = True
        reasons.append(
            f"{noise_ratio:.0%} of non-empty lines are <=2 chars "
            f"({short}/{len(nonempty)}) — likely watermark or fragmentation noise"
        )
    if word_count < MIN_WORDS:
        low_quality = True
        reasons.append(f"only {word_count} words extracted (expected >= {MIN_WORDS})")

    return {
        "low_quality": low_quality,
        "noise_ratio": round(noise_ratio, 3),
        "word_count": word_count,
        "short_line_count": short,
        "reasons": reasons,
    }
