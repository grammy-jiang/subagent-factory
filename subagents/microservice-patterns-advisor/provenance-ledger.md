# Provenance Ledger — microservice-patterns-advisor

## Source pack

| source_id | title | author | year | rights_status | sha256 (short) |
|-----------|-------|--------|------|---------------|----------------|
| microservicepatternl-20260608230325 | Microservice Pattern Language (microservices.io pattern map) | Chris Richardson | 2020 | distillation-only | a36be0e9 |
| chris-richardson-mic-20260611091020 | Microservices Patterns: With examples in Java | Chris Richardson | 2018 | distillation-only | 4bb1a621 |

**Second source (2026-06-11): the full book.** Added the complete book
*Microservices Patterns: With examples in Java* (Chris Richardson, Manning, 2018)
on the same slug. The book carries "All rights reserved" (no open license), an
authored Manning title — classified `distillation-only` (distillation allowed, no
verbatim quotation). Converted PDF → Markdown via `markitdown` (≈190,000 words,
`conversion_status=ok`). This source supplies the per-pattern mechanics, forces,
and benefit/drawback trade-offs that the one-page pattern map only named, and
promotes the package from **tier 0** (catalogue map) to **tier 2** (a
forces-and-trade-offs advisor backed by an evidence chain). The book's Java/Spring
/Eventuate implementation code is deliberately **not** distilled — it is out of
scope (the advisor teaches patterns and trade-offs, not turnkey code).

**Rights detection.** The source's footer reads "© Copyright 2020. Chris
Richardson Consulting, Inc. All rights reserved." No open license (MIT, Apache,
Creative Commons, public domain) is present. Per the rights-and-quotation
policy, the source is classified `distillation-only`: distillation is permitted,
verbatim quotation is not. Pattern names are short factual taxonomy labels (not
quotable prose) and are reproduced as the established vocabulary of the field.

**Conversion.** PDF → Markdown via the `markitdown` converter (Docling not
installed; markitdown is the wired fallback). 1 page, 856 words extracted,
`is_scanned=False`, `noise_ratio=0.0`, derived `conversion_status=ok`. No OCR or
human-review queue entry was required. The source is a single-page 2D pattern
map, so it has no Markdown headings and the anchor injector produced 0 anchors
(expected for a heading-less diagram; not a defect).

## Field distillation log

Every profile field is traced to its source and the interrogation QID(s) used.

| Profile field | source_id | QID(s) | Note |
|---------------|-----------|--------|------|
| `display_name` | microservicepatternl-… | Q1 | Synthesized role label "Microservice Patterns Advisor"; the map titles itself "Microservice patterns / pattern language". |
| `role` | microservicepatternl-… | Q1, Q2 | Advisory role: map an architecture concern onto pattern-language patterns and explain forces and trade-offs. |
| `when_to_use[]` | microservicepatternl-… | Q3 | Five triggers, one per major pattern group present on the map (decomposition; data/consistency/querying; communication/discovery/external API; deployment/infrastructure; observability/security/testing). |
| `when_not_to_use[]` | microservicepatternl-… | Q4 | Three exclusions: implementation/configuration, product/vendor selection, non-microservice concerns. The map names patterns only — it gives no implementation or product guidance. |
| `inputs.required[]` | microservicepatternl-… | Q5 | A statement of the architecture concern/decision and constraints, needed to pick the pattern group. |
| `outputs.primary_format` | microservicepatternl-… | Q6 | Named candidate-pattern shortlist with purpose, trade-offs, and a reasoned recommendation. |
| `outputs.modes[advise]` | microservicepatternl-… | Q9 | Evidence: the source is a pattern-selection map; guiding selection is advisory. |
| `outputs.modes[compare]` | microservicepatternl-… | Q9 | Evidence: patterns are grouped as alternative solutions to a shared problem, justifying comparison of alternatives. |
| `quality_bar[]` | microservicepatternl-… | Q7 | Three falsifiable checks: correct named pattern in correct group; forces/trade-offs stated; alternatives compared. |
| `minimum_useful_output` | microservicepatternl-… | Q11 | One correctly named pattern from the applicable group with a one-sentence purpose/trade-off. |
| `forbidden_behaviours[]` | microservicepatternl-… | Q10 | Three do-not rules: no invented patterns; no product/vendor prescription; no implementation code. |
| `handoff_rules[]` | microservicepatternl-… | Q8 | Architect/engineering team owns the final selection and implementation; the advisor informs, not owns. |
| `source_of_truth_policy.canonical_owner` | microservicepatternl-… | Q8, Q17 | Human architecture owner has final authority; the published pattern language is the authority for which patterns/groups exist. |
| `source_of_truth_policy.may_edit_canonical` | — | — | `false`: a specialist advisor does not edit the canonical design or the pattern language. |
| `source_of_truth_policy.precedence` | microservicepatternl-… | Q17 | Caller's forces/constraints govern the recommendation; names and groupings follow the published language. |
| `knowledge_partition.always_on[]` | microservicepatternl-… | Q12 | The full pattern catalogue grouped as on the map, plus the pattern-language principle (match forces, not universal application). |
| `knowledge_partition.skills[]` | microservicepatternl-… | Q13 | `pattern-selection-walkthrough` — a walkthrough of matching a concern to a group and shortlisting patterns is actionable but too procedural for the profile body. STATUS: stub / draft. |
| `knowledge_partition.references[]` | microservicepatternl-… | Q14 | `microservice-pattern-language-map` — the full grouped catalogue as a reference file. STATUS: stub / draft. |
| `knowledge_partition.mcp` | — | Q15 | Empty — no tool/MCP retrieval evidenced in the source. |
| `knowledge_partition.caller_supplied` | — | Q16 | Empty — no per-project runtime context evidenced; the single required input is the concern statement, kept in `inputs.required`. |

## Evidence gaps (recorded, not invented)

- The source is a one-page pattern map: it names patterns and groups but gives
  no prose on each pattern's mechanics. Per-pattern mechanism and detailed
  trade-off analysis are therefore **out of scope for this package** and must
  not be fabricated; if such depth is wanted it must come from the wider
  microservices.io body in a later, separately-sourced version. The
  `pattern-selection-walkthrough` skill and `microservice-pattern-language-map`
  reference are scaffolded as **stubs (status: draft)** and are not yet
  authored.
- Q15 (MCP/tools) and Q16 (caller-supplied) had no source evidence and are
  recorded as empty rather than inferred.

## Tier-2 evidence chain (2026-06-11, from the book)

The book source drives an evidence chain rather than a flat summary:

- `analysis/claims.jsonl` — 57 atomic claims (`claims-v1`), one paraphrased
  pattern definition or benefit/drawback per claim, all anchored to
  `chris-richardson-mic-20260611091020`. The book's 44 canonical "Pattern: X —
  <solution>" definition lines and its explicit benefit/drawback sections were the
  extraction backbone (e.g. Saga ACD / lack-of-isolation / countermeasures; API
  composition vs. CQRS; choreography vs. orchestration; Database per service vs.
  Shared database; Transactional outbox vs. dual-write).
- `evidence/evidence-records.yaml` — one record per claim (`evidence-records-v1`),
  `quote_allowed: false` throughout (distillation-only). Most are
  `explanation`/`strong`; a few normative stances are `expert` (premature
  adoption C004, shared-database anti-pattern C025) or `moderate`/`medium` (DDD→
  boundary linkage C011).
- `principles/principles.yaml` — 16 operational principles (`principles-v1`)
  promoted from the evidence-backed claims, each mapped to a profile rule and/or a
  skill and/or a reference. These ground the profile's `quality_bar`,
  `forbidden_behaviours`, `always_on`, and modes (rule IDs P001–P016 are cited
  inline in the profile).
- `tests/principle-behaviour-tests.yaml` — one behavioural test per
  high-confidence principle (P014 is `medium`, not required).

### New skills / references (tier-2 partition)

| Profile field | Grounding principle(s) | Note |
|---------------|------------------------|------|
| `skills[pattern-selection-walkthrough]` | P001 | The umbrella concern→group→candidates→forces-weighted recommendation procedure. |
| `skills[service-decomposition-advice]` | P003, P013, P016 | Boundaries, aggregates, monolith migration. |
| `skills[saga-transaction-design]` | P004, P005 | Saga, ACD, countermeasures, choreography vs. orchestration. |
| `skills[cross-service-query-design]` | P006, P014 | API composition vs. CQRS; event sourcing. |
| `skills[interservice-communication-selection]` | P008, P009 | RPI vs. messaging, circuit breaker, transactional outbox, idempotency. |
| `skills[external-api-design]` | P010 | API gateway, BFF, access token. |
| `skills[microservice-testing-strategy]` | P011 | Test pyramid, consumer-driven contract tests. |
| `skills[production-readiness-review]` | P012, P015 | Observability, config, chassis; deployment options. |
| `references[microservice-pattern-language-map]` | P007 (+ catalogue) | Full grouped catalogue. |
| `references[pattern-forces-and-tradeoffs-table]` | P001 | Per-pattern problem / forces / benefits / drawbacks table. |
| `references[saga-countermeasures-checklist]` | P004 | The six saga countermeasures as a checklist. |
| `references[deployment-options-comparison]` | P015 | VM / container / serverless / service mesh comparison. |

## Version history

### 0.6.1 — 2026-07-25

- Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

### 0.1.0 — 2026-06-09
Initial derivation from `microservicepatternl-20260608230325`
(Microservice Pattern Language, Chris Richardson, 2020, distillation-only).
Modes: `advise`, `compare`. No prior decisions superseded (new package).

### 0.2.0 — 2026-06-11
Authored the tier-0 stub bodies (`pattern-selection-walkthrough`,
`microservice-pattern-language-map`) and promoted to `status: ready`.

### 0.3.0 — 2026-06-11
Added the full book *Microservices Patterns* (2018) as a second source on the
same slug; re-derived the profile from a tier-2 evidence chain (57 claims, 57
evidence records, 16 principles, 15 behaviour tests). Expanded the knowledge
partition from 1 skill + 1 reference to 8 skills + 4 references; enriched
`when_to_use`, `modes`, `quality_bar`, and `forbidden_behaviours` with
principle-grounded trade-off language (P001–P016 cited inline). No prior
decisions reversed — the earlier catalogue map remains a source and the original
skill/reference are retained and broadened. Package returned to `status: draft`
during re-derivation pending body authoring of the new stubs.

### 0.4.0 — 2026-06-11
Authored all 8 skill and 4 reference bodies from the package's own principles →
claims → evidence (`authored-doc-v1`, `status: ready`), stamped the drift baseline,
and promoted the package to `status: ready`. `validate_skill_authoring` clean and
quote-scan PASS (no verbatim; both sources `distillation-only`).
