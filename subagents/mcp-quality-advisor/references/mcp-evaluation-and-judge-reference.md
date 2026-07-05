---
name: mcp-evaluation-and-judge-reference
kind: reference
status: ready
provenance:
  principles:
  - P008
  - P009
  - P034
  - P037
  - P050
  - P051
  - P052
  - P070
  - P071
  - P072
  - P073
  - P078
  - P089
  - P090
  - P126
  - P127
  - P130
  - P136
  - P137
  - P169
  - P171
  - P178
  - P180
  - P181
  - P182
  - P183
  - P184
  - P019
  - P042
  claims:
  - C00096
  - C00211
  - C00212
  - C00094
  - C00122
  - C00237
  - C00238
  - C00239
  - C00240
  - C00241
  - C00242
  - C00331
  - C00333
  - C00334
  - C00335
  - C00352
  - C00353
  - C00896
  evidence:
  - E00033
  - E00076
  - E00077
  - E00032
  - E00049
  - E00086
  - E00087
  - E00088
  - E00089
  - E00090
  - E00091
  - E00154
  - E00156
  - E00157
  - E00158
  source_anchors:
  - eaca3d50aebb-c0001
  - ba55f4c06980-c0000
  - b6b7517bef5b-c0000
  - ba55f4c06980-c0001
  - 1a9237dbcad1-c0001
  - 1a9237dbcad1-c0002
  authored_from_digest: 8ab37af631eb7efe1b0d00cc0406c57c15ef528466105de51680e0268a3a6b1d
---

# MCP Evaluation & LLM-as-Judge Reference

Reference for evaluating MCP servers and tool-augmented agents: metric selection, grader types, judge reliability, and failure diagnosis. Prove quality against real servers rather than asserting it [P009], [P008].

## Metrics

- Primary: single-run success rate; pass@k for capability under retries; pass^k for reliability [P008].
- Evaluate a server on accuracy, end-to-end latency, and token consumption together [P183].
- Measure description/tool changes with execution-based metrics (success rate, avg steps), not intuition [P037].
- Understand each method's trade-offs before relying on it; automated evals are fast and reproducible but partial [P034].

## Graders & judges

- Prefer deterministic code-based graders where possible; add an LLM rubric grader for open-ended quality [P052].
- For coding agents combine outcome tests with an LLM rubric [P169].
- Do not trust a single judge or assume the biggest model is best; use multiple independent judges [P051], [P127], [P072].
- Run a judge-reliability suite before deploying; stress with meaning-preserving perturbations and format-invariance tests [P073], [P089], [P171].
- Always report and pin the judge model version and per-model results [P127].

## Benchmark construction

- Use a two-stage proposer/validator human pipeline; write self-contained, single-answer questions [P071], [P014].
- Evaluate on large-scale, multi-server, dynamic toolsets that force real tool retrieval [P126].
- Make evaluation robust to tool-use hallucination by decomposing tasks into explicit completion criteria [P070].
- Score argument correctness with targeted metrics (hallucinated names, wrong values, missing required) [P137].

## Failure diagnosis & process

- Assign one primary failure mode plus contributing factors; separate query, retrieval, and reasoning errors [P178], [P019].
- Read transcripts and grades regularly; invest in transcript-viewing tooling [P130].
- Establish protocol-level orchestration benchmarks emitting binary plus structured results [P042].
- Practice eval-driven development: build evals early; treat the suite as a living, owned artifact [P182], [P181], [P180], [P090], [P078], [P050], [P184], [P016], [P033], [P066], [P082], [P087], [P093], [P094], [P129], [P136], [P170], [P197], [P198], [P011].

## Grounding

Principles: P008, P009, P034, P037, P050, P051, P052, P070, P071, P072, P073, P078, P089, P090, P126, P127, P130, P136, P137, P169, P171, P178, P180, P181, P182, P183, P184, P019, P042. Sources are distillation-only; no verbatim source quotation.
