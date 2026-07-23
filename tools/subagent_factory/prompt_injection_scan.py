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
import html
import re
import sys
import unicodedata
import urllib.parse
from collections.abc import Callable
from pathlib import Path

# ── Canonical denylist (case-insensitive) ────────────────────────────────────
_DENYLIST: list[tuple[str, re.Pattern[str]]] = [
    (
        "imperative-override",
        re.compile(
            r"ignore\s+(all\s+)?(the\s+)?(previous|prior|former|above)\s+instructions?", re.I
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
# Kept explicit as a fallback, but _strip_zero_width also strips the WHOLE Unicode Cf
# (format) category (F2) so inter-letter separators outside this hand-list — soft hyphen
# U+00AD, function-application U+2061, other zero-width / bidi controls — can't defeat the
# word-gap regexes by sitting between letters.
_ZERO_WIDTH = dict.fromkeys([0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x2060, 0xFEFF], None)

# Unicode-confusable fold (Cyrillic/Greek look-alikes → ASCII).
#
# NFKD normalization (applied first in _fold_confusables) is the *load-bearing* defense:
# it canonicalizes the bulk of compatibility/decomposable confusables. This hand-listed
# table is a deliberately small, KNOWN-INCOMPLETE supplement for the common homoglyph-
# substitution attack letters that NFKD leaves alone (Cyrillic/Greek look-alikes share no
# NFKD decomposition with their ASCII twins). Full Unicode TR39 confusable coverage is out
# of scope for this pass — do NOT treat this list as exhaustive.
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
# F4: floor lowered from 16 → 8 so short denylist phrases ("you are now", "TODO: …")
# encoded into a sub-16-char base64 token are still decoded. Tradeoff: 8-char base64
# runs appear more often in natural text, but matching stays gated behind the canonical
# denylist (a decoded fragment only surfaces if it matches a denylist family), so the
# false-positive cost is the extra decode work, not extra findings on benign prose.
# Alphabet includes the base64url chars (-_) so a urlsafe-encoded payload isn't shredded
# at every - / _ into garbage-decoding fragments; _base64_decoded translates -_ → +/ before
# decoding. Standard base64 never contains -_, so the translate is a no-op there.
_BASE64_TOKEN = re.compile(r"[A-Za-z0-9+/_-]{8,}={0,2}")
_B64URL = str.maketrans({"-": "+", "_": "/"})


# Collapse a \r\n\t run (plus immediately-adjacent spaces) that SEPARATES two characters of the
# same class. One template, two char classes — the class is the ONLY intended difference between
# the word-level and base64-level dewraps, so deriving both from `_dewrap` keeps that the single
# point of divergence (a prior bug crept in precisely because two hand-written copies silently
# diverged on the break/pad sets). Plain spaces are never in the break set: collapsing them would
# merge adjacent prose words (the base64 case) or be the accepted-residual letter-spacing attack
# (the word case).
def _dewrap(char_class: str) -> re.Pattern[str]:
    return re.compile(rf"(?<={char_class})[ ]*[\r\n\t]+[ ]*(?={char_class})")


# Word-level: an attacker breaks a denylist word mid-token ("ig\nnore", "ig\tnore") so neither the
# per-line scan nor the whole-doc base matches the literal phrase; rejoining the word fixes it.
# Applied as an ADDITIVE fixpoint transform — the untouched base still carries word-boundary
# whitespace, so a legitimate "previous\ninstructions" (where \s+ must match the newline) is
# unaffected. Merging whitespace can only ever REMOVE a separator, and every denylist phrase
# requires \s+ between words, so this can never manufacture a false hit.
_INTRAWORD_BREAK = _dewrap(r"\w")
# base64-level: a wrapped/newline-or-tab-split blob (MIME line-wrap, or a break at a non-4-aligned
# column to straddle the phrase) is rejoined into one aligned token before decode.
_BASE64_DEWRAP = _dewrap(r"[A-Za-z0-9+/_=-]")

# Bounds for the decode fixpoint (see _decode_fixpoint): _FIXPOINT_DEPTH layers of _TRANSFORMS
# are peeled, so LAYERED obfuscation (rot13∘base64, reversed∘base64, base64∘base64, …) is caught
# up to that many compositions; beyond it is accepted residual risk. _MAX_DERIVED caps total
# derived strings so a pathological re-decoding input cannot explode runtime.
_FIXPOINT_DEPTH = 3
_MAX_DERIVED = 256

# A run of base64-ish characters long enough to plausibly encode a denylist phrase (a layered
# payload's inner base64 always leaves one). Its presence on a line is the trigger for the per-line
# localizer to run the heavier COMPOSING fixpoint on that line — the only per-line path that peels a
# second layer (rot13∘base64, base64∘base64) to a real, redactable line. Lines without such a token
# take the cheap depth-1 path. Such tokens are rare in prose, so the fixpoint cost is paid only where
# an encoded payload plausibly hides.
_LONG_ENCODED_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{20,}")


def _strip_zero_width(text: str) -> str:
    """Strip the explicit zero-width set, every Unicode Cf (format) char, and combining marks.

    Generalizing from ~7 hand-picked codepoints to the whole format category (Cf) closes the
    gap where invisible inter-letter separators (soft hyphen U+00AD, function application
    U+2061, bidi controls, …) defeat the word-gap regexes. Combining marks (category M:
    Mn/Mc/Me) are stripped for the same reason — a lone combining mark inserted between two
    letters (e.g. ``i`` + U+0301 + ``gnore``) is invisible-ish glue that splits a word from
    the ``\\s+``/``\\b`` regexes without NFKD removing it. Legitimate Latin-script override
    phrases carry no bare inter-letter combining marks, so stripping category M is safe here.
    NFKD/confusable folding still runs after this in _fold_confusables.
    """

    def _drop(c: str) -> bool:
        cat = unicodedata.category(c)
        # Cf = format chars (zero-width/bidi); M* = combining marks. NOT Cc — that would
        # strip newlines/tabs and break the line-level + tail passes.
        return c in _ZERO_WIDTH or cat == "Cf" or cat[0] == "M"

    return "".join(c for c in text if not _drop(c))


def _fold_confusables(text: str) -> str:
    # NFKD decomposes a precomposed accented letter into base + combining mark; drop the
    # marks NFKD produces so a diacritic-split payload (precomposed í between letters)
    # collapses to its ASCII base here too — not only on the fixpoint's second strip pass.
    decomposed = unicodedata.normalize("NFKD", text)
    no_marks = "".join(c for c in decomposed if unicodedata.category(c)[0] != "M")
    return no_marks.translate(_CONFUSABLES)


def _strip_html_tags(text: str) -> str:
    """Reassemble DOM-fragmented payloads: ``<span>i</span><span>g</span>`` → ``ig``."""
    return _HTML_TAG.sub("", text)


def _base64_decoded(text: str) -> str:
    """Concatenate the decoded text of base64-looking tokens.

    Decoding is deliberately tolerant of attacker tricks rather than fail-open:
    - **whitespace inside a base64 run is collapsed first** (line-wrapped MIME base64, or a
      newline inserted at a non-4-aligned column to straddle the denylist phrase across two
      fragments), so the run decodes as one aligned token instead of two garbage halves;
    - ``-``/``_`` are translated to ``+``/``/`` so a base64url payload decodes instead of
      being shredded at every url-safe char;
    - unpadded tokens (``len % 4 != 0``) are padded to a multiple of 4 before decode, so a
      stripped ``=`` no longer drops the payload silently;
    - decode as UTF-8 with ``errors="replace"`` (not ASCII-only), so multi-byte payloads
      survive instead of being discarded on a UnicodeDecodeError;
    - fold confusables on the decoded text, so a homoglyph payload hidden inside base64
      still normalizes to the denylist before matching.
    """
    # Collapse \r\n\t between base64 chars so a wrapped/split blob is one token (MIME line-wrap,
    # or a break at a non-4-aligned column to straddle the phrase). Never spaces: collapsing
    # spaces would merge adjacent prose words into the run. Shares `_dewrap` with the word-level
    # break so the two stay in lockstep.
    dewrapped = _BASE64_DEWRAP.sub("", text)
    out: list[str] = []
    for m in _BASE64_TOKEN.finditer(dewrapped):
        tok = m.group(0).rstrip("=").translate(_B64URL)
        pad = (-len(tok)) % 4
        try:
            dec = base64.b64decode(tok + "=" * pad, validate=False).decode(
                "utf-8", errors="replace"
            )
        except (ValueError, UnicodeDecodeError):
            continue
        out.append(_fold_confusables(dec))
    return " ".join(out)


def _denylist_hits(text: str) -> list[str]:
    return sorted({fam for fam, rx in _DENYLIST if rx.search(text)})


def _norm(s: str) -> str:
    return _fold_confusables(_strip_zero_width(s))


# Decode transforms peeled by the fixpoint: name → callable producing a derived string.
# `unescaped` decodes HTML entities / numeric char refs (&#105;…, &#x69;…) — the most common
# DOM obfuscation; `dewrapped` rejoins a word broken mid-token by \r\n\t. In the fixpoint they
# compose with each other (entity∘base64, dewrap∘reverse, …) up to _FIXPOINT_DEPTH.
_TRANSFORMS: dict[str, Callable[[str], str]] = {
    "reversed": lambda s: s[::-1],
    "rot13": lambda s: codecs.decode(s, "rot13"),
    "base64": _base64_decoded,
    "detagged": _strip_html_tags,
    "unescaped": html.unescape,
    "dewrapped": lambda s: _INTRAWORD_BREAK.sub("", s),
    # Percent-decode: URL is a first-class ingested source type (fetch_url.py), where
    # %69%67%6e%6f%72%65 → "ignore" is a zero-effort obfuscation channel not covered above.
    "urldecoded": urllib.parse.unquote,
}


def _scan_lines(raw: str, name: str) -> list[dict]:
    """Line-level denylist on the confusable-folded text (gives line numbers + tail flag).

    Tail hits (last few lines ≈ document tail, where injection success is highest) are raised to
    ``high``/``tail``; body hits are ``medium``/``body``. A single-line document trivially counts
    as tail. The obfuscation pass (``_decode_fixpoint``), by contrast, reports every hit as
    ``high`` with no tail flag — obfuscation itself is the signal there, independent of position.
    """
    folded = _fold_confusables(_strip_zero_width(raw))
    lines = folded.splitlines()
    n = len(lines)
    out: list[dict] = []
    for i, line in enumerate(lines, 1):
        for fam, rx in _DENYLIST:
            if rx.search(line):
                in_tail = i >= max(1, n - 5)
                out.append(
                    {
                        "file": name,
                        "line": i,
                        "family": fam,
                        "vector": "tail" if in_tail else "body",
                        "severity": "high" if in_tail else "medium",
                        "excerpt": line.strip()[:120],
                    }
                )
    return out


def _decode_fixpoint(raw: str, name: str) -> list[dict]:
    """Bounded-depth fixpoint over the decode transforms (whole-doc; findings reported at line 0).

    A flat set of single-transform variants is bypassable by LAYERED obfuscation (rot13∘base64,
    reversed∘base64, base64∘base64, base64-in-reversed). Instead, seed a worklist with the
    normalized BASE (detag → strip zero-width → fold confusables) and, for up to _FIXPOINT_DEPTH
    layers, apply each _TRANSFORMS decode to every newly derived string. Each product is
    re-normalized, deduped via a ``seen`` set (which also breaks transform cycles like
    reverse∘reverse), and matched against the denylist. _MAX_DERIVED bounds total work so a
    pathological re-decoding input cannot blow up.
    """
    base = _norm(_strip_html_tags(raw))
    seen: set[str] = {base}
    # worklist entries: (string, chain-of-transforms-applied-so-far). The chain length is the
    # depth; the base seed has an empty chain (it is the normalized document, no decode applied).
    worklist: list[tuple[str, tuple[str, ...]]] = [(base, ())]
    # (family, vector, decoded-text) dedupe: keying on the decoded text too means a SECOND, distinct
    # payload of the same family/vector is still reported — keying on (family, vector) alone hid it.
    reported: set[tuple[str, str, str]] = set()
    out: list[dict] = []
    while worklist and len(seen) < _MAX_DERIVED:
        current, chain = worklist.pop()
        # The reported vector is the OUTERMOST (first-applied) transform that began the decode
        # path — "base64" for base64>reversed — so a single phrase reached two ways isn't double
        # reported under each composition. The excerpt names the full chain so the
        # source-safety-reviewer can reproduce the exact decode sequence. The base seed (empty
        # chain) reports under "detagged" (it is already detag+strip+fold normalized).
        vector = chain[0] if chain else "detagged"
        for fam in _denylist_hits(current):
            key = (fam, vector, current)
            if key in reported:
                continue
            reported.add(key)
            seq = " > ".join(chain) if chain else "base normalization"
            out.append(
                {
                    "file": name,
                    "line": 0,
                    "family": fam,
                    "vector": vector,
                    "severity": "high",
                    "excerpt": f"payload revealed after {seq}",
                }
            )
        if len(chain) >= _FIXPOINT_DEPTH:
            continue
        for tname, fn in _TRANSFORMS.items():
            try:
                product = _norm(fn(current))
            except (ValueError, UnicodeDecodeError):
                continue
            if not product or product in seen:
                continue
            seen.add(product)
            worklist.append((product, (*chain, tname)))
            if len(seen) >= _MAX_DERIVED:
                break  # stop mid-expansion at the cap; the outer guard then drains the worklist
    return out


def _scan_css(raw: str, name: str) -> list[dict]:
    """Presentation-layer hiding: CSS that renders a payload invisible (opacity:0, display:none…).

    Matches on the SAME confusable-folded / zero-width-stripped text as ``_scan_lines`` (not raw), so
    a homoglyph-substituted property name — e.g. Cyrillic ``о`` in ``оpacity:0`` — is folded to ASCII
    before ``_CSS_HIDDEN`` runs and cannot slip past the presentation-layer detector. Folding is
    per-character and zero-width stripping keeps newlines, so line numbers stay valid."""
    out: list[dict] = []
    for i, line in enumerate(_fold_confusables(_strip_zero_width(raw)).splitlines(), 1):
        if _CSS_HIDDEN.search(line):
            out.append(
                {
                    "file": name,
                    "line": i,
                    "family": "css-hidden",
                    "vector": "css-hidden",
                    "severity": "high",
                    "excerpt": line.strip()[:120],
                }
            )
    return out


def _localize_obfuscation(
    raw: str, name: str, skip_lines: frozenset[int] = frozenset()
) -> list[dict]:
    """Per-line obfuscation scan (SEC-1 localization): report a single-line obfuscated payload — a
    base64 blob, a reversed / rot13 line, an inline DOM-fragmented line — at its REAL source line so it
    is **redactable** (a reviewer can point a ``suspicious`` verdict there), instead of only at
    whole-document ``line 0``.

    Two per-line strategies, chosen per line by a cheap token test:

    - A line carrying a long base64-ish token (``_LONG_ENCODED_TOKEN``) gets the composing
      ``_decode_fixpoint`` on that single line — the ONLY per-line path that peels a **LAYERED**
      single-line payload (rot13∘base64, base64∘base64) down to its real line. The whole-doc fixpoint
      would only ever pin such a payload at ``line 0``, and it can even MISS it: its base64 dewrap
      merges the token with a base64-ish char on an adjacent prose line, corrupting the token. Run on
      one line there is no neighbour to merge, so this both localizes AND detects. Bounded by
      ``_MAX_DERIVED``; such tokens are rare in prose, so the fixpoint cost is paid only where a payload
      plausibly hides.
    - Every other line gets a cheap **single-transform** (depth-1) pass — the detagged line + one
      application of each transform — which localizes a single-LAYER payload (lone base64, reversed,
      rot13, inline DOM) without the fixpoint's expansion.

    A genuinely *cross-line* payload (spanning several source lines) has no single line to point at and
    stays a whole-document ``line 0`` finding — blocked, not localized (the fundamental residual).
    ``skip_lines`` are the lines ``_scan_lines`` already flags plainly."""
    out: list[dict] = []
    for i, line in enumerate(raw.splitlines(), 1):
        if i in skip_lines or not line.strip():
            continue
        if _LONG_ENCODED_TOKEN.search(line):
            # Composing fixpoint on THIS line only: localizes a LAYERED single-line payload (and detects
            # a base64 token the whole-doc dewrap would corrupt by merging a prose neighbour). Its
            # findings are line-0 (whole-"doc" == this one line); relabel to the real line i. The base
            # seed can also hit here for an inline-DOM payload, subsuming the depth-1 detagged candidate.
            out.extend({**f, "line": i} for f in _decode_fixpoint(line, name))
            continue
        base = _norm(_strip_html_tags(line))
        # Candidates: the detagged/normalized line itself (inline DOM fragmentation reveals the payload
        # with no further decode) + one application of each transform (single layer).
        candidates: list[tuple[str, str]] = [("detagged", base)]
        for tname, fn in _TRANSFORMS.items():
            try:
                candidates.append((tname, _norm(fn(base))))
            except (ValueError, UnicodeDecodeError):
                continue
        seen: set[tuple[str, str]] = set()  # (family, vector) per line
        for vector, decoded in candidates:
            if not decoded:
                continue
            for fam in _denylist_hits(decoded):
                if (fam, vector) in seen:
                    continue
                seen.add((fam, vector))
                out.append(
                    {
                        "file": name,
                        "line": i,
                        "family": fam,
                        "vector": vector,
                        "severity": "high",
                        "excerpt": f"payload revealed after {vector}",
                    }
                )
    return out


def _scan_file(path: Path) -> list[dict]:
    """All findings for one markdown file: line-level + per-line + whole-doc obfuscation + CSS-hidden."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        # Fail closed: "could not read" is a different (non-clean) state than "scanned, no
        # concerns"; returning [] would let an unreadable source pass silently. Surface it for
        # triage instead (mirrors adapter_policy_scan's fail-closed handling of unmodelled shapes).
        return [
            {
                "file": str(path),
                "line": 0,
                "family": "scan-error",
                "vector": "unreadable",
                "severity": "high",
                "excerpt": f"could not read file: {e.__class__.__name__}",
            }
        ]
    name = str(path)
    line_findings = _scan_lines(raw, name)
    plain_lines = frozenset(f["line"] for f in line_findings)
    return [
        *line_findings,
        # SEC-1 localization: single-line obfuscated payloads at their REAL, redactable source line.
        # This also catches base64 the whole-doc pass misses when a token is newline-adjacent to prose
        # (the dewrap merges the neighbour into the token), so it is a detection improvement too.
        *_localize_obfuscation(raw, name, plain_lines),
        # Whole-doc fixpoint (line 0): the backstop for genuinely cross-line payloads.
        *_decode_fixpoint(raw, name),
        *_scan_css(raw, name),
    ]


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
        findings.extend(_scan_file(md))
    return findings


def scan_book_module(module_dir: str | Path) -> list[dict]:
    """Scan a chunk_source book-extract module (``cache/book-extracts/<sha>/``) for injection payloads.

    The map-reduce (Tier-1+) path never populates per-package ``sources/markdown/``, so
    ``prompt_injection_scan`` above is vacuous there; the untrusted book text lives in the module's
    ``source.md`` (the chunks are overlapping windows of it, so scanning ``source.md`` once covers
    every chunk the MAP session reads). Same advisory finding shape and semantics — a hit means
    *quarantine/escalate*, not *block*. ``file`` is the ``source.md`` path so a downstream redactor
    can locate the span. Empty list = scanned clean; a missing ``source.md`` is reported as a
    ``scan-error`` finding (NOT ``[]``), so "not scanned" fails closed instead of reading as clean.
    """
    src = Path(module_dir) / "source.md"
    if not src.exists():
        # Absent source ≠ clean. Mirror _scan_file's fail-closed on an unreadable file: surface a
        # scan-error finding so a downstream reader (verify / the gate) treats it as un-scanned.
        return [
            {
                "file": str(src),
                "line": 0,
                "family": "scan-error",
                "vector": "missing-source",
                "severity": "high",
                "excerpt": "source.md absent — module was not scanned",
            }
        ]
    return _scan_file(src)


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
    # Advisory by design: this scanner is WARN/triage, never a hard block (untrusted-source-policy.md,
    # WARN-not-block at a ~225:1 benign:attack base rate). It intentionally exits 0 even on findings;
    # gating happens in validate_generated_package + source-safety triage, not in this entry point.
    sys.exit(0)


if __name__ == "__main__":
    main()
