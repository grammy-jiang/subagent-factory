# Provenance Ledger — software-architecture

Canonical owner of this ledger: the subagent-factory. This records the distillation of **nine**
canonical software-architecture books into the `software-architecture` reviewer package. From
v1.1.0 the package carries the **calibrated map→reduce spine** (`build_map_reduce --select 0.25`
over the same nine books): 2420 source-anchored claims and **69** operational principles — the
top quarter of the deduplicated principle pool by importance.

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

- **Step-16 GRADE** (v1.1.0): every one of the 69 principles carries a `grade` block (`source_type`
  + up/down factors) derived from real evidence signal — the dominant source's authority and
  distinct-source replication. 28 high principles from canonical texts grade `classic`; 4 high
  multi-source grade `expert-book + [replication]`; 19 high single-source grade
  `expert-book + [corroborated]`; 5 medium from canonical texts grade `classic + [indirectness]`; 13
  medium grade `expert-book`. `validate_confidence_grade` enforces
  `grade_confidence(grade).level == confidence` (0 mismatch).
- **Step-13 ask-gate** (v1.1.0): the opt-in is declared in profile `ask_gate{enabled, slot_source,
  measured_by}` and **measured** by `tests/behaviour-tests.yaml` — 51 missing-context tests (25
  enriched with one specific decision-variable `must_ask_for` slot each) paired with 51 answerable
  twins, scored two-axis (reward the single missing variable, penalise over-asking). `must_ask_for`
  is NOT placed on principles (`principles-v1` forbids it via `additionalProperties:false`); the
  runtime `ask_gate` reads each principle's `applies_when` as the secondary slot source — 51/69
  principles are runtime-ask-capable.

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
- 1.1.0 (2026-06-24): **calibrated 0.25× rebuild** (branch `rebuild/software-architecture-v2`).
  v1.0.0 promoted a stale hand-picked 50-principle spine that bypassed `build_map_reduce --select`;
  this release runs the calibrated pipeline over the **same nine books** (byte-identical cached
  per-book MAP — no re-extraction): 303 per-book principles → reduce/dedup → 51 candidate clusters →
  in-thread precision filter (41 split / 10 confirm) → `select_top(0.25)` of the ~221-group merged
  pool = **69 principles** (the measured best grounding/size tradeoff). 2420 claims, 410 evidence
  records. The authored layer (profile prose, 17 skills, 5 references, faithfulness verdicts) is
  reused from the same-source v1.0.0 sibling and **regrounded** onto this spine — every principle,
  claim, evidence, and source-anchor id remapped to resolve here (0 unresolved); profile `(Pxxx)`
  citations and faithfulness notes remapped by statement similarity. Step-16 GRADE re-derived per the
  note above; Step-13 ask-gate suite regenerated. Per the supersession rule, the 0.1.0–1.0.0
  decisions remain on record; the calibrated spine supersedes the hand-picked one. `agent_version`
  `1.0.0` → `1.1.0`. Adapter re-exported; validate PASS (0 FAIL, 3 WARN benign injection-scan);
  faithfulness valid; quote-scan clean.
- 1.2.0 (2026-06-24): added the Step-7 **C-track principle graph** over the calibrated 0.25× spine —
  `principle-clusters.json` (6 cross-source confirmed clusters), `principle-graph.json` (21 typed
  edges incl. one scoped `conflicts`), `conflict-log.md`. Seeded deterministically
  (`seed_principle_clusters`, MiniLM) then in-thread confirm + edge authoring against `P001–P069`;
  the two no-shared-term cosine over-merges were split into real cross-source concepts and a lexical
  false-merge dropped. `validate_principle_clusters` / `validate_principle_graph` / package validate
  all PASS. Auxiliary; adapter behaviour unchanged. `agent_version` `1.1.0` → `1.2.0`.

## Version History

- **1.3.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.
