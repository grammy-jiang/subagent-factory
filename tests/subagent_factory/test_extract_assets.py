"""Coverage for extract_assets: base64 data-URI extraction + Markdown rewrite (was untested).

The ingestion pipeline runs every converted source through this, so a regression silently corrupts a
document's embedded images. These pin the four behaviours: a known image extracts to a correctly
named file with the Markdown rewritten to the relative path; an unknown MIME falls back to .bin;
corrupt base64 is left in place and never raises; and a doc with no data-URIs is passed through.
"""

import base64

from tools.subagent_factory.extract_assets import extract_assets

_PNG = base64.b64encode(b"\x89PNG\r\n\x1a\nfake-image-bytes").decode()


def _md(tmp_path, text):
    p = tmp_path / "in.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_png_data_uri_extracted_and_rewritten(tmp_path):
    src = _md(tmp_path, f"# Doc\n\n![logo](data:image/png;base64,{_PNG})\n\ntail\n")
    assets = tmp_path / "assets"
    r = extract_assets(src, assets, "src1")

    assert r["asset_count"] == 1
    out_file = assets / "src1-asset-0000.png"
    assert out_file.exists()
    assert out_file.read_bytes() == base64.b64decode(_PNG)  # bytes decoded correctly
    # Markdown rewritten to the relative reference; the inline data-URI is gone.
    assert "![logo](../assets/src1/src1-asset-0000.png)" in r["updated_markdown_text"]
    assert "data:image/png;base64" not in r["updated_markdown_text"]


def test_unknown_mime_falls_back_to_bin(tmp_path):
    src = _md(tmp_path, f"![x](data:application/x-weird;base64,{_PNG})\n")
    assets = tmp_path / "assets"
    r = extract_assets(src, assets, "src1")
    assert r["asset_count"] == 1
    assert (assets / "src1-asset-0000.bin").exists()  # unknown MIME → .bin


def test_corrupt_base64_left_in_place_no_raise(tmp_path):
    src = _md(tmp_path, "![bad](data:image/png;base64,!!!not-base64!!!)\n")
    assets = tmp_path / "assets"
    r = extract_assets(src, assets, "src1")  # must not raise
    # The undecodable data-URI is left untouched, and no asset file was written for it.
    assert "data:image/png;base64,!!!not-base64!!!" in r["updated_markdown_text"]
    assert not any(assets.glob("src1-asset-*"))


def test_no_data_uris_is_passthrough(tmp_path):
    body = "# Doc\n\n![kept](../assets/existing.png)\n\njust text\n"
    src = _md(tmp_path, body)
    assets = tmp_path / "assets"
    r = extract_assets(src, assets, "src1")
    assert r["asset_count"] == 0
    assert r["updated_markdown_text"] == body  # unchanged
    assert not any(assets.glob("src1-asset-*"))  # nothing written
