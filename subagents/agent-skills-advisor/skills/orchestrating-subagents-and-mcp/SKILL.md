---
name: orchestrating-subagents-and-mcp
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P010
  - P013
  - P033
  - P039
  - P051
  - P054
  - P056
  - P066
  - P068
  - P069
  - P089
  - P116
  - P121
  - P126
  - P143
  claims:
  - C00037
  - C00038
  - C00039
  - C00431
  - C00435
  - C00819
  - C01133
  - C01134
  - C01444
  - C00042
  - C00043
  - C00046
  evidence:
  - E00025
  - E00026
  - E00027
  - E00196
  - E00197
  - E00372
  - E00531
  - E00532
  - E00622
  - E00028
  - E00029
  - E00031
  source_anchors:
  - 0bc9d8042bad-c0000
  - de706ba6765f-c0000
  - 59f8ec5e7b03-c0000
  - 107bd586b996-c0000
  - da6e3e928ff2-c0000
  authored_from_digest: 7a6ba866610ab5356d1045ed04759c32cb3243ff82d865f6bc9afc828f561b63
---

# Skill: orchestrating-subagents-and-mcp

## Purpose

Decide when a need is best met by a skill, a subagent, or an MCP server — and how to compose them
— so procedural knowledge, context isolation, and external connectivity each land in the right
primitive. Grounded in P006, P010, P039, P069, P056.

## When to use

- You are choosing among a skill, a subagent, an MCP server, or a plain prompt for a capability.
- A task reads many files or runs a long investigation whose intermediate output you will not reuse.
- You are wiring a skill to external systems, or building a multi-agent workflow.

## Procedure

1. **Assign responsibilities by layer.** Use MCP servers to give the agent connectivity and access
   to external systems and data it cannot otherwise reach; use skills to supply the procedural
   know-how for using them. Treat skills and MCP as complementary, not substitutes — the most
   capable workflows use both [P010], [P069], [P033].
2. **Offload isolated side work to a subagent.** When a subtask should run in isolation from the
   main agent — codebase research, log analysis, a dependency audit, running a test suite — give
   it to a subagent so only its focused result returns to the main context [P006], [P039],
   [P116]. Run a skill in a forked context when it reads many files or runs a long investigation
   and should return only a focused result [P013].
3. **Add an adversarial reviewer, never self-certify.** Before treating quality-critical work as
   done, spawn a dedicated reviewer subagent that inspects the output rather than letting the
   producing agent certify its own work [P054].
4. **Reserve multi-agent orchestration for the cases that earn it.** Use an orchestrator–worker
   architecture only for high-value, breadth-first tasks with heavy parallelization or information
   exceeding one context window, and budget for the extra token cost across separate context
   windows [P089], [P143].
5. **Reference MCP tools unambiguously.** Refer to MCP tools by fully qualified
   `ServerName:tool_name` to avoid tool-not-found errors when several servers are available
   [P056]. Keep MCP-server instructions generic (how to operate the server and its tools);
   put process-specific, multi-server workflow steps in the skill [P121].
6. **Prefer scripts-as-tools where code is clearer than an opaque tool.** Provide capability as
   code the agent can read and modify, and capture recurring operations as reusable scripts
   [P051], [P068].
7. **Match the primitive to the process shape.** Recommend a custom agent for a project or process
   with distinct stages needing specialized capability, tool restrictions, or strict handoffs;
   define its scope and handoffs explicitly [P126].

## Pitfalls / anti-patterns

- Treating skills and MCP as interchangeable rather than complementary [P069].
- Letting the producing agent grade its own output instead of using an independent reviewer [P054].
- Spinning up a multi-agent architecture for a task a single context handles — paying the token
  cost without the breadth-first payoff [P089], [P143].

## Grounding

Principles: P006, P010, P013, P033, P039, P051, P054, P056, P066, P068, P069, P089, P116, P121,
P126, P143. Distillation-only: no verbatim source quotation.
