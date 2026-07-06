---
name: runtime-governance-and-policy-layers
kind: skill
status: ready
provenance:
  principles:
  - P022
  - P010
  - P021
  - P027
  - P054
  - P055
  - P032
  - P052
  - P053
  - P026
  claims:
  - C00016
  - C00040
  - C00134
  - C00135
  - C00013
  - C00014
  - C00017
  - C00041
  - C00057
  - C00117
  - C00160
  - C00115
  - C00116
  - C00118
  - C00158
  - C00176
  - C00179
  - C00190
  - C00201
  - C00202
  - C00203
  - C00025
  - C00082
  - C00083
  - C00186
  - C00197
  - C00191
  - C00209
  - C00180
  - C00192
  - C00207
  - C00208
  evidence: []
  source_anchors: []
---

# Runtime Governance and Policy Layers

## Purpose

Govern agent behaviour with a deterministic, versioned policy and permission stack rather than trusting the model to remember the rules.

## When this applies

- implementing runtime governance.
- evolving agent tools, policies, behaviors, or cross-agent capabilities.
- composing agent permissions, policies, prompts, tools, agents, sessions, or delegated tasks.
- a harness has security-sensitive responsibilities.
- hardening pipelines against tampering, leakage, or nondeterministic decisions.
- When authoring skills or running a CLI without an equivalent native planning surface.
- tasks contain ambiguous ownership, scope, or authority boundaries.
- evaluating agent permission systems.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Implement runtime governance as a non-decomposable stack with policy evaluation, action interception, state tracking, audit logs, rollback, recovery, and staged capability rollout. (P022)
2. Compose permissions and policies with deny-first precedence and monotonic narrowing so delegation never expands authority. (P010)
3. Keep authentication, authorization, audit, cryptography, and final security decisions in deterministic wrapper code rather than model reasoning. (P021)
4. Encode agent policy in deterministic, versioned, verifiable layers instead of relying on the model to remember behavioral rules. (P027)
5. Apply manifest precedence monotonically: durable hard constraints outrank project policy, project policy outranks runtime overlays, overlays outrank skills, and skills outrank session plans. (P054)
6. Keep skills and session plans operationally scoped: skills encode reusable procedures with observable outcomes, and plans record the current task contract before edits. (P055)
7. Evaluate permission systems on unauthorized-operation rate, scope-overstep rate, ask-user cost, usability, and adaptive escape rate. (P032)
8. Require branch and review governance for agent work: agents use feature branches and agent-authored PRs require CI plus human review. (P052)
9. Run agents in a constrained sandbox that limits filesystem writes, network access, process resources, secret exposure, package installation, and protected branch writes. (P053)
10. Enforce structural least privilege through the tool graph: expose only needed capabilities, keep planning non-executing, scope adapters, and withhold commit authority until gates pass. (P026)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P022** (high) — Implement runtime governance as a non-decomposable stack with policy evaluation, action interception, state tracking, audit logs, rollback, recovery, and staged capability rollout.
- **P010** (high) — Compose permissions and policies with deny-first precedence and monotonic narrowing so delegation never expands authority.
- **P021** (high) — Keep authentication, authorization, audit, cryptography, and final security decisions in deterministic wrapper code rather than model reasoning.
- **P027** (medium) — Encode agent policy in deterministic, versioned, verifiable layers instead of relying on the model to remember behavioral rules.
- **P054** (medium) — Apply manifest precedence monotonically: durable hard constraints outrank project policy, project policy outranks runtime overlays, overlays outrank skills, and skills outrank session plans.
- **P055** (medium) — Keep skills and session plans operationally scoped: skills encode reusable procedures with observable outcomes, and plans record the current task contract before edits.
- **P032** (high) — Evaluate permission systems on unauthorized-operation rate, scope-overstep rate, ask-user cost, usability, and adaptive escape rate.
- **P052** (medium) — Require branch and review governance for agent work: agents use feature branches and agent-authored PRs require CI plus human review.
- **P053** (medium) — Run agents in a constrained sandbox that limits filesystem writes, network access, process resources, secret exposure, package installation, and protected branch writes.
- **P026** (medium) — Enforce structural least privilege through the tool graph: expose only needed capabilities, keep planning non-executing, scope adapters, and withhold commit authority until gates pass.

