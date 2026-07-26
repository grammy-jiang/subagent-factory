# Changelog — instructional-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.5.0] — 2026-07-27

Adversarial-verify repair (`/review-subagent` Step 6, `verify2`). No re-distillation: spine,
principle numbering, claims, and the eleven sources are unchanged from 1.4.0. One must-fix and two
citation-hygiene advisories closed. No claim was introduced that is not already in
`principles/principles.yaml`; the advice-only boundary and every safety hedge are unchanged in force.

### Fixed
- **`examples[0].ideal_response` turned P067's degree-caution into a categorical bar
  (HEDGING_REMOVED).** The worked example read "A multiple-choice quiz **cannot show
  understanding**", while P067 says only that evidence of understanding is *less direct and more
  complicated than* objective-test evidence — a caution with a prescribed remedy, not an exclusion.
  Two aggravating factors made this a must-fix rather than a citation slip: an `ideal_response`
  models the exact phrasing the subagent should emit to a caller, and it exported verbatim into the
  installed adapter. Restated to the source's own strength — evidence of understanding is less
  direct and more complicated than what a multiple-choice quiz yields, so ferret out the reasons
  behind the answers rather than the percentage correct — which also restores P067's remedy clause,
  previously dropped. The transfer-testing recommendation that follows (P196, P016, P017) is intact.

### Changed
- **`quality_bar[5]` cited `(P148, P152, P140, P004)` for "evaluated for learning and workplace
  transfer"** — none of the four states workplace transfer (P140 covers formative *draft*
  evaluation). The claim was true and grounded elsewhere in the profile but not at the site.
  `P096` — evaluate impact only after target learners can perform in context, gathering unobtrusive
  workplace evidence — is added, so the clause now carries its own grounding.
- **`knowledge_partition.always_on[10]` listed `P041` with no sentence reflecting it.** Rather than
  drop the id (which would leave P041 uncovered by any block), the block gains its content: an
  innovation persists only where it has an identifiable support group and constituency and can be
  monitored cost-effectively. In scope for an impact-and-evaluation block, and a direct restatement
  of the principle.

### Recorded, no action taken
- `forbidden_behaviours[0]`'s trailing `(P107)` on a compound sentence reads as covering both
  clauses; the raw finding was adjudicated down to advisory because the rule is a self-restricting
  role boundary (under-claiming its own authority carries none of the risk the faithfulness rule
  exists to prevent) and `verify1` already examined and accepted this exact construction.
- `compile_invariants._to_invariant()` renders only each principle's first sentence, dropping an
  operative second sentence on 6 of 75 rules (P157, P153, P122, P092, P156, P002). Every retained
  rule is a grammatically complete sentence — documented, deliberate, factory-wide behaviour, not a
  defect of this package.
- `forbidden_behaviours[3]` cites `P093` (do not *add* seductive details) on a rule about *treating*
  added interest as evidence learning occurred. Adjacent theme, imprecise fit, fairly read as
  WITHIN_SCOPE.
- `source_of_truth_policy.precedence` cites only `P193` on a clause also covering teacher-of-record
  and institutional ownership. Left uncited deliberately: 1.3.0 established that the ownership
  boundary is factory policy, not principle-derived.

## [1.4.0] — 2026-07-27

Review-loop repair round r1 (`/review-subagent`, consolidated panel: deterministic gates +
agent-skills-advisor + profile-reviewer + faithfulness-reviewer + ai-agent-engineering-reviewer).
No re-distillation: spine, principle numbering, claims, and the eleven sources are unchanged.
Three must-fix and four should-fix findings closed.

### Fixed
- **11 of 13 `SKILL.md` files ended with a stray unmatched `</content>` tag** — an authoring-wrapper
  delimiter that leaked from the skill-author step into the shipped bodies, which load verbatim into
  model context at trigger time. Stripped from all 11; each file now ends at its "Derived from …"
  provenance sentence. No other content in any skill body was touched.
- **`provenance-ledger.md` tail was a terminal-colorized diff paste — 38 raw ANSI escape sequences**
  (lines 180–218), a second, control-character-laden restatement of the 1.3.0 Version History entry
  that already existed cleanly at 132–179. The corrupted duplicate is deleted; the clean entry stands.
  `grep -c $'\x1b' provenance-ledger.md` → 0.
- **`reports/faithfulness-report.yaml` was stale at four sites** — it was last regenerated at 1.2.0 and
  still described the pre-1.3.0 citations that the adversarial-verify round removed
  (`handoff_rules[0]`, `source_of_truth_policy.precedence`, `forbidden_behaviours[4]`,
  `source_of_truth_policy.canonical_owner`). All four entries are rewritten in the
  `"REPAIRED in 1.x.0 … Now WITHIN_SCOPE"` pattern already used for the `always_on` entries, so the
  1.3.0 repair is recorded rather than leaving pre-fix prose in place.
- **`forbidden_behaviours[0]` stretched `P193` onto a clause it does not ground.** P193 is specifically
  about giving a *qualified content expert* validated goals and skill frameworks as explicit review
  standards for subject-matter correctness (used correctly at `forbidden_behaviours[5]` and
  `handoff_rules[1]`); here it was carrying the general advisor-supplies-criteria-rather-than-building
  boundary, which no principle states. `P193` is dropped; `P107` keeps the "practitioner makes the
  teaching theory their own" half, and the advisor-boundary half stands as uncited structural policy
  (see the carve-out below). No advice behaviour changes — the clause is an advisory restriction.

### Changed
- **Profile body trimmed 994 → 935 words** to restore headroom under the 1000-word hard-FAIL cap: at
  994 the package had a 6-word margin, so any future citation addition would have blocked validation.
  Redundant prose only — the enumerated advice-only tail of `role` (restated in full by
  `when_not_to_use` and `forbidden_behaviours`), the "built deliverable / promise of effectiveness"
  tails duplicated across `outputs.primary_format` and `modes[advise]` (stated in full at
  `forbidden_behaviours[0]` and `[1]`), and clause-level compression in `quality_bar`,
  `forbidden_behaviours`, and `handoff_rules[0]`. Every `P`-id citation and every distinct rule is
  retained; the phase-8 body-size WARNING is accepted at 935 words (65-word margin) and recorded as
  such in the ledger.
- **`source_of_truth_policy.canonical_owner` gained a citation-discipline clause** closing the
  finding that ~30 principle IDs are cited in the adapter's Quality bar / Forbidden behaviours /
  worked examples whose text never appears in the loaded prompt (the printed invariants list covers
  only a curated subset), so the agent could attach a fabricated gloss to a real-looking ID. It now
  directs the agent to read `references/instructional-design-principles-index.md` for any cited ID
  not spelled out in the invariants list rather than asserting from memory what the ID says.
  Placed in `canonical_owner` because that field renders into the adapter and is excluded from the
  body-size budget, so the fix costs no headroom.

### Recorded, no action taken
- **`outputs.primary_format` and `minimum_useful_output` still render nowhere in the adapter** — the
  shared template has no slot for either (confirmed again against
  `templates/claude-agent-adapter.md.j2`); their distinctive content stays duplicated into
  `outputs.modes[*].output` so it reaches the model. Factory-level template gap, re-flagged at this
  bump rather than silently carried.
- **`instructional-strategy-and-events` loads 35 principles on any trigger**, ~2× the next-largest
  sibling. A split along its existing `###` seams would break the 13-skill ↔ 13
  `knowledge_partition.always_on` 1:1 mapping and force a profile edit under body-size pressure;
  deferred to a later version as a scoped change of its own.

## [1.3.0] — 2026-07-27

Adversarial-verify repair (`/review-subagent` Step 6, `verify1`). No re-distillation: spine,
principle numbering, claims, and the eleven sources are unchanged. Two must-fix findings closed.

### Fixed
- **P157 invariant lost its scope condition (SCOPE_BROADENED, non-negotiable tier).**
  `compile_invariants._to_invariant` reduces a principle statement to its first sentence, and
  P157's bound ("in a system-paced presentation") lived in the second sentence — so the adapter
  carried the modality prescription unconditioned at its highest precedence, while `profile.yaml`
  and `skills/multimedia-and-elearning-design/SKILL.md` all kept the bound. The P157 *statement*
  in `principles/principles.yaml` is reordered so its first sentence is self-sufficient ("In a
  system-paced presentation, route words away from the visual channel when a graphic is
  present: ... Prefer narration over concurrent onscreen text."). Same claim, same scope, no new
  content — the adapter invariant now carries the pacing condition. The multimedia skill and the
  two references were re-stamped (`detect_stale --stamp`): they cite P157 and their bodies already
  stated the bound, so only the upstream digest moved.
- **P107/P134 cited to ground ownership and authority claims they do not state (mis-citation,
  four sites in `profile.yaml`).** P107 covers making the teaching theory explicit and adapting it
  to local learners; P134 covers systematic action-research cycles. Neither says who *owns* the
  course, the grades, the subject matter, or the decision to run it.
  - `source_of_truth_policy.precedence` — dropped `P107`; `P193` now attaches only to the
    subject-matter-referral clause it supports. The ownership clause stands as factory policy.
  - `handoff_rules[0]` — dropped `P107, P134`; `P021` retained on the criterion-based
    outcome-judgement clause.
  - `source_of_truth_policy.canonical_owner` — split, so `(P107, P134)` attaches only to the
    make-the-theory-explicit / adapt-through-systematic-cycles clause; final authority over the
    course is stated separately and uncited.
  - `forbidden_behaviours[4]` — dropped the spurious `P107`; `P021` and `P172` already ground it
    fully.

  The advice-only ownership boundary is unchanged in force — it is now stated as policy rather
  than dressed as principle-derived.

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
