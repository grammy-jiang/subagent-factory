---
name: api-design-and-lifecycle-governance
kind: skill
status: ready
provenance:
  principles:
  - P017
  - P019
  - P020
  - P026
  - P033
  - P037
  - P049
  claims:
  - C00143
  - C00144
  - C00044
  - C00045
  - C00069
  - C00070
  - C00076
  - C00077
  - C00006
  - C00011
  - C00042
  - C00043
  - C00018
  - C00019
  evidence:
  - E00096
  - E00097
  - E00033
  - E00034
  - E00048
  - E00049
  - E00055
  - E00056
  - E00006
  - E00009
  - E00031
  - E00032
  - E00015
  - E00016
  source_anchors:
  - 1a5b18f0f07e-c0004
  - 1a5b18f0f07e-c0001
  - 1a5b18f0f07e-c0002
  - 1a5b18f0f07e-c0000
  authored_from_digest: 3c491939fa377abf300669444321efc2dcf3c3e6e079c59c7d1b6b321519f42d
---

# Api Design And Lifecycle Governance

Govern the API across its lifecycle and layer its controls. This skill packages 7 grounded
principles the application-security-reviewer applies when this surface is in scope. Each finding
names the weakness, the attack it enables, the countermeasure, and the trade-off or residual risk.

## When this applies

- One user grants another user access to API-controlled data or physical device functionality.
- Classifying an API by intended audience and data sensitivity.
- Reviewing API implementation code, upload endpoints, or error responses.
- Migrating APIs to cloud infrastructure or adopting newer distributed architectures.
- Migrating existing APIs into cloud environments.
- Selecting API security mechanisms or user/group provisioning patterns.
- Selecting among private, public, and partner API models.
- Evaluating whether an API security design is sufficient.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope:
identify where untrusted data or an access decision enters, name the attack it enables, apply the
countermeasure, and state the trade-off or residual risk. Never weaken a defence below what the
source supports, and never present a single control as complete security.

1. **P017 (medium confidence).** For user-to-user sharing of connected-device access, do not rely on ordinary OAuth alone; use an added identity layer such as OpenID Connect to represent the resource owner, delegate, and scopes.
2. **P019 (medium confidence).** Favor private or partner API models for sensitive personal data or secure systems, and reserve public exposure for open data that does not connect to confidential systems.
3. **P020 (medium confidence).** Reject just-enough API code: validate inputs, prevent unsafe file upload behavior, avoid overbroad storage paths, handle errors safely, and suppress raw implementation diagnostics from external callers.
4. **P026 (medium confidence).** Reassess security assumptions when adopting microservices, API-management changes, or cloud infrastructure, including decentralization, physical control loss, backups, file security, and possible co-residency risks.
5. **P033 (medium confidence).** Prefer peer-reviewed, proven security standards and products over bespoke mechanisms, combining protocols such as OAuth, OpenID Connect, SCIM, JWT, strong second factors, and policy systems as the use case requires.
6. **P037 (medium confidence).** Choose API licensing and availability at the start of the lifecycle, matching exposure to the API purpose, data sensitivity, business model, upkeep capacity, and monetization goals.
7. **P049 (medium confidence).** Do not present API keys, OAuth adoption, or any single control as complete API security; require layered controls across enterprise, mobile, network, and API surfaces.

## Anti-patterns to flag

- Trusting client-supplied data, or relying on a blacklist where a whitelist is possible.
- Leaving untrusted input un-parameterized, un-encoded, or rendered into a script/DOM sink.
- Presenting one control (a key, one flow, one header check) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P017, P019, P020, P026, P033, P037, P049. Every cited claim, evidence record, and source
anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-
records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.

