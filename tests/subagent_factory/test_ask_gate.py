"""Tests for the Step-13 deterministic ask-gate (Answer / Ask / Abstain).

Test-first: these pin the gate's decision logic with **fakes only — NO live model**. The gate is the
deterministic half of the two-stage ask-gate; the LLM half (``.claude/skills/ask-gate``) only *phrases*
the chosen action. Every case here is a pure function of a principle dict + a conversation list.
"""

from __future__ import annotations

from tools.subagent_factory.ask_gate import (
    Slot,
    already_asked,
    filled_slots,
    gate,
    required_slots,
)


def _user(text: str) -> dict:
    return {"role": "user", "content": text}


def _assistant(text: str) -> dict:
    return {"role": "assistant", "content": text}


# --- required_slots ---------------------------------------------------------------------------


def test_required_slots_from_must_ask_for() -> None:
    slots = required_slots({"must_ask_for": ["budget", "timeline"]})
    assert [s.name for s in slots] == ["budget", "timeline"]
    assert all(isinstance(s, Slot) and s.question for s in slots)


def test_required_slots_dedup_preserves_order() -> None:
    slots = required_slots({"must_ask_for": ["budget", "budget", "timeline"]})
    assert [s.name for s in slots] == ["budget", "timeline"]


def test_required_slots_secondary_applies_when_when_no_must_ask_for() -> None:
    # must_ask_for is primary; applies_when is the secondary, schema-free source.
    slots = required_slots(
        {"applies_when": ["When the user provides a deployment target environment."]}
    )
    assert slots  # at least one slot derived from the clause
    assert all(s.question for s in slots)


def test_required_slots_must_ask_for_suppresses_applies_when() -> None:
    # When must_ask_for is present it is authoritative — applies_when does not add extra slots.
    slots = required_slots(
        {"must_ask_for": ["budget"], "applies_when": ["Some unrelated condition holds."]}
    )
    assert [s.name for s in slots] == ["budget"]


def test_required_slots_empty_principle() -> None:
    assert required_slots({}) == []


# --- filled_slots / already_asked -------------------------------------------------------------


def test_filled_slots_scans_user_turns_only() -> None:
    slots = required_slots({"must_ask_for": ["budget", "timeline"]})
    conv = [_user("My budget is about 50k"), _assistant("noted, timeline?")]
    # "timeline" appears only in an assistant turn → not filled.
    assert filled_slots(slots, conv) == {"budget"}


def test_filled_slots_accumulates_across_turns() -> None:
    slots = required_slots({"must_ask_for": ["budget", "timeline"]})
    conv = [_user("budget is 50k"), _assistant("and the timeline?"), _user("timeline is Q3")]
    assert filled_slots(slots, conv) == {"budget", "timeline"}


def test_already_asked_requires_question_in_assistant_turn() -> None:
    budget = required_slots({"must_ask_for": ["budget"]})[0]
    assert not already_asked(budget, [_user("help me")])
    assert not already_asked(budget, [_assistant("Your budget looks fine.")])  # no '?'
    assert already_asked(budget, [_assistant("What is the budget for this?")])


# --- gate -------------------------------------------------------------------------------------


def test_gate_answers_when_all_filled() -> None:
    d = gate(
        {"must_ask_for": ["budget", "timeline"]},
        [_user("Budget is 50k and the timeline is 3 months")],
    )
    assert d["action"] == "answer"
    assert d["missing"] == []
    assert d["slot"] is None


def test_gate_asks_first_missing_slot() -> None:
    d = gate({"must_ask_for": ["budget", "timeline"]}, [_user("My budget is 50k, please advise")])
    assert d["action"] == "ask"
    assert d["slot"] == "timeline"
    assert d["missing"] == ["timeline"]


def test_gate_asks_highest_priority_first() -> None:
    # Both missing → ask the first must_ask_for entry (priority = declaration order).
    d = gate({"must_ask_for": ["budget", "timeline"]}, [_user("please advise on my plan")])
    assert d["action"] == "ask"
    assert d["slot"] == "budget"
    assert d["missing"] == ["budget", "timeline"]


def test_gate_multi_turn_fill_then_answer() -> None:
    p = {"must_ask_for": ["budget"]}
    turn1 = [_user("Help me plan the rollout")]
    d1 = gate(p, turn1)
    assert d1["action"] == "ask" and d1["slot"] == "budget"
    # User supplies the slot on the next turn → answer, no re-ask.
    turn2 = turn1 + [_assistant("What is the budget?"), _user("The budget is 20k")]
    d2 = gate(p, turn2)
    assert d2["action"] == "answer"
    assert d2["missing"] == []


def test_gate_anti_re_ask_escalates_to_abstain() -> None:
    # A prior assistant turn already asked for the slot; the user never supplied it → abstain,
    # don't loop the same question (the bounded multi-turn anti-re-ask rule).
    conv = [
        _user("Help me plan the rollout"),
        _assistant("What is the budget for this rollout?"),
        _user("I'm not sure, just give me your best guidance"),
    ]
    d = gate({"must_ask_for": ["budget"]}, conv)
    assert d["action"] == "abstain"
    assert d["slot"] == "budget"


def test_gate_out_of_scope_abstains() -> None:
    d = gate({"must_ask_for": ["budget"]}, [_user("anything")], out_of_scope=True)
    assert d["action"] == "abstain"
    assert d["missing"] == []


def test_gate_no_required_context_answers() -> None:
    # A principle with no required-context slots just answers.
    d = gate({}, [_user("anything")])
    assert d["action"] == "answer"
