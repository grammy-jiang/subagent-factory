# Changelog — Agent Skills Advisor

All notable changes to this subagent are documented here.

## [0.1.0] — 2026-07-04

Initial authored release. The distilled spine (claims, evidence records, principles,
anchors, source pack) was assembled by the map→reduce build; this release adds the
LLM-authored layer on top of it and takes the package to `status: ready`, `tier: 2`.

### Added

- `profile.yaml` (portable-profile-v1, tier 2, status ready) with a platform-neutral
  role, five caller-observable triggers, three read-only advisory modes
  (advise / review / eval-guide), a principle-cited quality bar, forbidden behaviours,
  handoff rules, and a source-of-truth policy — all grounded in the package principles
  (P001–P150) and listing all 57 ingested `sources[]`.
- Four skills — `authoring-agent-skills`, `evaluating-and-iterating-on-skills`,
  `deploying-skills-across-platforms`, `orchestrating-subagents-and-mcp`.
- Three references — `skill-format-and-frontmatter-reference`,
  `platform-customization-matrix`, `context-and-harness-engineering-reference`.
- `reports/faithfulness-report.yaml` grading each gradable profile rule against the
  package evidence and principles (no rule exceeds its evidence).
- `tests/golden-tests.yaml` (positive / negative-routing / missing-context) and
  `tests/principle-behaviour-tests.yaml` covering every high-confidence principle
  (126 of the 150).
- `tests/test-results.md` from the Phase 8 self-check gate.
- `provenance-ledger.md` and this changelog.

### Fixed

- Corrected source metadata `source_type` from the invalid `md` to the schema value
  `markdown` for all 57 ingested sources (a defect the map→reduce rebuild had
  introduced; the same fix is recorded in sibling packages built the same way).

### Changed

- Exported the Claude Code runtime adapter and installed it under
  `.claude/agents/generated/`.
- Set `agent_version` to `0.1.0`.

### Sources

- 57 primary and secondary sources on Agent Skills, subagents, MCP, evaluation,
  context engineering, and instruction files, spanning the Claude (Code + API),
  OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard.

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was not modified.
