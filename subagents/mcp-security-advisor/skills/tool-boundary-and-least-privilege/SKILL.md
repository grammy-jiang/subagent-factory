---
name: tool-boundary-and-least-privilege
kind: skill
status: ready
provenance:
  principles:
  - P025
  - P027
  - P028
  - P032
  - P111
  - P112
  - P156
  - P182
  - P201
  claims:
  - C00113
  - C00114
  - C00153
  - C00190
  - C00191
  - C00194
  - C00333
  - C00334
  - C00395
  - C00396
  - C00423
  - C00424
  - C00425
  - C00426
  - C00435
  - C00436
  - C00951
  - C00952
  evidence:
  - E00094
  - E00095
  - E00125
  - E00157
  - E00158
  - E00161
  - E00278
  - E00279
  - E00339
  - E00340
  - E00357
  - E00358
  - E00359
  - E00360
  - E00364
  - E00365
  - E00754
  - E00755
  source_anchors:
  - 347696d03493-c0002
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - c82772e8c087-c0000
  - d59e5c41ce9d-c0000
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0001
  authored_from_digest: d7e780b1d9c663609e9bd0e5ae56a391eff9b36bd383ca5bd6bb81ed1a08d249
---

# Tool Boundary and Least Privilege

Treat MCP tools as the primary security boundary — narrow, single-purpose, task-required tools with per-tool authorization, and explicit human confirmation for critical or irreversible actions.

This skill packages 9 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- when agents operate across trust boundaries or can invoke sensitive operations.
- A proposed MCP tool call can delete, modify, spend, transfer, disclose, or otherwise affect sensitive resources.
- MCP-connected tools can run commands or make changes in sensitive environments.
- when actions can be destructive, financial, administrative, externally visible, or otherwise high impact.
- the action is critical, high-impact, or irreversible.
- MCP clients, agents, tools, servers, users, or services authenticate, authorize, invoke tools, or access data.
- designing or reviewing MCP tool interfaces.
- human-in-the-loop confirmation is a control for risky MCP actions.
- the client offers one-click configuration that executes local MCP server commands.
- when configuring agent tool access.
- An LLM can autonomously sequence MCP tools or pass one tool's output into another across systems.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P025 (high confidence).** Enforce authentication and authorization at the per-tool level for every tool that can reach a sensitive operation; missing per-tool checks enable unauthorized access to sensitive operations.
2. **P027 (high confidence).** Avoid auto-approving command execution in MCP-enabled environments, especially where commands can affect sensitive data, local systems, development workspaces, or production infrastructure.
3. **P028 (high confidence).** Gate critical, high-impact, or irreversible actions behind explicit human confirmation before execution (Plan-then-Execute pre-execution gating, with a two-person rule for the highest-impact actions), accepting the efficiency loss for…
4. **P032 (high confidence).** Enforce strong MCP authentication and authorization with mutual authentication, short-lived scoped and bound tokens, server-side validation, per-request deny-by-default RBAC or ABAC, lifecycle controls, least privilege, centralized IA…
5. **P111 (high confidence).** Treat tools as the primary security boundary: give each tool a single, explicitly bounded purpose, prefer narrow purpose-built tools over powerful general ones (e.g., a prepared statement over arbitrary SQL), and never delegate securi…
6. **P112 (high confidence).** Make security-relevant elicitations clear about their implications and do not rely solely on the human user; where the risk of dangerous tool execution is unacceptable, enforce host/client configurations that unprivileged users cannot…
7. **P156 (high confidence).** Gate one-click local MCP server configuration behind explicit, fully transparent consent: show the exact untruncated command, flag it as code execution on the user's machine, require approval with a cancel option, and highlight danger…
8. **P182 (high confidence).** Grant agents only task-required tools, and constrain each tool by explicit resources and operations instead of broad wildcard permissions.
9. **P201 (medium confidence).** Constrain cross-tool composition with explicit approval, inter-tool data-flow limits, state validation, integrity checks, rollback, and anomaly detection for suspicious multi-step chains.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P025, P027, P028, P032, P111, P112, P156, P182, P201. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
