"""Tests for the verbatim-quotation scan.

The rights policy contract is word-based — 40+ consecutive source words in output require
manual review. The scan slides a word window over the presentation-stripped body, so detection is
quote-style-independent: unquoted prose, straight/smart quotes, and block-quotes are all caught,
and a 40-word lift of short words (negotiation scripts, dialogue, aphorisms) is never missed by a
character floor.
"""

import json

from tools.subagent_factory.quote_scan import (
    MIN_WORDS_FOR_CONCERN,
    quote_scan,
    quote_scan_report,
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


def test_short_word_verbatim_quote_is_flagged(tmp_path):
    # A 40-word verbatim quote of short words is < 200 chars — the old 200-char
    # regex floor missed it entirely. The window scan has no char floor, so it must be caught.
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
    assert any("Verbatim run" in f["issue"] for f in findings)


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
    assert any("Verbatim run" in f["issue"] for f in findings)


def test_multiline_block_quote_is_coalesced_and_flagged(tmp_path):
    # Markdown wraps a long quoted passage across several `> ` lines. Each line is
    # under the 40-word threshold, but together they reproduce a 40+-word verbatim
    # passage. A per-line check never sums them; the run must be coalesced so the
    # whole lift is caught. Regression for the per-line block-quote false negative.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 4)
    words = quote.split()
    third = len(words) // 3
    line_a = " ".join(words[:third])
    line_b = " ".join(words[third : 2 * third])
    line_c = " ".join(words[2 * third :])
    assert all(len(seg.split()) < MIN_WORDS_FOR_CONCERN for seg in (line_a, line_b, line_c)), (
        "test premise: no single block-quote line reaches the threshold"
    )

    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        f"As the book puts it:\n\n> {line_a}\n> {line_b}\n> {line_c}\n\nend.\n",
        encoding="utf-8",
    )

    findings = quote_scan(base)
    assert findings, "multi-line verbatim block quote must be flagged"
    assert any("Verbatim run" in f["issue"] for f in findings)


def test_short_block_quote_run_not_flagged(tmp_path):
    # A coalesced block-quote run that stays under 40 words must not be flagged.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN - 5)
    words = quote.split()
    half = len(words) // 2
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "ok.md").write_text(
        f"> {' '.join(words[:half])}\n> {' '.join(words[half:])}\n",
        encoding="utf-8",
    )
    assert quote_scan(base) == []


def test_unquoted_verbatim_prose_is_flagged(tmp_path):
    # The plagiarism the rights policy exists to catch: a generated body that reproduces a
    # 40+-word source run with NO quote marks at all. The old quote-punctuation-gated scan
    # missed this entirely. The window check is quote-style-independent.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 5)
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        f"Here is some framing and then {quote} and then a closing sentence.\n",
        encoding="utf-8",
    )
    findings = quote_scan(base)
    assert findings, "unquoted verbatim prose must be flagged (rights gate)"


def test_smart_quoted_verbatim_is_flagged(tmp_path):
    # PDF→markdown converters emit curly/smart quotes. A verbatim lift wrapped in “ ” must
    # still be caught — quote glyph must not be an evasion vector.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 2)
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        f"The book says: “{quote}” here.\n", encoding="utf-8"
    )
    findings = quote_scan(base)
    assert findings, "smart-quoted verbatim quote must be flagged (rights gate)"


def test_inline_markdown_markup_in_output_does_not_evade(tmp_path):
    # A verbatim lift where the output italicizes/code-spans one word inside the run must still be
    # caught: the source side and output side must normalize markdown markup symmetrically, or
    # `*word*` in the output breaks the substring match against a source that has plain `word`.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 5)
    words = quote.split()
    words[len(words) // 2] = f"*{words[len(words) // 2]}*"  # emphasis on one mid-run word
    leak = "Here it is: " + " ".join(words) + " done.\n"
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(leak, encoding="utf-8")
    findings = quote_scan(base)
    assert findings, "inline markdown markup in the output must not evade the verbatim scan"


def test_inline_html_tag_in_output_does_not_evade(tmp_path):
    # `<b>word</b>` renders identically to `*word*` but the markup chars `<`/`>`/`/` are not in the
    # glyph set — an inline HTML tag inside a verbatim run must not break the match.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 5)
    words = quote.split()
    mid = len(words) // 2
    words[mid] = f"<b>{words[mid]}</b>"
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        "Here: " + " ".join(words) + " done.\n", encoding="utf-8"
    )
    assert quote_scan(base), "inline HTML tag in the output must not evade the verbatim scan"


def test_backslash_escape_in_output_does_not_evade(tmp_path):
    # A markdown backslash escape (`word\`) inside a verbatim run must not break the match.
    quote = _short_word_quote(MIN_WORDS_FOR_CONCERN + 5)
    words = quote.split()
    words[len(words) // 2] = words[len(words) // 2] + "\\"
    base, _ = _build_package(tmp_path, source_text=f"intro {quote} outro")
    (base / "references").mkdir()
    (base / "references" / "leak.md").write_text(
        "Here: " + " ".join(words) + " done.\n", encoding="utf-8"
    )
    assert quote_scan(base), "backslash escape in the output must not evade the verbatim scan"


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


# ── A: map-reduce cache fallback + rights-not-verified visibility ──────────────
# The real corpus withholds sources/markdown/ (distillation-only), so quote_scan was vacuous — []
# on every package because there was nothing to compare against. These pin the cache-level fix.
def _build_map_reduce_package(tmp_path, source_text, rights="distillation-only"):
    """A package with NO sources/markdown/ (withheld) but a manifest ``sha256`` + a synthetic cache
    module at ``<cache>/<sha>/source.md`` — the real-corpus shape. Returns (base, source_id, cache_root)."""
    base = tmp_path / "pkg"
    (base / "sources" / "metadata").mkdir(parents=True)
    source_id, sha = "src-1", "a" * 64
    meta_rel = f"sources/metadata/{source_id}.metadata.json"
    (base / meta_rel).write_text(
        json.dumps({"source_id": source_id, "rights_status": rights, "sha256": sha}),
        encoding="utf-8",
    )
    (base / "source-pack.manifest.yaml").write_text(
        "schema_version: source-pack-manifest-v1\nsources:\n"
        f"  - source_id: {source_id}\n    sha256: {sha}\n    metadata_path: {meta_rel}\n",
        encoding="utf-8",
    )
    cache_root = tmp_path / "cache"
    mod = cache_root / sha
    mod.mkdir(parents=True)
    (mod / "source.md").write_text(source_text, encoding="utf-8")
    return base, source_id, cache_root


def test_cache_fallback_catches_verbatim_quote(tmp_path):
    source = _short_word_quote(MIN_WORDS_FOR_CONCERN + 10)  # 50 short words
    base, _sid, cache_root = _build_map_reduce_package(tmp_path, f"chapter text {source} end")
    lift = " ".join(source.split()[:MIN_WORDS_FOR_CONCERN])  # 40-word verbatim lift into the output
    (base / "references").mkdir()
    (base / "references" / "skill.md").write_text(f"Intro. {lift} Outro.\n", encoding="utf-8")
    # sources/markdown/ is absent → the scan must fall back to the cache module and catch the lift.
    assert quote_scan(base, cache_root=cache_root)


def test_report_scanned_true_via_cache(tmp_path):
    base, _sid, cache_root = _build_map_reduce_package(
        tmp_path, "some restricted source prose here"
    )
    r = quote_scan_report(base, cache_root=cache_root)
    assert r["restricted"] == 1 and r["scanned"] is True


def test_report_scanned_false_when_no_source_available(tmp_path):
    # Restricted source, but no sources/markdown/ AND no cache module (cold cache) → the gate COULD NOT
    # run. This is "rights not verified", which the validate gate surfaces instead of a silent pass.
    base, _sid, _cache = _build_map_reduce_package(tmp_path, "src text")
    r = quote_scan_report(base, cache_root=tmp_path / "empty-cache")
    assert r["restricted"] == 1 and r["scanned"] is False


def test_check_quote_scan_warns_rights_not_verified(tmp_path):
    import tools.subagent_factory.validate_generated_package as vgp

    base, _sid, _cache = _build_map_reduce_package(tmp_path, "src text")
    warns: list[tuple[str, str]] = []
    oks: list[tuple[str, str]] = []
    # default cache root has no module for the fake sha → could-not-scan → WARN, not a silent OK.
    vgp._check_quote_scan(
        base, warn=lambda c, m: warns.append((c, m)), ok=lambda c, m: oks.append((c, m))
    )
    assert oks == [] and any("rights NOT verified" in m for _c, m in warns)
