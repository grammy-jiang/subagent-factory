---
name: get-to-green-then-refactor
kind: skill
status: ready
provenance:
  principles:
  - P004
  claims:
  - TDD-003
  - TDD-004
  - TDD-005
  source_anchors:
  - kent-beck-test-drive-47a4610a-h0024
  authored_from_digest: e8697e4a271773b3cbb656296991cd17e229df0627950254af51db38475bab19
---

# Get to green, then refactor

## Purpose

Guide a developer through the middle and final phases of a single TDD cycle iteration:
make the currently failing test pass as fast as possible using any means that works, then
immediately remove every piece of duplication that getting to green introduced. Keeping
these two moves in strict order — first pass, then clean — avoids the trap of trying to
design the perfect solution before any test is passing. (P004)

## When to use

- A failing test exists and the developer is deciding how to make it pass.
- A developer is stuck because they cannot see a clean implementation and have not yet
  reached a green bar.
- The bar just turned green and the question is what to clean up before writing the next
  test.
- Reviewing whether a change followed the discipline: green first, refactor second, never
  entangled.

Do not apply this skill when no failing test yet exists — the preceding step (writing the
failing test) belongs to the `red-green-refactor-cycle` skill.

## Procedure

### Phase 1 — Get to green

1. **Confirm the bar is red.** Run all tests. Verify that exactly the new test fails and
   all previously passing tests still pass. If anything unexpected is red, stop and treat
   it as a separate problem before proceeding.

2. **Choose a get-to-green strategy.** Select the approach that matches current confidence
   (see `getting-to-green-strategies` skill for full guidance):
   - *Obvious Implementation* — if the real code is clear and quick to type, type it in.
   - *Fake It* — if the real code is not yet clear, return a hard-coded constant that
     satisfies the assertion. Generalise only when a second example forces it.
   - *Triangulation* — if you need justification for an abstraction, write a second example
     first, then let both examples drive the generalisation together.
   - On an unexpected red bar while using Obvious Implementation, back up immediately to
     Fake It and take smaller steps.

3. **Make the change.** Write only enough production code to turn the bar green. Resist the
   pull to also clean the code or add behaviour not yet demanded by a test. The goal in this
   phase is speed to green, not elegance. A temporarily ugly solution is acceptable — but
   only temporarily. (TDD-005)

4. **Run all tests.** Confirm every test passes. If any test is still red, remain in Phase 1
   — do not begin refactoring on a red bar.

### Phase 2 — Refactor

5. **Identify the duplication introduced.** With the bar green, examine the code that just
   changed. Look for:
   - Duplicated literals or constants that now appear in both the test and the production
     code (the classic sign of a Fake It solution).
   - Repeated logic or structure across methods or classes.
   - Any other structural noise that was accepted to reach green quickly.

6. **Remove one piece of duplication at a time.** Make a single, small refactoring move.
   Do not restructure the entire design in one pass. Each move should leave the code
   slightly cleaner without altering observable behaviour.

7. **Run all tests after each refactoring move.** The bar must stay green throughout. If a
   refactoring move causes a failure, revert it immediately and find a smaller move. A red
   bar during refactoring means the change altered behaviour, not just structure.

8. **Repeat steps 6–7** until no further duplication remains that was introduced by getting
   to green. Stop when the code is as clean as it needs to be for the next test — not
   perfectly architected, but free of the shortcuts taken in Phase 1.

9. **Record any follow-on work discovered.** If you notice additional tests to write,
   further refactorings, or design questions that surfaced during this step, add them to the
   TDD to-do list rather than acting on them now. Stay on the current small step. (See
   `tdd-to-do-list` reference.)

10. **Hand off to the next red step.** With the bar green and duplication removed, the cycle
    is complete for this increment. The next action is to pick the next item from the to-do
    list and write the next small failing test.

### Decision branch — Refactoring reveals a larger design issue

If step 5 or 6 uncovers a structural problem that cannot be fixed with small moves while the
bar stays green:

- Do not attempt a large restructuring on the current green bar.
- Add a to-do list item describing the design concern.
- Finish removing the immediate duplication from this cycle.
- Address the structural issue in a future cycle once it is driven by a failing test or a
  concrete refactoring opportunity with its own green bar.

## Inputs

- The code change that just turned the bar green (production code and test code).
- The full test suite and its current pass/fail state (must be all-green before refactoring
  begins).
- The TDD to-do list, so that newly noticed work is captured rather than acted on
  mid-cycle.

## Output

A concrete, ordered sequence of actions for the current cycle iteration:

- **During green phase:** the specific change (or Fake It constant) to make, named against
  the strategy chosen, with the rationale — including why speed to green takes priority over
  elegance at this moment. (TDD-004)
- **During refactor phase:** each individual duplication to remove, in order, with a
  check-the-bar reminder after each move.
- **At handoff:** confirmation that the bar is green and duplication is cleared, plus any
  items to add to the to-do list before the next failing test is written.

Each step names whether it belongs to the green or refactor phase so the developer always
knows where in the cycle they are.

## References

- [red-green-refactor-cycle](../red-green-refactor-cycle/SKILL.md) — the full cycle,
  including the preceding step (writing the failing test) that produces the red bar this
  skill starts from.
- [getting-to-green-strategies](../getting-to-green-strategies/SKILL.md) — detailed
  guidance on choosing between Fake It, Obvious Implementation, and Triangulation for step 2
  of this skill's procedure.
- [tdd-to-do-list](../../references/tdd-to-do-list.md) — the running list where newly
  discovered tests and refactorings are captured at step 9 rather than acted on mid-cycle.

## Provenance

Derived from principle **P004** (claims **TDD-003**, **TDD-004**, **TDD-005**), grounded
in the general TDD cycle description at the head of Chapter 2 of Kent Beck's
"Test-Driven Development By Example" (anchor
`kent-beck-test-drive-47a4610a-h0024`).
Distillation-only source: paraphrased throughout, no verbatim quotation.
