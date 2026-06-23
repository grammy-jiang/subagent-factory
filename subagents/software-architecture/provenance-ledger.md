# Provenance Ledger — software-architecture

Canonical owner of this ledger: the subagent-factory. This records the distillation of **nine**
canonical software-architecture books into the `software-architecture` reviewer package. From
v0.4.0 the package carries the **deep map→reduce spine** (promoted from the
`software-architecture-p0` build): 2420 source-anchored claims and 50 operational principles over
the same nine books.

## Rights status

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| fundamentals-of-soft-6b15bd8c | Fundamentals of Software Architecture | Mark Richards, Neal Ford | 2020 | distillation-only |
| book-clean-architect-a547bab6 | Clean Architecture | Robert C. Martin | 2018 | distillation-only |
| software-architectur-1c336f5c | Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani | 2021 | distillation-only |
| patterns-of-enterpri-fbd95667 | Patterns of Enterprise Application Architecture | Martin Fowler | 2002 | distillation-only |
| mark-richards-softwa-8afbdb74 | Software Architecture Patterns | Mark Richards | 2015 | distillation-only |
| designing-event-driv-ddde058a | Designing Event-Driven Systems | Ben Stopford | 2018 | distillation-only |
| enterprise-integrati-be84e4ec | Enterprise Integration Patterns | Gregor Hohpe, Bobby Woolf | 2003 | distillation-only |
| scalable-architectur-705fce79 | Scalable Internet Architectures | Theo Schlossnagle | 2006 | distillation-only |
| scalability-rules-745dee44 | Scalability Rules: 50 Principles for Scaling Web Sites | Martin L. Abbott, Michael T. Fisher | 2011 | distillation-only |

**All nine sources are copyrighted, authored, commercially published books** (O'Reilly,
Pearson/Addison-Wesley/Sams). Each carries an explicit "All rights reserved" copyright notice in its
front matter. Per `.claude/rules/rights-and-quotation-policy.md` they are classified
`distillation-only`: distillation and paraphrase are permitted; **no verbatim quotation** appears
in any generated artifact, and `quote_allowed: false` on every evidence record. The quote-scan gate
confirms no 40+ consecutive-word source spans in output.

## Multi-source authoring note

This package is grounded in **all nine** sources at once (multi-source). The nine sources are
complementary, not contradictory, on the rules promoted: foundations and trade-off thinking
(Fundamentals), dependency/boundary discipline (Clean Architecture), distributed hard parts
(The Hard Parts), enterprise structure and persistence (PoEAA), style selection (Software
Architecture Patterns), event collaboration (Designing Event-Driven Systems), asynchronous
integration (Enterprise Integration Patterns), and internet-scale scalability (Scalable Internet
Architectures, Scalability Rules). No inter-source conflict required resolution; cross-source
clustering / conflict-graph synthesis is deferred (`multisource_synthesis: deferred`).

## Tier classification

`classify_tier` computes **tier 2** (multiple long, content-dense sources). The deep Tier-1+
evidence chain is the **map→reduce build over the nine books**: `analysis/claims.jsonl`
(**2420 claims**) → `evidence/evidence-records.yaml` (**298 evidence records**) →
`principles/principles.yaml` (**50 principles**, `P001–P050`) → `tests/principle-behaviour-tests.yaml`
+ the Step-13 `tests/behaviour-tests.yaml`, with `reports/faithfulness-report.yaml` over every
load-bearing profile rule. 17 skills and 5 references are authored bodies.

## Provenance traceability

Every profile field traces to its sources through the evidence chain rather than a flat Q-map: each
profile rule cites principle IDs (`P0NN`), each principle's `derived_from_claims` lists the claim
IDs it was promoted from (`analysis/claims.jsonl`), and each claim is source-anchored to one of the
nine `sources/markdown/*` (with `sources/anchors/*`). `sources[]` in `profile.yaml` traces each
`source_id` + `sha256` to ingested `sources/metadata/*.metadata.json`. The Q1–Q18 source
interrogation behind the profile fields is recorded in `interrogation-records.yaml`.

## Evidence-grading + ask-gate provenance

- **Step-16 GRADE** (v1.0.0): every principle carries a `grade` block (`source_type` + up/down
  factors). The 10 cross-source-corroborated principles (`P001–P012`, derived from ≥2 sources) grade
  `expert-book + [corroborated]`; 32 single-source high principles grade `classic`; the 8 medium
  principles grade `expert-book`. `validate_confidence_grade` enforces
  `grade_confidence(grade).level == confidence`.
- **Step-13 ask-gate** (v1.0.0): 48 decision-context-dependent principles carry `must_ask_for` slots
  (the profile's declared driving forces — prioritized characteristics + constraints); the two
  universal-invariant principles (`P001`, `P024`) carry none, to avoid over-asking.

## Version history

- 0.1.0 (2026-06-20): initial multi-source authoring from the original seven sources. Tier-2
  evidence chain authored in-thread; package status `draft` with skill/reference stubs.
- 0.2.0 (2026-06-20): authored every skill and reference body; package promoted `draft` → `ready`;
  adapter re-exported. No source, claim, or principle change.
- 0.3.0 (2026-06-20): **incremental add-source** via the subagent-maintenance flow. Added two
  scalability books — *Scalable Internet Architectures* (`scalable-architectur-705fce79`) and
  *Scalability Rules* (`scalability-rules-745dee44`), both `distillation-only`. The shallow build
  reached 42 claims / 20 principles over the nine books. (Superseded by 0.4.0.)
- 0.4.0 (2026-06-24): **promoted the deep `software-architecture-p0` spine to canonical.** The
  shallow 42-claim / 20-principle build was replaced by the deep map→reduce build over the **same
  nine books** (byte-identical source hashes): 2420 claims, 298 evidence records, 50 principles
  (`P001–P050`), 17 authored skills, 5 references, regenerated behaviour suite — all
  faithfulness-clean. `sources/markdown` + `sources/{metadata,assets,original}` kept from the
  canonical package; `sources/anchors` adopted from the p0 build to match its claim grounding. Per
  the supersession rule, the 0.1.0–0.3.0 decisions above remain on record; the deep spine supersedes
  the shallow one. Adapter re-exported; validate PASS; quote-scan clean.
- 1.0.0 (2026-06-24): **first stable release of the modernized deep build.** Added Step-16 GRADE
  evidence grading to all 50 principles (`validate_confidence_grade` gate) and the opt-in Step-13
  Answer/Ask/Abstain ask-gate (`must_ask_for` cues on 48 principles + a measured behaviour suite).
  Refreshed README / this ledger / profile prose to the nine-book deep spine. `agent_version`
  `0.4.0` → `1.0.0`. The `software-architecture-p0` staging package is retired. validate PASS;
  faithfulness clean; quote-scan clean.
