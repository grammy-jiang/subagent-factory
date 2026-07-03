# Provenance Ledger — ui-design-advisor

Canonical source of truth: `subagents/ui-design-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (1597 claims),
`evidence/evidence-records.yaml` (671 records), `principles/principles.yaml` (110 principles, 94
high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked
layer. The LLM-authored layer (this profile, the faithfulness report, the skills, references, and
tests) is derived from those principles and their backing claims, evidence, and anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `refactoring-ui-watha-aee4982c` | Refactoring UI | Adam Wathan, Steve Schoger | 2018 | distillation-only |
| `designing-interfaces-14cab2ec` | Designing Interfaces: Patterns for Effective Interaction Design | Jenifer Tidwell | — | distillation-only |
| `web-form-design-wrob-c8bbfe0c` | Web Form Design: Filling in the Blanks | Luke Wroblewski | 2008 | distillation-only |
| `about-face-cooper-4de086e6` | About Face: The Essentials of Interaction Design | Cooper, Reimann, Cronin, Noessel | 2014 | distillation-only |

All sources are `distillation-only`: content is paraphrased and restructured, never quoted
verbatim. The quote-scan passes over the ingested markdown; the prompt-injection scan findings are
benign body content (triaged, not executed) per `.claude/rules/untrusted-source-policy.md`.

## Profile field → principle traceability

Every load-bearing profile rule traces to one or more promoted principles in
`principles/principles.yaml`, which in turn resolve into `derived_from_claims` in
`analysis/claims.jsonl` and their evidence records in `evidence/evidence-records.yaml`. The mapping
is recorded per finding in `reports/faithfulness-report.yaml` (each finding's `note` names the
backing principle IDs). No profile field value is an orphan.

| Profile field | Grounding principles |
|---------------|----------------------|
| `role` (goal-directed UI critique) | P009, P011, P033, P001, P059, P043 |
| `quality_bar[0]` (name the user goal / persona first) | P009, P011, P005, P033 |
| `quality_bar[1]` (visual hierarchy and grouping) | P001, P099, P074, P100, P102 |
| `quality_bar[2]` (low-effort, error-resistant forms) | P006, P019, P008, P059, P060, P062 |
| `quality_bar[3]` (low-excise, considerate interaction) | P043, P016, P055, P071, P039, P042 |
| `quality_bar[4]` (state trade-off, test with users) | P024, P021, P091 |
| `forbidden_behaviours[1]` (no ungrounded pattern) | P009, P011, P024 |
| `forbidden_behaviours[2]` (no universal rule) | P024, P021 |
| `handoff_rules[0]` (team owns the decision) | P011, P032 |
| `source_of_truth_policy.precedence` | P024, P042 |
| `knowledge_partition.always_on[0]` (goal / mental model) | P009, P011, P033, P007, P016, P094 |
| `knowledge_partition.always_on[1]` (hierarchy and structure) | P001, P099, P074, P100, P102, P028, P058, P061 |
| `knowledge_partition.always_on[2]` (type, color, depth, imagery) | P052, P053, P054, P048, P082, P083, P084 |
| `knowledge_partition.always_on[3]` (forms and inputs) | P006, P019, P003, P031, P058, P061, P059, P060, P062, P063, P008 |
| `knowledge_partition.always_on[4]` (navigation and data display) | P004, P098, P097, P072, P027, P070, P107, P110 |
| `knowledge_partition.always_on[5]` (considerate, low-excise interaction) | P043, P013, P071, P101, P055, P044, P010, P057, P090, P108, P109, P047 |
| `knowledge_partition.always_on[6]` (posture, platform, mobile) | P042, P039, P023, P103, P104, P105, P026, P029, P036 |

## Skills and references

| Artifact | Grounding principles (theme) |
|----------|------------------------------|
| `skills/visual-hierarchy-and-layout` | P001, P028, P053, P056, P058, P061, P074, P099, P100, P102, P110 |
| `skills/typography-color-and-visual-polish` | P048, P052, P054, P082, P083, P084 |
| `skills/form-and-input-design` | P002, P003, P006, P008, P017, P019, P020, P031, P038, P040, P059, P060, P062, P063, P065, P066, P086 |
| `skills/navigation-and-information-structure` | P004, P018, P027, P046, P069, P070, P072, P073, P079, P089, P097, P098, P106, P107 |
| `skills/interaction-controls-and-feedback` | P010, P013, P037, P043, P044, P045, P047, P050, P055, P057, P064, P068, P071, P075, P076, P077, P078, P090, P101, P108, P109 |
| `skills/goal-directed-design-and-research` | P005, P009, P011, P012, P015, P021, P025, P032, P049, P051, P081, P091, P092, P093, P094, P095, P096 |
| `skills/posture-platform-and-mobile-context` | P007, P014, P016, P022, P023, P024, P026, P029, P033, P034, P035, P036, P039, P042, P080, P085, P087, P088, P103, P104, P105 |
| `references/ui-design-principles-index` | all 110 principles, grouped by skill |
| `references/ui-design-evidence-notes` | empirical thresholds (P030 label placement, P103 touch targets, P109 response-time budgets) |

## Distillation notes

- `display_name`, `slug`, `role`: synthesized from the four sources' shared subject (UI / interaction
  design) and the goal-directed framing that dominates the high-confidence principles.
- `when_to_use` / `when_not_to_use`: derived from the principle themes (visual, form, navigation,
  interaction, goal-directed) and the rights/scope boundary (distillation, not implementation).
- `modes` (review / advise / compare): the three recurring critique shapes the principles support.
- `examples`: two worked few-shot cases (happy-path hierarchy/form review; failure-recovery decline
  of code/tool production), grounded in the cited principle IDs.
- Metadata fix: source metadata `source_type` corrected from `md` to `markdown` (schema enum);
  source bytes unchanged.
