# Changelog — mcp-security-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.2] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.1.1] — 2026-07-05

### Added

- Authoritative-answer mode: bundled 7 verbatim, open-licensed security standards (spec authorization + security-best-practices, OWASP MCP Top-10 + cheatsheets, NSA CSI, CoSAI) under
  `references/mcp-security-standards/` with a section index (`README.md`) and `NOTICE.md` attribution.
  Extended `source_of_truth_policy.precedence` to Read and cite the original text for exact
  requirements. Distillation-only sources (arXiv, vendor blogs) are not bundled.

### Fixed

- Set `rights_status: open` on the bundled open sources, clearing quote-scan rights warnings.

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
