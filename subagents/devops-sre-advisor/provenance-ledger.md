# Provenance Ledger — devops-sre-advisor

Single source of truth: `profile.yaml` (v0.3.1). Every profile field traces to the
distilled evidence chain in this package.

## Sources

- `accelerate-the-scien-9d4b1cf2` — Accelerate: The Science of Lean Software and DevOps (sha256 `9d4b1cf206e5…`, distillation-only)
- `automated-root-cause-05cb6ffe` — The Complete Guide to Automated Root Cause Analysis (sha256 `05cb6ffe0ccb…`, distillation-only)
- `comp109-5dbbef8d-50b64948` — Continuous Delivery and DevOps: A Quickstart Guide (sha256 `50b64948b031…`, distillation-only)
- `comp500-15893c30-9fe26df3` — The Site Reliability Workbook: Practical Ways to Implement SRE (sha256 `9fe26df35c80…`, distillation-only)
- `pipeline-as-code-con-7f54213f` — Pipeline as Code: Continuous Delivery with Jenkins, Kubernetes, and Terraform (sha256 `7f54213fedb8…`, distillation-only)
- `site-reliability-eng-0bea4daa` — Site Reliability Engineering: How Google Runs Production Systems (sha256 `0bea4daa68ab…`, distillation-only)
- `the-devops-handbook-861f0551` — The DevOps Handbook: How to Create World-Class Agility, Reliability, and Security in Technology Organizations (sha256 `861f0551c788…`, distillation-only)

## Evidence chain

- Claims: `analysis/claims.jsonl` (4484 atomic claims, ids `C#####`).
- Evidence records: `evidence/evidence-records.yaml` (903 records, ids `E#####`).
- Principles: `principles/principles.yaml` (175 promoted principles, ids `P###`).
- Anchors: `sources/anchors/*.anchors.jsonl` (chunk anchors `<sha12>-cNNNN`).

## Derivation

- `profile.yaml` rules (quality_bar, forbidden_behaviours, modes) are induced from the
  promoted principles; each bracket tag names the current principle id(s) the rule rests on.
- `skills/` and `references/` bodies map principle `operational_mapping` to procedure; their
  frontmatter `provenance` cites the resolvable claim / evidence / chunk-anchor ids they draw on.
- `reports/faithfulness-report.yaml` grades each profile rule against the evidence chain; no
  rule exceeds its source support.
- `tests/principle-behaviour-tests.yaml` exercises every principle (`principle_id`) plus every
  `operational_mapping.test_cases` criterion.

## Version history

- v0.3.1: regenerated the LLM-authored layer (profile sources/tags, faithfulness,
  skills/references provenance, principle-behaviour tests, adapter) onto the map-reduce spine
  (150 principles). Distilled spine unchanged.
- v0.3.2: realigned the authored layer with the current map-reduce spine (175 principles, 4484
  claims, 903 evidence records) after the deep 7-book rebuild renumbered it. Regenerated
  `tests/principle-behaviour-tests.yaml` from the current principles (covers new P151–P160 and
  every `expected_behaviour` matches its current statement); corrected `sources/metadata`
  `source_type` to `markdown`; corrected the evidence-chain counts above; re-exported the adapter
  to refresh the invariant layer. Distilled spine unchanged. Profile / faithfulness / skill bodies
  retained (validate-passing, anchored to source); their secondary principle-id citations still
  reference the pre-rebuild numbering.
