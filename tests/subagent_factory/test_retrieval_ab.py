"""Tests for the Step-14 G1 in-prompt-vs-retrieval A/B harness (fakes only — no live model)."""

import json

from tools.subagent_factory.retrieval_ab import (
    Passage,
    build_retriever,
    load_passages,
    retrieval_ab,
    retrieval_runner,
)


def _test(tid, prompt, minimum):
    return {
        "test_id": tid,
        "section": "golden",
        "prompt": prompt,
        "expected_route": "invoke",
        "expected_mode": None,
        "must_ask_for": [],
        "minimum_output": minimum,
        "must_not_do": [],
        "file": "golden-tests.yaml",
    }


# Reflect BOTH the adapter (system prompt) and the prompt, so retrieved context injected into the
# prompt shows up in the "answer" — a deterministic stand-in for a model that uses its context.
def _echo_runner(adapter_text, prompt):
    return f"{adapter_text}\n{prompt}"


PASSAGES = [
    Passage(
        "A1",
        "Write-ahead logging writes each change to a durable log before the data pages, which "
        "guarantees crash recovery after a failure.",
    ),
    Passage("A2", "A B-tree index keeps keys sorted to support range scans and ordered traversal."),
    Passage(
        "A3", "Vacuum reclaims storage occupied by dead tuples left behind by updates and deletes."
    ),
]


def test_retrieve_ranks_by_overlap():
    retrieve = build_retriever(PASSAGES, k=2)
    hits = retrieve("how does write-ahead logging guarantee durability and crash recovery")
    assert hits and hits[0].id == "A1"  # most lexically relevant passage first
    assert len(hits) <= 2


def test_retrieve_drops_zero_score():
    retrieve = build_retriever(PASSAGES, k=3)
    assert retrieve("xylophone marsupial quark") == []  # no overlap → nothing retrieved


def test_retrieval_runner_injects_passage_text():
    seen = {}

    def base(adapter_text, prompt):
        seen["prompt"] = prompt
        return "ok"

    run = retrieval_runner(base, build_retriever(PASSAGES, k=1))
    run("ADAPTER", "tell me about write-ahead logging crash recovery")
    assert "[A1]" in seen["prompt"] and "durable log" in seen["prompt"]


def test_ab_detects_retrieval_help():
    # The required token ("crash recovery") lives only in passage A1 — NOT in the adapter or the
    # prompt. Distilled misses it; retrieval injects A1 → higher score → verdict retrieval-helps.
    tests = [_test("GT-001", "explain write-ahead logging durability", "crash recovery")]
    res = retrieval_ab("base adapter knows nothing here", tests, _echo_runner, PASSAGES, k=2)
    assert res["delta"] > 0
    assert res["verdict"] == "retrieval-helps"
    assert res["retrieval_mean"] > res["distilled_mean"]


def test_ab_distillation_suffices_when_adapter_already_has_it():
    # The adapter already states the answer → retrieval adds nothing → delta ~0 → distillation-suffices.
    tests = [_test("GT-001", "explain write-ahead logging durability", "crash recovery")]
    adapter = "the adapter already explains crash recovery in full"
    res = retrieval_ab(adapter, tests, _echo_runner, PASSAGES, k=2)
    assert res["verdict"] == "distillation-suffices"
    assert abs(res["delta"]) <= 0.02


def test_load_passages_skips_trivial_and_dedupes(tmp_path):
    base = tmp_path / "pkg"
    (base / "sources" / "anchors").mkdir(parents=True)
    rows = [
        {
            "anchor_id": "P1",
            "text": "Write-ahead logging guarantees durable crash recovery always.",
        },
        {"anchor_id": "P2", "text": "(preamble)"},  # trivial placeholder
        {"anchor_id": "P3", "text": "Too short"},  # below min_tokens
        {
            "anchor_id": "P1",
            "text": "duplicate id ignored the second time around entirely",
        },  # dup id
    ]
    (base / "sources" / "anchors" / "s.anchors.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows), encoding="utf-8"
    )
    passages = load_passages(base)
    assert [p.id for p in passages] == ["P1"]
    assert "crash recovery" in passages[0].text
