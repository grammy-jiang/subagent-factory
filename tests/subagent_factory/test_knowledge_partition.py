"""Tests for the G1 distill-vs-retrieve routing rule (Step-14 / G-track)."""

from tools.subagent_factory.knowledge_partition import partition_plan, route_knowledge_item


def test_distill_when_stable_high_reuse_small_noncitable():
    r = route_knowledge_item("core principle", reuse="high", volatility="stable", size="small")
    assert r["route"] == "distill" and r["placement"] == "always_on"
    assert r["fine_tune_candidate"] is False


def test_volatile_routes_to_retrieve():
    r = route_knowledge_item(reuse="high", volatility="volatile", size="small")
    assert r["route"] == "retrieve" and r["placement"] == "skills/references"
    assert "volatile" in r["reasons"]


def test_low_reuse_routes_to_retrieve():
    r = route_knowledge_item(reuse="low", volatility="stable", size="small")
    assert r["route"] == "retrieve"
    assert any("long-tail" in x for x in r["reasons"])


def test_large_routes_to_retrieve():
    r = route_knowledge_item(reuse="high", volatility="stable", size="large", citation_need=False)
    assert r["route"] == "retrieve" and "large" in r["reasons"]


def test_citation_need_forces_retrieve_even_if_otherwise_distillable():
    r = route_knowledge_item(reuse="high", volatility="stable", size="small", citation_need=True)
    assert r["route"] == "retrieve" and "citation-bearing" in r["reasons"]


def test_fine_tune_candidate_degrades_to_retrieve_with_note():
    # transferable bulk: high-reuse + large + stable + non-citable → fine-tune ideal, no training step
    r = route_knowledge_item(reuse="high", volatility="stable", size="large")
    assert r["route"] == "retrieve" and r["fine_tune_candidate"] is True
    assert "no training step" in r["note"]


def test_unknown_attributes_default_conservative_to_retrieve():
    # half-specified item must NOT be baked into the prompt
    r = route_knowledge_item(reuse="?", volatility="?", size="?")
    assert r["route"] == "retrieve"


def test_citation_need_accepts_strings():
    assert (
        route_knowledge_item(reuse="high", volatility="stable", size="small", citation_need="yes")[
            "route"
        ]
        == "retrieve"
    )


def test_case_insensitive():
    r = route_knowledge_item(reuse="HIGH", volatility="Stable", size="SMALL")
    assert r["route"] == "distill"


def test_partition_plan_buckets_and_measurement_flag():
    items = [
        {"name": "always-rule", "reuse": "high", "volatility": "stable", "size": "small"},
        {"name": "rate-table", "reuse": "high", "volatility": "volatile", "size": "small"},
        {"name": "big-reference", "reuse": "high", "volatility": "stable", "size": "large"},
        {
            "name": "cited-stat",
            "reuse": "high",
            "volatility": "stable",
            "size": "small",
            "citation_need": True,
        },
    ]
    plan = partition_plan(items)
    assert plan["distill"] == ["always-rule"]
    assert set(plan["retrieve"]) == {"rate-table", "big-reference", "cited-stat"}
    assert plan["fine_tune_candidates"] == ["big-reference"]
    assert plan["measurement_required"] is True  # G1 unproven → A/B before trusting


def test_partition_plan_empty():
    plan = partition_plan([])
    assert plan["distill"] == [] and plan["retrieve"] == []
    assert plan["measurement_required"] is False
