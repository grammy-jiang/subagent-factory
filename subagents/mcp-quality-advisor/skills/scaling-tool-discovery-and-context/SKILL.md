---
name: scaling-tool-discovery-and-context
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P004
  - P013
  - P018
  - P025
  - P026
  - P027
  - P035
  - P043
  - P045
  - P046
  - P047
  - P048
  - P049
  - P059
  - P060
  - P068
  - P069
  - P075
  - P076
  - P077
  - P092
  - P106
  - P107
  - P108
  - P109
  - P110
  - P112
  - P118
  - P121
  - P122
  - P132
  - P138
  - P139
  - P140
  - P144
  - P145
  - P146
  - P147
  - P148
  - P173
  - P174
  - P175
  - P176
  - P186
  claims:
  - C00820
  - C00821
  - C00822
  - C00823
  - C00825
  - C00831
  - C00855
  - C00871
  - C00872
  - C00878
  - C00743
  - C00744
  - C01082
  - C01083
  - C01084
  - C01085
  - C00734
  - C00735
  evidence:
  - E00534
  - E00535
  - E00536
  - E00537
  - E00538
  - E00539
  - E00545
  - E00555
  - E00556
  - E00558
  - E00475
  - E00476
  - E00672
  - E00673
  - E00674
  source_anchors:
  - f73c30b5ffa6-c0000
  - b0365df12519-c0000
  - 5e5bb110f00c-c0000
  - bbac4c57d226-c0000
  authored_from_digest: 53a127de816ed86f9e93e6419e9773cfd64bff2a1c30a2053f42f17af171486a
---

# Skill: scaling-tool-discovery-and-context

## Purpose

Keep tool-definition and tool-result context within the model's budget when one or many servers expose dozens to hundreds of tools. Choose how tool definitions reach the model — static injection, retrieval, deferred/dynamic discovery, or code execution — and quantify the recurring per-turn cost (the Tools Tax) [P001], [P060], [P138].

## When to use

- A deployment exposes many tools (dozens to hundreds), often across multiple servers.
- Per-turn token cost, latency, or context bloat from tool schemas is hurting the agent.
- You are deciding between MCP tool calls and code execution / a CLI for a capability.

## Procedure

1. **Do not statically inject the whole catalog.** Retrieve only a small, semantically relevant subset per query rather than exposing every tool: static provisioning wastes tokens (a 100-tool catalog is ~20K-80K tokens before any query), bloats context, and hits window limits [P001], [P106]. Prefer intent-gated two-phase loading over both naive full-schema injection and simple top-k of full schemas [P025].
2. **Retrieve about five candidate tools per query.** Choose retrieval k on accuracy grounds — retrieving too few (k=1) significantly hurts success while a few extra candidates cost little; ~5 is a good default and the token/latency savings are essentially free [P049], [P076]. Structure the query with an explicit server-and-tool descriptor [P176].
3. **Architect explicit discovery + execution operations.** Structure a large-toolset agent around a retrieval/route tool as the discovery entry point plus an execution tool, and provide a search_tools call with a tool-category overview so the model knows what exists [P048], [P004], [P112]. Use deferred/dynamic tool discovery so the model loads only the definitions a task needs [P013], [P121].
4. **Budget the Tools Tax explicitly.** Treat per-turn tool-schema injection as a first-class recurring cost, quantify it, and keep context spent on tool definitions well under ~40% utilisation [P060], [P138], [P132]. Verbose JSON schemas loaded for every registered tool are the fixed planning cost to attack first [P092], [P068].
5. **Diagnose the bottleneck before optimizing.** Identify the bottleneck class from the client type — customized environments are usually input-bottlenecked (planning + schema injection), while the tool-result phase dominates the token budget on complex open-ended tasks [P069], [P093], [P075]. Evaluate the Tools Tax on all three coupled failure modes: cost, reasoning degradation, and hallucinated calls [P077].
6. **Prefer code execution for the right workflows.** Use programmatic tool calling when code can cut context bloat, inference round-trips, or fragile multi-step chaining; opt in only appropriate tools and keep their raw results inside the execution environment [P018], [P139]. Choose a code-execution MCP architecture only when the expected token/latency/privacy/composition gains justify it [P109], [P108].
7. **Keep large data out of the context window.** Do not use the model context as a data bus for large intermediate results — move, filter, and summarise data outside it, and wrap/trim tool results to task-relevant fields rather than injecting the entire raw JSON [P118], [P140]. Return results processed enough to be usable but keep the underlying detail accessible [P035].
8. **Use memory and caching to inject only what's relevant.** Cache deterministic tool outputs keyed by a hash of tool name plus parameters, and inject only the relevant slice of memory rather than everything, because stale or off-topic memory hurts [P026], [P144]. Memory plus caching beats memoryless baselines on latency, tokens, and cost and raises completion rates [P027], [P145].
9. **Choose CLI vs MCP deliberately.** Prefer a CLI when the agent already knows the tool from training (gh, kubectl, terraform); prefer MCP when the platform's API surface is larger than the agent's training knowledge, and ship a companion skills layer that turns raw tool access into guided workflows [P147], [P148], [P173], [P175]. Budget for the dynamic-toolset trade-off (~2-3x more tool calls) [P122], [P043].

## Pitfalls / anti-patterns

- Loading every tool definition statically 'so the model can see everything' — the top scaling hazard [P106], [P121].
- Optimizing latency before identifying whether the client is input- or output-bottlenecked [P093].
- Passing whole raw JSON responses back into context instead of trimming to task-relevant fields [P140].

## Grounding

Principles: P001, P004, P013, P018, P025, P026, P027, P035, P043, P045, P046, P047, P048, P049, P059, P060, P068, P069, P075, P076, P077, P092, P106, P107, P108, P109, P110, P112, P118, P121, P122, P132, P138, P139, P140, P144, P145, P146, P147, P148, P173, P174, P175, P176, P186. Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.
