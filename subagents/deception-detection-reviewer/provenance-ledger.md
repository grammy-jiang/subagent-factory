# Provenance Ledger — deception-detection-reviewer

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` → `analysis/claims.jsonl` → `evidence/evidence-records.yaml` →
`sources/anchors/*.anchors.jsonl`), which was assembled by the map→reduce build. No profile field
value is an orphan: every load-bearing rule cites the promoted principle(s) it restates.

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| double-cross-system-34ce671d | The Double-Cross System | J. C. Masterman | 1972 | distillation-only |

The source is **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). It is the official
history of Britain's WWII double-agent operations run by the Twenty (XX / "Double-Cross") Committee.

## Distilled spine

- **94 promoted principles** (`principles/principles.yaml`, P001–P094; 66 high-confidence, 28 medium).
- **303 atomic claims** (`analysis/claims.jsonl`, C-ids), each source-anchored.
- **303 evidence records** (`evidence/evidence-records.yaml`, E-ids keyed by `claim_id`).
- **21 paragraph/chunk anchors** for the source (`sources/anchors/*.anchors.jsonl`, `<sha12>-cNNNN`).

## Profile → principle mapping

The eight skills partition all 94 principles (each principle cited exactly once); the profile's
`quality_bar`, `forbidden_behaviours`, `handoff_rules`, and `knowledge_partition.always_on` carry the
`(Pxxx)` tags of the principles they restate. Coverage:

| Skill | Principles |
|-------|-----------|
| turning-and-running-a-controlled-agent | P001, P002, P008, P012, P019, P020, P026, P030, P031, P036, P055, P065, P072, P073, P080 |
| building-and-feeding-the-deception | P003, P009, P023, P029, P032, P039, P051, P057, P058, P066, P067, P068, P075, P090, P094 |
| network-security-and-compartmentation | P005, P007, P010, P015, P024, P054, P062, P063, P069 |
| assessing-enemy-trust-and-belief | P004, P013, P021, P022, P038, P064, P091 |
| governance-approval-and-organization | P006, P016, P017, P025, P027, P028, P033, P042, P049, P056, P076, P079, P092 |
| strategic-stewardship-and-timing | P014, P034, P035, P040, P043, P047, P052, P053, P060, P061, P071, P083, P086, P087, P088, P089, P093 |
| physical-and-technical-deception-craft | P018, P037, P041, P044, P046, P081, P082, P084, P085 |
| counter-deception-and-the-mirror | P011, P045, P048, P050, P059, P070, P074, P077, P078 |

## Faithfulness

`reports/faithfulness-report.yaml` grades each load-bearing profile rule against its promoted
principles on the five-level claim-strength scale. All findings are `EXACT_SUPPORT` or
`WITHIN_SCOPE` — no rule is stronger than its evidence; the profile restates the source's double-agent
and counter-deception tradecraft and narrows it to review and advice. `source_anchors` are omitted
deliberately; provenance is carried in each finding's note via principle + claim IDs.

## Scope caveat

The spine is one book, one service, one war. The source itself warns that future operations may not
enjoy the same favourable conditions and that evolved control methods are adaptable guides, not fixed
laws (P045). The 28 medium-confidence principles carry that caveat and are treated as guidance to
weigh, not doctrine.

## Version History

### v1.0.0 — 2026-07-11
Initial release. LLM-authored layer (profile, 8 skills, 2 references, faithfulness report, golden +
principle-behaviour tests, adapter) generated over the map→reduce distilled spine. No prior profile
decisions superseded (first version).
