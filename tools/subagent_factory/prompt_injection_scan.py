"""Deterministic prompt-injection scan over ingested source markdown (Step 1).

Scans ``sources/markdown/*.md`` for indirect-prompt-injection (IPI) payloads, following
the research synthesis (``docs/Research/prompt-injection-defense/``):

- **Normalize before matching** — obfuscation is the primary evasion: strip zero-width
  characters, fold Unicode confusables, and re-scan base64 / ROT13 / reversed variants.
- **Presentation-layer sanitize** — reassemble DOM-fragmented spans (strip HTML tags) and
  flag CSS-hidden content before matching.
- **Canonical-phrase denylist** — the stable imperative-override / authority-spoof /
  fake-completion / delimiter-spoof / task-injection families that recur across every
  benchmark (BIPIA, InjecAgent, AgentDojo, ASB).
- **Scan-tail priority** — injection placed at the END of content has the highest attack
  success rate, so tail hits are raised in severity.

Findings are **advisory triage**, never a hard block: at a realistic ~225:1 benign:attack
base rate even a 1% false-positive rate floods legitimate content, and adaptive attacks
break detectors outright. ``validate_generated_package`` surfaces these as WARN; the
``source-safety-reviewer`` agent triages each flag (true instruction vs benign quote).
Source content is data, never instruction (``.claude/rules/untrusted-source-policy.md``).
"""

import base64
import codecs
import re
import sys
import unicodedata
from pathlib import Path

# ── Canonical denylist (case-insensitive) ────────────────────────────────────
_DENYLIST: list[tuple[str, re.Pattern[str]]] = [
    (
        "imperative-override",
        re.compile(
            r"ignore\s+(all\s+)?(the\s+)?(previous|prior|former|above)\s+instructions", re.I
        ),
    ),
    ("imperative-override", re.compile(r"disregard\s+(all\s+)?(previous|prior|the\s+above)", re.I)),
    ("authority-spoof", re.compile(r"###\s*(system|important\s+messages?)\b", re.I)),
    ("authority-spoof", re.compile(r"important!!!", re.I)),
    ("authority-spoof", re.compile(r"</?information>", re.I)),
    (
        "authority-spoof",
        re.compile(r"strictly\s+adhere\s+to\s+the\s+following\s+instruction", re.I),
    ),
    ("task-injection", re.compile(r"(^|\n)\s*todo:\s*\S", re.I)),
    ("fake-completion", re.compile(r"###\s*response:", re.I)),
    ("fake-completion", re.compile(r"<<sys>>", re.I)),
    ("fake-completion", re.compile(r"\btask\s+complete\b", re.I)),
    ("delimiter-spoof", re.compile(r"<\|im_(start|end)\|>", re.I)),
    ("delimiter-spoof", re.compile(r"</(data|system|user|assistant)>", re.I)),
    ("role-override", re.compile(r"\byou\s+are\s+now\b", re.I)),
]

# CSS / presentation-layer hiding tricks.
_CSS_HIDDEN = re.compile(
    r"(opacity\s*:\s*0(\.0+)?\b|font-size\s*:\s*0|display\s*:\s*none|visibility\s*:\s*hidden"
    r"|left\s*:\s*-?\d{4,}px|z-index\s*:\s*-\d+)",
    re.I,
)

# Zero-width / bidi-control codepoints used to obfuscate payloads. Written as hex
# escapes (not literals) so the source itself contains no bidi controls (bandit B613).
_ZERO_WIDTH = dict.fromkeys([0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x2060, 0xFEFF], None)

# Minimal Unicode-confusable fold (Cyrillic/Greek look-alikes → ASCII). NFKD handles
# many; this covers the common homoglyph-substitution attack letters NFKD leaves alone.
_CONFUSABLES = str.maketrans(
    {
        "а": "a",
        "е": "e",
        "о": "o",
        "р": "p",
        "с": "c",
        "х": "x",
        "у": "y",
        "і": "i",
        "ѕ": "s",
        "ԛ": "q",
        "ո": "n",
        "А": "A",
        "Е": "E",
        "О": "O",
        "Р": "P",
        "С": "C",
        "ο": "o",
        "α": "a",
        "ν": "v",
        "ρ": "p",
        "ϲ": "c",
    }
)

_HTML_TAG = re.compile(r"<[^>]+>")
_BASE64_TOKEN = re.compile(r"[A-Za-z0-9+/]{16,}={0,2}")
_TAIL_CHARS = 1000


def _strip_zero_width(text: str) -> str:
    return text.translate(_ZERO_WIDTH)


def _fold_confusables(text: str) -> str:
    return unicodedata.normalize("NFKD", text).translate(_CONFUSABLES)


def _strip_html_tags(text: str) -> str:
    """Reassemble DOM-fragmented payloads: ``<span>i</span><span>g</span>`` → ``ig``."""
    return _HTML_TAG.sub("", text)


def _base64_decoded(text: str) -> str:
    """Concatenate the decoded text of base64-looking tokens that decode to printable ASCII."""
    out: list[str] = []
    for m in _BASE64_TOKEN.finditer(text):
        tok = m.group(0)
        if len(tok) % 4:
            continue
        try:
            dec = base64.b64decode(tok, validate=True).decode("ascii")
        except (ValueError, UnicodeDecodeError):
            continue
        if dec.isprintable():
            out.append(dec)
    return " ".join(out)


def _denylist_hits(text: str) -> list[str]:
    return sorted({fam for fam, rx in _DENYLIST if rx.search(text)})


def _scan_file(path: Path, findings: list[dict]) -> None:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    name = str(path)
    folded = _fold_confusables(_strip_zero_width(raw))

    # 1. Line-level denylist on the folded text (gives line numbers + tail flag).
    lines = folded.splitlines()
    n = len(lines)
    for i, line in enumerate(lines, 1):
        for fam, rx in _DENYLIST:
            if rx.search(line):
                in_tail = i >= max(1, n - 5)  # last few lines ≈ document tail
                findings.append(
                    {
                        "file": name,
                        "line": i,
                        "family": fam,
                        "vector": "tail" if in_tail else "body",
                        "severity": "high" if in_tail else "medium",
                        "excerpt": line.strip()[:120],
                    }
                )

    # 2. Obfuscation variants (whole-doc; report at line 0 with the vector that revealed it).
    variants = {
        "detagged": _strip_html_tags(folded),
        "reversed": folded[::-1],
        "rot13": codecs.decode(folded, "rot13"),
        "base64": _base64_decoded(raw),
    }
    for vector, variant in variants.items():
        for fam in _denylist_hits(variant):
            findings.append(
                {
                    "file": name,
                    "line": 0,
                    "family": fam,
                    "vector": vector,
                    "severity": "high",
                    "excerpt": f"payload revealed after {vector} normalization",
                }
            )

    # 3. Presentation-layer hiding.
    for i, line in enumerate(raw.splitlines(), 1):
        if _CSS_HIDDEN.search(line):
            findings.append(
                {
                    "file": name,
                    "line": i,
                    "family": "css-hidden",
                    "vector": "css-hidden",
                    "severity": "high",
                    "excerpt": line.strip()[:120],
                }
            )

    # 4. Explicit scan-tail denylist sweep (last N chars), in case the tail is one long line.
    tail = folded[-_TAIL_CHARS:]
    if n <= 1:  # single-line docs never hit the line-tail heuristic above
        for fam in _denylist_hits(tail):
            findings.append(
                {
                    "file": name,
                    "line": 0,
                    "family": fam,
                    "vector": "tail",
                    "severity": "high",
                    "excerpt": tail.strip()[-120:],
                }
            )


def prompt_injection_scan(subagent_dir: str | Path) -> list[dict]:
    """Scan ingested source markdown for injection payloads.

    Returns advisory findings ``{file, line, family, vector, severity, excerpt}``.
    Empty list = no concerns. A hit means *quarantine/escalate*, not *block*.
    """
    base = Path(subagent_dir)
    findings: list[dict] = []
    md_dir = base / "sources" / "markdown"
    if not md_dir.exists():
        return findings
    for md in sorted(md_dir.glob("*.md")):
        _scan_file(md, findings)
    return findings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.prompt_injection_scan subagents/<slug>")
        sys.exit(1)
    findings = prompt_injection_scan(sys.argv[1])
    for f in findings:
        print(
            f"WARN {f['file']}:{f['line']} [{f['family']}/{f['vector']}/{f['severity']}] {f['excerpt']}"
        )
    if not findings:
        print("prompt-injection-scan PASS — no payloads detected")
    sys.exit(0)


if __name__ == "__main__":
    main()
