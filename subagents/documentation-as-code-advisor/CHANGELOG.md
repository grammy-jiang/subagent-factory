# Changelog — documentation-as-code-advisor

## [0.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## 0.1.0 — 2026-06-28

### Added

- **Initial release.** A documentation-as-code advisor grounded in three sources: the Diátaxis
  framework (`diataxis-7065cb6e`), Google's technical-writing courses
  (`google-tech-writing-3ae5f96e`), and *Docs Like Code* case studies
  (`docs-like-code-stori-9b3c3a53`).
- **Distilled spine** assembled deterministically by the per-book map→reduce build: 354 claims
  (`C#####`), evidence records, and 64 principles (`P001–P064`; 42 high-confidence), with chunk
  anchors (`<sha12>-cNNNN`). The spine was not hand-edited.
- **Source layer** reconciled to the spine: `source-pack.manifest.yaml` plus
  `sources/{original,markdown,metadata,reports}` for all three sources, with `profile.yaml`
  `sources[]` sha256 matching the ingested metadata. Chunk anchors preserved from the build (the
  ingest's heading anchors were overwritten with the build's chunk anchors).
- **Profile** with `advise` / `classify` / `review` modes, quality bar, and forbidden behaviours,
  each rule citing the principles it is grounded in.
- **Skills (4)** — `classify-with-the-diataxis-compass`, `write-the-four-documentation-types`,
  `write-clear-technical-prose`, `operate-a-docs-as-code-workflow` — and one reference,
  `diataxis-compass-reference`, each grounded in real principle / claim / chunk-anchor IDs.
- **Tests** — `golden-tests.yaml` (positive + negative routing) and
  `principle-behaviour-tests.yaml` covering every high-confidence principle.
- **Faithfulness report** grading each gradable profile rule against the evidence and chunk
  anchors; no rule stronger than its source. Distillation-only sources — no verbatim quotation.
- **Claude Code adapter** exported from the profile.
