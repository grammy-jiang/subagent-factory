# Changelog — research-career-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.0] — 2026-07-25

### Changed
- Re-authored all 8 skill bodies to the GOLD shape: added a trigger-oriented `description:`
  frontmatter field to each (progressive-disclosure routing signal), rewrote every
  "Anti-patterns to flag" bullet as a complete, standalone observable-failure-symptom sentence
  (one per provenance principle — replacing character-truncated substrings), and expanded the
  bare one-line Procedure steps to carry their concrete criteria. `provenance:` blocks (and
  `authored_from_digest`) preserved verbatim.
- `evaluation-metrics-and-research-judgment` and `writing-and-publishing-scientific-work`:
  restored the anti-pattern bullet for the previously-dropped principle (P038 and P046).
- `profile.yaml`: weakened `quality_bar[2]` to restore P010's tie-break hedge (established
  reputation used only when protection factors are comparable — was flattened to "not prestige");
  shortened the `role` closing to a pointer to remove ~40 words duplicating `forbidden_behaviours`;
  narrowed `when_to_use[3]` to the strategy slice this advisor owns and added a `when_not_to_use`
  handoff pointer to `research-writing-advisor` for craft-level writing.

### Added
- `profile.yaml` `router_description:` (≤320 chars) covering all five `when_to_use` domains plus the
  core advice-only exclusion, so the exported adapter description no longer under-covers scope.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-career-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (48 principles
  P001-P048 / 611 claims from four distillation-only sources).
- `profile.yaml` derived from the 48 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  8-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 8 authored skills partitioning all 48 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (7 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 48 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Four distillation-only sources: *A PhD Is Not Enough! A Guide to Survival in Science* (Peter J.
  Feibelman, 2011); *The Art of Doing Science and Engineering* / *You and Your Research* (Richard W.
  Hamming, 1997); a Chinese guide to succeeding in academic research; and *Empirical Methods for
  Artificial Intelligence* (Paul R. Cohen, 1995).
