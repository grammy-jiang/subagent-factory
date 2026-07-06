---
name: harness-architecture-and-scope
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P037
  - P029
  - P062
  - P047
  - P066
  - P036
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00026
  - C00130
  - C00132
  - C00153
  - C00174
  - C00175
  - C00185
  - C00052
  - C00089
  - C00090
  - C00059
  - C00060
  - C00096
  - C00152
  - C00058
  - C00168
  - C00173
  evidence: []
  source_anchors: []
---

# Harness Architecture and Scope

## Purpose

Treat the agent as a governed runtime harness — one execution envelope, not a prompt or model weight — and stage, compare, and evolve it as engineered infrastructure.

## When this applies

- building production-grade agent systems.
- comparing agent capability, reliability, or safety.
- designing, evaluating, or optimizing agent harnesses.
- staging practical harness implementation.
- planning factory or platform implementation work.
- comparing first-party and third-party agent harnesses.
- allocating model capacity inside a harness.
- routing memory operations is separable from main reasoning.
- building domain-specific agent systems with SMEs and developers.
- prioritizing rules from the synthesis.
- summarizing the state of the field after Iteration 9.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Design and evaluate AI agents as governed runtime harnesses, not as prompts or model weights in isolation. (P005)
2. Treat the local coding-agent harness as part of the product: it must control visibility, tool authority, write scope, failure detection, memory, cost, auditability, and final acceptance. (P037)
3. Stage harness implementation with observability, supply-chain security, context, storage, governance, verification, and monitoring before advanced self-evolution. (P029)
4. Do not presume first-party harnesses are superior overall; compare them empirically across the relevant reliability and affordance axes. (P062)
5. Use smaller control-plane models for routing, verification, monitoring, or memory routing only when the task is separable from creative reasoning and governance is preserved. (P047)
6. Use a staged SME-developer-agent process that produces reusable requirements, grounding, tool, reasoning-policy, prompt-architecture, and evaluation artifacts for domain-specific agents. (P066)
7. Weight rule confidence by domain evidence strength, and preserve partial/open gap status rather than overstating the synthesis. (P036)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P005** (high) — Design and evaluate AI agents as governed runtime harnesses, not as prompts or model weights in isolation.
- **P037** (medium) — Treat the local coding-agent harness as part of the product: it must control visibility, tool authority, write scope, failure detection, memory, cost, auditability, and final acceptance.
- **P029** (high) — Stage harness implementation with observability, supply-chain security, context, storage, governance, verification, and monitoring before advanced self-evolution.
- **P062** (medium) — Do not presume first-party harnesses are superior overall; compare them empirically across the relevant reliability and affordance axes.
- **P047** (medium) — Use smaller control-plane models for routing, verification, monitoring, or memory routing only when the task is separable from creative reasoning and governance is preserved.
- **P066** (medium) — Use a staged SME-developer-agent process that produces reusable requirements, grounding, tool, reasoning-policy, prompt-architecture, and evaluation artifacts for domain-specific agents.
- **P036** (medium) — Weight rule confidence by domain evidence strength, and preserve partial/open gap status rather than overstating the synthesis.

