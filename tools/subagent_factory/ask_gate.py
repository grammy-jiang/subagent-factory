"""Step-13 ask-gate — the **deterministic** half of a two-stage Answer / Ask / Abstain gate.

Default LLMs almost never ask or abstain and are overconfident, and retrieved context *suppresses*
asking further (calibration findings #3). So the behaviour must be **imposed by an explicit gate**, not
hoped for. The factory determinism boundary applies: this module owns *which action and which slot* —
pure functions, no model call — and the LLM skill ``.claude/skills/ask-gate`` owns only the *wording*
of the chosen action (the one specific clarification question, or the scoped abstention).

What the gate decides, per the research spec (``docs/enhancement-steps/step-13-ask-gate.md``):

- **answer** — every required-context slot the principle needs is already supplied.
- **ask** — a decision-relevant slot is missing; ask the single highest-priority one (information
  gain, not a generic "tell me more"). Over-asking hurts and is nonmonotonic (#5), so the gate asks
  for exactly one slot at a time and never re-asks.
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
    if not keywords:
        return False
    present = sum(1 for k in keywords if k in tokens)
    return present >= 1 and present / len(keywords) >= _FILL_FRACTION


def already_asked(slot: Slot, conversation: list[dict]) -> bool:
    """True if a prior **assistant** turn already asked for this slot.

    Requires both a question mark (the turn is interrogative, not merely discussing the topic) and the
    slot's keywords present — so a normal answer that happens to mention the slot does not count."""
    keywords = _slot_keywords(slot)
    if not keywords:
        return False
    for turn in conversation:
        if _role(turn) != "assistant":
            continue
        text = _turn_text(turn)
        if "?" not in text:
            continue
        if _fraction_present(keywords, _content_tokens(text)):
            return True
    return False


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

    Returns ``{"action", "slot", "missing", "reason"}``. ``slot`` is the slot to ask about (for
    ``ask``) or the unsupplied slot that triggered escalation (for the anti-re-ask ``abstain``), else
    ``None``. ``missing`` is every still-unfilled required slot, in priority order."""
    if out_of_scope:
        return {
            "action": "abstain",
            "slot": None,
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
            "missing": [],
            "reason": "all required context is present",
        }
    first = next(s for s in slots if s.name == missing[0])
    if already_asked(first, conversation):
        return {
            "action": "abstain",
            "slot": first.name,
            "missing": missing,
            "reason": f"already asked for '{first.name}' and it was not supplied — escalate, do not re-ask",
        }
    return {
        "action": "ask",
        "slot": first.name,
        "missing": missing,
        "reason": f"missing decision-relevant context: '{first.name}'",
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
