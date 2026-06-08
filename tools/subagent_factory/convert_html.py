"""Convert HTML snapshot to Markdown. Primary: readability + markdownify. Fallback: Pandoc."""

import re
import subprocess
from pathlib import Path


def convert_html(source_path: str | Path, output_path: str | Path) -> dict:
    """
    Convert HTML to Markdown.

    Returns dict: markdown_text, converter_used, warnings, errors, stats
    """
    src = Path(source_path)
    html = src.read_text(encoding="utf-8", errors="replace")
    result = {
        "markdown_text": "",
        "converter_used": None,
        "warnings": [],
        "errors": [],
        "stats": {},
    }

    text, used, warns, errs = _try_readability_markdownify(html)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns
        result["errors"] = errs
        result["markdown_text"] = text
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    text, used, warns, errs = _try_pandoc(src)
    if text:
        result["converter_used"] = used
        result["warnings"] = warns + ["readability pipeline failed; used Pandoc fallback"]
        result["errors"] = errs
        result["markdown_text"] = text
        result["stats"] = _compute_stats(text)
        Path(output_path).write_text(text, encoding="utf-8")
        return result

    result["errors"].append("All HTML converters failed")
    result["converter_used"] = "none"
    return result


def _try_readability_markdownify(html: str):
    try:
        from readability import Document
        from markdownify import markdownify

        doc = Document(html)
        clean_html = doc.summary()
        text = markdownify(clean_html, heading_style="ATX", strip=["a"])
        text = _clean_markdown(text)
        if len(text.strip()) < 50:
            return None, None, [], ["readability extracted too little content"]
        return text, "readability+markdownify", [], []
    except ImportError as e:
        return None, None, [], [f"readability/markdownify not installed: {e}"]
    except Exception as e:
        return None, None, [], [f"readability error: {e}"]


def _try_pandoc(src: Path):
    try:
        proc = subprocess.run(
            ["pandoc", "--from=html", "--to=markdown", "--wrap=none", str(src)],
            capture_output=True, text=True, timeout=60,
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


def _clean_markdown(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


def _compute_stats(text: str) -> dict:
    return {
        "word_count": len(text.split()),
        "heading_count": len(re.findall(r"^#{1,6} ", text, re.MULTILINE)),
        "table_count": len(re.findall(r"^\|", text, re.MULTILINE)) // 2,
        "code_block_count": text.count("```") // 2,
        "figure_count": len(re.findall(r"!\[", text)),
    }
