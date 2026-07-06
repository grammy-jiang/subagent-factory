---
name: repository-readiness-and-agent-workflows
kind: skill
status: ready
provenance:
  principles:
  - P038
  - P039
  - P020
  - P071
  - P072
  - P073
  - P074
  - P059
  claims:
  - C00187
  - C00188
  - C00189
  - C00200
  - C00220
  - C00221
  - C00198
  - C00199
  - C00235
  - C00236
  - C00237
  - C00241
  - C00242
  - C00244
  - C00245
  - C00249
  - C00250
  evidence: []
  source_anchors: []
---

# Repository Readiness and Agent Workflows

## Purpose

Bootstrap a local coding-agent repository with explicit manifests, operating budgets, incident paths, and task-typed workflows before agents may edit source.

## When this applies

- For repositories where local agents may edit source code.
- For user-facing behavior, schema changes, security-sensitive code, or large refactors.
- When out-of-scope writes or sensitive-data exposure are detected.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Bootstrap each repository with explicit runtime metadata and core manifests that define constraints, conventions, data classes, enforcement hooks, success criteria, scope, quality gates, and cost policy. (P038)
2. Treat a repository as ready for local-agent editing only after sandboxing, inspectable policy, scoped writes, verification, audit trails, manifest review, AI-readiness scoring, and any needed readiness PR are complete. (P039)
3. Define operating budgets and incident paths before agent work begins, including limits for turns, tokens, tools, time, network, commands, human escalation, compaction triggers, quarantine, revert, secret rotation, trace replay, and labels for local-policy thresholds. (P020)
4. Use the spec-first workflow for high-impact production changes: check constraints, plan first, scope edits, verify, evaluate harness changes, and open a PR with trace evidence. (P071)
5. Use the test-first workflow for bug fixes: reproduce the failure, constrain implementation and test edits, verify focused and neighboring tests, and promote only reviewed recurring fix patterns. (P072)
6. Use the dependency-update workflow for package changes: inspect changelogs and advisories, update lockfiles in a sandbox, run tests and security/license scans, record transitive changes, and review postinstall scripts. (P073)
7. Use the documentation-only workflow for docs tasks: state target files, preserve wiki-link syntax when present, avoid generated and unrelated artifacts, validate Markdown when tooling exists, and report changed documents. (P074)
8. When an agent crosses scope or exposes sensitive data, stop and preserve evidence, revert only the offending agent changes, quarantine or rotate secrets as applicable, tighten controls, and add a regression or post-incident review. (P059)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P038** (medium) — Bootstrap each repository with explicit runtime metadata and core manifests that define constraints, conventions, data classes, enforcement hooks, success criteria, scope, quality gates, and cost policy.
- **P039** (medium) — Treat a repository as ready for local-agent editing only after sandboxing, inspectable policy, scoped writes, verification, audit trails, manifest review, AI-readiness scoring, and any needed readiness PR are complete.
- **P020** (medium) — Define operating budgets and incident paths before agent work begins, including limits for turns, tokens, tools, time, network, commands, human escalation, compaction triggers, quarantine, revert, secret rotation, trace replay, and labels for local-policy thresholds.
- **P071** (medium) — Use the spec-first workflow for high-impact production changes: check constraints, plan first, scope edits, verify, evaluate harness changes, and open a PR with trace evidence.
- **P072** (medium) — Use the test-first workflow for bug fixes: reproduce the failure, constrain implementation and test edits, verify focused and neighboring tests, and promote only reviewed recurring fix patterns.
- **P073** (medium) — Use the dependency-update workflow for package changes: inspect changelogs and advisories, update lockfiles in a sandbox, run tests and security/license scans, record transitive changes, and review postinstall scripts.
- **P074** (medium) — Use the documentation-only workflow for docs tasks: state target files, preserve wiki-link syntax when present, avoid generated and unrelated artifacts, validate Markdown when tooling exists, and report changed documents.
- **P059** (medium) — When an agent crosses scope or exposes sensitive data, stop and preserve evidence, revert only the offending agent changes, quarantine or rotate secrets as applicable, tighten controls, and add a regression or post-incident review.

