---
name: stub-query-methods
kind: skill
status: ready
provenance:
  principles:
  - PRP-003
  claims:
  - CL012
  - CL013
  - CL014
  source_anchors: []
  authored_from_digest: 6d0bbfac56ef94f25ae79da475f0450da722d44c2dd4d7fadbee0473ece784d1
---

# Stub Query Methods

## Purpose

Control the return value of a collaborator's value-returning (query) methods so the class under
test can be driven down a specific code path (PRP-003). Stubbing replaces a real call with a
chosen result, keeping the test deterministic and isolated.

## When to use

- Stubbing a collaborator method that returns a value so the subject can proceed down a target path.
- Controlling return values for query methods in Arrange–Act–Assert tests.

## Procedure

1. **Stub the value with `when(...).thenReturn(...)` (CL013, PRP-003).** Identify the method with
   `Mockito.when(mock.method(args))` and supply the result with `.thenReturn(value)`; use argument
   matchers where the exact input is not fixed.
2. **Choose the stubbing action by intent (CL014):** Mockito offers four actions —
   `thenReturn(value)` for a fixed result; `thenThrow(throwable)` to raise an exception from a
   non-void method; `thenAnswer(answer)` only when the result must be computed from the arguments;
   `thenCallRealMethod()` only for partial mocks (spies). Prefer `thenReturn` and reach for the
   others only when the scenario genuinely needs them.
3. **Know the unstubbed default (CL012).** An unstubbed mock method silently returns the type's
   default: `false` for boolean, `null` for objects, `0` for int/long. Rely on that default only
   when the return value is irrelevant to the scenario; otherwise stub it explicitly so the test's
   intent is visible.
4. **Stay on query methods.** This skill is for value-returning methods. Void methods take the
   `doThrow/doReturn/doAnswer` family and are asserted with `verify()` — see interaction-verification
   (PRP-004). Never stub a method on the class under test itself; mocks are for collaborators.

## Inputs

- The collaborator query method to stub and the value (or computed answer/exception) it must yield.
- Whether the default unstubbed return is acceptable for the scenario.

## Output

A stubbed collaborator that returns the chosen value (or throws) for the test's inputs, with the
stubbing action matched to intent.

## References

- (none — this package declares no reference docs.)

## Provenance

Principle PRP-003; claims CL012 (default unstubbed returns), CL013 (`when().thenReturn()`),
CL014 (the four stubbing actions). Distillation-only source; paraphrased, no verbatim quotation.
