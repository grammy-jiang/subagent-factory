"""Code-enforced quarantine of confirmed prompt-injection spans (Step 5.5, corrective half).

The prompt-injection scan (``prompt_injection_scan.py``) is high-recall advisory triage; the
``source-safety-reviewer`` agent decides which flagged spans are REAL injections. Until now that
verdict was enforced only by INSTRUCTION ("treat this span as data-only, do not distill it") — the
raw payload still reached the interrogation session's context verbatim. This tool makes the verdict
enforcement CODE: it reads the reviewer's structured verdicts and neutralizes every span marked
``suspicious`` from the canonical Markdown the interrogation session actually reads.

Contract (deliberately strict — at the realistic ~225:1 benign:attack base rate, over-redaction is
the greater harm, so redaction is driven ONLY by an explicit ``suspicious`` verdict, never by a raw
scan hit):

- Input verdicts: ``reports/source-safety-verdicts.yaml`` (schema ``source-safety-verdicts-v1``).
  Each ``suspicious`` verdict names a concrete source ``line`` (1-indexed) to neutralize — the
  reviewer has read the file, so it can always point at the line; this also covers obfuscated
  payloads (a base64 blob lives on some line even though its *decoded* excerpt is not literal
  source text, so literal-excerpt matching would be fragile).
- Neutralization is WHOLE-LINE replacement with a placeholder, preserving line count so existing
  source anchors (``L<n>`` / line-keyed provenance) stay valid.
- The pristine pre-redaction Markdown is preserved under ``sources/markdown-raw/<name>.md`` for
  audit and reversibility. Each run rebuilds the redaction from that pristine copy, so the tool is a
  pure function of the verdicts file: removing a verdict restores its line, re-runs never compound.
- ``file`` is resolved by BASENAME under ``sources/markdown/`` — a verdicts file cannot point the
  redactor outside the package (no ``../`` traversal).

The paired enforcement is ``validate_generated_package``'s ``injection-quarantine`` gate: a
``suspicious`` verdict whose line is not the placeholder FAILs the package, so the redactor cannot be
silently skipped. ``sources/markdown-raw/`` is skipped by ``quote_scan`` (its path starts with
``sources/markdown``) and is not re-scanned by ``prompt_injection_scan`` (which globs
``sources/markdown/*.md`` only), so the pristine copy adds no new rights or scan surface.
"""

import json
import sys
from pathlib import Path

import yaml

# Whole-line replacement text. Kept anchorless and whitespace-free so a `.strip()` compare in the
# validate gate matches regardless of the neutralized line's original indentation / trailing space.
PLACEHOLDER = (
    "[REDACTED: prompt-injection span — source-safety verdict=suspicious; "
    "see reports/source-safety-verdicts.yaml]"
)


def _verdicts_path(base: Path) -> Path:
    return base / "reports" / "source-safety-verdicts.yaml"


def _parse_verdicts(p: Path) -> list[dict]:
    """Parse + validate a source-safety-verdicts-v1 file at an explicit path.

    Returns ``[]`` when absent. Raises ``ValueError`` on a malformed file: this is a security gate,
    so an unparseable/ill-formed verdicts file fails closed rather than reading as "no suspicious
    spans". Shared by the package path (reports/…) and the book-module path (module/…).
    """
    if not p.exists():
        return []
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as e:
        raise ValueError(f"unreadable/invalid verdicts file {p}: {e}") from e
    if data is None:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("verdicts"), list):
        raise ValueError(f"{p}: must be a mapping with a 'verdicts' list")
    out: list[dict] = []
    for i, v in enumerate(data["verdicts"]):
        if not isinstance(v, dict):
            raise ValueError(f"{p}: verdict[{i}] is not a mapping")
        if v.get("verdict") not in ("suspicious", "benign"):
            raise ValueError(f"{p}: verdict[{i}] has invalid verdict {v.get('verdict')!r}")
        if not str(v.get("file") or "").strip():
            raise ValueError(f"{p}: verdict[{i}] missing 'file'")
        out.append(v)
    return out


def load_verdicts(subagent_dir: str | Path) -> list[dict]:
    """Load a package's ``reports/source-safety-verdicts.yaml`` (schema source-safety-verdicts-v1)."""
    return _parse_verdicts(_verdicts_path(Path(subagent_dir)))


def _line_ending(s: str) -> str:
    if s.endswith("\r\n"):
        return "\r\n"
    if s.endswith("\n"):
        return "\n"
    return ""  # final line without a trailing newline


def redact_injection_spans(subagent_dir: str | Path) -> dict:
    """Neutralize every ``suspicious`` span in the canonical Markdown; return a summary.

    Summary keys: ``verdicts`` (total), ``suspicious``, ``redacted`` (lines neutralized), ``files``
    (canonical files rewritten), ``restored`` (files whose suspicious verdicts were removed → line
    restored from the pristine copy), ``unresolved`` (suspicious verdicts that could not be applied,
    e.g. missing file / line out of range — surfaced, never silently dropped).
    """
    base = Path(subagent_dir)
    md_dir = base / "sources" / "markdown"
    raw_dir = base / "sources" / "markdown-raw"
    verdicts = load_verdicts(base)
    suspicious = [v for v in verdicts if v.get("verdict") == "suspicious"]

    # Group suspicious verdicts by canonical file basename (basename resolution blocks traversal).
    by_file: dict[str, list[dict]] = {}
    unresolved: list[dict] = []
    for v in suspicious:
        name = Path(str(v["file"])).name
        if not (md_dir / name).exists():
            unresolved.append(
                {"file": name, "line": v.get("line"), "reason": "markdown file not found"}
            )
            continue
        by_file.setdefault(name, []).append(v)

    written: list[str] = []
    for name in sorted(by_file):
        target = md_dir / name
        raw = raw_dir / name
        # Snapshot the pristine source ONCE; thereafter always redact from it (idempotent, no compounding).
        if not raw.exists():
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        lines = raw.read_text(encoding="utf-8").splitlines(keepends=True)
        for v in by_file[name]:
            ln = v.get("line")
            if not isinstance(ln, int) or isinstance(ln, bool) or ln < 1 or ln > len(lines):
                unresolved.append({"file": name, "line": ln, "reason": "line out of range"})
                continue
            lines[ln - 1] = PLACEHOLDER + _line_ending(lines[ln - 1])
        target.write_text("".join(lines), encoding="utf-8")
        written.append(name)

    # Reversibility: a file whose suspicious verdicts were all removed is restored from its pristine
    # copy, so the on-disk state is a pure function of the current verdicts file.
    restored: list[str] = []
    if raw_dir.exists():
        for raw in sorted(raw_dir.glob("*.md")):
            if raw.name not in by_file:
                target = md_dir / raw.name
                # Restore only a file that still exists — never re-materialize one deliberately
                # deleted between runs; just drop the orphan snapshot.
                if target.exists():
                    target.write_text(raw.read_text(encoding="utf-8"), encoding="utf-8")
                    restored.append(raw.name)
                raw.unlink()
        try:
            raw_dir.rmdir()  # drop the dir once it holds no snapshots
        except OSError:
            pass

    return {
        "verdicts": len(verdicts),
        "suspicious": len(suspicious),
        "redacted": len(suspicious) - len(unresolved),
        "files": written,
        "restored": restored,
        "unresolved": unresolved,
    }


def redact_book_module(module_dir: str | Path) -> dict:
    """Neutralize confirmed-``suspicious`` spans in a chunk_source book-extract module (approach A).

    The map-reduce MAP session reads the module's ``chunks/*.md`` — verbatim copies of spans of
    ``source.md``, which the injection scan flagged. Driven by
    ``<module>/source-safety-verdicts.yaml`` (schema source-safety-verdicts-v1, ``file`` = source.md):
    whole-line-redact each suspicious source line, then propagate to every chunk by matching the exact
    pristine line text — so the payload is gone from BOTH source.md and every chunk before MAP reads
    it. Chunk ids (filenames) are unchanged — only line contents are neutralized — so
    content-addressing and anchors stay valid. Pristine copies (``source.md.raw``, ``chunks-raw/``)
    are kept for audit and idempotent rebuild (each run redacts from pristine, never compounds).
    """
    base = Path(module_dir)
    suspicious = [
        v
        for v in _parse_verdicts(base / "source-safety-verdicts.yaml")
        if v.get("verdict") == "suspicious"
    ]
    summary: dict = {
        "suspicious": len(suspicious),
        "source_lines_redacted": 0,
        "chunk_lines_redacted": 0,
        "unresolved": [],
    }
    src = base / "source.md"
    if not suspicious or not src.exists():
        return summary

    raw = base / "source.md.raw"
    if not raw.exists():
        raw.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    pristine = raw.read_text(encoding="utf-8").splitlines(keepends=True)
    lines = list(pristine)
    payloads: set[str] = set()
    for v in suspicious:
        ln = v.get("line")
        if not isinstance(ln, int) or isinstance(ln, bool) or ln < 1 or ln > len(pristine):
            summary["unresolved"].append({"line": ln, "reason": "line out of range"})
            continue
        text = pristine[ln - 1].strip()
        if text:
            payloads.add(text)
        lines[ln - 1] = PLACEHOLDER + _line_ending(pristine[ln - 1])
        summary["source_lines_redacted"] += 1
    src.write_text("".join(lines), encoding="utf-8")

    # Propagate to the chunks (what MAP actually reads) by exact pristine-line match.
    chunks_dir = base / "chunks"
    if payloads and chunks_dir.is_dir():
        raw_chunks = base / "chunks-raw"
        raw_chunks.mkdir(exist_ok=True)
        for ch in sorted(chunks_dir.glob("*.md")):
            praw = raw_chunks / ch.name
            if not praw.exists():
                praw.write_text(ch.read_text(encoding="utf-8"), encoding="utf-8")
            clines = praw.read_text(encoding="utf-8").splitlines(keepends=True)
            changed = False
            for i, cl in enumerate(clines):
                if cl.strip() and cl.strip() in payloads:
                    clines[i] = PLACEHOLDER + _line_ending(cl)
                    summary["chunk_lines_redacted"] += 1
                    changed = True
            if changed:
                ch.write_text("".join(clines), encoding="utf-8")
    return summary


def _real_line(f: dict) -> int | None:
    """A finding's 1-indexed source line, or ``None`` for a whole-document (line-0 / obfuscated) hit.

    Rejects ``bool`` (``True``/``False`` are ``int`` subclasses that would coerce to 1/0) and any
    line < 1, so callers can branch on "has a real source line" without repeating the guard."""
    ln = f.get("line")
    if isinstance(ln, bool) or not isinstance(ln, int) or ln < 1:
        return None
    return ln


def _load_scan_findings(path: Path) -> list[dict]:
    """Load a book module's injection-scan.jsonl (one JSON finding per line); [] if absent."""
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def verify_book_module(module_dir: str | Path) -> dict:
    """Verify a book module after redaction. Returns ``{"leaks": [...], "untriaged": [...]}``.

    Both lists fail the gate closed (callers exit non-zero on either): "cannot prove the payload is
    gone" must never read as clean.

    - ``leaks``: a **suspicious** verdict that is not provably neutralized — either its pristine
      payload text still appears in ``source.md``/a chunk (a redaction FAILURE), or it cannot be
      checked at all: no pristine snapshot yet (redaction never ran), a line out of range, or a
      verdict with no real source line (a line-0 obfuscated finding). An unverifiable suspicious
      verdict is flagged ``unverified`` rather than silently skipped — the reviewer asserted the line
      is a live payload, so "can't verify removed" is treated as a leak.
    - ``untriaged``: a chunk-time scan finding with **no** matching verdict — a triage gap that fails
      closed. A **genuinely-obfuscated** line-0 finding (decoded from base64/rot13/… with no
      same-family line-level sibling) counts: it cannot be pinned to a source line, so it is the most
      important to surface, not the least. A line-0 *base-seed duplicate* (``detagged``/``dewrapped``
      normalization of a payload that IS also found at a real line — same family) does **not** count:
      triaging/redacting that real line neutralizes it, so requiring a separate line-0 verdict would
      permanently fail-close every plain injection. Clear a genuine obfuscated finding with a verdict
      at line 0 (a whole-document acknowledgement).
    """
    base = Path(module_dir)
    findings = _load_scan_findings(base / "injection-scan.jsonl")
    verdicts = _parse_verdicts(base / "source-safety-verdicts.yaml")
    verdict_lines = {v.get("line") for v in verdicts}
    # Families that appear at a real (≥1) line — a line-0 finding of such a family is a base-seed
    # duplicate of that line-level finding, neutralized when the real line is triaged/redacted, so it
    # must NOT independently keep the module untriaged (else every plain injection fails closed).
    line_level_families = {f.get("family") for f in findings if _real_line(f) is not None}
    untriaged = [
        {
            "file": Path(str(f.get("file", ""))).name,
            "line": f.get("line"),
            "family": f.get("family"),
            "vector": f.get("vector"),
        }
        for f in findings
        if f.get("line") not in verdict_lines
        # keep line-level findings + genuinely-obfuscated-only line-0 findings; drop base-seed dups.
        and (_real_line(f) is not None or f.get("family") not in line_level_families)
    ]

    raw = base / "source.md.raw"
    raw_exists = raw.exists()
    pristine = raw.read_text(encoding="utf-8").splitlines() if raw_exists else []
    src_text = (
        (base / "source.md").read_text(encoding="utf-8") if (base / "source.md").exists() else ""
    )
    chunk_texts = (
        {p.name: p.read_text(encoding="utf-8") for p in sorted((base / "chunks").glob("*.md"))}
        if (base / "chunks").is_dir()
        else {}
    )
    leaks: list[dict] = []
    for v in verdicts:
        if v.get("verdict") != "suspicious":
            continue
        ln = v.get("line")
        if not isinstance(ln, int) or isinstance(ln, bool) or ln < 1:
            # A suspicious verdict with no real source line (e.g. a confirmed line-0 obfuscated
            # finding) cannot be proven removed by pristine-line matching — fail closed as unverified.
            leaks.append({"line": ln, "where": "unverifiable — no source line", "unverified": True})
            continue
        if not raw_exists or ln > len(pristine):
            # No pristine snapshot (redaction never ran) or the line is out of range: we cannot prove
            # the payload is gone. Treat "cannot verify removed" as a leak, not a silent clean.
            leaks.append(
                {
                    "line": ln,
                    "where": "unverified — redaction not run / line out of range",
                    "unverified": True,
                }
            )
            continue
        payload = pristine[ln - 1].strip()
        if not payload:
            continue
        if payload in src_text:
            leaks.append({"line": ln, "where": "source.md"})
        for name, ct in chunk_texts.items():
            if payload in ct:
                leaks.append({"line": ln, "where": f"chunks/{name}"})
    return {"leaks": leaks, "untriaged": untriaged}


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python -m tools.subagent_factory.redact_injection_spans "
            "(subagents/<slug> | --book-module <module> | --verify-book-module <module>)"
        )
        sys.exit(1)
    # Verify-only mode: report leaks + untriaged for a book module without mutating it.
    if sys.argv[1] == "--verify-book-module":
        if len(sys.argv) < 3:
            print("redact-injection-spans FAIL — --verify-book-module requires a module dir")
            sys.exit(1)
        try:
            vr = verify_book_module(sys.argv[2])
        except ValueError as e:
            print(f"redact-injection-spans FAIL — {e}")
            sys.exit(1)
        for leak in vr["leaks"]:
            print(
                f"  LEAK: suspicious span (source line {leak['line']}) present in {leak['where']}"
            )
        for u in vr["untriaged"]:
            print(f"  UNTRIAGED: {u['file']}:{u['line']} (scan finding with no verdict)")
        print(f"verify-book-module — {len(vr['leaks'])} leak(s), {len(vr['untriaged'])} untriaged")
        # Fail closed on EITHER: a leak (payload provably/unverifiably present) OR an untriaged
        # finding (a scan hit nobody decided on). An untriaged finding that never gates is a safety
        # net that is computed but not load-bearing — exactly the silent bypass this verify prevents.
        sys.exit(1 if (vr["leaks"] or vr["untriaged"]) else 0)
    # Book-module mode (map-reduce path): neutralize source.md + chunks from the module's verdicts.
    if sys.argv[1] == "--book-module":
        if len(sys.argv) < 3:
            print("redact-injection-spans FAIL — --book-module requires a module dir")
            sys.exit(1)
        try:
            bs = redact_book_module(sys.argv[2])
        except ValueError as e:
            print(f"redact-injection-spans FAIL — {e}")
            sys.exit(1)
        print(
            f"redact-book-module — {bs['source_lines_redacted']} source line(s) + "
            f"{bs['chunk_lines_redacted']} chunk line(s) neutralized "
            f"({bs['suspicious']} suspicious verdict(s))"
        )
        # Fail closed if a suspicious payload survived / could not be verified removed (a bug), OR if
        # any scan finding was never triaged — map_book.sh gates on this rc, so both must exit non-zero.
        verify = verify_book_module(sys.argv[2])
        if verify["leaks"]:
            for leak in verify["leaks"]:
                print(
                    f"  LEAK: suspicious span (source line {leak['line']}) still present in {leak['where']}"
                )
            sys.exit(1)
        if bs["unresolved"]:
            for u in bs["unresolved"]:
                print(f"  UNRESOLVED: line {u['line']} — {u['reason']}")
            sys.exit(1)
        if verify["untriaged"]:
            for u in verify["untriaged"]:
                print(f"  UNTRIAGED: {u['file']}:{u['line']} — scan finding with no verdict")
            sys.exit(1)
        return
    try:
        summary = redact_injection_spans(sys.argv[1])
    except ValueError as e:
        print(f"redact-injection-spans FAIL — {e}")
        sys.exit(1)
    if not summary["suspicious"]:
        print("redact-injection-spans — no suspicious verdicts; nothing to neutralize")
        return
    print(
        f"redact-injection-spans — neutralized {summary['redacted']}/{summary['suspicious']} "
        f"span(s) across {len(summary['files'])} file(s)"
    )
    for name in summary["files"]:
        print(f"  redacted: sources/markdown/{name} (pristine → sources/markdown-raw/{name})")
    for name in summary["restored"]:
        print(f"  restored: sources/markdown/{name} (suspicious verdict removed)")
    for u in summary["unresolved"]:
        print(f"  UNRESOLVED: {u['file']}:{u['line']} — {u['reason']}")
    if summary["unresolved"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
