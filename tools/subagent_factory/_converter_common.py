"""Shared helpers for the document converters (docx / epub / html / pdf).

The per-format ``convert_*`` modules each copied the same Markdown-stats counter, and the
pandoc-based formats (docx, epub) additionally copied an identical pandoc/markitdown attempt pair
plus a result-finalize step. This module is the one place that knowledge lives now; the per-format
modules keep only what genuinely differs (the format string and their orchestration).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package

# Every converter attempt returns (text, converter_used, warnings, errors).
_Attempt = tuple[str | None, str | None, list[str], list[str]]


def compute_stats(text: str) -> dict:
    """Count words/headings/tables/code-blocks/figures in converted Markdown."""
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }


def try_pandoc(src: Path, from_format: str) -> _Attempt:
    """Convert ``src`` from ``from_format`` (e.g. "docx", "epub") to Markdown via pandoc."""
    try:
        proc = subprocess.run(
            ["pandoc", f"--from={from_format}", "--to=markdown", "--wrap=none", str(src)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout, "pandoc", [], []
        return None, None, [], [f"pandoc exit {proc.returncode}: {proc.stderr[:200]}"]
    except FileNotFoundError:
        return None, None, [], ["pandoc not installed"]
    except subprocess.TimeoutExpired:
        return None, None, [], ["pandoc timed out"]
    except Exception as e:
        return None, None, [], [f"pandoc error: {e}"]


def try_markitdown(src: Path, purpose: str) -> _Attempt:
    """Convert ``src`` to Markdown via MarkItDown (self-healed); ``purpose`` names the format."""
    md_mod = ensure_package("markitdown", purpose=purpose)
    if md_mod is None:
        return None, None, [], ["markitdown not installed and could not be auto-installed"]
    try:
        md = md_mod.MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
    except Exception as e:
        return None, None, [], [f"markitdown error: {e}"]


def finalize(
    result: dict[str, Any],
    text: str,
    used: str | None,
    warns: list[str],
    errs: list[str],
    output_path: str | Path,
) -> dict[str, Any]:
    """Fill quality/stats/warnings on ``result``, write ``text`` to ``output_path``, return it."""
    result["converter_used"] = used
    result["errors"] = errs
    result["markdown_text"] = text
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    result["stats"] = compute_stats(text)
    Path(output_path).write_text(text, encoding="utf-8")
    return result
