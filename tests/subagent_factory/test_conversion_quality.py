"""Tests for conversion quality assessment."""

from tools.subagent_factory.conversion_quality import assess_quality


def test_clean_text_is_ok():
    text = " ".join(["word"] * 600) + "\n\nA real paragraph with genuine content here.\n"
    q = assess_quality(text)
    assert q["low_quality"] is False
    assert q["noise_ratio"] < 0.4
    assert q["word_count"] >= 600


def test_watermark_noise_is_flagged():
    # Simulate a vertical spine watermark: thousands of single-character lines.
    noise = "\n".join(list("ConcurrentProgrammingInJava" * 50))
    text = noise + "\n" + " ".join(["word"] * 600)
    q = assess_quality(text)
    assert q["low_quality"] is True
    assert q["noise_ratio"] > 0.4
    assert any("watermark" in r or "<=2 chars" in r for r in q["reasons"])


def test_short_text_is_flagged():
    q = assess_quality("only a handful of words here")
    assert q["low_quality"] is True
    assert any("words extracted" in r for r in q["reasons"])


def test_empty_text_is_flagged():
    q = assess_quality("   \n   \n\t\n")
    assert q["low_quality"] is True
    assert q["word_count"] == 0
    assert q["reasons"]
