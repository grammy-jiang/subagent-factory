# Changelog — technical-translation-advisor

All notable changes to this generated subagent package.

## 1.0.0 — 2026-07-11

### Added
- Initial LLM-authored layer over the deterministically-valid distilled spine (150 principles from 2 distillation-only sources by Jody Byrne).
- `profile.yaml` (tier 2, advice-only) with role, when-to-use/not, three modes (advise/review/compare), quality bar, forbidden behaviours, handoff rules, and a 10-skill / 2-reference knowledge partition — every rule grounded in cited principle ids.
- `reports/faithfulness-report.yaml`: every load-bearing profile rule graded against the principles/claims (EXACT_SUPPORT or deliberate WITHIN_SCOPE narrowing; no over-claim).
- 10 authored skills and 2 references, each with resolving principle/claim/evidence provenance.
- `tests/`: golden tests (6 positive, 3 negative-routing, 2 missing-context) and principle-behaviour tests covering all 150 principles.
- Claude Code adapter exported and installed.
