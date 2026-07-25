---
name: experimental-design-and-measurement
description: >-
  Guides designing sound empirical studies and judging whether their measurements can be
  trusted. Use when reported precision, a null-hypothesis test, a factorial design, an
  instrument or self-generated telemetry stream, or an accelerated-test extrapolation
  needs to be checked before a claim is built on it. Checks that uncertainty accounts for
  apparatus tuning and selection effects, that significance testing uses a valid sampling
  distribution and a preselected rejection region, that factorial designs carry only the
  interactions the claims require, and that instruments and reliability projections are
  validated independently rather than trusted by default. Not for generic software QA or
  business analytics with no empirical-study-soundness dimension; adjudicating suspected
  p-hacking or misconduct belongs to research-integrity-reproducibility-advisor.
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

This skill guides designing sound empirical studies and judging whether their measurements
can be trusted — checking that reported precision is treated as possibly optimistic until the
uncertainty process accounts for apparatus tuning and selection effects and is verified by an
independent check; that null-hypothesis tests use an appropriate sampling distribution and a
preselected rejection region; that factorial designs carry only the factor combinations and
interactions the claims require; and that instruments, telemetry, and accelerated-test
reliability projections are validated independently rather than trusted by default.

## When to use

- A study reports a precision figure and the analyst has not shown the uncertainty process
  accounts for apparatus tuning and selection effects and has been checked independently
  (P014).
- A null-hypothesis test's significance claim needs its sampling distribution, standard-error
  framing, and rejection region checked (P040).
- A factorial design's factor combinations and interactions need to be checked against what
  the research claims actually require (P041).
- An instrument, test apparatus, or self-generated telemetry stream is being trusted without
  independent validation against the system it measures (P047).
- A reliability or lifetime claim rests on accelerated-test extrapolation beyond the window
  the test actually validated (P048).

## Procedure

1. Treat any reported precision as possibly optimistic; require that the uncertainty process
   name and account for apparatus tuning and selection effects, and confirm it has been
   checked by independent, holdout, or later measurements before accepting the figure (P014).
2. For a null-hypothesis test, verify the analysis obtained an appropriate null sampling
   distribution for the statistic in question, expressed the observed deviation in
   standard-error units where that framing applies, and rejected the null only inside a
   preselected unlikely region fixed before the data were examined (P040).
3. Check the factorial design against the research claims: retain only the factor
   combinations and interactions the claims actually need, and require the study be split
   into smaller trials when unneeded higher-order interactions would otherwise inflate the
   trial count (P041).
4. Require that instruments, test apparatus, and self-generated telemetry be validated
   independently — against a known reference or an outside check — before they are trusted
   as more accurate than the system under test they are measuring (P047).
5. When the claimed service life exceeds the window the test covered, treat any
   accelerated-test extrapolation as uncertain by default; require an explicit validation
   plan for the untested horizon and confirm reliability was built into the design rather
   than assumed from the accelerated result (P048).

## Inputs

- The study design, statistical test, or measurement setup, the claims it must support, and
  the reliability of its instruments and the service horizon.
- The reasoning offered for the decision under review: the goal, the plan or practice in
  place, and any claim of importance, readiness, or soundness made.

## Output

Shape the output to the mode the request calls for:

- **advise** — one recommendation tied to the situation, naming the principle(s) it engages and the residual trade-off or referral.
- **review** — a findings list keyed to area; per finding name the gap and the principle it engages, give the correction, state the trade-off or referral, and end with a concrete next step, highest-impact first.
- **plan** — an ordered plan of steps, each tied to its principle and scoped to the horizon.

Whichever mode: this skill advises on research-career and empirical practice; it does not run the study, write the paper or grant, or make the hiring, admission, funding, or tenure decision for the caller.

## Anti-patterns to flag

- A reported precision figure carries no account of apparatus tuning or selection effects and
  has never been checked against an independent, holdout, or later measurement (P014).
- A significance claim is asserted without showing the null sampling distribution used, the
  standard-error framing, or a rejection region that was fixed before the data were seen
  (P040).
- A fully crossed factorial design runs every combination and higher-order interaction even
  though the research claims only need a subset, inflating the trial count without
  justification (P041).
- An instrument, test apparatus, or self-generated telemetry stream is treated as more
  trustworthy than the system it measures with no independent validation on record (P047).
- A reliability or lifetime claim extrapolates an accelerated test past its validated window
  with no explicit plan to validate the untested horizon (P048).

## References

Consult `../../references/research-career-principles-index.md` only when a finding's principle needs its full source-grounded statement, or when the issue may belong to a sibling skill and you need to confirm which skill owns it. Consult `../../references/research-career-evidence-notes.md` only when the caller disputes a finding's grounding and you need its source basis.

## Provenance

Derived from P014, P040, P041, P047, P048, grounded in the four distillation-only sources (*A
PhD Is Not Enough* by Peter J. Feibelman, a survival guide for a career in science; *The Art
of Doing Science and Engineering* / *You and Your Research* by Richard W. Hamming, on doing
high-impact research; a Chinese guide to succeeding in academic research; and *Empirical
Methods for Artificial Intelligence* by Paul R. Cohen, on experimental method and
measurement). The frontmatter `provenance` block lists the exact principle and claim ids,
which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
