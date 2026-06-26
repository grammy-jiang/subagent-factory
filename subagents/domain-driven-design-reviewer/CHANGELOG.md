# Changelog — Domain-Driven Design Reviewer

All notable changes to this subagent are documented here.

## [0.5.0] — 2026-06-27

### Changed

- **Re-source supersession: Domain-Driven Design Quickly → full Eric Evans text.**
  The distilled spine (claims, evidence, principles, chunk anchors) was rebuilt by the
  per-book map→reduce pipeline from the full text of Eric Evans, *Domain-Driven Design:
  Tackling Complexity in the Heart of Software* (Addison-Wesley, 2003), source_id
  `ddd-evans-full-9e0c1e6c` (500 claims, 259 evidence records, 50 principles). This
  supersedes the condensed summary *Domain-Driven Design Quickly* (source_id
  `domaindrivendesignqu-20260612231910`) as the canonical source.
- Synced `source-pack.manifest.yaml` + added `sources/metadata/ddd-evans-full-9e0c1e6c.metadata.json`
  for the new source; removed the superseded summary's orphaned markdown/metadata/anchors.
- Regenerated the LLM-authored layer to match the new 50-principle scheme:
  - `profile.yaml` rule citations remapped from the old P001–P013 numbering to the current
    P001–P050 principle IDs; `sources[]` updated to the full-Evans source; structure
    (rule counts, mode names) preserved.
  - Re-grounded all 6 skill and 4 reference bodies onto current principles/claims/evidence/
    chunk anchors (provenance frontmatter + footers; drift baseline re-stamped). The timeless
    DDD prose was retained; only the citations and source attribution were updated.
  - Regenerated `reports/faithfulness-report.yaml` (22 findings) against the new evidence and
    real chunk anchors; no rule graded stronger than its source, no CONTRADICTED findings.
  - Regenerated behaviour tests: `tests/behaviour-tests.yaml` (150 golden/negative-routing/
    missing-context) and `tests/principle-behaviour-tests.yaml` (one test per principle), so
    every high-confidence principle is exercised.
- Re-exported the Claude Code adapter (invariant layer refreshed to the new principles).
- Bumped `agent_version` 0.4.1 → 0.5.0. Package validates with 0 failures / 0 warnings.

### Notes

- Rights unchanged: `distillation-only` — the copyrighted full text is withheld from the
  package (`sources/markdown` is empty by policy); all content is paraphrase.
- `analysis/claim-importance-scores.yaml` and `interrogation-records.yaml` remain from the
  prior interrogation build; they are not consumed by the validator and were left as-is.

## [0.4.1] — 2026-06-26

### Fixed

- Populated the previously empty `sha256` for source
  `domaindrivendesignqu-20260612231910` in `profile.yaml` (verified to match the
  source-pack manifest and the original PDF), clearing the `source-provenance`
  validation warning.

### Changed

- Re-validated and re-exported the Claude Code adapter under the refactored
  factory tooling. No behavioural change to principles, profile rules, skills,
  or references.

## [0.4.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase, no verbatim quotation). Rendered into the adapter's `## Worked examples` section on re-export.

### Changed

- Bumped `agent_version` 0.3.0 → 0.4.0.

## [0.3.0] — 2026-06-13

### Changed

- **Full re-grounding supersession.** The source PDF was re-converted with Docling,
  recovering 70 real section-heading anchors. The prior MarkItDown conversion produced
  0 headings and an empty anchor index, leaving all previous evidence grounded to nothing.
  All claims, evidence records, and principles (P001–P013) have been rebuilt on the new
  heading anchors under source ID `domaindrivendesignqu-20260612231910`.

- Set `tier: 1` in profile (principles.yaml with 13 principles present).

- Re-grounded `quality_bar` and `forbidden_behaviours` to principle IDs P001–P013
  (inline citations in each item).

- Re-grounded all seven `always_on` knowledge items to principle IDs.

- Re-grounded all six `when_to_use` triggers to principle IDs.

- Replaced modes `patch-suggest` and `compare` with `extract` (justified by Q9;
  Q9 evidences implicit concept extraction via P010). Mode set is now:
  review, validate, advise, extract.

- Added new `when_to_use` trigger for refactoring-toward-deeper-insight and
  Core Domain identification (P010, P013).

- Added principle-ID citations to `handoff_rules` language-change rule (P001).

- Updated `minimum_useful_output` to require principle reference citation per finding.

- Source ID updated to `domaindrivendesignqu-20260612231910`.

### Preserved

- Slug, display name, role, expert topic.
- All six skill names and four reference names (unchanged — principles.yaml
  `operational_mapping` references these exact names).
- Golden test IDs GT-001, GT-002, GT-003, NR-001, NR-002, MC-001.

## [0.2.0] — 2026-06-11

### Added

- Authored all 6 skill bodies (ubiquitous-language-session, refactoring-toward-deeper-insight,
  aggregate-design, repository-and-factory-design, anticorruption-layer-design, domain-distillation)
  and all 4 reference bodies (building-block-pattern-summaries, context-map-pattern-catalogue,
  layered-architecture-layer-responsibilities, refactoring-checklist) from the source, replacing stubs.

### Changed

- Promoted package `status: draft → ready` (Step 8 skill/reference authoring).

### Notes

- Tier 0 authoring: bodies grounded in profile `always_on` + source markdown (no principle/claim
  layer); provenance principle/claim arrays empty by design.
- Drift baseline stamped (`cli stale --stamp`). quote-scan PASS; skill-authoring validator OK.

## [0.1.0] — 2026-06-09

### Added

- Initial generation from source pack
- Sources: Domain-Driven Design Quickly (Avram & Marinescu, InfoQ/C4Media, 2006)

### Profile

- Role: Reviews, critiques, and guides domain models, ubiquitous language, bounded contexts, and tactical DDD building blocks...
- Modes: review, advise, validate, patch-suggest, compare

### Notes

- Generated by subagent-factory v0.1.0
- Rights status: distillation-only — no verbatim quotation from source; all profile content is paraphrase
- Skills and references are stubs pending expansion in next authoring cycle
