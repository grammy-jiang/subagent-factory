"""URL snapshot cache + offline mode (item #1, leg C) and the prefetch warmer.

The author session runs network-denied; URL sources are prefetched into a cache before it, and its
in-session ingest serves them offline. These tests pin: online fetch populates the cache; offline
serves from it with NO network; an offline cache miss fails closed (no live fetch, not even DNS); the
cache never bypasses the SSRF guard; and env config is opt-in (unset → unchanged behaviour).
"""

from pathlib import Path

import tools.subagent_factory.fetch_url as fu
import tools.subagent_factory.prefetch_url_sources as pf
from tools.subagent_factory.fetch_url import DEFAULT_URL_CACHE, cache_config_from_env, fetch_url


class _Resp:
    """Minimal stand-in for a streamed requests.Response (non-redirect 200)."""

    def __init__(self, body=b"<html>body</html>", url="http://example.com/x", ctype="text/html"):
        self._body = body
        self.status_code = 200
        self.url = url
        self.headers = {"content-type": ctype}

    is_redirect = False
    is_permanent_redirect = False

    def iter_content(self, chunk_size=65536):
        yield self._body

    def close(self):
        pass


def _mock_ok(monkeypatch, body=b"BODY", url="http://example.com/x"):
    """Make an online fetch succeed without touching the network or DNS."""
    monkeypatch.setattr(fu, "_url_safety_error", lambda u: None)  # skip real DNS
    monkeypatch.setattr(fu.requests, "get", lambda *a, **k: _Resp(body=body, url=url))


def _no_network(monkeypatch):
    """Any network or DNS use is a hard failure (asserts offline really is offline)."""

    def _boom(*a, **k):
        raise AssertionError("network/DNS used in offline mode")

    monkeypatch.setattr(fu.requests, "get", _boom)
    monkeypatch.setattr(fu.socket, "getaddrinfo", _boom)


def test_online_populates_cache_then_offline_serves(monkeypatch, tmp_path):
    cache = tmp_path / "cache"
    _mock_ok(monkeypatch, body=b"HELLO")
    r = fetch_url("http://example.com/x", tmp_path / "snap", cache_dir=cache)
    assert r["error"] is None
    assert Path(r["local_path"]).read_bytes() == b"HELLO"
    blob, meta = fu._cache_paths(cache, "http://example.com/x")
    assert blob.exists() and meta.exists()  # cache warmed

    # Offline serve: no network available at all — must come from the cache.
    _no_network(monkeypatch)
    r2 = fetch_url("http://example.com/x", tmp_path / "snap2", cache_dir=cache, offline=True)
    assert r2["error"] is None
    assert Path(r2["local_path"]).read_bytes() == b"HELLO"
    assert r2["sha256"] == r["sha256"]


def test_offline_cache_miss_fails_closed_no_network(monkeypatch, tmp_path):
    _no_network(monkeypatch)
    r = fetch_url(
        "http://example.com/missing", tmp_path / "d", cache_dir=tmp_path / "cache", offline=True
    )
    assert r["local_path"] is None
    assert "offline" in r["error"].lower()


def test_offline_without_cache_dir_fails_closed(monkeypatch, tmp_path):
    _no_network(monkeypatch)
    r = fetch_url("http://example.com/x", tmp_path / "d", offline=True)  # no cache_dir
    assert r["local_path"] is None and "offline" in r["error"].lower()


def test_cache_does_not_bypass_ssrf(tmp_path):
    # Online with a cache dir must still refuse an internal target (real SSRF guard, no egress).
    r = fetch_url("http://127.0.0.1/x", tmp_path / "d", cache_dir=tmp_path / "c")
    assert r["local_path"] is None
    assert "unsafe" in r["error"].lower()


def test_no_cache_dir_is_backward_compatible(monkeypatch, tmp_path):
    _mock_ok(monkeypatch, body=b"X")
    r = fetch_url("http://example.com/x", tmp_path / "d")  # cache_dir=None → no caching
    assert r["error"] is None and Path(r["local_path"]).read_bytes() == b"X"
    # An offline read afterwards has nothing cached → fails closed (nothing was written).
    _no_network(monkeypatch)
    r2 = fetch_url("http://example.com/x", tmp_path / "d2", offline=True)
    assert r2["local_path"] is None


def test_cache_config_from_env(monkeypatch):
    monkeypatch.delenv("SUBAGENT_FACTORY_URL_CACHE", raising=False)
    monkeypatch.delenv("SUBAGENT_FACTORY_OFFLINE", raising=False)
    assert cache_config_from_env() == (None, False)  # opt-in: default off
    monkeypatch.setenv("SUBAGENT_FACTORY_OFFLINE", "1")
    assert cache_config_from_env() == (DEFAULT_URL_CACHE, True)  # offline defaults the cache dir
    monkeypatch.setenv("SUBAGENT_FACTORY_URL_CACHE", "/tmp/mycache")
    assert cache_config_from_env() == (Path("/tmp/mycache"), True)  # explicit path honored
    monkeypatch.setenv("SUBAGENT_FACTORY_OFFLINE", "0")
    assert cache_config_from_env() == (Path("/tmp/mycache"), False)  # falsey offline


def test_prefetch_warms_cache_and_skips_local(monkeypatch, tmp_path):
    _mock_ok(monkeypatch, body=b"PGBODY", url="http://example.com/page")
    cache = tmp_path / "cache"
    res = pf.prefetch_url_sources(
        ["http://example.com/page", "/some/local/book.pdf"], cache_dir=cache
    )
    assert res["cached"] == ["http://example.com/page"]
    assert res["skipped"] == ["/some/local/book.pdf"]
    assert res["errors"] == []
    # The warmed cache is what an offline session serves.
    _no_network(monkeypatch)
    r = fetch_url("http://example.com/page", tmp_path / "d", cache_dir=cache, offline=True)
    assert Path(r["local_path"]).read_bytes() == b"PGBODY"


def test_prefetch_reports_errors(tmp_path):
    # An unsafe URL fails the SSRF guard (no network) → reported, not cached.
    res = pf.prefetch_url_sources(["http://127.0.0.1/x"], cache_dir=tmp_path / "c")
    assert res["cached"] == []
    assert len(res["errors"]) == 1 and res["errors"][0]["url"] == "http://127.0.0.1/x"


def test_prefetch_default_cache_dir(monkeypatch, tmp_path):
    # cache_dir omitted → prefetch targets DEFAULT_URL_CACHE (same dir the offline session defaults
    # to), so a warm-then-serve round trip works without threading a path through.
    monkeypatch.setattr(fu, "DEFAULT_URL_CACHE", tmp_path / "default-cache")
    monkeypatch.setattr(pf, "DEFAULT_URL_CACHE", tmp_path / "default-cache")
    _mock_ok(monkeypatch, body=b"DEF", url="http://example.com/d")
    res = pf.prefetch_url_sources(["http://example.com/d"])
    assert res["cached"] == ["http://example.com/d"]
    assert (tmp_path / "default-cache").exists()
