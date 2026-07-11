# Changelog — descriptive-translation-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.0] — 2026-07-12

Review-loop round 1 (`reports/review-loop/descriptive-translation-reviewer.r1.review.md`): applied
all must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **Adapter invariant layer truncation** — the installed/canonical adapter had 101 `…`-severed
  invariant lines and a mid-clause frontmatter `description`. Re-exported through the current
  `compile_invariants`/`export_claude_agent` path so each invariant renders its full principle
  sentence and the routing description ends at a clause boundary.
- **Skill bodies re-authored to the GOLD shape** — all 12 `skills/*/SKILL.md` rewritten so every
  Procedure and Anti-patterns bullet is a complete, self-contained sentence before its `(Pxxx)` cite
  (removing the mid-clause truncations such as "Surface a translation's (P113)."), Anti-patterns now
  cover every principle in the skill (not a silent 7-item cap) as concrete bad-finding symptoms, and
  each gains a `description:` frontmatter field for routing. Frontmatter provenance preserved.
- **Faithfulness re-grounding** — `handoff_rules[0]` re-anchored to P029 (publisher holds the publish
  decision) + P070 (macro/micro split), dropping the mis-grounded P009/P162/P080; `handoff_rules[1]`
  re-anchored to P029 for commercial/economic constraints. `faithfulness-report.yaml` gains entries
  for `handoff_rules[0..2]` and `canonical_owner`.
- **Cross-sibling routing** — `when_not_to_use` + `handoff_rules` now name `translation-equivalence-advisor`,
  `translation-quality-reviewer`, and `technical-translation-advisor` by slug/axis; `when_to_use[0]`
  differentiated from the quality-reviewer sibling.
- **Faithfulness weakening** — P047 no longer states Blum-Kulka's explicitation hypothesis as
  "confirmed by corpus study" (now a proposed, contested tendency with varying support); P115 frames
  the technical-texts-easier point as Ortega's comparative observation and marks technical/scientific
  subject-matter risk out of remit.

### Changed
- `tier: 1` → `tier: 2` (3-source manifest; matches siblings and the build record).
- Profile body trimmed (removed quality_bar/forbidden redundancy) toward the word budget.
- `agent_version` 1.0.0 → 1.1.0.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **descriptive-translation-reviewer** subagent (Tier 1), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles P001-P180 /
  984 claims from three distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, when/when-not-to-use, three modes
  (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 180 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 180 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: Jeremy Munday, *Introducing Translation Studies* (2016);
  Lawrence Venuti, ed., *The Translation Studies Reader* (2012); Gideon Toury, *The Nature and Role
  of Norms in Translation* (1995).
