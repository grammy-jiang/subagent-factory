# Provenance Ledger — translation-equivalence-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` → `analysis/claims.jsonl` → `evidence/evidence-records.yaml` →
`sources/anchors/*.anchors.jsonl`), which was assembled by the map→reduce build. No load-bearing
profile rule field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| in-other-words-baker-8e6c3cb1 | In Other Words: A Coursebook on Translation | Mona Baker | 1992 | distillation-only |
| dynamic-formal-equiv-e6872198 | Toward a Science of Translating: dynamic and formal equivalence | Eugene A. Nida | 1964 | distillation-only |

Both sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`).

## Distilled spine

- **116 promoted principles** (`principles/principles.yaml`, P001–P116; 5 high-confidence, 111
  medium).
- **415 atomic claims** (`analysis/claims.jsonl`, C-ids), each source-anchored.
- **Evidence records** (`evidence/evidence-records.yaml`, keyed by `claim_id`).
- **28 chunk anchors** across the two sources (`sources/anchors/*.anchors.jsonl`, `<sha12>-cNNNN`).

## Profile → principle mapping

The `knowledge_partition.skills` list partitions all 116 principles across nine skills, each
principle appearing in exactly one skill:

| skill | principles |
|-------|-----------|
| Word-Level Non-Equivalence and Strategies (`word-level-nonequivalence-and-strategies`) | P001, P011, P012, P037, P059, P060, P080, P081, P082, P095, P102, P103, P104, P105, P106 |
| Collocation, Idiom, and Fixed Expression (`collocation-idiom-and-fixed-expression`) | P013, P014, P040, P042, P043, P044, P058, P061, P063, P083, P107, P108, P109, P110 |
| Grammatical Equivalence (`grammatical-equivalence`) | P009, P015, P025, P026, P045, P046, P055, P057, P064, P084, P085 |
| Thematic and Information Structure (`thematic-and-information-structure`) | P002, P003, P016, P024, P027, P028, P029, P030, P047, P048, P065, P066, P067, P086, P088, P089, P090 |
| Cohesion and Texture (`cohesion-and-texture`) | P004, P017, P018, P031, P038, P049, P068, P069, P087, P091, P112 |
| Pragmatic Equivalence, Coherence, and Implicature (`pragmatic-equivalence-coherence-and-implicature`) | P007, P019, P020, P032, P033, P050, P070, P071, P072, P073, P092, P093, P113 |
| Dynamic and Formal Equivalence and Receptor Response (`dynamic-and-formal-equivalence`) | P008, P021, P022, P023, P034, P035, P036, P052, P053, P054, P056, P074, P094, P097, P098, P100, P115 |
| Register, Style, and Literary Form (`register-style-and-literary-form`) | P005, P041, P075, P076, P077, P099, P114, P116 |
| Text-Level Approach and the Limits of Equivalence (`text-level-approach-and-limits-of-equivalence`) | P006, P010, P039, P051, P062, P078, P079, P096, P101, P111 |

The five high-confidence principles (P009, P024, P037, P038, P058) are compiled into the adapter's
`## Operating invariants (must hold)` layer at export and each carries a behaviour test.

## Version history

- **v1.0.0** (2026-07-11) — initial LLM-authored layer (profile, nine skills, two references,
  faithfulness report, golden + principle-behaviour tests, adapter) generated over the pre-built
  distilled spine. Distilled spine unchanged.
