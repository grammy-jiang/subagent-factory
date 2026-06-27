---
name: author-and-split-user-stories
kind: skill
status: ready
provenance:
  principles:
  - P038
  - P039
  - P040
  - P041
  - P058
  - P059
  - P066
  - P078
  - P085
  - P087
  claims: []
  evidence: []
  source_anchors: []
---

# Author and Split User Stories

## Purpose

Write, review, and split user stories so each is a small, value-oriented, testable
unit that the customer owns. Stories are placeholders for a conversation, not
miniature specifications, and their power comes from being deferred until needed and
sized for planning.

## When to use

- Drafting or reviewing a story or story set for value, size, and testability.
- An epic is too large to estimate or to finish in an iteration and must be split.
- A "story" is really a constraint or non-functional need that should not be forced
  into story form.

## Procedure

### Step 1 — Model each story as Card, Conversation, Confirmation

Write just enough text on the card to remember and plan the story; put the detail in
the conversation and the acceptance tests (P038). The card is a token for a future
conversation, not the full requirement.

### Step 2 — Write for value to a user or purchaser

Frame each story around value to a user or purchaser, not to developers, and keep UI
and technology assumptions out (P059). The surest way to achieve this is to have the
customer write the stories. Optionally use the "As a (role), I want (function), so
that (value)" template to name the role, keep one user in mind, and surface
ambiguities (P066).

### Step 3 — Keep stories terse and comprehensible

Keep stories terse and value-oriented so both business and developers understand them
(P078). People recall story-organised information better; size each story just right
for planning, programming, and testing without further aggregation.

### Step 4 — Size small; treat large ones as epics

Prefer many small stories (P058): size each so one or a pair of programmers can finish
it in roughly half a day to two weeks. Treat a large story as an **epic** — a
placeholder you refine into smaller stories only when the feature is certain (P085),
which keeps detail deferred and exploits stories' iterability.

### Step 5 — Make every story testable

Write every story so that passing its tests proves it is done (P087). Rewrite vague
stories — especially non-functional ones — into measurable form, and avoid absolutes
like "never" or "always".

### Step 6 — Ensure each story is estimatable

If a story cannot be estimated, fix the specific cause (P040): discuss with the
customer for missing domain knowledge, run a timeboxed spike for missing technical
knowledge, or disaggregate a too-big story.

### Step 7 — Split epics end-to-end, not in layers

Split a compound epic into end-to-end constituent stories, grouping or splitting along
data boundaries, without over-splitting (P039). For a complex or uncertain epic,
split off a timeboxed investigative **spike** plus a development story, ideally in
separate iterations, so research can be prioritised on its own.

### Step 8 — Do not force every requirement into a story

Handle non-functional requirements as **Constraint** cards with an automated daily
compliance test where feasible, and express more complex needs (such as a data
dictionary) in whatever additional format suits them (P041). Not everything is a
story.

## Inputs

- The story, story set, or epic under review, or the goal/feature to capture.
- The user role(s) and the value the feature delivers.
- Access to the customer for the conversation and for writing or confirming stories.

## Output

A story or review finding containing:

- **Story text**: terse, role-named, value-oriented card text (or a rewrite of the
  submitted story).
- **Size verdict**: small / epic, with a proposed end-to-end or spike+story split for
  oversized items.
- **Testability**: measurable acceptance criteria framing, with vague or absolute
  wording flagged.
- **Non-story items**: constraints or data needs redirected to the appropriate form.
- **Corrective steps**: one per finding, each grounded in a cited principle.

## Provenance

Grounded in principles P038, P039, P040, P041, P058, P059, P066, P078, P085, P087 of
this package, derived from Mike Cohn, "User Stories Applied" (2004). Source is
`distillation-only` — all content is paraphrased; no verbatim quotation.
