"""
Scan generated artifacts for potential verbatim quotation from restricted sources.

A restricted source has rights_status of 'distillation-only' or 'proprietary/restricted'.
The scan is heuristic: long quoted passages (>40 words in quotes) trigger warnings.
"""

import json
import re
import sys
from pathlib import Path

import yaml


QUOTE_PATTERN = re.compile(r'"([^"]{200,})"', re.DOTALL)
BLOCKQUOTE_PATTERN = re.compile(r"^> .{100,}", re.MULTILINE)
MIN_WORDS_FOR_CONCERN = 40


def quote_scan(subagent_dir: str | Path) -> list[dict]:
    """
    Scan subagent package for potential rights violations.

    Returns list of findings: {file, line, issue, excerpt}
    """
    base = Path(subagent_dir)
    findings = []

    # Load restricted source IDs from manifest
    manifest_path = base / "source-pack.manifest.yaml"
    restricted_sources = _load_restricted_sources(base, manifest_path)

    # Scan Markdown files
    for md_file in base.rglob("*.md"):
        if "sources/original" in str(md_file):
            continue
        _scan_markdown(md_file, restricted_sources, findings)

    # Scan YAML files
    for yaml_file in base.rglob("*.yaml"):
        if "source-pack.manifest" in yaml_file.name:
            continue
        _scan_text_file(yaml_file, restricted_sources, findings)

    return findings


def _load_restricted_sources(base: Path, manifest_path: Path) -> set[str]:
    restricted = set()
    if not manifest_path.exists():
        return restricted

    try:
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f) or {}
    except Exception:
        return restricted

    for source in manifest.get("sources", []):
        source_id = source.get("source_id")
        meta_path = base / source.get("metadata_path", "")
        if not meta_path.exists():
            continue
        try:
            with open(meta_path) as f:
                meta = json.load(f)
            rights = meta.get("rights_status", "")
            if "restricted" in rights.lower() or "distillation-only" in rights.lower():
                restricted.add(source_id)
        except Exception:
            pass

    return restricted


def _scan_markdown(path: Path, restricted_sources: set, findings: list) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return

    lines = text.splitlines()
    for line_num, line in enumerate(lines, 1):
        # Long inline quotes
        for m in QUOTE_PATTERN.finditer(line):
            words = len(m.group(1).split())
            if words >= MIN_WORDS_FOR_CONCERN:
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Possible verbatim quote ({words} words) — verify rights",
                    "excerpt": m.group(1)[:100] + "...",
                })
        # Block quotes
        if re.match(r"^> ", line):
            block_words = len(line[2:].split())
            if block_words >= MIN_WORDS_FOR_CONCERN:
                findings.append({
                    "file": str(path),
                    "line": line_num,
                    "issue": f"Block quote ({block_words} words) — verify rights",
                    "excerpt": line[:100],
                })


def _scan_text_file(path: Path, restricted_sources: set, findings: list) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return
    for m in QUOTE_PATTERN.finditer(text):
        words = len(m.group(1).split())
        if words >= MIN_WORDS_FOR_CONCERN:
            line_num = text[:m.start()].count("\n") + 1
            findings.append({
                "file": str(path),
                "line": line_num,
                "issue": f"Possible verbatim quote ({words} words) in YAML — verify rights",
                "excerpt": m.group(1)[:100] + "...",
            })


if __name__ == "__main__":
    findings = quote_scan(sys.argv[1])
    for f in findings:
        print(f"WARN {f['file']}:{f['line']}: {f['issue']}")
        print(f"     {f['excerpt']}")
    if not findings:
        print("quote-scan PASS — no potential verbatim quotation found")
    sys.exit(0)
