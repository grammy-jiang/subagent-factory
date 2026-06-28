# Changelog — devops-sre-advisor

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
