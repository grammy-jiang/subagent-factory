---
name: mcp-threat-modeling-and-deployment-patterns
kind: skill
status: ready
provenance:
  principles:
  - P016
  - P035
  - P049
  - P052
  - P053
  - P074
  - P092
  - P095
  - P104
  - P105
  - P108
  - P113
  - P122
  - P129
  - P147
  - P160
  - P164
  - P167
  - P171
  - P183
  - P185
  - P197
  - P210
  claims:
  - C00023
  - C00024
  - C00118
  - C00119
  - C00120
  - C00123
  - C00140
  - C00141
  - C00170
  - C00171
  - C00215
  - C00216
  - C00238
  - C00259
  - C00382
  - C00383
  - C00394
  - C00413
  - C00552
  - C00553
  - C00651
  - C00652
  - C00663
  - C00664
  - C00722
  - C00723
  - C00742
  - C00743
  - C00823
  - C00841
  - C00856
  - C00857
  - C00863
  - C00864
  - C00872
  - C00873
  - C01017
  - C01018
  - C01178
  - C01180
  - C01196
  - C01197
  - C01215
  - C01217
  - C01289
  - C01290
  evidence:
  - E00016
  - E00017
  - E00097
  - E00098
  - E00099
  - E00102
  - E00115
  - E00116
  - E00138
  - E00139
  - E00182
  - E00183
  - E00200
  - E00213
  - E00327
  - E00328
  - E00338
  - E00351
  - E00442
  - E00443
  - E00517
  - E00518
  - E00526
  - E00527
  - E00575
  - E00576
  - E00593
  - E00594
  - E00663
  - E00676
  - E00681
  - E00682
  - E00683
  - E00684
  - E00689
  - E00690
  - E00815
  - E00816
  - E00866
  - E00868
  - E00881
  - E00882
  - E00894
  - E00895
  - E00939
  - E00940
  source_anchors:
  - 0d5e0b52d96a-c0000
  - 2c66587b05e5-c0000
  - 347696d03493-c0000
  - 357204ac930a-c0000
  - 38612cf35377-c0000
  - 457ef5c30a3b-c0000
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - 6954b21807d3-c0000
  - 6ff87e35998d-c0000
  - b5eaaf20d167-c0000
  - ceb67441a627-c0000
  - ceb67441a627-c0001
  - d59e5c41ce9d-c0000
  - d59e5c41ce9d-c0001
  - dcbba5b2c9ad-c0000
  - e6ab8dd9a85c-c0000
  authored_from_digest: ce03c4de2e32f79125bc53e3109aff47797459ba0e84d0af9864ec3f0bbfc1bf
---

# MCP Threat Modeling and Deployment Patterns

Threat-model MCP by deployment pattern — classify all-local / single-tenant / multi-tenant, map trust boundaries across host/client/server/transport, and account for MCP’s architectural weaknesses.

This skill packages 23 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- a tool or model receives parameters or forwarded inputs.
- An MCP server accepts parameters generated or influenced by an LLM.
- Scoping MCP security requirements, audits, mitigations, research agendas, or secure-by-design guidance.
- Creating or reviewing MCP server identity metadata, tools, resources, prompt templates, or capability handlers.
- Designing, reviewing, or testing an MCP integration or threat model.
- An agent can send messages or other data through a trusted connector.
- Earlier tool calls exposed chat history, contact lists, or other user communication data to the agent context.
- an MCP client receives an authorization URL from an MCP server.
- reviewing or designing any MCP deployment.
- assessing residual risk that protocol design imposes on an MCP deployment.
- An MCP host or client exposes external tools, data sources, or services to an LLM-driven workflow.
- The MCP integration is intended for non-developer or broad user adoption.
- The MCP server must call authenticated remote services.
- Designing or reviewing an MCP integration architecture.
- The control point currently governs tool calls but not pre-invocation metadata ingestion.
- a client is resolving authorization-server metadata from an issuer URL.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P016 (high confidence).** Validate every tool invocation and model-execution request against well-defined schemas, expected ranges, and the intended execution context (checking malformed inputs, missing fields, and excessive sizes), and block or restrict param…
2. **P035 (medium confidence).** Use lifecycle-centric MCP threat modeling that covers creation, deployment, operation, maintenance, attacker type, threat origin, consequence, supply-chain risk, and LLM-specific tool risks.
3. **P049 (medium confidence).** Treat MCP metadata, configuration, tool lists, resource lists, prompt templates, capability declarations, and handlers as security-critical artifacts that must be scoped and validated against implementation.
4. **P052 (high confidence).** Do not cache or persist authorization state and reuse it across tool invocations without a per-invocation, caller-scoped re-check; one-time authorization combined with server-level trust lets later calls inherit an authorized state re…
5. **P053 (high confidence).** Recognize that MCP middleware executes tools in its own execution context, so backend services authenticate only the MCP server's identity and cannot see the originating agent or the intent of individual invocations; therefore the MCP…
6. **P074 (high confidence).** Trace the control flow from each tool entry point to every operation that interacts with system, file, network, or physical resources — including sensitive operations reached transitively through helpers or libraries — and along each…
7. **P092 (medium confidence).** Model MCP integrations explicitly around host, client, server, transport, and the server capability classes of tools, resources, and prompts.
8. **P095 (medium confidence).** Before executing external-send tools, inspect and constrain outgoing arguments for unexpected destinations, hidden payloads, and inclusion of prior chat, contact, or history data.
9. **P104 (high confidence).** Allowlist authorization-URL schemes: permit only http/https (https in production), reject javascript:, data:, file:, vbscript: and other dangerous schemes, and prefer allowlist over blocklist validation to prevent XSS via malicious au…
10. **P105 (high confidence).** Before securing an MCP system, classify its deployment pattern (all-local, single-tenant hybrid, or multi-tenant cloud) and explicitly map the resulting trust boundaries, because security posture is set by where server code originates…
11. **P108 (high confidence).** Account for MCP's inherent architectural weaknesses when threat modeling: centralized credential stores are high-value targets, the spec lacks native fine-grained authorization, LLMs transform but do not sanitize malicious input, and…
12. **P113 (high confidence).** Review MCP deployments as agent-mediated security boundaries where model-selected tool calls can reach sensitive systems, not merely as conventional API integrations.
13. **P122 (medium confidence).** Avoid making user-facing MCP authorization depend on local server setup and plaintext API credentials; use an authorization flow that removes manual credential provisioning from the normal path.
14. **P129 (medium confidence).** Model MCP integrations around explicit host, client, server, data-source, and remote-service responsibilities so capability ownership and access boundaries stay clear.
15. **P147 (medium confidence).** Apply MCP security checks during connection and tool discovery, before server-provided metadata reaches the model, rather than waiting for explicit tool invocation.
16. **P160 (high confidence).** When discovering authorization-server metadata, clients MUST probe multiple well-known endpoints in the defined priority order, which differs depending on whether the issuer URL includes a path component.
17. **P164 (high confidence).** Open authorization URLs without a shell: never invoke cmd.exe/sh/PowerShell to open URLs, use platform non-shell openers, and web clients should apply a restrictive CSP (script-src/default-src 'self') to block injected JavaScript and…
18. **P167 (high confidence).** Separate sensitive MCP servers from general-purpose servers so payment, authentication, and personal-data capabilities are not exposed to broad shared contexts.
19. **P171 (high confidence).** Strictly validate and sanitize every input with allowlists at each trust boundary (path canonicalization, parameterized queries, context-aware output encoding for SQL/shell/HTML), treat AI-generated content as untrusted requiring the…
20. **P183 (high confidence).** Model MCP as a client-server protocol over stateful JSON-RPC 2.0 in which the host instantiates one client per server (n servers means n clients) and each client keeps a persistent session across RPC calls.
21. **P185 (high confidence).** Concentrate interception and approval at the Host as the policy enforcement point and security boundary (the LLM never touches a data source directly), and do not let Human-in-the-Loop approval be the only line of defense.
22. **P197 (medium confidence).** Map MCP server identities to their required permissions and remediate overprivileged servers before lower-impact posture findings.
23. **P210 (medium confidence).** Treat MCP tools as executable trust boundaries: declare structured inputs and validate or sanitize every user-controlled argument before using it.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P016, P035, P049, P052, P053, P074, P092, P095, P104, P105, P108, P113, P122, P129, P147, P160, P164, P167, P171, P183, P185, P197, P210. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
