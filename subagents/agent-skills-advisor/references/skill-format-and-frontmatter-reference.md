---
name: skill-format-and-frontmatter-reference
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P005
  - P008
  - P009
  - P014
  - P018
  - P022
  - P023
  - P026
  - P028
  - P032
  - P033
  - P035
  - P039
  - P040
  - P043
  - P044
  - P048
  - P050
  - P052
  - P054
  - P056
  - P057
  - P062
  - P064
  - P066
  - P067
  - P068
  - P072
  - P074
  - P075
  - P077
  - P083
  - P085
  - P113
  - P119
  - P120
  - P121
  - P122
  - P125
  - P141
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00005
  - C00006
  - C00008
  - C00009
  - C00017
  - C00019
  - C00021
  - C00022
  - C00023
  - C00056
  evidence: []
  source_anchors: []
  authored_from_digest: 333ee9ee7b75b2e32b8cfc05fcc3269a1fe47c339234aeb0720f99b38c167fae
---


# Reference: skill-format-and-frontmatter-reference

## Purpose

The structural and frontmatter rules for a valid Agent Skill — folder shape, the SKILL.md entry file, the name/description contract, bundled scripts and resources, progressive-disclosure layering, and portability. Use it as a lookup when authoring or reviewing a SKILL.md.

## Principle index

Every principle this reference indexes, owned by the `authoring-agent-skills` skill. Each entry restates the operative core; the full statement lives in `../principles/principles.yaml`.

- **P001** — Package every skill as a minimal, valid skill folder.
- **P002** — Design Skills for three-tier progressive disclosure.
- **P003** — Treat the SKILL.md description as the sole triggering signal and invest effort accordingly.
- **P005** — Design Skills for progressive disclosure and a small context footprint.
- **P008** — Apply progressive disclosure.
- **P009** — Author skills from the agent's perspective and iterate empirically.
- **P014** — Write instructions that are structured, scannable.
- **P018** — Write the SKILL.md body as an operational recipe.
- **P022** — Give each skill a directory with SKILL.md as its required entrypoint, keep the body concise and under 500 lines.
- **P023** — Write concise skill descriptions with clear scope and boundaries, front-loading the primary use case and trigger words.
- **P026** — Author every Skill as a SKILL.md with valid YAML frontmatter carrying the required name and description; keep name ≤64 chars of lowercase letters, numbers and hyphens with no XML tags and no reserved.
- **P028** — For deterministic, repeatable work, ship an executable script and have Claude run it via bash rather than generating code inline.
- **P032** — For reusable logic, bundle a self-contained script that declares its dependencies inline _(supporting)_.
- **P033** — Package skills in the standard Agent Skills folder format.
- **P035** — Always supply the required SKILL.md frontmatter.
- **P039** — Package reusable procedural knowledge and organization-, team-, or user-specific context into portable, version-controlled skill folders loaded on demand.
- **P040** — Constrain the skill name to 1-64 characters using only lowercase alphanumerics and hyphens, never starting or ending with a hyphen and never using consecutive hyphens.
- **P043** — Author valid frontmatter.
- **P044** — Bundle reusable deterministic scripts for recurring, mechanically-checkable operations and have the agent run them by default instead of regenerating the code.
- **P048** — Design skill resources around lazy access.
- **P050** — Name each skill in lowercase letters, numbers.
- **P052** — Rely on Claude's automatic Skill matching and progressive disclosure rather than hardcoding invocation.
- **P054** — For complex skills, route by task type with a decision tree, show complex patterns with paired good/bad examples.
- **P056** — Write a precise, trigger-oriented description.
- **P057** — Keep SKILL.md focused on task instructions and push optional material into the conventional subfolders.
- **P062** — Author skills as small, single-purpose composable units rather than monoliths.
- **P064** — Author skills against the open Agent Skills standard so they stay portable across any AI platform that implements it.
- **P066** — Provide output templates whose strictness matches the need.
- **P067** — Always use forward-slash file paths in skill instructions and references so skills work across platforms, including Unix.
- **P068** — In bundled scripts, handle error conditions explicitly and justify/document every configuration constant.
- **P072** — Aim for moderate detail.
- **P074** — Give a single sensible default with an escape hatch, mentioning alternatives only briefly.
- **P075** — When inputs can be rendered as images, have the model inspect them visually to reason about spatial layout, form structure.
- **P077** — Scaffold a new skill with the skill-creator skill instead of hand-editing files _(supporting)_.
- **P083** — Make frontmatter descriptions precise enough for automatic loading.
- **P085** — Prefer a runtime dependency-resolving tool runner.
- **P113** — Author each skill to encode discovery, orchestration _(supporting)_.
- **P119** — Structure every skill as a directory whose SKILL.md opens with YAML frontmatter defining name and description; the agent pre-loads that metadata at startup as the first level of progressive.
- **P120** — Package deterministic or expensive operations as executable code inside the skill instead of relying on token generation; code is cheaper for such work and gives consistent, repeatable results.
- **P121** — Keep the main skill file concise, structured.
- **P122** — Package multi-step workflows with bundled instructions, scripts.
- **P125** — Offer multiple authoring paths.
- **P141** — Structure every Agent Skill as a folder containing a single SKILL.md file that opens with a YAML frontmatter block.

## Grounding

Indexes 43 of the package's 150 principles, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`). Every id resolves into `principles/principles.yaml`.
