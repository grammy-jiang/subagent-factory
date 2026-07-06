---
name: evaluation-and-benchmark-integrity
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P011
  - P028
  - P040
  - P025
  claims:
  - C00019
  - C00020
  - C00045
  - C00046
  - C00076
  - C00077
  - C00078
  - C00101
  - C00102
  - C00103
  - C00104
  - C00149
  - C00196
  - C00214
  - C00215
  - C00216
  - C00217
  - C00218
  - C00219
  - C00222
  - C00223
  - C00224
  - C00225
  - C00204
  - C00205
  - C00247
  - C00126
  - C00127
  - C00128
  - C00129
  evidence: []
  source_anchors: []
---

# Evaluation and Benchmark Integrity

## Purpose

Evaluate the harness on a multidimensional reliability surface and audit benchmarks for reward hacking rather than trusting pass@1 or leaderboard rank.

## When this applies

- using, publishing, or interpreting benchmarks for harness comparison or deployment reliability.
- searching, maintaining, or updating an iterative research corpus in a young or shifting field.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Audit harness benchmarks for reward hacking and report fixed-model metadata, ablations, reliability, robustness, determinism, security, cost, rubric quality, chaos cases, and checkpoint scores. (P002)
2. Maintain local evaluations from realistic work: include hidden edge checks, fail-to-pass and pass-to-pass tests, manifest regressions, ambiguity cases, original prompts when privacy allows, hidden solutions, relevance checks, flaky-test exclusion, harness condition records, and rolling refresh. (P011)
3. Use multiple evaluation signals; do not rely solely on pass-at-one, public tests, model leaderboard rank, or agent self-rating. (P028)
4. Test prompt-like artifacts as behavior specifications: state required and forbidden behavior with examples, add visible and hidden tests, semantic mutations, trace assertions, generated-file checks, refusal or clarification checks, regression runs, evidence, and rollback notes. (P040)
5. Search emerging research areas with expanded term atlases, direct identifier ingestion, coverage audits, and promotion of relevant exploratory shortlists. (P025)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P002** (high) — Audit harness benchmarks for reward hacking and report fixed-model metadata, ablations, reliability, robustness, determinism, security, cost, rubric quality, chaos cases, and checkpoint scores.
- **P011** (medium) — Maintain local evaluations from realistic work: include hidden edge checks, fail-to-pass and pass-to-pass tests, manifest regressions, ambiguity cases, original prompts when privacy allows, hidden solutions, relevance checks, flaky-test exclusion, harness condition records, and rolling refresh.
- **P028** (medium) — Use multiple evaluation signals; do not rely solely on pass-at-one, public tests, model leaderboard rank, or agent self-rating.
- **P040** (medium) — Test prompt-like artifacts as behavior specifications: state required and forbidden behavior with examples, add visible and hidden tests, semantic mutations, trace assertions, generated-file checks, refusal or clarification checks, regression runs, evidence, and rollback notes.
- **P025** (high) — Search emerging research areas with expanded term atlases, direct identifier ingestion, coverage audits, and promotion of relevant exploratory shortlists.

