---
name: skill-format-and-frontmatter-reference
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P006
  - P007
  - P011
  - P014
  - P015
  - P017
  - P019
  - P020
  - P021
  - P022
  - P024
  - P025
  - P032
  - P037
  - P045
  - P047
  - P048
  - P053
  - P055
  - P056
  - P058
  - P061
  - P079
  - P085
  - P086
  - P087
  - P100
  - P108
  - P109
  - P110
  - P112
  - P113
  - P116
  - P119
  - P120
  - P123
  - P137
  - P139
  - P147
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00006
  - C00008
  - C00009
  - C00017
  - C00019
  - C00021
  - C00022
  - C00023
  - C00056
  - C00057
  evidence: []
  source_anchors: []
  authored_from_digest: 79884ee9a61c2909ebbe8e670d594967f48568d22e30eda084a5ef5b2550175b
---


# Reference: skill-format-and-frontmatter-reference

## Purpose

The structural and frontmatter rules for a valid Agent Skill — folder shape, the SKILL.md entry file, the name/description contract, bundled scripts and resources, progressive-disclosure layering, and portability. Use it as a lookup when authoring or reviewing a SKILL.md.

## Principle index

Every principle this reference indexes, owned by the `authoring-agent-skills` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P001** — Design Skills for progressive disclosure and a small context footprint.
- **P002** — Treat the SKILL.md description as the sole triggering signal and invest effort accordingly.
- **P003** — Apply progressive disclosure.
- **P004** — Author each agent skill as a self-contained directory whose SKILL.md is the entry point and which also holds any scripts or resources the instructions reference; Copilot auto-discovers every file.
- **P006** — Author skills from the agent's perspective and iterate empirically.
- **P007** — Design Skills for three-tier progressive disclosure.
- **P011** — Write instructions that are structured, scannable.
- **P014** — Treat Skills as executable software.
- **P015** — Write concise skill descriptions with clear scope and boundaries, front-loading the primary use case and trigger words.
- **P017** — For deterministic, repeatable work, ship an executable script and have Claude run it via bash rather than generating code inline.
- **P019** — Match instruction strictness to task risk and fragility.
- **P020** — Package skills in the standard Agent Skills folder format.
- **P021** — Always supply the required SKILL.md frontmatter.
- **P022** — Use progressive disclosure.
- **P024** — Enforce Skill frontmatter constraints.
- **P025** — Bundle reusable deterministic scripts for repeatable, mechanically checkable skill operations.
- **P032** — Rely on Claude's automatic Skill matching and progressive disclosure rather than hardcoding invocation.
- **P037** — Write the SKILL.md body as actionable instructions, examples.
- **P045** — Use skills to turn multi-step tasks into consistent, auditable, repeatable procedures rather than one-off ad-hoc runs.
- **P047** — Author skills against the open Agent Skills specification to keep them portable across compatible AI platforms.
- **P048** — Use forward-slash file paths in skill instructions and references for cross-platform compatibility.
- **P053** — Aim for moderate detail.
- **P055** — When multiple tools or approaches could work, pick one default and mention alternatives only briefly instead of presenting equal options.
- **P056** — Use rendered images and visual inspection when a skill must reason about spatial layout, form structure, or other visual input properties.
- **P058** — Scaffold a new skill with the skill-creator skill instead of hand-editing files _(supporting)_.
- **P061** — Make frontmatter descriptions precise enough for automatic loading.
- **P079** — Keep every Skill concise.
- **P085** — Author every Skill as a SKILL.md with valid YAML frontmatter carrying the required name and description; keep name ≤64 chars of lowercase letters, numbers and hyphens with no XML tags and no reserved.
- **P086** — Write skill metadata so discovery works.
- **P087** — Author a skill as a SKILL.md plus optional scripts, references.
- **P100** — Author each skill to encode discovery, orchestration _(supporting)_.
- **P108** — For reusable logic, bundle a self-contained script that declares its dependencies inline _(supporting)_.
- **P109** — Structure every skill as a directory whose SKILL.md opens with YAML frontmatter defining name and description; the agent pre-loads that metadata at startup as the first level of progressive.
- **P110** — Package deterministic or expensive operations as executable code inside the skill instead of relying on token generation; code is cheaper for such work and gives consistent, repeatable results.
- **P112** — Keep the main skill file concise, structured.
- **P113** — Package multi-step workflows with bundled instructions, scripts.
- **P116** — Constrain the skill name to 1-64 characters using only lowercase alphanumerics and hyphens, never starting or ending with a hyphen and never using consecutive hyphens.
- **P119** — Offer multiple authoring paths.
- **P120** — Package every skill as a minimal, valid skill folder.
- **P123** — Match instruction specificity to task fragility.
- **P137** — Package a skill as a directory containing a SKILL.md.
- **P139** — Structure every Agent Skill as a folder containing a single SKILL.md file that opens with a YAML frontmatter block.
- **P147** — Prefer high-fidelity references.

## Grounding

Indexes 43 of the package's 150 principles, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
