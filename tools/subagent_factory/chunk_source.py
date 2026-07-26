"""Deterministic structure-aware chunker for staged book Markdown (per-book MAP-inner).

Splits a `pymupdf4llm`-converted book (which carries ATX `#` headings) into contiguous,
heading-aligned chunks sized for deep per-chunk claim extraction — the MAP-inner unit of the
per-book authoring upgrade (`docs/per-book-authoring-upgrade.md`). Whole-book-in-one-prompt is
infeasible for the real corpus (200k-880k tok) and degrades extraction (flat reading loses recall
past ~800 tok); a structure-aware chunk carrying its heading breadcrumb + a neighbour-overlap is the
recall-preserving unit (long-document-structure-mapping research: neighbour context recovers
boundary-spanning units, ~3.6% overhead).

Deterministic — NO LLM (factory determinism boundary). Content-addressed by sha256 of the source
bytes, so a book chunked on any machine yields identical chunk ids.

Library:
    chunk_markdown(text, target_tokens=8000, overlap_chars=1500) -> list[Chunk]
CLI:
    python -m tools.subagent_factory.chunk_source <staged.md> [--out cache/book-extracts]
        [--target-tokens 8000] [--overlap-chars 1500]
    -> writes <out>/<sha>/source.md, <out>/<sha>/chunks/<chunk_id>.md, <out>/<sha>/chunks.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from tools.subagent_factory._common import CHARS_PER_TOKEN
from tools.subagent_factory.prompt_injection_scan import scan_book_module

# ATX heading. The trailing group strips ONLY a true ATX closing sequence — a whitespace-preceded
# `#` run (`# Title ###` -> "Title") — not a `#` fused to the title text (`# C#` stays "C#").
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
# A fenced code block opens/closes on a line whose first non-space run is ``` or ~~~ (3+).
_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")


@dataclass
class Chunk:
    """One heading-aligned chunk: metadata + the text actually fed to extraction.

    Two distinct sizes are recorded and MUST NOT be conflated:
    - ``char_start``/``char_end`` index **the source** (``source.md``): ``source[char_start:char_end]``
      is the chunk's raw body, which feeds line-number provenance (``emit_chunk_anchors``). They do
      *not* index ``text``.
    - ``est_tokens`` estimates **the fed text** (``text`` = breadcrumb header + optional
      neighbour-overlap + body), i.e. what extraction actually reads — larger than the source body.
    ``body_chars`` (= ``char_end - char_start``) is the source-body length, kept alongside so a
    consumer can compare the source span against the fed-text token estimate without re-deriving it.
    """

    chunk_id: str  # "<sha12>-c0001"
    index: int
    heading_path: str  # "Part II > Chapter 3 > 3.2 Foo" (breadcrumb), or "(preamble)"
    char_start: int  # offset into source.md (NOT into `text`) of the chunk body start
    char_end: int  # offset into source.md of the chunk body end
    est_tokens: (
        int  # token estimate of the FED text (breadcrumb + overlap + body), not the source body
    )
    text: str  # the fed text actually sent to extraction (header + overlap + body)
    body_chars: int = 0  # length of the source body span (char_end - char_start)


def _iter_segments(text: str) -> list[tuple[list[str], int, str]]:
    """Split into (heading_path, char_start, body) segments at every heading boundary.

    Each segment begins with its own heading line (or is the pre-heading preamble) and carries the
    full heading breadcrumb (stack of ancestor titles) active at that point.

    Fence-aware: a ``#`` line *inside* a ```` ``` ````/``~~~`` fenced code block is body text (e.g. a
    shell comment), never an ATX heading — heading detection is suppressed until the fence closes, so
    such a line cannot corrupt the breadcrumb stack or open a spurious segment.
    """
    segments: list[tuple[list[str], int, str]] = []
    stack: list[tuple[int, str]] = []
    seg_lines: list[str] = []
    seg_path: list[str] = []
    seg_start = 0
    offset = 0
    started = False
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\n")
        fence_m = _FENCE.match(stripped)
        if fence_m:
            marker = fence_m.group(1)[0]  # ` or ~
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                # A fence only closes on its own marker type (``` does not close a ~~~ block).
                in_fence, fence_marker = False, ""
        m = None if in_fence else _HEADING.match(stripped)
        if m:
            if seg_lines:
                segments.append((seg_path, seg_start, "".join(seg_lines)))
            level = len(m.group(1))
            title = m.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            seg_path = [t for _, t in stack]
            seg_lines = [line]
            seg_start = offset
            started = True
        else:
            if not started:
                seg_path = []
                seg_start = offset
                started = True
            seg_lines.append(line)
        offset += len(line)
    if seg_lines:
        segments.append((seg_path, seg_start, "".join(seg_lines)))
    return segments


def _split_oversize(
    path: list[str], start: int, body: str, target_chars: int
) -> list[tuple[list[str], int, str]]:
    """Split a single over-target segment into <=target paragraph groups (keeps paragraphs whole).

    Offset-exact: the emitted pieces concatenate back to ``body`` byte-for-byte (the separator is
    re-attached to the piece it followed, never collapsed), so each piece's ``char_start`` stays a
    true offset into the source. A single paragraph larger than ``target_chars`` is emitted whole
    (paragraphs are never broken), so a piece may exceed the target — best-effort, not a hard cap.
    """
    out: list[tuple[list[str], int, str]] = []
    cur: list[str] = []
    cur_len = 0
    cur_start = start
    offset = start
    # Keep the "\n\n" separators by splitting with a capturing group and re-pairing each paragraph
    # with the delimiter that followed it; pieces then reconstruct body exactly.
    parts = re.split(r"(\n\n)", body)
    paras: list[str] = []
    for i in range(0, len(parts), 2):
        sep = parts[i + 1] if i + 1 < len(parts) else ""
        paras.append(parts[i] + sep)
    for piece in paras:
        if not piece:
            continue
        if cur and cur_len + len(piece) > target_chars:
            out.append((path, cur_start, "".join(cur)))
            cur, cur_len, cur_start = [], 0, offset
        cur.append(piece)
        cur_len += len(piece)
        offset += len(piece)
    if cur:
        out.append((path, cur_start, "".join(cur)))
    return out


def chunk_markdown(
    text: str, *, target_tokens: int = 8000, overlap_chars: int = 1500
) -> list[Chunk]:
    """Chunk staged Markdown into heading-aligned, <=target-token pieces with neighbour overlap."""
    target_chars = max(target_tokens, 1) * CHARS_PER_TOKEN
    sha12 = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

    pieces: list[tuple[list[str], int, str]] = []
    for path, start, body in _iter_segments(text):
        if len(body) <= target_chars:
            pieces.append((path, start, body))
        else:
            pieces.extend(_split_oversize(path, start, body, target_chars))

    # Greedily pack consecutive pieces up to target; the chunk's path is its first piece's path.
    # Track the true end offset of the last packed piece so char_end is a real source offset
    # (start + len(joined_body) only holds if pieces tile the source contiguously; carrying the
    # end explicitly keeps char_end correct under any future packing change).
    packed: list[tuple[list[str], int, int, str]] = []  # (path, start, end, body)
    cur: tuple[list[str], int, int, list[str]] | None = None  # (path, start, end, bodies)
    cur_len = 0
    for path, start, body in pieces:
        end = start + len(body)
        if cur is None:
            cur, cur_len = (path, start, end, [body]), len(body)
        elif cur_len + len(body) <= target_chars:
            cur[3].append(body)
            cur = (cur[0], cur[1], end, cur[3])
            cur_len += len(body)
        else:
            packed.append((cur[0], cur[1], cur[2], "".join(cur[3])))
            cur, cur_len = (path, start, end, [body]), len(body)
    if cur is not None:
        packed.append((cur[0], cur[1], cur[2], "".join(cur[3])))

    chunks: list[Chunk] = []
    prev_body = ""
    for i, (path, start, end, body) in enumerate(packed):
        breadcrumb = " > ".join(path) if path else "(preamble)"
        header = f"<!-- chunk {i} context: {breadcrumb} -->\n\n"
        if overlap_chars and prev_body:
            # Start the overlap at a WHOLE-LINE boundary. A raw char slice can cut mid-line, leaving a
            # truncated suffix of a (possibly injection-flagged) line in the next chunk's header that
            # whole-line redaction/verification cannot match (SEC-4). Dropping the partial leading line
            # guarantees the overlap carries only complete lines, so a flagged line here is redacted
            # like any other. If the slice holds no newline (a single line longer than overlap_chars),
            # there is no whole line to keep, so the overlap is omitted for that boundary.
            tail = prev_body[-overlap_chars:]
            nl = tail.find("\n")
            tail = tail[nl + 1 :] if nl != -1 else ""
            if tail:
                header += f"<!-- neighbour-overlap (prev chunk tail, for context only) -->\n{tail}\n<!-- begin new content -->\n\n"
        fed = header + body
        chunks.append(
            Chunk(
                chunk_id=f"{sha12}-c{i:04d}",
                index=i,
                heading_path=breadcrumb,
                char_start=start,
                char_end=end,
                est_tokens=len(fed) // CHARS_PER_TOKEN,  # of the FED text, not the source body
                text=fed,
                body_chars=end - start,  # source-body span length (char_end - char_start)
            )
        )
        prev_body = body
    return chunks


def write_book_module(
    source_md: Path, out_root: Path, *, target_tokens: int = 8000, overlap_chars: int = 1500
) -> dict:
    """Chunk a staged book md into a content-addressed `cache/book-extracts/<sha>/` module.

    The module dir ``<sha>`` and the per-chunk ``<sha12>`` are derived from the SAME canonical bytes
    (the UTF-8 re-encoding of the decoded text), so ``sha.startswith(sha12)`` always holds — even for
    a source with invalid UTF-8. (Hashing ``raw`` for the dir while ``chunk_markdown`` hashes the
    decoded text let the two diverge on malformed input, contradicting content-addressing.)
    """
    raw = source_md.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    canonical = text.encode("utf-8")
    sha = hashlib.sha256(canonical).hexdigest()
    chunks = chunk_markdown(text, target_tokens=target_tokens, overlap_chars=overlap_chars)

    base = out_root / sha
    (base / "chunks").mkdir(parents=True, exist_ok=True)
    (base / "source.md").write_bytes(raw)
    manifest_lines: list[str] = []
    for c in chunks:
        text_path = f"chunks/{c.chunk_id}.md"
        (base / text_path).write_text(c.text, encoding="utf-8")
        manifest_lines.append(
            json.dumps(
                {
                    "chunk_id": c.chunk_id,
                    "index": c.index,
                    "heading_path": c.heading_path,
                    "char_start": c.char_start,  # offset into source.md, not text_path
                    "char_end": c.char_end,
                    "body_chars": c.body_chars,  # source-body span length
                    "est_tokens": c.est_tokens,  # estimate of the fed text in text_path
                    "text_path": text_path,
                },
                ensure_ascii=False,
            )
        )
    (base / "chunks.jsonl").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # Injection scan AT CHUNK TIME (approach A): the map-reduce path never populates per-package
    # sources/markdown/, so the classic prompt_injection_scan is vacuous there. Scan the untrusted
    # book text HERE — deterministically, before any MAP `claude -p` session reads it — and record
    # findings as a module artifact. Advisory (non-blocking): map_book.sh gates/triage on it. Always
    # written (0 lines when clean) so a downstream reader can tell "scanned, clean" from "not scanned".
    injection = scan_book_module(base)
    (base / "injection-scan.jsonl").write_text(
        "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in injection), encoding="utf-8"
    )

    total_tok = sum(c.est_tokens for c in chunks)
    return {
        "sha": sha,
        "source": str(source_md),
        "title": source_md.stem,
        "n_chunks": len(chunks),
        "est_tokens": total_tok,
        "module": str(base),
        "n_injection_findings": len(injection),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic structure-aware Markdown chunker.")
    ap.add_argument("source", type=Path, help="staged book markdown")
    ap.add_argument("--out", type=Path, default=Path("cache/book-extracts"))
    ap.add_argument("--target-tokens", type=int, default=8000)
    ap.add_argument("--overlap-chars", type=int, default=1500)
    args = ap.parse_args()
    if not args.source.is_file():
        print(f"not a file: {args.source}", file=sys.stderr)
        return 2
    info = write_book_module(
        args.source,
        args.out,
        target_tokens=args.target_tokens,
        overlap_chars=args.overlap_chars,
    )
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
