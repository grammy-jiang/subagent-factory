---
name: fowler-code-smell-catalogue
kind: reference
status: ready
provenance:
  principles:
  - P010
  - P015
  - P019
  - P029
  - P011
  - P007
  claims:
  - C00450
  - C00481
  - C00482
  - C00483
  - C00484
  - C00485
  - C00486
  - C00487
  - C00488
  - C00493
  - C00575
  - C00609
  - C00621
  - C00650
  - C00670
  - C00672
  source_anchors:
  - 0574f24ece08-c0000
  - 5b1b9ca368a5-c0000
  - 5b1b9ca368a5-c0001
  - 5b1b9ca368a5-c0004
  - 5b1b9ca368a5-c0006
  authored_from_digest: 11ed5779f94bb0f33bcd5658f74728ca7399504491fa6c92d0b3064546c2a218
---

# Fowler Code-Smell Catalogue

A catalogue of recognisable structural warning signs in code. A *smell* is a surface symptom
that suggests where refactoring is likely to pay off; it is a heuristic for *when* and *where*
to refactor, **not** a strict rule that mandates action (clm-063; PRC-013). Use this catalogue
with `skills/detect-code-smells/` to name findings and with
`skills/plan-behaviour-preserving-refactoring/` to choose the transformation that removes each.

## Using the catalogue

For each smell, record its canonical **name**, the **location**, the **structural root cause**
it signals, and the **refactoring family** that addresses it. Name the family only — the
specific mechanics belong to the refactoring-planning skill. A smell found in stable code that
is not being modified and is not linked to a reported symptom is a *watch item*, not a required
action (clm-063; PRC-013).

## Catalogue

| Smell | What to look for | Structural root cause | Refactoring family |
|---|---|---|---|
| **Duplicated code** | The same or very similar code structure in more than one place | A single piece of knowledge with no single home — a DRY violation (clm-064; clm-039; PRC-009) | Extract Function / Extract Class / Pull Up Method |
| **Long function** | A function long enough that its intent is harder to grasp than its name implies | An abstraction not yet extracted; multiple steps not yet named (clm-065) | Extract Function |
| **Long parameter list** | A signature with so many parameters it is hard to reason about | A missing concept that should group the parameters into one object (clm-066) | Introduce Parameter Object / Preserve Whole Object |
| **Divergent change** | One module changed in different ways for different reasons across different change events | More than one responsibility housed in one module (clm-067; PRC-015) | Extract Class / Split Module |
| **Shotgun surgery** | One logical change forces many small edits scattered across many modules | A responsibility spread across many places that belongs gathered into one (clm-068) | Move Function / Move Field / Inline Class |
| **Feature envy** | A function more interested in another module's data than its own | Behaviour placed away from the data it uses (clm-069) | Move Function |
| **Data clumps** | The same group of data items always travels together as loose parameters or repeated fields | A missing type that should make the clump a single concept (clm-070) | Introduce Parameter Object / Extract Class |
| **Primitive obsession** | Raw primitives used where a small named value object would carry the value and its constraints | Over-reliance on raw types where a richer type belongs (clm-070) | Replace Primitive with Object / Extract Class |
| **Dead code** | Unreachable branches, unused variables, functions never called | Code whose purpose has gone; noise without value (clm-056) | Remove Dead Code / Inline |
| **Function that does too much** | A function body holding several distinct operations or levels of abstraction | Single responsibility violated at the function level (clm-056; PRC-014) | Extract Function |
| **Comment as deodorant** | A comment is needed to explain a confusing block | Code that does not yet explain itself; the comment masks unclear structure (clm-071; PRC-017) | Extract Function (name the block so the comment becomes unnecessary) |

## Cross-catalogue note

Several smells converge with entries in `ousterhout-red-flags-catalogue.md` — for example,
*duplicated code* ↔ *repetition*, *function that does too much* ↔ *shallow / overexposed
module*, *divergent change* ↔ a single-responsibility breach. When a finding matches both
catalogues, cite both; the convergence raises confidence that the symptom is real (clm-025).

## Ranking guidance

Rank smells by cost, not cosmetics (PRC-002; PRC-013):

1. **Shotgun surgery** and **divergent change** — they cause change amplification across the
   codebase (clm-067; clm-068).
2. **Duplicated code** and **feature envy** — they create covert dependencies between sites that
   will eventually diverge incorrectly and silently (clm-064; clm-069; PRC-009).
3. **Long function**, **long parameter list**, **data clumps**, **primitive obsession** —
   significant but usually local in impact (clm-065; clm-066; clm-070).
4. **Dead code**, **comment-as-deodorant** — lower cost unless they obscure behaviour with wider
   consequences (clm-056; clm-071).

## Provenance

Derived from *Refactoring* (Fowler, source `martin-fowler-refact-0574f24e`, `distillation-only`),
with corroborating warning-sign material from *Clean Code* (Martin, `clean-code-a-handboo-5b1b9ca3`)
and the DRY rule from *Code Simplicity* (Kanat-Alexander, `code-simplicity-the-aca1f344`), via
principles PRC-013 and PRC-009 and their supporting claims (clm-063–clm-071, clm-056, clm-039),
grounded in source anchors `martin-fowler-refact-0574f24e-h0133` through `-h0156`,
`clean-code-a-handboo-5b1b9ca3-h0358`, and `code-simplicity-the-aca1f344-h0078`/`-h0079` as
recorded in `principles/principles.yaml` and `analysis/claims.jsonl`. All content is paraphrased;
no verbatim source wording appears in this file.
