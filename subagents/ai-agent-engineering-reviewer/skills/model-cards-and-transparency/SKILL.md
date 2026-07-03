---
name: model-cards-and-transparency
kind: skill
status: ready
provenance:
  principles: [P014, P021, P050]
---

# Model Cards and Transparency

## Purpose

This skill reviews or authors the transparency documentation that should accompany a released
model or agent: a short model card naming what the model is, who it is for, and how it was
evaluated (P014); performance reporting that is broken down by group and by group intersections
rather than collapsed into one aggregate number (P021); and a clear account of the evaluation
data itself — what it is, why it was chosen, and how it was prepared (P050). Use it whenever the
caller is releasing a model or agent, or reviewing someone else's card or evaluation report for
gaps that would leave a reader unable to judge whether the model fits their context.

## When this applies

- A trained model or agent is being released, deployed, or published, and needs a model card.
- An existing model card, evaluation report, or documentation draft is under review for
  completeness or honesty about limits.
- The model is human-centric — its performance is plausibly uneven across population groups —
  and quantitative results are being written up.
- A reviewer needs to check what evaluation data was used and whether it represents realistic and
  challenging conditions, not only easy cases.

## Procedure

1. **Confirm a card exists and is the right size.** A model card should be short — roughly one to
   two pages — and should sit alongside, not replace, documentation of the training data (P014).
   A card that has ballooned into a full report, or that is missing altogether, both fail the
   purpose: a compact, checkable summary.
2. **Check it states basic characteristics and intended use.** The card should let a reader
   quickly answer: what kind of model is this, what was it built to do, and what is it not meant
   for (P014). Flag a card that only lists performance numbers without this framing — numbers
   without context invite use outside the conditions they were measured under.
3. **Check it is written for its actual readers, not only its builders.** A card informs several
   different audiences at once — the team that built it, the team integrating it downstream,
   people deciding whether to adopt it, and people who may be affected by its outputs (P014).
   Reject a card that assumes deep familiarity with the model's internals as its only audience.
4. **Check the evaluation procedure is disclosed.** The card should describe how the reported
   numbers were produced, not just state them (P014) — this is what lets a reader judge whether
   the evaluation matches their own use case.
5. **Check the evaluation data is documented, not just the results.** Confirm the card names which
   datasets were used, why those were chosen over alternatives, and what preprocessing was applied
   before scoring; prefer datasets that are publicly available so others can reproduce or extend
   the benchmark (P050).
6. **Check evaluation coverage includes hard cases, not only typical ones.** Evaluating only on
   data that mirrors the easiest or most common use case will miss failures; check that the data
   also covers anticipated difficult or edge-of-distribution scenarios likely to stress the model
   (P050).
7. **Treat synthetic evaluation data as a narrow supplement, never full coverage.** Synthetic data
   can usefully fill a gap when a population is otherwise unrepresented in available real data, but
   flag any card that treats a synthetic set as comprehensive — note explicitly that it covers only
   a narrow slice of cases (P050).
8. **Check results are broken down by group, not reported only in aggregate.** Quantitative results
   should be disaggregated by the cultural, demographic, or phenotypic groups and other
   domain-relevant conditions that matter for the model's intended use, not collapsed into one
   overall score (P021).
9. **Check for intersectional breakdowns, not only single-factor ones.** Beyond each group
   considered alone, confirm the card also reports performance across combinations of two or more
   groups together; looking at one characteristic at a time can miss effects that only appear when
   characteristics interact (P021).
10. **Look for a hidden disparity behind a good aggregate number.** An acceptable overall score can
    still mask a subgroup that performs far worse; treat an aggregate-only report as incomplete
    regardless of how strong the headline number looks (P021).
11. **Where feasible, check disaggregated numbers carry an uncertainty measure.** Small subgroup
    slices are noisier than the full evaluation set; prefer a card that reports a confidence
    interval or similar variation alongside each disaggregated figure over a bare point estimate
    (P021).
12. **Summarize as a gap list, not a verdict.** Close the review with the specific gaps found
    against these checks — card scope and audience, evaluation-data documentation, disaggregated
    and intersectional reporting — so the author has a concrete next step rather than a pass/fail
    judgment.

## Anti-patterns

- Reporting one aggregate accuracy or quality number with no breakdown by group or condition,
  which lets a real disparity hide behind a healthy-looking overall score (P021).
- Reporting group-level results only in isolation, never intersectionally, so an interaction
  effect between two characteristics goes unnoticed (P021).
- Publishing evaluation results without documenting which datasets were used, why, or how they
  were preprocessed, leaving a reader unable to judge whether the numbers transfer to their
  context (P050).
- Evaluating only on data that mirrors the easy, typical case and never on harder or
  edge-of-distribution scenarios (P050).
- Presenting a synthetic evaluation set as if it comprehensively covered a population, rather than
  flagging it as a narrow supplement (P050).
- Releasing a model with no intended-use or limitations section, so readers cannot tell what
  contexts the model was and was not built or checked for (P014).
- Writing the card only for the team that built the model, leaving downstream integrators,
  decision-makers, or people affected by the model's outputs without the context they need (P014).

## Principles covered

- P014 — accompany every released model with a short, stakeholder-readable card covering its
  characteristics, intended use, and evaluation procedure.
- P021 — report performance disaggregated by individual group and intersectionally across groups,
  not by aggregate metrics alone.
- P050 — document the evaluation data itself (datasets, motivation, preprocessing), cover typical
  and challenging scenarios, and treat synthetic data as narrow, not comprehensive.
