---
name: agent-evaluation-methods
kind: skill
status: ready
provenance:
  principles: [P013, P019, P020, P036, P037, P059]
---

# Agent Evaluation Methods

## Purpose

Guide how to plan or review an evaluation of an LLM agent's capability and its user-perceived
quality: match the scoring method to the response type, cover all four user-facing facets rather
than one aggregate number, combine subjective and objective methods, run the evaluation across
the whole development-to-deployment lifecycle instead of a single static pass, and — when
believability or human-participant substitution is at stake — apply the interview/ablation method
and keep simulated agents in a strictly complementary role to real people.

## When this applies

- Selecting how to score agent outputs, so the computation method fits the response type (P019).
- Evaluating end-to-end, user-perceived agent performance across completion, quality, latency,
  and cost (P020).
- Assessing agent capability generally, especially a quality that is hard to quantify, such as
  intelligence or user-friendliness (P036).
- Planning an agent's evaluation strategy or lifecycle, from pre-release testing through
  post-deployment monitoring (P037).
- Validating whether an agent's behaviour is believable, and which of its components actually
  drive that believability (P013).
- Considering generative or simulated agents as stand-ins for human participants or stakeholders
  in a study or design process (P059).

## Procedure

1. **Name the facets in scope (P020).** Separate task completion, output quality, latency, and
   cost as four distinct user-perceived facets instead of folding them into one score; a review
   that only asks "did it finish the task" is missing three of the four.
2. **Match the scoring method to each response type (P019).** For well-defined, objective outputs,
   use code-based checks — rules, test cases, assertions — because they are deterministic and
   reproducible, while noting they are inflexible for open-ended output. For subjective or
   safety-critical judgments, use human-in-the-loop scoring as the gold standard, while budgeting
   for its cost and weak scalability. For scalable scoring of nuanced, subjective tasks, use an
   LLM-as-a-Judge or Agent-as-a-Judge approach.
3. **Treat completion-rate metrics as coarse (P020).** When task completion is measured with a
   success-rate or pass@k-style metric, read it as a coarse pass/fail signal that hides failure
   detail, especially once success rates are low — do not let it stand alone as the verdict.
4. **Score output quality as its own facet (P020).** Separately assess accuracy, relevance,
   clarity, coherence, and adherence to the task specification, because an agent can complete the
   task and still leave a poor experience; the gap is sharpest for multi-turn conversational
   agents, where the user's goal is only reached across several turns.
5. **Combine subjective and objective evaluation (P036).** Use a subjective method — human
   annotation or a Turing-style test — when no evaluation dataset exists or the quality is hard to
   specify quantitatively (for example, judging intelligence or user-friendliness), accepting its
   cost and bias; use an objective, quantitative method where metrics can be computed, compared,
   and tracked over time; combine both for a comprehensive picture, and consider an LLM-based
   evaluator to reduce the cost of the subjective side.
6. **Balance offline and online evaluation (P037).** Start from offline/static evaluation against
   a fixed dataset as a cheap baseline, but recognize that it lacks nuance and propagates its own
   errors; complement it with online/dynamic evaluation — simulated interactions, real user
   sessions, or live monitoring — to surface what the static tests miss.
7. **Make evaluation continuous, not a one-time gate (P037).** Adopt an evaluation-driven approach
   that runs offline during development and online after deployment, so regressions and new use
   cases are caught on an ongoing basis; this matters most for an agent that keeps learning or
   evolving after release.
8. **When believability itself is under test, interview and ablate (P013).** Probe the agent in
   natural language across the faculties it is meant to exhibit — self-knowledge, memory
   retrieval, planning, reacting to the unexpected, and reflecting — and use the believability of
   the responses as the outcome measure. Show that each of the three architectural components
   genuinely contributes by removing memory, reflection, and planning one at a time and confirming
   that believability drops as each one goes; do not assume a component helps just because it was
   included.
9. **Keep generative or simulated agents complementary to real people (P059).** When simulated or
   generative agents are proposed as a stand-in for human participants, treat that as a
   complement, never a replacement, for real human input in a study or a design decision: they
   are best suited to early-stage idea prototyping or to probing a theory that would be
   impractical or unsafe to test on real participants. Apply established human-AI design practice
   so any agent-generated error is traced through to its effect on the end user.
10. **Report the plan or the finding.** State which facets and response types are in scope, which
    method covers each, the offline/online balance and lifecycle cadence, and — where believability
    or human-substitution is at stake — the interview/ablation design or the participant-
    substitution risk; tie every element back to its governing principle and its trade-off.

## Anti-patterns

- Reporting a single aggregate success rate as the whole verdict on agent quality, instead of
  separating task completion from output quality, latency, and cost (P020).
- Using one general-purpose judge — human or LLM — for every response type instead of matching the
  scoring method to whether the output is well-defined and objective or open-ended and
  subjective (P019).
- Running only offline/static evaluation and never complementing it with online/dynamic
  evaluation, so nothing catches what the static tests miss (P037).
- Treating evaluation as a single milestone rather than a continuous activity across development
  and deployment, especially for an agent that keeps learning or evolving (P037).
- Declaring an agent "believable" without ablating its architecture, so no component is actually
  shown to matter (P013).
- Relying on only objective or only subjective methods when the quality in question — such as
  intelligence or user-friendliness — is hard to specify quantitatively and needs both (P036).
- Letting a generative or simulated agent substitute for real human participants in a study or a
  design decision, rather than using it to complement them (P059).

## Principles covered

- **P013** — Evaluate believability with a natural-language faculties interview, and confirm each
  architectural component matters by ablating memory, reflection, and planning.
- **P019** — Match the metric-computation method — code-based, human-in-the-loop, or
  LLM/Agent-as-a-Judge — to the response type.
- **P020** — Assess task completion, output quality, latency, and cost as separate user-perceived
  facets, and treat completion-rate metrics as coarse.
- **P036** — Combine subjective (human annotation, Turing-style test) and objective quantitative
  evaluation for a comprehensive assessment.
- **P037** — Complement offline/static evaluation with online/dynamic evaluation, under a
  continuous, evaluation-driven lifecycle.
- **P059** — Use generative or simulated agents to complement, never replace, real human input,
  and trace how agent error reaches the user.

## Inputs

- The response types the agent produces (well-defined/objective versus open-ended/subjective)
  that need to be scored.
- Which of the four facets — task completion, output quality, latency, cost — matter for the case
  at hand.
- The point in the agent's lifecycle the evaluation targets (pre-release, offline test,
  post-deployment monitoring), and whether the agent keeps learning or evolving after release.
- Whether believability of simulated human-like behaviour is itself being tested, and whether
  generative or simulated agents are being proposed as stand-ins for real participants.

## Output

An evaluation plan or review finding that names the facet(s) and response type(s) in scope, the
scoring method matched to each, the offline/online balance and lifecycle cadence, and — when
relevant — the believability interview/ablation design or the human-participant-substitution
risk, with every element tied to its governing principle and its stated trade-off.

## References

- `references/agent-engineering-principles-index.md` — the package's principle index, for the
  full statement and evidence trail behind each principle cited above.

## Provenance

Distilled, with no verbatim quotation, from three of the package's `distillation-only` sources: a
survey on evaluating and benchmarking LLM agents (metric-computation methods, the four
user-perceived facets, and the offline/online evaluation lifecycle — P019, P020, P037); a survey
on LLM-based autonomous agents (subjective versus objective evaluation — P036); and a study of
generative agents (the believability interview and ablation method, and the guidance that
generative agents should complement rather than replace human participants — P013, P059).
Grounded in principles P013, P019, P020, P036, P037, P059.
