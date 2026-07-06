---
name: multi-agent-and-self-evolution
kind: skill
status: ready
provenance:
  principles:
  - P023
  - P024
  - P063
  claims:
  - C00034
  - C00048
  - C00095
  - C00105
  - C00051
  - C00111
  - C00112
  - C00131
  - C00138
  evidence: []
  source_anchors: []
---

# Multi-Agent Coordination and Governed Self-Evolution

## Purpose

Coordinate multiple agents with explicit routing and shared-state consistency, and constrain any harness self-evolution with formal guardrails and rollback.

## When this applies

- multiple agents collaborate on shared work or shared state.
- agent systems can modify harness components, skills, or harness code.
- adding governance structure to self-evolving modules.
- preserving peer privacy or reducing social attack vectors.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Coordinate multi-agent systems with explicit routing, artifact coherence, controlled delegation, shared-state consistency, and compatibility checks. (P023)
2. Constrain self-evolution and meta-harness search with formal guardrails, verified fallbacks, local contracts, compatibility checks, staged rollout, rollback, and attention to diminishing returns. (P024)
3. Balance peer identity anonymization against accountability requirements in multi-agent systems. (P063)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P023** (high) — Coordinate multi-agent systems with explicit routing, artifact coherence, controlled delegation, shared-state consistency, and compatibility checks.
- **P024** (high) — Constrain self-evolution and meta-harness search with formal guardrails, verified fallbacks, local contracts, compatibility checks, staged rollout, rollback, and attention to diminishing returns.
- **P063** (medium) — Balance peer identity anonymization against accountability requirements in multi-agent systems.

