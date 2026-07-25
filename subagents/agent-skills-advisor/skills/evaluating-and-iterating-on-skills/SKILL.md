---
name: evaluating-and-iterating-on-skills
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P013
  - P015
  - P053
  - P055
  - P061
  - P063
  - P078
  - P090
  - P092
  - P098
  - P099
  - P103
  - P108
  - P110
  - P112
  - P116
  - P124
  claims:
  - C00069
  - C00076
  - C00102
  - C00103
  - C00104
  - C00105
  - C00108
  - C00113
  - C00123
  - C00124
  - C00125
  - C00126
  - C00127
  - C00130
  evidence: []
  source_anchors: []
  authored_from_digest: 3fcedee48b176628921a9598e44de4a8c860a774c51784f196c3d500f17f3abe
---


# Skill: evaluating-and-iterating-on-skills

## Purpose

Prove and improve a skill's effect on agent behaviour with evaluation rather than assertion. It practises eval-driven development: define eval tasks first, run a baseline (skill vs no-skill) comparison in a clean, isolated context, choose graders by their trade-offs, design a small varied realistic test set, treat agentic evals as end-to-end system tests that audit confounders, and iterate the skill by adjusting the dimension that fails.

## When to use

- Proving a skill actually helps, with a baseline comparison rather than an assertion.
- Designing the eval task set, the graders, and the isolated run harness for a skill.
- A skill triggers on the wrong prompts, loads the wrong guidance, or underperforms and must be debugged by dimension.
- Deciding what a skill's evals must prove before shipping it.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Practice eval-driven development [P006].
- Debug a skill by adjusting the dimension that fails [P013].
- Treat skill evaluation as an iterative loop [P015].
- Evaluate a skill with a baseline comparison [P053].
- Test each skill against every model it will run [P055].
- Iterate skills from real-world usage [P061].
- Isolate each eval run with a clean context so only SKILL.md drives behaviour, using fresh subagent tasks where available or a separate session otherwise [P063].
- Use blind A/B comparison [P078].
- Treat agentic evals as end-to-end system tests and audit all confounders [P090].
- Diagnose every inaccurate analytics-agent answer as one of three failure modes - concept-to-entity ambiguity, data staleness, or retrieval failure - and architect each stack layer to attack a specific one; the largest gains come [P092].
- Separate infrastructure-reliability gains from capability gains [P098].
- Understand each evaluation method's trade-offs before relying on it [P099].
- Treat a wrong analytics answer as a mapping failure [P103].
- Choose grader types by trade-off [P108].
- Design a small, varied, realistic test set [P110].
- Classify a skill as capability uplift or encoded preference before deciding what its evals must prove [P112].
- Evaluate tool quality with realistic workflow tasks, realistic data, verifiable outcomes [P116].
- Before deploying, test the skill with a three-class matrix [P124].

## Inputs

- The skill under evaluation, the capability or behaviour it should improve, and the realistic prompts, data, and success criteria to judge it on.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P006]: Practice eval-driven development.
- Overlooking [P013]: Debug a skill by adjusting the dimension that fails.
- Overlooking [P015]: Treat skill evaluation as an iterative loop.
- Overlooking [P053]: Evaluate a skill with a baseline comparison.
- Overlooking [P055]: Test each skill against every model it will run.
- Overlooking [P061]: Iterate skills from real-world usage.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P006, P013, P015, P053, P055, P061, P063, P078, P090, P092, P098, P099, P103, P108, P110, P112, P116, P124, grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
