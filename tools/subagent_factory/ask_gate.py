"""Step-13 ask-gate — the **deterministic** half of a two-stage Answer / Ask / Abstain gate.

Default LLMs almost never ask or abstain and are overconfident, and retrieved context *suppresses*
asking further (calibration findings #3). So the behaviour must be **imposed by an explicit gate**, not
hoped for. The factory determinism boundary applies: this module owns *which action and which slot* —
pure functions, no model call — and the LLM skill ``.claude/skills/ask-gate`` owns only the *wording*
of the chosen action (the one specific clarification question, or the scoped abstention).

What the gate decides, per the research spec (``docs/enhancement-steps/step-13-ask-gate.md``):

- **answer** — every required-context slot the principle needs is already supplied.
- **ask** — a decision-relevant slot is missing; ask the single first-declared required slot (the
  deterministic layer owns *which slot is missing*, in ``must_ask_for`` declaration order — it does
  **not** compute an information-gain ranking; sharpening to "ask the most informative one" is the
  LLM skill's job). Over-asking hurts and is nonmonotonic (#5), so the gate asks for exactly one slot
  at a time and only re-asks a slot that has not been supplied since it was last asked.
- **abstain** — either the request is out of scope, or the missing slot was *already asked* in a prior
  assistant turn and the user still has not supplied it (the bounded multi-turn **anti-re-ask** rule:
  the user can't or won't give it → escalate, don't loop the same question).

The required-context "slots" are a **schema-free** approximation of a required-context ontology
(round-3 residual novelty #2): derived from a principle's ``must_ask_for`` (primary, an explicit list)
and, only when that is absent, from its ``applies_when`` clauses (secondary). Slot fill and prior-ask
detection are lexical over the conversation — deterministic, model-free, and unit-testable with fakes.

What this module deliberately does **not** do: a black-box single-turn *calibrated risk score* (act iff
risk ≤ τ). That is **DEFERRED** — hosted (API-only) Claude exposes no logprobs/latents, so the
white-box answerability probe the research recommends does not transfer (the open ACADEMIC residual).

CLI::

    python -m tools.subagent_factory.ask_gate <principle.json> <conversation.json>
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from tools.subagent_factory.claim_recall import _content_tokens

Action = Literal["answer", "ask", "abstain"]

# A slot counts as filled / previously-asked when this fraction of its content keywords is present
# (with at least one present). For a single-keyword slot this is exact presence; for a multi-word
# requirement it tolerates partial phrasing without demanding the whole clause verbatim.
_FILL_FRACTION = 0.5
# applies_when fallback: how many leading content tokens of a clause form the secondary slot name.
_CLAUSE_SLOT_TOKENS = 3


@dataclass(frozen=True)
class Slot:
    """One required-context slot a principle needs before it can safely answer.

    ``name`` is the canonical identifier surfaced in the gate decision; ``question`` is a plain
    fallback prompt (the LLM skill replaces it with one sharpened, information-gain question)."""

    name: str
    question: str


def _ordered_content_tokens(text: str) -> list[str]:
    """Content tokens in first-occurrence order (``_content_tokens`` returns an unordered set; slot
    naming needs determinism). Same tokenizer/stopword family as the rest of the factory."""
    keep = _content_tokens(text)
    seen: set[str] = set()
    out: list[str] = []
    for t in str(text).lower().replace("/", " ").split():
        tok = "".join(c for c in t if c.isalnum())
        if tok in keep and tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


def _normalize_name(raw: str) -> str:
    """Canonical slot name from a ``must_ask_for`` entry: lower-cased, whitespace-collapsed."""
    return " ".join(str(raw).lower().split())


def _question_for(raw: str) -> str:
    """A plain fallback question for a slot (the skill replaces it with a sharpened one)."""
    text = str(raw).strip()
    if text.endswith("?"):
        return text
    return f"What is the {text.rstrip('.')}?"


def _slot_keywords(slot: Slot) -> set[str]:
    """The content tokens that signal this slot's information is present in a turn."""
    return _content_tokens(slot.name)


def required_slots(principle: dict) -> list[Slot]:
    """Derive the required-context slots a principle needs (the schema-free ontology).

    ``must_ask_for`` is **primary**: each entry becomes one slot, in order, de-duplicated. Only when
    ``must_ask_for`` is absent/empty does the secondary ``applies_when`` source apply — each clause
    yields one slot named from its leading content tokens (an approximation, the flagged round-3
    residual). Returns ``[]`` when the principle declares no required context."""
    slots: list[Slot] = []
    seen: set[str] = set()
    for raw in principle.get("must_ask_for") or []:
        name = _normalize_name(raw)
        if name and name not in seen:
            seen.add(name)
            slots.append(Slot(name, _question_for(raw)))
    if slots:
        return slots
    for clause in principle.get("applies_when") or []:
        toks = _ordered_content_tokens(clause)[:_CLAUSE_SLOT_TOKENS]
        name = " ".join(toks)
        if name and name not in seen:
            seen.add(name)
            slots.append(Slot(name, f"Please provide context for: {str(clause).strip()}"))
    return slots


def _turn_text(turn: dict) -> str:
    return str(turn.get("content", turn.get("text", "")))


def _role(turn: dict) -> str:
    return str(turn.get("role", "")).lower()


def _fraction_present(keywords: set[str], tokens: set[str]) -> bool:
    # 2-token edge (P011, documented, intentionally not changed): with _FILL_FRACTION=0.5 a
    # two-keyword slot is satisfied by EITHER keyword (1/2 == 0.5), so a turn that mentions only one
    # half of a two-word slot name counts as a fill — a potential premature false-fill. The threshold
    # stays 0.5 unless a test demonstrates a real false-fill; tightening it would also break the
    # single-keyword exact-presence case (1/1).
    #
    # NOTE: this 0.5 FILL threshold is used for slot *fill* detection (filled_slots) AND, separately,
    # for the *recency-reset* leg of already_asked (a user turn that supplies the slot). It is NOT
    # used for the assistant-question (ASK) detection leg — that uses the stricter _all_present below.
    # See _all_present for why ASK-detection demands the full slot phrasing.
    if not keywords:
        return False
    present = sum(1 for k in keywords if k in tokens)
    return present >= 1 and present / len(keywords) >= _FILL_FRACTION


def _all_present(keywords: set[str], tokens: set[str]) -> bool:
    # Stricter bar than _fraction_present, used ONLY for assistant-question (ASK) detection in
    # already_asked. Requires EVERY slot keyword to be present (full normalized-name match).
    #
    # Why stricter for ASK-detection specifically: gate() runs not only on gate-GENERATED transcripts
    # (replay_conversation, where only the gate writes assistant turns using the full slot phrasing)
    # but also on EXTERNALLY-supplied transcripts (the CLI, validate_generated_package wiring). On an
    # external transcript a real assistant rhetorical/clarifying question can incidentally share >=50%
    # of a slot's keywords (e.g. slot "deployment target" and the assistant says "Is the deployment
    # ready?"). Under the loose 0.5 bar that incidental question would count as "we already asked this
    # slot" and the gate would ABSTAIN instead of ASK — a silent-commit-adjacent false negative,
    # exactly what this module exists to prevent. Demanding the full slot phrasing avoids that while
    # still matching every gate-generated fallback question (which embeds the whole slot name).
    if not keywords:
        return False
    return all(k in tokens for k in keywords)


def already_asked(slot: Slot, conversation: list[dict]) -> bool:
    """True if the slot was asked in an **assistant** turn and has **not been supplied since**.

    Requires both a question mark (the turn is interrogative, not merely discussing the topic) and the
    slot's **full** keyword set present — so a normal answer that happens to mention the slot, or an
    incidental external question that merely shares part of the slot phrasing, does not count. The
    ASK-detection bar is deliberately stricter (``_all_present``) than the fill bar (``_fraction_present``,
    0.5): on EXTERNALLY-supplied transcripts an incidental assistant question sharing only half a slot's
    keywords must NOT be read as "we already asked this slot" (that would drive a silent abstain instead
    of the needed ask). Gate-generated fallback questions embed the full slot phrasing, so the strict bar
    still matches them — the recency/re-ask behaviour is unchanged for gate-generated conversations.

    Recency bound (fix for silent over-abstention): an ask only triggers escalation while it is still
    *outstanding*. If a later **user** turn supplies the slot, that ask is satisfied and no longer
    counts — so a slot that was asked, answered, then becomes relevant again is re-asked rather than
    abstained on. (``filled_slots`` deliberately accumulates a slot as filled forever; this prior-ask
    detection must NOT accumulate the same way, or it would escalate a slot that was already answered.)
    """
    keywords = _slot_keywords(slot)
    if not keywords:
        return False
    asked_outstanding = False
    for turn in conversation:
        role = _role(turn)
        text = _turn_text(turn)
        if role == "assistant":
            # ASK-detection uses the stricter full-keyword bar (not _fraction_present) so an incidental
            # external question that merely shares part of the slot phrasing does not trip a silent abstain.
            if "?" in text and _all_present(keywords, _content_tokens(text)):
                asked_outstanding = True
        elif role == "user":
            # A user turn that supplies the slot satisfies any earlier ask for it.
            if _fraction_present(keywords, _content_tokens(text)):
                asked_outstanding = False
    return asked_outstanding


def filled_slots(slots: list[Slot], conversation: list[dict]) -> set[str]:
    """Names of slots whose information appears in any **user** turn (lexical, accumulated across all
    user turns — a slot supplied on turn 1 stays filled on turn 5)."""
    user_tokens: set[str] = set()
    for turn in conversation:
        if _role(turn) == "user":
            user_tokens |= _content_tokens(_turn_text(turn))
    return {s.name for s in slots if _fraction_present(_slot_keywords(s), user_tokens)}


def gate(principle: dict, conversation: list[dict], *, out_of_scope: bool = False) -> dict:
    """Decide Answer / Ask / Abstain for ``principle`` given the ``conversation`` so far.

    Returns ``{"action", "slot", "question", "missing", "reason"}``. ``slot`` is the slot to ask about
    (for ``ask``) or the unsupplied slot that triggered escalation (for the anti-re-ask ``abstain``),
    else ``None``; ``question`` is that slot's fallback clarification question (``None`` when ``slot``
    is ``None``) so callers need not re-look-up or re-derive it. ``missing`` is every still-unfilled
    required slot, in declaration order. The chosen slot is simply the **first declared** missing slot
    — this layer owns *which slot is missing*, not an information-gain ranking (that is the skill's)."""
    if out_of_scope:
        return {
            "action": "abstain",
            "slot": None,
            "question": None,
            "missing": [],
            "reason": "request is out of scope for this advisor",
        }
    slots = required_slots(principle)
    filled = filled_slots(slots, conversation)
    missing = [s.name for s in slots if s.name not in filled]
    if not missing:
        return {
            "action": "answer",
            "slot": None,
            "question": None,
            "missing": [],
            "reason": "all required context is present",
        }
    first = next(s for s in slots if s.name == missing[0])
    if already_asked(first, conversation):
        return {
            "action": "abstain",
            "slot": first.name,
            "question": first.question,
            "missing": missing,
            "reason": f"already asked for '{first.name}' and it was not supplied — escalate, do not re-ask",
        }
    return {
        "action": "ask",
        "slot": first.name,
        "question": first.question,
        "missing": missing,
        "reason": f"missing required context: first declared unfilled slot '{first.name}'",
    }


def replay_conversation(
    principle: dict,
    user_turns: list[str],
    *,
    out_of_scope_steps: set[int] | None = None,
) -> list[dict]:
    """Replay a **multi-turn** scenario through the gate, one user turn at a time (Step-13 Phase C).

    After each user turn the gate decides; when it decides ``ask`` the (fallback) clarification
    question is appended as an assistant turn *before the next user turn* — exactly so the next step's
    ``already_asked`` check can see it and the anti-re-ask escalation fires. This is the executable
    "ask on turn 1 → answer on turn 2, **no re-ask**" multi-turn behaviour, composed from the
    validated single-turn parts (the round-3 compose-from-validated-parts adapt path). Returns the
    decision dict at each step (one per user turn).

    Calibration that *updates as context grows* (round-3 residual #1) is approximated structurally:
    each step re-derives fill from the whole conversation so far, so a slot supplied on any earlier
    turn stays satisfied — the gate's confidence to answer rises monotonically as slots fill."""
    oos = out_of_scope_steps or set()
    conversation: list[dict] = []
    decisions: list[dict] = []
    for i, utterance in enumerate(user_turns):
        conversation.append({"role": "user", "content": utterance})
        decision = gate(principle, conversation, out_of_scope=(i in oos))
        decisions.append(decision)
        if decision["action"] == "ask":
            # gate returns the chosen slot's fallback question; reuse it verbatim so the next step's
            # already_asked check sees the same phrasing (no re-look-up, no divergent reconstruction).
            conversation.append({"role": "assistant", "content": decision["question"]})
    return decisions


def ask_f1(expected: list[str], actual: list[str]) -> dict:
    """ASK-F1 over a scenario: precision / recall / F1 of the ``ask`` action — the gate's central
    decision (calibration eval metric, round-3). TP = asked when it should; FP = asked when it should
    not (over-asking); FN = should have asked but did not (silent-commit). ``exact_match`` is whether
    the full action sequence matched (catches answer↔abstain confusions ASK-F1 alone misses).

    Precision/recall default to 1.0 when there are no positive predictions/targets (a scenario that
    correctly never asks is perfect, not undefined)."""
    pairs = list(zip(expected, actual, strict=False))
    tp = sum(1 for e, a in pairs if e == "ask" and a == "ask")
    fp = sum(1 for e, a in pairs if e != "ask" and a == "ask")
    fn = sum(1 for e, a in pairs if e == "ask" and a != "ask")
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "exact_match": all(e == a for e, a in pairs) if pairs else True,
        "n_steps": len(pairs),
    }


def evaluate_tests(missing_context: list[dict], twins: list[dict] | None = None) -> dict:
    """Run the deterministic gate over a package's OWN behaviour tests — the Step-13 measurement
    surface (no model call). Each test dict needs ``test_id``, ``prompt``, ``must_ask_for``.

    Two guards, reported **separately** because they differ in reliability:

    * **silent-commit** (reliable) — every ``missing_context`` test's prompt omits the required
      context it declares in ``must_ask_for``, so the gate MUST decide ``ask``. A test where the gate
      instead ``answer``\\ s/``abstain``\\ s is a *false-fill*: the prompt lexically names the slot, so
      the gate can't tell context is missing — the real, actionable defect this guard catches.
    * **over-ask** (diagnostic, only when ``twins`` are supplied) — each answerable twin inherits the
      same ``must_ask_for`` but its prompt supplies the context, so ideally the gate ``answer``\\ s.
      Slot-fill is a *lexical, schema-free approximation* (Step-13 residual #2): a twin that signals
      sufficiency in prose ("every specific is provided") rather than by naming the slot reads as an
      over-ask. So a high over-ask rate flags twins whose sufficient-context is not lexically aligned
      with the declared slots (typical of template-mode test generation) — **not** a gate pass/fail.

    Returns per-guard rows + tallies, and the ASK-F1 over the silent-commit set (where, since every
    expected action is ``ask``, ASK-F1 collapses to ask-recall)."""

    def _act(t: dict) -> str:
        return gate(
            {"must_ask_for": t.get("must_ask_for") or []},
            [{"role": "user", "content": str(t.get("prompt", ""))}],
        )["action"]

    sc_rows = [{"test_id": t.get("test_id"), "action": _act(t)} for t in missing_context]
    tw_rows = [{"test_id": t.get("test_id"), "action": _act(t)} for t in (twins or [])]
    return {
        "silent_commit": {
            "total": len(sc_rows),
            "asked": sum(1 for r in sc_rows if r["action"] == "ask"),
            "misses": [r for r in sc_rows if r["action"] != "ask"],
            "rows": sc_rows,
            "f1": ask_f1(["ask"] * len(sc_rows), [str(r["action"]) for r in sc_rows]),
        },
        "over_ask": {
            "total": len(tw_rows),
            "answered": sum(1 for r in tw_rows if r["action"] == "answer"),
            "over_asked": [r for r in tw_rows if r["action"] == "ask"],
            "rows": tw_rows,
        },
    }


def _load_json(path: str | Path) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Deterministic Answer/Ask/Abstain ask-gate (Step-13). Decides the action + slot; "
        "the .claude/skills/ask-gate skill phrases it."
    )
    ap.add_argument(
        "principle", help="path to a principle JSON ({must_ask_for, applies_when, ...})"
    )
    ap.add_argument(
        "conversation", help="path to a conversation JSON (list of {role, content} turns)"
    )
    ap.add_argument(
        "--out-of-scope",
        action="store_true",
        help="mark the request out of scope (forces abstain)",
    )
    args = ap.parse_args()

    principle = _load_json(args.principle)
    conversation = _load_json(args.conversation)
    if not isinstance(principle, dict):
        print("principle JSON must be an object")
        return 2
    if not isinstance(conversation, list):
        print("conversation JSON must be a list of turns")
        return 2

    decision = gate(principle, conversation, out_of_scope=args.out_of_scope)
    print(json.dumps(decision, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
