# Provenance Ledger — product-blueprint-reviewer

Canonical source of truth: `subagents/product-blueprint-reviewer/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (527 claims),
`evidence/evidence-records.yaml` (520 records), `principles/principles.yaml` (191 principles, 63
high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked
layer. The LLM-authored layer (this profile, the faithfulness report, the six skills, two
references, and the tests) is derived from those principles and their backing claims, evidence, and
anchors — never from raw source instructions.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `blueprint-contract-8707406d` | Product Blueprint and Stage-Boundary Skill Contract | — | — | distillation-only |
| `stage-boundaries-f4cae146` | Architecture and UX Stage Boundaries | — | — | distillation-only |
| `escaping-the-build-t-8988bab5` | Escaping the Build Trap | Melissa Perri | 2018 | distillation-only |
| `lean-startup-katila-2a049107` | Lean Startup in Technology-Driven Teams (Katila et al.) | — | 2020 | distillation-only |

All sources are `distillation-only`: content is paraphrased and restructured, never quoted verbatim.
The quote-scan and prompt-injection scans pass over the ingested markdown.

## Profile field derivation

Every profile field traces to the promoted principles (which in turn resolve to claims → evidence →
source anchors). Principle IDs cited below are the load-bearing ones; the full grounding is in
`reports/faithfulness-report.yaml`.

| Field | Derived from (principles) | Note |
|-------|---------------------------|------|
| `role` | P030, P034, P090, P029, P012, P021 | Blueprint-altitude reviewer synthesized across the four sources' altitude, build-trap, lean-startup, routing, and product-experience themes; scoped to review/advise (no downstream authoring). |
| `when_to_use` | P090, P031, P029, P147, P067 | Caller-observable review situations: altitude drift, gap/MVP discipline, stage routing, product-experience boundary, outcome framing. |
| `when_not_to_use` | P030, P090, P169 | Exclusions: authoring downstream artifacts, more literature research, out-of-domain sign-off. |
| `outputs.primary_format` + modes | P034, P029, P106, P166 | Structured critique naming outcome/assumption, checking altitude, gaps, routing, and trade-offs; review/advise/compare modes. |
| `quality_bar` | P034/P090/P067; P030/P169/P058/P101; P031/P051/P136/P137; P029/P166/P168/P167; P139/P160/P016 | Five falsifiable checks, each citing its backing principles. |
| `minimum_useful_output` | P034, P029 | Floor: one finding naming outcome + assumption + a named principle + trade-off. |
| `forbidden_behaviours` | P030/P169; P034/P051/P136; P168/P141 | No downstream authoring; no untethered/speculative scope; no trade-off-free recommendation. |
| `handoff_rules` | P021, P144 | Product team + leadership own the blueprint decision and downstream work. |
| `source_of_truth_policy` | P128 | Team owns decisions; the four works are the authority for the principles; the Markdown research report outranks structured artifacts on conflict. |
| `knowledge_partition.always_on` + skills + references | all 191 principles (clustered by theme) | Six always-on rule clusters + six skills + two references (see `CHANGELOG.md`). |
| `examples` | P030/P169/P034/P031/P029; P147/P148 | One happy-path (altitude + build-trap + gap review) and one failure-recovery (decline downstream authoring). |

## Distilled-spine note

The distilled spine is unchanged by this authoring pass. The only edit outside the authored layer was
a schema-compliance correction in `sources/metadata/*.metadata.json`: `source_type` `md` →
`markdown` (the enum value); no distilled content, hash, or anchor changed.

## Supersession

No prior profile decisions were superseded; this is the initial authored layer (`agent_version`
1.0.0) over the deterministic spine.
