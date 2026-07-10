# Changelog — deception-detection-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-11

### Added
- Initial release of the **deception-detection-reviewer** subagent (Tier 1).
- `profile.yaml` derived from the 94 promoted principles (P001–P094): role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and an
  eight-skill / two-reference `knowledge_partition` covering all principles exactly once.
- Eight authored skills: turning-and-running-a-controlled-agent, building-and-feeding-the-deception,
  network-security-and-compartmentation, assessing-enemy-trust-and-belief,
  governance-approval-and-organization, strategic-stewardship-and-timing,
  physical-and-technical-deception-craft, counter-deception-and-the-mirror.
- Two references: deception-detection-principles-index, deception-detection-evidence-notes.
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded EXACT_SUPPORT or
  WITHIN_SCOPE against its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (5 golden, 2 negative-routing, 2 missing-context) and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle, 94 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- One distillation-only source: J. C. Masterman, *The Double-Cross System* (1972) — the official
  history of Britain's WWII double-agent operations run by the Twenty (XX) Committee. Spine: 303
  atomic claims, 303 evidence records, 21 chunk anchors.
