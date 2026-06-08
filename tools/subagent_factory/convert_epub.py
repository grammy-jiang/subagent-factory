"""Convert ePUB to Markdown. Primary: Pandoc. Fallback: MarkItDown (self-healed)."""

import re
import subprocess
from pathlib import Path

from tools.subagent_factory.conversion_quality import assess_quality
from tools.subagent_factory.self_heal import ensure_package


def convert_epub(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert ePUB to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors,
                  low_quality, quality, stats
    """
    src = Path(source_path)
    result = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "low_quality": False,
        "quality": {},
        "stats": {},
    }

    text, used, warns, errs = _try_pandoc(src)
    if not text:
        text2, used2, warns2, errs2 = _try_markitdown(src)
        if text2:
            text, used = text2, used2
            warns = warns2 + ["Pandoc unavailable or failed; used MarkItDown fallback"]
            errs = errs2
        else:
            result["errors"] = errs + errs2
            result["errors"].append("All ePUB converters failed")
            result["converter_used"] = "none"
            return result

    return _finalize(result, text, used, warns, errs, output_path)


def _finalize(result, text, used, warns, errs, output_path):
    result["converter_used"] = used
    result["errors"] = errs
    result["markdown_text"] = text
    quality = assess_quality(text)
    result["quality"] = quality
    result["low_quality"] = quality["low_quality"]
    result["warnings"] = warns + [f"Low conversion quality: {r}" for r in quality["reasons"]]
    result["stats"] = _compute_stats(text)
    Path(output_path).write_text(text, encoding="utf-8")
    return result


def _try_pandoc(src: Path):
    try:
        proc = subprocess.run(
            ["pandoc", "--from=epub", "--to=markdown", "--wrap=none", str(src)],
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
    md_mod = ensure_package("markitdown", purpose="ePUB conversion")
    if md_mod is None:
        return None, None, [], ["markitdown not installed and could not be auto-installed"]
    try:
        md = md_mod.MarkItDown()
        result = md.convert(str(src))
        return result.text_content, "markitdown", [], []
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
