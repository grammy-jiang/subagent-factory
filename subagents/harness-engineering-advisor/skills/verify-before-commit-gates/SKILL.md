---
name: verify-before-commit-gates
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P033
  - P044
  - P046
  - P060
  - P014
  - P067
  - P068
  - P056
  - P041
  - P045
  - P035
  claims:
  - C00007
  - C00008
  - C00022
  - C00042
  - C00043
  - C00091
  - C00136
  - C00106
  - C00148
  - C00159
  - C00181
  - C00194
  - C00213
  - C00054
  - C00021
  - C00079
  - C00080
  - C00081
  - C00150
  - C00195
  - C00243
  - C00211
  - C00212
  - C00251
  - C00252
  - C00253
  - C00175
  - C00182
  - C00184
  - C00204
  - C00246
  evidence: []
  source_anchors: []
---

# Verify-Before-Commit Gates

## Purpose

Gate every state-changing action behind external, formal, or executable verification, and treat a failing gate as authoritative.

## When this applies

- actions can affect external state, memory, tools, or user-visible artifacts.
- task intent can be represented as specifications or invariants.
- formal or executable verification is available.
- a harness has properties expressible through temporal logic, TLA+, Hoare-style contracts, preconditions, postconditions, or equivalent checks.
- When code changes are safety-, security-, workflow-, schema-, or authorization-sensitive.
- choosing a verification strategy.
- generators are optimized against learned or proxy verifiers.
- learned or agentic judges are used in acceptance workflows.
- validating learned execution environments or virtual test runners.
- When the DryRUN pattern is part of the verification gate.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Gate state-changing actions with external, programmatic, formal, or executable verification before committing them. (P008)
2. Convert formal lifecycle, state, task, and component invariants into automated harness gates where those properties are expressible. (P033)
3. Use deterministic verification as the acceptance authority, with a minimum gate covering formatting or linting, tests, secret scanning, SAST, dependency scanning, and domain invariants. (P044)
4. For high-risk changes, add domain-specific external guards such as state-machine invariants, schema compatibility checks, authorization tests, property checks, or formal safety properties. (P046)
5. Prefer external verification over unstructured self-feedback, allowing structured self-verification only when the source condition makes checking easier than generation. (P060)
6. Harden learned or agentic verifiers with process monitors, maker-checker separation, explicit terminal states, real-execution benchmarks, and iterative verifier updates. (P014)
7. Add maintainability gates that can reject behavior-correct patches for poor locality, duplicated paths, mixed responsibilities, bad dependencies, unclear state ownership, or boundary-crossing side effects. (P067)
8. Use the safe-refactor workflow when behavior must be preserved: characterize existing behavior, freeze interfaces, scope edit tools, run invariants and public-output checks, and reject unapproved behavior changes. (P068)
9. Use DryRUN for change verification by recording intended behavior, expected files, representative cases, predicted effects, risks, and invariants before test results, then repairing or explaining mismatches before commit. (P056)
10. When verification, budget, or supply-chain gates fail, treat the gate as authoritative: stop or block merge, compare evidence, fix faulty verifiers separately, checkpoint or split over-budget work, and require provenance-backed clean rebuilds for supply-chain alerts. (P041)
11. Evaluate harness changes by holding the model and runtime constant while varying manifests, tool scope, permissions, or verification gates. (P045)
12. Evolve harness behavior only as a measured experiment: vary one harness variable with the model fixed, use held-out tasks and regression checks, keep only improvements without new regressions, and preserve rollback. (P035)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P008** (high) — Gate state-changing actions with external, programmatic, formal, or executable verification before committing them.
- **P033** (high) — Convert formal lifecycle, state, task, and component invariants into automated harness gates where those properties are expressible.
- **P044** (medium) — Use deterministic verification as the acceptance authority, with a minimum gate covering formatting or linting, tests, secret scanning, SAST, dependency scanning, and domain invariants.
- **P046** (medium) — For high-risk changes, add domain-specific external guards such as state-machine invariants, schema compatibility checks, authorization tests, property checks, or formal safety properties.
- **P060** (high) — Prefer external verification over unstructured self-feedback, allowing structured self-verification only when the source condition makes checking easier than generation.
- **P014** (high) — Harden learned or agentic verifiers with process monitors, maker-checker separation, explicit terminal states, real-execution benchmarks, and iterative verifier updates.
- **P067** (medium) — Add maintainability gates that can reject behavior-correct patches for poor locality, duplicated paths, mixed responsibilities, bad dependencies, unclear state ownership, or boundary-crossing side effects.
- **P068** (medium) — Use the safe-refactor workflow when behavior must be preserved: characterize existing behavior, freeze interfaces, scope edit tools, run invariants and public-output checks, and reject unapproved behavior changes.
- **P056** (medium) — Use DryRUN for change verification by recording intended behavior, expected files, representative cases, predicted effects, risks, and invariants before test results, then repairing or explaining mismatches before commit.
- **P041** (medium) — When verification, budget, or supply-chain gates fail, treat the gate as authoritative: stop or block merge, compare evidence, fix faulty verifiers separately, checkpoint or split over-budget work, and require provenance-backed clean rebuilds for supply-chain alerts.
- **P045** (medium) — Evaluate harness changes by holding the model and runtime constant while varying manifests, tool scope, permissions, or verification gates.
- **P035** (medium) — Evolve harness behavior only as a measured experiment: vary one harness variable with the model fixed, use held-out tasks and regression checks, keep only improvements without new regressions, and preserve rollback.

