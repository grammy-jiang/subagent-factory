"""Convert PDF to Markdown. Chain: Docling → MarkItDown (self-heals) → PyMuPDF4LLM/PyMuPDF."""

import importlib.util
import os
import re
from pathlib import Path
from typing import Any, NamedTuple

from tools.subagent_factory._converter_common import compute_stats
from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package
from tools.subagent_factory.table_quality import table_quality


class ConvertAttempt(NamedTuple):
    """Outcome of one converter attempt in the chain.

    ``text`` is None when the converter could not produce output (then ``errors`` carries the
    reason); a non-empty ``text`` means success and ``converter`` names which converter ran.
    """

    text: str | None
    converter: str | None
    warnings: list[str]
    errors: list[str]


# Below this many characters per page, a PDF is likely scanned/image-only (calibrated ~150 chars/page;
# born-digital pages carry far more text). Unit is chars/page — no scaling at the call site.
SCANNED_CHARS_PER_PAGE = 150
_MIN_WORDS_BORN_DIGITAL = 30  # below this, with no page signal, suspect a failed scan
# A multi-page PDF with zero recovered headings is almost certainly a flattened (MarkItDown)
# or scanned conversion: the heading hierarchy the anchor layer needs is gone, so anchoring
# degrades to the paragraph fallback. Warn at convert time rather than discover it downstream.
_MIN_PAGES_FOR_HEADINGS = 5


def preferred_pdf_converter() -> str:
    """Name of the highest-fidelity PDF converter currently importable (the cache discriminator).

    The chain order — Docling > MarkItDown > PyMuPDF — is the same one ``convert_pdf`` runs below;
    ``ingest_source`` keys its markdown cache on this so installing a higher-fidelity converter
    auto-invalidates older lower-fidelity entries. Uses ``find_spec`` so the check never imports
    Docling's heavy ML stack. Returns ``"none"`` when no PDF converter is installed.
    """
    for name, tag in (("docling", "docling"), ("markitdown", "markitdown"), ("fitz", "pymupdf")):
        if importlib.util.find_spec(name) is not None:
            return tag
    return "none"


def convert_pdf(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert PDF to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors,
                  is_scanned, low_quality, quality, page_count, stats
    """
    src = Path(source_path)
    result: dict[str, Any] = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "is_scanned": False,
        "low_quality": False,
        "quality": {},
        "page_count": None,
        "stats": {},
    }

    # Ordered converter chain. Docling (best layout/table fidelity) is the
    # intended primary but is not auto-installed (heavy ML deps). MarkItDown
    # self-heals; PyMuPDF is a pure-extraction last resort. Docling and PyMuPDF
    # are soft deps — enable Docling with `bootstrap --extra convert-full`.
    text: str | None = None
    used: str | None = None
    warns: list[str] = []
    attempt_errors: list[str] = []
    for name, fn in (
        ("docling", _try_docling),
        ("markitdown", _try_markitdown),
        ("pymupdf", _try_pymupdf),
    ):
        attempt = fn(src)
        if attempt.text:
            text, used, warns = attempt.text, attempt.converter, attempt.warnings
            if name != "docling":
                warns = list(warns) + [
                    f"Docling unavailable or failed; used {used} fallback. Enable Docling "
                    "for best layout/table fidelity: `bootstrap --extra convert-full`."
                ]
            break
        attempt_errors += attempt.errors
    else:
        result["errors"] = attempt_errors + ["All PDF converters failed"]
        result["converter_used"] = "none"
        return result

    result["converter_used"] = used
    result["markdown_text"] = text
    _assess_and_enrich(result, text, src, warns)
    Path(output_path).write_text(text, encoding="utf-8")
    return result


def _assess_and_enrich(result: dict, text: str, src: Path, warns: list[str]) -> None:
    """Post-conversion analysis: scanned detection, quality, stats, and heading warning.

    Mutates ``result`` in place — fills ``page_count``, ``is_scanned``, ``quality``,
    ``low_quality``, ``warnings`` (converter warnings + quality/heading warnings), and ``stats``.
    A distinct responsibility from converter-chain selection in ``convert_pdf``.
    """
    page_count = _pdf_page_count(src)
    result["page_count"] = page_count
    result["is_scanned"] = _detect_scanned(text, page_count)
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    stats = compute_stats(text)
    stats["page_count"] = page_count
    result["stats"] = stats
    if page_count and page_count >= _MIN_PAGES_FOR_HEADINGS and stats["heading_count"] == 0:
        result["warnings"].append(
            f"0 headings recovered from a {page_count}-page PDF — flattened or scanned "
            "conversion; structure anchoring degrades to the paragraph fallback. Enable Docling "
            "(bootstrap --extra convert-full) for heading recovery."
        )


def _tables_enabled() -> bool:
    """Whether to run Docling's table-structure model (Step-20 H, table-extraction research).

    Opt-in via ``SUBAGENT_FACTORY_DOCLING_TABLES=1``. Default OFF preserves the fast born-digital
    path (TableFormer dominates CPU). Turn it on for table-heavy sources (finance, data) where the
    ~20x slowdown buys recoverable tabular facts — the measured ~33pp QA gap on table-dependent
    questions. NB: this is increment 1 (run TSR → proper table grids); structure-preserving HTML/OTSL
    export + anchoring table content so claims can cite it is the documented follow-on (the anchor
    layer currently skips pipe-rows).
    """
    return os.environ.get("SUBAGENT_FACTORY_DOCLING_TABLES", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


_PIPE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")


def _export_table_html(table: object, doc: object | None = None) -> str:
    """Render one Docling table to HTML, tolerating both the doc-arg and no-arg signatures."""
    try:
        return table.export_to_html(doc=doc)  # type: ignore[attr-defined]
    except TypeError:
        return table.export_to_html()  # type: ignore[attr-defined]


def _table_warnings(tables: list, doc: object | None = None) -> list[str]:
    """WARN lines for structurally degenerate extracted tables (Step-20 H3, flag-on path only).

    Each table that fails the ``table_quality`` structural-degeneracy heuristic is reported so a
    table-heavy convert can route it to human review. **Advisory only** — never blocks the convert,
    never alters the Markdown. A failure *assessing* a table is itself reported as a warning (not
    silently skipped): the tables that throw are the malformed ones this function exists to surface,
    so swallowing them would invert its purpose.
    """
    warns: list[str] = []
    for i, t in enumerate(tables):
        try:
            q = table_quality(_export_table_html(t, doc))
        except Exception as e:  # noqa: BLE001 — assessment failure is itself a low-confidence signal
            warns.append(
                f"Table {i}: could not assess quality ({type(e).__name__}: {e}) "
                "— review before grounding claims on it."
            )
            continue
        if not q["ok"]:
            warns.append(
                f"Table {i}: low-confidence extraction ({'; '.join(q['reasons'])}) "
                f"[rows={q['rows']} cells={q['cells']}] — review before grounding claims on it."
            )
    return warns


def _tables_to_html(markdown: str, tables: list, doc: object | None = None) -> str:
    """Replace each Markdown pipe-table block with the corresponding table's HTML (Step-20 H, part 2).

    Docling's ``export_to_markdown`` renders recognized tables as pipe-tables, which lose merged cells
    and which ``inject_anchors`` skips as noise. This swaps each contiguous pipe-row block (≥2 lines)
    for ``tables[i].export_to_html()`` — a ``<table>`` block that part 3 anchors and that preserves
    spans. **Order-based + count-guarded:** the i-th pipe block ↔ ``tables[i]`` (both document order);
    extra pipe blocks (or a stray single ``|`` line) pass through unchanged, so a miscount degrades to
    the old behaviour rather than corrupting. ``tables=[]`` (flag off) → returns the markdown verbatim.
    """
    if not tables:
        return markdown
    lines = markdown.splitlines()
    out: list[str] = []
    ti = 0
    i = 0
    while i < len(lines):
        if _PIPE_ROW_RE.match(lines[i]):
            j = i
            while j < len(lines) and _PIPE_ROW_RE.match(lines[j]):
                j += 1
            if (j - i) >= 2 and ti < len(tables):  # a real table block + a table to map it to
                out.append(_export_table_html(tables[ti], doc).strip())
                ti += 1
            else:
                out.extend(lines[i:j])  # single stray pipe line, or no table left → leave as-is
            i = j
        else:
            out.append(lines[i])
            i += 1
    if ti == 0:
        return markdown  # nothing replaced → byte-identical (strong no-op guarantee)
    result = "\n".join(out)
    if markdown.endswith("\n") and not result.endswith("\n"):
        result += "\n"  # splitlines drops the trailing newline; restore it
    return result


def _try_docling(src: Path) -> ConvertAttempt:
    """Docling PDF→Markdown with a born-digital fast path.

    The default ``DocumentConverter`` runs OCR plus the table-structure ML model on every page.
    On a born-digital book PDF (the factory's norm) OCR is dead weight and the table model
    dominates CPU time, pushing a ~100-page convert into tens of minutes on CPU. Disabling both
    keeps the heading hierarchy — the structure the anchor layer actually needs — while cutting
    convert time roughly 20x (≈70s vs tens of minutes). Tables degrade to inline text, which is
    acceptable for the text-dense advisory/reference sources this factory distils. A scanned PDF
    then yields little/no text and falls through to the next converter; ``_detect_scanned`` and
    the low-quality gate catch the residue.

    Table-structure recognition is **opt-in** (``_tables_enabled``): off by default (the fast path
    above), on for table-heavy sources via ``SUBAGENT_FACTORY_DOCLING_TABLES=1``.
    """
    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
    except ImportError:
        return ConvertAttempt(None, None, [], ["docling not installed"])
    tables_on = _tables_enabled()
    # Each try produces ONLY a converted ``doc``: it wraps just converter construction +
    # ``convert(src)``, the part that can fail on a docling API change. Post-processing
    # (``_finish_docling`` — export + table HTML + warnings) runs exactly once, AFTER a converter
    # succeeds and OUTSIDE both try blocks. That keeps the fallback's blast radius scoped to real
    # construction/API failures: a genuine post-processing failure surfaces as itself rather than
    # being misattributed as a construction failure and silently retried on the ~20x slower
    # OCR+table default pipeline (which would fail the same way and mask the real error).
    try:
        opts = PdfPipelineOptions()
        opts.do_ocr = False
        opts.do_table_structure = tables_on
        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
        doc = converter.convert(str(src))
    except Exception as e:
        # Any failure in the fast-path construction (e.g. a docling API change) must not strand
        # the chain — fall back to a default converter before giving up on docling entirely.
        try:
            from docling.document_converter import DocumentConverter

            doc = DocumentConverter().convert(str(src))
        except Exception as e2:
            return ConvertAttempt(None, None, [], [f"docling error: {e}; default-fallback: {e2}"])
    # Post-processing runs once. A failure here is its own error (export / table post-processing),
    # surfaced verbatim and NOT retried on the slow default pipeline — soft-fail, never raise.
    try:
        text, warns = _finish_docling(doc.document, tables_on)
    except Exception as e:
        return ConvertAttempt(None, None, [], [f"docling post-processing error: {e}"])
    return ConvertAttempt(text, "docling", warns, [])


def _finish_docling(document: object, tables_on: bool) -> tuple[str, list[str]]:
    """Export a converted Docling document to Markdown and apply table post-processing once.

    Owns the single table-handling block shared by ``_try_docling``'s fast path and its
    default-converter fallback: export to markdown, then (when ``tables_on``) swap pipe-tables for
    structure-preserving HTML and collect low-confidence-extraction warnings.
    """
    text = document.export_to_markdown()  # type: ignore[attr-defined]
    warns: list[str] = []
    if tables_on:
        tbls = getattr(document, "tables", []) or []
        text = _tables_to_html(text, tbls, doc=document)
        warns = _table_warnings(tbls, doc=document)
    return text, warns


def _try_markitdown(src: Path) -> ConvertAttempt:
    md_mod = ensure_package("markitdown", purpose="PDF conversion")
    if md_mod is None:
        return ConvertAttempt(
            None, None, [], ["markitdown not installed and could not be auto-installed"]
        )
    try:
        md = md_mod.MarkItDown()
        result = md.convert(str(src))
        return ConvertAttempt(result.text_content, "markitdown", [], [])
    except Exception as e:
        return ConvertAttempt(None, None, [], [f"markitdown error: {e}"])


def _try_pymupdf(src: Path) -> ConvertAttempt:
    """Fast PyMuPDF extraction. Prefers ``pymupdf4llm.to_markdown`` (recovers heading
    structure, no ML/OCR wait) and falls back to raw ``fitz`` plain text. Both are soft deps.

    The raw ``get_text()`` path is flat (``headings=0``), which degrades provenance anchoring
    downstream; pymupdf4llm keeps the heading hierarchy, so it is the preferred fast converter
    when Docling is unavailable.
    """
    pymupdf4llm_err: str | None = None
    try:
        import pymupdf4llm
    except ImportError:
        pass
    else:
        try:
            return ConvertAttempt(pymupdf4llm.to_markdown(str(src)), "pymupdf4llm", [], [])
        except Exception as e:
            pymupdf4llm_err = f"pymupdf4llm error: {e}"

    try:
        import fitz  # PyMuPDF
    except ImportError:
        errs = ["pymupdf not installed"]
        return ConvertAttempt(None, None, [], [pymupdf4llm_err] + errs if pymupdf4llm_err else errs)
    try:
        with fitz.open(str(src)) as doc:
            text = "\n\n".join(page.get_text() for page in doc)
        return ConvertAttempt(text, "pymupdf", [], [pymupdf4llm_err] if pymupdf4llm_err else [])
    except Exception as e:
        errs = [f"pymupdf error: {e}"]
        return ConvertAttempt(None, None, [], [pymupdf4llm_err] + errs if pymupdf4llm_err else errs)


def _pdf_page_count(src: Path) -> int | None:
    """Real page count straight from the PDF page tree (converter-agnostic).

    Uses pdfminer when available — a soft dependency that MarkItDown's PDF path
    already pulls in, so it is present exactly on the fallback path that needs it.
    Returns None when pdfminer is absent or the PDF cannot be parsed.
    """
    try:
        from pdfminer.pdfpage import PDFPage
    except ImportError:
        return None
    try:
        with open(src, "rb") as fh:
            return sum(1 for _ in PDFPage.get_pages(fh)) or None
    except Exception:
        return None


def _detect_scanned(text: str, page_count: int | None = None) -> bool:
    """Detect a scanned/image-only PDF independent of which converter ran.

    Density signal, in priority order:
      1. real page count from the PDF (works for any converter),
      2. Docling's ``<!-- page N -->`` markers if no count is available,
      3. no page signal at all → flag only near-empty extraction as a suspected scan.
    """
    if not text or not text.strip():
        return True
    pages = page_count
    if not pages:
        markers = len(re.findall(r"<!-- page \d+", text, re.IGNORECASE))
        pages = markers or None
    if not pages:
        return len(text.split()) < _MIN_WORDS_BORN_DIGITAL
    chars_per_page = len(text) / pages
    return chars_per_page < SCANNED_CHARS_PER_PAGE
