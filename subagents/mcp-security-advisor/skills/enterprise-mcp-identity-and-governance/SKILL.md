---
name: enterprise-mcp-identity-and-governance
kind: skill
status: ready
provenance:
  principles:
  - P011
  - P044
  - P079
  - P090
  - P107
  - P141
  - P142
  - P143
  - P165
  - P196
  claims:
  - C00225
  - C00226
  - C00278
  - C00279
  - C00354
  - C00355
  - C00487
  - C00488
  - C00494
  - C00495
  - C00499
  - C00500
  - C00508
  - C00509
  - C00523
  - C00538
  - C00541
  - C00542
  - C00818
  - C00820
  evidence:
  - E00189
  - E00190
  - E00223
  - E00224
  - E00299
  - E00300
  - E00388
  - E00389
  - E00393
  - E00394
  - E00398
  - E00399
  - E00407
  - E00408
  - E00417
  - E00431
  - E00432
  - E00433
  - E00658
  - E00660
  source_anchors:
  - 38612cf35377-c0000
  - 515304c317e3-c0002
  - 73827be00a9b-c0000
  - 8aab528164de-c0000
  - c8cf335ba0d6-c0000
  - dcbba5b2c9ad-c0001
  - fa0ccb38ff81-c0001
  authored_from_digest: 3269b9158306623c61d499868d1e7269451d552721cdf869e91e5907a6bbfe36
---

# Enterprise MCP Identity and Governance

Govern enterprise MCP identity — route authentication through the enterprise IdP/SSO, keep authorization policy under admin control, prefer IdP-mediated cross-app access, and prevent shadow or zombie servers.

This skill packages 10 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- Access is to enterprise-managed resources and an enterprise policy authority can approve integrations centrally.
- Access involves company-controlled accounts or enterprise application data.
- Current integration setup would require users to approve multiple redirect-based OAuth connections.
- A downstream MCP server is accessed through an enterprise SSO-backed service.
- Enterprise policy visibility is required for AI-client access to tools.
- An MCP client requests access to a downstream tool in an enterprise-managed environment.
- The client, enterprise IdP, and MCP authorization server support the enterprise-managed flow.
- When MCP connects an AI agent or model runtime to enterprise tools, services, or data sources.
- The parties can use the in-progress identity-chaining OAuth extension for the app-to-app access case.
- The requesting and resource applications are both configured for SSO with the relevant enterprise IdP.
- Enterprise policy already authorizes the requesting application to access the resource application for the user.
- Teams can create, expose, test, or operate MCP servers or AI infrastructure outside a tightly governed deployment path.
- The underlying application already supports enterprise SSO or can delegate login through an authorization server.
- An AI agent or MCP client is being rolled out inside an enterprise.
- The agent needs access to company-managed applications or data.
- Designing MCP authorization for scalable enterprise adoption.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P011 (medium confidence).** For enterprise app-to-app MCP access, put authorization policy under enterprise admin and IdP control instead of relying on each user to approve direct OAuth connections.
2. **P044 (medium confidence).** For enterprise MCP deployments, avoid direct client-to-server OAuth as the only control point when the enterprise IdP would lack visibility into downstream tool connections.
3. **P079 (medium confidence).** Treat MCP as a privileged enterprise integration layer and explicitly model trust boundaries for authentication, token movement, tool metadata, runtime execution, and supply-chain provenance.
4. **P090 (medium confidence).** Prefer IdP-mediated Cross-App Access or identity chaining for enterprise MCP app-to-app connections when the requesting and resource applications can rely on the same enterprise IdP policy domain.
5. **P107 (high confidence).** Prevent shadow MCP deployments by requiring central registration before deployment, CI/CD gates, owner and compliance metadata, continuous discovery, secure baseline templates, central IAM, service identities, segmentation, anomaly mo…
6. **P141 (medium confidence).** Integrate enterprise SSO by routing user authentication through the existing enterprise identity path behind the MCP authorization server, without changing the MCP client or resource server flow.
7. **P142 (medium confidence).** Treat enterprise-deployed MCP clients and AI agents as first-class enterprise applications that require SSO integration and central access governance.
8. **P143 (medium confidence).** Design enterprise-ready MCP authorization as a paired model: CIMD scales decentralized client identity, while Enterprise-Managed Authorization centralizes enterprise policy decisions.
9. **P165 (high confidence).** Continuously detect and eliminate shadow, zombie, and malicious MCP servers through automated discovery, a centralized inventory, and decommissioning, because absent provenance and inventory controls attackers deploy unauthorized serv…
10. **P196 (medium confidence).** Treat MCP's security as implementation-dependent rather than protocol-guaranteed: adopt it with caution and heightened scrutiny—drawing on lessons from prior distributed and plugin ecosystems—especially in national-security or other h…

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P011, P044, P079, P090, P107, P141, P142, P143, P165, P196. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
