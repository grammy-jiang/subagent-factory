# Changelog — application-security-reviewer

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.0] — 2026-07-03

### Added

- Initial LLM-authored layer over the deterministic map→reduce distilled spine (2 sources —
  *Web Application Security* (Hoffman, 2020) and *Securing the API Stronghold* (Nordic APIs, 2015);
  501 claims, 50 principles, 25
  high-confidence).
- `profile.yaml` — role, scope, three modes (review / advise / compare), quality bar, forbidden
  behaviours, handoff rules, and a knowledge partition of seven skills + two references mapped to
  all 50 principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength check; every load-bearing rule is
  `WITHIN_SCOPE` of its evidence.
- Seven skills, two references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle).
- Fixed source metadata `source_type` (`md` → `markdown`) and enriched source titles/authors/years.
