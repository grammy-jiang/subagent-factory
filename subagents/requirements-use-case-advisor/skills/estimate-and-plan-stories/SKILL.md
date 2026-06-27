---
name: estimate-and-plan-stories
kind: skill
status: ready
provenance:
  principles:
  - P016
  - P043
  - P062
  - P063
  - P064
  - P069
  - P070
  - P089
  claims: []
  evidence: []
  source_anchors: []
---

# Estimate and Plan Stories

## Purpose

Estimate stories collectively, measure velocity honestly, prioritise with the
customer, and build a release plan that is held loosely as a forecast rather than a
fixed commitment.

## When to use

- A team is estimating a backlog or planning a release or iteration.
- Velocity is being computed (or mis-computed from partial work).
- Story priority is disputed, or a deadline is forcing premature commitment.

## Procedure

### Step 1 — Estimate collectively

Own story estimates collectively as a team, involving as many developers as
practical, using an iterative Wideband-Delphi process where developers reveal private
estimates simultaneously and the customer only answers questions (P069). Fix any
non-estimatable story by its specific cause before sizing.

### Step 2 — Build the release plan in four steps

Create the release plan in four steps (P064): select iteration length, estimate
velocity, prioritise stories, and allocate them to iterations. Use short iterations
against a fixed near-term deadline so real velocity can be measured before committing
the rest. When a story's interpretation could swing its estimate, clarify with the
customer before sizing it.

### Step 3 — Allocate by priority up to velocity

Allocate the highest-priority stories into iterations up to the team's velocity
(P016). Hold the plan loosely: it gives an approximate duration, not a fixed date, so
use it to set — and then continually reset — expectations as velocity is measured and
stories are re-estimated.

### Step 4 — Prioritise with the customer

Let the customer prioritise, using user value and cohesion and weighing each story's
story-point cost, while taking developer input on risk and complementarity (P089).
Prioritise with MoSCoW and sort by technical factors (completion risk, deferral
impact) and customer factors (broad and key-user desirability, cohesion); when
sequence is disputed the customer decides, using estimates because cost changes
priority, and splits a story she cannot prioritise (P043).

### Step 5 — Measure velocity from completed work only

Use one iteration's measured velocity to forecast future iterations of the same
length (P062), valid when productivity was normal, estimates were consistent, and
stories were independent. Count only fully completed stories toward velocity, at full
value (P063): exclude partials, which hide last-10% complexity and signal oversized
stories or weak teamwork. Use the pre-iteration estimates without retroactive change,
and finish one story before starting the next.

### Step 6 — Plan the iteration one level deeper

Hold an iteration planning meeting with the whole team — customer plus all developers
— that plans one level deeper than the release plan, in the sequence
discuss-disaggregate-accept-estimate, with the customer reading stories in priority
order and details deferred to keep it efficient (P070).

## Inputs

- The estimated (or to-be-estimated) story set and the iteration length.
- The customer (for prioritisation) and the developers (for estimation).
- Any deadline and prior-iteration velocity data.

## Output

A planning artifact or review finding containing:

- **Estimates**: collectively-derived story sizes, with non-estimatable causes
  resolved.
- **Priority order**: a MoSCoW / value-and-cost ordering owned by the customer.
- **Release plan**: stories allocated to iterations up to velocity, framed as a
  forecast with explicit reset cadence.
- **Velocity check**: computed from completed stories only, with partial-credit or
  retroactive-estimate practices flagged.
- **Corrective steps**: one per finding, each grounded in a cited principle.

## Provenance

Grounded in principles P016, P043, P062, P063, P064, P069, P070, P089 of this
package, derived from Mike Cohn, "User Stories Applied" (2004). Source is
`distillation-only` — all content is paraphrased; no verbatim quotation.
