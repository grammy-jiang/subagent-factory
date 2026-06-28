---
name: assertion-programming-patterns
kind: skill
status: ready
provenance:
  principles:
  - P045
  - P031
  - P059
  - P029
  - P035
  claims:
  - C00183
  - C00184
  - C00185
  - C00186
  - C00181
  - C00182
  - C00160
  - C00188
  source_anchors: []
  authored_from_digest: e9345c9b52a7bdfe276e0d4e52eff0218327a152c2a2a7d14499abc1be64a80f
---

## Purpose

Place assertions correctly: verify every "this can't happen" assumption, keep assertions
free of side effects, leave them enabled where they earn their keep, and decide how a
program should react when an impossible state is nonetheless reached.

## When to use

- Reviewing or writing code that contains an implicit "this case is impossible" assumption.
- A defect surfaced from a state the author believed unreachable.
- Deciding whether assertions should be compiled out of production builds.
- Encoding Design-by-Contract clauses as runtime checks (paired with
  `design-by-contract-authoring`).

## Procedure

1. **Find the silent assumptions.** Scan for any place the code assumes a condition cannot
   occur: a switch with no default, an "always non-null" value, an index always in range,
   a value that "must" be positive. Each such assumption is a candidate assertion. Every
   switch or case statement without a default clause is a concrete gap to close (P031,
   C00181).

2. **Assert the assumption explicitly.** If you think something can never happen, add an
   assertion to ensure it will not (P045, C00183). An explicit assertion fails loudly at
   the source of the violated assumption rather than allowing corrupted state to propagate
   downstream.

3. **Keep assertions side-effect free.** Never put an expression that changes program
   state inside an assertion condition. If the assertion can be disabled, a side-effecting
   condition creates a Heisenbug — the program behaves differently with and without the
   check (P045, C00185).

4. **Do not use assertions for error handling.** Assertions guard conditions that should
   never happen. Expected runtime conditions — bad input, missing file, network failure —
   are handled by real error handling, not by assert. Blurring this boundary weakens both
   mechanisms (P045, C00184).

5. **Decide the production posture deliberately.** Accept that testing never exercises
   more than a tiny fraction of real permutations and that production exposes conditions
   no test reached (P059, C00160). Leave assertions enabled in production where cost
   allows; if you must turn off specific assertions for a measured performance cost,
   document which ones and why. Do not disable assertions wholesale on the assumption that
   testing already caught everything (P045, C00186).

6. **Crash early on the impossible.** When an assertion detects a truly impossible state,
   treat the program as no longer viable and terminate it as soon as possible — everything
   it does afterward is suspect (P031, C00182). A dead program does far less damage than a
   crippled one writing corrupted data or driving a device into a bad state (P031, C00181).
   Use exceptions only to clean up resources during the termination path, not to recover
   and continue (P035, C00188).

7. **Apply complementary defensive idioms.** Assertions are one layer. Apply defensive
   coding practices around them: validate all inputs before processing, never pass
   unvalidated data to functions that assert clean input, and null out pointer or object
   references immediately after freeing or finishing with them so that stale references
   raise an error rather than silently corrupting state (P029).

## Inputs

- The code path containing the implicit assumption.
- The build configuration (whether assertions are stripped in release).
- Any contract clauses from `design-by-contract-authoring` that require runtime enforcement.

## Output

- Added or located assertions guarding each "impossible" assumption.
- A flag on any side-effecting or error-handling misuse of assert.
- A documented decision on production assertion posture and crash-early behaviour.

## References

- `skills/design-by-contract-authoring/SKILL.md` — what to assert (preconditions,
  postconditions, invariants).
- `references/pragmatic-tips-70-cheatsheet.md` — If It Can't Happen, Use Assertions;
  Crash Early.

## Provenance

Derived from principles P045 (assertive programming: guard impossibilities, no side
effects, stay on in production, never substitute for error handling), P031 (crash early:
a dead program does far less damage than a crippled one), P059 (accept imperfect software;
code defensively), P029 (defensive coding idioms), and P035 (exceptions only for
exceptional problems). Claims used: C00183 (assert the impossible), C00184 (assertions
are not error handling), C00185 (no side effects in assertions), C00186 (leave assertions
on in production), C00181 (crash early: detect and terminate), C00182 (impossible state
means terminate immediately), C00160 (accept imperfect software), C00188 (exceptions only
for exceptional events). Source is distillation-only; all wording is paraphrased.
