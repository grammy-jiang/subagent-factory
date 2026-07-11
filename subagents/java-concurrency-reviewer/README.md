# java-concurrency-reviewer

**Version:** 0.1.0
**Status:** draft

## Purpose

Evaluates Java concurrent code and designs for safety, liveness, and performance using
the design principles and patterns from Doug Lea's "Concurrent Programming in Java:
Design Principles and Patterns" (1997). Identifies specific hazard categories (atomicity
violations, visibility errors, races, deadlock paths, starvation), names the applicable
Lea pattern, and provides targeted recommendations.

## Modes

| Mode | When to invoke |
|------|---------------|
| `review` | Submit existing Java code with concurrent constructs for safety and liveness evaluation |
| `advise` | Ask which concurrency pattern to apply to a given situation |
| `compare` | Submit two or more concurrency design alternatives for side-by-side evaluation |

## Required inputs

- The Java source code or design description to review (at minimum the class or method
  definitions with concurrent constructs: synchronized blocks/methods, wait/notify usage,
  thread creation, or shared mutable state)
- Enough context about the class's concurrent role to judge whether its synchronization
  policy is appropriate

## What you get

A structured critique listing named safety failures (races, atomicity violations, visibility
gaps) and liveness failures (deadlock paths, lockout scenarios, starvation risks), each with
the hazard category identified and a targeted recommendation naming the applicable Lea
pattern or technique.

## Source

"Concurrent Programming in Java: Design Principles and Patterns" by Doug Lea,
Addison-Wesley, 1997.
Rights status: distillation-only. No verbatim quotation in generated artifacts.

## Package layout

```
subagents/java-concurrency-reviewer/
  profile.yaml                    canonical profile (source of truth)
  provenance-ledger.md            field-by-field derivation log
  CHANGELOG.md                    version history
  README.md                       this file
  tests/golden-tests.yaml         routing and output tests
```
