"""Detect file type from extension and/or magic bytes."""

import mimetypes
from pathlib import Path

EXTENSION_MAP = {
    ".pdf": "pdf",
    ".epub": "epub",
    ".docx": "docx",
    ".doc": "docx",
    ".md": "markdown",
    ".markdown": "markdown",
    ".mdown": "markdown",
    ".txt": "markdown",
    ".html": "html",
    ".htm": "html",
    ".xhtml": "html",
}

PDF_MAGIC = b"%PDF"
# epub and docx are both ZIP containers → identical local-file-header magic
ZIP_MAGIC = b"PK\x03\x04"


def detect_file_type(path: str | Path) -> str:
    """Return canonical file type string or 'unknown'."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext in EXTENSION_MAP:
        candidate = EXTENSION_MAP[ext]
        if candidate == "docx" and ext == ".docx":
            return "docx"
        if candidate in ("epub", "docx"):
            magic = _read_magic(p, 4)
            if magic[:4] == ZIP_MAGIC:
                return candidate
        return candidate

    magic = _read_magic(p, 4)
    if magic[:4] == PDF_MAGIC:
        return "pdf"
    if magic[:4] == ZIP_MAGIC:
        mime, _ = mimetypes.guess_type(str(p))
        if mime and "epub" in mime:
            return "epub"
        return "zip-unknown"

    return "unknown"


def _read_magic(path: Path, n: int) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read(n)
    except OSError:
        return b""
