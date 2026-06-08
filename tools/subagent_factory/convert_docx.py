"""Convert DOCX to Markdown. Primary: Pandoc. Fallback: MarkItDown."""

import re
import subprocess
from pathlib import Path


def convert_docx(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert DOCX to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors, stats
    """
    src = Path(source_path)
    result = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "stats": {},
    }

    text, used, warns, errs = _try_pandoc(src)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns
        result["errors"] = errs
        result["markdown_text"] = text
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    text, used, warns, errs = _try_markitdown(src)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns + ["Pandoc unavailable or failed; used MarkItDown fallback"]
        result["errors"] = errs
        result["markdown_text"] = text
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    result["errors"].append("All DOCX converters failed")
    result["converter_used"] = "none"
    return result


def _try_pandoc(src: Path):
    try:
        proc = subprocess.run(
            ["pandoc", "--from=docx", "--to=markdown", "--wrap=none", str(src)],
            capture_output=True, text=True, timeout=120,
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


def _try_markitdown(src: Path):
    try:
        from markitdown import MarkItDown

        md = MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
    except ImportError:
        return None, None, [], ["markitdown not installed"]
    except Exception as e:
        return None, None, [], [f"markitdown error: {e}"]


def _compute_stats(text: str) -> dict:
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }
