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
import json
import os
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

# URL snapshot cache (item #1, leg C). A PREFETCH step fetches source URLs over the network and
# populates this cache; the network-denied author session's in-session ingest then reads the cache
# instead of fetching, so the session needs no egress. Content-addressed by sha256(url) because the
# snapshot filename is timestamped (not stable). Populated as a side effect of any online fetch that
# is given a cache_dir; served (never re-fetched) when offline. Default location is repo-local and
# gitignored; it holds only bytes the operator already chose to fetch.
DEFAULT_URL_CACHE = Path(__file__).resolve().parents[2] / "inputs" / "url-cache"


def cache_config_from_env() -> tuple[Path | None, bool]:
    """Resolve (cache_dir, offline) from the environment.

    - ``SUBAGENT_FACTORY_OFFLINE`` truthy → offline: serve URL fetches from cache, never touch the
      network (a cache miss is a hard error, not a live fetch).
    - ``SUBAGENT_FACTORY_URL_CACHE`` → explicit cache dir; defaults to ``DEFAULT_URL_CACHE`` when
      offline is on but the path is unset.
    - Neither set → ``(None, False)``: caching is OFF and ``fetch_url`` behaves exactly as before
      (opt-in, so ordinary runs are unchanged).
    """
    raw = os.environ.get("SUBAGENT_FACTORY_URL_CACHE", "").strip()
    offline = os.environ.get("SUBAGENT_FACTORY_OFFLINE", "").strip().lower() not in (
        "",
        "0",
        "false",
        "no",
    )
    if raw:
        return Path(raw), offline
    if offline:
        return DEFAULT_URL_CACHE, offline
    return None, offline


def _cache_paths(cache_dir: Path, url: str) -> tuple[Path, Path]:
    """(blob, meta) cache paths for a URL, keyed by sha256(url)."""
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return cache_dir / f"{key}.snapshot", cache_dir / f"{key}.json"


def _serve_from_cache(url: str, dest: Path, cache_dir: Path, result: dict) -> dict | None:
    """Write the cached snapshot for ``url`` into ``dest`` and fill ``result``; None on cache miss.

    No network and no SSRF re-check: the cache is only ever populated by an online fetch that already
    passed the SSRF guard, so serving cached bytes cannot reach a new host.
    """
    blob, meta_p = _cache_paths(cache_dir, url)
    if not (blob.exists() and meta_p.exists()):
        return None
    try:
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    data = blob.read_bytes()
    local_path = dest / (_url_to_filename(url) + meta.get("ext", ".html"))
    local_path.write_bytes(data)
    result["local_path"] = str(local_path)
    result["content_type"] = meta.get("content_type")
    result["final_url"] = meta.get("final_url", url)
    result["sha256"] = meta.get("sha256") or hashlib.sha256(data).hexdigest()
    return result


def _populate_cache(
    url: str, data: bytes, ext: str, content_type: str | None, final_url: str, cache_dir: Path
) -> None:
    """Store a fetched snapshot in the cache so a later offline session can serve it (best effort)."""
    blob, meta_p = _cache_paths(cache_dir, url)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        blob.write_bytes(data)
        meta_p.write_text(
            json.dumps(
                {
                    "url": url,
                    "final_url": final_url,
                    "content_type": content_type,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "ext": ext,
                }
            ),
            encoding="utf-8",
        )
    except OSError:
        pass  # a cache-write failure must not fail the fetch itself


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


def fetch_url(
    url: str,
    dest_dir: str | Path,
    *,
    cache_dir: str | Path | None = None,
    offline: bool = False,
) -> dict:
    """
    Fetch a public URL and save snapshot to dest_dir.

    Returns dict with keys:
      local_path, content_type, final_url, sha256, needs_auth, error

    ``cache_dir`` (opt-in) — after a successful online fetch the snapshot is also stored here, keyed
    by sha256(url), so a later ``offline`` call can serve it without the network.
    ``offline`` — never touch the network: serve the snapshot from ``cache_dir`` if present, else
    fail closed with an error (a cache miss is NOT a live fetch). Used to run the network-denied
    author session after a prefetch has warmed the cache.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    cache = Path(cache_dir) if cache_dir else None

    result = {
        "url": url,
        "local_path": None,
        "content_type": None,
        "final_url": url,
        "sha256": None,
        "needs_auth": False,
        "error": None,
    }

    # Offline: serve from cache or fail closed — NO network, not even DNS (the SSRF guard resolves
    # the host, which offline mode must also avoid).
    if offline:
        served = _serve_from_cache(url, dest, cache, result) if cache else None
        if served is None:
            result["error"] = (
                "offline mode (SUBAGENT_FACTORY_OFFLINE): URL not in prefetch cache — run the "
                "prefetch step before the network-denied session"
            )
        return result

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
            if cache is not None:
                _populate_cache(url, data, ext, content_type, resp.url, cache)
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
