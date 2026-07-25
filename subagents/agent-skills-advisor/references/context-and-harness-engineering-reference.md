---
name: context-and-harness-engineering-reference
kind: reference
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


# Reference: context-and-harness-engineering-reference

## Purpose

How to choose and compose building blocks and engineer the harness around them — skills vs subagents vs MCP vs hooks vs loops, tool-contract design, context budgeting, multi-agent orchestration, and long-running-task failure modes. Use it when the question is orchestration and context rather than a single skill's format.

## Principle index

Every principle this reference indexes, owned by the `orchestrating-subagents-and-mcp` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P007** — Offload discrete specialized work to subagents for context isolation and parallelism.
- **P011** — For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth.
- **P017** — Run a skill in a forked context.
- **P019** — Expose many tools cheaply through deferred loading.
- **P025** — Assign responsibilities by layer.
- **P027** — Package recurring domain expertise as a Skill instead of repeating prompt instructions.
- **P034** — Use a subagent to isolate a side task whose intermediate output you will not reuse.
- **P036** — Reuse before building.
- **P037** — Engineer tool descriptions and schemas as part of the prompt.
- **P041** — Extend Claude's reach with MCP servers for internal tools, data sources.
- **P042** — Treat tool design as a first-class interface.
- **P049** — Delegate complex subtasks that should run in isolation from the main agent to subagents.
- **P051** — Do not rely on context compaction alone to preserve continuity across sessions; add explicit externally-persisted state _(supporting)_.
- **P060** — Prefer scripts-as-tools over opaque built-in tools and capture recurring ones _(supporting)_.
- **P065** — Before treating work as done, require an adversarial review by a dedicated subagent in a fresh context on only the diff/query and the acceptance criteria; fix blocking correctness findings.
- **P069** — Reference MCP tools by fully qualified ServerName:tool_name to avoid tool-not-found errors, especially when multiple MCP servers are available.
- **P070** — Let model capability justify simpler scaffolding and greater autonomy _(supporting)_.
- **P071** — Keep tool and script output bounded to protect the agent's context budget _(supporting)_.
- **P076** — Build validation feedback loops into quality-critical workflows.
- **P079** — Match the building block to the need _(supporting)_.
- **P080** — For behavior that must happen reliably or must be blocked, enforce it deterministically with hooks.
- **P081** — Use programmatic tool calling for workflows where code can reduce context bloat, inference round-trips, or fragile manual synthesis.
- **P082** — Treat skills and MCP as complementary rather than substitutes.
- **P086** — Prefer a dynamic workflow over the single-context default harness when a task is long-running, massively parallel, highly structured, or adversarial _(supporting)_.
- **P095** — Avoid irreversible retain/discard context decisions on long-horizon tasks.
- **P096** — Use tool input examples to teach conventions that schemas cannot express, including optional-field patterns, nested object usage, correlated parameters.
- **P097** — Write precise, context-rich prompts.
- **P100** — Reserve a multi-agent orchestrator-worker architecture for high-value, breadth-first tasks with heavy parallelization, information exceeding one context window, or many complex tools; do not use it.
- **P107** — On difficult, policy-heavy domains, pair the think tool with an optimized prompt that gives domain-specific reasoning examples.
- **P109** — Do not couple session, harness.
- **P111** — Prefer judgement-anchored guidance over rigid rules for newer-generation models.
- **P114** — Budget context as a scarce resource _(supporting)_.
- **P115** — Design agent tools as clear, non-overlapping, token-efficient contracts with robust behavior and unambiguous parameters _(supporting)_.
- **P117** — Start with the simplest LLM design that can solve the task _(supporting)_.
- **P118** — Choose workflows for predictable predefined paths and choose autonomous agents only when flexible, model-directed control is needed for an open-ended task _(supporting)_.
- **P123** — Right-size context for capable models.
- **P126** — Keep MCP-server instructions generic and scoped to how to operate the server and its tools correctly.
- **P131** — Recommend custom agents for projects or processes with distinct stages that need specialized capability, tool restrictions, or strict handoffs; define the persona at the correct location.
- **P132** — Use turn-based loops for short, irregular tasks.
- **P133** — Improve loop output quality by maintaining a clean codebase, accessible technical documentation, explicit verification.
- **P134** — Manage loop cost by selecting the right primitive and model, defining clear stop criteria, piloting large runs, scripting deterministic work, tuning intervals.
- **P135** — Rely on live agentic search rather than a maintained embedding index.
- **P136** — Exploit the filesystem model.
- **P137** — Diagnose MCP call failures in layers.
- **P139** — Use MCP to connect Codex to capabilities outside the local repo.
- **P147** — Design explicit mechanisms against the two dominant long-task failure modes.
- **P148** — Prefer high-fidelity references.
- **P149** — Position the think tool as an in-flight reconsideration step used after generation has begun.
- **P150** — Budget for multi-agent token cost explicitly.

## Grounding

Indexes 49 of the package's 150 principles, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
