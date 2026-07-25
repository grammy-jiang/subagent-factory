# Changelog — Agent Skills Advisor

All notable changes to this subagent are documented here.

## [0.3.0] — 2026-07-25

Fold-in of a 59th source — Anthropic's official *skill-creator* SKILL.md (the authoring loop:
capture intent, interview, draft, evaluate, iterate; the skill-writing guide; the description
optimizer) — into the distilled spine. The map->reduce rebuild re-clustered and renumbered the
principles (P001-P150), so the LLM-authored layer was regenerated to match — no rule
stronger than its evidence, every cited id resolves into the current spine.

### Changed

- Re-grounded the LLM-authored layer against the rebuilt spine (150 principles,
  126 high-confidence, 2059 claims): all four skills, three references,
  `reports/faithfulness-report.yaml`, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle) now cite the current
  principle ids; skill/reference frontmatter `authored_from_digest` re-stamped from the current
  grounding.
- `profile.yaml` refreshed: `quality_bar` / `forbidden_behaviours` / `outputs` /
  `source_of_truth_policy` citations remapped to the current spine, the 59th source
  (*skill-creator-skill*) added to `sources[]`, the source-count prose updated, and `agent_version`
  bumped to 0.3.0.
- Re-exported the Claude Code adapter and reinstalled it under `.claude/agents/generated/`.

### Fixed

- Source metadata `source_type` corrected from the invalid `md` to the schema value `markdown` for
  all ingested sources (the map->reduce rebuild reintroduced the defect; the same fix was applied at
  0.2.0).

### Sources

- 59 primary and secondary distillation-only sources on Agent Skills, subagents, MCP, evaluation,
  context engineering, and instruction files, spanning the Claude (Code + API), OpenAI Codex, and
  GitHub Copilot surfaces and the open Agent Skills standard.

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was assembled by the map->reduce build and is not
  edited by this release.

## [0.2.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.2.0] — 2026-07-25

Fold-in of a 58th source, *new-rules-of-context-engineering-claude-5*, into the distilled spine.
The map->reduce rebuild re-clustered and renumbered the principles (P001-P150), so the
LLM-authored layer was regenerated to match — no rule stronger than its evidence, every cited id
resolves into the current spine.

### Changed

- Re-grounded the LLM-authored layer against the rebuilt spine (150 principles,
  130 high-confidence, 2011 claims): all four skills, three references,
  `reports/faithfulness-report.yaml`, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle) now cite the current
  principle ids; skill/reference frontmatter `authored_from_digest` re-stamped from the current
  grounding.
- `profile.yaml` refreshed: `quality_bar` / `forbidden_behaviours` / `source_of_truth_policy`
  citations remapped to the current spine, the 58th source added to `sources[]`, the source count
  updated, and `agent_version` bumped to 0.2.0.
- Re-exported the Claude Code adapter and reinstalled it under `.claude/agents/generated/`.

### Fixed

- Source metadata `source_type` corrected from the invalid `md` to the schema value `markdown` for
  all 58 ingested sources (the map->reduce rebuild reintroduced the defect; the same fix was applied
  at 0.1.0).

### Sources

- 58 primary and secondary distillation-only sources on Agent Skills, subagents, MCP, evaluation,
  context engineering, and instruction files, spanning the Claude (Code + API), OpenAI Codex, and
  GitHub Copilot surfaces and the open Agent Skills standard.

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was not modified by this release.

## [0.1.1] — 2026-07-04

PR #52 Copilot review fixes; no behavioural change.

### Fixed

- Citation format: `[P119 via profile]`, `[P102 via profile]`, `[P066 via profile]`
  standardized to plain `[P###]`; P119 (`authoring-agent-skills`) and P066
  (`context-and-harness-engineering-reference`) now declared in their artifact's
  frontmatter grounding (P102 was already declared; P119/P066 were already
  footer-listed or evidence-backed — declaration only, no new claims).
- `tests/test-results.md` table cells no longer truncate mid-word: the Phase 8
  self-check generator (`profile_self_check.py`) now appends an explicit ellipsis;
  report regenerated.
- `campaign/agent-skills-advisor.sources` comment typo: Claude/Codex/Codex →
  Claude/Codex/Copilot.

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
