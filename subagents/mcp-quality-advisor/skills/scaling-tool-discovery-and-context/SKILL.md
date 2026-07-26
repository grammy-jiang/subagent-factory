---
name: scaling-tool-discovery-and-context
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P005
  - P012
  - P014
  - P015
  - P025
  - P029
  - P032
  - P034
  - P035
  - P052
  - P064
  - P065
  - P080
  - P086
  - P087
  - P088
  - P117
  - P118
  - P123
  - P131
  - P133
  - P143
  - P151
  - P153
  - P155
  - P159
  - P185
  - P186
  - P187
  - P188
  authored_from_digest: 113d7220c6a8bbbc81e550b004931f386eb0c27d9270cea29cc085a7b9b24c23
---

# Skill: scaling-tool-discovery-and-context

## Purpose

Keep tool-definition and tool-result context within the token budget as a server (or many servers)
exposes dozens to hundreds of tools. Retrieve a small relevant subset, defer loading, quantify the
per-turn Tools Tax, and keep large data out of the model context [P001], [P012], [P002].

## When to use

- A tool-augmented agent or MCP deployment exposes many tools across one or more servers.
- Per-turn tool-schema injection is a large share of context, or context bloat degrades accuracy.
- Deciding how tool definitions reach the model — static injection, retrieval, deferred discovery, or
  code execution.

## Procedure

1. **Do not statically expose the whole catalog.** Retrieve only a small, semantically relevant subset
   (typically 3–5 tools) per query; retrieving too few hurts, and beyond ~5 plateaus [P001], [P065].
2. **Quantify the Tools Tax.** Treat per-turn tool-schema injection as a first-class recurring cost
   (~turns × catalog-size × per-tool tokens) and evaluate all three coupled failure modes — cost,
   reasoning degradation, and an enlarged tool-poisoning attack surface [P012], [P088].
3. **Prefer deferred / intent-gated loading.** Use a small always-loaded core plus a searchable long tail,
   or intent-gated two-phase loading, over naive full-schema injection or simple top-k of full schemas
   [P002], [P004], [P118], [P133].
4. **Choose retrieval parameters on accuracy grounds.** The token and latency savings are essentially
   free and domain-invariant; make tool summaries self-documenting and query-shaped to raise retrieval
   quality [P087], [P003].
5. **Apply context engineering to guidance and results.** Keep agent guidance minimal, judgment-anchored,
   and non-overlapping; load context progressively; wrap and trim tool results to task-relevant fields
   and keep large artifacts out of the context [P025], [P052], [P151], [P014].
6. **Consider code execution for large or composed toolsets.** When token, latency, or composition gains
   justify the infrastructure and security cost, expose tools as code interfaces and keep raw results
   inside the execution flow until the final step [P123], [P035], [P149].

## Pitfalls / anti-patterns

- Treating upfront loading of all tool definitions as free — it is a scaling hazard [P118].
- Using the model context as a data bus for large intermediate results [P131].
- Injecting the entire raw tool response and retaining it across turns [P151].

## Principles applied

- **[P001]** Do not statically expose the entire tool catalog to the LLM; retrieve only a small, semantically relevant subset (typically 3-5 tools) per query via dense-embedding similarity search.
- **[P002]** Use deferred tool loading with a small always-loaded core and searchable long tail so full tool definitions stay out of context until needed and tool metadata remains within the context budget.
- **[P003]** Make tool summaries self-documenting and query-shaped: descriptive names and intent-voiced summaries substantially raise retrieval quality, and an LLM can regenerate cryptic implementer-voiced summaries to be shorter yet more retrievable.
- **[P004]** Prefer intent-gated two-phase loading over both naive full-schema injection and simple top-k retrieval of full schemas: it can cut measured per-turn tool tokens by roughly 95% while keeping effective context utilization high, and unlike static manual pruning it does not starve tasks of tools they need.
- **[P005]** Treat MCP tools as untrusted and map each threat vector to its defense: prompt injection via image metadata to sanitization and semantic filters, schema bypass to strict enforcement and audit logs, remote code execution to capability scoping and sandboxing, privilege escalation to role-based tool binding, stale memory to TTL and garbage collection, cross-tool leakage to secure memory zones, provenance loss to output tagging, and command injection to input escaping.
- **[P012]** Treat per-turn MCP tool-schema injection as a first-class recurring cost (the Tools Tax): quantify it as approximately turns x catalog-size x ~200-500 tokens per tool, because stateless chat-completions APIs re-inject the full catalog on every turn and audits place it in the tens of thousands of tokens.
- **[P014]** Keep sensitive and intermediate data out of the model context by default, exposing only explicitly logged, returned, or policy-approved values through least-exposure controls such as tokenization, read-only mode, or metadata-only secret access.
- **[P015]** Provide intelligent, searchable tool discovery with adjustable detail levels once tool catalogs grow large enough that browsing or static exposure is inefficient.
- **[P025]** Keep agent guidance minimal, judgment-anchored, and non-overlapping across prompts, skills, CLAUDE.md, and user requests, verifying that removed constraints do not hurt behavior.
- **[P029]** For token-critical or large MCP servers, prefer dynamic toolsets: they hold token consumption roughly constant from 40 to 400 tools and cut total tokens by about 90-96% at a 100% task success rate, and adding new tools does not raise baseline token usage.
- **[P032]** Expect customized MCP clients to be input-bottlenecked: LLM planning plus tool-schema injection dominate their token and latency budgets, and cloud custom setups carry a planning/prefill latency floor that grows with task complexity.
- **[P034]** Extend vision tool schemas with explicit semantic-role, modality, and coordinate-system fields; over 60% of composition failures came from schema-valid but semantically mismatched outputs.
- **[P035]** Use programmatic tool calling for workflows where code can reduce context bloat, inference round-trips, or fragile manual synthesis.
- **[P052]** Apply progressive disclosure: load the right context at the right time via a tree of files rather than one upfront repository — move situational instructions (verification, code review) into selectively-called skills and split long skills into multiple files.
- **[P064]** Structure a large-toolset agent around two explicit operations - a retrieval (route) tool used as the discovery step when the model cannot solve the request alone or is unsure which tool to use, and an execution tool that may invoke only tools returned by the preceding route step and may retry a failing execution up to three times.
- **[P065]** Retrieve around five candidate tools per query: retrieving too few (k=1) significantly hurts success while increasing beyond five plateaus, and the tool-retrieval methodology - not the embedding model choice - is the dominant bottleneck, so invest there first.
- **[P080]** When an LLM agent performs a recurring multi-step tool task, separate one-time intelligence (deciding what to do) from repeated execution (carrying it out): have the agent reason once to produce a reusable plan, then execute that plan with no further agent reasoning.
- **[P086]** On complex, open-ended tasks the tool-result (retrieval) phase dominates the token budget across client types; large or retained tool outputs, not tool execution time, are the primary inflator.
- **[P087]** Choose retrieval parameters on accuracy grounds, because the token and latency savings are essentially free and domain-invariant: semantic filtering removes ~99% of tool-definition tokens across every server and K, and retrieval adds sub-100ms latency negligible next to LLM inference.
- **[P088]** Evaluate a tool-heavy agent on all three coupled failure modes of the Tools Tax - cost, reasoning degradation, and an enlarged tool-poisoning attack surface - not on token cost alone, because reducing in-context schemas improves all three at once.
- **[P117]** Prefer high-fidelity references — code, detailed test suites, functions to port, and HTML artifacts/mockups — over prose descriptions or screenshots, and @-mention them so the model can consult in-depth information for the current plan.
- **[P118]** Treat upfront loading of all MCP tool definitions as a scaling hazard, and design agents to disclose tool definitions only as needed.
- **[P123]** Choose a code-execution MCP architecture only when the expected token, latency, privacy, or composition gains justify the added infrastructure and security cost.
- **[P131]** Avoid using the model context as a data bus for large intermediate results; move, filter, and summarize data inside the execution environment before returning model-visible output.
- **[P133]** When an MCP server must expose many tools (dozens to hundreds), do not load every tool definition statically; use a dynamic/lazy discovery mechanism, because static exposure grows token usage roughly linearly with toolset size and soon hits the context-window limit.
- **[P143]** Account for tool metadata being repeatedly injected into the FM context on every interaction: excessive detail saturates the context window and raises cost, so any augmentation must justify its token cost and seek compact representations.
- **[P151]** Wrap and trim tool results to task-relevant fields: injecting the entire raw JSON response (metadata, headers, auxiliary fields) and retaining it across turns is a client orchestration-policy choice, not a protocol requirement, and is the dominant token inflator for off-the-shelf clients.
- **[P153]** Treat tool-description quality as the retrieval ceiling: invest in informative, semantically distinct descriptions.
- **[P155]** Inject only the relevant slice of memory into the context rather than everything, because stale or off-topic memory distracts the LLM and inflates latency and cost; curate what state is supplied and optionally summarize or knowledge-graph-distill it before storage.
- **[P159]** Prefer MCP over CLI when the platform's API surface is larger than the agent's training knowledge (use a describe/discovery tool for runtime capability discovery instead of guessing undocumented calls), in multi-tenant or multi-user environments (per-user OAuth, explicit tool boundaries, structured audit trails instead of ambient credentials), or when safety requires constraining the agent to declared tools with typed inputs rather than arbitrary shell.
- **[P185]** Prefer standardized MCP connectors over bespoke agent-to-system integrations when building agents that must reach many external tools or data sources.
- **[P186]** Expose MCP tools as code interfaces in a navigable filesystem or equivalent API surface when an agent has a secure execution environment.
- **[P187]** Ship a companion skills layer alongside the tools that turns raw MCP tool access into guided, IDE-native, multi-step workflows, structured in three levels: an auto-loaded shared agent-instruction file per IDE, server-side prompt templates any client can invoke, and individual slash-command skills.
- **[P188]** Structure the retrieval query with an explicit server-and-tool descriptor - server as the platform or permission domain and tool as the operation type plus target - and generate a concise server-level summary from each server's name, description, and tools to support server-level retrieval.

Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.

