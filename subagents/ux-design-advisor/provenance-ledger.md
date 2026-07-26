# Provenance Ledger — ux-design-advisor

Canonical source of truth: `subagents/ux-design-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (1469 claims),
`evidence/evidence-records.yaml` (540 records), `principles/principles.yaml` (70 principles, 28
high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked
layer. The LLM-authored layer (this profile, the faithfulness report, the skills, references, and
tests) is derived from those principles and their backing claims, evidence, and anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `information-architec-861e11e3` | Information Architecture: For the Web and Beyond (4th ed.) | Rosenfeld, Morville, Arango | 2015 | distillation-only |
| `just-enough-research-e7b74866` | Just Enough Research | Erika Hall | 2019 | distillation-only |
| `conversational-desig-2cf0ebac` | Conversational Design | Erika Hall | 2018 | distillation-only |
| `dont-make-me-think-k-c0958e02` | Don't Make Me Think, Revisited | Steve Krug | 2014 | distillation-only |
| `silva-canedo-chatbot-e16b4082` | Chatbot Design Guidelines | Silva, Canedo | — | distillation-only |
| `conversational-ux-de-2c3bf56d` | Conversational UX Design (practitioner guidance) | — | — | distillation-only |
| `cui20-moore-f888cfc0` | Conversational UX Design (CUI 2020, Moore) | Robert J. Moore | 2020 | distillation-only |

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
| `role` / `quality_bar[0]` (self-evident, effortless use) | P037, P003, P057, P005, P058 |
| `quality_bar[1]` (research matched to problem maturity) | P035, P034, P018, P051, P002 |
| `quality_bar[2]` (IA/navigation from users, content, context) | P017, P015, P019, P064, P029 |
| `quality_bar[3]` (conversation, not facade) | P033, P001, P063, P016, P024 |
| `quality_bar[4]` (state trade-off; test before commit) | P011, P050, P004, P059, P017 |
| `forbidden_behaviours` | P017, P018, P002, P033, P024 |
| `knowledge_partition.always_on` (7 groups) | all 70 principles, one skill group each |

## Skill / reference → principle partition

| Artifact | Grounding principles |
|----------|----------------------|
| `skills/information-architecture-foundations` | P006, P008, P012, P013, P017, P019, P025, P026, P028, P038, P039, P041, P065, P067, P068, P069, P070 |
| `skills/navigation-search-and-findability` | P014, P015, P020, P027, P029, P030, P040, P058, P064 |
| `skills/usability-and-self-evident-design` | P003, P005, P023, P037, P050, P057, P060 |
| `skills/usability-testing-and-evaluation` | P004, P009, P011, P059 |
| `skills/user-research-methods` | P002, P010, P018, P034, P035, P042, P043, P044, P051, P052, P053, P054, P055, P056 |
| `skills/conversational-and-chatbot-design` | P001, P007, P016, P022, P024, P033, P036, P062, P063 |
| `skills/ia-strategy-and-deliverables` | P021, P031, P032, P045, P046, P047, P048, P049, P061, P066 |
| `references/ux-design-principles-index` | all 70 principles (index) |
| `references/conversational-ux-evidence-notes` | P001, P007, P016, P022, P024, P033, P036, P049, P061, P062, P063 |

## Version History

### 0.2.2 — 2026-07-25

- Restated the `router_description` out-of-scope clause by capability instead of naming sibling packages: generated subagents are independent of one another and the orchestrating session does the routing, so a routing string says what this agent does not cover rather than asserting which other package owns it. Also added that `router_description` in the first place (same day), for the routing-truncation reason above. Boundary content unchanged; adapter re-exported. Supersedes only same-day wording, not any principle or rule.

### 0.1.0 — 2026-07-03

Initial authored layer over the map→reduce distilled spine. Derived `profile.yaml` (7 always-on
groups, 3 modes, 5 quality-bar checks), `reports/faithfulness-report.yaml`, seven skills, two
references, and the behaviour + golden test suites from the 70 principles. No prior profile
decisions were superseded (first version).
