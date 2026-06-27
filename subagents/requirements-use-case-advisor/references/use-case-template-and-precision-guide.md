---
name: use-case-template-and-precision-guide
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P006
  - P007
  - P017
  - P019
  - P030
  - P046
  - P049
  - P050
  claims: []
  evidence: []
  source_anchors: []
---

# Use-Case Template and Precision Guide

A reference for choosing how much use-case structure to use and in what order to add
it. Use alongside `write-use-case-scenarios`. The governing idea: there is no single
best template — match density and ceremony to the project (P001).

---

## Template density: pick per project

- **One-paragraph brief** — the lightest form; a short prose summary of the goal and
  main path.
- **Casual** — a few labelled paragraphs (primary actor, main scenario, a handful of
  extensions).
- **Fully dressed** — the full field set below.

All forms carry the same information; format is a project choice, not a quality
ranking (P019). Match template density, tolerance, and ceremony to project
criticality, size, and communication needs (P001).

## Fully dressed fields (Cockburn)

- Use-case name (an active-verb goal phrase)
- Scope and Level (optional icons)
- Primary Actor
- Stakeholders and Interests
- Preconditions (only what the system guarantees)
- Success End Condition / Minimal Guarantees (failure protection)
- Trigger
- Main Success Scenario (numbered, one-column, plain prose, full sentences)
- Extensions (condition + handling fragments)
- Technology & Data Variations (optional)
- Related information / secondary requirements (in a sortable table)

Cockburn's preferred presentation is one-column, numbered, plain-prose, full-sentence
text (P019).

---

## Precision passes: breadth-first, low to high

Manage writing energy by working breadth-first and from low to high precision in
staged passes (P017):

1. Actors and goals (get the goal list accurate first)
2. Main success scenario
3. Failure/alternative conditions
4. Failure handling

Remember: **precision is not accuracy** — a precise but wrong use case is still wrong.

## The writing recipe

Follow the overall writing recipe — the 12-step process plus the complementary
top-down and middle-out work orders — and use the within-use-case pass/fail
checklist, the readability habits, and the set-level quality checks (P050).

---

## Economy: prefer writing too little

Prefer writing too little over too much (P006): a readable, approximate use case is
valuable, diminishing returns set in fast (a first draft yields about two-thirds of
the value, and writing costs roughly 100× reading), and the use case mainly serves as
a marker to remind the team. Optimise every use case for human readability and
communication — that is its ultimate purpose; you may trade some precision for
readability, but only so far before it stops serving its purpose (P046).

## Keep the use case in its text

Prefer plain prose over diagrams and formal notations, which only augment the text and
cut off untrained readers (P007). Prose handles complex parallel, optional, and
exceptional sequencing best.

---

## Keep data and the wider requirements out

Keep data descriptions out of the use case and manage them in three precision levels
(P049): information **nicknames** in the use-case text, with **field lists** and
**field details/checks** linked separately in the requirements file.

Recognise that use cases are only the functional portion — about chapter two, roughly
a quarter — of the requirements, and act as a hub linking the rest (P030). Do not
force non-interaction requirements into them; attach each use case's secondary
information in a sortable table.

---

## Provenance

Grounded in principles P001, P006, P007, P017, P019, P030, P046, P049, P050 of this
package, derived from Alistair Cockburn, "Writing Effective Use Cases" (2001). Source
is `distillation-only` — all content is paraphrased; no verbatim quotation.
