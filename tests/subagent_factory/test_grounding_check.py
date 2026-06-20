"""Tests for the deterministic grounding-leak scorer (cross-source borrow detection)."""

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
