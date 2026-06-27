---
name: goal-levels-and-scope-reference
kind: reference
status: ready
provenance:
  principles:
  - P002
  - P018
  - P031
  - P075
  - P076
  claims: []
  evidence: []
  source_anchors: []
---

# Goal Levels and Scope Reference

A quick reference for classifying a use case's goal level and design scope. Use
alongside `scope-and-goal-leveling`.

---

## Goal levels (Cockburn's colours)

| Level | Colour | Meaning | Test |
|-------|--------|---------|------|
| Summary / strategic | white (cloud) | Spans multiple user goals or a long horizon | Multi-sitting, multiple goals; serves as context/index |
| User goal | **blue (sea level)** | One actor, one sitting, measurable value | ~2-20 minutes; the actor would feel done |
| Subfunction | indigo (underwater) | A step shared by other use cases | Below the user goal; only write if genuinely shared |
| Too low | black | Mechanical detail, not worth a use case | A single field edit or button click |

Anchor on the **user-goal (blue)** level: one person, one place, one sitting of about
2-20 minutes, and respect how the levels nest (P018).

## Raising an under-level use case

Getting goal levels right is the single hardest thing about use cases. Do not write or
read below-sea-level (indigo/subfunction) use cases except as needed (P075). To raise
an under-level use case, ask:

- **"What does the actor really want?"**
- **"Why is the actor doing this step?"**

Repeat until you reach a goal the actor would consider worth a sitting.

## Where the requirements live

Justify the system by the list of blue (user-goal) use cases it supports — the
shortest summary of its function and the basis for planning (P076). Spend most of your
detection energy finding the blue goals; consider the use cases "done" when every
primary actor's blue goals are written.

Write at least one wide corporate or strategic (white) use case by finding the
outermost primary actor (P031). These few high-level use cases serve as context and
index and pay for themselves — but the functional requirements still reside in the
blue use cases, not the white ones.

---

## Design scope

| Scope | What it specifies |
|-------|-------------------|
| Enterprise / organisation | The business and its processes (often technology-free) |
| System | The software system under discussion |
| Subsystem | A component within the system |

Get the design scope clear and label every use case with its scope and level (P002):

- Name and broadcast the scope levels (e.g. corporate, system, subsystem).
- Distinguish **business** scope from **system** scope.
- Use an **in/out list** to resolve ambiguity about what is inside the boundary.

An element's classification (actor, scope, level) is always relative to the chosen
scope, so fix the scope before classifying.

---

## Provenance

Grounded in principles P002, P018, P031, P075, P076 of this package, derived from
Alistair Cockburn, "Writing Effective Use Cases" (2001). Source is `distillation-only`
— all content is paraphrased; no verbatim quotation.
