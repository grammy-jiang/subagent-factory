---
name: context-and-memory-engineering
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P070
  - P001
  - P006
  - P019
  - P043
  - P051
  - P057
  - P058
  - P031
  - P069
  claims:
  - C00031
  - C00032
  - C00109
  - C00110
  - C00133
  - C00140
  - C00151
  - C00164
  - C00238
  - C00035
  - C00097
  - C00162
  - C00163
  - C00230
  - C00232
  - C00011
  - C00012
  - C00033
  - C00036
  - C00037
  - C00092
  - C00093
  - C00094
  - C00183
  - C00202
  - C00226
  - C00227
  - C00234
  - C00084
  - C00085
  - C00233
  - C00231
  - C00239
  - C00240
  - C00086
  - C00087
  - C00170
  - C00229
  evidence: []
  source_anchors: []
---

# Context and Memory Engineering

## Purpose

Engineer context and persistent memory as governed runtime resources with budgets, schema-grounded records, gated writes, and preserved provenance.

## When this applies

- agent sessions accumulate context over time.
- multi-agent or long-horizon systems need selective context sharing.
- documents are repeatedly fed to agents.
- memory must support planning, diagnosis, causal recall, state update, or structured records.
- agents write persistent or cross-session memory.
- memory can influence future behavior.
- When deciding whether a lesson belongs in long-term project memory or a skill.
- memory must handle changing facts over time.
- evaluating long-term personal or organizational agent memory.
- When a memory lookup concerns exact project facts.
- When storing durable project memory records.
- claiming dynamic memory architecture selection.
- mixed workloads require different memory capabilities.
- When multiple agents or subagents operate on related artifacts.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Engineer context as a runtime resource with real-time budgets, staged compaction, selective routing, and structure-preserving document formats. (P007)
2. Compact context in stages by warning on budget pressure, retaining relevant ranges, pruning resolved dead ends, summarizing repeated traces, and checkpointing before hard-limit restarts. (P070)
3. For agentic project memory, store facts as schema-grounded, tool-retrievable records (causal or bi-temporal where applicable) instead of unverified natural-language / authoritative prose summaries. (P001)
4. Treat persistent memory as governed state: separate mutable records from immutable history, gate writes, scope reads, monitor drift, and preserve provenance. (P006)
5. Promote lessons into durable memory only when they are structured, causal, tool-retrievable, triggered by concrete conditions, testable, rollbackable, owned, and durable across tasks. (P019)
6. Preserve superseded memory records with provenance rather than deleting them when memory must handle temporal conflict. (P043)
7. Answer exact project-fact questions by querying validated memory records and re-promote only durable records into manifests or skills. (P051)
8. On memory writes, validate every required field, preserve source links, record unknowns and rejected options, and make the update reviewable like code. (P057)
9. Use cache and retrieval conservatively: cache only permitted stable material, prefer narrow symbol or file search, never cache secrets, and re-validate retrieved memory before edits. (P058)
10. Do not claim dynamic memory selection is solved unless a meta-router actually routes among memory substrates by task capability. (P031)
11. Use artifact ownership states in multi-agent workflows so agents know when they may edit, when they may only read, and when they must re-read stale state. (P069)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P007** (high) — Engineer context as a runtime resource with real-time budgets, staged compaction, selective routing, and structure-preserving document formats.
- **P070** (medium) — Compact context in stages by warning on budget pressure, retaining relevant ranges, pruning resolved dead ends, summarizing repeated traces, and checkpointing before hard-limit restarts.
- **P001** (high) — For agentic project memory, store facts as schema-grounded, tool-retrievable records (causal or bi-temporal where applicable) instead of unverified natural-language / authoritative prose summaries.
- **P006** (high) — Treat persistent memory as governed state: separate mutable records from immutable history, gate writes, scope reads, monitor drift, and preserve provenance.
- **P019** (medium) — Promote lessons into durable memory only when they are structured, causal, tool-retrievable, triggered by concrete conditions, testable, rollbackable, owned, and durable across tasks.
- **P043** (medium) — Preserve superseded memory records with provenance rather than deleting them when memory must handle temporal conflict.
- **P051** (medium) — Answer exact project-fact questions by querying validated memory records and re-promote only durable records into manifests or skills.
- **P057** (medium) — On memory writes, validate every required field, preserve source links, record unknowns and rejected options, and make the update reviewable like code.
- **P058** (medium) — Use cache and retrieval conservatively: cache only permitted stable material, prefer narrow symbol or file search, never cache secrets, and re-validate retrieved memory before edits.
- **P031** (high) — Do not claim dynamic memory selection is solved unless a meta-router actually routes among memory substrates by task capability.
- **P069** (medium) — Use artifact ownership states in multi-agent workflows so agents know when they may edit, when they may only read, and when they must re-read stale state.

