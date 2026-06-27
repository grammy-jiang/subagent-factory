---
name: story-quality-invest-checklist
kind: reference
status: ready
provenance:
  principles:
  - P038
  - P058
  - P059
  - P066
  - P078
  - P087
  - P061
  claims: []
  evidence: []
  source_anchors: []
---

# Story Quality and INVEST Checklist

A checklist for judging whether a user story is well-formed, and for reading common
story "smells". Use alongside `author-and-split-user-stories`.

---

## INVEST: the qualities of a good story

- [ ] **Independent** — minimally entangled with other stories; interdependent
      stories are combined or re-split as end-to-end slices (P061).
- [ ] **Negotiable** — a card is a token for a conversation, not a fixed contract
      (P038).
- [ ] **Valuable** — describes value to a user or purchaser, not to developers; UI and
      technology assumptions kept out; ideally the customer wrote it (P059).
- [ ] **Estimatable** — the team can size it; if not, fix the specific cause (missing
      domain knowledge, missing technical knowledge, or too big).
- [ ] **Small** — sized so one or a pair of programmers can finish it in roughly half a
      day to two weeks; large items are epics to be split (P058).
- [ ] **Testable** — passing its tests proves it is done; vague or non-functional
      stories are rewritten into measurable form, avoiding "never"/"always" (P087).

## Form

- [ ] Card text is terse and value-oriented, comprehensible to both business and
      developers (P078).
- [ ] Names the **user role** (not the generic "the user"), for one user, in the
      active voice — optionally "As a (role), I want (function), so that (value)"
      (P066).
- [ ] Card / Conversation / Confirmation are all accounted for: just enough text on the
      card, detail in conversation, specifics in acceptance tests (P038).
- [ ] Sized just right for planning, programming, and testing without needing further
      aggregation (P078).

## Story smells to act on (P061)

- [ ] **Too small / too many tiny stories** — combine into a meaningful end-to-end
      slice.
- [ ] **Interdependent stories** — re-split along end-to-end value, not technical
      layers.
- [ ] **Goldplating** — developers adding unrequested scope; curb it by keeping them on
      prioritised stories and raising task visibility via daily meetings, demos, and QA.
- [ ] **Epic masquerading as a story** — refine into smaller stories only when the
      feature is certain.

## When a story is the wrong vehicle

- [ ] Non-functional or constraint needs are handled as constraint cards or other
      formats, not forced into story shape.
- [ ] When shared understanding cannot be reached through stories, switch to a use case
      or scenario.

---

## Provenance

Grounded in principles P038, P058, P059, P061, P066, P078, P087 of this package,
derived from Mike Cohn, "User Stories Applied" (2004). Source is `distillation-only` —
all content is paraphrased; no verbatim quotation.
