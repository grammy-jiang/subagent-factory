---
name: interaction-verification
kind: skill
status: ready
provenance:
  principles:
  - PRP-004
  - PRP-007
  claims:
  - CL015
  - CL016
  - CL017
  - CL018
  - CL019
  - CL020
  - CL024
  - CL026
  source_anchors: []
  authored_from_digest: abc5d7d3b0efd52c507676277481fc779b3688cdd1e61ae7f143a4be08ed1501
---

# Interaction Verification

## Purpose

Assert that the class under test made (or did not make) the right side-effecting calls on its
collaborators — especially void/command methods — using `verify()`, invocation-count modes, and
`ArgumentCaptor` (PRP-004, PRP-007). Void methods return nothing, so verification of the call is
the only way to assert the side effect happened.

## When to use

- The collaborator method under test returns void and the contract is that a specific call is (or
  is not) made.
- Asserting how many times a method was called, or what argument values/ordering were passed.
- Testing error-handling branches where a void method must throw.

## Procedure

1. **Verify void/command calls with `verify()` (CL015, CL016, PRP-004).** Void mock methods are
   auto-stubbed and never reach the real implementation, so they return nothing to assert on. After
   the act phase, call `verify(mock).method(args)`; if the code under test never invoked it,
   `verify()` raises an exception, flagging the bug.
2. **Throw from a void method with `doThrow(...)` (CL020, CL024, PRP-004).** The
   `when().thenThrow()` syntax is invalid for void methods. Use
   `doThrow(exception).when(mock).voidMethod(args)` — e.g. to make a DAO `create()` fail and test a
   service's error-handling branch without a real database.
3. **Pin the invocation count (CL017, PRP-007).** `verify(mock).method(args)` defaults to
   `times(1)`. Use a mode when the count matters: `times(n)`, `never()`, `atLeastOnce()`,
   `atLeast(n)`, `atMost(n)`, `only()`, or `timeout(ms)`.
4. **Capture and assert arguments with `ArgumentCaptor` (CL026, PRP-007).** Build
   `ArgumentCaptor.forClass(T.class)`, pass `captor.capture()` inside the `verify()` call, then read
   `captor.getValue()` / `captor.getAllValues()`. `getAllValues()` returns captures in invocation
   order, which lets you assert argument content and sequencing (e.g. SQL parameters built internally).
5. **Use the "no interaction" assertions deliberately (CL018, CL019, PRP-007).**
   `verifyZeroInteractions(mock)` asserts no calls at all on a collaborator; `verifyNoMoreInteractions(mock)`
   asserts nothing beyond the calls already verified. Apply `verifyNoMoreInteractions()` selectively
   after the expected `verify()` calls — not as a blanket default, because over-specifying
   interaction makes tests fragile.
6. **Do not pile interaction checks onto a return-value test.** If the test already asserts a
   returned value, adding `verify()` on the same path tests the same thing twice and couples the
   test to implementation (`does_not_apply_when`). Prefer asserting the result for query methods.

## Inputs

- The void/command method(s) whose invocation (or non-invocation) is the contract under test.
- The expected call count and, where relevant, the argument values/ordering to assert.

## Output

`verify()` assertions (with the right count mode), `doThrow(...)` stubs for void error branches,
and `ArgumentCaptor` checks of argument content/order, scoped so the test is not over-specified.

## References

- (none — this package declares no reference docs.)

## Provenance

Principles PRP-004, PRP-007; claims CL015 (void auto-stub → verify), CL016 (`verify()` raises on
missing call), CL017 (count modes), CL018 (`verifyZeroInteractions`), CL019 (`verifyNoMoreInteractions`),
CL020 (`doThrow` for void), CL024 (void DAO error branch), CL026 (`ArgumentCaptor`, `getAllValues`
ordering). Distillation-only source; paraphrased, no verbatim quotation.
