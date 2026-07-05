---
name: indirect-prompt-injection-defense
kind: skill
status: ready
provenance:
  principles:
  - P024
  - P029
  - P033
  - P034
  - P043
  - P047
  - P057
  - P085
  - P087
  - P094
  - P096
  - P098
  - P110
  - P131
  - P132
  - P139
  - P140
  - P148
  - P149
  - P150
  - P151
  - P152
  - P168
  - P169
  - P204
  - P205
  claims:
  - C00290
  - C00291
  - C00322
  - C00323
  - C00383
  - C00413
  - C00428
  - C00429
  - C00456
  - C00457
  - C00724
  - C00726
  - C00728
  - C00729
  - C00730
  - C00765
  - C00766
  - C00768
  - C00769
  - C00770
  - C00771
  - C00772
  - C00773
  - C00774
  - C00775
  - C00776
  - C00777
  - C00778
  - C00779
  - C00789
  - C00791
  - C00794
  - C00795
  - C00796
  - C00797
  - C00800
  - C00801
  - C00803
  - C00804
  - C00827
  - C00828
  - C00943
  - C00944
  - C00993
  - C00994
  - C01011
  - C01012
  - C01013
  - C01014
  evidence:
  - E00235
  - E00236
  - E00267
  - E00268
  - E00328
  - E00351
  - E00362
  - E00363
  - E00366
  - E00367
  - E00577
  - E00578
  - E00580
  - E00581
  - E00582
  - E00613
  - E00614
  - E00616
  - E00617
  - E00618
  - E00619
  - E00620
  - E00621
  - E00622
  - E00623
  - E00624
  - E00625
  - E00626
  - E00627
  - E00636
  - E00637
  - E00640
  - E00641
  - E00642
  - E00643
  - E00646
  - E00647
  - E00649
  - E00650
  - E00666
  - E00667
  - E00748
  - E00749
  - E00792
  - E00793
  - E00810
  - E00811
  - E00812
  - E00813
  source_anchors:
  - 347696d03493-c0002
  - 347696d03493-c0004
  - 357204ac930a-c0000
  - 38612cf35377-c0000
  - 457ef5c30a3b-c0000
  - 867e7bf944fa-c0000
  - b4bcb3ed0e87-c0000
  - c82772e8c087-c0000
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0000
  - fa0ccb38ff81-c0001
  authored_from_digest: e72660011ae3b6634634e772ee99c426b3c371bdd39f58273c7264bfe6ea0c0e
---

# Indirect Prompt Injection Defense

Contain indirect prompt injection and exfiltration — treat resources, tool outputs, and sampling as adversarial data, refuse or break the lethal trifecta, and never rely on prompt-level guardrails alone.

This skill packages 26 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- when external content is placed in an agent context.
- when preparing production deployment or changing prompts, tools, memory, retrieval, policies, or model providers.
- MCP agents can act across repositories, cloud APIs, ticketing systems, CI/CD, production settings, identity systems, or sensitive data stores.
- External context, tool output, retrieved documents, schemas, or long-lived memory can influence multi-step MCP planning.
- When threat-modeling MCP deployments or choosing remediation priorities.
- Assessing MCP as infrastructure for tool-augmented LLM agents.
- Composing or reviewing LLM tools for end users or applications.
- All three lethal capabilities are present in one workflow or tool chain.
- A user or team assembles tools outside a single vendor-controlled product boundary.
- The composition can recreate private-data access, untrusted input, and outbound communication.
- Agents connect to MCP tools that can receive untrusted metadata, changed descriptions, or attacker-controlled tool results.
- The agent reads web pages, email, documents, images, issue text, chat messages, or other third-party content.
- Trusted and untrusted material are combined in the model context.
- An attacker can place messages or other content into a trusted tool result that the agent reads.
- Received content appears before a later operation that can send data outward.
- Sampled output may be displayed, summarized, stored, or carried forward into conversation context.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P024 (high confidence).** Treat all contextual and Resource input (documents, pasted text, retrieved content, emails, Slack) as untrusted rather than authoritative, because obfuscated embedded directives can redirect tool calls (indirect prompt injection).
2. **P029 (high confidence).** Institute regular red-team and adversarial-testing exercises using external experts or automated attack frameworks to simulate prompt injections and tool tampering, so weaknesses are found and patched before real adversaries exploit t…
3. **P033 (high confidence).** Bound every MCP agent with unique identity, documented least-privilege scopes, policy-as-code enforcement, just-in-time elevation for risky access, continuous entitlement review, runtime guardrails, tamper-evident action logs, and sep…
4. **P034 (high confidence).** Preserve MCP intent-flow integrity by anchoring the original user goal, treating retrieved resources and tool outputs as untrusted data, validating every planned action against the goal, using isolated checker or policy-decision contr…
5. **P043 (medium confidence).** Assess MCP controls by the attack preconditions they remove, especially untrusted input, sensitive-data access, action capability, broad privileges, token forwarding, unvalidated metadata, arbitrary egress, and weak server trust.
6. **P047 (medium confidence).** Evaluate MCP security as an LLM-tool safety problem that includes prompt manipulation, unsafe execution, untrusted endpoints, unsafe workflows, ambiguous documentation, model behavior, and alignment tradeoffs.
7. **P057 (medium confidence).** Reject or redesign any agent workflow that simultaneously has private-data access, exposure to untrusted content, and an outbound channel capable of carrying data away.
8. **P085 (medium confidence).** Do not assume vendor fixes for known prompt-injection incidents secure arbitrary user-assembled tool chains; enforce local capability boundaries for the actual composition.
9. **P087 (medium confidence).** Cover both malicious MCP metadata and indirect prompt injections in MCP security guardrails, rather than treating user approval or user caution as sufficient protection.
10. **P094 (medium confidence).** Treat attacker-controlled content as executable-looking instruction data and do not rely on the model to infer that it has lower authority than user or system instructions.
11. **P096 (medium confidence).** Treat externally received communication content in tool results as adversarial data and prevent it from creating memory, policy, or send-parameter instructions.
12. **P098 (medium confidence).** Prevent sampled response text from becoming durable behavioral instruction for later turns unless it has passed an explicit trust and safety check.
13. **P110 (high confidence).** Use one unified threat model in which security breaches and safety failures converge: an indirect prompt injection can cause an honestly-mistaken destructive action, and a tool-parameter hallucination can cause a breach, so never tria…
14. **P131 (medium confidence).** Normalize and evaluate suspicious structured-context payloads in tool outputs, because injections may imitate surrounding serialization rather than appear as plain instructions.
15. **P132 (medium confidence).** Treat every MCP sampling prompt supplied by a server as untrusted input that crosses a security boundary before reaching the LLM.
16. **P139 (medium confidence).** Require explicit user approval for tool execution that arises from or is adjacent to MCP sampling output.
17. **P140 (medium confidence).** Use prompt-level guardrails only as defense-in-depth; do not count natural-language instructions as the sole boundary preventing prompt-injection exfiltration.
18. **P148 (medium confidence).** Do not treat a plausible or useful MCP tool as trustworthy merely because it performs the visible user-requested task.
19. **P149 (medium confidence).** Model outbound capability broadly: HTTP requests, image loads, API calls, public writes, and generated links can all be exfiltration paths if they can encode private context.
20. **P150 (medium confidence).** Review aggregate tool composition, not just individual tools, because safe-looking components can become unsafe when their combined capabilities satisfy the lethal trifecta.
21. **P151 (medium confidence).** Classify email and similar message-reading tools as untrusted-input channels and isolate them from permissions that can expose private data or perform outbound actions.
22. **P152 (medium confidence).** Make sampled outputs auditable enough that hidden generated content cannot be concealed by UI summarization or result condensation alone.
23. **P168 (high confidence).** Treat each connected MCP server as a separate untrusted security domain and monitor or mediate cross-server data flows.
24. **P169 (high confidence).** Treat every MCP integration as a privilege-execution boundary, not a passive text interface: MCP turns the LLM into an active system component with shell-level privileges acting on untrusted context, and the attack surface grows with…
25. **P204 (medium confidence).** After an agent ingests untrusted input, constrain its ability to perform consequential actions so that the untrusted input cannot directly trigger those actions.
26. **P205 (medium confidence).** Treat MCP tool outputs from external or user-generated sources as adversarial content and detect or neutralize hidden instructions before model use.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P024, P029, P033, P034, P043, P047, P057, P085, P087, P094, P096, P098, P110, P131, P132, P139, P140, P148, P149, P150, P151, P152, P168, P169, P204, P205. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
