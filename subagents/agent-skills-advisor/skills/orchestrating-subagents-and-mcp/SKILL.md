---
name: orchestrating-subagents-and-mcp
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P011
  - P017
  - P019
  - P025
  - P027
  - P034
  - P036
  - P037
  - P041
  - P042
  - P049
  - P051
  - P060
  - P065
  - P069
  - P070
  - P071
  - P076
  - P079
  - P080
  - P081
  - P082
  - P086
  - P095
  - P096
  - P097
  - P100
  - P107
  - P109
  - P111
  - P114
  - P115
  - P117
  - P118
  - P123
  - P126
  - P131
  - P132
  - P133
  - P134
  - P135
  - P136
  - P137
  - P139
  - P147
  - P148
  - P149
  - P150
  claims:
  - C00024
  - C00026
  - C00028
  - C00033
  - C00037
  - C00038
  - C00039
  - C00042
  - C00043
  - C00045
  - C00046
  - C00047
  - C00048
  - C00052
  evidence: []
  source_anchors: []
  authored_from_digest: 0c5f30f82a959922be864d5cb5d697c7aa59abbe72fb337e4c38e45a39f7f714
---


# Skill: orchestrating-subagents-and-mcp

## Purpose

Choose and compose the right building block — a skill, a subagent, an MCP server, a hook, a loop, or a workflow — and engineer the surrounding harness and tools. It assigns responsibilities by layer, offloads isolated side tasks to subagents, extends reach through MCP servers referenced by fully-qualified name, designs tools as clear token-efficient contracts, budgets context as a scarce resource, enforces must-happen behaviour deterministically with hooks, and reserves multi-agent orchestration for high-value parallel work while accounting for its token cost.

## When to use

- Deciding whether a capability should be a skill, a subagent, an MCP server, a prompt, or an instruction file, and how to compose them.
- Isolating a side task in a forked or subagent context, or standing up an orchestrator-worker or loop-based workflow.
- Extending an agent's reach with MCP servers and engineering the tool descriptions, schemas, and output bounds.
- Budgeting context and token cost across a long-running or multi-agent harness and guarding its dominant failure modes.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Offload discrete specialized work to subagents for context isolation and parallelism [P007].
- For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth [P011].
- Run a skill in a forked context [P017].
- Expose many tools cheaply through deferred loading [P019].
- Assign responsibilities by layer [P025].
- Package recurring domain expertise as a Skill instead of repeating prompt instructions [P027].
- Use a subagent to isolate a side task whose intermediate output you will not reuse [P034].
- Reuse before building [P036].
- Engineer tool descriptions and schemas as part of the prompt [P037].
- Extend Claude's reach with MCP servers for internal tools, data sources [P041].
- Treat tool design as a first-class interface [P042].
- Delegate complex subtasks that should run in isolation from the main agent to subagents [P049].
- Do not rely on context compaction alone to preserve continuity across sessions; add explicit externally-persisted state [P051].
- Prefer scripts-as-tools over opaque built-in tools and capture recurring ones [P060].
- Before treating work as done, require an adversarial review by a dedicated subagent in a fresh context on only the diff/query and the acceptance criteria; fix blocking correctness findings and re-review rather than letting [P065].
- Reference MCP tools by fully qualified ServerName:tool_name to avoid tool-not-found errors, especially when multiple MCP servers are available [P069].
- Let model capability justify simpler scaffolding and greater autonomy [P070].
- Keep tool and script output bounded to protect the agent's context budget [P071].
- Build validation feedback loops into quality-critical workflows [P076].
- Match the building block to the need [P079].
- For behavior that must happen reliably or must be blocked, enforce it deterministically with hooks [P080].
- Use programmatic tool calling for workflows where code can reduce context bloat, inference round-trips, or fragile manual synthesis [P081].
- Treat skills and MCP as complementary rather than substitutes [P082].
- Prefer a dynamic workflow over the single-context default harness when a task is long-running, massively parallel, highly structured, or adversarial [P086].
- Avoid irreversible retain/discard context decisions on long-horizon tasks [P095].
- Use tool input examples to teach conventions that schemas cannot express, including optional-field patterns, nested object usage, correlated parameters [P096].
- Write precise, context-rich prompts [P097].
- Reserve a multi-agent orchestrator-worker architecture for high-value, breadth-first tasks with heavy parallelization, information exceeding one context window, or many complex tools; do not use it for work that requires all [P100].
- On difficult, policy-heavy domains, pair the think tool with an optimized prompt that gives domain-specific reasoning examples [P107].
- Do not couple session, harness [P109].
- Prefer judgement-anchored guidance over rigid rules for newer-generation models [P111].
- Budget context as a scarce resource [P114].
- Design agent tools as clear, non-overlapping, token-efficient contracts with robust behavior and unambiguous parameters [P115].
- Start with the simplest LLM design that can solve the task [P117].
- Choose workflows for predictable predefined paths and choose autonomous agents only when flexible, model-directed control is needed for an open-ended task [P118].
- Right-size context for capable models [P123].
- Keep MCP-server instructions generic and scoped to how to operate the server and its tools correctly [P126].
- Recommend custom agents for projects or processes with distinct stages that need specialized capability, tool restrictions, or strict handoffs; define the persona at the correct location [P131].
- Use turn-based loops for short, irregular tasks [P132].
- Improve loop output quality by maintaining a clean codebase, accessible technical documentation, explicit verification [P133].
- Manage loop cost by selecting the right primitive and model, defining clear stop criteria, piloting large runs, scripting deterministic work, tuning intervals [P134].
- Rely on live agentic search rather than a maintained embedding index [P135].
- Exploit the filesystem model [P136].
- Diagnose MCP call failures in layers [P137].
- Use MCP to connect Codex to capabilities outside the local repo [P139].
- Design explicit mechanisms against the two dominant long-task failure modes [P147].
- Prefer high-fidelity references [P148].
- Position the think tool as an in-flight reconsideration step used after generation has begun [P149].
- Budget for multi-agent token cost explicitly [P150].

## Inputs

- The task or workflow to build, the building blocks and tools available, and the context, parallelism, and reliability constraints it runs under.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P007]: Offload discrete specialized work to subagents for context isolation and parallelism.
- Overlooking [P011]: For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth.
- Overlooking [P017]: Run a skill in a forked context.
- Overlooking [P019]: Expose many tools cheaply through deferred loading.
- Overlooking [P025]: Assign responsibilities by layer.
- Overlooking [P027]: Package recurring domain expertise as a Skill instead of repeating prompt instructions.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P007, P011, P017, P019, P025, P027, P034, P036, P037, P041, P042, P049, P051, P060, P065, P069, P070, P071, P076, P079, P080, P081, P082, P086, P095, P096, P097, P100, P107, P109, P111, P114, P115, P117, P118, P123, P126, P131, P132, P133, P134, P135, P136, P137, P139, P147, P148, P149, P150, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
