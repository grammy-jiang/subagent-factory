# Provenance Ledger — harness-engineering-advisor

The canonical source of truth for this package is `profile.yaml`. Every profile field, principle, and
authored body traces back to one of the two ingested sources through the distilled evidence chain
(`analysis/claims.jsonl` → `evidence/evidence-records.yaml` → `principles/principles.yaml`) and the
chunk-level anchor index (`sources/anchors/*.anchors.jsonl`). No orphan field values.

## Sources

| source_id | Title | Rights | sha256 (12) |
|-----------|-------|--------|-------------|
| harness-engineering-a4430459 | Harness Engineering for AI Agents — Literature Synthesis | distillation-only | a4430459ad17 |
| harness-engineering-7631b6ed | Harness Engineering for Local AI Coding Agents — Engineering Guide | distillation-only | 7631b6ed4409 |

Both sources are `distillation-only`: distillation is permitted, verbatim quotation is not. The
`quote_scan` gate passes (no 40+ consecutive source-word runs), and the verbatim `sources/original`
directory is withheld by the rights-clean export policy.

## Distillation chain

- **Claims** — 265 atomic, typed, source-anchored claims (`analysis/claims.jsonl`), each bound to a
  chunk-level (paragraph) anchor via `source_anchors`.
- **Evidence** — 265 evidence records (`evidence/evidence-records.yaml`) linking each claim to its
  source anchors, evidence strength, and support level.
- **Principles** — 75 promoted operational principles (`principles/principles.yaml`), each resolving to
  its backing claims through `derived_from_claims`. 29 are high-confidence; the remainder medium.
- **Faithfulness** — `reports/faithfulness-report.yaml` grades the load-bearing profile rules against
  the principles/claims on the claim-strength ladder. All findings sit at WITHIN_SCOPE; the profile
  narrows the sources to review/advice and never broadens them.

## Authored layer

- **profile.yaml** — role, scope, modes, quality bar, forbidden behaviours, and knowledge partition,
  each citing the principle IDs it rests on. `sources[]` mirrors the manifest source_ids and sha256s.
- **skills/** — nine skills partition the 75 principles by harness layer (architecture, governance,
  verification, context/memory, tools/supply-chain, observability, evaluation, multi-agent/self-evolution,
  repository readiness). Each cites its principles and backing claims.
- **references/** — `harness-engineering-principles-index` (all 75 principles) and
  `harness-engineering-evidence-notes` (grounding and confidence distribution).
- **tests/** — `golden-tests.yaml` (routing + behaviour) and `principle-behaviour-tests.yaml` (one test
  per principle, referencing its `principle_id`).

## Version history

### 0.1.1 — 2026-07-25

- Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

### 0.1.0 — 2026-07-06

Initial release. Distilled spine assembled by the map→reduce build (265 claims, 265 evidence records,
75 principles across two sources). LLM-authored layer (profile, faithfulness report, nine skills, two
references, golden + principle-behaviour tests, adapter) derived from the principles. No prior profile
decisions superseded.
