---
name: secure-development-lifecycle
kind: skill
status: ready
provenance:
  principles:
  - P016
  - P022
  - P023
  - P036
  - P048
  claims:
  - C00401
  - C00402
  - C00217
  - C00219
  - C00427
  - C00428
  - C00064
  - C00065
  - C00002
  - C00017
  evidence:
  - E00240
  - E00241
  - E00125
  - E00126
  - E00260
  - E00261
  - E00043
  - E00044
  - E00002
  - E00014
  source_anchors:
  - 3d98983ce864-c0012
  - 3d98983ce864-c0000
  - 3d98983ce864-c0014
  - 1a5b18f0f07e-c0001
  - 1a5b18f0f07e-c0002
  - 1a5b18f0f07e-c0000
  authored_from_digest: 89970baf9c85aed2097874db15b08e4242fc4d26606a8b0a5e0fdbbf022fd585
---

# Secure Development Lifecycle

Fold security into the lifecycle from the architecture phase, for the worst case. This skill
packages 5 grounded principles the application-security-reviewer applies when this surface is in
scope. Each finding names the weakness, the attack it enables, the countermeasure, and the trade-off
or residual risk.

## When this applies

- Designing or reviewing the architecture of a new application or feature.
- Designing or reviewing the architecture of a feature or system to be deployed at scale.
- The system stores or shares data among many users.
- Reviewing code or design for recurring insecure patterns.
- Designing provider-controlled API foundations or assigning security ownership.
- Starting or revising an API design, including private or internal APIs.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope:
identify where untrusted data or an access decision enters, name the attack it enables, apply the
countermeasure, and state the trade-off or residual risk. Never weaken a defence below what the
source supports, and never present a single control as complete security.

1. **P016 (high confidence).** Begin security in the architecture phase, before any code is written, by collecting and risk-evaluating all business requirements, building communication between security and engineering, and focusing on data flow — securing data in transit (require all network data encrypted, preferring TLS over deprecated SSL to…
2. **P022 (high confidence).** Design and review architecture for the worst case by assuming malicious users and accounting for the application's distributed nature; designing only for legitimate, well-intentioned users is a fatal flaw, and proper planning raises the cost of attack.
3. **P023 (high confidence).** Avoid the core secure-coding anti-patterns: do not ship temporary mitigations without a planned permanent fix, do not rely on blacklists (prefer whitelists, easing their maintenance with vetting), do not launch unevaluated boilerplate or default framework configuration (which can leak version information or ship…
4. **P036 (medium confidence).** Make the API provider responsible for the base security design early, including transport protection, authentication and authorization policy, session handling, delegation, and federation verification.
5. **P048 (medium confidence).** Build security into API designs from the outset, assuming even initially private APIs may later face public exposure.

## Anti-patterns to flag

- Trusting client-supplied data, or relying on a blacklist where a whitelist is possible.
- Leaving untrusted input un-parameterized, un-encoded, or rendered into a script/DOM sink.
- Presenting one control (a key, one flow, one header check) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P016, P022, P023, P036, P048. Every cited claim, evidence record, and source anchor
resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-
records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.

