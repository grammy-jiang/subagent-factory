# Changelog — microservice-patterns-advisor

All notable changes to this generated subagent package are documented here.
This package is the canonical source of truth; the installed Claude Code adapter
is a derived artifact and must be re-exported after any profile change.

## [0.6.0] — 2026-07-11

### Changed

- Re-grounded the entire LLM-authored layer onto the rebuilt map→reduce distilled
  spine (510 claims `C00001`–`C00510`, 149 principles `P001`–`P149`), which replaced
  the prior 57-claim / 16-principle numbering the authored layer was written against.
  - **profile.yaml** — corrected `sources[]` `source_id` + `sha256` to the ingested
    metadata (`microservicepatternl-a51cf685`, `chris-richardson-mic-19016f24`), and
    remapped every inline principle citation in `quality_bar`,
    `forbidden_behaviours`, `knowledge_partition.always_on`, and `examples` to the
    current principle ids.
  - **skills/ + references/** — re-authored all 8 skill bodies and 4 reference bodies
    against the current principles → claims, with correct `provenance` frontmatter and
    inline citations; dropped the stale `authored_from_digest` stamps (re-stamped on
    release). `validate_skill_authoring` clean (8/8 skills, 4/4 references).
  - **reports/faithfulness-report.yaml** — refreshed each finding's backing claim ids
    to the current spine (verdicts unchanged — no rule is stronger than its evidence).
  - **tests/** — regenerated `behaviour-tests.yaml` (193 tests carrying per-principle
    `principle_coverage`) and `principle-behaviour-tests.yaml` (149 tests, one
    `principle_id` per principle) so every high-confidence principle is covered.
- Re-exported the adapter (invariant layer recompiled from the 149 principles).
- Bumped `agent_version` 0.5.0 → 0.6.0.

## [0.5.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.4.0 → 0.5.0.

## [0.4.0] — 2026-06-11

### Added
- Authored all 8 skill bodies and 4 reference bodies from the package's own
  principles → claims → evidence (`authored-doc-v1`, `status: ready`, real
  provenance IDs): skills `pattern-selection-walkthrough`,
  `service-decomposition-advice`, `saga-transaction-design`,
  `cross-service-query-design`, `interservice-communication-selection`,
  `external-api-design`, `microservice-testing-strategy`,
  `production-readiness-review`; references `microservice-pattern-language-map`,
  `pattern-forces-and-tradeoffs-table`, `saga-countermeasures-checklist`,
  `deployment-options-comparison`.

### Changed
- Promoted package `status: draft → ready`; stamped the drift baseline
  (`authored_from_digest`) on every authored body.
- `validate_skill_authoring` clean (8/8 skills, 4/4 references), quote-scan PASS
  (no verbatim; `distillation-only`).
- Bumped `agent_version` 0.3.0 → 0.4.0 and re-exported the adapter.

## [0.3.0] — 2026-06-11

### Added
- Second source on the same slug: the full book *Microservices Patterns: With
  examples in Java* (Chris Richardson, Manning, 2018), source_id
  `chris-richardson-mic-20260611091020`, `distillation-only`.
- Tier-2 evidence chain derived from the book: `analysis/claims.jsonl` (57
  atomic claims), `evidence/evidence-records.yaml` (57 records),
  `principles/principles.yaml` (16 principles), and
  `tests/principle-behaviour-tests.yaml` (15 behaviour tests, one per
  high-confidence principle).
- Expanded `knowledge_partition` from 1 skill + 1 reference to **8 skills + 4
  references**: skills `service-decomposition-advice`, `saga-transaction-design`,
  `cross-service-query-design`, `interservice-communication-selection`,
  `external-api-design`, `microservice-testing-strategy`,
  `production-readiness-review` (joining `pattern-selection-walkthrough`);
  references `pattern-forces-and-tradeoffs-table`, `saga-countermeasures-checklist`,
  `deployment-options-comparison` (joining `microservice-pattern-language-map`).

### Changed
- Set `tier: 0 → 2` and re-derived the profile from the evidence chain: richer
  `when_to_use`, `modes`, `quality_bar`, `forbidden_behaviours`, and `always_on`,
  with principle IDs (P001–P016) cited inline so each rule traces to an
  evidence-backed claim.
- Bumped `agent_version` 0.2.0 → 0.3.0.

### Status
- Returned to `status: draft` during re-derivation; promoted to `ready` once the
  new skill/reference bodies are authored (see 0.3.0 promotion below).

## [0.2.0] — 2026-06-11

### Added
- Authored the skill body `pattern-selection-walkthrough` (the repeatable
  concern → group → candidate-patterns → forces-weighted recommendation
  procedure behind the `advise` / `compare` modes).
- Authored the reference body `microservice-pattern-language-map` (the full
  grouped pattern catalogue with a concern → group index).

### Changed
- Promoted package `status: draft → ready`; both authored bodies are
  `status: ready` (`authored-doc-v1`). Tier 0 grounding (profile `always_on` +
  `when_to_use` + source), so provenance principle/claim arrays are empty.
- Bumped `agent_version` 0.1.0 → 0.2.0 and re-exported the adapter.

## [0.1.0] — 2026-06-09

### Added
- Initial profile derived from the Microservice Pattern Language map
  (Chris Richardson, 2020, `distillation-only`), source_id
  `microservicepatternl-20260608230325`.
- Role: Microservice Patterns Advisor — maps an architecture concern onto the
  microservices pattern language and explains candidate patterns, their forces,
  and trade-offs.
- Modes: `advise` (recommend applicable patterns) and `compare` (contrast
  alternative patterns addressing the same concern).
- Golden tests: positive routing for `advise` and `compare`, one negative
  routing test (product/technology selection is out of scope), and one
  missing-context test.
- Scaffolded skill stub `pattern-selection-walkthrough` and reference stub
  `microservice-pattern-language-map` (both `status: draft`, not yet authored).

### Status
- Package `status: draft` until the skill and reference are authored.
