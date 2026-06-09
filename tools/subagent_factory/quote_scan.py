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

import json
import re
import sys
from pathlib import Path

import yaml

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
    findings = []

    restricted_sources = _load_restricted_sources(base)
    source_texts = _load_source_texts(base, restricted_sources)

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


def _load_restricted_sources(base: Path) -> set[str]:
    restricted = set()
    manifest_path = base / "source-pack.manifest.yaml"
    if not manifest_path.exists():
        return restricted
    try:
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f) or {}
        for source in manifest.get("sources", []):
            meta_path = base / source.get("metadata_path", "")
            if not meta_path.exists():
                continue
            with open(meta_path) as f:
                meta = json.load(f)
            rights = meta.get("rights_status", "")
            if "restricted" in rights.lower() or "distillation-only" in rights.lower():
                restricted.add(source.get("source_id"))
    except Exception:
        pass
    return restricted


def _load_source_texts(base: Path, restricted_sources: set) -> dict[str, str]:
    """Load lowercased text of restricted sources for verbatim-match checking."""
    texts = {}
    markdown_dir = base / "sources" / "markdown"
    if not markdown_dir.exists():
        return texts
    for source_id in restricted_sources:
        md_path = markdown_dir / f"{source_id}.md"
        if md_path.exists():
            try:
                texts[source_id] = md_path.read_text(encoding="utf-8").lower()
            except Exception:
                pass
    return texts


def _is_verbatim(text: str, source_texts: dict) -> bool:
    """Return True only if the first 15 words of text appear in a source."""
    words = text.lower().split()
    if len(words) < MIN_WORDS_FOR_CONCERN:
        return False
    probe = " ".join(words[:15])
    return any(probe in src for src in source_texts.values())


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

    for line_num, line in enumerate(lines, 1):
        # Long inline quotes in prose — only flag if text actually appears in source
        for m in INLINE_QUOTE_RE.finditer(line):
            words = len(m.group(1).split())
            if words >= MIN_WORDS_FOR_CONCERN and _is_verbatim(m.group(1), source_texts):
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Verbatim inline quote ({words} words) — verify rights",
                    "excerpt": m.group(1)[:120] + ("..." if len(m.group(1)) > 120 else ""),
                })

        # Block quotes — only flag if long AND text appears in source
        if line.startswith("> "):
            content = line[2:]
            block_words = len(content.split())
            if block_words >= MIN_WORDS_FOR_CONCERN and _is_verbatim(content, source_texts):
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Verbatim block-quote ({block_words} words) — verify rights",
                    "excerpt": line[:120],
                })


def _strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


if __name__ == "__main__":
    findings = quote_scan(sys.argv[1])
    for f in findings:
        print(f"WARN {f['file']}:{f['line']}: {f['issue']}")
        print(f"     {f['excerpt']}")
    if not findings:
        print("quote-scan PASS — no potential verbatim quotation found")
    sys.exit(0)
