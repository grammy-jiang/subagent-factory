# Changelog — Software Design Reviewer

All notable changes to this generated subagent package are recorded here.

## [1.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [1.1.0] — 2026-07-02

### Changed
- **Map→reduce rebuild of the distilled spine** (67 principles, up from the calibrated
  34) with the LLM-authored layer regenerated to match. The deterministic spine
  (`analysis/claims.jsonl`, `principles/principles.yaml`, `evidence/evidence-records.yaml`,
  `sources/anchors/*`) was assembled by the build and left untouched.
- **Regenerated the behaviour-test layer** against the 67-principle spine:
  `tests/behaviour-tests.yaml` (golden-tests-v1) rebuilt via `gen_behaviour_tests`
  (112 golden / 45 missing-context cells, every high-confidence principle covered) and
  `tests/principle-behaviour-tests.yaml` regenerated deterministically (67 entries, one
  per principle, mode round-robin) so every high-confidence principle carries a
  behavioural test.
- **Re-exported the adapter** to recompile the must-hold invariant layer over the current
  principle set.
- **Committed the reduce provenance triple** (`.build/clusters.json`, `.build/decisions.json`,
  `.build/groups.json`) so the distilled spine is deterministically rebuildable. The prior
  package predated `groups.json`; without it a re-assemble recomputes the clustering and can
  mis-map the group-indexed decisions. `--select 0.5` reused the byte-identical cached
  `decisions.json` (clusters reproduced exactly), so no LLM precision-filter re-run was needed.

### Fixed
- **Preserved curated source provenance.** The assemble step re-synthesized
  `sources/metadata/*.metadata.json` + `source-pack.manifest.yaml` from the staging markdown,
  dropping curated `title`/`author`/`year`/`assets_path`; restored the hand-curated values from
  the pre-rebuild package (identical source bytes — sha256 unchanged). No claim/anchor content changed.

### Deferred
- **Dropped the stale 34-era Step-7 synthesis** (`principle-clusters.json`, `principle-graph.json`,
  `conflict-log.md`) rather than ship a graph covering only 34 of the 67 principles;
  `multisource_synthesis: deferred` stands. Regenerate via the Step-7 C-track
  (seed → LLM-confirm) when cross-source synthesis over the full set is wanted.

## [1.0.0] — 2026-06-24

### Changed
- **Calibrated 0.25x rebuild.** Rebuilt the distilled spine via `build_map_reduce
  --select 0.25` over the cached per-book MAP (no re-extraction): the uncalibrated
  134-principle pool (>25% dilution) is reduced to the measured-best top quarter —
  **886 claims → 34 principles → 291 evidence records**.
- **Regrounded the authored layer onto the new spine** (reground, not re-author): the 8
  skills, 5 references, profile prose, golden-tests and principle-behaviour-tests had every
  principle citation remapped from the old 134-id space to the surviving 34 (survivors keep
  ids/statements; dropped ids → nearest survivor by MiniLM similarity with hand-curated
  overrides). Bodies unchanged; `authored_from_digest` re-stamped. Pruned the 100
  principle-behaviour tests for dropped principles.

### Added
- **Step-16 GRADE confidence blocks** on all 34 principles (`grade` = source_type +
  downgrades/upgrades); `confidence == grade_confidence(grade).level` for all (0 mismatches).
- **Step-13 ask-gate**: opt-in Answer/Ask/Abstain gate. Authored `applies_when` decision
  cues on the 11 principles that lacked them (all 34 now gated); regenerated
  `tests/behaviour-tests.yaml` — 68 golden (incl. 34 answerable twins) + 34 missing-context.
- **Step-7 C-track**: `principle-clusters.json` (4 cross-source clusters, each ≥2 sources),
  `principle-graph.json` (18 typed edges; 1 resolved cross-source conflict), `conflict-log.md`.

### Verification
- `validate_generated_package`: PASS (0 fail, 0 warn). Faithfulness: 25 verdicts, all ≤ source
  support (6 EXACT_SUPPORT, 19 WITHIN_SCOPE, 0 over-claims). `quote_scan`: PASS.

## [0.3.1] — 2026-06-22

### Changed
- Regenerated `tests/principle-behaviour-tests.yaml` to cover **all 134 principles**
  (P001–P134), one `principle_id`-keyed test per principle, replacing the prior file that
  stopped at P050 and left 43 high-confidence principles (P051–P059, P077–P090, P105–P117,
  P126–P132) with no behavioural test. Restores full high-confidence principle→test coverage.
- Re-exported the adapter so the `## Operating invariants (must hold)` layer covers every
  current must-hold principle (the prior adapter predated P051+ and was stale).

## [0.3.0] — 2026-06-22

### Changed
- Re-grounded the LLM-authored layer onto the map→reduce-rebuilt distilled spine, whose
  globally-renumbered ids (`P###` principles, `C#####` claims, `<sha12>-cNNNN` chunk anchors)
  had orphaned every citation in the prior `PRC-*`/`clm-*`/`-hNNNN` scheme.
- Re-grounded all 8 skill + 5 reference `provenance` blocks to the new principle ids, each
  principle's `derived_from_claims`, and those claims' real chunk anchors (bodies unchanged);
  re-stamped `authored_from_digest`.
- Regenerated `tests/principle-behaviour-tests.yaml` as one `principle_id`-keyed test per
  principle (P001–P050), restoring high-confidence principle→test coverage.
- Remapped residual `PRC-*` citations in `profile.yaml` prose and `tests/golden-tests.yaml`
  to the matching new `P###` ids; re-exported the adapter (invariant must-hold layer now
  covers the current high-confidence principles).

### Removed
- Deleted the stale `principles/principle-clusters.json` and `principle-graph.json` (authored
  against the defunct 26-principle `PRC-*` scheme; the rebuild emitted no id-keyed synthesis).
  Cross-source synthesis is acknowledged via `multisource_synthesis: deferred`.

## [0.2.0] — 2026-06-20

### Added
- Authored the body of the final stub skill, `facilitate-design-it-twice` (compare mode),
  grounded in PRC-020 (design it twice) with comparison axes from PRC-002/005/006/003/007.
- Authored all five reference bodies from the package's own principles, claims, and source
  anchors (no verbatim quotation; all sources `distillation-only`):
  `ousterhout-red-flags-catalogue`, `fowler-code-smell-catalogue`,
  `clean-code-heuristics-summary`, `equation-of-software-design-summary`,
  `gof-pattern-selection-guide`.
- Stamped `authored_from_digest` drift baselines into all 8 skills and 5 references (Step 9).

### Changed
- Promoted package status `draft` → `ready`: all 8 skills and 5 references authored
  (0 stubs), `validate_skill_authoring` clean, quote-scan clean, adapter re-exported.

## [0.1.0] — 2026-06-20

### Added
- Initial generation of the `software-design` subagent package (Tier 2, multi-source).
- Five canonical sources ingested (`distillation-only`): *A Philosophy of Software Design*
  (Ousterhout), *Code Simplicity* (Kanat-Alexander), *Clean Code* (Martin), *Refactoring*
  (Fowler), and *Design Patterns* (Gamma, Helm, Johnson, Vlissides).
- Tier-2 evidence chain: 82 atomic claims, 82 evidence records, importance scores,
  26 operational principles, 6 cross-source clusters, and a 20-edge principle graph
  (including one logged, resolved cross-source conflict).
- `profile.yaml` with five modes (review, advise, compare, validate, patch-suggest),
  `policy/patch-policy.yaml` (`patch_suggest_only`).
- `reports/faithfulness-report.yaml`, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml`.
- Skill and reference stubs scaffolded; package status is `draft`.

### Notes
- Verbatim quotation is prohibited (all sources `distillation-only`).
- To author the skill/reference bodies and promote to `ready`, re-run Step 8.7
  (`--author-skills`).
