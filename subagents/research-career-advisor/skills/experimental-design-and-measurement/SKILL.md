---
name: experimental-design-and-measurement
kind: skill
status: ready
provenance:
  principles:
  - P014
  - P040
  - P041
  - P047
  - P048
  claims:
  - C00228
  - C00229
  - C00230
  - C00231
  - C00233
  - C00234
  - C00235
  - C00236
  - C00241
  - C00242
  - C00243
  - C00244
  - C00245
  - C00246
  - C00249
  - C00250
  evidence: []
  source_anchors: []
  authored_from_digest: 064a7142f87aa1117ddacdb9eb44387940091499a0b3b57e9cd34d5749ff20a4
---

# Experimental Design And Measurement

## Purpose

This skill guides designing sound empirical studies and knowing when to trust their measurements. It checks that reported precision is treated as possibly optimistic until the uncertainty process accounts for apparatus tuning and selection effects and is checked by independent, holdout, or later measurements; that null-hypothesis testing obtains an appropriate null sampling distribution, expresses the observed deviation in standard-error units where applicable, and rejects only under a preselected unlikely region; that a fully-crossed factorial design is used only for the factor combinations and interactions the research claims need, splitting the study when unneeded higher-order interactions would make the trial count excessive; that instruments, test apparatus, and self-generated telemetry are validated independently before being trusted over the system they measure; and that when intended service life exceeds the validation window, accelerated-test extrapolation is treated as uncertain, validation is planned explicitly, and reliability is built into the design.

## When to use

- Measurement uncertainty must account for tuning and selection effects and be checked independently before reported precision is trusted (P014).
- A null-hypothesis test needs a valid sampling distribution, standard-error framing, and a preselected rejection region (P040).
- A factorial design must retain only the factor combinations and interactions the claims require, splitting the study otherwise (P041).
- Instruments or self-generated telemetry must be validated independently, and accelerated-test extrapolation beyond the validation window treated as uncertain (P047, P048).

## Procedure

1. Assume reported precision may be optimistic until the uncertainty process accounts for apparatus tuning and selection effects and is checked by independent, holdout, or later measurements (P014).
2. For null-hypothesis testing, obtain an appropriate null sampling distribution, express the observed deviation in standard-error units when applicable, and reject only under a preselected unlikely region (P040).
3. Use a fully crossed factorial design only for factor combinations and interactions that answer the research claims; split the study when unneeded higher-order interactions would make the trial count excessive (P041).
4. Validate instruments, test apparatus, and self-generated telemetry independently before treating them as more trustworthy than the system they measure (P047).
5. When intended service life exceeds the validation window, treat accelerated-test extrapolation as uncertain, plan validation explicitly, and build reliability into the design (P048).

## Inputs

- The study design, statistical test, or measurement setup, the claims it must support, and the reliability of its instruments and the service horizon.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of importance, readiness, or soundness made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-career and empirical practice; it does not run the study, write the paper or grant, or make the hiring, admission, funding, or tenure decision for the caller.

## Anti-patterns to flag

- Overlooking P014: Assume reported precision may be optimistic until the uncertainty process accounts for apparatus tuning and selection effects and is checked.
- Overlooking P040: For null-hypothesis testing, obtain an appropriate null sampling distribution, express the observed deviation in standard-error units when.
- Overlooking P041: Use a fully crossed factorial design only for factor combinations and interactions that answer the research claims; split the study when unneeded.
- Overlooking P047: Validate instruments, test apparatus, and self-generated telemetry independently before treating them as more trustworthy than the system they.
- Overlooking P048: When intended service life exceeds the validation window, treat accelerated-test extrapolation as uncertain, plan validation explicitly, and build.

## References

See `../../references/research-career-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/research-career-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P014, P040, P041, P047, P048, grounded in the four distillation-only sources (*A PhD Is Not Enough* by Peter J. Feibelman, a survival guide for a career in science; *The Art of Doing Science and Engineering* / *You and Your Research* by Richard W. Hamming, on doing high-impact research; a Chinese guide to succeeding in academic research; and *Empirical Methods for Artificial Intelligence* by Paul R. Cohen, on experimental method and measurement). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
