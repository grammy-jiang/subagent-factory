---
name: mcp-client-identity-and-registration
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P054
  - P062
  - P065
  - P127
  - P191
  - P194
  - P206
  claims:
  - C00026
  - C00027
  - C00028
  - C00029
  - C00032
  - C00034
  - C00483
  - C00484
  - C00526
  - C00527
  - C00528
  - C00559
  - C00566
  - C00591
  - C00608
  evidence:
  - E00019
  - E00020
  - E00021
  - E00022
  - E00025
  - E00027
  - E00385
  - E00386
  - E00420
  - E00421
  - E00422
  - E00448
  - E00455
  - E00474
  - E00480
  source_anchors:
  - 0d5e0b52d96a-c0000
  - 8aab528164de-c0000
  - b5eaaf20d167-c0000
  - c8cf335ba0d6-c0000
  - ff3fcb8bc185-c0000
  authored_from_digest: 89de2b3754fe9e48d4fcfe86dd93f4fe2844323471e6cdbb6bcf9b0ef363567d
---

# MCP Client Identity and Registration

Manage MCP client identity at scale — Dynamic Client Registration scoping and abuse controls, Client ID Metadata Documents, and the priority order among client-registration mechanisms.

This skill packages 8 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- The authorization server exposes a dynamic registration endpoint.
- The ecosystem allows arbitrary or frequently added LLM clients and MCP servers.
- Previously unknown MCP clients need to initiate authorization against the server.
- The authorization platform supports a registration endpoint.
- An MCP client or workbench needs to onboard many or previously unknown MCP servers.
- An MCP authorization design proposes Dynamic Client Registration for an open or enterprise-facing ecosystem.
- Authorization servers accept Dynamic Client Registration from MCP clients.
- Clients depend on dynamically registered credentials.
- Client ID Metadata Documents are used for client identification.
- The service chooses Dynamic Client Registration for MCP client onboarding.
- Building or reviewing a production MCP authorization deployment.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P004 (medium confidence).** Use Dynamic Client Registration to onboard LLM clients without manual administrator pre-registration when MCP clients and services are numerous or frequently changing.
2. **P054 (medium confidence).** Treat Dynamic Client Registration as a risky default for broad MCP interoperability unless the server and client lifecycle controls are explicit.
3. **P062 (medium confidence).** If DCR is used, require abuse controls, bounded registration storage, a stale-registration policy, client recovery behavior, and a way to avoid repeated unnecessary registrations.
4. **P065 (high confidence).** When using Client ID Metadata Documents, host the metadata at an HTTPS URL that contains a path and whose client_id equals the URL exactly, include at least client_id/client_name/redirect_uris, and have the authorization server valida…
5. **P127 (medium confidence).** Support the three client-registration mechanisms and, when several are available, select in priority order: pre-registered credentials, then Client ID Metadata Documents (if the AS advertises support), then Dynamic Client Registration…
6. **P191 (medium confidence).** If Dynamic Client Registration is enabled for production MCP use, scope it to the MCP authorization server and prevent dynamically registered clients from gaining regular API access by default.
7. **P194 (medium confidence).** Authorization servers should fetch and cache (respecting HTTP cache headers) URL-formatted client_ids and advertise client_id_metadata_document_supported; clients should check that capability, may authenticate with private_key_jwt, an…
8. **P206 (medium confidence).** Treat the MCP authorization specification as a baseline and add production controls for multi-tenancy, auditability, SSO, DCR abuse, and token lifecycle management.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P004, P054, P062, P065, P127, P191, P194, P206. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
