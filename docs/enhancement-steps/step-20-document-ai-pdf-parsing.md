# Step 20 — Document-AI / PDF parsing (heading recovery + migration tooling)

The binding constraint the Step-10 A/B surfaced: **anchor quality is only as good as the
PDF→Markdown conversion.** Most book PDFs were converted by MarkItDown, which flattens them to
heading-less walls of text. With no `^#` headings, `inject_anchors` fell back to page-break
anchoring on running-head lines → the anchor index was empty or pure page-header noise, and every
downstream `source_anchor` pointed at junk. No reading-strategy improvement matters below that
floor.

## Solution: Docling, CPU-only

`convert_pdf` already had Docling first in its chain (Docling → MarkItDown → PyMuPDF); it was
simply never installed (heavy ML deps). Installing it CPU-only is the fix — no code change to the
chain.

```bash
# CPU-only (no GPU): install CPU torch FIRST so Docling skips the ~5-8 GB CUDA stack
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install docling
```

Proven on a real book PDF: **Docling 126 headings vs MarkItDown 0** (+ real tables);
`inject_anchors` then emits semantic heading anchors instead of the paragraph fallback.

### Born-digital fast path

`_try_docling` disables OCR and the table-structure ML model (`do_ocr=False`,
`do_table_structure=False`). Both are dead weight on born-digital book PDFs and dominate CPU time;
disabling them keeps the heading hierarchy (what the anchor layer needs) while cutting a ~100-page
convert from tens of minutes to ~70s. Falls back to the default converter on any API mismatch.
Tables degrade to inline text — acceptable for text-dense advisory/reference sources. Scanned PDFs
yield little text and fall through to the next converter (the `_detect_scanned` + low-quality gate
catch the residue).

## Supporting reliability / tooling (shipped together)

| Capability | Module | What it does |
|---|---|---|
| Converter-keyed cache | `ingest_source._preferred_pdf_converter` | `inputs/markdown-cache/<sha>.<converter>.md` — installing Docling auto-invalidates MarkItDown entries (no manual purge) |
| Zero-heading gate | `convert_pdf` | WARN at convert time when a multi-page PDF yields 0 headings (flattened/scanned) |
| Deterministic `source_id` | `ingest_source._content_source_id` | `<stem>-<sha8>` (was `<stem>-<timestamp>`) — re-author reuses the id, no orphaning on partial runs |
| Faithfulness anchor guard | `validate_faithfulness_report` | flags free-text `source_anchors` distinctly from missing ids |
| Faithfulness repair | `repair_faithfulness_report` | deterministically quarantines invalid anchors so a flaky report validates without a manual rerun |
| Corpus health | `corpus_health` / `cli corpus-health` | one-shot audit: converter, anchor type/count, tier, claims, dead-refs, health flag |
| Claim-recall harness | `claim_recall` | deterministic token-F1 claim recall/precision for A/B on content, no ML |

## Heading-less floor (no Docling)

When Docling is unavailable, `inject_anchors`' paragraph fallback still recovers real-prose anchors
on a heading-less PDF: it skips conversion noise (running heads, page numbers, pipe/TOC rows) and
sub-chunks the prose at sentence boundaries, so anchors land on body text, not page headers. Docling
is strictly better (semantic heading anchors); the fallback is the floor.

## Status

Implemented + merged. Docling installed CPU-only on the dev machine; it is the active PDF converter.
Corpus migration in progress (re-author empty/flattened packages on Docling) — see
`docs/factory-ops.md`.
