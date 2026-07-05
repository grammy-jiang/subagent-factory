---
name: operating-mcp-on-serverless
kind: skill
status: ready
provenance:
  principles:
  - P044
  - P058
  - P061
  - P062
  - P067
  - P074
  - P095
  - P096
  - P119
  - P120
  - P131
  - P141
  - P143
  - P199
  - P200
  claims:
  - C01463
  - C01464
  - C01465
  - C01466
  - C01469
  - C01471
  - C00589
  - C00591
  - C00592
  - C00593
  - C00594
  - C00795
  - C00800
  - C00801
  - C00802
  - C00803
  - C01012
  - C01013
  evidence:
  - E00832
  - E00833
  - E00834
  - E00835
  - E00836
  - E00837
  - E00370
  - E00372
  - E00373
  - E00374
  - E00375
  - E00516
  - E00521
  - E00522
  - E00523
  source_anchors:
  - 74c00514b52f-c0001
  - c983186538ad-c0000
  - dfe0874c00ba-c0001
  - 48702ecaa6e3-c0001
  authored_from_digest: 95116a22d8eeebad8dfcd255ad078498310ffee962300b38d783d39067592a69
---

# Skill: operating-mcp-on-serverless

## Purpose

Operate MCP-enabled agentic workloads cost-effectively on serverless/FaaS with external memory and caching, and compose multi-agent roles and orchestration around MCP. Optimise for the dominant cost (LLM tokens) while keeping large artifacts out of context and off local disk [P143], [P141], [P146].

## When to use

- You are deploying or right-sizing MCP servers and agent workflows on serverless/FaaS.
- You are designing caching, external memory, or a planner/actor/evaluator decomposition.
- You are building an orchestration layer over multiple MCP servers.

## Procedure

1. **Host on FaaS and expose servers over HTTP.** Host MCP-enabled agentic workflows on serverless FaaS rather than monolithic VMs for autoscaling and pay-per-use, and wrap each server as an HTTP-exposed function (e.g. a Lambda Function URL) because MCP's stdio/local model does not fit FaaS directly [P143], [P131].
2. **Consolidate and right-size functions.** Consolidate an application's MCP servers into a single function sized to the peak of its constituents, and provision cost-consciously by choosing among independent, per-workflow-unified, or globally-unified layouts [P062], [P120].
3. **Optimize input tokens first.** Optimise input-token consumption before FaaS execution: LLM token charges dominate total cost (roughly, tokens dwarf compute), so account for tool metadata being re-injected on every interaction and trim it [P141], [P132].
4. **Persist memory and cache deterministic outputs.** Persist agent memory in an external store keyed by a session id (with a per-request invocation id), and cache deterministic tool outputs in object storage keyed by tool name plus parameters — valued for reliability, not only efficiency [P059], [P026], [P145]. Keep large content and file artifacts in external storage, out of context and off local disk [P146].
5. **Decompose agentic roles into functions.** Decompose the agentic pattern into one function per role (Planner, Actor, Evaluator) orchestrated as a pipeline, and give each agent a strict-JSON prompt contract so roles compose predictably [P095], [P119]. Bound the planner-evaluator loop with an explicit maximum-iteration cap [P096].
6. **Treat descriptions as configuration you can override.** Advise users to treat tool descriptions as mutable client-side configuration they can override at runtime, and select the model as a lever that reshapes both the cost profile and its predictability [P074], [P061]. Recommend the design-once/execute-many pattern when a multi-step task recurs and separate one-time planning from repeated execution [P067].
7. **Build orchestration as a Mediator with a small DSL.** Build an MCP orchestration layer as a Mediator that is itself an MCP server exposing workflow tools, and constrain the orchestration DSL to a small fixed set of composable step primitives (call, loop, parallel, pipeline) [P199], [P200]. Build the registry entry deterministically from the repository [P044].

## Pitfalls / anti-patterns

- Optimizing compute/memory sizing before input tokens, which dominate cost [P141].
- Holding large artifacts in the model context or on function-local disk instead of object storage [P146].
- Running a planner/evaluator loop with no maximum-iteration cap [P096].

## Grounding

Principles: P044, P058, P061, P062, P067, P074, P095, P096, P119, P120, P131, P141, P143, P199, P200. Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.
