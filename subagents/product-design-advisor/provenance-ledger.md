# Provenance Ledger — product-design-advisor

Canonical source of truth: `subagents/product-design-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl`,
`evidence/evidence-records.yaml` (682 records), `principles/principles.yaml` (110 principles, 87
high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked
layer. The LLM-authored layer (this profile, the faithfulness report, the skills, references, and
tests) is derived from those principles and their backing claims, evidence, and anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `inspired-cagan-4c877a0e` | Inspired: How to Create Tech Products Customers Love | Marty Cagan | 2017 | distillation-only |
| `continuous-discovery-95f398b4` | Continuous Discovery Habits | Teresa Torres | 2021 | distillation-only |
| `escaping-the-build-t-37d2b8d9` | Escaping the Build Trap | Melissa Perri | 2018 | distillation-only |
| `user-story-mapping-p-eaae3b39` | User Story Mapping | Jeff Patton | 2014 | distillation-only |
| `shape-up-singer-47d5381b` | Shape Up | Ryan Singer | 2019 | distillation-only |
| `lean-ux-gothelf-seid-6124b61e` | Lean UX | Jeff Gothelf, Josh Seiden | 2016 | distillation-only |
| `amershi-guidelines-h-eaf47437` | Guidelines for Human-AI Interaction | Saleema Amershi et al. | 2019 | distillation-only |
| `horvitz-mixed-initia-46752b70` | Principles of Mixed-Initiative User Interfaces | Eric Horvitz | 1999 | distillation-only |
| `shneiderman-human-ce-8e4a3c16` | Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy | Ben Shneiderman | 2020 | distillation-only |
| `shneiderman-hcai-new-aee5e108` | Human-Centered AI: A New Synthesis | Ben Shneiderman | 2021 | distillation-only |
| `shneiderman-hcai-thr-8fbc2091` | Human-Centered AI: Three Fresh Ideas | Ben Shneiderman | 2020 | distillation-only |

All sources are `distillation-only`: content is paraphrased and restructured, never quoted
verbatim. The quote-scan and prompt-injection scans pass over the ingested markdown.

## Profile field → principle traceability

Every load-bearing profile rule traces to one or more promoted principles in
`principles/principles.yaml`, which in turn resolve into `derived_from_claims` in
`analysis/claims.jsonl` and their evidence records in `evidence/evidence-records.yaml`. The mapping
is recorded per finding in `reports/faithfulness-report.yaml` (each finding's `note` names the
backing principle and claim IDs). No profile field value is an orphan.

| Profile field | Grounding principles |
|---------------|----------------------|
| `role` | Synthesis of the eight principle clusters below. |
| `quality_bar`, `forbidden_behaviours` | P002, P057, P059, P093 (outcomes); P046, P088, P003, P085 (discovery/MVP); P038, P106, P069 (trade-off/appetite); P030, P031, P033, P099 (prototyping); P001, P026, P005, P052 (human-centered AI); P004, P094, P106 (build-trap forbidden). |
| `handoff_rules`, `source_of_truth_policy` | P021, P089 (lead by influence; produce value, not push ideas). |
| `knowledge_partition.always_on` | The eight clusters (one rule each), citing their principals inline. |
| `outputs.modes` (review/advise/compare) | Cross-cutting: the advisor reviews, advises, and compares against the principle set. |

## Knowledge-partition clusters → skills / references

Each `knowledge_partition.skills` entry operationalizes one cluster of the 110 principles; each
`references` entry indexes or catalogs them. The full principle→skill assignment is recorded in
`references/product-principles-index.md`, and every authored body cites its backing principle,
claim, evidence, and chunk-anchor IDs in its `provenance` frontmatter.

| Skill | Cluster theme | Representative principles |
|-------|---------------|---------------------------|
| `product-strategy-and-outcomes` | Output→outcome, escaping the build trap, deployable strategy | P002, P004, P044, P047, P057, P059, P069, P097 |
| `continuous-discovery-and-research` | User contact, interviewing, opportunity solution trees, personas | P084, P088, P079, P025, P040, P046, P029 |
| `assumptions-hypotheses-and-mvp-experiments` | Testable hypotheses, MVPs, experiments | P003, P093, P092, P085, P073, P100 |
| `prototyping-and-usability-testing` | Fidelity choice, prototype-as-spec, testing with real users | P030, P036, P031, P099, P033, P053 |
| `story-mapping-and-workshops` | Backbone maps, story template, slicing, workshops | P050, P011, P070, P034, P101, P028 |
| `shaping-and-betting-work` | Appetite, shaping abstraction, pitches, scopes, baseline | P038, P063, P105, P106, P051, P067 |
| `empowered-product-teams-and-leadership` | PM role, empowered teams, reviews, org support | P021, P082, P019, P045, P103, P089, P042 |
| `human-centered-ai-interaction-design` | Control vs automation, Prometheus/mixed-initiative, Amershi guidelines | P001, P026, P052, P110, P005, P015, P041 |

| Reference | Content |
|-----------|---------|
| `product-principles-index` | Thematic index of all 110 principles grouped by cluster → skill. |
| `human-ai-interaction-guidelines` | Catalog of the human-centered-AI guidance (Amershi guidelines, Prometheus principles, mixed-initiative rules). |

## Notes

- `sources/metadata/*.metadata.json` `source_type` was corrected from the non-schema token `md` to
  the schema enum value `markdown` (the sources were ingested as Markdown). This is a
  schema-compliance correction only; no distilled content, hash, or anchor changed.

## Version History

- **0.2.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.
