"""Fetch public URLs and preserve snapshots."""

import hashlib
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


TIMEOUT = 30
MAX_SIZE = 50 * 1024 * 1024  # 50 MB
USER_AGENT = "subagent-factory/0.1.0 (research-tool)"

AUTH_PATTERNS = [
    r"login", r"sign[_-]?in", r"auth", r"oauth", r"sso",
    r"accounts\.", r"id\.", r"passport",
]
AUTH_RE = re.compile("|".join(AUTH_PATTERNS), re.IGNORECASE)


def fetch_url(url: str, dest_dir: str | Path) -> dict:
    """
    Fetch a public URL and save snapshot to dest_dir.

    Returns dict with keys:
      local_path, content_type, final_url, sha256, needs_auth, error
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    result = {
        "url": url,
        "local_path": None,
        "content_type": None,
        "final_url": url,
        "sha256": None,
        "needs_auth": False,
        "error": None,
    }

    try:
        resp = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            stream=True,
            allow_redirects=True,
        )
        result["final_url"] = resp.url

        if resp.status_code in (401, 403):
            result["needs_auth"] = True
            result["error"] = f"HTTP {resp.status_code} — authentication required"
            return result

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        if AUTH_RE.search(resp.url):
            result["needs_auth"] = True
            result["error"] = "Redirected to login page"
            return result

        content_type = resp.headers.get("content-type", "").split(";")[0].strip()
        result["content_type"] = content_type

        ext = _guess_extension(content_type, resp.url)
        filename = _url_to_filename(url) + ext
        local_path = dest / filename

        data = b""
        for chunk in resp.iter_content(chunk_size=65536):
            data += chunk
            if len(data) > MAX_SIZE:
                result["error"] = f"Response exceeds {MAX_SIZE} bytes limit"
                return result

        local_path.write_bytes(data)
        result["local_path"] = str(local_path)
        result["sha256"] = hashlib.sha256(data).hexdigest()

    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection error: {e}"
    except requests.exceptions.Timeout:
        result["error"] = "Request timed out"
    except Exception as e:
        result["error"] = str(e)

    return result


def _url_to_filename(url: str) -> str:
    parsed = urlparse(url)
    base = parsed.netloc + parsed.path
    base = re.sub(r"[^\w\-.]", "_", base)[:80]
    ts = str(int(time.time()))
    return f"snapshot_{ts}_{base}"


def _guess_extension(content_type: str, url: str) -> str:
    ct_map = {
        "application/pdf": ".pdf",
        "application/epub+zip": ".epub",
        "text/html": ".html",
        "application/xhtml+xml": ".html",
    }
    if content_type in ct_map:
        return ct_map[content_type]
    if url.lower().endswith(".pdf"):
        return ".pdf"
    if url.lower().endswith(".epub"):
        return ".epub"
    return ".html"
