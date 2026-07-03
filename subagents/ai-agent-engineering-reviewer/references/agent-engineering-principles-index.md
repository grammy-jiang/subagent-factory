---
name: agent-engineering-principles-index
kind: reference
status: ready
provenance:
  principles: [P001, P008, P029, P040, P051, P019, P014, P009]
---

# Agent Engineering Principles Index

This is a compact index of all 60 promoted principles (P001–P060) behind this advisor, one line
each, grouped under the eight agent-engineering themes the accompanying skills cover. Each entry
paraphrases the principle's `statement`; consult `principles/principles.yaml` for the full text,
confidence level, and derived claims.

## Memory & Reflection

- **P001** — Score candidate memories by recency, relevance, and importance, tune the weights to the task, and keep the top-scoring subset that fits the context window.
- **P002** — Budget for the token cost and latency of many memory-driven agents, and manage it with caching, just-in-time planning, batching, and parallelism.
- **P012** — Periodically synthesize raw observations into higher-level reflections once accumulated importance crosses a threshold, and have each insight cite its supporting memories.
- **P018** — Store every agent experience as a natural-language memory object with a description and timestamps in a persistent, comprehensive memory stream.
- **P031** — Plan over a long horizon so behavior stays coherent: build a broad top-down agenda, then recursively decompose the near future into timed actions.
- **P048** — Do not stuff the whole memory stream into the prompt or just summarize it; retrieve only the compact subset relevant to the current situation.
- **P049** — Expect group-level social behavior (diffusion, relationships, coordination) to emerge from individually seeded agents that remember and reference prior interactions.
- **P058** — When believability is judged by ranking, convert comparisons to interval ratings, test significance with correction for multiple comparisons, and include a human baseline.

## Reasoning & Acting Loops

- **P003** — For shopping tasks, reason over the user's constraints, reject mismatched candidates, verify page-level options, and buy only once every critical attribute matches.
- **P005** — For household-object tasks, plan acquisition, required transformation, and placement, using likely locations and subgoal-state updates to drive each next action.
- **P007** — Choose a tool by the task's failure mode: direct question-answering, calculator, calendar, translation, or retrieval, matched to what the task actually needs.
- **P008** — Build reasoning-and-acting agents as interleaved trajectories: language thoughts update the working context, and environment actions gather observations for later reasoning.
- **P010** — Make each thought operational: decomposing goals, extracting salient observations, tracking progress, applying commonsense, reformulating searches, or handling exceptions.
- **P011** — Ground knowledge-intensive answers with external retrieval or environment actions, letting each observation guide the next information target before answering.
- **P016** — For multi-hop questions, decompose into retrieval targets, reformulate incomplete searches, compare retrieved facts explicitly, and finish only once evidence is sufficient.
- **P017** — For fact verification, search the claim's subject, compare evidence to its predicates and qualifiers, refute direct conflicts, and flag insufficient evidence.
- **P026** — Author few-shot demonstrations as natural, concise reasoning-action trajectories, prioritizing example quality and model capability over adding more examples.
- **P028** — Treat repeated thoughts, repeated ineffective actions, or uninformative observations as failure signals, and replan from the last useful state.
- **P032** — When prompt-only reasoning-and-acting is insufficient, fine-tune on high-quality successful trajectories so the model learns to gather and use information.
- **P041** — Match thought frequency to task shape: dense thought-action-observation cycles for reasoning bottlenecks, sparse thoughts at decision points for long action horizons.
- **P042** — Keep decision-task thoughts capable of goal decomposition and subgoal reasoning, not reduced to dense external-feedback reminders.
- **P057** — Expose reasoning, observations, and actions separately so a reviewer can inspect, diagnose, and, where supported, edit intermediate thoughts.

## Tool Use & Augmentation

- **P004** — Diagnose agent behavior against the ten canonical tool-use failure modes, from acting on incomplete information to over-trusting tool output.
- **P029** — Add external tools to offset a model weakness only when the tool is text-invocable and its result actually addresses that weakness.
- **P030** — Evaluate tool-use gains against same-backbone, continued-training, and disabled-tool baselines so any improvement is attributable to the tool use itself.
- **P035** — Extend the action space with external tools to offset missing knowledge and hallucination, training precise call arguments and falling back on the model otherwise.
- **P043** — Fine-tune on ordinary text augmented with only the selected helpful API calls and results interleaved into the original corpus.
- **P044** — When useful tool-call opportunities are sparse, combine targeted corpus prefilters with adjusted sampling thresholds before scaling up annotation.
- **P045** — For translation-call data, target useful non-English spans, filter out non-linguistic spans, and drop examples that depend on text after the call.
- **P046** — For temporal evaluation, separate dynamic factual knowledge from calendar arithmetic and attribute gains by checking which tools were actually called.
- **P047** — Prefer selective information requests over always-on retrieval or metadata augmentation, so the model learns when extra information is actually useful.

## Retrieval-Augmented Generation

- **P040** — Build a baseline retrieval-augmented system as a pretrained sequence-to-sequence generator connected to a neural retriever over a dense external text index.
- **P055** — Plan retrieval-augmented training and serving around index-search and memory footprint as a concern separate from model training itself.
- **P056** — Normalize question-answering supervision into supported generation targets: use valid annotations, filter unsupported variants, and resolve regex-form labels before training.

## Agent Safety Evaluation

- **P006** — Prioritize the empirically hardest risks and failure modes first: unsafe-information spread, fabricated parameters, dangerous tools, unvalidated options, and ignored constraints.
- **P015** — Build agent-safety datasets by refining existing data and by controlled model-driven augmentation using fresh environment names and targeted risk categories.
- **P022** — Scope agent-safety evaluation for comprehensive coverage: diverse interaction environments, the eight risk categories, and explicit failure-mode annotation.
- **P023** — Do not rely on a general-purpose LLM as the safety scorer; finetune a small local judgment model on human-labeled data instead.
- **P024** — Measure safety and helpfulness as separate axes, and judge safety as more than refusal across both fulfillable and unfulfillable tasks.
- **P025** — Do not treat defense prompts as a sufficient safety fix: they help only modestly, plateau below target, and add context cost.
- **P038** — Represent each safety test case with explicit fields and implement environments as a dual schema-plus-code layer, each labeled with its failure modes.
- **P039** — Author realistic test cases with implicit rather than explicit malicious intent, concrete parameters, sufficient information to act, and consistent formatting.
- **P051** — Evaluate an agent's behavioral safety from tool use and environment interaction as a first-class dimension, distinct from and weaker than content safety.
- **P052** — Recognize pervasive safety weakness across current agents; stronger or proprietary agents tend to be safer, but capability alone does not ensure safety.
- **P053** — Attribute safety failures to two defects: lack of robustness and lack of risk awareness; address both, not tool precision alone.
- **P054** — Control data quality with layered review: manual passes, automated consistency checks, and independent cross-validation of both test cases and labels.

## Agent Evaluation Methods

- **P013** — Evaluate believability by interviewing the agent across its expected faculties, and confirm each architecture component matters by ablating it in turn.
- **P019** — Match the metric method to the response type: code-based checks for objective outputs, human review for subjective or safety-critical judgments, model-based judges for scalable scoring.
- **P020** — Assess user-perceived behavior across task completion, output quality, latency, and cost, scoring quality separately since success can mask a poor experience.
- **P036** — Combine subjective methods (human or comparative judgment) with objective quantitative methods, and consider a model-based evaluator to reduce subjective-evaluation cost.
- **P037** — Complement cheap offline evaluation with online, dynamic evaluation, and keep evaluation continuous through development and deployment rather than a one-time check.
- **P059** — Do not let generative agents substitute for real human input in studies; use them to complement humans and follow established human-AI design practice.

## Model Cards & Transparency

- **P014** — Accompany every released model with a short model card documenting its characteristics, intended use, and evaluation procedures for stakeholders.
- **P021** — Report model performance disaggregated by individual demographic or cultural groups and intersectionally across groups, not by aggregate metrics alone.
- **P050** — Document evaluation datasets with their selection motivation and preprocessing, prefer public datasets, and note that synthetic data is narrow and non-comprehensive.

## Agent Design Strategy

- **P009** — For believable open-world behavior, prefer a language-model core augmented with memory, reflection, and planning over rule systems, reinforcement learning, or symbolic architectures.
- **P027** — Acquire capability without fine-tuning via prompt and mechanism engineering (critic loops, multi-agent debate, skill libraries, self-driven evolution) within context-window limits.
- **P033** — Select a profile-generation strategy by its trade-offs (handcrafting, model-generation, dataset alignment), combining strategies when that adds value.
- **P034** — Drive plan revision with combined environment, human, and model feedback, favoring detailed failure reasons and verbal feedback over bare success signals.
- **P060** — Choose a fine-tuning data source by trade-off: human-annotated data is versatile but costly, model-generated data is cheap but lower quality, real-world data suits domain-specific tasks.

## Provenance

Indexes all 60 principles in `principles/principles.yaml`. The frontmatter provenance lists one
representative principle per theme; the full principle-to-claim-to-evidence mapping is in
`provenance-ledger.md`.
