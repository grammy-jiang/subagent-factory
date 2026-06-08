"""Extract embedded assets from Markdown and copy to assets directory."""

import base64
import re
from pathlib import Path

DATA_URI_RE = re.compile(
    r"!\[([^\]]*)\]\(data:([^;]+);base64,([^)]+)\)",
    re.DOTALL,
)
FILE_REF_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

MIME_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}


def extract_assets(
    markdown_path: str | Path,
    assets_dir: str | Path,
    source_id: str,
) -> dict:
    """
    Extract base64 data URIs from Markdown, write them as files in assets_dir.
    Update Markdown to use relative file references.

    Returns dict: asset_count, updated_markdown_text
    """
    src = Path(markdown_path)
    assets = Path(assets_dir)
    assets.mkdir(parents=True, exist_ok=True)

    text = src.read_text(encoding="utf-8")
    asset_count = 0
    asset_map = {}

    def replace_data_uri(m: re.Match) -> str:
        nonlocal asset_count
        alt = m.group(1)
        mime = m.group(2)
        b64 = m.group(3).strip()
        ext = MIME_EXT.get(mime, ".bin")
        filename = f"{source_id}-asset-{asset_count:04d}{ext}"
        asset_count += 1
        asset_path = assets / filename
        try:
            asset_path.write_bytes(base64.b64decode(b64))
        except Exception:
            return m.group(0)
        rel_path = f"../assets/{source_id}/{filename}"
        asset_map[filename] = str(asset_path)
        return f"![{alt}]({rel_path})"

    updated = DATA_URI_RE.sub(replace_data_uri, text)

    if updated != text:
        src.write_text(updated, encoding="utf-8")

    return {
        "asset_count": asset_count,
        "updated_markdown_text": updated,
        "assets": list(asset_map.keys()),
    }
