---
name: operate-a-docs-as-code-workflow
kind: skill
status: ready
provenance:
  principles:
  - P049
  - P051
  - P050
  - P026
  - P017
  - P012
  - P001
  - P052
  claims:
  - C00305
  - C00306
  - C00307
  - C00335
  - C00339
  - C00340
  - C00331
  - C00292
  - C00324
  - C00312
  - C00006
  - C00059
  source_anchors:
  - 9b3c3a535ed6-c0001
  - 9b3c3a535ed6-c0000
  - 7065cb6e73a0-c0000
  authored_from_digest: 42f8695a64156246d0c72293674807b6fd7bed27399464fa3cb5c9f94dba429a
---

# Operate a docs-as-code workflow

## Purpose

Shape a documentation pipeline that lives beside the code: source in (or alongside) the
repository, the same authoring and review tooling writers can actually use, and a build/test gate
before documentation is continuously delivered. The aim is a sustainable workflow, not just a
file format — capacity, ownership, and gating are planned, and the documentation is improved
iteratively like the code.

## When to use

- A team is moving documentation into the code repository and must plan the workflow.
- A docs pipeline ships broken or stale pages and needs a build/test gate.
- A team is choosing where documentation lives and how writers collaborate on it.
- Documentation has stagnated and needs a repeating improvement cycle.

Do not use this skill to pick or configure a specific static-site generator or CI system; it
guides the workflow shape, and tool selection hands off to the team.

## Procedure

### Step 1 — Plan capacity and ownership before adopting docs-in-code

1. **Plan for writer capacity, backup ownership, load balancing, and the cost of context
   switching** before committing to a docs-in-code workflow — these decide whether it is
   sustainable. (P049)

2. **If documentation source lives inside product code, give writers the same practical workflow
   access** that code contributors have, so they are not second-class. (P026)

### Step 2 — Choose where documentation lives

3. **Use the organization's normal collaboration platform** for documentation when it improves
   internal alignment, lowers the barrier to contribution, and writers already work there. (P050)

4. **Preserve simple authoring** (e.g. Markdown) with static-site metadata and templates so
   shared content, product variants, and presentation are supported without burdening writers.
   (P012)

### Step 3 — Let reference tooling and narrative coexist

5. **Select or extend API-documentation tooling so generated reference can coexist with narrative
   integration docs** — the generated reference and the hand-written guides live in one set.
   (P017)

### Step 4 — Gate continuous delivery on a passing build

6. **Continuously deliver documentation only when CI can build and test accepted commits**, block
   production on failures, and keep published docs in step with the code. (P051)

### Step 5 — Improve iteratively, never "finished"

7. **Treat documentation as a guide to process, not a plan**: work in small steps, publish or
   commit every improvement immediately, and let good structure grow organically. Documentation
   is never finished but can always be complete. (P001)

8. **Run a repeating improvement cycle**: choose any page (even at random), assess it critically
   against its type and clarity, improve it, and move on. (P052)

## Inputs

- **Required:** where the documentation lives today (or the intent to move it to the repo), the
  team's authoring tools, and whether a CI build/test exists.
- **Optional:** writer headcount and the product's release cadence.

## Output

A concrete next workflow step — a capacity/ownership plan, a place for the docs, a tooling-coexist
arrangement, a build/test gate, or an improvement-cycle cadence — with the reason it matters.

## Provenance

Derived from the capacity-planning principle **P049**, the CI-gate principle **P051**, the
collaboration-platform principle **P050**, and the tooling/iteration principles
**P026/P017/P012/P001/P052** (claims **C00305**, **C00335**, **C00331**, **C00292**, **C00324**,
**C00312**, **C00006**, **C00059**), grounded in Anne Gentle, *Docs Like Code*, at chunk anchors
`9b3c3a535ed6-c0001` and `9b3c3a535ed6-c0000`, and in Diátaxis (`7065cb6e73a0-c0000`) for the
iterate-in-small-steps principles. Distillation-only sources: paraphrased throughout, no verbatim
quotation.
