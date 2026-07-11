# Changelog — scalability-mr

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.1] — 2026-06-22

### Fixed

- Behaviour-test coverage: the distilled spine was re-expanded from 50 to 95 principles (67
  high-confidence) after the authored layer was first generated, leaving 25 high-confidence
  principles (P051, P062–P080, P088–P092) without a referencing test. Added 25 `PB-<pid>` entries to
  `tests/principle-behaviour-tests.yaml`, each grounded in the principle's statement/`applies_when`.
- Re-exported the adapter so its invariant layer covers the full must-hold principle set (was stale,
  missing the same 25 principles).

## [0.1.0] — 2026-06-21

### Added

- Initial authored layer over the deterministic map→reduce distilled spine (524 claims, 50
  principles, evidence records, and chunk/paragraph anchors).
- `profile.yaml` — scalability reviewer/advisor role derived from the 50 principles, with
  `when_to_use`/`when_not_to_use`, three modes (review/advise/compare), quality bar, forbidden
  behaviours, and knowledge partition; `tier: 2`, `status: ready`.
- `reports/faithfulness-report.yaml` — per-rule claim-strength review of every load-bearing profile
  rule against the principles/claims/evidence; no rule stronger than its evidence.
- Eight skills under `skills/` and three references under `references/`, each grounded in a cluster
  of principles and their backing claims/evidence/anchors.
- `tests/principle-behaviour-tests.yaml` (one behaviour test per principle), `tests/golden-tests.yaml`
  (positive/negative/missing-context routing), and `tests/test-results.md`.
- Claude Code adapter exported to `adapters/claude-code/scalability-mr.md` and installed at
  `.claude/agents/generated/scalability-mr.md`.

### Sources

- Scalability Rules: 50 Principles for Scaling Web Sites — Martin L. Abbott, Michael T. Fisher
  (2011), `distillation-only`.
- Scalable Internet Architectures — Theo Schlossnagle (2006), `distillation-only`.
