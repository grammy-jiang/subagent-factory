"""Tests for the verbatim-quotation scan.

Regression focus: the inline-quote pre-filter regex must admit the *shortest
possible* MIN_WORDS_FOR_CONCERN-word quoted span, so a real 40-word verbatim quote
made of short words (negotiation scripts, dialogue, aphorisms) is not silently
missed. The rights policy contract is word-based — 40+ consecutive source words —
and the regex character floor must never raise that bar.
"""

import json

from tools.subagent_factory.quote_scan import (
    _MIN_QUOTE_CHARS,
    MIN_WORDS_FOR_CONCERN,
    quote_scan,
)


def _build_package(tmp_path, source_text: str, rights: str = "distillation-only"):
    """Create a minimal package: manifest + metadata + source markdown.

    Returns the package base dir; the caller writes the artifact(s) to scan.
    """
    base = tmp_path / "pkg"
    (base / "sources" / "markdown").mkdir(parents=True)
    (base / "sources" / "metadata").mkdir(parents=True)

    source_id = "src-1"
    (base / "sources" / "markdown" / f"{source_id}.md").write_text(source_text, encoding="utf-8")

    meta = {
        "schema_version": "source-metadata-v1",
        "source_id": source_id,
        "rights_status": rights,
    }
    meta_rel = f"sources/metadata/{source_id}.metadata.json"
    (base / meta_rel).write_text(json.dumps(meta), encoding="utf-8")

    manifest = (
        "schema_version: source-pack-manifest-v1\n"
        "sources:\n"
        f"  - source_id: {source_id}\n"
        f"    metadata_path: {meta_rel}\n"
    )
    (base / "source-pack.manifest.yaml").write_text(manifest, encoding="utf-8")
    return base, source_id


def _short_word_quote(n_words: int) -> str:
    """An n-word string of short words, < 200 chars for n around 40-46."""
    base = "it feels like you do not want to lose this deal and that is right".split()
    return " ".join((base * 6)[:n_words])


def test_char_floor_is_derived_from_word_policy():
    # The floor must be the minimum chars a MIN_WORDS_FOR_CONCERN-word string can
    # occupy: N single-char words + (N-1) single spaces = 2N - 1.
    assert _MIN_QUOTE_CHARS == 2 * MIN_WORDS_FOR_CONCERN - 1


def test_short_word_verbatim_quote_is_flagged(tmp_path):
    # A 40-word verbatim quote of short words is < 200 chars — the old 200-char
    # regex floor missed it entirely. It must now be caught.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN)
    assert len(quote) < 200, "test premise: this quote is under the old 200-char floor"
    assert len(quote.split()) == MIN_WORDS_FOR_CONCERN

    base, _ = _build_package(tmp_path, source_text=f"prose {quote} more prose")
    # A generated artifact (not under sources/) that reproduces the quote verbatim.
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        f'The advisor said: "{quote}" to the counterpart.\n', encoding="utf-8"
    )

    findings = quote_scan(base)
    assert findings, "40-word short-word verbatim quote must be flagged"
    assert any("Verbatim inline quote" in f["issue"] for f in findings)


def test_under_threshold_quote_not_flagged(tmp_path):
    # A 39-word verbatim quote is below the policy threshold — no finding.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN - 1)
    base, _ = _build_package(tmp_path, source_text=f"prose {quote} more prose")
    (base / "references").mkdir()
    (base / "references" / "ok.md").write_text(
        f'The advisor said: "{quote}" to the counterpart.\n', encoding="utf-8"
    )
    assert quote_scan(base) == []


def test_long_quote_not_in_source_not_flagged(tmp_path):
    # A 50-word quote that does NOT appear in the source is synthesised, not lifted.
    source = "the source talks about negotiation tactics in general terms only"
    novel = " ".join(f"word{i}" for i in range(50))
    base, _ = _build_package(tmp_path, source_text=source)
    (base / "references").mkdir()
    (base / "references" / "novel.md").write_text(
        f'A paraphrase: "{novel}" follows.\n', encoding="utf-8"
    )
    assert quote_scan(base) == []


def test_source_material_is_never_scanned(tmp_path):
    # The source markdown itself trivially contains the verbatim text; it must
    # never be reported (it IS the source).
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 3)
    base, _ = _build_package(tmp_path, source_text=f'"{quote}"')
    assert quote_scan(base) == []


def test_verbatim_quote_flagged_despite_source_whitespace(tmp_path):
    # PDF-to-markdown conversion (markitdown) routinely emits double spaces between
    # words and wraps lines, so the source text's whitespace differs from the
    # single-spaced output. The verbatim probe is single-space normalized; the
    # source side must be normalized too or a real lift slips through. Regression
    # for the source-side normalization gap in _load_source_texts.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN)
    # Same words as `quote`, but with double spaces and a line break injected —
    # exactly what a converted PDF looks like.
    noisy_source = quote.replace(" ", "  ").replace("  ", " \n ", 1)
    base, _ = _build_package(tmp_path, source_text=f"prose {noisy_source} more prose")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        f'The advisor said: "{quote}" verbatim.\n', encoding="utf-8"
    )

    findings = quote_scan(base)
    assert findings, "verbatim quote must be flagged even when source whitespace differs"
    assert any("Verbatim inline quote" in f["issue"] for f in findings)


def test_open_rights_source_not_loaded_for_matching(tmp_path):
    # Only restricted/distillation-only sources are loaded for verbatim matching;
    # an `open`-licensed source's text is quotable, so a long quote is not flagged.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 2)
    base, _ = _build_package(tmp_path, source_text=f"prose {quote} more", rights="open")
    (base / "references").mkdir()
    (base / "references" / "quoted.md").write_text(
        f'As the open source states: "{quote}".\n', encoding="utf-8"
    )
    assert quote_scan(base) == []
