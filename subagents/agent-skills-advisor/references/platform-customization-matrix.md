---
name: platform-customization-matrix
kind: reference
status: ready
provenance:
  principles:
  - P016
  - P018
  - P026
  - P027
  - P028
  - P036
  - P038
  - P039
  - P054
  - P062
  - P066
  - P067
  - P069
  - P071
  - P072
  - P080
  - P081
  - P083
  - P090
  - P091
  - P092
  - P101
  - P111
  - P122
  - P124
  - P133
  - P134
  - P136
  - P138
  - P140
  - P141
  - P142
  - P143
  - P144
  - P145
  claims:
  - C00029
  - C00030
  - C00031
  - C00032
  - C00033
  - C00262
  - C00263
  - C00264
  - C00265
  - C00355
  - C00362
  - C00363
  - C00370
  - C00371
  evidence: []
  source_anchors: []
  authored_from_digest: 376fa514cf7c99d117d7a989f06be84b6486768cb0972c8b90d12c94865ea862
---


# Reference: platform-customization-matrix

## Purpose

How skills and instruction files deploy and are governed across surfaces — install locations, runtime limits, API beta headers, tool permissions and invocation visibility, and the repository/personal/organization instruction files each platform supports. Use it when deciding what to set and where for a named target surface.

## Principle index

Every principle this reference indexes, owned by the `deploying-skills-across-platforms` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P016** — Use manually invoked prompt files.
- **P018** — Select Skills for a request via the Messages API container parameter, giving each entry type "anthropic", a skill_id.
- **P026** — Retrieve a Skill-generated file through the Files API.
- **P027** — Set invocation visibility deliberately with user-invocable and disable-model-invocation.
- **P028** — Place a skill in the directory that matches its intended scope.
- **P036** — Pre-approve the tools a skill needs via the SKILL.md allowed-tools frontmatter field to avoid a per-use confirmation prompt; any tool omitted from allowed-tools will trigger a permission prompt each.
- **P038** — Write a precise, trigger-oriented description.
- **P039** — Put guidance that should apply to every request in a repository-wide file located exactly at .github/copilot-instructions.md, creating the .github directory first if it does not exist.
- **P054** — Do not rely on Zero Data Retention for Agent Skills.
- **P062** — Select a Copilot customization feature by matching its trigger model to the task.
- **P066** — Before promising a customization feature works on a given IDE or surface, verify it against the feature-support matrix and recommend the latest stable IDE/CLI/extension versions _(supporting)_.
- **P067** — Manage the skill lifecycle with the gh skill CLI.
- **P069** — Maintain a lean CLAUDE.md of only broadly-applicable, non-obvious project context.
- **P071** — Account for IDE differences in supported instruction mechanisms.
- **P072** — Scope narrower guidance to matching files by adding .github/instructions/NAME.instructions.md files whose names end in .instructions.md, each beginning with an applyTo frontmatter key using glob.
- **P080** — Design each Skill for its target surface's runtime limits.
- **P081** — When invoking Agent Skills through the API, always enable a code-execution tool and include the skills-2025-10-02 beta header; any code-execution tool version works.
- **P083** — Use a Project for persistent, always-loaded context that should inform every conversation about an initiative.
- **P090** — Do not assume Skills sync across surfaces.
- **P091** — Restrict which skills Claude can invoke by denying the Skill tool wholesale in /permissions or scoping with Skill(name) exact and Skill(name *) prefix rules.
- **P092** — Maintain AGENTS.md as a feedback loop.
- **P101** — Treat project context for an AI coding agent as durable infrastructure _(supporting)_.
- **P111** — Account for the code execution environment's platform limits.
- **P122** — Manage skill visibility from settings with skillOverrides.
- **P124** — Scope every rule that applies to only some paths with a 'paths' frontmatter; leave a rule unscoped only when it truly must apply to all sessions.
- **P133** — Enable the code execution tool and set the code-execution-2025-08-25 and skills-2025-10-02 beta headers on every Skills request, adding files-api-2025-04-14 when files are transferred.
- **P134** — Separate authoring from distribution.
- **P136** — Place a skill in the location matching its intended audience.
- **P138** — Layer Codex guidance in two tiers.
- **P140** — Design instruction files around Codex precedence.
- **P141** — Keep instruction files non-empty and within the size cap.
- **P142** — Troubleshoot instruction discovery systematically.
- **P143** — Select the instruction level.
- **P144** — Recommend always-on custom instructions when a team needs standards, guidelines, or expectations applied automatically across a scope; place them at the matching scope file.
- **P145** — When onboarding a repository with cloud-agent-generated instructions, keep them under two pages and non-task-specific.

## Grounding

Indexes 35 of the package's 150 principles, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
