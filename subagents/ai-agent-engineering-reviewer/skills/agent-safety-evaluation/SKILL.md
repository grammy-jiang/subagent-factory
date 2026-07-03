---
name: agent-safety-evaluation
kind: skill
status: ready
provenance:
  principles: [P006, P015, P022, P023, P024, P025, P038, P039, P051, P052, P053, P054]
---

# Agent Safety Evaluation

## Purpose

Guide the review of, and advice on, how an LLM agent's *behavioural* safety — unsafe actions taken through tool use and environment interaction — is evaluated and improved, as a first-class axis that is distinct from, and typically weaker than, the safety of the text the agent produces (P051). Scope evaluation for real coverage: diverse interaction environments, the full eight-category risk taxonomy, and explicit failure-mode annotation on every case (P022), then prioritise effort on the risk category and failure modes shown to be empirically hardest rather than spreading it evenly (P006). Build and curate the underlying test data with refinement of existing material plus controlled augmentation (P015), explicit structured test cases paired with matching dual-layer environments (P038), scenarios that are realistic and actually callable by the agent (P039), and layered manual-plus-automated review (P054). Score behaviour with a small, task-specific finetuned judge rather than a general-purpose model alone (P023), and measure safety and helpfulness as separate axes rather than treating refusal as safety (P024). Diagnose failures against the two root defects — lack of robustness and lack of risk awareness (P053) — calibrate expectations because pervasive weakness shows up even in capable and proprietary agents (P052), and reject a defense prompt alone as a sufficient fix (P025).

## When this applies

- The caller submits an existing agent-safety evaluation plan, benchmark, or test suite for review of its scope, data quality, or scorer.
- The caller, or a vendor, claims an agent "is safe" on the basis of refusal behaviour, a defense prompt, or a capability/benchmark score alone.
- The caller is building or expanding a safety test corpus and its simulated environments.
- The caller has safety-evaluation results and wants help prioritising what to fix or diagnosing why the agent is unsafe.
- The caller is deciding how to improve a deployed agent's safety after a disappointing score.

## Procedure

1. **Separate behavioural safety from content safety (P051).** Confirm the review or plan treats unsafe *actions* taken through tools and the environment as its own evaluated dimension, not a by-product of content-safety testing. Set the expectation explicitly up front: behavioural safety evaluations typically score the same agents meaningfully lower than content-only safety tests do, so a strong content-safety result is not evidence of behavioural safety.

2. **Check scope for coverage, not just volume (P022).** Confirm the plan or benchmark spans: (a) diverse interaction environments, including realistic domains that have no existing public interface to reuse, since these are commonly under-represented and are where novel risk shows up; (b) the full eight-category risk taxonomy, applying a finer breakdown to behaviour-level risks that depend on tool or environment interaction and a coarser breakdown to content-level risks, noting that a harmful/vulnerable-code risk can land on either side depending on whether a tool was used to act on it; and (c) explicit failure-mode annotation on every test case, drawn from a canonical set of ten failure modes, not just a pass/fail outcome. Flag a plan that covers only content-style prompts, or records only an outcome label with no failure-mode tag, as under-scoped.

3. **Prioritise by measured difficulty, not intuition (P006).** Within the risk taxonomy, treat the category covering an agent spreading unsafe or misleading information through its tools as a priority — it is consistently one of the hardest for agents to handle safely. Within failure modes, prioritise: fabricating parameters when required information is missing and then proceeding to use a dangerous or flagged tool anyway; failing to validate the single option a tool returns; ignoring a tool the agent should have called; and bypassing explicit or implicit constraints. Content-style generation risk and cases offering multiple explicit choices are comparatively well handled already, so do not spend scarce red-teaming or mitigation effort there first.

4. **Structure test cases for analysability (P038).** Each case should carry explicit fields: the risk(s) it targets, the initiating instruction or dialogue, the environment(s) involved with their tools and initialisation parameters, and the failure mode(s) it anticipates — one primary risk category is enough, but more than one failure-mode label per case is expected and useful. Where environments are simulated, look for a dual-layer implementation: a machine-readable tool definition plus the executable logic behind it, sharing common scaffolding, so environments stay configurable and consistent instead of ad hoc per case.

5. **Check test-case realism (P039).** A well-formed case keeps any malicious intent implicit in the scenario rather than stated outright, gives the environment concrete and realistic initialisation content, and supplies the agent enough information in the instruction that it can actually call the tools the case expects. Tool naming and schema formatting should be consistent across cases. Tool-free, content-only risk needs a simplified path with no simulated environment attached.

6. **If building or expanding the corpus, combine refinement with controlled augmentation (P015).** When reusing existing safety data: clarify or discard cases whose failure mode is unclear, remove near-duplicates, and standardise how environments are defined across sources. When generating new cases: force each generation to include a fresh, distinct environment fed back into the prompt so it is not reused, which keeps topic diversity up; supply in-context examples so the generator produces the expected sequence of risky actions alongside the case, which raises usable-case quality; and specify the target risk category per generation so the resulting distribution can be controlled rather than left to chance.

7. **Control data quality with layered review, not a single pass (P054).** Require at least two rounds of manual review per test case — an authoring-time check and a separate post-hoc check — plus an automated consistency check that a case's declared tool definition actually matches its executable implementation, with any mismatch fixed by hand. Add a cross-validation step where a second, independent reviewer checks both the test case itself and its assigned safety label.

8. **Choose or build the scorer deliberately (P023).** Do not accept a general-purpose model used directly as the safety judge as sufficient: in the source study, direct judgment from a capable general-purpose model reached only about 75.5% accuracy at the safe/unsafe call, too low to trust for a release decision. Prefer a small model finetuned specifically for the task on human-labelled interaction records, trained to emit both a safe/unsafe label and a structured analysis explaining it; a fitted judge of this kind reached about 91.5% accuracy in the same study, roughly fifteen points higher. Where training data for the analysis target is scarce, a capable general-purpose model can generate the analysis text once given the ground-truth label to explain, and the resulting training mix should stay close to balanced between safe and unsafe examples.

9. **Measure safety and helpfulness on separate axes, and treat safety as more than refusal (P024).** Label each test case as fulfillable — the request can be completed safely — or unfulfillable, and expect safety scores to run lower on unfulfillable cases: agents are more prone to unsafe behaviour precisely when a request cannot be safely completed, which points to a risk-awareness gap rather than a capability gap. On fulfillable cases, an agent with genuinely strong safety should also stay helpful; safety achieved mainly through refusal shows up as a safety score unmatched by helpfulness on tasks that were, in fact, safely completable. On unfulfillable cases expect the reverse: a genuinely risk-aware agent deliberately gives less help, and that drop in helpfulness is itself a positive signal, not a defect.

10. **Diagnose failures against the two root defects, not surface symptoms (P053).** Trace unsafe behaviour back to lack of robustness — tool calls that are imprecise or unreliable across scenarios, where even a small parameter error can have an outsized real-world consequence — or lack of risk awareness — tool calls that are technically correct but ignore the implicit risk of the action itself — or both. Improving robustness alone is not enough: an agent can call the right tool with the right parameters and still act unsafely because it never registered the risk, so risk awareness has to be diagnosed and addressed as its own defect.

11. **Calibrate expectations to capability realistically (P052).** Do not accept "it is a strong or well-regarded agent" as evidence of adequate safety on its own. In the source study even the best-scoring agents stayed below a 60% total safety score, and while stronger or proprietary agents tended to score somewhat better than weaker or open-weight ones, none of them cleared an acceptable bar. Treat capability as a contributor to safety, through better robustness and risk awareness, but never as sufficient by itself.

12. **Judge mitigation sufficiency, and push past defense prompts alone (P025).** If the proposed or existing mitigation is a system-prompt-level defense — enumerating failure modes and instructing the agent to avoid them, however detailed the description — treat it as a partial measure at best: it helps stronger agents only modestly, does little for weaker ones, plateaus well short of an acceptable safety level even in its most detailed form, and adds ongoing context cost. Recommend stronger interventions, such as finetuning a judge or the agent itself, and name defense-prompt-only mitigation as insufficient whenever it is presented as the whole fix.

13. **Compile and hand off.** Summarise findings against the principles above — coverage gaps, prioritisation misses, data-quality gaps, scorer risk, safety/helpfulness conflation, root-cause diagnosis, capability-as-proxy reasoning, and mitigation sufficiency — each with its trade-off, and hand the fix itself (data collection, scorer training, mitigation engineering, the release decision) back to the owning team.

## Anti-patterns

- **Refusal-only "safe" claims.** Reporting an agent as safe because it refuses unsafe requests, without checking whether it stays helpful on safely-completable requests and appropriately less helpful on unfulfillable ones (P024).
- **Defense-prompt-only mitigation.** Treating a system-prompt enumeration of failure modes as the safety fix, rather than as a modest, capability-dependent, context-costly partial measure that still leaves scores well short of acceptable (P025).
- **A general-purpose model as the sole scorer.** Trusting a general-purpose model's direct safe/unsafe judgment without a finetuned, task-specific judge behind it, especially at release-gating accuracy levels (P023).
- **Capability treated as sufficient for safety.** Assuming a strong or well-regarded agent is safe because it is capable, instead of checking its measured behavioural-safety score against an acceptable bar (P052).
- **Content-safety-only review.** Auditing only text-generation risk and calling it "agent safety", when behavioural risk from tool and environment interaction is typically the larger gap and needs its own coverage (P051, P022).
- **Even effort across risk categories and failure modes.** Spreading red-teaming or mitigation budget evenly instead of weighting it toward the category and failure modes shown to be hardest (P006).
- **Robustness fixes presented as the whole safety fix.** Improving tool-call precision and calling the safety problem solved, without separately checking and improving risk awareness (P053).
- **Poorly-formed test cases.** Scenarios that state malicious intent outright, environments left too abstract to execute, or instructions that do not give the agent enough information to call the tools the case is meant to test, so the resulting failures cannot be attributed reliably to the agent (P038, P039).
- **Unreviewed or single-pass test data.** Shipping a safety benchmark or expanded test set without at least two review passes, automated schema-consistency checks, and independent cross-validation of labels (P054).

## Principles covered

- **P006** — Prioritise red-teaming and mitigation effort on the empirically hardest risk category and failure modes, not spread it evenly.
- **P015** — Build or expand safety datasets by refining existing data and by controlled, diversity-forcing augmentation.
- **P022** — Scope safety evaluation for environment, risk-category, and failure-mode coverage, with a finer taxonomy for behaviour-level risk.
- **P023** — Do not rely on a general-purpose model as the safety scorer; finetune a small local judge on human-labelled records instead.
- **P024** — Measure safety and helpfulness as separate axes using fulfillable-versus-unfulfillable labelling; safety is more than refusal.
- **P025** — Treat defense prompts as a partial, capability-dependent measure, not a sufficient safety solution.
- **P038** — Give every test case explicit fields and implement its environment as a matching definition-plus-logic pair.
- **P039** — Author test cases that are realistic, implicit in intent, and actually callable by the agent.
- **P051** — Evaluate behavioural safety as a first-class axis, distinct from and generally weaker than content safety.
- **P052** — Expect pervasive safety weakness even in capable or proprietary agents; capability is not sufficient.
- **P053** — Attribute and target unsafe behaviour to lack of robustness and lack of risk awareness, as two distinct defects.
- **P054** — Control data quality with layered manual review, automated consistency checks, and independent cross-validation.

## Inputs

- The agent or agent design under review, or being planned, including which tools and environments it can act in.
- The current safety-evaluation plan, benchmark, or test corpus, if one exists, and how its test cases are structured and reviewed.
- The current scorer or judging approach, and any accuracy evidence for it.
- Any available results: scores by risk category and failure mode, fulfillable-versus-unfulfillable breakdowns, and the measured effect of any defense prompt already tried.

## Output

A structured safety-evaluation critique or recommendation keyed to the principles above: coverage gaps against the risk/failure-mode/environment scope, prioritisation guidance toward the empirically hardest risks, data-quality and scorer findings, a safety-versus-helpfulness reading that does not conflate refusal with safety, a robustness-versus-risk-awareness diagnosis, and a verdict on whether the proposed mitigation is sufficient — each tied to a principle, with its trade-off, and ending in a concrete next step.

## References

- `references/agent-safety-and-evaluation-evidence-notes.md` — the risk-category and failure-mode detail this procedure prioritises against.

## Provenance

Distilled from this package's agent-safety evaluation source: a benchmark study of LLM agent behavioural safety (`distillation-only` rights — paraphrase only, no verbatim quotation). Grounded in P006, P015, P022, P023, P024, P025, P038, P039, P051, P052, P053, P054.
