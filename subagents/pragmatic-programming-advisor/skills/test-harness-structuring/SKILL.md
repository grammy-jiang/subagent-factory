---
name: test-harness-structuring
kind: skill
status: ready
provenance:
  principles:
  - P013
  - P041
  - P028
  - P068
  claims:
  - C00326
  - C00328
  - C00270
  - C00274
  - C00271
  - C00353
  - C00275
  - C00352
  source_anchors: []
  authored_from_digest: b0d26ba9764f837c9e7ce29411c98c791313a189667cb0971d0a12c4d39559d4
---

## Purpose

Structure a project's automated test suite so testing happens early, often, and
automatically — covering the full range of test types in the right order, and treating
"all tests pass" as the definition of done rather than an optional final step.

## When to use

- A team runs tests manually or infrequently and needs an automated strategy.
- A suite exists but its coverage of test types is unknown or lopsided.
- Setting the completion bar for a coding task ("when is this done?").
- Wiring tests into the build (pairs with `skills/build-and-release-automation/SKILL.md`).

## Procedure

### Step 1: Design contracts and tests before writing the module

Before implementing any module, design the module's contract and the tests that verify it
together (P028 / C00270). Write the tests first — this forces you to try the interface
before committing to it and surfaces boundary conditions early. Require that a module's
subcomponents are tested and passing before the module that depends on them is tested
(C00269): if subcomponent tests pass but the module test fails, the fault is localized to
the module or its use of those subcomponents.

When designing components intended for reuse, design them to be tested in the field, not
only at build time (C00265 / P028). Build testability in from the beginning and test each
piece thoroughly before wiring pieces together (C00266).

### Step 2: Establish the cadence — test early, test often, test automatically

Start running tests as soon as any production code exists rather than saving them for the
deadline (P041 / C00352). Automated tests that run with every build are far more effective
than a test plan sitting on a shelf; the earlier a bug is found, the cheaper it is to fix
(C00326).

Run tests automatically and interpret results automatically. Schedule infrequent tests
(such as stress tests) on a regular repeating basis rather than ad hoc. Always run tests
before checking code in (C00352).

Running tests is not optional — they must run, and run often (C00273 / P013).

### Step 3: Build a composable, reusable test harness

Build one standard test harness for the project that provides setup and teardown, test
selection, output analysis, and standardized failure reporting (C00274 / P013). Reuse an
existing framework such as xUnit rather than writing your own from scratch.

Make the full suite invocable as a single automated step so it can run on every build and
by every developer, not just on a special machine. Tests should return process exit codes
(zero for pass, nonzero for fail) so that they compose into larger automated test runs
(C00379 / P013).

Build internal test drivers freely even when nothing in the requirements calls for them,
such as a small script language that drives a component under test. Such drivers allow
quick and exhaustive testing (C00378 / P013).

### Step 4: Make tests easy to find and ship them with the code

Keep unit tests conveniently located — embedded in the source for small projects,
in a dedicated subdirectory for large ones (C00271 / P013). Tests that are hard to find go
unused; accessible test code also documents how to use the module.

Ship the tests with the code so you can diagnose problems in the field (C00272 / P013).
Build a test window into deployed software — consistent-format log files, a hot-key
diagnostic window, or a built-in web server for server code — so internal state can be
viewed without a debugger (C00276 / P013).

### Step 5: Test against the contract over boundary conditions

Write tests that verify each unit honors its contract over a wide range of inputs and
boundary conditions (C00268 / P028). Doing so reveals both whether the code meets the
contract and whether the contract means what you think it means.

Treat a unit test as code that exercises a module in isolation under controlled conditions,
checking results against known values or prior runs for regression testing (C00267 / P028).

### Step 6: Formalize ad hoc tests into the suite

When debugging produces a throwaway test, add it to the unit tests immediately rather than
discarding it (C00275 / P013). Code that broke once is likely to break again. This is also
the foundation of the "find bugs once" rule.

### Step 7: Enforce the done bar

A coding task is not finished until all available tests pass — you cannot claim code is
usable until it passes every available test (C00328 / P041). No one may declare code done
while tests are failing.

Write test code at the same time as or before the production code. A project may end up
with more test code than production code; treat that as worthwhile when it produces near-
zero defects (C00327 / P041).

### Step 8: Find bugs once — add a regression test for every defect

When a bug is found, modify the automated tests so that a human never has to find that
same bug again (C00353 / P068). Every bug found in the field or in review becomes a
permanent addition to the regression suite before the fix is committed.

## Inputs

- The current test inventory and how it is invoked.
- The module/integration boundary map (for ordering and contract design).
- The build system the suite will hook into (for cadence and automation).

## Output

- A test strategy naming which of the major test types are covered and the gaps.
- A design-before-code rule: contracts and tests authored before each module is implemented.
- A subcomponent-before-module ordering rule wired into the pipeline.
- A composable harness with exit-code-returning tests.
- A "done = all tests pass" completion gate.
- A practice of converting every found bug into a regression test immediately.

## References

- `references/test-type-taxonomy.md` — the major test types and what each verifies.
- `skills/build-and-release-automation/SKILL.md` — running the suite on every build.

## Provenance

Derived from principles P013 (make tests easy to find, ship with code, composable harness,
ad hoc formalization, test window, exit codes), P041 (test early, test often, test
automatically; write test code before or with production code; coding is not done until
all tests run), P028 (design to test; write tests before code; test against contract over
boundary conditions; test subcomponents first), and P068 (find bugs once; every found bug
gets an automated test so it is never found twice by a human). Key grounding claims:
C00326 (automated tests beat shelved test plans; earlier detection is cheaper),
C00328 (coding is not done until all tests run), C00270 (design contract and tests
together, write tests first), C00274 (build a standard composable harness; reuse xUnit),
C00271 (keep tests easy to find), C00353 (find bugs once via automated tests),
C00275 (formalize throwaway debug tests into the suite), and C00352 (start testing as
soon as any production code exists; run automatically before check-in).
Source is distillation-only; all wording is paraphrased.
