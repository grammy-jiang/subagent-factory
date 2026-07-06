# Changelog — harness-engineering-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.0] — 2026-07-06

### Added

- Initial release of the harness-engineering-advisor package. Advises and reviews the engineering of
  AI-agent runtime harnesses — tools, memory, verification, context/cost budgets, observability,
  supply-chain trust, runtime governance, and evaluation as one governed system.
- Distilled spine (map→reduce): 265 atomic claims, 265 evidence records, and 75 promoted principles
  across two distillation-only sources — a harness-engineering literature synthesis and a
  local-coding-agent engineering guide.
- Authored layer derived from the principles: `profile.yaml` (tier 2, review/advise/compare modes),
  `reports/faithfulness-report.yaml`, nine skills partitioning the principles by harness layer, two
  references (principles index + evidence notes), and behaviour tests (`golden-tests.yaml` plus
  `principle-behaviour-tests.yaml` covering every principle).
- Claude Code adapter exported to `adapters/claude-code/` and installed under `.claude/agents/generated/`.
