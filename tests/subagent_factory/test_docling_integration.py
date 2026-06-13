"""End-to-end Docling integration test (Step 20): real PDF -> headings via the fast path.

Skipped when docling is not installed (the light `convert` profile / CI without `convert-full`),
so it never breaks the default suite. When present, it guards the load-bearing §20 property:
Docling recovers heading structure that MarkItDown flattens away, and convert_pdf selects it.
"""

import re

import pytest

pytest.importorskip("docling")

import tools.subagent_factory.convert_pdf as cp  # noqa: E402


def _minimal_pdf(lines: list[tuple[int, int, str]]) -> bytes:
    """Build a one-page PDF (correct xref offsets) with absolutely-positioned text runs.

    ``lines`` is ``(font_size, y, text)``; a larger font size is what Docling reads as a heading.
    """
    content = b"BT\n"
    for fs, y, t in lines:
        content += f"/F1 {fs} Tf 1 0 0 1 72 {y} Tm ({t}) Tj\n".encode()
    content += b"ET"
    objs = [
        b"<</Type/Catalog/Pages 2 0 R>>",
        b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
        b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R"
        b"/Resources<</Font<</F1 5 0 R>>>>>>",
        f"<</Length {len(content)}>>\nstream\n".encode() + content + b"\nendstream",
        b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<</Size {len(objs) + 1}/Root 1 0 R>>\nstartxref\n{xref}\n%%EOF".encode()
    return out


def test_docling_recovers_headings_end_to_end(tmp_path):
    src = tmp_path / "doc.pdf"
    src.write_bytes(
        _minimal_pdf(
            [
                (24, 700, "Chapter One Caching Basics"),  # big font -> heading
                (11, 660, "This is body paragraph text about cache invalidation strategy."),
            ]
        )
    )
    out = tmp_path / "out.md"
    result = cp.convert_pdf(src, out)

    assert result["converter_used"] == "docling"
    assert result["stats"]["heading_count"] >= 1  # the §20 win: structure recovered
    body = out.read_text(encoding="utf-8")
    assert re.search(r"^#{1,6} .*Caching Basics", body, re.M)
    assert "cache invalidation" in body
    # headings present -> the zero-heading degradation warning must not fire
    assert not any("0 headings recovered" in w for w in result["warnings"])
