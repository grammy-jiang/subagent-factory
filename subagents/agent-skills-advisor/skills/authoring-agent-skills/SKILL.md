---
name: authoring-agent-skills
kind: skill
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


# Skill: authoring-agent-skills

## Purpose

Author an Agent Skill as a self-contained SKILL.md — plus optional bundled scripts, references, and assets — that an agent can discover from its description, load lazily, and run reliably. It keeps the always-loaded frontmatter tiny, designs for three-tier progressive disclosure, writes the body as a scannable operational recipe within its context budget, pushes deterministic work into bundled scripts, and stays portable across the platforms that implement the open Agent Skills standard.

## When to use

- Creating a new skill, or restructuring one whose SKILL.md has grown large or unfocused.
- Writing or reviewing the frontmatter name and description that drive discovery and triggering.
- Deciding how to split instructions, references, scripts, and assets across the skill folder for progressive disclosure.
- Making one skill run unchanged across the agent platforms that implement the standard.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Package every skill as a minimal, valid skill folder [P001].
- Design Skills for three-tier progressive disclosure [P002].
- Treat the SKILL.md description as the sole triggering signal and invest effort accordingly [P003].
- Design Skills for progressive disclosure and a small context footprint [P005].
- Apply progressive disclosure [P008].
- Author skills from the agent's perspective and iterate empirically [P009].
- Write instructions that are structured, scannable [P014].
- Write the SKILL.md body as an operational recipe [P018].
- Give each skill a directory with SKILL.md as its required entrypoint, keep the body concise and under 500 lines [P022].
- Write concise skill descriptions with clear scope and boundaries, front-loading the primary use case and trigger words [P023].
- Author every Skill as a SKILL.md with valid YAML frontmatter carrying the required name and description; keep name ≤64 chars of lowercase letters, numbers and hyphens with no XML tags and no reserved words [P026].
- For deterministic, repeatable work, ship an executable script and have Claude run it via bash rather than generating code inline [P028].
- For reusable logic, bundle a self-contained script that declares its dependencies inline [P032].
- Package skills in the standard Agent Skills folder format [P033].
- Always supply the required SKILL.md frontmatter [P035].
- Package reusable procedural knowledge and organization-, team-, or user-specific context into portable, version-controlled skill folders loaded on demand [P039].
- Constrain the skill name to 1-64 characters using only lowercase alphanumerics and hyphens, never starting or ending with a hyphen and never using consecutive hyphens [P040].
- Author valid frontmatter [P043].
- Bundle reusable deterministic scripts for recurring, mechanically-checkable operations and have the agent run them by default instead of regenerating the code [P044].
- Design skill resources around lazy access [P048].
- Name each skill in lowercase letters, numbers [P050].
- Rely on Claude's automatic Skill matching and progressive disclosure rather than hardcoding invocation [P052].
- For complex skills, route by task type with a decision tree, show complex patterns with paired good/bad examples [P054].
- Write a precise, trigger-oriented description [P056].
- Keep SKILL.md focused on task instructions and push optional material into the conventional subfolders [P057].
- Author skills as small, single-purpose composable units rather than monoliths [P062].
- Author skills against the open Agent Skills standard so they stay portable across any AI platform that implements it [P064].
- Provide output templates whose strictness matches the need [P066].
- Always use forward-slash file paths in skill instructions and references so skills work across platforms, including Unix [P067].
- In bundled scripts, handle error conditions explicitly and justify/document every configuration constant [P068].
- Aim for moderate detail [P072].
- Give a single sensible default with an escape hatch, mentioning alternatives only briefly [P074].
- When inputs can be rendered as images, have the model inspect them visually to reason about spatial layout, form structure [P075].
- Scaffold a new skill with the skill-creator skill instead of hand-editing files [P077].
- Make frontmatter descriptions precise enough for automatic loading [P083].
- Prefer a runtime dependency-resolving tool runner [P085].
- Author each skill to encode discovery, orchestration [P113].
- Structure every skill as a directory whose SKILL.md opens with YAML frontmatter defining name and description; the agent pre-loads that metadata at startup as the first level of progressive disclosure [P119].
- Package deterministic or expensive operations as executable code inside the skill instead of relying on token generation; code is cheaper for such work and gives consistent, repeatable results [P120].
- Keep the main skill file concise, structured [P121].
- Package multi-step workflows with bundled instructions, scripts [P122].
- Offer multiple authoring paths [P125].
- Structure every Agent Skill as a folder containing a single SKILL.md file that opens with a YAML frontmatter block [P141].

## Inputs

- The skill or capability being authored, its current SKILL.md and folder layout if any, and the workflow it must perform.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P001]: Package every skill as a minimal, valid skill folder.
- Overlooking [P002]: Design Skills for three-tier progressive disclosure.
- Overlooking [P003]: Treat the SKILL.md description as the sole triggering signal and invest effort accordingly.
- Overlooking [P005]: Design Skills for progressive disclosure and a small context footprint.
- Overlooking [P008]: Apply progressive disclosure.
- Overlooking [P009]: Author skills from the agent's perspective and iterate empirically.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P001, P002, P003, P005, P008, P009, P014, P018, P022, P023, P026, P028, P032, P033, P035, P039, P040, P043, P044, P048, P050, P052, P054, P056, P057, P062, P064, P066, P067, P068, P072, P074, P075, P077, P083, P085, P113, P119, P120, P121, P122, P125, P141, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
