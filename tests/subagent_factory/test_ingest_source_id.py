"""Tests for the deterministic, content-addressed source_id (re-author stability)."""

import re
from pathlib import Path

from tools.subagent_factory.ingest_source import _content_source_id

# Stand-in hashes: only the first 8 chars are used, and non-hex avoids detect-secrets false hits.
_SHA_A = "z" * 64
_SHA_B = "y" * 64


def test_deterministic_for_same_content():
    p = Path("/x/Some Book Title.pdf")
    assert _content_source_id(p, _SHA_A) == _content_source_id(p, _SHA_A)


def test_slugified_stem_and_sha_prefix():
    sid = _content_source_id(Path("/x/Some Book Title.pdf"), "prefix00" + "z" * 56)
    assert sid.startswith("some-book") and sid.endswith("prefix00")


def test_differs_by_content():
    p = Path("/x/Book.pdf")
    assert _content_source_id(p, _SHA_A) != _content_source_id(p, _SHA_B)


def test_no_timestamp_component():
    # The prior scheme appended a 14-digit UTC timestamp; the content-addressed id must not, so
    # re-ingesting the same file never churns the id (the orphaning root cause).
    assert not re.search(r"\d{14}", _content_source_id(Path("/x/Doc.pdf"), _SHA_A))
