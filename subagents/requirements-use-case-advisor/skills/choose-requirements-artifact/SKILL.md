---
name: choose-requirements-artifact
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P023
  - P045
  - P051
  - P052
  - P053
  - P056
  - P057
  - P079
  - P082
  claims: []
  evidence: []
  source_anchors: []
---

# Choose the Requirements Artifact

## Purpose

Help a team pick the right requirements vehicle — user stories, use cases, or
Use-Case 2.0 slices — for its context, and combine them coherently rather than
treating one method as universally correct.

## When to use

- A team is deciding how to capture requirements for a new product or release.
- Stories alone are losing the system view, or use-case ceremony is too heavy.
- Someone proposes an exhaustive "the system shall" specification as the primary
  approach.

## Procedure

### Step 1 — Understand how the artifacts relate

A story is roughly one scenario and, with its tests, approximates a use case — but is
smaller-scoped, more transient, less UI-laden, and meant to initiate rather than
document analysis (P015). Keep the Use-Case 2.0 model linked (P053): use cases
express goals and related requirements, slices scope independently workable value,
and stories explore stakeholder needs.

### Step 2 — Default to conversation over heavy specification

Favour frequent face-to-face conversation over heavy written specification, writing
documents only when they help deliver working software (P051). Writing shifts focus
to the document and away from the shared understanding the customer needs.

### Step 3 — Reject up-front exhaustive specs as the primary approach

Reject IEEE-830 "the system shall" specifications as a primary requirements approach
(P052): they are tedious and unread, obscure the big picture, hide each requirement's
cost until the whole document exists, and provoke document-rewriting blame games —
because it is impossible to fully specify a non-trivial system up front.

### Step 4 — Frame requirements around goals, not feature lists

Focus on the user's goals rather than a checklist of system behaviours (P079). Reject
the "change of scope" framing for evolving requirements, and ask "how and why will
this feature be used?" — turning feature lists into scenarios to reveal unneeded
features.

### Step 5 — Prefer use cases / slices when scale demands structure

Prefer use cases and use-case slices over standalone stories when the context needs
scalable structure, a stronger system view, test-asset management, impact analysis,
scope control, or missing-functionality detection (P023) — that is, larger systems,
larger teams, complex development, limited expert access, severe escaped-requirement
costs, or growing future complexity.

### Step 6 — Make the use-case slice the unit of work

When using Use-Case 2.0, make the use-case slice the primary unit of work — the
backlog item that carries its selected stories through design, implementation, and
verification (P045). A slice's structure gives it independence, value, testability,
estimability, negotiability, and further sliceability, and slices connect
requirements across the lifecycle to architecture, design, tests, planning, and reuse
(P056).

### Step 7 — Start light; add precision only when justified

Adopt Use-Case 2.0 as a lightweight, use-case-driven practice that structures
selected management, engineering, and delivery practices without dictating them
(P057). Start work products at the bare-essential level and increase detail only when
team context, communication needs, criticality, contractual constraints, or the
handoff model justify it (P082).

## Inputs

- Project context: system and team size, criticality, distribution, formality, and
  expert/user access.
- The current or proposed requirements approach.
- Whether a backlog-driven iterative process (e.g. Scrum) is in use.

## Output

An artifact-choice recommendation or review finding containing:

- **Recommended vehicle(s)**: stories, use cases, and/or Use-Case 2.0 slices, matched
  to scale and need, with the trade-offs named.
- **Anti-patterns flagged**: exhaustive up-front shall-lists, feature-checklist
  framing, or method dogma.
- **Combination model**: how stories, use cases, and slices link in this context, and
  the starting precision level.
- **Decision boundary**: the recommendation stays with the team; the advisor supplies
  options and trade-offs, each grounded in a cited principle.

## Provenance

Grounded in principles P015, P023, P045, P051, P052, P053, P056, P057, P079, P082 of
this package, derived from Mike Cohn, "User Stories Applied" (2004); Alistair
Cockburn, "Writing Effective Use Cases" (2001); and Ivar Jacobson et al., "Use-Case
2.0" (2011). Sources are `distillation-only` — all content is paraphrased; no verbatim
quotation.
