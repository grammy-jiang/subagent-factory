# Changelog — mcp-quality-advisor

All notable changes to this generated subagent package are documented here.

## 0.1.0 — 2026-07-05

### Added
- Initial release of the MCP Quality Advisor package.
- Distilled spine (map→reduce): 29 sources → 1475 claims → 837 evidence records → 200 principles.
- Authored layer derived from the spine:
  - `profile.yaml` (role, scope, quality bar, forbidden behaviours, three modes, 5 skills, 3 references).
  - 5 skills: `designing-mcp-tool-descriptions`, `scaling-tool-discovery-and-context`,
    `verifying-mcp-protocol-compliance`, `evaluating-mcp-agents-and-judges`, `operating-mcp-on-serverless`.
  - 3 references: `mcp-protocol-compliance-checklist`, `tool-description-quality-rubric`,
    `mcp-evaluation-and-judge-reference`.
  - `tests/principle-behaviour-tests.yaml` (per-principle coverage) + `tests/golden-tests.yaml`.
  - `reports/faithfulness-report.yaml` (every gradable profile rule graded; no over-claim).
- Fixed source metadata `source_type`/`file_type` `md` → `markdown` to satisfy the metadata schema.
