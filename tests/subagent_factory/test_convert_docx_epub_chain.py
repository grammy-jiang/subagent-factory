"""Fallback-chain tests for the pandoc→markitdown converters (docx, epub), which are structurally
identical. The external converters are mocked at the attempt-function seam (try_pandoc /
try_markitdown) so no real pandoc/markitdown is needed — the chain orchestration (fallback trigger,
warning surfacing, error aggregation) is what's under test. finalize/assess_quality/compute_stats
run for real (pure)."""

import pytest

import tools.subagent_factory.convert_docx as cdocx
import tools.subagent_factory.convert_epub as cepub

# fmt -> (module, convert fn, label used in the "All <label> converters failed" error)
_CASES = {
    "docx": (cdocx, cdocx.convert_docx, "DOCX"),
    "epub": (cepub, cepub.convert_epub, "ePUB"),
}


def _src(tmp_path, fmt):
    src = tmp_path / f"in.{fmt}"
    src.write_bytes(b"binary-bytes")
    return src, tmp_path / "out.md"


@pytest.mark.parametrize("fmt", ["docx", "epub"])
def test_primary_pandoc_succeeds(monkeypatch, tmp_path, fmt):
    mod, convert, _ = _CASES[fmt]
    monkeypatch.setattr(
        mod, "try_pandoc", lambda s, f: ("# T\n\nbody text here\n", "pandoc", [], [])
    )
    # markitdown must not be reached when pandoc succeeds
    monkeypatch.setattr(
        mod, "try_markitdown", lambda s, p: (None, None, [], ["should not be used"])
    )
    src, out = _src(tmp_path, fmt)
    r = convert(src, out)
    assert r["converter_used"] == "pandoc"
    assert out.read_text().strip()  # written by finalize
    assert not any("fallback" in w.lower() for w in r["warnings"])


@pytest.mark.parametrize("fmt", ["docx", "epub"])
def test_fallback_to_markitdown_when_pandoc_empty(monkeypatch, tmp_path, fmt):
    mod, convert, _ = _CASES[fmt]
    monkeypatch.setattr(mod, "try_pandoc", lambda s, f: (None, None, [], ["pandoc failed"]))
    monkeypatch.setattr(
        mod, "try_markitdown", lambda s, p: ("body text here\n", "markitdown", [], [])
    )
    src, out = _src(tmp_path, fmt)
    r = convert(src, out)
    assert r["converter_used"] == "markitdown"
    assert any("fallback" in w.lower() for w in r["warnings"])  # fallback surfaced
    assert out.read_text().strip()


@pytest.mark.parametrize("fmt", ["docx", "epub"])
def test_both_converters_fail_yields_none(monkeypatch, tmp_path, fmt):
    mod, convert, label = _CASES[fmt]
    monkeypatch.setattr(mod, "try_pandoc", lambda s, f: (None, None, [], ["pandoc failed"]))
    monkeypatch.setattr(mod, "try_markitdown", lambda s, p: (None, None, [], ["markitdown failed"]))
    src, out = _src(tmp_path, fmt)
    r = convert(src, out)
    assert r["converter_used"] == "none"
    assert r["markdown_text"] == ""
    assert any(f"All {label} converters failed" in e for e in r["errors"])
    assert not out.exists()  # nothing written on total failure
