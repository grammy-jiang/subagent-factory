# Changelog — requirements-use-case-advisor

All notable changes to this generated subagent package are recorded here.
Versioning tracks `agent_version` in `profile.yaml`.

## [0.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.1.0] — 2026-06-28

Initial release of the authored layer over the per-book map → reduce distilled
spine.

### Added
- `profile.yaml` — portable-profile-v1, Tier 2, `status: ready`. Role: advise and
  review requirements capture via use cases and user stories. Four advisory modes
  (review, advise, validate, draft); 5 quality-bar checks; 5 forbidden behaviours;
  examples including one failure-recovery case.
- Six skills: `scope-and-goal-leveling`, `write-use-case-scenarios`,
  `author-and-split-user-stories`, `run-requirements-elicitation`,
  `estimate-and-plan-stories`, `choose-requirements-artifact`.
- Four references: `use-case-template-and-precision-guide`,
  `goal-levels-and-scope-reference`, `extension-and-failure-checklist`,
  `story-quality-invest-checklist`.
- `tests/golden-tests.yaml` (4 golden, 2 negative routing, 1 missing-context) and
  `tests/principle-behaviour-tests.yaml` (90 tests, one per principle).
- `reports/faithfulness-report.yaml` — 24 findings, all WITHIN_SCOPE / EXACT_SUPPORT.
- Reconstructed deterministic `source-pack.manifest.yaml` and
  `sources/metadata/*.metadata.json` for the three sources (Cockburn 2001,
  Cohn 2004, Jacobson et al. 2011).
- Claude Code adapter exported to `adapters/claude-code/` and installed.

### Notes
- Distilled spine (claims, principles, evidence, anchors) was produced by the
  map → reduce build and is unchanged by this release.
- All three sources are `distillation-only`; no verbatim quotation appears in any
  generated artifact.
