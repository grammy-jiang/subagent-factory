---
name: deception-detection-evidence-notes
description: How the deception/counter-deception principles are grounded and how to
  keep findings faithful to the source.
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
  - P083
  - P084
  - P085
  - P086
  - P087
  - P088
  - P089
  - P090
  - P091
  - P092
  - P093
  - P094
  claims: []
  evidence: []
  source_anchors: []
  authored_from_digest: 3c52e343cc3ad8f2a6a5622a1817425c2cf98bd34a851b341295bd3b46fb0928
---

# Deception & Counter-Deception Evidence Notes

How the principles are grounded and how to keep findings faithful to the source.

## Grounding chain

Each principle in `principles/principles.yaml` carries `derived_from_claims`; every claim resolves into `analysis/claims.jsonl`, and claims carry evidence in `evidence/evidence-records.yaml` and chunk anchors in `sources/anchors/*.anchors.jsonl` (shape `<sha12>-cNNNN`). A finding cites the principle ID; the chain behind it is auditable.

## Source

- **The Double-Cross System (J. C. Masterman, 1972)** — the official history of Britain's WWII double-agent operations run by the Twenty (XX) Committee: turning and running double agents, feeding deception, network security, assessing enemy belief, governance and approval, strategic stewardship, the physical craft of a plant, and the counter-deception mirror. A **distillation-only** source: paraphrase and restructure only, no verbatim quotation (`.claude/rules/rights-and-quotation-policy.md`, enforced by `quote_scan`).

## Scope and faithfulness rule

The source is one book, from one service, in one war. No finding states a rule more strongly than the source supports: the source itself warns that future operations may not enjoy the same favourable conditions and that evolved control methods are adaptable guides, not fixed laws (P045). Medium-confidence principles (P045–P048, P071–P094) carry that caveat; treat them as guidance to weigh, not doctrine. See `reports/faithfulness-report.yaml` for the per-rule claim-strength check.

