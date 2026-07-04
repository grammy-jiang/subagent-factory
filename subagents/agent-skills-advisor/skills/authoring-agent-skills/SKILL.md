---
name: authoring-agent-skills
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P003
  - P005
  - P012
  - P014
  - P024
  - P025
  - P029
  - P032
  - P034
  - P035
  - P038
  - P040
  - P088
  - P092
  - P093
  - P112
  - P113
  - P114
  - P115
  - P120
  - P135
  - P150
  - P019
  - P059
  claims:
  - C00003
  - C00004
  - C00021
  - C00022
  - C00023
  - C00059
  - C00060
  - C00061
  - C00062
  - C00063
  - C00070
  - C00071
  evidence:
  - E00003
  - E00004
  - E00012
  - E00013
  - E00014
  - E00041
  - E00042
  - E00043
  - E00044
  - E00045
  - E00051
  - E00052
  source_anchors:
  - 3a6becc3c67a-c0000
  - 0bc9d8042bad-c0000
  - b2e7bb6f60c4-c0000
  authored_from_digest: 8404a9a4aa5733bc7e8b8d6eeb80fa5dd6f1078d2ee21de6fc7ee93feecd6680
---

# Skill: authoring-agent-skills

## Purpose

Author an Agent Skill as a self-contained `SKILL.md` (plus optional scripts, references, and
assets) that an agent can discover, load lazily, and run reliably — keeping the always-loaded
footprint tiny and pushing bulk detail behind progressive disclosure. Grounded in P001, P003,
P005, P088, P112, P135.

## When to use

- You are creating a new skill, or restructuring one whose `SKILL.md` has grown large.
- A skill covers multiple processes or carries heavy reference material that does not belong in
  the always-loaded body.
- You need one skill to run unchanged across the agent platforms that implement the standard.

## Procedure

1. **Create the skill folder and entry file.** The folder name is kebab-case; the entry file is
   exactly `SKILL.md` at its root; scripts, references, and assets live beside it in the same
   directory so the skill is self-contained [P003], [P115], [P120], [P135].
2. **Write valid frontmatter first.** Open `SKILL.md` with a YAML frontmatter block declaring a
   `name` (lowercase letters, numbers, hyphens; ≤64 chars; no leading/trailing hyphen, no reserved
   words or XML tags) and a `description` stating what the skill does and when to use it — this
   metadata is pre-loaded for discovery [P025], [P032], [P034], [P092], [P112], [P150]. For the
   exact field rules see the `skill-format-and-frontmatter-reference`.
3. **Design for three-tier progressive disclosure.** Keep only the tiny name+description in
   frontmatter (always loaded, aim ~100 tokens), put the working instructions in the `SKILL.md`
   body (loaded when the skill is judged relevant), and move bulk detail into a `references/`
   directory loaded only on demand — so an agent can hold many skills without exhausting context
   [P001], [P005], [P038].
4. **Write the body as an operational recipe.** State what it accomplishes, when to use it, the
   step-by-step procedure, and input/output examples; use markdown headers, bullets, and code
   blocks with a clear section hierarchy so it is scannable and actionable [P012], [P014].
5. **Keep it concise and within budget.** Hold the `SKILL.md` body under ~500 lines / ~5,000
   tokens; add only context the model lacks and challenge each line against its token cost. Prefer
   concise stepwise guidance with a working example over exhaustive documentation [P029], [P088],
   [P114], [P059].
6. **Push deterministic work into scripts.** For recurring, mechanically-checkable, or expensive
   operations, bundle a self-contained executable script and instruct the agent to run it by
   default rather than regenerating code inline — the script's source is auditable and repeatable
   [P019], [P035], [P113].
7. **Choose an authoring path and keep it portable.** Author against the open Agent Skills
   standard (assisted creation, direct instruction writing, or a skill-creator workflow) so one
   skill built once runs across platforms [P024], [P093], [P119 via profile].

## Pitfalls / anti-patterns

- Dumping every detail into `SKILL.md` instead of layering it — bloats context and buries the
  signal [P088], [P114].
- A vague `name`/`description` that the agent cannot match at load time [P025].
- Generating deterministic code inline every run instead of shipping a script [P035].
- Platform-specific paths baked into instructions; use forward-slash paths for portability.

## Grounding

Principles: P001, P003, P005, P012, P014, P019, P024, P025, P029, P032, P034, P035, P038, P040,
P059, P088, P092, P093, P112, P113, P114, P115, P120, P135, P150. Distillation-only: no verbatim
source quotation.
