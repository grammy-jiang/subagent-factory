---
name: harness-engineering-evidence-notes
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
  claims: []
  evidence: []
  source_anchors: []
---

# Harness Engineering — Evidence Notes

How the 75 principles are grounded. The distilled spine holds **253 atomic claims** and **250 evidence records** across two distillation-only sources, each claim bound to a chunk-level (paragraph) anchor in the source markdown.

## Sources

- **Harness Engineering for AI Agents — Literature Synthesis** (`harness-engineering-a4430459`): a multi-paper research synthesis defining harness engineering, the 12-layer reference architecture, the field's themes (harness as the unit of evaluation, observability mandate, verify-before-commit, memory as a governed resource, tool-access governance, runtime governance as a non-decomposable stack, supply-chain and adversarial defense), points of agreement and contradiction, and open research gaps.
- **Harness Engineering for Local AI Coding Agents — Engineering Guide** (`harness-engineering-7631b6ed`): the practical counterpart — bootstrap checklist, manifest hierarchy, permissions and tool DAG, sandbox and supply-chain controls, the verify-before-commit gate sequence and DryRUN contract, and the evaluation harness (Harness Condition Sheet, AI-readiness score).

## Confidence distribution

- **high**: 29 principles — grounded in convergent, replicated, or directly-stated source support.
- **medium**: 46 principles — grounded in the engineering guide's practices or a single strong source passage.

## Faithfulness posture

The per-rule faithfulness review (`reports/faithfulness-report.yaml`) grades each load-bearing profile rule against the promoted principles and their backing claims on the claim-strength ladder (EXACT_SUPPORT → WITHIN_SCOPE → SCOPE_BROADENED → HEDGING_REMOVED → CONTRADICTED). Rules that would overstate an open problem — dynamic memory-router selection (P031), compound attestation (P049), solved adversarial control (P016) — are held at the source's hedged strength.

