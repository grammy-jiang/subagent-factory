---
name: mcp-evaluation-and-judge-reference
kind: reference
status: ready
provenance:
  principles:
  - P009
  - P019
  - P022
  - P036
  - P040
  - P067
  - P068
  - P078
  - P082
  - P083
  - P084
  - P089
  - P097
  - P119
  - P120
  - P137
  - P140
  - P141
  - P147
  - P148
  - P190
  - P191
  - P192
  authored_from_digest: bd5aa2d9842583078960372f0b17158930f70a02884a9e55175ded033c050af0
---

# Reference: MCP evaluation and LLM-judge reference

Reference for evaluating MCP agents and servers and for using an LLM-as-a-Judge reliably. Prove quality
by measurement against real servers, not assertion [P022].

## Metric selection

- Match the metric to the reliability question: single-run success or pass@k when one success suffices,
  pass^k when every attempt must succeed [P019].
- Read classification metrics diagnostically — low precision means over-triggering, low recall means
  missed invocation [P040].
- Watch for saturation: a 100% pass rate tracks regressions but gives no improvement signal [P068].
- Judge efficiency on a cost–accuracy Pareto frontier (execution steps), not by model size [P078].
- Expect a wide performance spread across servers; benchmark candidates [P137].

## Grading and judges

- Choose a strong judge; do not assume the largest or most expensive model is best [P009], [P036].
- Prefer deterministic code-based graders where possible; use LLM judges for open-ended quality [P067].
- Before trusting a judge, run a reliability suite with meaning-preserving perturbations and require
  format invariance [P084], [P097].
- Score argument correctness with targeted metrics (hallucinated names, all-expected-args, wrong values) [P148].
- Treat tool-use hallucination as real but low-prevalence and largely detectable [P119].
- Use one shared failure-mode vocabulary for human reviewers and diagnostic judges [P120].

## Benchmark construction and operation

- Build tasks with a two-stage proposer/validator human pipeline [P083].
- Ground each key point against the raw output; decompose tasks into explicit completion criteria [P082].
- Structure the offline pipeline as fulfilment → grading → aggregation stages [P089].
- Structure diagnostic judging around the verified evidence trace and expected vs missed claims [P190].
- Report mean coverage and pass rate at several thresholds; treat the threshold as a reporting decision [P191].
- For conversational agents, evaluate the interaction (end-state outcomes plus transcript constraints) [P192].
- Read transcripts regularly and verify tasks and graders are fair before trusting poor scores [P140], [P141].

## Principles applied

- **[P009]** Choose a strong judge model for LLM-as-a-Judge evaluation, and when any single evaluator's reliability is uncertain use multi-model majority voting; relative agent rankings are robust to evaluator bias even though absolute agreement varies by judge.
- **[P019]** Select evaluation metrics to match the reliability question: use single-run success or pass@k when one successful attempt is enough, and pass^k when every attempt must succeed consistently.
- **[P022]** Run evaluation against exclusively real, production servers rather than mocked substitutes so authentic error modes (rate limits, pagination, schema-version mismatches, transient errors) are exercised.
- **[P036]** Do not assume any single judge is uniformly reliable, or that the largest or most expensive model is the best judge; benchmark cost against reliability, since a smaller, cheaper open model can match or beat premium frontier judges at a fraction of the inference cost.
- **[P040]** Read the classification metrics diagnostically: low precision for a tool means it is being over-triggered (called when not expected), and low recall typically means it is under-triggered (missed, or confused with another tool); when two semantically similar tools are confused, expect the over-called tool's precision and the under-called tool's recall to both drop.
- **[P067]** Choose grader types by trade-off: prefer deterministic code-based graders where possible (fast, cheap, reproducible, but brittle to valid variation), use model-based graders where flexibility or nuance is needed (scalable but non-deterministic and needing calibration), and use human graders judiciously for validation (gold standard but expensive and slow).
- **[P068]** Watch for saturation: an eval at 100% pass rate tracks regressions but gives no signal for improvement, and near saturation large capability gains show up as small score increases (e.g. SWE-Bench Verified moved from ~30% to >80% within a year), so retire or refresh saturated evals for capability measurement.
- **[P078]** Judge efficiency by execution steps on a cost-accuracy Pareto frontier rather than by model size: richer descriptions push most tasks to more steps, and a smaller model can dominate a larger one that spends more steps for equal or lower accuracy.
- **[P082]** Make evaluation robust to tool-use hallucination by decomposing the task into explicit completion criteria and grounding each key point against the raw tool outputs, rather than trusting the agent's self-reported completion or brittle rule-based/answer-based checks that do not scale in dynamic environments.
- **[P083]** Construct benchmark tasks with a two-stage human pipeline of separate proposers and validators, allowing LLM-assisted ideation only when each candidate task is human-vetted for authenticity, and having verifiers consolidate duplicates and check feasibility and execution quality.
- **[P084]** Before trusting or deploying an LLM judge, run a reliability validation suite that stress-tests it with targeted perturbations rather than relying on a single point estimate of agreement with human raters on a small validation set.
- **[P089]** Structure the offline evaluation pipeline as three stages — fulfillment (run each benchmark across multiple models with the full tool list supplied, recording invoked tools and arguments), evaluation (compute metrics and scores from the raw outputs), and summarization (aggregate dataset-level statistics into a final report).
- **[P097]** Test a judge's consistency with meaning-preserving perturbations — formatting-only changes, semantic paraphrase, and verbosity variants — and require its score to stay constant when the underlying quality is unchanged.
- **[P119]** Treat tool-use hallucination as real but low-prevalence and largely detectable (about 9% of invocations, ~1.6% evaluation inconsistency, detection stable across judges), while still guarding the known weak spot: evaluators overlook critical details in excessively long, complex trajectories.
- **[P120]** Use one shared failure-mode vocabulary for human reviewers and automated diagnostic judges, assigning the primary root-cause mode plus contributing modes with explicit confidence and disambiguation rules.
- **[P137]** Evaluate MCP tool-use agents on large-scale, multi-server, dynamic toolsets that force real tool retrieval and multi-tool composition; do not rely on single-server setups that inject a fixed tool list directly into the model context.
- **[P140]** Read transcripts and grades from many trials regularly and invest in transcript-viewing tooling, because you cannot know whether graders work without doing so; a failed-task transcript reveals whether the agent made a genuine mistake or the grader rejected a valid solution.
- **[P141]** Before trusting poor eval scores, verify that the tasks and graders are fair, unambiguous, and correctly configured so failures reflect agent behavior rather than broken evaluation.
- **[P147]** Recognize that single-tool-call evaluation does not cover real sequential multi-tool flows, where later calls consume earlier outputs; to evaluate such flows, actually execute the tool calls or faithfully mock their responses instead of only fetching the tool list, and score selection as multi-label (not multi-class) classification when one input can trigger several tools.
- **[P148]** Score argument correctness with four targeted metrics — argument hallucination (arg names not defined for the tool), all-expected-arguments-provided, all-required-arguments-provided, and exact value match — and compute them only over tool calls that were correctly selected.
- **[P190]** Structure diagnostic judging around the verified evidence trace, expected claims, missed claims, and actual behavior so failures are localized without penalizing alternative valid plans.
- **[P191]** Treat the coverage threshold as a reporting decision (the rubric returns a real-valued coverage score), report mean coverage and pass rate at several thresholds, and expect model rankings to be largely preserved across thresholds.
- **[P192]** For conversational agents, evaluate the interaction itself: combine verifiable end-state outcomes, transcript constraints (e.g. finished under N turns), and LLM rubrics for task completion and interaction quality, often using a second LLM to simulate the user across multi-turn dialogue.

Sources are distillation-only: this reference paraphrases and restructures; no verbatim quotation.

