---
name: evaluating-mcp-agents-and-judges
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P009
  - P010
  - P011
  - P014
  - P016
  - P019
  - P033
  - P034
  - P037
  - P042
  - P050
  - P051
  - P052
  - P066
  - P070
  - P071
  - P072
  - P073
  - P078
  - P082
  - P087
  - P089
  - P090
  - P093
  - P094
  - P126
  - P127
  - P129
  - P130
  - P136
  - P169
  - P170
  - P171
  - P178
  - P180
  - P181
  - P182
  - P183
  - P184
  - P197
  - P198
  claims:
  - C00096
  - C00211
  - C00212
  - C00094
  - C00122
  - C00050
  - C00158
  - C00469
  - C00470
  - C00472
  - C00473
  - C00474
  - C00475
  - C00476
  - C00477
  - C00481
  - C00493
  - C00417
  evidence:
  - E00033
  - E00076
  - E00077
  - E00032
  - E00049
  - E00003
  - E00056
  - E00268
  - E00269
  - E00271
  - E00272
  - E00273
  - E00274
  - E00275
  - E00276
  source_anchors:
  - eaca3d50aebb-c0001
  - ba55f4c06980-c0000
  - b6b7517bef5b-c0000
  - 46bbfd26b8df-c0004
  - b6b7517bef5b-c0001
  - b348d1cbd170-c0001
  authored_from_digest: 96c787a60a206aecddd1c834d22d0657d766359040325b77a95baf6ea3f9fb16
---

# Skill: evaluating-mcp-agents-and-judges

## Purpose

Design evaluations that prove — rather than assert — the quality of an MCP server or tool-augmented agent. Choose metrics, run against real servers, construct sound benchmarks, select and reliability-check LLM judges, and localize failures to the responsible stage [P008], [P009], [P051], [P078].

## When to use

- You need to measure or compare MCP servers, tools, or agent tool-use quality.
- You are choosing metrics, graders, or an LLM-as-judge setup for an agent eval.
- You are building a benchmark or diagnosing why an agent fails on tool tasks.

## Procedure

1. **Match the metric to the question.** Use single-run success rate as the primary measure, pass@k for capability-under-retries, and pass^k for reliability; evaluate an MCP server on answer accuracy, end-to-end latency, and token consumption together, not one axis alone [P008], [P183]. Understand each method's trade-offs before relying on it [P034].
2. **Evaluate against real production servers.** Run evaluation against exclusively real, production servers rather than mocked substitutes so authentic errors and behaviours surface, and evaluate on large-scale, multi-server, dynamic toolsets that force real tool retrieval [P009], [P126]. Expect a wide performance spread across servers and select accordingly [P184].
3. **Choose grader types by trade-off.** Prefer deterministic code-based graders where possible (fast, cheap, reproducible); add an LLM rubric grader for open-ended quality; for coding agents combine outcome tests with a rubric [P052], [P169]. Make evaluation robust to tool-use hallucination by decomposing tasks into explicit completion criteria [P070].
4. **Do not trust a single judge.** Do not assume any single judge is uniformly reliable, or that the largest/most expensive model is best; score with multiple independent judges and always report and pin the judge model version [P051], [P127], [P072]. Before deploying a judge, run a reliability suite that stress-tests it with targeted perturbations [P073].
5. **Test judge consistency with perturbations.** Stress judges with meaning-preserving perturbations — formatting-only changes, semantic paraphrase — and explicitly test format invariance (blank lines, spacing, indentation), because judges are frequently more sensitive to format than meaning [P089], [P171].
6. **Construct benchmarks with a proposer/validator pipeline.** Build tasks with a two-stage human pipeline of separate proposers and validators; write self-contained plain-English questions with a single unambiguous answer, and require multi-hop reasoning across scattered sources where you mean to test it [P071], [P014], [P010]. Establish protocol-level orchestration benchmarks that emit binary plus structured results [P042].
7. **Diagnose failures by mode and stage.** Assign one primary failure mode plus contributing factors; separate query errors, retrieval/selection errors, and reasoning errors, and expect cognitive failures to dominate once basic tool mechanics are solved [P019], [P178], [P129]. Diagnose wrong-tool selection and bad arguments as a specification problem in the description [P128].
8. **Read transcripts and practice eval-driven development.** Read transcripts and grades from many trials regularly and invest in transcript-viewing tooling — you cannot fix what you do not inspect [P130]. Build evals early and practice eval-driven development: define eval tasks expressing planned capabilities before the agent can pass them, and treat the suite as a living, owned artifact [P170], [P182], [P181].

## Pitfalls / anti-patterns

- Declaring quality from a demo or a single run against a mock server [P009].
- Trusting one big judge model as ground truth without a reliability check [P051], [P073].
- Comparing only accuracy while ignoring latency and token cost [P183].

## Grounding

Principles: P008, P009, P010, P011, P014, P016, P019, P033, P034, P037, P042, P050, P051, P052, P066, P070, P071, P072, P073, P078, P082, P087, P089, P090, P093, P094, P126, P127, P129, P130, P136, P169, P170, P171, P178, P180, P181, P182, P183, P184, P197, P198. Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.
