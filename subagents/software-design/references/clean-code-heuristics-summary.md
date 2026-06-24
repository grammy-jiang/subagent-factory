---
name: clean-code-heuristics-summary
kind: reference
status: ready
provenance:
  principles:
  - P004
  - P005
  - P014
  - P018
  - P029
  - P022
  - P030
  claims:
  - C00438
  - C00439
  - C00453
  - C00456
  - C00459
  - C00460
  - C00461
  - C00462
  - C00463
  - C00465
  - C00469
  - C00470
  - C00471
  - C00472
  - C00475
  - C00476
  source_anchors:
  - 5b1b9ca368a5-c0000
  - 5b1b9ca368a5-c0001
  authored_from_digest: c219a7e07ee72a576e9743953311af422daaf731d7cab5584bd8b95dcdf4b196
---

# Clean-Code Heuristics Summary

A condensed rubric of Martin's clean-code rules covering naming, functions, comments, classes,
and what makes a design simple. Use with `skills/review-naming-and-comments/` and
`skills/apply-single-responsibility/`. These are heuristics for readability and changeability,
not absolute laws; weigh each against the cost it removes (PRC-019; PRC-002).

## Naming

| Heuristic | Test | Grounding |
|---|---|---|
| **Intention-revealing names** | A good name says why the entity exists, what it does, and how it is used, reducing the need for a comment | clm-043; PRC-016 |
| **A name should create a precise image** | If a precise name cannot be found, treat that as a red flag that the underlying entity is not cleanly defined | clm-043; PRC-016 |

## Functions

| Heuristic | Test | Grounding |
|---|---|---|
| **Small** | Functions should be small, and then smaller; length is itself a smell when it hides intent | clm-044; PRC-014 |
| **Do one thing** | A function should do one thing, do it well, and do it only; if it does several things, split it | clm-045; PRC-014 |
| **One level of abstraction** | All statements in a function should sit at the same level of abstraction; mixing high- and low-level steps makes it harder to read | clm-046; PRC-014 |

## Comments

| Heuristic | Test | Grounding |
|---|---|---|
| **Comments do not fix bad code** | When tempted to write a comment, first make the code clear enough that the comment is unnecessary | clm-047; PRC-017 |
| **Extract and name instead of comment** | If a block needs a comment to explain it, extract it into a well-named function so the code explains itself | clm-071; PRC-017 |
| **Reserve comments for what code cannot say** | Design rationale, intent, units, and non-obvious external constraints are legitimate comments | clm-047; PRC-017 |

## Classes and responsibilities

| Heuristic | Test | Grounding |
|---|---|---|
| **Small classes, sized by responsibility** | Measure a class by its number of responsibilities, not its lines of code | clm-052; PRC-015 |
| **Single Responsibility Principle** | A class or module should have one, and only one, reason to change | clm-053; PRC-015 |
| **High cohesion** | Keeping each class cohesive naturally produces more, smaller classes — accept that as the cost of cohesion, but do not split so far that tightly-shared information leaks across the boundary | clm-054; PRC-015 |

## Objects, errors, and tests

| Heuristic | Test | Grounding |
|---|---|---|
| **Objects vs data structures** | Objects expose behaviour and hide data; data structures expose data and have little behaviour. A hybrid that does both gets the worst of each — avoid it | clm-048 |
| **Exceptions over error codes** | Prefer exceptions to returned error codes, and define exception classes in terms of the caller's needs so error handling does not obscure the main logic | clm-049; PRC-024 |
| **Clean tests, FIRST** | Unit tests keep production code flexible, maintainable, and reusable; keep them clean and Fast, Independent, Repeatable, Self-validating, and Timely | clm-051; PRC-012 |

## The four rules of simple design

In priority order, a design is simple when it (clm-055; PRC-019):

1. **Runs all the tests.**
2. **Contains no duplication** (DRY — see `fowler-code-smell-catalogue.md` and PRC-009).
3. **Expresses the intent of the programmer.**
4. **Minimises the number of classes and methods** — applied last, so it never overrides
   tests, deduplication, or clarity.

## Provenance

Derived from *Clean Code* (Martin, source `clean-code-a-handboo-5b1b9ca3`, `distillation-only`),
with the extract-don't-comment heuristic corroborated by *Refactoring* (Fowler,
`martin-fowler-refact-0574f24e`), via principles PRC-014–PRC-019 and their supporting claims
(clm-043–clm-055, clm-071), grounded in source anchors `clean-code-a-handboo-5b1b9ca3-h0035`
through `-h0407` and `martin-fowler-refact-0574f24e-h0156`, as recorded in
`principles/principles.yaml` and `analysis/claims.jsonl`. All content is paraphrased; no verbatim
source wording appears in this file.
