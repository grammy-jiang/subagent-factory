---
name: analytic-method-evidence-notes
kind: reference
status: ready
provenance:
  principles:
    - P001
    - P002
    - P003
    - P004
    - P005
    - P006
    - P007
    - P008
    - P009
    - P010
    - P011
    - P012
    - P013
    - P014
    - P015
    - P016
    - P017
    - P018
    - P019
    - P020
    - P021
    - P022
    - P023
    - P024
    - P025
    - P026
    - P027
    - P028
    - P029
    - P030
    - P031
    - P032
    - P033
    - P034
    - P035
    - P036
    - P037
    - P038
    - P039
    - P040
    - P041
    - P042
    - P043
    - P044
    - P045
    - P046
    - P047
    - P048
    - P049
    - P050
    - P051
    - P052
    - P053
    - P054
    - P055
    - P056
    - P057
    - P058
    - P059
    - P060
    - P061
    - P062
    - P063
    - P064
    - P065
    - P066
    - P067
    - P068
    - P069
    - P070
    - P071
    - P072
    - P073
    - P074
    - P075
    - P076
    - P077
    - P078
    - P079
    - P080
    - P081
    - P082
  claims: []
  evidence: []
  source_anchors: []
---
# Analytic-Method Evidence Notes

How this package's principles are grounded, and how to read a finding's provenance.

## Sources

Six works on analytic tradecraft, all `distillation-only` (principles are distilled and
paraphrased; no verbatim quotation appears in generated artifacts):

- **Psychology of Intelligence Analysis** — Richards J. Heuer Jr. (1999): mind-sets, schemata,
  Analysis of Competing Hypotheses, and the perception errors structured techniques counter.
- **A Tradecraft Primer** — US CIA, Sherman Kent School (2009): the structured analytic techniques
  themselves (brainstorming, Key Assumptions Check, Outside-In, Alternative Futures, Red Team,
  Indicators) and how to sequence them.
- **Thinking, Fast and Slow** — Daniel Kahneman (2011): dual-process reasoning and the cognitive
  biases (affect heuristic, anchoring, availability, WYSIATI) that distort intuitive judgment.
- **Superforecasting** — Philip E. Tetlock and Dan Gardner (2015): probabilistic judgment,
  calibration, the outside view, coherence, and aggregating independent estimates.
- **Expert Political Judgment** — Philip E. Tetlock (2005): the measured limits of expert
  prediction, data-driven versus conceptually-driven analysis, and over-confidence.
- **Perception and Misperception in International Politics** — Robert Jervis (1976): how states
  and adversaries perceive and misperceive, deterrence versus spiral models, and signaling.

## Grounding chain

Each principle is promoted from one or more atomic claims extracted from these sources; each claim
is anchored to a source chunk and backed by an evidence record. A finding cites a **principle ID**
(e.g. `P013`); to trace it, follow `principles.yaml → derived_from_claims → analysis/claims.jsonl`
(and `evidence/evidence-records.yaml`).

## Faithfulness

No generated rule is stronger than its source support. The profile narrows these sources to a
review-and-advise posture — it critiques analytic method and never makes the substantive judgment.
`reports/faithfulness-report.yaml` grades each profile rule on the claim-strength ladder
(`EXACT_SUPPORT → WITHIN_SCOPE → SCOPE_BROADENED → HEDGING_REMOVED → CONTRADICTED`).
