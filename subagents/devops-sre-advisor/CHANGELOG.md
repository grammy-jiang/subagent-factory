# Changelog — devops-sre-advisor

## 0.4.0 — 2026-07-04

### Added

- **Eighth source: *Continuous Delivery* (Jez Humble & David Farley).** Folds the canonical
  deployment-pipeline, build/test automation, and release-engineering material into the DevOps/SRE
  corpus (165 principles mapped from the book).

### Changed

- **Rebuilt as an 8-book package and tuned `--select` 150 → 175 principles** (pool of 1193).
  Aligned the authored layer with the current map-reduce spine (175 principles, 4484 claims,
  903 evidence records) after the deep rebuild renumbered the spine.
- tests/principle-behaviour-tests.yaml: regenerated from the current 175 principles so every
  high-confidence principle (incl. the new P151–P160) is exercised and every `expected_behaviour`
  matches its current statement. The prior suite only covered P001–P150 with pre-rebuild text.
- sources/metadata: corrected `source_type` from the invalid `md` to `markdown` (source-metadata-v1
  enum) across all 8 sources.
- provenance-ledger.md: corrected the evidence-chain counts to the current spine.
- Re-exported the Claude Code adapter to refresh the invariant layer with the current must-hold
  principles (P038, P042, P055, P065–P066, P085–P092, P136–P148, P151–P160, …).
- Distilled spine (claims / principles / evidence / anchors) unchanged. Profile / faithfulness /
  skill bodies were left intact (they validate; primary grounding is source anchors); their
  secondary principle-id citations still reference the pre-rebuild numbering.

## 0.3.1

- Regenerated the authored layer onto the deterministic map-reduce spine (150
  principles, 3638 claims, 769 evidence records).
- profile.yaml: corrected `sources[]` to the ingested source ids + sha256; re-tagged
  quality_bar / forbidden_behaviours to current principle ids.
- reports/faithfulness-report.yaml: re-graded all profile rules against the evidence chain
  with resolvable chunk anchors.
- skills/ + references/: remapped frontmatter provenance to resolvable claim / evidence /
  anchor ids (bodies unchanged).
- tests/principle-behaviour-tests.yaml: regenerated to cover every principle and every
  operational_mapping test_case.
- sources/metadata: corrected `source_type` to `markdown`.
- Re-exported the Claude Code adapter (refreshed invariant layer).
