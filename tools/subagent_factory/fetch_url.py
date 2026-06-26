"""Fetch public URLs and preserve snapshots.

SSRF posture: the scheme is restricted to http/https and the resolved host address is checked
against private/loopback/link-local/reserved ranges (incl. the cloud-metadata IP) up front and on
every redirect hop. ACCEPTED RESIDUAL: this validates a DNS resolution that requests.get does NOT
reuse — a rebinding attacker (short-TTL host that resolves public for the check, internal for the
connect) can still bypass it. Closing that needs pinning the connection to the validated IP (with
Host header + TLS SNI via a custom adapter); deferred as out of scope for local-dev tooling where
the operator picks the URL. Do not feed fetch_url URLs from an untrusted queue until pinned.
"""

import hashlib
import ipaddress
import re
import socket
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

TIMEOUT = 30
MAX_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_REDIRECTS = 5
USER_AGENT = "subagent-factory/0.1.0 (research-tool)"
_ALLOWED_SCHEMES = {"http", "https"}


def _ip_is_blocked(ip: str) -> bool:
    """True if an IP is in a range we must never fetch from (SSRF guard)."""
    try:
        addr: ipaddress.IPv4Address | ipaddress.IPv6Address = ipaddress.ip_address(ip)
    except ValueError:
        return True  # unparseable → refuse
    # Unwrap IPv4-in-IPv6 forms before classifying: an IPv6Address wrapping an internal IPv4
    # (::ffff:127.0.0.1, a 6to4/Teredo address) is the embedded address's range, but older
    # ipaddress versions don't inspect the embedded v4 in is_loopback/is_private. Classify the
    # unwrapped v4 so the guard is correct regardless of CPython version.
    if isinstance(addr, ipaddress.IPv6Address):
        teredo = addr.teredo  # (server, client) or None
        embedded = addr.ipv4_mapped or addr.sixtofour or (teredo[1] if teredo else None)
        if embedded is not None:
            addr = embedded
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local  # 169.254.0.0/16 — incl. cloud metadata 169.254.169.254
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def _url_safety_error(url: str) -> str | None:
    """Return an SSRF-reason string if ``url`` must not be fetched, else None.

    Restricts the scheme to http/https (rejects file://, ftp://, gopher://, …) and resolves the
    host, refusing if ANY resolved address is private/loopback/link-local/reserved — so a URL
    cannot reach localhost, RFC1918 hosts, or the cloud-metadata endpoint (169.254.169.254). This
    is re-checked on every redirect hop, since a public URL can 30x-redirect to an internal target.
    """
    parsed = urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        return f"scheme '{parsed.scheme}' not allowed (only http/https)"
    host = parsed.hostname
    if not host:
        return "no host in URL"
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError as e:
        return f"DNS resolution failed: {e}"
    for info in infos:
        ip = str(info[4][0])
        if _ip_is_blocked(ip):
            return f"host {host} resolves to a blocked address ({ip})"
    return None


AUTH_PATTERNS = [
    r"login",
    r"sign[_-]?in",
    r"auth",
    r"oauth",
    r"sso",
    r"accounts\.",
    r"id\.",
    r"passport",
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

    # SSRF guard: validate the input URL's scheme + resolved address before any request.
    safety = _url_safety_error(url)
    if safety:
        result["error"] = f"refused unsafe URL: {safety}"
        return result

    try:
        # Follow redirects MANUALLY (allow_redirects=False) so each hop's resolved address is
        # re-validated — a public URL can 30x-redirect to an internal target, which auto-redirect
        # would fetch before any check.
        current = url
        resp = None
        for _ in range(MAX_REDIRECTS + 1):
            resp = requests.get(
                current,
                timeout=TIMEOUT,
                headers={"User-Agent": USER_AGENT},
                stream=True,
                allow_redirects=False,
            )
            if resp.is_redirect or resp.is_permanent_redirect:
                nxt = resp.headers.get("location")
                if not nxt:
                    break
                nxt = requests.compat.urljoin(current, nxt)
                hop_unsafe = _url_safety_error(nxt)
                if hop_unsafe:
                    resp.close()
                    result["error"] = f"refused unsafe redirect: {hop_unsafe}"
                    return result
                resp.close()
                current = nxt
                continue
            break
        else:
            result["error"] = f"too many redirects (> {MAX_REDIRECTS})"
            return result

        # Always release the terminal streamed response (the manual-redirect loop already closes
        # intermediate hops; auto-redirect mode used to close them for us).
        try:
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

            # Reject early on a declared oversize body (Content-Length can lie, so the streaming
            # tally below remains the authoritative cap).
            clen = resp.headers.get("content-length")
            if clen and clen.isdigit() and int(clen) > MAX_SIZE:
                result["error"] = f"Response Content-Length {clen} exceeds {MAX_SIZE} bytes limit"
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
        finally:
            resp.close()

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
