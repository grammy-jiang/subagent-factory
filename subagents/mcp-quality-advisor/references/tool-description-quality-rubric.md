---
name: tool-description-quality-rubric
kind: reference
status: ready
provenance:
  principles:
  - P006
  - P033
  - P037
  - P043
  - P044
  - P045
  - P046
  - P047
  - P055
  - P057
  - P058
  - P070
  - P090
  - P126
  - P138
  - P144
  - P189
  - P196
  - P198
  - P199
  - P200
  authored_from_digest: 3cbd4dd372d202d434f1b8dc01006d89911f1466cb4440ec34f68579c7c894cb
---

# Reference: MCP tool-description quality rubric

A review rubric for the model-facing description surface of an MCP tool. Treat descriptions as
first-class engineering artifacts and score components on a graded (5-point) scale, with 3 as the
minimum viable threshold [P045], [P090].

## Core components (always score Purpose)

- **Purpose** — the function, behaviour, and return data; always present and retained [P046], [P196].
- **Usage guidance** — when and when not to use, and disambiguation from similar tools [P043].
- **Information completeness** — everything needed to build a valid call and read the result [P070].
- **Parameter clarity** — meanings and constraints; the input schema already supplies names/types, so
  prune Parameter Explanation before other components under a tight budget [P198].
- **Examples** — lowest-priority and safest to omit under constraints [P199].

## Prevalent smells (fix highest-prevalence first)

- Unstated Limitations (~90%), Missing Usage Guidelines (~89%), Opaque Parameters [P044].
- Inaccuracy — state only implemented behaviour and concrete constraints [P006].
- Verbosity / low signal-to-noise — remove redundancy, hedge words, jargon, and clutter [P058], [P126].

## Grounding and measurement

- Ground Examples and Limitations in observed executions and source code, not the description alone [P055], [P057].
- Trim Examples first, then Parameter Explanation, when reducing size [P037].
- Treat a rubric smell as a risk signal, not a deterministic predictor of failure [P144].
- Score automatically with a well-defined analytic rubric via a multi-model LLM jury [P189].
- Diagnose selection failures by mode: an under-specific description misses invocation; an over-broad one
  causes wrong selection [P200], [P138].
- Give each tool a unique, semantically meaningful name distinct within its namespace [P047].

## Principles applied

- **[P006]** Keep tool descriptions accurate and precise: state only implemented behavior, concrete constraints, parameter meanings, and boundaries, while removing ambiguous, contradictory, or self-referential wording.
- **[P033]** Assume tool-description quality is poor by default and always review it: in a large empirical study 97.1% of descriptions carried at least one smell and 56% failed to state purpose clearly, where a smell is a recurring component-specific pattern that degrades clarity, correctness, or maintainability without being an outright fault.
- **[P037]** Drop the Examples component first when trimming a description: removing it did not significantly degrade performance and even slightly improved cross-domain consistency, consistent with Anthropic's deprioritization though contrary to generic few-shot expectations; keep examples only where a tool is unfamiliar or complex enough to benefit.
- **[P043]** Write tool descriptions with all core quality components present and viable: purpose, usage guidance, limitations, parameter details, and self-sufficient prose, with examples only supplementing the description.
- **[P044]** Prioritize the most prevalent smells when reviewing descriptions: Unstated Limitations (~90%), Missing Usage Guidelines (~89%), and Opaque Parameters (~84%) dominate, only ~2.9% of descriptions are fully smell-free, and completeness drops sharply as more components are required, so most descriptions lack boundary conditions, when/how-to-use guidance, and parameter insight.
- **[P045]** Treat tool descriptions as first-class engineering artifacts: run rubric-based smell detection in review or CI as a blocking release criterion, fix the highest-leverage components first, add examples or exhaustive parameter detail only where they justify their token cost, and use manual refinement for small servers but reviewed semi-automated augmentation for large ones, always resolving ambiguity without inflating the token footprint past its efficiency payoff.
- **[P046]** Select the minimal effective component set for each domain-model pair, always retaining Purpose: there is no universal 'golden' combination, but a pruned combination that keeps the core purpose and the most relevant constraints solves largely the same tasks as full augmentation (strong statistical agreement) while cutting tokens and latency, provided the pruning is tailored to the domain.
- **[P047]** For Functionality, make the tool distinct within a shared namespace: give it a unique, semantically meaningful name (not a generic utility name such as read_file or get_data), a clear functional description, and explicit trigger conditions stating when this tool should be prioritized over similar tools.
- **[P055]** Do not write Examples or the full Limitations from the description alone; ground them in observed tool executions by generating at least one success task and one error task per tool plus edge cases (prioritizing harder cases first), because an FM cannot reliably infer them without traces and augmentation must preserve the tool's original meaning and intent.
- **[P057]** Use source-code grounding as a reliability safeguard for tool-description faithfulness, especially for behavior- and input-tied components, while not assuming it will always improve task success.
- **[P058]** For Conciseness, maximize signal-to-noise: remove redundant or repeated content, irrelevant clutter, needless technical jargon, and useless qualifiers, because verbosity inflates token cost and dilutes model attention — while treating conciseness as the lowest-impact of the four dimensions.
- **[P070]** For Information Completeness, document everything the agent needs to build a valid call and interpret the result without guessing: every parameter and its type, the return values, side effects, and error handling; omitting return-value descriptions forces zero-shot output handling and invites hallucination.
- **[P090]** Score each component on a graded (5-point) scale rather than a yes/no check, treating 3 as the minimum viable threshold, 4-5 as increasing precision and clarity, and a mean below 3 as a detected smell, because a component can be present yet semantically ambiguous or sub-optimal.
- **[P126]** Also avoid vague hedge words (for example maybe or probably), keep terminology consistent, and keep wording understandable to the model; these general documentation qualities matter, but for short MCP descriptions they are secondary to the four core dimensions and were not among the mapped MCP smells.
- **[P138]** Diagnose wrong-tool selection, invalid or over-broad arguments, and unnecessary steps as a specification problem in the tool description, not a model bug, since defective, underspecified, or misleading descriptions directly cause these failures.
- **[P144]** Interpret a rubric smell as a potential risk signal, not a deterministic predictor of failure: whether a missing component actually hurts depends on tool complexity, task difficulty, available context budget, and the model's prior exposure to the tool, API, or domain.
- **[P189]** When automatically scoring tool descriptions, apply a well-defined analytic rubric (more consistent than open-ended prompts) via a multi-model LLM jury drawn from disparate model families to mitigate single-model bias; such rubric scoring aligns with human judgment at substantial agreement.
- **[P196]** Ensure every tool description clearly states its purpose (the function, behavior, and return data), guides the FM on when and how to use the tool, and includes relevant caveats; a bare purpose statement without behavioral or output detail is only minimally viable.
- **[P198]** When the context budget is tight, prune Parameter Explanation before other components: the MCP input schema already supplies parameter names and types at runtime, the component often duplicates that information, and including every component can otherwise inflate context and reduce efficiency.
- **[P199]** Treat Examples as the lowest-priority component and the safest to omit under constraints: their value is contested, they scored only moderate inter-rater reliability, and they can be too large to fit the context window.
- **[P200]** Diagnose tool-selection failures by mode: an under-specific or vague description causes missed invocation (the correct tool is not selected), whereas an over-general or ambiguous description causes erroneous selection (a wrong tool is chosen); remediate by increasing specificity and disambiguating.

Sources are distillation-only: this reference paraphrases and restructures; no verbatim quotation.

