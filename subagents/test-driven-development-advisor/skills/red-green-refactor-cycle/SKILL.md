---
name: red-green-refactor-cycle
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P033
  - P017
  claims:
  - C00004
  - C00005
  - C00006
  - C00007
  - C00008
  - C00011
  - C00002
  - C00003
  - C00009
  - C00010
  - C00033
  source_anchors:
  - e619fe9a0394-c0000
  - e619fe9a0394-c0001
  authored_from_digest: 1768127b93af2fa5aa0b8067a61301bf4b38360bb58af769bb64b5647b500313
---

# Red-green-refactor cycle

## Purpose

Guide a developer through one complete iteration of the TDD cycle: write one small failing
test that specifies the next behaviour, run all tests to confirm the new one is the only
failing test, make the smallest change that gets every test to pass, then refactor to remove
the duplication the green solution introduced — before the next test begins. (P002)

The cycle also governs the order in which design emerges: each refactor step adds one design
decision to the code. The design grows organically from these small increments rather than
being sketched up front. (P017)

## When to use

- A developer asks what the next step is when adding a feature or fixing a bug test-first.
- A developer or team wants to verify that a recent change followed the cycle: failing test
 first, minimal change to green, refactoring before the next step.
- A developer is uncertain how large the next increment should be.
- A team is tempted to design the whole structure before writing any tests.

Do not use this skill when the work is a spike or throwaway exploration whose code will be
discarded, or when no automated test loop is feasible for the target.

## Procedure

### Phase 1 — Red: write one small failing test

1. **Identify the next behaviour to specify.** Pick the smallest behaviour not yet covered
 by a passing test. Consult the TDD to-do list if one exists; otherwise name the simplest
 case of the desired change.

2. **Invent the interface you wish you had.** Write the test as if the interface already
 exists. The test should assert one concrete outcome for one concrete input.

3. **Run all tests and confirm exactly the new test fails.** If more than the new test is
 failing, the starting point is already broken — fix that before proceeding.

4. **If the test passes immediately, it is not testing anything new.** Either the behaviour
 is already covered or the assertion is wrong. Revise until the bar is genuinely red for
 the right reason.

### Phase 2 — Green: make the bar pass as quickly as possible

5. **Make the smallest change that gets every test to pass.** Speed of reaching green
 dominates everything else at this step. A quick, temporarily ugly solution is acceptable
 here — the next phase removes it. 

6. **Do not try to write the clean or final solution yet.** Mixing "make it work" with
 "make it clean" slows both. Commit to getting green first, then refactoring.

7. **Choose a get-to-green strategy if the path is not obvious.** (See the
 `getting-to-green-strategies` skill for full guidance.)
 - *Obvious Implementation*: type the real code when it is clear and short.
 - *Fake It*: return a constant; the test will pass and duplication becomes explicit.
 - *Triangulation*: add a second example to force the abstraction if confidence is low.

8. **Run all tests and confirm every test is now green.** If an unexpected test is still
 failing, back up to a smaller or faked step rather than expanding the change.

### Phase 3 — Refactor: remove the duplication before the next test

9. **Identify the duplication the green solution introduced.** Look for literals duplicated
 between the test and the production code, repeated logic, or structural redundancy. (P001)

10. **Remove one piece of duplication at a time.** Each removal is a separate, focused
 edit — one design decision at a time. Run all tests after each edit to confirm the bar
 stays green. (P010)

11. **Do not add new behaviour during refactoring.** If a refactor reveals the need for
 another change, add it to the to-do list and finish the current refactor first.

12. **Confirm the bar is still fully green after all refactoring is complete.** Only then
 is the cycle finished and the next test may begin.

### Handling discoveries mid-cycle

13. **When new work surfaces mid-change, add it to the to-do list — do not pivot.** Stay
 on the current small step to completion. The to-do list ensures nothing is lost. (P009)

14. **Keep increments small.** If the current test is proving difficult to get to green,
 the increment is too large. Back up, break the behaviour into a simpler sub-case, and
 restart the cycle from Phase 1 with that smaller target. 

### Review mode: assess whether a change followed the cycle

15. **Check the order of events:** did a failing automated test exist before the production
 code was written? If not, the two rules were violated. (P002)

16. **Check the green change size:** was the change the smallest that could pass? A large
 change that skipped incremental steps is a signal that the cycle was bypassed.

17. **Check the refactor step:** was duplication introduced by the green solution removed
 promptly, before the next test was added? If duplication remains, the cycle is
 incomplete. (P004)

18. **Name each finding against the cycle phase it failed** (red, green, or refactor) so
 the correction is targeted.

## Inputs

- **Required:** the behaviour or change the developer wants to make; the current code or
 interface under test (or confirmation that none exists yet); the language and test
 framework in use.
- **Optional:** an existing TDD to-do list of tests still to write; a description of what
 has already passed and what remains.

## Output

A concrete next step named against the phase of the cycle it serves (red, green, or
refactor), with a brief rationale grounded in P001 or P010. Examples of expected output:

- *Red*: "Write a failing test that asserts `money.times(2)` returns a `Money` with amount 10."
- *Green*: "Return the constant `Money(10, 'USD')` to get the bar green; the duplication
 with the test makes the next refactor obvious."
- *Refactor*: "Replace the duplicated literal `10` in both test and production code with
 `amount * multiplier`; run all tests before the next step."

In review mode: a phase-labelled finding for each cycle violation, with the correction.

## References

- [tdd-to-do-list](../../references/tdd-to-do-list.md) — the companion reference for
 maintaining the running list of tests to write and refactorings to make, so nothing
 discovered mid-cycle is lost.

## Provenance

Derived from the red-green-refactor cycle principle **P002** and the two-rules principle
**P033** (write production code only for a failing test; then remove duplication), with the
small-steps / organic-design principle **P017** (claims **C00004**, **C00002**, **C00009**),
grounded in Kent Beck, *Test-Driven Development By Example* (Addison-Wesley, 2002) at chunk
anchors `e619fe9a0394-c0000` and `e619fe9a0394-c0001`.
Distillation-only source: paraphrased throughout, no verbatim quotation.
