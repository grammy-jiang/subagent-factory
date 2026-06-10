"""
Scan generated artifacts for potential verbatim quotation from restricted sources.

What this scan looks for:
  Long inline quoted passages ("...40+ words...") in markdown BODY prose.
  Long block-quotes (> ...) in markdown BODY prose.

What this scan does NOT flag:
  - sources/markdown/ and sources/original/ — these ARE the source material
  - YAML string values (frontmatter, multi-line > blocks) — Claude-synthesised text,
    not lifted verbatim from the source
  - interrogation records — synthesised answers, not quotation
  - Profile body fields — should be paraphrased; covered by rights policy separately

Target files: adapter body prose, skill SKILL.md files, reference files, provenance
ledger prose sections. NOT YAML key-value data.
"""

import re
import sys
from pathlib import Path

from tools.subagent_factory.source_text import (
    contains_span,
    load_restricted_source_ids,
    load_source_texts,
)

MIN_WORDS_FOR_CONCERN = 40

# The rights policy contract (.claude/rules/rights-and-quotation-policy.md) is
# word-based: "Any finding of 40+ consecutive source words in output requires
# manual review." The inline-quote regex below is only a cheap pre-filter — the
# authoritative word count (>= MIN_WORDS_FOR_CONCERN) and source-match are applied
# afterwards in _scan_markdown_prose / _is_verbatim. Its character floor must
# therefore admit the *shortest possible* MIN_WORDS_FOR_CONCERN-word string, or a
# real 40-word verbatim quote of short words slips through undetected. The shortest
# such string is N single-character words joined by N-1 single spaces = 2*N - 1
# chars. A higher fixed floor (the previous hard-coded 200) silently raised the
# effective threshold to ~46+ short words — a false negative on prose sources made
# of short, highly-quotable phrases (negotiation scripts, dialogue, aphorisms).
# Deriving the floor from the constant keeps regex and policy from drifting apart.
_MIN_QUOTE_CHARS = 2 * MIN_WORDS_FOR_CONCERN - 1

# Match "quoted text" only in markdown prose lines (not YAML string syntax).
INLINE_QUOTE_RE = re.compile(r'"([^"\n]{' + str(_MIN_QUOTE_CHARS) + r',})"')

# Directories that ARE the source material — never scan
_SOURCE_DIRS = {"sources/original", "sources/markdown", "sources/snapshots"}


def quote_scan(subagent_dir: str | Path) -> list[dict]:
    """
    Scan generated artifacts for potential verbatim quotation.

    Returns list of findings: {file, line, issue, excerpt}
    Empty list = no concerns.
    """
    base = Path(subagent_dir)
    findings: list[dict] = []

    restricted_sources = load_restricted_source_ids(base)
    source_texts = load_source_texts(base, restricted_sources)

    # Scan markdown prose files (not YAML — those contain synthesised fields)
    for md_file in base.rglob("*.md"):
        if _is_source_material(md_file, base):
            continue
        _scan_markdown_prose(md_file, source_texts, findings)

    return findings


def _is_source_material(path: Path, base: Path) -> bool:
    rel = str(path.relative_to(base)).replace("\\", "/")
    for src_dir in _SOURCE_DIRS:
        if rel.startswith(src_dir):
            return True
    return False


def _is_verbatim(text: str, source_texts: dict) -> bool:
    """Return True only if the first 15 words of text appear in a source."""
    words = text.lower().split()
    if len(words) < MIN_WORDS_FOR_CONCERN:
        return False
    probe = " ".join(words[:15])
    return contains_span(probe, source_texts)


def _scan_markdown_prose(path: Path, source_texts: dict, findings: list) -> None:
    """
    Scan markdown prose for long inline quoted strings and long block-quotes.
    Skip YAML frontmatter (between --- delimiters at top of file).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return

    # Strip YAML front matter before scanning
    body = _strip_front_matter(text)
    lines = body.splitlines()

    # Consecutive ``>`` lines form ONE logical block quote. Markdown wraps a long
    # quoted passage across many short lines, so a single 40+-word verbatim lift
    # routinely lands as several sub-40-word ``> `` lines — a per-line check never
    # sums them and the rights gate misses the whole passage. Coalesce the run and
    # test the joined content; the finding is attributed to the block's first line.
    block_lines: list[str] = []
    block_start = 0

    def _flush_block() -> None:
        if not block_lines:
            return
        content = " ".join(block_lines).strip()
        block_words = len(content.split())
        if block_words >= MIN_WORDS_FOR_CONCERN and _is_verbatim(content, source_texts):
            findings.append(
                {
                    "file": str(path),
                    "line": block_start,
                    "issue": f"Verbatim block-quote ({block_words} words) — verify rights",
                    "excerpt": ("> " + content)[:120],
                }
            )

    for line_num, line in enumerate(lines, 1):
        # Long inline quotes in prose — only flag if text actually appears in source
        for m in INLINE_QUOTE_RE.finditer(line):
            words = len(m.group(1).split())
            if words >= MIN_WORDS_FOR_CONCERN and _is_verbatim(m.group(1), source_texts):
                findings.append(
                    {
                        "file": str(path),
                        "line": line_num,
                        "issue": f"Verbatim inline quote ({words} words) — verify rights",
                        "excerpt": m.group(1)[:120] + ("..." if len(m.group(1)) > 120 else ""),
                    }
                )

        # Block quotes — accumulate the run, then test the joined passage on flush.
        if line.startswith(">"):
            if not block_lines:
                block_start = line_num
            block_lines.append(line[1:].lstrip())
        else:
            _flush_block()
            block_lines = []

    _flush_block()


def _strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


if __name__ == "__main__":
    findings = quote_scan(sys.argv[1])
    for f in findings:
        print(f"WARN {f['file']}:{f['line']}: {f['issue']}")
        print(f"     {f['excerpt']}")
    if not findings:
        print("quote-scan PASS — no potential verbatim quotation found")
    sys.exit(0)
