# Changelog — mcp-protocol-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.1] — 2026-07-05

### Added

- Authoritative-answer mode: bundled the verbatim MCP specification (24 pages, version 2025-11-25)
  under `references/mcp-spec-2025-11-25/` with a section index (`README.md`) and `NOTICE.md`
  (Apache-2.0 / CC-BY-4.0 attribution), plus 3 reference server examples under
  `references/mcp-examples/`. Extended `source_of_truth_policy.precedence` to direct the advisor to
  Read the original spec section and cite it for exact protocol requirements (MUST/SHOULD wording,
  message shapes, error codes, capability contracts).

### Fixed

- Corrected source `rights_status` to `open` for the MCP specification sources (Apache-2.0 /
  CC-BY-4.0), clearing spurious quote-scan rights warnings on the bundled verbatim text.

## [0.1.0] — 2026-07-05

### Added

- Initial LLM-authored layer over the deterministic map→reduce distilled spine (the Model Context
  Protocol specification, revisions 2024-11-05 through 2025-11-25; 632 claims,
  253 principles, 220 high-confidence).
- `profile.yaml` — role, scope, three modes (review / advise / compare), quality bar, forbidden
  behaviours, handoff rules, and a knowledge partition of 13 skills +
  2 references mapped to all 253 principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength check; every load-bearing rule is
  `WITHIN_SCOPE` of its evidence.
- 13 skills, 2 references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle).
- Fixed source metadata `source_type` (`md` → `markdown`).
