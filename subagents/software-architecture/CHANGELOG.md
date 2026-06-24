# Changelog — software-architecture

All notable changes to this generated subagent package are recorded here.

## 1.2.0 — 2026-06-24

- Added the Step-7 **C-track principle graph**: `principles/principle-clusters.json` (6 cross-source
  confirmed clusters — concurrency, coupling, distributed-transactions, architecture-characteristics,
  style-pattern-selection, async-decoupling), `principles/principle-graph.json` (21 typed
  alias/refines/specializes/supports/conflicts edges, including one scoped `conflicts` edge), and the
  rendered `principles/conflict-log.md`. Closes the C-track artifacts the base validate did not require
  but `validate_principle_clusters` / `validate_principle_graph` flagged on absence. Auxiliary —
  adapter behaviour unchanged. `agent_version` `1.1.0` → `1.2.0`.

## 1.1.0 — 2026-06-24

**Calibrated 0.25× rebuild** (branch `rebuild/software-architecture-v2`).

### Changed

- **Spine recalibrated via `build_map_reduce --select 0.25`.** v1.0.0 promoted a hand-picked
  50-principle spine that bypassed the calibrated `--select`. This release runs the calibrated
  pipeline over the **same nine books**, reusing the byte-identical cached per-book MAP (no
  re-extraction): 303 per-book principles → reduce/dedup → 51 candidate clusters → in-thread
  precision filter (41 split / 10 confirm) → `select_top(0.25)` of the ~221-group merged pool =
  **69 principles** (the measured best grounding/size tradeoff). 2420 claims, 410 evidence records.
- **Authored layer regrounded.** Profile prose, 17 skills, 5 references, and the 18 faithfulness
  verdicts are reused from the same-source v1.0.0 sibling and regrounded onto this spine — every
  principle / claim / evidence / source-anchor id remapped to resolve here (0 unresolved); profile
  `(Pxxx)` citations and faithfulness notes remapped by statement similarity.
- **Step-16 GRADE re-derived** for all 69 principles from real evidence signal (dominant-source
  authority + distinct-source replication); `validate_confidence_grade` passes (0 mismatch).
- **Step-13 ask-gate suite regenerated**: 120 golden (69 + 51 answerable twins) + 51 missing-context
  tests, 25 enriched with a specific decision-variable `must_ask_for` slot.
- `agent_version` `1.0.0` → `1.1.0`. Adapter re-exported.

### Notes

- `must_ask_for` is not stored on principles (`principles-v1` forbids it via
  `additionalProperties:false`); the runtime ask-gate uses each principle's `applies_when` as the
  slot source (51/69 runtime-ask-capable).
- `validate_generated_package`: PASS (0 FAIL, 3 WARN = benign Enterprise Integration Patterns
  injection-scan triage hits). quote-scan clean.

## 1.0.0 — 2026-06-24

First stable release of the modernized deep build (promotion in 0.4.0 + the Step-16 and Step-13
feature layers below).

### Added

- **Step-16 GRADE evidence grading.** Every one of the 50 principles carries a `grade` block
  (`source_type` + up/down factors) whose `grade_confidence().level` equals its declared confidence,
  enforced by the `validate_confidence_grade` gate. Evidence-grounded: 10 cross-source-corroborated
  high principles (`P001–P012`, ≥2 sources) → `expert-book + [corroborated]`; 32 single-source high
  principles → `classic`; 8 medium principles → `expert-book`.
- **Step-13 Answer/Ask/Abstain ask-gate** (opt-in `ask_gate` profile capability). The 48
  decision-context-dependent principles carry `must_ask_for` slots (the profile's declared driving
  forces — prioritized characteristics + constraints); the 2 universal-invariant principles
  (`P001`, `P024`) carry none to avoid over-asking. A generated `tests/behaviour-tests.yaml`
  (100 golden incl. 50 answerable twins; 50 missing-context, 48 enriched with the principle's
  specific slots) makes the gate measurable two-axis via `behaviour_replay`.

### Changed

- Refreshed the README, provenance ledger, and profile role/source_of_truth prose from the stale
  7-book / 42-claim / 20-principle era to the deep spine (nine books / 2420 claims / 50 principles /
  17 skills / 5 references).
- `agent_version` `0.4.0` → `1.0.0`. Adapter re-exported; `validate` PASS, faithfulness clean
  (all findings EXACT_SUPPORT/WITHIN_SCOPE), quote-scan clean.

### Note

- The `software-architecture-p0` staging package is retired with this release; its deep spine now
  lives here as canonical.

## 0.4.0 — 2026-06-24

### Changed

- **Promoted the deep `software-architecture-p0` spine to canonical.** The shallow build
  (42 claims / 20 principles) is replaced by the deep map→reduce build over the **same nine
  `distillation-only` books** (identical source hashes): **2420 claims** (`analysis/claims.jsonl`),
  **50 principles** (`principles/principles.yaml`, `P001–P050`), the matching evidence chain
  (`evidence/evidence-records.yaml`), 17 authored skills, 5 references, and the regenerated
  behaviour suite — all faithfulness-clean. Distilled artifacts, provenance ledger, manifest, and
  interrogation records were taken from the p0 build and re-slugged `software-architecture`.
- `sources/markdown` + `sources/{metadata,assets,original}` kept from the canonical package (the
  source bytes are byte-identical between the two builds); `sources/anchors` adopted from p0 to match
  its claim grounding.
- `agent_version` `0.3.0` → `0.4.0`. Adapter re-exported; `validate` PASS.

## 0.3.0 — 2026-06-20

### Added

- **Incremental add-source** (subagent-maintenance flow): two scalability books, both
  `distillation-only` — *Scalable Internet Architectures* (Theo Schlossnagle, 2006) and
  *Scalability Rules: 50 Principles for Scaling Web Sites* (Martin L. Abbott, Michael T. Fisher,
  2011). The package now spans nine sources.
- Evidence chain extended **append-only**: claims `C025–C042` (24 → 42), evidence `E025–E042`
  (24 → 42), principles `P013–P020` (12 → 20), behaviour tests `PB-P013–PB-P020` (12 → 20).
- Eight new scalability principles: scale out over up (P013), AKF Scale Cube decomposition (P014),
  stateless services / no sticky sessions (P015), aggressive caching + computational reuse (P016),
  high-availability ≠ load-balancing (P017), don't-overengineer / D-I-D right-sizing (P018),
  right storage tool / not-everything-in-an-RDBMS (P019), end-to-end observability (P020).
- Five authored skills (`scale-out-and-axis-decomposition`, `stateless-and-caching-for-scale`,
  `availability-and-load-balancing-review`, `economical-scalability-and-tooling`,
  `observability-for-scale-review`) and one authored reference (`akf-scale-cube`).
- New `quality_bar` and `knowledge_partition.always_on` entries for the scalability dimension, with
  matching faithfulness findings.

### Changed

- Strengthened existing principles without dropping any: P001 (trade-off primacy, +C042) and P012
  (relax temporal constraints for scale, +C041). All twelve original principles, their claims, and
  every prior profile decision are preserved.
- `agent_version` `0.2.0` → `0.3.0`. Adapter re-exported; `validate` PASS, faithfulness clean,
  quote-scan clean.

## 0.2.0 — 2026-06-20

### Added

- **Authored every skill and reference body** (`author-skills` / Step 8). All 12 skills
  (`skills/<slug>/SKILL.md`) and 4 references (`references/<slug>.md`) are now authored bodies
  grounded only in this package's principles, claims, evidence, and source anchors — no invention,
  no verbatim quotation (all sources `distillation-only`).
- Stamped the drift baseline (`provenance.authored_from_digest`) into all 16 ready docs via
  `cli stale --stamp` so Step 9 can detect future grounding drift.

### Changed

- Package status promoted `draft` → `ready`. Skill-authoring validator reports all skills and
  references authored (0 stub); quote-scan and faithfulness pass. Adapter re-exported.

## 0.1.0 — 2026-06-20

### Added

- Initial generation of the `software-architecture` (Software Architecture Reviewer) package via
  the `/author-subagent` pipeline.
- **Multi-source authoring** grounded in seven canonical architecture books (all
  `distillation-only`): Fundamentals of Software Architecture; Clean Architecture; Software
  Architecture: The Hard Parts; Patterns of Enterprise Application Architecture; Software
  Architecture Patterns; Designing Event-Driven Systems; Enterprise Integration Patterns.
- Tier-2 evidence chain: 24 source-anchored claims (`analysis/claims.jsonl`), 24 evidence records
  (`evidence/evidence-records.yaml`), 12 operational principles (`principles/principles.yaml`),
  12 principle-behaviour tests (`tests/principle-behaviour-tests.yaml`), and a faithfulness report
  (`reports/faithfulness-report.yaml`).
- `profile.yaml` with three evidence-backed modes (review, advise, compare), golden tests, and the
  provenance ledger.

### Status

- Package status: `draft`. Skill and reference bodies are scaffolded as stubs and not yet authored;
  re-run with `--author-skills` to author the bodies and promote to `ready`.
