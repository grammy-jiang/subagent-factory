# Changelog — research-integrity-reproducibility-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [1.1.0] — 2026-07-25

### Changed
- Re-authored all 7 skill bodies to the gold shape: fixed Procedure steps that were truncated
  mid-clause, added a `description:` frontmatter line to each skill (the Agent-Skills triggering
  signal), and rewrote each `## Anti-patterns to flag` section as concrete, observable red-flag
  symptoms rather than restatements of the principles. Frontmatter `provenance` blocks preserved
  verbatim; no principle statement changed, so the distilled spine and adapter invariants are
  unaltered.
- Broadened P027's `applies_when` to match its own general statement (documenting/storing/depositing/
  sharing a dataset, in addition to reusing others' data) — resolves the SCOPE_BROADENED candidate in
  `always_on[0]`.
- Flipped P020 and P026 `operational_mapping.profile_rule` to `true` to match their use in
  `knowledge_partition.always_on`.

### Added
- A third worked example exercising `plan` mode (reproducibility + open-release setup for a new
  data-science project).
- A `when_to_use` trigger for contributing to an existing open research project (grounded in P024).
- Faithfulness report coverage for all 7 `knowledge_partition.always_on` skill bullets, with
  per-rule comparison notes replacing the prior templated note; ledger now records the PASS outcome.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-integrity-reproducibility-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (34 principles
  P001-P034 / 753 claims from three distillation-only sources).
- `profile.yaml` derived from the 34 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  7-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 7 authored skills partitioning all 34 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 34 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: *The Turing Way: A Handbook for Reproducible, Ethical and
  Collaborative Research* (The Turing Way Community, 2022); *On Being a Scientist: A Guide to
  Responsible Conduct in Research*, 3rd ed. (National Academies, 2009); and a higher-education
  academic-norms guide.
