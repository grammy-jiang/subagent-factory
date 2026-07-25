---
name: deploying-skills-across-platforms
kind: skill
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


# Skill: deploying-skills-across-platforms

## Purpose

Deploy and govern a skill on a specific target surface. It matches the install location to the intended audience, designs each skill for its surface's runtime limits, sets the required API beta headers, pre-approves tools and sets invocation visibility deliberately, restricts which skills an agent may invoke, and places instruction files (AGENTS.md, .github/copilot-instructions, Codex tiers, scoped path rules) at the right level and location for the surface — verifying feature support before promising it and never assuming skills sync across surfaces.

## When to use

- Choosing where a skill installs and which runtime limits, headers, and permissions the target surface requires.
- Governing skill availability and invocation visibility, or restricting which skills an agent may call.
- Placing repository, personal, or organization instruction files (AGENTS.md, Copilot, Codex) at the level and location that matches their scope.
- Reconciling differences in what each IDE or surface supports before relying on a customization feature.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Use manually invoked prompt files [P016].
- Select Skills for a request via the Messages API container parameter, giving each entry type "anthropic", a skill_id [P018].
- Retrieve a Skill-generated file through the Files API [P026].
- Set invocation visibility deliberately with user-invocable and disable-model-invocation [P027].
- Place a skill in the directory that matches its intended scope [P028].
- Pre-approve the tools a skill needs via the SKILL.md allowed-tools frontmatter field to avoid a per-use confirmation prompt; any tool omitted from allowed-tools will trigger a permission prompt each time it is used [P036].
- Write a precise, trigger-oriented description [P038].
- Put guidance that should apply to every request in a repository-wide file located exactly at .github/copilot-instructions.md, creating the .github directory first if it does not exist [P039].
- Do not rely on Zero Data Retention for Agent Skills [P054].
- Select a Copilot customization feature by matching its trigger model to the task [P062].
- Before promising a customization feature works on a given IDE or surface, verify it against the feature-support matrix and recommend the latest stable IDE/CLI/extension versions [P066].
- Manage the skill lifecycle with the gh skill CLI [P067].
- Maintain a lean CLAUDE.md of only broadly-applicable, non-obvious project context [P069].
- Account for IDE differences in supported instruction mechanisms [P071].
- Scope narrower guidance to matching files by adding .github/instructions/NAME.instructions.md files whose names end in .instructions.md, each beginning with an applyTo frontmatter key using glob syntax [P072].
- Design each Skill for its target surface's runtime limits [P080].
- When invoking Agent Skills through the API, always enable a code-execution tool and include the skills-2025-10-02 beta header; any code-execution tool version works [P081].
- Use a Project for persistent, always-loaded context that should inform every conversation about an initiative [P083].
- Do not assume Skills sync across surfaces [P090].
- Restrict which skills Claude can invoke by denying the Skill tool wholesale in /permissions or scoping with Skill(name) exact and Skill(name *) prefix rules [P091].
- Maintain AGENTS.md as a feedback loop [P092].
- Treat project context for an AI coding agent as durable infrastructure [P101].
- Account for the code execution environment's platform limits [P111].
- Manage skill visibility from settings with skillOverrides [P122].
- Scope every rule that applies to only some paths with a 'paths' frontmatter; leave a rule unscoped only when it truly must apply to all sessions [P124].
- Enable the code execution tool and set the code-execution-2025-08-25 and skills-2025-10-02 beta headers on every Skills request, adding files-api-2025-04-14 when files are transferred to or from the container [P133].
- Separate authoring from distribution [P134].
- Place a skill in the location matching its intended audience [P136].
- Layer Codex guidance in two tiers [P138].
- Design instruction files around Codex precedence [P140].
- Keep instruction files non-empty and within the size cap [P141].
- Troubleshoot instruction discovery systematically [P142].
- Select the instruction level [P143].
- Recommend always-on custom instructions when a team needs standards, guidelines, or expectations applied automatically across a scope; place them at the matching scope file [P144].
- When onboarding a repository with cloud-agent-generated instructions, keep them under two pages and non-task-specific [P145].

## Inputs

- The skill or instruction guidance to deploy, the named target surface(s) and their runtime and permission model, and the scope over which the guidance should apply.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P016]: Use manually invoked prompt files.
- Overlooking [P018]: Select Skills for a request via the Messages API container parameter, giving each entry type "anthropic", a skill_id.
- Overlooking [P026]: Retrieve a Skill-generated file through the Files API.
- Overlooking [P027]: Set invocation visibility deliberately with user-invocable and disable-model-invocation.
- Overlooking [P028]: Place a skill in the directory that matches its intended scope.
- Overlooking [P036]: Pre-approve the tools a skill needs via the SKILL.md allowed-tools frontmatter field to avoid a per-use confirmation prompt; any tool.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P016, P018, P026, P027, P028, P036, P038, P039, P054, P062, P066, P067, P069, P071, P072, P080, P081, P083, P090, P091, P092, P101, P111, P122, P124, P133, P134, P136, P138, P140, P141, P142, P143, P144, P145, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
