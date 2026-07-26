# Changelog — instructional-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.2.0] — 2026-07-27

Review-loop repair round 1 (`/review-subagent`). No re-distillation: spine, principle numbering,
claims, and the eleven sources are unchanged.

### Fixed
- **Truncated skill bodies (all 13 skills).** The body generator cut `## Procedure` steps and every
  `## Anti-patterns to flag` bullet at a ~150-character prefix and closed the fragment with a
  period, so neither an ellipsis nor an unbalanced parenthesis existed for the truncation gate to
  catch. 101 procedure steps and 87 anti-pattern bullets re-authored from the full principle
  statements; restored, among others, P095's five triangulation sources, P158's three processing
  demands, P159's contiguity instruction (previously the bare label "Contiguity principle 1"),
  P032, P037 and P054's cut clauses. No new claim: each body still cites only the principle ids in
  its own unchanged frontmatter `provenance` block.
- **Four over-claims in `knowledge_partition.always_on`**, each repaired and mirrored into the
  matching skill `## Purpose`:
  - `[5]` (SCOPE_BROADENED) the preference for narration over concurrent on-screen text was stated
    unconditioned; it now carries P157's bound, "in a system-paced presentation".
  - `[1]` (HEDGING_REMOVED) "refuses retention evidence as proof a design worked" dropped P153's
    "alone"; restored, so retention evidence is insufficient by itself rather than rejected outright.
  - `[3]` (SCOPE_BROADENED) immediate self-checkable feedback in embedded practice was listed as a
    default design element; P165 states it as a repair when formative evidence exposes a relevance or
    fairness problem, and the rule is now conditioned that way.
  - `[4]` (HEDGING_REMOVED) "rather than lowered expectations" dropped P163's "solely from prior
    attainment"; restored.
  The last three were found only because the faithfulness pass was extended to cover this block —
  see below.
- **Mis-cited clause in `source_of_truth_policy.canonical_owner`**: certification and accreditation
  authority was attributed to P021/P172, neither of which mentions accreditation. Split into a
  grading-conversion clause (P021, P172) and a certification clause citing P096/P109/P004, the same
  grounding `forbidden_behaviours[1]` uses.
- **`forbidden_behaviours` gap**: "grades learners" and "rules on subject-matter correctness" were
  stated in `role` and `when_not_to_use` but never reached the enforcement list. Added as two
  principle-cited entries (P021, P172, P107; P193).
- **Orphan field value**: `source_of_truth_policy.canonical_owner` now cites the principles it
  restates (P107, P134, P193, P021, P172), matching the ledger's no-orphan claim.
- **`outputs.primary_format` / `minimum_useful_output` never rendered** into the adapter (no
  template slot). Their unique "never a bare good/bad verdict" constraint was folded into each
  `outputs.modes[*].output`, which does render — the shared adapter template was left untouched so
  no other package's adapter is affected.
- **Rights gate was vacuous**: `quote_scan` reported "rights NOT verified" for 11
  distillation-only sources (no `sources/markdown/`, cold cache). With the book-extract cache warm
  the 40-consecutive-word gate ran against all 11 sources — no verbatim quotation found.

### Changed
- **Anti-pattern sections** are no longer a mechanical `Overlooking Pxxx:` dump capped at seven
  regardless of skill size. They are curated, symptom-phrased failure modes scaled to the skill:
  every principle for the 6- and 9-principle skills, roughly half for the larger ones.
- **`description:` frontmatter** added to all 13 `SKILL.md` files.
- **`instructional-strategy-and-events`** (35 steps) grouped under five `###` sub-headers with one
  continuous 1-35 numbering run; `teaching-scholarship-and-quality` step 8 (P162) rewritten so it
  states what it adds beyond step 7 (P134) instead of restating it.
- **`learning-outcomes-and-taxonomy` / `teaching-for-understanding-and-transfer`** `## When to use`
  reworded so their triggers no longer both lead on "transfer".
- **Skill `## Provenance`** reduced to the principle-id list plus a pointer to the principles index;
  the identical ~130-word eleven-book block no longer repeats in all 13 files.
- **`role`** reworded from "prototype materials" to "plan prototyping and evaluation".
- **`reports/faithfulness-report.yaml`** extended from 19 rule locations to 43, adding
  `knowledge_partition.always_on[0]`-`[12]` (per-clause where dense) and the rules changed this
  round. That extension is what surfaced the `[1]`, `[3]`, `[4]` and `canonical_owner` defects above;
  all 43 entries now read WITHIN_SCOPE against the repaired profile.
- Profile body trimmed to ~987 words to stay inside the body budget after the additions.
- Claude Code adapter re-exported and reinstalled.

### Deferred
- Tiering the adapter's ~90-bullet always-on invariant layer. That set is compiled deterministically
  from `confidence: high` + `profile_rule: true` principles and gated by
  `validate_invariant_coverage`; tiering needs a generator-level notion of "cross-cutting" that does
  not exist yet. A factory-level change, not a package edit — see `provenance-ledger.md`.

## [1.1.0] — 2026-07-26

### Added
- *Instructional-Design Theories and Models: A New Paradigm of Instructional Theory / In Action*
  (Reigeluth, ed.) folded in as an eleventh source, adding instructional-theory selection
  (prescribe a method together with the situation it fits) and elaboration sequencing (the
  epitome -> elaborate -> synthesize zoom-lens cycle).

### Changed
- *Multimedia Learning* (Mayer) re-ingested from the full text, replacing the partial conversion
  (`mayer-multimedia-lea-f516bca0` -> `mayer-multimedia-lea-40e2757d`); the multimedia principles no
  longer lean on *e-Learning and the Science of Instruction* to cover Mayer's own material.
- Distilled spine rebuilt over the eleven sources: 200 principles (was 180) over
  7860 claims (was 6851). The rebuild renumbered every principle.
- LLM-authored layer fully re-derived against the new P001-P200 numbering — the
  13-skill partition, `profile.yaml` (quality bar, forbidden behaviours, handoff rules,
  precedence, examples, `knowledge_partition.always_on`), `reports/faithfulness-report.yaml`, all
  13 skills, both references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (200 tests, one per principle). The 1.0.0 principle
  ids do not carry over.
- Claude Code adapter re-exported to `adapters/claude-code/` and reinstalled under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` written as `md` by the rebuild, which is not a
  member of the `source-metadata-v1` enum; normalised back to `markdown`.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **instructional-design-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles / 6851 claims from ten
  distillation-only sources).
- `profile.yaml` derived from the promoted principles: role, router description,
  when/when-not-to-use, three modes (advise / review / plan), quality bar, forbidden behaviours,
  handoff rules, and a 13-skill / 2-reference `knowledge_partition` covering
  every principle exactly once.
- 13 authored skills; 2 references (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` and `tests/principle-behaviour-tests.yaml`.
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Eleven distillation-only sources: *Understanding by Design* (Wiggins & McTighe, 2005); *Teaching
  for Quality Learning at University* (Biggs & Tang, 2011); *Creating Significant Learning
  Experiences* (Fink, 2013); *A Taxonomy for Learning, Teaching, and Assessing* (Anderson &
  Krathwohl, 2001); *Principles of Instructional Design* (Gagné, Briggs & Wager, 1992); *First
  Principles of Instruction* (Merrill, 2002); *The Systematic Design of Instruction* (Dick, Carey &
  Carey, 2015); *Leaving ADDIE for SAM* (Allen, 2012); *Multimedia Learning* (Mayer, 2009);
  *e-Learning and the Science of Instruction* (Clark & Mayer, 2016); and *Instructional-Design
  Theories and Models* (Reigeluth, ed., 1999).
