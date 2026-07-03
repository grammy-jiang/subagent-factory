---
name: test-double-taxonomy
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P007
  - P039
  claims:
  - C00591
  - C00597
  - C00626
  - C00807
  - C00979
  source_anchors:
  - 11f28a2119c7-c0000
  - 140e06385751-c0000
  authored_from_digest: b5e9f25ce82cfabcf89899d17eb8f0f6e2ec4ba01914b144007d7f7523df484c
---

# Test-double taxonomy

A reference for the five kinds of test double, what each is for, and how it is verified. Use it with
the `selecting-test-doubles` skill. Terminology follows Meszaros, *xUnit Test Patterns*, reconciled
with Ammann & Offutt's taxonomy (P001, P007).

## The five doubles

| Double | Role | Provides indirect input? | Records/verifies indirect output? | Typical use |
|--------|------|--------------------------|-----------------------------------|-------------|
| **Dummy** | A placeholder that is never actually used | No | No | Fill a required parameter that the code path does not exercise |
| **Stub** | Returns pre-configured, fixed responses | Yes | No | Feed the SUT specific indirect inputs; set responses before exercising |
| **Fake** | A working but simplified implementation | Yes | No | Replace a slow/complex collaborator (e.g. in-memory store) deterministically, without encoding call order |
| **Spy** | A stub that also records how it was called | Yes | Records (assert afterwards) | Capture indirect outputs and assert on them after the exercise |
| **Mock** | Pre-programmed with expected calls; self-verifies | Optional | Verifies during/after exercise | Assert an interaction protocol (arguments, counts, order) is honoured |

**Saboteur** — a specialised stub/mock configured to raise an exception or return an error, used to
force a collaborator's exceptional behaviour that is hard or unsafe to trigger for real (P001).

## Choosing verification style

- **State verification** — assert the SUT's observable end state (return value, stored state). Prefer
  this when the value or state change *is* the behaviour.
- **Behaviour (interaction) verification** — assert the calls the SUT made. Reserve for genuine
  indirect outputs and collaboration obligations, and configure expectations only to the level the
  contract requires.

## Choosing the implementation of a double

Choose between hard-coded, configurable, generated, and dynamically-mocked doubles according to
reuse, variation across tests, language support, and readability — not habit (P039).

## Placement

Install every double through a substitutable dependency: prefer dependency injection, then
dependency lookup, and use test-specific hooks only as a last resort. Keep the double
API-compatible with the collaborator while implementing only the behaviour the test needs.

## Provenance

Distilled from Meszaros, *xUnit Test Patterns* (Test Double patterns; state vs behaviour
verification) and Ammann & Offutt's double taxonomy. Principles P001, P007, P039; claims C00591,
C00597, C00626, C00807, C00979; chunk anchors 11f28a2119c7-c0000, 140e06385751-c0000. Source is
distillation-only — no verbatim quotation; the table is a synthesized summary.
