---
name: deploying-skills-across-platforms
kind: skill
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

- Place a skill in the location matching its intended audience [P004].
- To run Skills on the Claude API, send the three required beta headers [P010].
- Place guidance at the right location [P012].
- Use allowed-tools to pre-approve tools while a skill is active and disallowed-tools to remove them [P016].
- Treat skills as an untrusted-code supply chain [P020].
- Design each Skill for its target surface's runtime limits [P021].
- Use prompt files (*.prompt.md under .github/prompts/) for reusable, task-specific chat interactions run repeatedly with different inputs, keeping them distinct from codebase-wide custom instructions and invoking them manually [P024].
- Select Skills for a request via the Messages API container parameter, giving each entry type "anthropic", a skill_id [P029].
- Design instruction files around Codex precedence [P030].
- Match instruction strictness to task fragility [P031].
- Install skills per surface [P038].
- Retrieve a Skill-generated file through the Files API [P045].
- Set invocation visibility deliberately with user-invocable and disable-model-invocation [P046].
- Keep AGENTS.md small and scoped to durable, repo-specific rules the agent must follow every time [P047].
- Put guidance that should apply to every request in a repository-wide file located exactly at .github/copilot-instructions.md, creating the .github directory first if it does not exist [P058].
- Recognize that GitHub Copilot supports three repository custom-instruction types [P059].
- Do not rely on Zero Data Retention for Agent Skills [P073].
- Select a Copilot customization feature by matching its trigger model to the task [P084].
- Treat project context for an AI coding agent as durable infrastructure [P087].
- Before promising a customization feature works on a given IDE or surface, verify it against the feature-support matrix and recommend the latest stable IDE/CLI/extension versions [P088].
- Manage the skill lifecycle with the gh skill CLI [P089].
- Maintain a lean CLAUDE.md of only broadly-applicable, non-obvious project context [P091].
- Account for IDE differences in supported instruction mechanisms [P093].
- Scope narrower guidance to matching files by adding .github/instructions/NAME.instructions.md files whose names end in .instructions.md, each beginning with an applyTo frontmatter key using glob syntax [P094].
- Use a Project for persistent, always-loaded context that should inform every conversation about an initiative [P101].
- Check runtime and plan prerequisites before choosing a block [P102].
- Do not assume Skills sync across surfaces [P104].
- Restrict which skills Claude can invoke by denying the Skill tool wholesale in /permissions or scoping with Skill(name) exact and Skill(name *) prefix rules [P105].
- Maintain AGENTS.md as a feedback loop [P106].
- Manage skill visibility from settings with skillOverrides [P127].
- Match instruction specificity to task fragility [P128].
- Scope every rule that applies to only some paths with a 'paths' frontmatter; leave a rule unscoped only when it truly must apply to all sessions [P129].
- Avoid custom output styles unless a significant role change is required; prefer the built-in Proactive/Explanatory/Learning styles [P130].
- Enable the code execution tool and set the code-execution-2025-08-25 and skills-2025-10-02 beta headers on every Skills request, adding files-api-2025-04-14 when files are transferred to or from the container [P138].
- Layer Codex guidance in two tiers [P140].
- Keep instruction files non-empty and within the size cap [P142].
- Troubleshoot instruction discovery systematically [P143].
- Select the instruction level [P144].
- Recommend always-on custom instructions when a team needs standards, guidelines, or expectations applied automatically across a scope; place them at the matching scope file [P145].
- When onboarding a repository with cloud-agent-generated instructions, keep them under two pages and non-task-specific [P146].

## Inputs

- The skill or instruction guidance to deploy, the named target surface(s) and their runtime and permission model, and the scope over which the guidance should apply.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P004]: Place a skill in the location matching its intended audience.
- Overlooking [P010]: To run Skills on the Claude API, send the three required beta headers.
- Overlooking [P012]: Place guidance at the right location.
- Overlooking [P016]: Use allowed-tools to pre-approve tools while a skill is active and disallowed-tools to remove them.
- Overlooking [P020]: Treat skills as an untrusted-code supply chain.
- Overlooking [P021]: Design each Skill for its target surface's runtime limits.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P004, P010, P012, P016, P020, P021, P024, P029, P030, P031, P038, P045, P046, P047, P058, P059, P073, P084, P087, P088, P089, P091, P093, P094, P101, P102, P104, P105, P106, P127, P128, P129, P130, P138, P140, P142, P143, P144, P145, P146, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
