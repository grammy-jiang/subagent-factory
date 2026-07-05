---
name: audit-logging-and-runtime-monitoring
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P031
  - P039
  - P040
  - P060
  - P075
  - P081
  - P097
  - P174
  - P180
  - P187
  - P200
  - P203
  - P212
  - P213
  claims:
  - C00154
  - C00197
  - C00198
  - C00223
  - C00281
  - C00282
  - C00319
  - C00320
  - C00345
  - C00346
  - C00696
  - C00697
  - C00795
  - C00796
  - C00822
  - C00823
  - C00879
  - C00881
  - C00882
  - C00883
  - C01001
  - C01002
  - C01141
  - C01143
  - C01146
  - C01154
  - C01184
  - C01186
  - C01284
  - C01326
  evidence:
  - E00126
  - E00164
  - E00165
  - E00187
  - E00226
  - E00227
  - E00264
  - E00265
  - E00290
  - E00291
  - E00549
  - E00550
  - E00641
  - E00642
  - E00662
  - E00663
  - E00696
  - E00698
  - E00699
  - E00700
  - E00800
  - E00801
  - E00840
  - E00842
  - E00843
  - E00849
  - E00871
  - E00873
  - E00936
  - E00956
  source_anchors:
  - 2c66587b05e5-c0000
  - 2c66587b05e5-c0001
  - 347696d03493-c0000
  - 347696d03493-c0001
  - 347696d03493-c0004
  - 38612cf35377-c0000
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - 515304c317e3-c0002
  - b4bcb3ed0e87-c0000
  - c5ec2b54074b-c0000
  - ceb67441a627-c0000
  - cf7957044f40-c0000
  - fa0ccb38ff81-c0000
  - fa0ccb38ff81-c0001
  authored_from_digest: ae15f98c6afbe183fa4de4ab592524ac97efa4d961d14f21883981651e9b2714
---

# Audit Logging and Runtime Monitoring

Make MCP accountable — log tool invocations with parameters and originating prompt at every layer, protect log integrity, monitor for injection symptoms and resource abuse, and prioritise remediation by real attack paths.

This skill packages 15 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- operating MCP in any environment requiring troubleshooting, forensics, or accountability.
- operating MCP where compliance, accountability, or forensics is required.
- operating MCP servers, especially in multi-tenant environments.
- Reviewing whether an MCP server is subject to caller identity confusion.
- MCP clients, servers, agents, or tools handle tokens, API keys, service credentials, prompts, logs, traces, context memory, or vector stores that may contain secrets.
- MCP systems perform autonomous actions, access sensitive data, make decisions, or operate under compliance, security, or forensic requirements.
- Running MCP servers after deployment or applying patches, upgrades, credential changes, resource address changes, or policy updates.
- assessing or monitoring MCP server maintenance and attack surface.
- Evaluating or designing MCP defenses for production, enterprise, or benchmarked environments.
- MCP servers are permitted to request LLM completions that consume user or organization quota.
- an MCP deployment incurs metered LLM, tool, or API cost.
- MCP tools execute host-level commands, scripts, binaries, or other operations whose misuse could affect files, networks, databases, or runtime resources.
- building detection or permission models for agent tool calls.
- A client records or displays tool execution to the user or reviewer.
- A trusted tool call could carry redirected recipients, hidden arguments, or concealed data movement.
- When ranking MCP security findings or deciding which exposed servers to fix first.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P015 (high confidence).** Log tool invocations with their parameters and originating prompt at every layer (host, client, server), centralize cross-cutting logging via MCP gateways or proxies, keep immutable records of actions and authorizations (e.g., IdP tok…
2. **P031 (high confidence).** Do not infer authorization correctness from the presence of authorization logic, specific APIs, or framework constructs; authorization state may be cached in memory, held as a global flag, tied to a session, or embedded in initializat…
3. **P039 (high confidence).** Handle MCP credentials as ephemeral, scoped, vault-backed secrets: inject them only at runtime, keep them out of model context and stored diagnostics, redact sensitive records, audit credential flows, and rotate immediately on suspect…
4. **P040 (high confidence).** Make MCP audit and telemetry complete enough for accountability and incident response: capture structured action and context evidence, protect log integrity, forward telemetry to central monitoring, preserve privacy through redaction…
5. **P060 (medium confidence).** Maintain MCP servers with auditable version control, controlled configuration changes, authenticated compatible updates, local-configuration preservation, rollback, access auditing, and integrity-protected logs.
6. **P075 (high confidence).** Judge an MCP server's security posture from repository signals - project size, lines of code, and commit history - and continuously monitor maintenance: about 21.9% of servers are inactive over a year (an unpatched long tail) and over…
7. **P081 (medium confidence).** Benchmark MCP defenses across multiple attack types, hosts, and client configurations, then prefer layered defenses combining identity, policy, scanning, detection, arbitration, logging, firewalling, gateways, and isolation.
8. **P097 (medium confidence).** Detect resource-abuse attempts by comparing sampled-token volume and sampling frequency against operation-specific baselines and caps.
9. **P174 (high confidence).** Enforce resource-consumption controls—token, context-size, and API-call quotas plus cost management—to prevent resource-exhaustion denial of service and denial-of-wallet, since the protocol specifies none by default.
10. **P180 (high confidence).** Monitor MCP command execution for injection symptoms by correlating forbidden syntax, failed validation, privilege-escalation primitives, suspicious process arguments, abnormal syscall patterns, unexpected outbound traffic, sensitive…
11. **P187 (high confidence).** Assume the malicious action will be performed by a legitimate, already-registered tool while the poisoned tool is never executed; do not gate solely on 'new or unknown tool', because that stealth pattern is chosen specifically to look…
12. **P200 (medium confidence).** Audit logs and tool-call displays should reveal actual destinations, arguments, and data movements so malicious behavior cannot hide behind ordinary trusted-tool usage.
13. **P203 (medium confidence).** Prioritize MCP remediation using real attack paths that combine identity, network reachability, runtime privilege, and connected data sensitivity.
14. **P212 (medium confidence).** Filter and monitor MCP intent mapping and command execution so requests match declared capabilities and tool calls remain structured, serialized, monitored, and isolated.
15. **P213 (medium confidence).** Validate Tool-Poisoning robustness against live, real-world MCP servers and toolsets, not simulated environments; simulated IPI-style benchmarks understate the ecosystem-level TPA threat.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P015, P031, P039, P040, P060, P075, P081, P097, P174, P180, P187, P200, P203, P212, P213. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
