# Changelog — ux-design-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.2.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.2.0] — 2026-07-03

### Changed

- Re-synced the LLM-authored layer to a rebuilt map→reduce distilled spine, which renumbered
  principles from 70 to 85 (15 new IA / navigation / research / strategy principles) and appended
  242 claims (1711 total; existing claim IDs preserved). Applied a statement-preserving principle-ID
  remap across `profile.yaml`, all seven skills, both references, the faithfulness report, and both
  test suites so every citation resolves to the correct current principle.
- `knowledge_partition.always_on` now covers all 85 principles (added P021, P024, P025, P029, P054,
  P076–P085 to their topical groups).
- `tests/principle-behaviour-tests.yaml` — added one behaviour test per new principle (85 total), so
  every principle is exercised by a test that references it.
- Re-stamped skill / reference drift baselines to the current grounding and re-exported the Claude
  Code adapter so its must-hold operating-invariant layer covers the current high-confidence
  principles.

### Fixed

- Reverted the rebuild's regression of the eight source metadata records' `source_type`
  (`md` → `markdown`) so source-metadata schema validation passes; source content is unchanged.

## [0.1.0] — 2026-07-03

### Added

- Authored the LLM layer over the deterministic map→reduce distilled spine (1469 claims, 540
  evidence records, 70 principles / 28 high-confidence, chunk anchors).
- `profile.yaml` — UX-design advisor role, when-to-use / when-not-to-use, three modes
  (review / advise / compare), five evidence-citing quality-bar checks, forbidden behaviours,
  handoff and source-of-truth policy, and a seven-group `knowledge_partition.always_on` covering all
  70 principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength findings; no profile rule is stronger
  than its principle evidence.
- Seven skills grounded in their principles, claims, evidence, and source anchors:
  `information-architecture-foundations`, `navigation-search-and-findability`,
  `usability-and-self-evident-design`, `usability-testing-and-evaluation`, `user-research-methods`,
  `conversational-and-chatbot-design`, `ia-strategy-and-deliverables`.
- Two references: `references/ux-design-principles-index.md` (all 70 principles grouped by skill) and
  `references/conversational-ux-evidence-notes.md` (conversational/chatbot practices and their
  user-outcome evidence base).
- `tests/principle-behaviour-tests.yaml` (one behaviour test per principle) and
  `tests/golden-tests.yaml` (routing + negative-routing golden tests).

### Fixed

- Corrected the seven source metadata records' `source_type` from the invalid `md` to `markdown`
  (schema enum) so the source-metadata validation passes; source content is unchanged.
