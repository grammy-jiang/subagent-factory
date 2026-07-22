"""Fallback-chain tests for the HTML converter (readability+markdownify → pandoc). The two attempt
functions are mocked so no real readability/pandoc is needed; the chain orchestration is under
test. assess_quality/compute_stats run for real (pure)."""

import tools.subagent_factory.convert_html as ch


def _src(tmp_path):
    src = tmp_path / "in.html"
    src.write_text("<html><body><p>hello world</p></body></html>", encoding="utf-8")
    return src, tmp_path / "out.md"


def test_primary_readability_succeeds(monkeypatch, tmp_path):
    monkeypatch.setattr(
        ch,
        "_try_readability_markdownify",
        lambda html: ("# T\n\nbody text here\n", "readability+markdownify", [], []),
    )
    # pandoc fallback must not be reached
    monkeypatch.setattr(ch, "_try_pandoc", lambda src: (None, None, [], ["should not be used"]))
    src, out = _src(tmp_path)
    r = ch.convert_html(src, out)
    assert r["converter_used"] == "readability+markdownify"
    assert out.read_text().strip()
    assert not any("fallback" in w.lower() for w in r["warnings"])


def test_fallback_to_pandoc_when_readability_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(
        ch, "_try_readability_markdownify", lambda html: (None, None, [], ["readability failed"])
    )
    monkeypatch.setattr(ch, "_try_pandoc", lambda src: ("body text here\n", "pandoc", [], []))
    src, out = _src(tmp_path)
    r = ch.convert_html(src, out)
    assert r["converter_used"] == "pandoc"
    assert any("fallback" in w.lower() for w in r["warnings"])
    assert out.read_text().strip()


def test_both_converters_fail_yields_none(monkeypatch, tmp_path):
    monkeypatch.setattr(
        ch, "_try_readability_markdownify", lambda html: (None, None, [], ["readability failed"])
    )
    monkeypatch.setattr(ch, "_try_pandoc", lambda src: (None, None, [], ["pandoc failed"]))
    src, out = _src(tmp_path)
    r = ch.convert_html(src, out)
    assert r["converter_used"] == "none"
    assert r["markdown_text"] == ""
    assert any("All HTML converters failed" in e for e in r["errors"])
    assert not out.exists()
