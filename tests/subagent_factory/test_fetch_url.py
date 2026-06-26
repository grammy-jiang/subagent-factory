"""Tests for fetch_url — SSRF guard + safety. Network is never actually hit: the SSRF check
runs before any request, so the unsafe-URL paths return without touching requests."""

import tempfile

from tools.subagent_factory.fetch_url import (
    _ip_is_blocked,
    _url_safety_error,
    fetch_url,
)


def test_blocked_ip_ranges():
    assert _ip_is_blocked("127.0.0.1")  # loopback
    assert _ip_is_blocked("10.0.0.5")  # private
    assert _ip_is_blocked("192.168.1.1")  # private
    assert _ip_is_blocked("169.254.169.254")  # link-local / cloud metadata
    assert _ip_is_blocked("::1")  # ipv6 loopback
    assert _ip_is_blocked("not-an-ip")  # unparseable → refuse
    assert not _ip_is_blocked("93.184.216.34")  # a public address


def test_ipv4_mapped_ipv6_is_blocked():
    # IPv4-in-IPv6 forms must be unwrapped and classified by their embedded v4 range — on older
    # CPython, IPv6Address.is_loopback/is_private don't inspect the embedded v4.
    assert _ip_is_blocked("::ffff:127.0.0.1")  # mapped loopback
    assert _ip_is_blocked("::ffff:169.254.169.254")  # mapped cloud-metadata
    assert _ip_is_blocked("::ffff:10.0.0.1")  # mapped RFC1918


def test_non_http_scheme_rejected():
    assert _url_safety_error("file:///etc/passwd")
    assert _url_safety_error("ftp://example.com/x")
    assert _url_safety_error("gopher://example.com")


def test_loopback_and_metadata_host_rejected():
    assert _url_safety_error("http://localhost/x")
    assert _url_safety_error("http://127.0.0.1/x")
    assert _url_safety_error("http://169.254.169.254/latest/meta-data/")


def test_no_host_rejected():
    assert _url_safety_error("http:///nohost")


def test_fetch_unsafe_url_returns_error_without_network(tmp_path):
    # A file:// URL must be refused by the scheme guard before any request is attempted.
    with tempfile.TemporaryDirectory() as d:
        r = fetch_url("file:///etc/passwd", d)
    assert r["error"] and "unsafe" in r["error"].lower()
    assert r["local_path"] is None


def test_fetch_localhost_refused(tmp_path):
    r = fetch_url("http://127.0.0.1:8080/secret", str(tmp_path))
    assert r["error"] and "unsafe" in r["error"].lower()
    assert r["local_path"] is None
