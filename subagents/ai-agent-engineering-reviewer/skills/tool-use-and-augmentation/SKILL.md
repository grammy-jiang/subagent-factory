---
name: tool-use-and-augmentation
kind: skill
status: ready
provenance:
  principles: [P004, P029, P030, P035, P043, P044, P045, P046, P047]
---

# Tool Use and Augmentation

## Purpose

Review and advise on augmenting a language-model agent's action space with external tools, APIs,
databases, or other models, so every addition compensates for a genuine model weakness instead of
being bolted on by default and assumed to help: it covers the decision to extend the action space
at all, a ten-item checklist for diagnosing tool-calling failures in a trajectory or transcript,
the data-construction choices that matter when tool use is fine-tuned rather than only prompted,
and the baseline comparisons a claimed capability gain must clear before it is credited to the tool.

## When this applies

- The caller is deciding whether to add a tool, API, database, knowledge base, or external model to
  an agent and wants the addition checked against a real weakness rather than assumed useful.
- The caller submits an agent trajectory, transcript, or tool-calling design for review or
  red-teaming.
- The caller reports a capability or accuracy gain after adding tool use and wants the claim checked
  for proper attribution.
- The caller is constructing or reviewing fine-tuning data for tool use, especially when useful call
  opportunities are sparse in the source corpus, or the tool is a translation or date/calendar tool.
- The caller is weighing selective, learned information requests against an always-on retrieval or
  metadata-augmentation design.

## Procedure

1. **Name the weakness, then check invocability (P029, P035).** Before endorsing any tool addition,
   require the caller to name the specific model weakness it targets — missing or outdated facts,
   arithmetic, low-resource language handling, temporal awareness, missing domain-specific expert
   knowledge, or hallucination the model cannot self-correct. Confirm the candidate tool's inputs and
   outputs can be represented and returned as plain text. If either check fails — no named weakness,
   or the tool cannot round-trip through text — decline the addition and point back to the model's
   own planning, conversation, and common-sense capability as the fallback.

2. **Screen for always-on augmentation (P047).** Reject a design that always splices retrieved text
   or metadata into every input regardless of need. Require instead that the model, or the training
   pipeline that shapes it, learn to request extra information selectively from filtered
   self-generated candidates, so it asks only when the information is actually likely to help.

3. **Run the ten-item tool-calling failure-mode checklist (P004).** Walk the submitted trajectory,
   transcript, or design against each item below, in order, and record every match as a finding:
   a. Harmful content produced directly, with no tool call at all.
   b. A tool called while required information stays incomplete or ambiguous and cannot be resolved
      by further tool use.
   c. A tool called before gathering constraint information that additional tool use could have
      supplied.
   d. A known constraint ignored and the tool called anyway.
   e. An implicit or potential risk ignored and the tool called anyway.
   f. Incorrect or inappropriate parameters supplied on the call.
   g. A flagged, unverified, or otherwise known-problematic tool used despite the issue.
   h. A necessary tool not called when the situation required it.
   i. A tool's returned output over-trusted or acted on without validation.
   j. An unsafe choice made among multiple options a tool returned.

4. **If tool use is trained rather than only prompted, check the data pipeline (P043, P044, P045,
   P046).**
   - Confirm the fine-tuning corpus interleaves only the calls whose results actually helped with
     the original text, and that examples where every candidate call was filtered out are dropped
     rather than kept call-free (P043).
   - If a broad corpus yields few retained calls for a given tool, confirm the design combines a
     cheap, targeted prefilter over likely-useful contexts with relaxed sampling thresholds before
     scaling up expensive annotation, rather than jumping straight to more annotation (P044).
   - For a translation tool, confirm call generation targets non-English spans that sit in useful
     surrounding context, filters spans that are only numbers or symbols, and drops any example
     whose relevant text appears only after the point of the call, since the deployed model cannot
     see that future text at inference time (P045).
   - For temporal evaluation or training data, confirm dynamic factual knowledge — facts that change
     over time — is kept separate from calendar arithmetic that needs only the current date, and
     confirm any reported gain is checked against which tool the model actually called rather than
     assumed from the tool's mere availability (P046).

5. **Attribute every claimed gain before accepting it (P030).** Require three comparisons before
   crediting an improvement to tool use: a same-backbone baseline without the tool-use training, a
   continued-training baseline that receives the same extra training compute without tools, and a
   disabled-tool variant of the tool-using model itself. An improvement that only beats an unrelated
   or smaller baseline is not evidence the tool helped.

6. **Compile findings and hand back the decision.** State each finding against the checklist item,
   principle, and trade-off it invokes. Do not write the tool-integration code or choose the
   API/vendor; return the critique and the residual decision to the caller's own team.

## Anti-patterns

- **Always-on retrieval or metadata injection** — appending retrieved text or metadata to every
  input regardless of whether it is needed, instead of letting the model learn when to ask (P047).
- **Tool bolt-on with no baseline** — adding a tool because it is available, without naming the
  weakness it addresses or confirming it is text-invocable, and without a same-backbone /
  disabled-tool comparison to test whether it actually helped (P029, P035, P030).
- **Unattributed gains** — crediting an accuracy or capability improvement to "tool use" without a
  same-backbone, continued-training, and disabled-tool comparison, or without checking which tool
  the model actually invoked (P030, P046).
- **Fabricated or ungrounded call parameters** — accepting a design where the agent supplies
  parameters it was not given rather than gathering them, or where a flagged or unverified tool is
  invoked without addressing the known issue (checklist items f and g, P004).
- **Unfiltered fine-tuning data** — training on every sampled candidate call rather than only the
  calls whose results measurably helped, or keeping examples whose calls were all filtered out
  (P043).
- **Ignoring train/inference asymmetry** — building translation or temporal training examples from
  context the deployed model will not have access to at inference time (P045, P046).

## Principles covered

- **P004** — Diagnose tool-calling behavior against the ten canonical failure modes (the checklist
  in step 3).
- **P029** — Add an external tool only when it is text-invocable and its result addresses a genuine
  model weakness.
- **P030** — Attribute tool-use gains against same-backbone, continued-training, and disabled-tool
  baselines.
- **P035** — Extend the action space with tools for missing domain knowledge or hallucination the
  model cannot self-correct; otherwise rely on its own planning, conversation, and common sense.
- **P043** — Fine-tune on an augmented corpus that interleaves only the helpful calls and their
  results with the original text.
- **P044** — For sparse tool-call opportunities, combine a targeted corpus prefilter with adjusted
  sampling before scaling up annotation.
- **P045** — Curate translation-call data: target non-English spans in useful context, filter
  non-linguistic spans, and drop future-context-dependent examples.
- **P046** — Separate dynamic factual knowledge from calendar arithmetic in temporal evaluation, and
  confirm which tool was actually called.
- **P047** — Prefer selective, learned information requests over always-on retrieval or metadata
  augmentation.

## Inputs

- The tool, API, database, or retrieval mechanism proposed or already in use, and the specific model
  weakness it is meant to address.
- Any available trajectory, transcript, or tool-call log to check against the failure-mode checklist.
- If training is involved, the data-construction pipeline (sampling, filtering, prefiltering) and,
  for translation or temporal tools, how spans and dates are curated.
- Any baselines already run, and how a reported gain is currently being attributed.

## Output

A findings list keyed to the checklist items and principles above: a verdict on whether the tool
addition targets a real, text-representable weakness or should be declined; every failure-mode match
found in the reviewed trajectory or design; data-curation gaps in the training pipeline where
relevant; and, for any claimed gain, whether the required same-backbone, continued-training, and
disabled-tool comparisons are in place. Each finding names its trade-off and ends with a concrete
next step handed back to the caller's own team.

## References

- `references/agent-engineering-principles-index.md` — the full principle index, including P004 and
  P029–P047.
- `references/agent-safety-and-evaluation-evidence-notes.md` — evidence notes underlying the
  failure-mode taxonomy.

## Provenance

Distilled from three sources, all under distillation-only rights (paraphrase only, no verbatim
quotation): an agent-safety benchmark study's failure-mode taxonomy, derived from open-coded analysis
of interaction records (P004); a tool-augmented language-model study's mechanism for compensating
model weaknesses through text-invocable tools, its fine-tuning data construction, and its baseline
design (P029, P030, P043, P044, P045, P046); and a survey of large-language-model agents on why and
when to extend the action space with external tools versus relying on the model's internal planning,
conversation, and common-sense capability (P035). Grounded in principles P004, P029, P030, P035,
P043, P044, P045, P046, P047.
