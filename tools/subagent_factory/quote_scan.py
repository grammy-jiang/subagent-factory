"""
Scan generated artifacts for potential verbatim quotation from restricted sources.

What this scan looks for:
  Any run of MIN_WORDS_FOR_CONCERN+ consecutive words in a generated markdown BODY that
  appears verbatim in a restricted source — independent of whether it is quoted, smart-
  quoted, block-quoted, or unquoted prose. Verbatim copying is the rights-policy concern
  (.claude/rules/rights-and-quotation-policy.md: "40+ consecutive source words"); the quote
  glyph is irrelevant to whether text was lifted, so the gate must not depend on it.

What this scan does NOT flag:
  - sources/markdown/ and sources/original/ — these ARE the source material
  - YAML string values (frontmatter, multi-line > blocks) — Claude-synthesised text,
    not lifted verbatim from the source
  - interrogation records — synthesised answers, not quotation
  - Profile body fields — should be paraphrased; covered by rights policy separately

Target files: adapter body prose, skill SKILL.md files, reference files, provenance
ledger prose sections. NOT YAML key-value data.
"""

import html
import re
import sys
from pathlib import Path

from tools.subagent_factory.source_text import (
    contains_span,
    load_restricted_source_ids,
    load_source_texts,
    normalize_ws,
)

MIN_WORDS_FOR_CONCERN = 40

# Cap how far the matched run is extended for REPORTING. The policy only needs ">= 40 verbatim
# words"; the exact length is cosmetic, so we stop extending here to bound the greedy walk (a body
# that is a near-copy of a large source would otherwise extend one word at a time across the whole
# document, an O(n^2) join+substring blowup).
_MAX_REPORT_RUN = 200

# Directories that ARE the source material — never scan
# markdown-raw is the redactor's pristine pre-redaction copy (injection quarantine) — source
# material, excluded from the quote gate like the others. Listed explicitly now that the match is
# segment-aware (it no longer rides on "sources/markdown" as a prefix).
_SOURCE_DIRS = {"sources/original", "sources/markdown", "sources/markdown-raw", "sources/snapshots"}

# Block-quote line marker, stripped so a `>`-fenced lift is detected like bare prose.
_BLOCKQUOTE_MARKER = re.compile(r"(?m)^\s{0,3}>\s?")
# Inline HTML tag, e.g. <b> </b> <em> <a href=...>. Removed WHOLE (tag name included) so an
# emphasis tag inside a run leaves no stray letters that would themselves break the match.
_INLINE_HTML = re.compile(r"</?[a-zA-Z][^>]*>")
# Quote glyphs + markdown inline-markup characters that wrap/decorate prose without being part of
# the words. Mapped to spaces so a verbatim run is matched whether the output (or source) quotes
# it, italicizes a word (``*word*``), code-spans it (`` `word` ``), or links it (``[t](u)``).
_MARKUP_CHARS = "\"'“”‘’«»*_`~#|[]()"
_MARKUP = str.maketrans({c: " " for c in _MARKUP_CHARS})


def _normalize_for_match(text: str) -> str:
    """Canonical form for verbatim comparison, applied IDENTICALLY to the source and the output.

    Decode HTML entities, drop block-quote markers, strip inline HTML tags, drop markdown backslash
    escapes, drop quote/markdown-markup glyphs, then collapse whitespace+case (normalize_ws). The
    invariant is SYMMETRY: whatever transform the output gets, the source gets the same one — any
    divergence is a verbatim-lift evasion vector, because all of these are markup that renders away
    while the words underneath are identical (``*word*``, ``<b>word</b>``, ``word\\``, ``&amp;``).
    Markdown link text survives (only the bracket/paren glyphs are dropped), so a linked verbatim
    phrase still matches.
    """
    text = html.unescape(text)
    text = _BLOCKQUOTE_MARKER.sub("", text)
    text = _INLINE_HTML.sub(" ", text)
    text = text.replace("\\", "")
    return normalize_ws(text.translate(_MARKUP))


def quote_scan(subagent_dir: str | Path) -> list[dict]:
    """
    Scan generated artifacts for potential verbatim quotation.

    Returns list of findings: {file, line, issue, excerpt}
    Empty list = no concerns.
    """
    base = Path(subagent_dir)
    findings: list[dict] = []

    restricted_sources = load_restricted_source_ids(base)
    # Re-normalize the source side through the SAME _normalize_for_match the output side uses, so
    # the substring comparison is symmetric (load_source_texts only does normalize_ws).
    source_texts = {
        sid: _normalize_for_match(txt)
        for sid, txt in load_source_texts(base, restricted_sources).items()
    }

    # Scan markdown prose files (not YAML — those contain synthesised fields)
    for md_file in base.rglob("*.md"):
        if _is_source_material(md_file, base):
            continue
        _scan_markdown_prose(md_file, source_texts, findings)

    return findings


def _is_source_material(path: Path, base: Path) -> bool:
    rel = str(path.relative_to(base)).replace("\\", "/")
    for src_dir in _SOURCE_DIRS:
        # Segment-aware: only the exact dir and its real children — a colliding sibling like
        # `sources/markdownX/` must NOT be excluded (that would let it evade the verbatim-quote gate).
        if rel == src_dir or rel.startswith(src_dir + "/"):
            return True
    return False


def _longest_verbatim_run(words: list[str], source_texts: dict) -> int:
    """Length (in words) of the longest run in ``words`` that appears verbatim in a source.

    Slides a MIN_WORDS_FOR_CONCERN-word window across the body and tests each window against the
    sources (already whitespace-normalized). Returns the matched window length (>= the threshold)
    on the first hit, else 0. This enforces the policy directly — "N CONSECUTIVE source words" —
    rather than probing a fixed-length head, so it has neither the head-only false negative nor the
    coincidental-head false positive of the old 15-word probe.
    """
    n = MIN_WORDS_FOR_CONCERN
    if len(words) < n:
        return 0
    for i in range(len(words) - n + 1):
        probe = " ".join(words[i : i + n])
        if contains_span(probe, source_texts):
            # Found a 40-word run; extend greedily to report the true run length, but stop at
            # _MAX_REPORT_RUN so a near-full-source copy can't drive an O(n^2) extension walk.
            j = i + n
            cap = min(len(words), i + _MAX_REPORT_RUN)
            while j < cap and contains_span(" ".join(words[i : j + 1]), source_texts):
                j += 1
            return j - i
    return 0


def _scan_markdown_prose(path: Path, source_texts: dict, findings: list) -> None:
    """Flag any MIN_WORDS_FOR_CONCERN+ word run that appears verbatim in a restricted source.

    The whole body is run through _normalize_for_match (the SAME transform applied to the source
    side) — YAML front matter removed, entities decoded, block-quote markers + quote/markdown-markup
    glyphs dropped, whitespace+case collapsed — then scanned with a sliding word window. This is
    quote-style- and markup-independent: an unquoted, straight/smart-quoted, block-quoted, or
    emphasized/linked lift are all caught. The finding is attributed to the run's starting line.
    """
    if not source_texts:
        return
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return

    body = _strip_front_matter(text)
    words = _normalize_for_match(body).split()
    run = _longest_verbatim_run(words, source_texts)
    if run < MIN_WORDS_FOR_CONCERN:
        return

    # Locate the matched run's starting line for attribution + excerpt.
    line_no, excerpt = _locate_run(body, words, run)
    findings.append(
        {
            "file": str(path),
            "line": line_no,
            "issue": f"Verbatim run ({run} words) appears in a restricted source — verify rights",
            "excerpt": excerpt[:120] + ("..." if len(excerpt) > 120 else ""),
        }
    )


def _locate_run(body: str, words: list[str], run: int) -> tuple[int, str]:
    """Best-effort (line_number, excerpt) for the matched verbatim run.

    The window words came from a presentation-stripped, whitespace-collapsed body, so an exact
    offset back into the raw text isn't generally recoverable. Attribute to the first body line
    that contains the run's opening word sequence (normalized), falling back to line 1.
    """
    head = " ".join(words[: min(run, 8)])
    for i, line in enumerate(body.splitlines(), 1):
        norm_line = _normalize_for_match(line)
        if head and head in norm_line:
            return i, normalize_ws(line.strip())
    return 1, " ".join(words[:20])


def _strip_front_matter(text: str) -> str:
    # Match a CLOSING fence that is `---` alone on its line (optionally CRLF), so a `---` inside a
    # value or a `----` horizontal rule doesn't truncate the strip early and drop real body prose.
    if re.match(r"﻿?\s*---[ \t]*\r?\n", text):
        m = re.search(r"\r?\n---[ \t]*(?:\r?\n|$)", text)
        if m:
            return text[m.end() :]
    return text


if __name__ == "__main__":
    findings = quote_scan(sys.argv[1])
    for f in findings:
        print(f"WARN {f['file']}:{f['line']}: {f['issue']}")
        print(f"     {f['excerpt']}")
    if not findings:
        print("quote-scan PASS — no potential verbatim quotation found")
    sys.exit(0)
