---
name: evaluating-and-iterating-on-skills
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P008
  - P041
  - P044
  - P045
  - P047
  - P052
  - P063
  - P065
  - P087
  - P099
  - P101
  - P102
  - P103
  - P107
  - P117
  - P145
  claims:
  - C00069
  - C00076
  - C00605
  - C00606
  - C01065
  - C01066
  - C01067
  - C01311
  - C01347
  - C01348
  - C00073
  - C00075
  evidence:
  - E00050
  - E00056
  - E00264
  - E00265
  - E00495
  - E00496
  - E00497
  - E00596
  - E00597
  - E00598
  - E00053
  - E00055
  source_anchors:
  - b2e7bb6f60c4-c0000
  - 2b076b2b50c8-c0000
  - 217629b356c0-c0000
  - ba55f4c06980-c0000
  - ba55f4c06980-c0001
  authored_from_digest: e8bd0def0517a7f2f44600c6d21893b6b1ce7a69b076ced89f353c4a5e185c92
---

# Skill: evaluating-and-iterating-on-skills

## Purpose

Prove whether a skill actually changes agent behaviour, and improve it in a disciplined loop —
rather than assuming it helps. Covers eval-driven development, baseline comparison, a realistic
test set, grader choice, and treating evals as perishable. Grounded in P007, P044, P045, P101,
P117.

## When to use

- You built or changed a skill and need to show it helps (capability uplift or encoded preference).
- A skill sometimes activates or behaves inconsistently and you must diagnose which dimension to fix.
- You are choosing how to grade agent output for an evaluation.

## Procedure

1. **Classify what the eval must prove.** Decide up front whether the skill is *capability uplift*
   or an *encoded preference*; this determines what a passing eval looks like [P102],
   [P007].
2. **Practise eval-driven development.** Define eval tasks that express the planned capability
   *before* the agent can fulfil them, then iterate until it performs [P007].
3. **Design a small, varied, realistic test set.** Begin with 2–3 cases; vary phrasing, detail,
   and formality; include at least one edge or boundary case; group by capability [P101].
4. **Run a baseline comparison.** Run each realistic prompt in a fresh session with the skill
   available, then again with it disabled, and compare — this isolates the skill's effect [P044].
   Use blind A/B comparison (outputs shown without revealing which variant produced which) to
   decide whether a change actually helped [P065].
5. **Isolate each run.** Give every eval run a clean context so only `SKILL.md` drives behaviour —
   a fresh subagent task where available, or a separate session otherwise [P052].
6. **Iterate as a loop.** Propose changes from the signals, apply them, rerun all cases in a new
   iteration directory, grade, aggregate, and repeat [P045]. Build a validation feedback loop:
   define quality criteria, run validation, fix the concrete failures, and re-run [P063].
7. **Choose graders by trade-off.** Prefer deterministic code-based graders where possible (fast,
   cheap, reproducible, but brittle to valid variation); use model-based or human graders where
   judgement is needed [P099]. Understand each method's trade-offs before relying on it [P087].
8. **Test across models and keep evals fresh.** Test the skill against every model it will run on
   and write instructions that work across them [P047]; treat evals as perishable — re-test each
   against new frontier-model releases and redesign when the model beats your strongest case
   [P145].
9. **Test the three-class matrix before deploying.** Exercise normal operations, edge cases, and
   out-of-scope requests, checking that the skill degrades gracefully [P117].
10. **Audit agentic-eval confounders.** Treat agentic evals as end-to-end system tests and audit
    confounders (cluster health, hardware, concurrency, bandwidth, time-of-day) before trusting a
    result [P103], [P107].

## Pitfalls / anti-patterns

- Declaring a skill effective with no baseline or eval to back the claim [P007], [P044].
- Iterating in the same polluted context so prior runs leak into the next [P052].
- Trusting a leaderboard delta inside noise, or an eval the current model has already saturated
  [P145].

## Grounding

Principles: P007, P008, P041, P044, P045, P047, P052, P063, P065, P087, P099, P101, P102, P103,
P107, P117, P145. Distillation-only: no verbatim source quotation.
