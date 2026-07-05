---
name: tool-poisoning-and-metadata-integrity
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P005
  - P009
  - P010
  - P012
  - P037
  - P048
  - P050
  - P061
  - P082
  - P084
  - P088
  - P089
  - P093
  - P109
  - P115
  - P116
  - P134
  - P138
  - P146
  - P155
  - P170
  - P175
  - P184
  - P202
  - P211
  - P214
  - P215
  claims:
  - C00145
  - C00146
  - C00183
  - C00184
  - C00220
  - C00229
  - C00240
  - C00241
  - C00301
  - C00302
  - C00385
  - C00390
  - C00691
  - C00692
  - C00693
  - C00694
  - C00696
  - C00697
  - C00698
  - C00702
  - C00703
  - C00705
  - C00718
  - C00719
  - C00721
  - C00727
  - C00742
  - C00743
  - C00744
  - C00747
  - C00748
  - C00750
  - C00752
  - C00753
  - C00756
  - C00757
  - C00826
  - C00831
  - C00918
  - C00919
  - C00932
  - C00933
  - C00968
  - C00969
  - C01022
  - C01023
  - C01026
  - C01027
  - C01142
  - C01148
  - C01149
  - C01159
  - C01163
  - C01169
  evidence:
  - E00119
  - E00120
  - E00150
  - E00151
  - E00186
  - E00193
  - E00202
  - E00203
  - E00246
  - E00247
  - E00330
  - E00334
  - E00544
  - E00545
  - E00546
  - E00547
  - E00549
  - E00550
  - E00551
  - E00555
  - E00556
  - E00558
  - E00571
  - E00572
  - E00574
  - E00579
  - E00593
  - E00594
  - E00595
  - E00598
  - E00599
  - E00601
  - E00602
  - E00603
  - E00606
  - E00607
  - E00665
  - E00670
  - E00727
  - E00728
  - E00737
  - E00738
  - E00771
  - E00772
  - E00818
  - E00819
  - E00822
  - E00823
  - E00841
  - E00845
  - E00846
  - E00853
  - E00855
  - E00860
  source_anchors:
  - 347696d03493-c0002
  - 347696d03493-c0003
  - 357204ac930a-c0000
  - 38612cf35377-c0000
  - 457ef5c30a3b-c0000
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - 515304c317e3-c0002
  - 6954b21807d3-c0000
  - c5ec2b54074b-c0000
  - c5ec2b54074b-c0001
  - cf7957044f40-c0000
  - dcbba5b2c9ad-c0000
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0000
  authored_from_digest: 102fea42bd4862cc1d679e8bcc6882d005b808864b94948d834648e7b3d4888e
---

# Tool Poisoning and Metadata Integrity

Treat tool metadata as an attack surface — tool descriptions, names, schemas, and tools/list responses are untrusted; screen, pin, hash, and re-review them, and defend against tool poisoning, line jumping, shadowing, and rug pulls.

This skill packages 28 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- A client connects to a malicious, compromised, or unreviewed MCP server.
- A client would otherwise load tool descriptions without showing or checking the full model-visible text.
- Server-provided tool metadata is about to be admitted to model context or a risky tool call may execute.
- Publishing, installing, loading, or forwarding MCP tool descriptions or usage fields.
- Tool definitions are discovered once and later used for execution or authorization decisions.
- MCP server or package architecture allows tool descriptions to change after approval.
- A client relies on an earlier approval to trust a current tool definition.
- MCP server tool metadata persists across sessions or is reused by a client, team, or deployment.
- Tool descriptions from different MCP servers are jointly visible to the model.
- A tool description mentions another server, another tool, recipients, credentials, routing, or execution rules outside its own scope.
- An agent connects MCP servers from different trust zones into the same model context.
- A tool description or tool output contains directives about recipients, payloads, or behavior for another MCP server.
- a client connects to MCP servers or ingests tool/resource metadata.
- Tool descriptions, schemas, return values, or retrieved content are provided to an LLM context.
- An MCP client imports tool metadata from an external or third-party server into model context.
- connecting an agent to MCP servers or loading third-party tool descriptions into the agent context.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P002 (medium confidence).** Treat MCP tool metadata as an instruction-injection surface: scan, constrain, whitelist, sanitize, and avoid forwarding imperative metadata to models before tool exposure.
2. **P005 (high confidence).** Pin and reverify MCP server and tool definitions by version, hash, or equivalent integrity check whenever tools are installed, refreshed, or executed.
3. **P009 (medium confidence).** Keep MCP instruction authority scoped to the tool or server that supplied it; metadata or outputs from one server must not direct how another server's tools are invoked.
4. **P010 (high confidence).** Treat all tool descriptions, annotations, schemas, and retrieved resource content as untrusted unless obtained from a trusted server, because tool poisoning, full-schema poisoning, resource-content poisoning, typosquatting, and shadow…
5. **P012 (high confidence).** Treat every tool's metadata — its name and natural-language description loaded at MCP registration — as untrusted data, never as instructions the agent may obey; a description must not be able to add steps to a tool's operation or inv…
6. **P037 (high confidence).** Treat MCP schemas, tool manifests, descriptors, and signed tool definitions as executable contracts: require author identity and signature or hash verification, immutable governed version control, semantic policy checks, provenance lo…
7. **P048 (medium confidence).** Resolve MCP tools by verified server-qualified identity and show provenance or trust level before sensitive automatic invocations, with load-time conflict checks across connected servers.
8. **P050 (high confidence).** Apply conventional security hygiene to MCP components: enforce least privilege to avoid overexposure, validate inputs against command injection and path traversal, add integrity validation to messages and responses, protect stored cre…
9. **P061 (medium confidence).** Do not rely on MCP server sandboxing alone for prompt-injection defense; add controls over model-visible tool metadata, tool outputs, and cross-tool instruction following.
10. **P082 (medium confidence).** Threat-model MCP line jumping for downstream effects such as code exfiltration, vulnerability insertion, and security-alert manipulation, even when the malicious server is never explicitly invoked.
11. **P084 (medium confidence).** Validate tool definitions before model-context injection, hash reviewed tool descriptions at deployment, verify each tools/list response against those hashes, and reject changed descriptions as unreviewed model-trusted behavior.
12. **P088 (medium confidence).** Control MCP configuration drift with canonical baseline comparison, version-controlled definitions, immutable manifests, signed policy descriptors, rollback, compliance auditing, and protocol-level checksum or schema hooks where avail…
13. **P089 (medium confidence).** Do not rely on human approval alone to neutralize MCP line-jumping risk; pair approval with automated checks and workflow restrictions.
14. **P093 (medium confidence).** Block or require explicit escalation for tool-description instructions that request sensitive-file access, credential handling, covert exfiltration, or concealment from the user.
15. **P109 (high confidence).** Require identity-bound server authentication and integrity or signature verification, because without them tool shadowing, model-switching, unauthorized context injection, and unverified message modification grant attackers silent con…
16. **P115 (high confidence).** Defend Tool Poisoning at the pre-execution reasoning stage: screen tool descriptions before they enter the agent's planning context rather than relying on content-based output filtering or model safety alignment, which do not catch TP…
17. **P116 (high confidence).** Enumerate and test all three attack paradigms when assessing an agent: explicit-trigger function hijacking (P1), implicit-trigger function hijacking (P2), and implicit-trigger parameter tampering (P3); covering only one leaves the oth…
18. **P134 (medium confidence).** Use end-to-end MCP security controls across client, server, protocol, tool metadata, and model dataflow rather than relying on a single confirmation prompt or prompt-level rule.
19. **P138 (medium confidence).** Treat MCP tool descriptions as untrusted model-facing input; do not allow server-supplied metadata to override user intent, system rules, or trusted-service rules.
20. **P146 (medium confidence).** Treat MCP tool-description changes as security-relevant changes that require visible review, diffing, or re-approval before the updated tool can influence the agent.
21. **P155 (medium confidence).** Do not assume a larger or reasoning-enabled model is safer against Tool Poisoning; inverse scaling holds — more capable models are often more vulnerable (enabling Qwen3 reasoning raised ASR by 27.8%; o1-mini reached 72.8%) because the…
22. **P170 (high confidence).** Verify MCP server provenance before deployment: require developers to publish code signatures and SBOMs, verify contents and signatures against an approved-source and signing-key policy, protect all data in transit with TLS, and prefe…
23. **P175 (high confidence).** Apply traditional controls (authentication, authorization, input validation) AND explicitly address agentic-specific risks—dynamic tool invocation, implicit trust between agents, and shared/overlapping context—across the entire lifecy…
24. **P184 (high confidence).** Validate and pin tool metadata and surface complete tool definitions to the approver before execution, because context/tool poisoning hides malicious instructions in tool metadata, schema, or docstrings that agents follow blindly.
25. **P202 (medium confidence).** Until robust MCP defenses are standardized and deployed, handle MCP connections as potentially hostile rather than assuming the protocol boundaries are sufficient.
26. **P211 (medium confidence).** Monitor MCP-enabled assistant behavior after tool setup as well as at explicit invocation boundaries, because malicious metadata can influence later actions without a visible malicious call.
27. **P214 (medium confidence).** Reduce MCP rug-pull risk with version pinning, reproducible builds, signature verification, update transparency, and runtime monitoring.
28. **P215 (medium confidence).** Require approval interfaces to expose the complete AI-visible tool description, full arguments, and security-relevant side effects before a tool call is trusted.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P002, P005, P009, P010, P012, P037, P048, P050, P061, P082, P084, P088, P089, P093, P109, P115, P116, P134, P138, P146, P155, P170, P175, P184, P202, P211, P214, P215. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
