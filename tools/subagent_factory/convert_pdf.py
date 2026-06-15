"""Convert PDF to Markdown. Chain: Docling → MarkItDown (self-heals) → PyMuPDF."""

import os
import re
from pathlib import Path
from typing import Any

from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package
from tools.subagent_factory.table_quality import table_quality

SCANNED_THRESHOLD = 0.15  # chars-per-page (×1000) below this suggests scanned
_MIN_WORDS_BORN_DIGITAL = 30  # below this, with no page signal, suspect a failed scan
# A multi-page PDF with zero recovered headings is almost certainly a flattened (MarkItDown)
# or scanned conversion: the heading hierarchy the anchor layer needs is gone, so anchoring
# degrades to the paragraph fallback. Warn at convert time rather than discover it downstream.
_MIN_PAGES_FOR_HEADINGS = 5


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
        t, u, w, e = fn(src)
        if t:
            text, used, warns = t, u, w
            if name != "docling":
                warns = list(warns) + [
                    f"Docling unavailable or failed; used {u} fallback. Enable Docling "
                    "for best layout/table fidelity: `bootstrap --extra convert-full`."
                ]
            break
        attempt_errors += e
    else:
        result["errors"] = attempt_errors + ["All PDF converters failed"]
        result["converter_used"] = "none"
        return result

    result["converter_used"] = used
    result["markdown_text"] = text
    page_count = _pdf_page_count(src)
    result["page_count"] = page_count
    result["is_scanned"] = _detect_scanned(text, page_count)
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    stats = _compute_stats(text)
    stats["page_count"] = page_count
    result["stats"] = stats
    if page_count and page_count >= _MIN_PAGES_FOR_HEADINGS and stats["heading_count"] == 0:
        result["warnings"].append(
            f"0 headings recovered from a {page_count}-page PDF — flattened or scanned "
            "conversion; structure anchoring degrades to the paragraph fallback. Enable Docling "
            "(bootstrap --extra convert-full) for heading recovery."
        )
    Path(output_path).write_text(text, encoding="utf-8")
    return result


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
    never alters the Markdown. Any failure assessing a table is swallowed so quality scoring can
    never break an otherwise-successful conversion.
    """
    warns: list[str] = []
    for i, t in enumerate(tables):
        try:
            q = table_quality(_export_table_html(t, doc))
        except Exception:
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


def _try_docling(src: Path):
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
        return None, None, [], ["docling not installed"]
    try:
        opts = PdfPipelineOptions()
        opts.do_ocr = False
        opts.do_table_structure = _tables_enabled()
        converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
        doc = converter.convert(str(src))
        text = doc.document.export_to_markdown()
        warns: list[str] = []
        if _tables_enabled():
            tbls = getattr(doc.document, "tables", []) or []
            text = _tables_to_html(text, tbls, doc=doc.document)
            warns = _table_warnings(tbls, doc=doc.document)
        return text, "docling", warns, []
    except Exception as e:
        # Any failure in the fast-path construction (e.g. a docling API change) must not strand
        # the chain — fall back to a default converter before giving up on docling entirely.
        try:
            from docling.document_converter import DocumentConverter

            doc = DocumentConverter().convert(str(src))
            text = doc.document.export_to_markdown()
            warns = []
            if _tables_enabled():
                tbls = getattr(doc.document, "tables", []) or []
                text = _tables_to_html(text, tbls, doc=doc.document)
                warns = _table_warnings(tbls, doc=doc.document)
            return text, "docling", warns, []
        except Exception as e2:
            return None, None, [], [f"docling error: {e}; default-fallback: {e2}"]


def _try_markitdown(src: Path):
    md_mod = ensure_package("markitdown", purpose="PDF conversion")
    if md_mod is None:
        return None, None, [], ["markitdown not installed and could not be auto-installed"]
    try:
        md = md_mod.MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
    except Exception as e:
        return None, None, [], [f"markitdown error: {e}"]


def _try_pymupdf(src: Path):
    """Last-resort plain-text extraction (PyMuPDF / fitz). Optional soft dep."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None, None, [], ["pymupdf not installed"]
    try:
        with fitz.open(str(src)) as doc:
            text = "\n\n".join(page.get_text() for page in doc)
        return text, "pymupdf", [], []
    except Exception as e:
        return None, None, [], [f"pymupdf error: {e}"]


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
    return chars_per_page < SCANNED_THRESHOLD * 1000


def _compute_stats(text: str) -> dict:
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }
