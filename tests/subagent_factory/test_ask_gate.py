"""Tests for the Step-13 deterministic ask-gate (Answer / Ask / Abstain).

Test-first: these pin the gate's decision logic with **fakes only — NO live model**. The gate is the
deterministic half of the two-stage ask-gate; the LLM half (``.claude/skills/ask-gate``) only *phrases*
the chosen action. Every case here is a pure function of a principle dict + a conversation list.
"""

from __future__ import annotations

from tools.subagent_factory.ask_gate import (
    Slot,
    already_asked,
    ask_f1,
    filled_slots,
    gate,
    replay_conversation,
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


def test_already_asked_resets_after_slot_is_supplied() -> None:
    # Recency bound: an ask is only "outstanding" until the user supplies the slot. Asked on an
    # assistant turn, then supplied on a later user turn → no longer counts as already-asked.
    budget = required_slots({"must_ask_for": ["budget"]})[0]
    asked_then_unanswered = [
        _assistant("What is the budget for this?"),
        _user("not sure"),
    ]
    assert already_asked(budget, asked_then_unanswered)
    asked_then_answered = [
        _assistant("What is the budget for this?"),
        _user("the budget is 20k"),
    ]
    assert not already_asked(budget, asked_then_answered)


def test_gate_re_asks_after_slot_supplied_then_needed_again() -> None:
    # The fix-#1 regression: vague → ask X, user supplies X (→answer), then a later assistant ask for
    # X with the user still not re-supplying it → the gate must ASK again, NOT abstain. The earlier
    # ask was satisfied when the slot was supplied, so it must not escalate forever.
    p = {"must_ask_for": ["budget", "timeline"]}
    conv = [
        _user("Help me plan the rollout"),
        _assistant("What is the budget?"),
        _user("the budget is 20k"),  # supplies budget → satisfies the earlier ask
        _assistant("What is the budget cap, to be precise?"),  # asks budget again, post-fill
        _user("please just advise"),  # does NOT re-supply; timeline still missing
    ]
    d = gate(p, conv)
    # budget is filled (accumulated); the still-missing slot is timeline → ask it, never abstain.
    assert d["action"] == "ask"
    assert d["slot"] == "timeline"


def test_gate_external_incidental_question_does_not_block_ask() -> None:
    # Bug fix: on an EXTERNALLY-supplied transcript (not gate-generated), a real assistant
    # rhetorical/clarifying question that incidentally shares ~half a slot's keywords must NOT be
    # read as "we already asked this slot". Slot "deployment target" = {deployment, target}; the
    # assistant's unrelated question mentions only "deployment" (1/2 keywords, NOT the full slot).
    # Under the old 0.5 ask-detection bar this tripped already_asked → silent ABSTAIN. The gate must
    # still ASK the slot (the false-negative this module exists to prevent).
    p = {"must_ask_for": ["deployment target"]}
    conv = [
        _user("Help me ship this service"),
        _assistant("Is the deployment ready to start?"),  # incidental: shares only "deployment"
        _user("just advise me"),
    ]
    d = gate(p, conv)
    assert d["action"] == "ask"
    assert d["slot"] == "deployment target"


def test_already_asked_strict_full_slot_match() -> None:
    # Directly pin the stricter ask-detection bar: a partial-keyword incidental question is NOT an
    # ask of the slot, but the gate's own full-phrasing fallback question IS detected as already-asked.
    slot = required_slots({"must_ask_for": ["deployment target"]})[0]
    incidental = [_assistant("Is the deployment ready to start?"), _user("not sure")]
    assert not already_asked(slot, incidental)
    # The gate-generated fallback embeds the full slot phrasing → still detected (recency/re-ask path).
    full_phrasing = [_assistant(slot.question), _user("not sure")]
    assert already_asked(slot, full_phrasing)


def test_gate_generated_re_ask_still_detected_after_fix() -> None:
    # Behaviour-preserving for gate-generated conversations: replay writes the slot's full fallback
    # question, so the anti-re-ask escalation to abstain still fires under the stricter bar.
    decisions = replay_conversation(
        {"must_ask_for": ["deployment target"]},
        ["Help me ship this service", "I'm not sure, just give your best guess"],
    )
    assert [d["action"] for d in decisions] == ["ask", "abstain"]


def test_gate_decision_includes_slot_question() -> None:
    # gate surfaces the chosen slot's fallback question so callers need not re-derive it.
    d = gate({"must_ask_for": ["budget"]}, [_user("please advise")])
    assert d["action"] == "ask"
    assert d["question"] == required_slots({"must_ask_for": ["budget"]})[0].question
    answer = gate({"must_ask_for": ["budget"]}, [_user("budget is 20k")])
    assert answer["action"] == "answer" and answer["question"] is None


def test_gate_out_of_scope_abstains() -> None:
    d = gate({"must_ask_for": ["budget"]}, [_user("anything")], out_of_scope=True)
    assert d["action"] == "abstain"
    assert d["missing"] == []


def test_gate_no_required_context_answers() -> None:
    # A principle with no required-context slots just answers.
    d = gate({}, [_user("anything")])
    assert d["action"] == "answer"


# --- multi-turn scenario replay (Phase C) -----------------------------------------------------


def test_replay_conversation_ask_then_answer() -> None:
    # The headline multi-turn behaviour: ask on turn 1, answer on turn 2, no re-ask.
    decisions = replay_conversation(
        {"must_ask_for": ["budget"]}, ["Help me plan the rollout", "The budget is 20k"]
    )
    assert [d["action"] for d in decisions] == ["ask", "answer"]


def test_replay_conversation_anti_re_ask_to_abstain() -> None:
    # Asked on turn 1; user never supplies it → escalate to abstain, do not re-ask the same slot.
    decisions = replay_conversation(
        {"must_ask_for": ["budget"]},
        ["Help me plan the rollout", "I'm not sure, just give your best guess"],
    )
    assert [d["action"] for d in decisions] == ["ask", "abstain"]


def test_replay_conversation_out_of_scope_step() -> None:
    decisions = replay_conversation(
        {"must_ask_for": ["budget"]}, ["something off topic"], out_of_scope_steps={0}
    )
    assert decisions[0]["action"] == "abstain"


def test_ask_f1_perfect_sequence() -> None:
    m = ask_f1(["ask", "answer"], ["ask", "answer"])
    assert m["f1"] == 1.0
    assert m["tp"] == 1 and m["fp"] == 0 and m["fn"] == 0
    assert m["exact_match"] is True


def test_ask_f1_no_ask_scenario_is_perfect() -> None:
    # A scenario that correctly never asks is perfect, not undefined.
    m = ask_f1(["answer", "answer"], ["answer", "answer"])
    assert m["f1"] == 1.0 and m["tp"] == 0 and m["exact_match"] is True


def test_ask_f1_penalizes_over_and_under_ask() -> None:
    # expected answer→got ask (FP, over-ask); expected ask→got answer (FN, silent-commit).
    m = ask_f1(["answer", "ask"], ["ask", "answer"])
    assert m["tp"] == 0 and m["fp"] == 1 and m["fn"] == 1
    assert m["f1"] == 0.0
    assert m["exact_match"] is False
