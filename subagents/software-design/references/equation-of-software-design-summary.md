---
name: equation-of-software-design-summary
kind: reference
status: ready
provenance:
  principles:
  - P027
  - P011
  - P030
  claims:
  - C00116
  - C00280
  - C00288
  - C00290
  - C00292
  - C00303
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00311
  - C00312
  - C00313
  - C00314
  - C00325
  source_anchors:
  - 5e67c59e0e18-c0001
  - aca1f3444508-c0000
  authored_from_digest: 10497c24f46532932a22d219f453c7e942956a4376e447f16d46d040aafaaefe
---

# Equation of Software Design — Summary

A compact statement of Kanat-Alexander's Equation of Software Design, the three flaws, and the
laws of change that follow from them. Use with `skills/apply-equation-of-software-design/`. This
reference gives the criteria a design judgement is weighed against; the skill applies them.

## Purpose first

The purpose of software is to help people. Every design decision is judged by whether it
increases the degree to which the software helps its users — a feature justified by technology
or competitors rather than user value should be deprioritised (clm-026; PRC-003).

## The Equation

> Desirability of a change is directly proportional to its **value** and inversely proportional
> to the **effort** required to make it (clm-027; PRC-002).

Two consequences govern how the Equation is applied to long-lived systems:

- **Maintenance effort dominates.** Over a system's lifetime, the effort of future maintenance
  outweighs the effort of present implementation, so reducing future maintenance effort
  outranks reducing present implementation effort (clm-028; PRC-002).
- **Quality tracks expected lifetime.** The quality level a design deserves is proportional to
  how long the system is expected to keep being used (clm-029).

## The three flaws of software design

| # | Flaw | What it means | Remedy | Grounding |
|---|---|---|---|---|
| 1 | **Unneeded code** | Writing code that is not yet needed | Do not write code until it is actually needed; remove code no longer used | clm-032; PRC-007 |
| 2 | **Not easy to change** | Failing to make code easy to change | Design for changeability based on what is known now | clm-033; PRC-008 |
| 3 | **Over-generality** | Being too generic / over-engineering | Make a design only as generic as present known requirements demand | clm-034; PRC-007 |

## Laws of change

| Law | Statement | Grounding |
|---|---|---|
| **Change is inevitable** | The longer a program exists, the more probable any given piece of it will need to change, so designing for change is essential | clm-031; PRC-008 |
| **Defect ∝ change size** | The probability of introducing a defect is proportional to the size of the change; smaller changes are safer | clm-036; PRC-008 |
| **Best design absorbs change** | The best design allows the most change in the environment with the least change to the software itself | clm-037; PRC-008 |
| **Design incrementally** | Develop and design in small steps, redesigning as needed, rather than attempting a complete design up front | clm-035; PRC-004 |
| **Change only on evidence** | Do not "fix" or optimise without evidence the problem is actually occurring; change without need risks introducing defects | clm-038; PRC-025 |
| **Do not predict the future** | The most common and costly error is predicting future needs and designing for them; decide on what is known now | clm-030; PRC-007 |

## Why simplicity is the lever

The ease of maintaining any piece of software is proportional to the simplicity of its
individual pieces, so simplicity is the central design lever for maintainability (clm-040;
PRC-019). The Equation and the three flaws all reduce to one operational rule: spend design
effort where it lowers future maintenance cost, and nowhere it merely adds speculative
generality.

## Provenance

Derived from *Code Simplicity: The Fundamentals of Software* (Kanat-Alexander, source
`code-simplicity-the-aca1f344`, `distillation-only`) via principles PRC-002, PRC-003, PRC-007,
PRC-008, and PRC-025 and their supporting claims (clm-026–clm-040), grounded in source anchors
`code-simplicity-the-aca1f344-h0020` through `-h0081`, as recorded in `principles/principles.yaml`
and `analysis/claims.jsonl`. All content is paraphrased; no verbatim source wording appears in
this file.
