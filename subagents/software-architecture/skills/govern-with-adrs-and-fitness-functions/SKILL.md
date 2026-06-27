---
name: govern-with-adrs-and-fitness-functions
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P001
  claims:
  - C00263
  - C00268
  - C00027
  - C00066
  evidence:
  - E00070
  - E00071
  - E00006
  - E00019
  source_anchors:
  - 508117177502-c0011
  - 508117177502-c0001
  - 508117177502-c0003
  authored_from_digest: 75916a987bfa8203f7ea238503c936f910793ed0281fb93f7e06bb43e807d79b
---

# Govern with ADRs and fitness functions

## Purpose

For the hard problems of distributed architecture there are no reusable "best practices"; the
correct decision is derived by analyzing trade-offs for the specific context, not copied from a
generic recipe. Once derived, a significant decision should be captured as an Architecture
Decision Record (context, decision, consequences) and continuously governed by fitness functions
that test whether the implementation still upholds it. This skill drives that derive → record →
govern loop.

## When to use

- A hard distributed-architecture decision has no obvious correct answer.
- The caller wants a generic best practice applied without analysis.
- A previously-made decision risks silently eroding as the implementation evolves.

Do not invoke when the decision is local and low-stakes with a well-established standard answer.

## Procedure

1. **Reject the copied recipe.** When a generic "best practice" is offered for a hard distributed
   problem, treat it as a hypothesis, not an answer. State that the context must drive the choice.
2. **Derive from trade-off analysis.** Run the specific options through trade-off analysis against
   the prioritized characteristics (use `architecture-tradeoff-analysis`) to reach a context-fit
   decision.
3. **Record an ADR.** Capture the decision in three parts: the *context* (forces and constraints),
   the *decision* itself, and the *consequences* (what it gains and what the team must now live
   with). The consequences section is the trade-off made durable.
4. **Define fitness functions.** For each property the decision must preserve (e.g. a layering
   rule, a coupling limit, a latency budget), specify an objective check that can be run against
   the implementation.
5. **Wire governance in.** Recommend running those fitness functions continuously so the
   implementation cannot silently drift from the recorded decision; a failing function signals
   erosion to be addressed or a decision to be revisited via a new ADR.
6. **Keep decisions visible.** When a decision is superseded, add a new ADR rather than rewriting
   the old one, so the decision history and its consequences stay auditable.

## Inputs

- The hard distributed decision, its candidate options, and the prioritized characteristics it
  must serve.

## Output

A derived, context-specific decision recorded as an ADR (context / decision / consequences) plus
the fitness functions that govern it against drift. Generic best practices are reframed as
hypotheses to test, not answers to copy.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — the
  trade-off frame these decisions are derived from.

## Provenance

Distilled from principle(s) **P018/P009**, claims **C00326/C00331/C00025/C00026**, evidence **E00070/E00071/E00008/E00009**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
