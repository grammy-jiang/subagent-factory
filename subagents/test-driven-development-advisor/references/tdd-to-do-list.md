---
name: tdd-to-do-list
kind: reference
status: ready
provenance:
  principles:
  - P010
  - P006
  - P009
  claims:
  - C00108
  - C00109
  - C00110
  - C00111
  - C00112
  - C00113
  - C00114
  - C00115
  - C00063
  - C00064
  - C00065
  - C00067
  source_anchors:
  - e619fe9a0394-c0005
  - e619fe9a0394-c0002
  authored_from_digest: 8e42a2043dd33d54732b11e6f250a04e1aff7a647695496377472a08cd8f5e22
---

# TDD to-do list

A lightweight working artifact used throughout a TDD session to track pending tests and
refactorings, keep the developer focused on one step at a time, and signal completion when
the list is empty.

## What it is

The TDD to-do list is a running, ordered collection of work items maintained alongside the
code during a test-driven development session. It has two categories of entry:

- **Tests still to write** — behaviours not yet covered by a failing test.
- **Refactorings still to make** — duplication or design problems noticed but deferred so
 the current test could reach green first.

The list is not a backlog or a project plan. It is a focus device for a single working
session: short, disposable, and expected to be empty when the session is complete.

## What goes on it

| Item type | When to add | Example entry |
|-----------|-------------|---------------|
| Planned test | Before the session begins, when listing the behaviours needed | `$5 + 10 CHF = $10 if rate is 2:1` |
| Planned test | At any point a new case is identified that would verify the design | `Money rounding?` |
| Refactoring note | When a code smell or duplication is noticed but cannot be addressed now | `Dollar side-effects?` |
| Refactoring note | After getting to green when cleanup was deliberately deferred | `Make "amount" private` |

A new item is added the moment it is noticed — mid-test, mid-implementation, mid-refactor —
so nothing is lost and the current step is not interrupted.

## How items move through the list

| State | Convention | Meaning |
|-------|------------|---------|
| Pending | Plain text | Identified but not yet started |
| In progress | **Bold** (or otherwise highlighted) | The one item being worked on right now |
| Done | ~~Strikethrough~~ | Completed and verified |

Only one item is in progress at a time. When a test passes and its refactoring is complete,
the item is crossed off. The developer then picks the next item from the remaining list and
makes it the active one.

## Relationship to the red/green/refactor cycle

The to-do list and the cycle interlock:

1. **Before red** — choose the next pending test from the list; make it in-progress.
2. **Red** — write the failing test for that item; run all tests and confirm failure.
3. **Green** — make the smallest change to pass; if new smells appear, add them to the list
 rather than fixing them now.
4. **Refactor** — remove the duplication introduced; cross off the item when clean.
5. **Repeat** — pick the next pending item; if the list is empty, the session is done.

The list enforces the discipline of working one test at a time: side-discoveries go onto the
list instead of derailing the current step.

## Checklist: is the to-do list being used well?

| Check | Pass condition |
|-------|----------------|
| List is written before the first test | At least the planned tests for the session are listed up front |
| Exactly one item is in-progress at any moment | No two items are simultaneously being worked on |
| Newly noticed tests and refactorings are added immediately | Nothing discovered mid-step is held only in memory |
| Items are crossed off only after green + refactor | Completion is not declared while tests are still failing or duplication remains |
| List is empty at session end | All planned and discovered items have been completed or explicitly deferred to a future session |

## When the list ends non-empty

If items remain at the end of a session, they are carried forward explicitly — not abandoned.
Carrying them forward is preferable to rushing the remaining items and leaving duplication
unrefactored. An incomplete list is not a failure; an unrefactored green bar is.

## Provenance

Built from the list-the-tests-first principle **P010**, the never-more-than-one-change-from-green
principle **P006**, and the back-out-to-green principle **P009** (claims **C00108**, **C00112**,
**C00063**), grounded in Kent Beck, *Test-Driven Development By Example* (Addison-Wesley, 2002)
at chunk anchors `e619fe9a0394-c0005` and `e619fe9a0394-c0002`.
Source is distillation-only; this reference paraphrases and restructures the demonstrated
technique — no verbatim quotation is present.
