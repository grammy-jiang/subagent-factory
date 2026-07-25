---
name: platform-customization-matrix
kind: reference
status: ready
provenance:
  principles:
  - P004
  - P010
  - P012
  - P016
  - P020
  - P021
  - P024
  - P029
  - P030
  - P031
  - P038
  - P045
  - P046
  - P047
  - P058
  - P059
  - P073
  - P084
  - P087
  - P088
  - P089
  - P091
  - P093
  - P094
  - P101
  - P102
  - P104
  - P105
  - P106
  - P127
  - P128
  - P129
  - P130
  - P138
  - P140
  - P142
  - P143
  - P144
  - P145
  - P146
  claims:
  - C00012
  - C00013
  - C00029
  - C00030
  - C00031
  - C00032
  - C00033
  - C00034
  - C00036
  - C00051
  - C00054
  - C00077
  - C00078
  - C00079
  evidence: []
  source_anchors: []
  authored_from_digest: ae577cc51a72e621daebf03d2710e0c839e21e83bb020e6e145956696b5aad3b
---


# Reference: platform-customization-matrix

## Purpose

How skills and instruction files deploy and are governed across surfaces — install locations, runtime limits, API beta headers, tool permissions and invocation visibility, and the repository/personal/organization instruction files each platform supports. Use it when deciding what to set and where for a named target surface.

## Principle index

Every principle this reference indexes, owned by the `deploying-skills-across-platforms` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P004** — Place a skill in the location matching its intended audience.
- **P010** — To run Skills on the Claude API, send the three required beta headers.
- **P012** — Place guidance at the right location.
- **P016** — Use allowed-tools to pre-approve tools while a skill is active and disallowed-tools to remove them.
- **P020** — Treat skills as an untrusted-code supply chain.
- **P021** — Design each Skill for its target surface's runtime limits.
- **P024** — Use prompt files (*.prompt.md under .github/prompts/) for reusable, task-specific chat interactions run repeatedly with different inputs, keeping them distinct from codebase-wide custom instructions.
- **P029** — Select Skills for a request via the Messages API container parameter, giving each entry type "anthropic", a skill_id.
- **P030** — Design instruction files around Codex precedence.
- **P031** — Match instruction strictness to task fragility.
- **P038** — Install skills per surface.
- **P045** — Retrieve a Skill-generated file through the Files API.
- **P046** — Set invocation visibility deliberately with user-invocable and disable-model-invocation.
- **P047** — Keep AGENTS.md small and scoped to durable, repo-specific rules the agent must follow every time.
- **P058** — Put guidance that should apply to every request in a repository-wide file located exactly at .github/copilot-instructions.md, creating the .github directory first if it does not exist.
- **P059** — Recognize that GitHub Copilot supports three repository custom-instruction types.
- **P073** — Do not rely on Zero Data Retention for Agent Skills.
- **P084** — Select a Copilot customization feature by matching its trigger model to the task.
- **P087** — Treat project context for an AI coding agent as durable infrastructure _(supporting)_.
- **P088** — Before promising a customization feature works on a given IDE or surface, verify it against the feature-support matrix and recommend the latest stable IDE/CLI/extension versions _(supporting)_.
- **P089** — Manage the skill lifecycle with the gh skill CLI.
- **P091** — Maintain a lean CLAUDE.md of only broadly-applicable, non-obvious project context.
- **P093** — Account for IDE differences in supported instruction mechanisms.
- **P094** — Scope narrower guidance to matching files by adding .github/instructions/NAME.instructions.md files whose names end in .instructions.md, each beginning with an applyTo frontmatter key using glob.
- **P101** — Use a Project for persistent, always-loaded context that should inform every conversation about an initiative.
- **P102** — Check runtime and plan prerequisites before choosing a block.
- **P104** — Do not assume Skills sync across surfaces.
- **P105** — Restrict which skills Claude can invoke by denying the Skill tool wholesale in /permissions or scoping with Skill(name) exact and Skill(name *) prefix rules.
- **P106** — Maintain AGENTS.md as a feedback loop.
- **P127** — Manage skill visibility from settings with skillOverrides.
- **P128** — Match instruction specificity to task fragility.
- **P129** — Scope every rule that applies to only some paths with a 'paths' frontmatter; leave a rule unscoped only when it truly must apply to all sessions.
- **P130** — Avoid custom output styles unless a significant role change is required; prefer the built-in Proactive/Explanatory/Learning styles.
- **P138** — Enable the code execution tool and set the code-execution-2025-08-25 and skills-2025-10-02 beta headers on every Skills request, adding files-api-2025-04-14 when files are transferred.
- **P140** — Layer Codex guidance in two tiers.
- **P142** — Keep instruction files non-empty and within the size cap.
- **P143** — Troubleshoot instruction discovery systematically.
- **P144** — Select the instruction level.
- **P145** — Recommend always-on custom instructions when a team needs standards, guidelines, or expectations applied automatically across a scope; place them at the matching scope file.
- **P146** — When onboarding a repository with cloud-agent-generated instructions, keep them under two pages and non-task-specific.

## Grounding

Indexes 40 of the package's 150 principles, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
