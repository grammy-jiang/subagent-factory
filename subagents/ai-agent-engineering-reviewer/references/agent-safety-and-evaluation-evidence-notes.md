---
name: agent-safety-and-evaluation-evidence-notes
kind: reference
status: ready
provenance:
  principles: [P006, P019, P020, P022, P023, P024, P025, P037, P051, P052, P053, P054]
---

# Agent Safety and Evaluation Evidence Notes

Measured findings backing this advisor's safety and evaluation guidance — the concrete numbers
and empirical patterns a reviewer can cite when pushing back on a safety claim or an evaluation
plan. Figures are approximate distillations of the underlying studies: read them as evidence of
direction and rough magnitude, not as exact reproducible statistics.

## Safety evidence

- (P051, P052) Behavioural safety — safe conduct during tool use and environment interaction — scored far below content safety across evaluated agents (roughly 30% versus roughly 68% on average), and no evaluated agent reached a total safety score above about 60%; treat behavioural safety as a distinct, currently weaker, still largely unsolved dimension, not something read off content-safety numbers.
- (P051) Most behavioural test cases carried no explicit jailbreak-style attack, so the gap between behavioural and content safety is not an attack-resistance artifact — it reflects a genuine weakness in safe tool use and environment interaction that deserves at least as much attention as content-level safety review.
- (P052) More capable model variants within the same family tended to score safer than weaker variants, and more hardened, commercially released agents tended to score safer than openly released ones, but the correlation only raised the ceiling — it did not close the gap to an acceptable safety level; treat high capability as necessary, not sufficient, before trusting an agent with a risky deployment.
- (P053) Failures trace back to two distinct defects: lack of robustness (imprecise or unreliable tool invocation, where even a small parameter error can carry outsized real-world impact) and lack of risk awareness (calling the right tool with correct parameters while still missing the danger the action itself poses).
- (P053) Robust, precise tool use is necessary but not sufficient for safety — an agent can invoke tools correctly and still act unsafely because it failed to recognize the risk, so risk-awareness work has to run alongside robustness work rather than substitute for it.
- (P006) The hardest risk category measured was spreading unsafe or unverified information — agents readily posted, published, or forwarded content without validating it, scoring only about 15% on average — while content-style "produce unsafe information" cases were comparatively well handled because they reduce to the already well-studied content-level jailbreak problem.
- (P006) The weakest failure modes were fabricating tool-call parameters under missing or incomplete information and knowingly invoking flagged or unverified tools; close behind were failing to call a tool the task actually required, bypassing explicit or implicit constraints, and validating a single available option when only one choice was offered — prioritize red-teaming and mitigation on these harder modes rather than spreading effort evenly across all of them.
- (P022, P054) A comprehensive safety benchmark spans diverse interaction environments — deliberately including realistic domains with no public API, since novel high-risk domains are exactly what earlier benchmarks tended to miss — risk-category coverage broad enough to separate behaviour-level risk (mediated by tool or environment use, needing a finer taxonomy) from content-level risk (arising from model output alone, needing only a coarse one), and explicit annotation of the failure mode(s) each test case is expected to trigger.
- (P054) Benchmark quality was controlled with layered review: at least two rounds of manual review on every test case, automated checks that a tool's schema and its implementing code stayed consistent, and independent cross-validation in which a second reviewer, uninvolved in the original authoring or labelling, re-checked a random sample of both test cases and safety labels — the large majority (roughly 97-98%) held up under that independent check.
- (P023) Scoring safety with a general-purpose LLM used directly reached only about 75.5% binary safe/unsafe classification accuracy on sampled interaction records — too low to trust for agent-safety evaluation on its own.
- (P023) Finetuning a small local judgment model on several thousand human-labelled interaction records, trained to output both a safe/unsafe label and a structured supporting analysis, raised scorer accuracy to about 91.5% — roughly 15 percentage points better than the general-purpose scorer used directly.
- (P023) A capable general-purpose LLM, given the ground-truth label, can generate a plausible supporting rationale for a human safety judgment with high reliability (about 94% judged reasonable) — a practical way to manufacture the analysis targets a local judge model needs, drawn from a near-balanced mix of safe and unsafe training examples.
- (P024) Labelling each test case fulfillable (safely completable) or unfulfillable, and scoring helpfulness (whether the behaviour advanced the task, independent of whether it was safe) alongside the safety score, separates genuine safety from mere refusal; helpfulness itself can be judged automatically with strong agreement (about 94%) against manual review.
- (P024) Agents were measurably less safe on unfulfillable tasks than on fulfillable ones — a general tendency to act unsafely once a task cannot be completed safely, and a sign of weak risk awareness rather than of scenario difficulty alone.
- (P024) The strongest-safety agents stayed just as helpful as weaker agents on fulfillable tasks — no helpfulness tax for being safe — but dropped sharply in helpfulness on unfulfillable tasks relative to weaker agents, evidence that they are safe because they correctly assess the situation and deliberately withhold help, not because they refuse indiscriminately.
- (P025) Enumerating known failure modes in a system prompt is not a sufficient safety fix on its own: tested both as a bare list and as an enhanced version with descriptions and examples, it produced no meaningful improvement for weaker or smaller models.
- (P025) The same defense prompts gave capable models only a modest improvement, and even the enhanced version left safety scores below an acceptable target while adding context length and cost — prompt-only mitigation plateaus below the bar and should be paired with, or replaced by, stronger methods such as finetuning.

## Evaluation evidence

- (P019, P020) Match the metric-computation method to what is being measured, and assess user-perceived agent performance across separate facets rather than one composite score: computation method should follow the response type (objective versus subjective, safety-critical versus not), and task completion should be scored apart from output quality because an agent can finish a task and still deliver a poor experience.
- (P019) Code-based checks (explicit rules, test cases, assertions) are the most deterministic and reproducible metric-computation method and suit well-defined, objective outputs such as numeric calculations, structured queries, or syntactic correctness, but they are inflexible and struggle wherever correctness is inherently subjective, such as open-ended or creative text.
- (P019) Human-in-the-loop evaluation remains the gold standard for subjective qualities and for safety-critical judgment calls, giving the highest reliability on open-ended tasks, but it is costly, slow, and does not scale to large or frequently run evaluation pipelines.
- (P019) LLM-as-a-judge scoring, and its multi-agent extension where several agents interact to refine the assessment, scales well and suits subjective, nuanced tasks such as summarization, reasoning, or conversation, trading some reliability for scale relative to direct human review.
- (P020) Task completion — success rate, goal completion, or pass@k and the stricter pass^k across repeated attempts — is a predominant, essential measure, but a coarse one: it hides failure detail, especially once success rates are already low, so pair it with finer-grained diagnostics rather than reporting it alone.
- (P020) Output quality (accuracy, relevance, clarity, coherence, and adherence to specification) needs a measurement of its own, separate from task completion — the gap between finishing the task and giving a good experience shows up most clearly in multi-turn, conversational interactions.
- (P037) Offline, static evaluation on pre-generated datasets is cheap and simple to run and maintain, but it lacks the nuance to cover the range of responses an agent can give, is more prone to propagating error forward, and is a less accurate stand-in for real system performance than it looks.
- (P037) Online, dynamic evaluation — simulation, human-in-the-loop review, or live production monitoring — typically runs after deployment and is where pain points and rich domain context that static tests miss actually surface; treat it as complementary to offline testing, not a replacement for it.
- (P037) Evaluation-Driven Development treats evaluation as continuous across the whole lifecycle — offline during development, online after deployment — rather than a single pre-release milestone; this matters most for agents that keep learning or changing behaviour after release.

## Provenance

Distilled from the agent-safety benchmark study and the agent-evaluation survey in this
package's source pack, both recorded as distillation-only in `provenance-ledger.md`; every
finding above is paraphrased, not quoted, and grounded in principles P006, P019, P020, P022,
P023, P024, P025, P037, P051, P052, P053, P054.
