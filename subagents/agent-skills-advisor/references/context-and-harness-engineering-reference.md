---
name: context-and-harness-engineering-reference
kind: reference
status: ready
provenance:
  principles:
  - P005
  - P008
  - P009
  - P013
  - P023
  - P029
  - P031
  - P043
  - P049
  - P051
  - P052
  - P057
  - P059
  - P060
  - P063
  - P064
  - P065
  - P068
  - P073
  - P074
  - P075
  - P076
  - P082
  - P084
  - P088
  - P093
  - P095
  - P097
  - P102
  - P103
  - P105
  - P106
  - P107
  - P114
  - P115
  - P118
  - P121
  - P125
  - P126
  - P127
  - P128
  - P129
  - P130
  - P131
  - P132
  - P135
  - P146
  - P148
  - P149
  - P150
  claims:
  - C00024
  - C00026
  - C00028
  - C00029
  - C00033
  - C00034
  - C00036
  - C00037
  - C00038
  - C00039
  - C00042
  - C00043
  - C00045
  - C00046
  evidence: []
  source_anchors: []
  authored_from_digest: b548e9d92d0dcbed038603cfb921f195507d811cf309a0516c598051b3716e26
---


# Reference: context-and-harness-engineering-reference

## Purpose

How to choose and compose building blocks and engineer the harness around them — skills vs subagents vs MCP vs hooks vs loops, tool-contract design, context budgeting, multi-agent orchestration, and long-running-task failure modes. Use it when the question is orchestration and context rather than a single skill's format.

## Principle index

Every principle this reference indexes, owned by the `orchestrating-subagents-and-mcp` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P005** — Offload discrete specialized work to subagents for context isolation and parallelism.
- **P008** — Assign responsibilities by layer.
- **P009** — For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth.
- **P013** — Expose many tools cheaply through deferred loading.
- **P023** — Extend Claude's reach with MCP servers for internal tools, data sources.
- **P029** — Delegate complex subtasks that should run in isolation from the main agent to subagents.
- **P031** — Do not rely on context compaction alone to preserve continuity across sessions; add explicit externally-persisted state _(supporting)_.
- **P043** — Prefer scripts-as-tools over opaque built-in tools and capture recurring ones _(supporting)_.
- **P049** — Reference MCP tools by fully qualified ServerName:tool_name to avoid tool-not-found errors, especially when multiple MCP servers are available.
- **P051** — As model capability improves, re-evaluate the harness against tested task performance, removing scaffolding that is no longer load-bearing and adding only pieces that unlock demonstrated capability _(supporting)_.
- **P052** — Keep tool and script output predictable and context-safe with bounded summary defaults, filtering or range selection, truncation guidance _(supporting)_.
- **P057** — For quality-critical refinement workflows, define a validation gate, check results immediately, fix concrete failures.
- **P059** — Match the building block to the need _(supporting)_.
- **P060** — Use programmatic tool calling for workflows where code can reduce context bloat, inference round-trips, or fragile manual synthesis.
- **P063** — Prefer a runtime dependency-resolving tool runner.
- **P064** — Prefer a dynamic workflow over the single-context default harness when a task is long-running, massively parallel, highly structured, or adversarial _(supporting)_.
- **P065** — Persist a progress file alongside git history so a fresh-context agent can quickly reconstruct the state of work and use git to revert bad changes and recover working states; this also removes wasted _(supporting)_.
- **P068** — For behavior that must happen reliably or must be blocked, enforce it deterministically with hooks.
- **P073** — Apply progressive disclosure.
- **P074** — Avoid irreversible retain/discard context decisions on long-horizon tasks.
- **P075** — Use tool input examples to teach conventions that schemas cannot express, including optional-field patterns, nested object usage, correlated parameters.
- **P076** — Write precise, context-rich prompts.
- **P082** — Reserve a multi-agent orchestrator-worker architecture for high-value, breadth-first tasks with heavy parallelization, information exceeding one context window, or many complex tools; do not use it.
- **P084** — Check runtime and plan prerequisites before choosing a block.
- **P088** — Treat skills and MCP as complementary rather than substitutes.
- **P093** — On difficult, policy-heavy domains, pair the think tool with an optimized prompt that gives domain-specific reasoning examples.
- **P095** — Do not couple session, harness.
- **P097** — Prefer judgement-anchored guidance over rigid rules for newer-generation models.
- **P102** — Budget context as a scarce resource _(supporting)_.
- **P103** — Design agent tools as clear, non-overlapping, token-efficient contracts with robust behavior and unambiguous parameters _(supporting)_.
- **P105** — Start with the simplest LLM design that can solve the task _(supporting)_.
- **P106** — Choose workflows for predictable predefined paths and choose autonomous agents only when flexible, model-directed control is needed for an open-ended task _(supporting)_.
- **P107** — Justify adopting the think tool by task complexity rather than adding it universally _(supporting)_.
- **P114** — Use a subagent to isolate a side task whose intermediate output you will not reuse.
- **P115** — Right-size context for capable models.
- **P118** — Choose a skill when the need is multi-step tool workflows, consistency-critical processes, capturing and sharing domain expertise, or preserving institutional knowledge against team attrition.
- **P121** — Keep MCP-server instructions generic and scoped to how to operate the server and its tools correctly.
- **P125** — Avoid custom output styles unless a significant role change is required; prefer the built-in Proactive/Explanatory/Learning styles.
- **P126** — Recommend custom agents for projects or processes with distinct stages that need specialized capability, tool restrictions, or strict handoffs; define the persona at the correct location.
- **P127** — Use turn-based loops for short, irregular tasks.
- **P128** — Improve loop output quality by maintaining a clean codebase, accessible technical documentation, explicit verification.
- **P129** — Manage loop cost by selecting the right primitive and model, defining clear stop criteria, piloting large runs, scripting deterministic work, tuning intervals.
- **P130** — Rely on live agentic search rather than a maintained embedding index.
- **P131** — Exploit the filesystem model.
- **P132** — Diagnose MCP call failures in layers.
- **P135** — Use MCP to connect Codex to capabilities outside the local repo.
- **P146** — Design explicit mechanisms against the two dominant long-task failure modes.
- **P148** — Position the think tool as an in-flight reconsideration step used after generation has begun.
- **P149** — Budget for multi-agent token cost explicitly.
- **P150** — Virtualize an agent into independently swappable components -- a session.

## Grounding

Indexes 50 of the package's 150 principles, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
