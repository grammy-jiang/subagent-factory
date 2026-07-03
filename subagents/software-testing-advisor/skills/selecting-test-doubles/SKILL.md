---
name: selecting-test-doubles
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P007
  - P013
  - P020
  - P024
  - P026
  - P037
  - P044
  - P071
  claims:
  - C00591
  - C00597
  - C00626
  - C00509
  - C00650
  - C00656
  - C00648
  - C00663
  source_anchors:
  - 11f28a2119c7-c0000
  - 140e06385751-c0000
  authored_from_digest: 7464a63f8b735ddf50284ac137d9dd72789e2cb931f3a0e85162ada35436bb3c
---

# Selecting and placing test doubles

## Purpose

Choose the specific kind of test double a situation calls for, install it through a substitutable
dependency, and configure it to only the level the contract requires — so collaborators are
isolated without over-specifying the test. Grounds the advice in Meszaros's *xUnit Test Patterns*
and Ammann & Offutt's double taxonomy (P001, P007).

## When to use

- A real collaborator is slow, unavailable, nondeterministic, unimplemented, hard to configure, or
  performs an unrecoverable action, and must be replaced for the test (P007).
- The developer is unsure which double to use — dummy, stub, mock, spy, or fake (P001).
- A collaborator's failure path (an exception, timeout, or error) is hard or unsafe to trigger with
  the real dependency (P071).
- A review finds interaction verification used where the observable result is what matters (P026).

## Procedure

1. **Decide whether a double is warranted.** Replace a collaborator only when it is slow,
   unavailable, nondeterministic, unimplemented, or must be observed indirectly; otherwise prefer
   the real object and keep at least one integration path that exercises it (P007).
2. **Pick the kind by what the test needs to control or observe** (P001, P013, P020, P026):
   - *Indirect input* the SUT reads from the collaborator → a **stub** that returns fixed data;
     configure its responses before exercising the SUT (P020).
   - *Indirect output* — a call the SUT makes that must be checked → a **spy** (records the calls
     for later assertion) or a **mock** (verifies expected calls). Configure expectations only to
     the level the contract requires (P013).
   - *A complex or slow collaborator* needing realistic-but-deterministic behaviour without
     encoding call order → a **fake** (a working, simplified implementation) (P037).
   - *An unused parameter* that only has to exist → a **dummy** (P001).
   - *A forced failure* (exception/error) that is hard to trigger for real → a **saboteur** (P071).
3. **Prefer state over interaction verification.** Verify the observable end state when that is the
   behaviour; reserve behaviour (interaction) verification for genuine indirect outputs and
   collaboration obligations (P026).
4. **Install the double through a substitutable dependency.** Prefer dependency injection, then
   dependency lookup, and use test-specific hooks only as a last resort; keep the double
   API-compatible with the collaborator while implementing only the behaviour the test needs
   (P024, P044).
5. **Name the choice against its principle** and state the failure it prevents (e.g. brittle
   over-mocking, or a test that passes despite a broken collaboration).

## Inputs

- The SUT and the collaborator to isolate, what the SUT reads from or does to it, and whether the
  test cares about a returned value/state or a call protocol.

## Output

A recommendation naming the double (dummy / stub / mock / spy / fake / saboteur), where and how to
inject it, what it should return or verify, and whether to verify by state or interaction — each
tied to the principle it follows.

## References

- `references/test-double-taxonomy.md` — the dummy/fake/stub/mock/spy comparison table.

## Provenance

Distilled from Meszaros, *xUnit Test Patterns* (double patterns, indirect input/output, state vs
behaviour verification, saboteurs, substitutable dependencies) and Ammann & Offutt's double
taxonomy. Principles P001, P007, P013, P020, P024, P026, P037, P044, P071; claims C00591, C00597,
C00626, C00509, C00650, C00656, C00648, C00663; chunk anchors 11f28a2119c7-c0000, 140e06385751-c0000.
Source is distillation-only — no verbatim quotation.
