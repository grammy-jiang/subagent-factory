# Provenance Ledger — technical-translation-advisor

## Sources

| source_id | title | author | year | rights |
|---|---|---|---|---|
| technical-translatio-41f3c47c | Technical Translation: Usability Strategies for Translating Technical Documentation | Jody Byrne | 2006 | distillation-only |
| scientific-technical-d92653ac | Scientific and Technical Translation Explained | Jody Byrne | 2012 | distillation-only |

## Distilled spine

- Claims: 850 (`analysis/claims.jsonl`), spanning 2 source(s).
- Evidence records: 713 (`evidence/evidence-records.yaml`).
- Principles: 150 (`principles/principles.yaml`) — 129 high, 21 medium.
- The spine was assembled by the map→reduce build and is deterministically valid; the profile, faithfulness report, skills, references, and tests are derived from it.

## Profile field provenance

Every profile rule cites the principle ids it derives from (see `quality_bar`, `forbidden_behaviours`, `handoff_rules`, `knowledge_partition.always_on`) and is graded in `reports/faithfulness-report.yaml`. Each of the 10 skills and 2 references carries a `provenance` block of real principle / claim / evidence ids that resolve into the spine.

## Skill → principle map

| skill | # principles | principle ids |
|---|---|---|
| analyzing-audience-brief-and-skopos | 13 | P002, P007, P020, P024, P056, P061, P069, P090, P099, P108, P109, P121, P129 |
| selecting-translation-strategy-and-procedures | 16 | P014, P015, P035, P046, P070, P089, P100, P107, P114, P115, P116, P130, P131, P132, P133, P136 |
| grounding-translation-in-reader-cognition | 22 | P003, P009, P010, P017, P023, P025, P030, P031, P037, P043, P045, P057, P058, P060, P062, P063, P082, P111, P112, P118, P123, P137 |
| handling-terminology-units-and-nomenclature | 12 | P071, P079, P093, P094, P098, P101, P103, P104, P122, P140, P149, P150 |
| applying-iconic-linkage-and-consistency | 7 | P013, P021, P026, P044, P074, P075, P134 |
| matching-document-type-and-genre | 15 | P068, P072, P077, P080, P091, P092, P095, P096, P097, P110, P113, P125, P126, P127, P128 |
| designing-document-structure-and-presentation | 13 | P004, P005, P012, P016, P028, P029, P038, P047, P083, P106, P124, P147, P148 |
| planning-usability-evaluations | 11 | P006, P018, P022, P032, P039, P040, P041, P042, P049, P064, P084 |
| running-and-analyzing-usability-studies | 19 | P019, P027, P033, P034, P050, P051, P052, P053, P054, P065, P066, P067, P073, P076, P085, P086, P087, P088, P120 |
| assuring-quality-safety-and-practice | 22 | P001, P008, P011, P036, P048, P055, P059, P078, P081, P102, P105, P117, P119, P135, P138, P139, P141, P142, P143, P144, P145, P146 |

## Version history

- **v1.1.0** (2026-07-12): Review-loop convergence via `/review-subagent` — resolved the 8 must-fix from the review panel (structural lenses + documentation-as-code + ux-design, plus the translation-equivalence and descriptive-translation domain lenses at adversarial verify), each grounded in the existing spine: regenerated all 10 skill bodies without the fixed-length truncation (MF2); attributed the P146 notice-severity table to Byrne and hedged to the governing warning-label standard (MF3); rephrased invariant P003 from a production imperative to advisory (MF8); added an explicit safety/legal sign-off forbidden behaviour (MF4); dropped a manufactured evidence anchor (P045) from precedence (MF5), narrowed the source-deficiency escalation to safety-critical content (MF6), and restored P133's client-permission caveat (MF7). Also graded the precedence rule in the faithfulness report and corrected the P078 handoff citation. Supersedes — does not delete — the v1.0.0 decisions below.
- **v1.0.0** (2026-07-11): Initial LLM-authored layer (profile, faithfulness, 10 skills, 2 references, tests, adapter) derived from the deterministically-valid 2-source, 150-principle distilled spine. Rights: distillation-only; no verbatim source quotation. multisource_synthesis deferred.
