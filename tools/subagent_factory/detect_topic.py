"""
Extract a human-readable topic string from a source file when --topic is not supplied.

Priority order per file type:
  Markdown  → front matter title → first H1 → cleaned filename
  PDF       → Docling/PyMuPDF document title metadata → first H1 in converted text → filename
  ePUB      → OPF dc:title → filename
  DOCX      → core.xml dc:title → filename
  HTML      → <title> tag → first <h1> → filename
  URL       → same as HTML after snapshot
  fallback  → clean up filename stem
"""

import re
import zipfile
from pathlib import Path

import yaml

from tools.subagent_factory.detect_file_type import detect_file_type


def detect_topic(source_path: str | Path) -> str:
    """Return best-guess topic string for a source file."""
    p = Path(source_path)
    if not p.exists():
        return _from_filename(p)

    file_type = detect_file_type(p)

    extractors = {
        "markdown": _topic_markdown,
        "pdf":      _topic_pdf,
        "epub":     _topic_epub,
        "docx":     _topic_docx,
        "html":     _topic_html,
    }

    topic = extractors.get(file_type, lambda _: None)(p)
    return topic or _from_filename(p)


# ── per-type extractors ────────────────────────────────────────────────────

def _topic_markdown(p: Path) -> str | None:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
        # front matter title
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                fm = yaml.safe_load(text[3:end]) or {}
                title = fm.get("title") or fm.get("name")
                if title:
                    return str(title).strip()
        # first H1
        m = re.search(r"^# (.+)$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None


def _topic_pdf(p: Path) -> str | None:
    # Try Docling metadata
    try:
        from docling.document_converter import DocumentConverter
        conv = DocumentConverter()
        doc = conv.convert(str(p))
        title = getattr(doc.document, "title", None)
        if title:
            return str(title).strip()
        # fall through to first heading in converted text
        text = doc.document.export_to_markdown()
        m = re.search(r"^# (.+)$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    # Try PyMuPDF
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(p))
        meta = doc.metadata or {}
        title = meta.get("title", "").strip()
        if title:
            return title
    except Exception:
        pass
    return None


def _topic_epub(p: Path) -> str | None:
    try:
        with zipfile.ZipFile(p, "r") as zf:
            # Find OPF file
            container = zf.read("META-INF/container.xml").decode("utf-8", errors="replace")
            m = re.search(r'full-path="([^"]+\.opf)"', container)
            if not m:
                return None
            opf_path = m.group(1)
            opf = zf.read(opf_path).decode("utf-8", errors="replace")
            title_m = re.search(r"<dc:title[^>]*>([^<]+)</dc:title>", opf)
            if title_m:
                return title_m.group(1).strip()
    except Exception:
        pass
    return None


def _topic_docx(p: Path) -> str | None:
    try:
        with zipfile.ZipFile(p, "r") as zf:
            if "docProps/core.xml" in zf.namelist():
                core = zf.read("docProps/core.xml").decode("utf-8", errors="replace")
                m = re.search(r"<dc:title>([^<]+)</dc:title>", core)
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return None


def _topic_html(p: Path) -> str | None:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<title[^>]*>([^<]+)</title>", text, re.IGNORECASE)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            if title:
                return title
        m = re.search(r"<h1[^>]*>([^<]+)</h1>", text, re.IGNORECASE)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()
    except Exception:
        pass
    return None


# ── fallback ───────────────────────────────────────────────────────────────

def _from_filename(p: Path) -> str:
    stem = p.stem
    stem = re.sub(r"[_\-]+", " ", stem)
    stem = re.sub(r"\bv\d+(\.\d+)*\b", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.title()


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    print(detect_topic(sys.argv[1]))
