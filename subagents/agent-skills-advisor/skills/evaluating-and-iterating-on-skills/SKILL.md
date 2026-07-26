---
name: evaluating-and-iterating-on-skills
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P012
  - P030
  - P033
  - P034
  - P035
  - P040
  - P041
  - P042
  - P044
  - P046
  - P050
  - P070
  - P077
  - P078
  - P089
  - P094
  - P096
  - P098
  - P099
  - P104
  - P117
  claims:
  - C00069
  - C00076
  - C00102
  - C00103
  - C00104
  - C00105
  - C00113
  - C00123
  - C00124
  - C00125
  - C00126
  - C00127
  - C00132
  - C00134
  evidence: []
  source_anchors: []
  authored_from_digest: 07e47134255b2ef46562a5d29d5ed02e03d7632ea5ab8e80d0fee2d562caacce
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

- Build evaluations before writing extensive documentation and develop the Skill test-first [P010].
- Use an independent, blinded A/B comparison to judge whether one Skill version or a Skill-enabled run is genuinely better than the alternative [P012].
- Debug a skill by adjusting the dimension that fails [P030].
- Evaluate a skill with a baseline comparison [P033].
- Treat skill evaluation as an iterative loop [P034].
- Test each Skill against every model it will run on and write instructions that work across all target models [P035].
- Capture each run's total token count and duration immediately when the completion notification arrives [P040].
- Use specific, objectively verifiable assertions and reusable scripts for programmatic checks; leave subjective qualities such as style or visual design to human review [P041].
- Before optimizing a Skill description, build about 20 realistic trigger-evaluation queries balanced between should-trigger cases and genuine should-not-trigger near-misses [P042].
- Maintain regression evals and rerun them when models or surrounding infrastructure change so behavioral regressions are visible before shipping [P044].
- Isolate each eval run with a clean context so only SKILL.md drives behaviour, using fresh subagent tasks where available or a separate session otherwise [P046].
- Evaluate and improve the model together with its harness [P050].
- Diagnose every inaccurate analytics-agent answer as one of three failure modes - concept-to-entity ambiguity, data staleness, or retrieval failure - and architect each stack layer to attack a specific one; the largest gains come [P070].
- Separate infrastructure-reliability gains from capability gains [P077].
- Understand each evaluation method's trade-offs before relying on it [P078].
- Treat a wrong analytics answer as a mapping failure [P089].
- Choose grader types by trade-off [P094].
- Design a small, varied, realistic test set [P096].
- Classify a skill as capability uplift or encoded preference before deciding what its evals must prove [P098].
- Treat agentic evals as end-to-end system tests and audit all confounders [P099].
- Evaluate tool quality with realistic workflow tasks, realistic data, verifiable outcomes [P104].
- Before deploying, test the skill with a three-class matrix [P117].

## Inputs

- The skill under evaluation, the capability or behaviour it should improve, and the realistic prompts, data, and success criteria to judge it on.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P010]: Build evaluations before writing extensive documentation and develop the Skill test-first.
- Overlooking [P012]: Use an independent, blinded A/B comparison to judge whether one Skill version or a Skill-enabled run is genuinely better.
- Overlooking [P030]: Debug a skill by adjusting the dimension that fails.
- Overlooking [P033]: Evaluate a skill with a baseline comparison.
- Overlooking [P034]: Treat skill evaluation as an iterative loop.
- Overlooking [P035]: Test each Skill against every model it will run on and write instructions that work across all target models.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P010, P012, P030, P033, P034, P035, P040, P041, P042, P044, P046, P050, P070, P077, P078, P089, P094, P096, P098, P099, P104, P117, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
