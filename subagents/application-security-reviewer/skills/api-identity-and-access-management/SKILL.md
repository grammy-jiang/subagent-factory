---
name: api-identity-and-access-management
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P005
  - P011
  - P018
  - P021
  - P027
  - P029
  - P032
  - P034
  - P035
  - P044
  - P050
  claims:
  - C00012
  - C00013
  - C00158
  - C00159
  - C00147
  - C00148
  - C00024
  - C00027
  - C00095
  - C00096
  - C00137
  - C00138
  - C00415
  - C00416
  - C00001
  - C00003
  - C00008
  - C00009
  - C00131
  - C00132
  - C00274
  - C00275
  - C00086
  - C00087
  evidence:
  - E00010
  - E00011
  - E00111
  - E00112
  - E00100
  - E00101
  - E00019
  - E00020
  - E00068
  - E00069
  - E00090
  - E00091
  - E00251
  - E00252
  - E00001
  - E00003
  - E00007
  - E00008
  - E00085
  - E00086
  - E00151
  - E00152
  - E00061
  - E00062
  source_anchors:
  - 1a5b18f0f07e-c0000
  - 1a5b18f0f07e-c0004
  - 1a5b18f0f07e-c0002
  - 1a5b18f0f07e-c0003
  - 3d98983ce864-c0013
  - 3d98983ce864-c0004
  authored_from_digest: e28fa354a052fd5f0b9befdebccf081f95b04cd3ea5b4cdf550b812f043b509c
---

# Api Identity And Access Management

Review API security as an identity-and-access-management system. This skill packages 12 grounded
principles the application-security-reviewer applies when this surface is in scope. Each finding
names the weakness, the attack it enables, the countermeasure, and the trade-off or residual risk.

## When this applies

- APIs or partner applications must reuse authenticated identity data across trusted services or organizations.
- Clients need authenticated user attributes, authentication context, federation, profile sharing, or modern OpenID migration.
- API traffic crosses a network boundary or carries sensitive information.
- Choosing encryption or transport-security protocols for API traffic.
- Many APIs or microservices must support delegated access to another user’s resources.
- Explaining, designing, or reviewing an API access-control architecture.
- Designing OAuth access-token representation, dereferencing, or proof-of-possession behavior.
- Microservices need user context without exposing readable value tokens over public boundaries.
- Designing or reviewing storage and verification of passwords, credentials, PII, or financial data.
- Assessing or designing security for APIs that expose valuable resources or interact with mobile, enterprise, IoT, or microservice systems.
- Designing, reviewing, or troubleshooting OAuth-based API integrations.
- A third-party client needs access to a user-controlled resource.
- Designing identity and access management for independent services.
- Selecting or reviewing an authentication mechanism.
- Planning OAuth or OpenID Connect for APIs that expose protected data.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope:
identify where untrusted data or an access decision enters, name the attack it enables, apply the
countermeasure, and state the trade-off or residual risk. Never weaken a defence below what the
source supports, and never present a single control as complete security.

1. **P029 (high confidence).** Protect credentials and sensitive data: enforce password strength by entropy (reject common-list passwords and any derived from the user's name, birthdate, or address rather than counting special characters), never store passwords in plain text but hash them with a deliberately slow algorithm such as BCrypt or…
2. **P044 (high confidence).** Choose authentication schemes that resist interception and replay: avoid HTTP basic auth because base64 is encoding not encryption and its credentials leak easily, prefer hashed schemes with replay defenses, couple authentication with two-factor authentication, and weigh that an OAuth provider compromise can cascade…
3. **P002 (medium confidence).** Add OpenID Connect and identity-provider federation when an OAuth-based API solution needs standardized user identity, authentication context, or cross-domain trust.
4. **P005 (medium confidence).** Prefer modern public-key-backed transport security for network APIs, validate key ownership, avoid plain symmetric-key use over networks, and use TLS over SSL whenever possible.
5. **P011 (medium confidence).** Prefer delegated tokens over API-side access tables for microservice-heavy user-to-user delegation, while accounting for application token-management complexity.
6. **P018 (medium confidence).** Keep authentication, authorization, federation, and delegation conceptually separate and apply each only to the responsibility it actually serves.
7. **P021 (medium confidence).** Choose token transport and profile by security need: use reference tokens when data should remain server-side, avoid bearer tokens when proof of presenter identity is required, prefer Holder-of-Key over custom proof schemes, and avoid obsolete MAC token drafts without strong external justification.
8. **P027 (medium confidence).** Expose reference tokens externally, translate them at an edge authentication server or API firewall, and pass JWTs internally when microservices need distributed identity.
9. **P032 (medium confidence).** Review API security as an identity and access-management system that includes the API, surrounding organization, servers, mobile clients, IoT devices, and microservice interactions.
10. **P034 (medium confidence).** Use OAuth for delegated access only, and model OAuth integrations around the client, authorization server, resource owner, and resource server responsibilities.
11. **P035 (medium confidence).** For microservices, avoid repeating monolithic per-service authentication; use OAuth delegation and OpenID Connect identity where clients need user context or backend sessions.
12. **P050 (medium confidence).** Deploy OAuth and OpenID Connect inside a broader security and identity-management program that also protects servers, mobile clients, networks, firewalls, and cloud infrastructure.

## Anti-patterns to flag

- Trusting client-supplied data, or relying on a blacklist where a whitelist is possible.
- Leaving untrusted input un-parameterized, un-encoded, or rendered into a script/DOM sink.
- Presenting one control (a key, one flow, one header check) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P002, P005, P011, P018, P021, P027, P029, P032, P034, P035, P044, P050. Every cited
claim, evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are
distillation-only: paraphrased, never quoted.

