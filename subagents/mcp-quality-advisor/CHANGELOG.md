# Changelog — mcp-quality-advisor

All notable changes to this generated subagent package are documented here.

## [0.2.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains and every sibling hand-off. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## 0.2.0 — 2026-07-25

### Changed
- Folded in a 30th source (`new-rules-of-context-engineering-claude-5`); the map→reduce build
  re-clustered and renumbered the distilled spine (30 sources → 1510 claims → 200 principles).
- Regenerated the whole LLM-authored layer against the renumbered principles so every `[Pxxx]`
  citation resolves to its current principle:
  - 5 skills + 3 references re-authored and re-partitioned over the current 200 principles
    (principles-only provenance; digests re-stamped).
  - `tests/principle-behaviour-tests.yaml` (200, per-principle) + `tests/golden-tests.yaml`
    regenerated from current statements; `principle_coverage` ids remapped.
  - `profile.yaml` quality-bar / forbidden-behaviour citations remapped to current ids; `sources[]`
    extended to 30; source-count prose updated.
- Fixed the new source's metadata `source_type`/`file_type` `md` → `markdown`.
- Re-exported the adapter with its must-hold operating-invariant layer intact: 137 invariants,
  46,965 bytes (0.1.0 shipped 127).

### Fixed

- Kept `attach_invariants: true`. The authoring run had set it to `false` — which drops the whole
  `## Operating invariants (must hold)` section from the adapter (8,238 bytes, 0 invariants) — as
  the only way to get `validate` green: must-hold principle P167 legitimately reads "…leaving TODO
  rows for ambiguity…", and `validate_adapter_quality`'s `\bTODO\b` stub-token guard fired on the
  compiled invariant line. Validation passed in that state, so the loss was silent. Root-caused and
  fixed in the factory instead: `tools/subagent_factory/validate_adapter_quality.py` now skips the
  machine-compiled `- **[Pxxx]** …` lines when scanning for stub tokens, since they are rendered
  verbatim from an already-validated spine rather than authored profile prose. Guarded by two
  regression tests in `tests/subagent_factory/test_validate_adapter_quality.py`.

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
