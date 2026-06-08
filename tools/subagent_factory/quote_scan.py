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

# Match "quoted text" only in markdown prose lines (not YAML string syntax)
INLINE_QUOTE_RE = re.compile(r'"([^"\n]{200,})"')
BLOCKQUOTE_RE = re.compile(r"^> ", re.MULTILINE)

# Directories that ARE the source material — never scan
_SOURCE_DIRS = {"sources/original", "sources/markdown", "sources/snapshots"}

# Files that contain synthesised data fields, not quotation
_SKIP_FILENAMES = {
    "source-pack.manifest.yaml",
    "interrogation-records.yaml",
    "profile.yaml",
}


def quote_scan(subagent_dir: str | Path) -> list[dict]:
    """
    Scan generated artifacts for potential verbatim quotation.

    Returns list of findings: {file, line, issue, excerpt}
    Empty list = no concerns.
    """
    base = Path(subagent_dir)
    findings = []

    restricted_sources = _load_restricted_sources(base)

    # Scan markdown prose files
    for md_file in base.rglob("*.md"):
        if _is_source_material(md_file, base):
            continue
        _scan_markdown_prose(md_file, restricted_sources, findings)

    # Scan only skill and reference markdown (not YAML data files)
    # YAML files are NOT scanned — their string values are synthesised, not quoted

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


def _scan_markdown_prose(path: Path, restricted_sources: set, findings: list) -> None:
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
        # Long inline quotes in prose
        for m in INLINE_QUOTE_RE.finditer(line):
            words = len(m.group(1).split())
            if words >= MIN_WORDS_FOR_CONCERN:
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Long inline quote ({words} words) in prose — verify not verbatim from source",
                    "excerpt": m.group(1)[:120] + ("..." if len(m.group(1)) > 120 else ""),
                })

        # Block quotes (> lines) — only flag if long AND in a non-source file
        if line.startswith("> "):
            block_words = len(line[2:].split())
            if block_words >= MIN_WORDS_FOR_CONCERN:
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Long block-quote ({block_words} words) — verify not verbatim from source",
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
