"""Tests for the deterministic grounding-leak scorer (cross-source borrow detection)."""

import json
import warnings

import pytest
import yaml

from tools.subagent_factory.grounding_check import grounding_check


def _pkg(root, slug, principle_statements):
    base = root / slug
    (base / "principles").mkdir(parents=True)
    (base / "profile.yaml").write_text(yaml.safe_dump({"tier": 1}), encoding="utf-8")
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {"principle_id": f"P{i}", "statement": s, "confidence": "high"}
                    for i, s in enumerate(principle_statements)
                ],
            }
        ),
        encoding="utf-8",
    )
    return base


def test_grounded_self_not_flagged_and_cross_source_borrow_named(tmp_path):
    root = tmp_path / "subagents"
    root.mkdir()
    # subject A grounds "alpha beta"; sibling B grounds "gamma delta".
    a = _pkg(root, "subject", ["The alpha beta principle lowers maintenance effort."])
    _pkg(
        root,
        "sibling",
        [
            "Apply gamma delta to govern the system safely.",
            "The epsilon zeta tactic prevents corruption.",
        ],
    )

    review = tmp_path / "review.md"
    review.write_text(
        "alpha beta holds here. alpha beta again.\n"
        "gamma delta is needed. gamma delta once more.\n"
        "epsilon zeta matters. epsilon zeta again.\n"
        "random noise word. random noise word.\n"
        "the shared doc thing. the shared doc thing.\n",
        encoding="utf-8",
    )
    doc = tmp_path / "doc.md"
    doc.write_text(
        "this design has a shared doc thing inside it; shared doc thing.\n", encoding="utf-8"
    )

    r = grounding_check(a, review, doc)

    # "alpha beta" is grounded in subject's own source → not a leak.
    leak_set = {bg for bg, _ in r["leak_terms"]}
    assert "alpha beta" not in leak_set
    # "gamma delta" leaks AND is named as a cross-source borrow from the sibling.
    cross = {bg: sibs for bg, _, sibs in r["cross_source_terms"]}
    assert "gamma delta" in cross and "sibling" in cross["gamma delta"]
    assert any(s == "sibling" for s, _ in r["suggested_sources"])
    # "shared doc thing" → "shared doc"/"doc thing" quoted from the doc → dropped, not leaked.
    assert "doc thing" not in leak_set and r["n_doc_quoted_dropped"] >= 1
    # "random noise" leaks but is NOT a cross-source borrow (no sibling grounds it).
    assert "random noise" in leak_set and "random noise" not in cross


def test_baseline_band_percentile():
    from tools.subagent_factory.grounding_check import baseline_band

    recs = [{"coverage": c} for c in (0.03, 0.05, 0.13, 0.25)]
    b = baseline_band(0.13, recs)
    assert b["n"] == 4
    assert b["floor"] == 0.03 and b["ceiling"] == 0.25
    assert b["median"] == 0.09  # mean of the two middle points (0.05, 0.13)
    assert b["percentile"] == 75  # 3 of 4 baseline points <= 0.13
    assert baseline_band(0.5, []) is None  # empty baseline -> no band


def test_no_cross_source_when_alone(tmp_path):
    root = tmp_path / "subagents"
    root.mkdir()
    a = _pkg(root, "solo", ["The alpha beta principle matters."])
    review = tmp_path / "r.md"
    review.write_text("gamma delta. gamma delta.\n", encoding="utf-8")
    r = grounding_check(a, review, None)
    assert r["cross_source_terms"] == [] and r["suggested_sources"] == []


def test_empty_review_is_not_applicable_not_perfect(tmp_path):
    # A review with no distinctive concept vocab must NOT score coverage 1.0 (a free gate pass);
    # it is "nothing to assess" → coverage None, scored False.
    root = tmp_path / "subagents"
    root.mkdir()
    a = _pkg(root, "solo", ["The alpha beta principle matters."])
    review = tmp_path / "empty.md"
    review.write_text("the a an of and to in.\n", encoding="utf-8")  # only stopwords/short
    r = grounding_check(a, review, None)
    assert r["coverage"] is None
    assert r["scored"] is False
    assert r["n_concept_terms"] == 0


def test_corpus_map_self_injection_matches_full_reparse(tmp_path):
    # Fix 1: the package under review is NOT re-parsed in the corpus loop; its precomputed bigrams
    # are injected instead. The resulting corpus bigram map (and every grounding number derived from
    # it) must be byte-identical to the old full-reparse behaviour. We compare the injected map
    # against a reparse-everything map over the same corpus.
    from tools.subagent_factory.grounding_check import _corpus_bigram_map, _grounded_vocab

    root = tmp_path / "subagents"
    root.mkdir()
    base = _pkg(root, "subject", ["The alpha beta principle lowers maintenance effort badly."])
    _pkg(root, "sibling", ["Apply gamma delta to govern alpha beta safely everywhere."])

    _, self_bi = _grounded_vocab(base)
    injected = _corpus_bigram_map(root, (base.name, self_bi))

    # Reference: re-parse EVERY package (the original behaviour, no injection).
    reference: dict = {}
    for pkg in sorted(root.iterdir()):
        if not pkg.is_dir() or not (pkg / "profile.yaml").exists():
            continue
        _, pkg_bi = _grounded_vocab(pkg)
        for bg in pkg_bi:
            reference.setdefault(bg, set()).add(pkg.name)

    assert injected == reference
    # Self bigram present and attributed to the subject; shared bigram attributed to both.
    assert "alpha beta" in injected and "subject" in injected["alpha beta"]
    assert injected["alpha beta"] == {"subject", "sibling"}


def test_corrupt_baseline_warns_absent_is_silent(tmp_path, recwarn):
    # Fix 2: a present-but-corrupt baseline warns (naming the path); a genuinely absent file is
    # silent (normal first run).
    from tools.subagent_factory.grounding_check import load_baseline

    missing = tmp_path / "nope.json"
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any warning would raise
        assert load_baseline(missing) == []  # absent → silent []

    corrupt = tmp_path / "baseline.json"
    corrupt.write_text("{not valid json", encoding="utf-8")
    with pytest.warns(RuntimeWarning, match=str(corrupt)):
        assert load_baseline(corrupt) == []

    # A well-formed baseline returns its records with no warning.
    good = tmp_path / "good.json"
    good.write_text(json.dumps([{"slug": "x", "coverage": 0.1}]), encoding="utf-8")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert load_baseline(good) == [{"slug": "x", "coverage": 0.1}]


def test_record_baseline_refuses_to_clobber_corrupt(tmp_path):
    # Fix 3 (data loss): record_baseline does read-modify-write via load_baseline, which returns []
    # for a corrupt file. Appending + overwriting would convert visible corruption into silent TOTAL
    # data loss of prior recoverable points. record_baseline must REFUSE on a corrupt non-empty file.
    from tools.subagent_factory.grounding_check import load_baseline, record_baseline

    # 1) Absent path → creates and appends normally.
    absent = tmp_path / "absent.json"
    record_baseline("a", 0.2, doc="d1", path=absent)
    recs = load_baseline(absent)
    assert len(recs) == 1 and recs[0]["slug"] == "a" and recs[0]["coverage"] == 0.2

    # 2) Valid prior records → appends and PRESERVES the prior points.
    valid = tmp_path / "valid.json"
    valid.write_text(json.dumps([{"slug": "p", "doc": "", "coverage": 0.1}]), encoding="utf-8")
    record_baseline("q", 0.3, path=valid)
    recs = load_baseline(valid)
    assert [r["slug"] for r in recs] == ["p", "q"]
    assert recs[0]["coverage"] == 0.1 and recs[1]["coverage"] == 0.3

    # 3) Legitimately-empty baseline ([]) → still appends normally.
    empty = tmp_path / "empty.json"
    empty.write_text("[]", encoding="utf-8")
    record_baseline("e", 0.4, path=empty)
    assert [r["slug"] for r in load_baseline(empty)] == ["e"]

    # 4) Corrupt non-empty file → RAISES and does NOT overwrite (corrupt bytes still on disk).
    corrupt = tmp_path / "corrupt.json"
    corrupt_bytes = "{not valid json — torn file from a prior crash"
    corrupt.write_text(corrupt_bytes, encoding="utf-8")
    with pytest.raises(Exception):  # noqa: B017 — any clear refusal is acceptable
        record_baseline("z", 0.9, path=corrupt)
    assert corrupt.read_text(encoding="utf-8") == corrupt_bytes  # untouched, not clobbered
