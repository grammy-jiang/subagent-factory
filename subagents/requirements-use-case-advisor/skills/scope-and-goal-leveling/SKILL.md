---
name: scope-and-goal-leveling
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P013
  - P014
  - P018
  - P024
  - P025
  - P031
  - P073
  - P075
  - P076
  claims: []
  evidence: []
  source_anchors: []
---

# Scope and Goal Leveling

## Purpose

Establish and check the two coordinates that make a use case legible before any
scenario is written: its **design scope** (what system you are specifying) and its
**goal level** (how high or low the actor's goal sits). Getting these right is the
single hardest part of use-case work, and most defects in a submitted use case trace
back to one of them being unstated or wrong.

## When to use

- A use case's title or steps feel "off" but the wording is fine — usually a scope
  or level problem, not a grammar problem.
- The boundary of the system under discussion is ambiguous or disputed.
- A use case reads as a tiny mechanical step (below sea level) or as a vague
  company-wide ambition (too high).
- You need an actor-goal list to negotiate scope with users, sponsors, and
  developers.

## Procedure

### Step 1 — Name and label the design scope

Decide and write down what system the use case specifies (P002). Distinguish
**business scope** (the organisation) from **system scope** (the software), and name
the scope level explicitly (for example: enterprise, system, or subsystem). When
scope is contested, build an **in/out list**: a two-column list of features or
responsibilities that are in scope versus out of scope. The in/out list resolves
most boundary arguments cheaply, before scenarios are written.

### Step 2 — Identify the primary actor and confirm a real goal

The primary actor is the stakeholder whose goal the use case serves (P014). Confirm
the use case has a genuine goal that can succeed or fail — not a system function or a
UI action. Treat the system under discussion as a **black box** when the use case is
a functional requirement: describe what it does for the actor, not how it does it
internally (P025).

### Step 3 — Place the goal on the level scale

Classify the goal level (P018):

- **User-goal (blue):** one primary actor, at one sitting, achieving something of
  measurable value — typically 2-20 minutes of work. This is the anchor level.
- **Summary / strategic (white):** spans multiple user-goals or a longer horizon;
  useful as context and index.
- **Subfunction (indigo):** a step shared by other use cases, below the user goal.
  Black marks "too low to be worth a use case".

### Step 4 — Anchor at the user-goal level

Most functional requirements live in the blue, user-goal use cases (P076). Justify
the system by its list of blue goals — that list is the shortest summary of what the
system does and the basis for planning. Spend your detection energy here.

### Step 5 — Raise an under-level use case

If the goal sits below sea level (indigo/black), do not write it as a standalone use
case unless genuinely shared (P075). Raise it: ask **"why is the actor doing this?"**
or **"what does the actor really want?"** until you reach a user-goal. A use case
titled for a button click or a single field edit almost always needs raising.

### Step 6 — Add wide context use cases sparingly

Write at least one wide, summary-level use case by finding the outermost primary
actor (P031). A few high-level use cases serve as context and index and pay for
themselves — but the functional requirements still reside in the blue use cases, not
the white ones.

### Step 7 — Produce the actor-goal list

Brainstorm actors (human and non-human) to surface goals; it is the goals, not the
actor names, that matter, so err toward over-listing actors early (P024). Produce the
**Actor-Goal List**: each blue goal with its primary actor (P073). This list is the
negotiating point among users, sponsors, and developers, and the set of use cases it
implies forms one ever-unfolding story (P013).

## Inputs

- The use case(s) or goal under review, or a description of the system and its
  primary actors.
- The system boundary, if known, and any disputed in/out features.
- Project context (criticality, size) to judge how many summary use cases are worth
  writing.

## Output

A structured scope-and-level finding:

- **Design scope**: the named system and scope level, plus an in/out list when the
  boundary was unclear.
- **Goal level**: the assigned level (blue/white/indigo) for each use case, with the
  raising question applied to any under-level case and a proposed user-goal title.
- **Actor-Goal List**: blue goals paired with primary actors, flagged where a goal
  or actor is missing.
- **Corrective steps**: one per finding, each grounded in a cited principle.

## Provenance

Grounded in principles P002, P013, P014, P018, P024, P025, P031, P073, P075, P076 of
this package, derived from Alistair Cockburn, "Writing Effective Use Cases" (2001)
and Ivar Jacobson et al., "Use-Case 2.0" (2011). Sources are `distillation-only` —
all content is paraphrased; no verbatim quotation.
