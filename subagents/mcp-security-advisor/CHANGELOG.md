# Changelog — mcp-security-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.0] — 2026-07-05

### Added

- Initial LLM-authored layer over the deterministic map→reduce distilled spine (25 MCP-security
  sources — the MCP specification, OWASP MCP Top 10 and cheat sheets, NSA CSI, CoSAI, OAuth-for-MCP
  practitioner and vendor writing, and MCP security research; 1352 claims, 220 principles, 106
  high-confidence).
- `profile.yaml` — role, scope, three modes (review / advise / compare), quality bar, forbidden
  behaviours, handoff rules, and a knowledge partition of eleven skills + two references mapped to
  all 220 principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength check; every load-bearing rule is
  `WITHIN_SCOPE` of its evidence.
- Eleven skills, two references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle).

### Fixed

- Source metadata `source_type` (`md` → `markdown`) across all 25 metadata files.
- One claim and one evidence record `evidence_type` (`hypothetical_instance` → `case`) to conform
  to the claims/evidence schema enums.
