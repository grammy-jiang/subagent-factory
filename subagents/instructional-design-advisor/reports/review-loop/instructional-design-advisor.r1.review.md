# Review — `instructional-design-advisor` (round r1)

Package: `subagents/instructional-design-advisor/` (agent_version **1.5.0**, tier 2, 11 sources,
200 principles, 13 skills, 2 references)
Date: 2026-07-27
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer (release
readiness) + faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design)

> This path previously held the round-1 report against **v1.3.0**; that content is superseded and
> overwritten here per the review instruction. Its must-fix items were addressed by the 1.4.0/1.5.0
> rounds (P067 hedge restored in `examples[0]`, P096 citation added to `quality_bar[5]`, P041
> sentence added to `always_on[10]`) — re-checked below and no longer present.

## Deterministic gate results

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate: `…` ellipsis in skills/adapter | no hits |
| truncation gate: severed invariant parenthetical in adapter | no hits |
| adapter-sync / adapter-fresh / injection-scan / stale-maintenance / adapter-quality | all OK |
| skill-authoring | all 13 skills + 2 references authored |

Non-fatal: `phase8: Phase 8 self-check WARNING` — carried below as F1 (body size ~935w against a
800w soft budget / 1000w hard FAIL).

**Deterministic FAIL count: 0.**

## Consolidated findings

No must-fix from any lens. All four reviewers independently returned `MUST_FIX_COUNT: 0`. Everything
below is should-fix or nice — improvements, not release blockers. Findings are deduped across lenses
(F2 was raised independently by both profile-reviewer and ai-agent-engineering-reviewer).

### F1 — Phase 8 body-size WARNING has a thin, shrinking margin
- **Where:** `profile.yaml` (whole body, ~935 words); `provenance-ledger.md:245-257`
- **Severity:** should-fix
- **Problem:** Soft budget 800 words, hard FAIL >1000; the profile sits at 935 — a 65-word margin,
  up from a 6-word margin at 1.2.0 only because of an emergency trim. Two consecutive versions have
  needed trims to stay under the hard FAIL, so this is structural (dense, citation-packed
  sentences), not a one-off. The next citation-precision fix of the kind that shipped at 1.3.0/1.5.0
  could tip it over.
- **Fix:** Before the next content edit, relocate prose into fields Phase 8 excludes from the word
  count (`knowledge_partition.always_on` and `canonical_owner` are already exempt) rather than
  spending the buffer; or shorten `quality_bar` / `forbidden_behaviours` clauses.

### F2 — `primary_format` / `minimum_useful_output` never render into the adapter
- **Where:** `profile.yaml:45-47`, `profile.yaml:77-78` vs
  `.claude/agents/generated/instructional-design-advisor.md:208-227`
- **Severity:** should-fix
- **Problem:** The shared adapter template has no slot for these two fields, so the umbrella output
  contract ("never a bare good/bad verdict") and the minimum-output floor are invisible in the
  artifact the model and router actually see. Their substance had to be copy-pasted into every
  `outputs.modes[*].output` to reach the model — a DRY violation, and the declared `primary_format`
  is not what the exported adapter delivers.
- **Fix:** Either escalate a factory-level template change to render an "Output contract" line from
  `primary_format` + `minimum_useful_output` above/below the mode list (benefits every package), or
  drop the two now-dead fields from this profile since `modes[*]` already carries the substance —
  recording the removal in the ledger.

### F3 — Must-hold invariant layer flattened, losing topical structure
- **Where:** `.claude/agents/generated/instructional-design-advisor.md:26-174` vs
  `profile.yaml:119-277`
- **Severity:** should-fix
- **Problem:** The adapter renders ~100 principles (P002…P200) as one flat, ID-ordered list that
  jumps between unrelated topics line to line (cause-diagnosis, unit-design focus, multimedia
  dual-channel, rubric wording, needs-branching, all interleaved). `knowledge_partition.always_on`
  organises the same content into 12 coherent topic-scoped paragraphs. A reviewer working on a
  rubric must scan the whole list rather than a grouped subsection.
- **Fix:** Group the invariants render by the same skill/topic clusters as `knowledge_partition`, or
  add subheadings, so the must-hold layer is navigable.

### F4 — Faithfulness report has coverage and currency gaps
- **Where:** `reports/faithfulness-report.yaml` (whole file)
- **Severity:** should-fix
- **Problem:** No entries at all for `examples[0].ideal_response` or `examples[1].ideal_response`,
  despite both carrying inline P-citations and despite `examples[0]` having had a genuine
  HEDGING_REMOVED bug fixed at v1.5.0. The report was also not refreshed for the v1.5.0 citation
  edits: its `quality_bar[5]` entry still reads "Restates P148/P152/P140/P004" (the profile now also
  cites P096), and its `always_on[10]` entry omits the new P041 sentence. The current profile text at
  each site was independently verified as correctly hedged, so this is an audit-artifact gap, not a
  live over-claim — but the ledger explicitly commits to refreshing the report on every version bump,
  and that did not happen for 1.5.0.
- **Fix:** Regenerate or hand-refresh the report: add `examples[0]` / `examples[1]` entries and
  update the two stale citation notes.

### F5 — Two pairs of colliding skill descriptions
- **Where:** `skills/backward-design-and-constructive-alignment/SKILL.md:3-5` vs
  `skills/learning-outcomes-and-taxonomy/SKILL.md:3-5`;
  `skills/iterative-prototyping-and-development/SKILL.md:3-5` vs
  `skills/evaluation-transfer-and-impact/SKILL.md:3-5`
- **Severity:** should-fix
- **Problem:** Pair 1 both foreground "outcomes" vocabulary for different lenses (design-sequencing
  and alignment order vs. taxonomy-level wording and classification). Pair 2 both use
  "evaluation"/testing vocabulary for different lenses (SAM-style development release gating vs.
  Dick & Carey-style formal evaluation and transfer methodology). Either collision can fire the
  wrong skill.
- **Fix:** Add a one-clause negative disambiguator to each description — e.g. backward-design:
  "…not outcome wording or taxonomy-level classification"; iterative-prototyping: "…process and
  release-cycle management during development, not formal impact or transfer-of-training
  evaluation."

### F6 — 7 of 13 skill descriptions lack an explicit trigger clause
- **Where:** `skills/{backward-design-and-constructive-alignment, learning-outcomes-and-taxonomy,
  instructional-strategy-and-events, needs-and-context-analysis, evaluation-transfer-and-impact,
  active-learning-and-group-formats, teaching-scholarship-and-quality}/SKILL.md:3-5`
- **Severity:** should-fix
- **Problem:** At load time the router sees only name + description. Six sibling skills already
  model the "triggers when… / use when…" pattern with concrete scenarios; these seven omit it,
  weakening match quality.
- **Fix:** Append a short "use when …" clause naming concrete scenarios to each of the seven,
  matching the sibling style.

### F7 — Boilerplate duplicated verbatim across all 13 skills
- **Where:** every `skills/*/SKILL.md` — the Inputs' second bullet, the full `## Output` paragraph,
  `## References`, and the Provenance closing sentence (compare
  `backward-design-and-constructive-alignment/SKILL.md:85` and
  `teaching-scholarship-and-quality/SKILL.md:72` — identical text)
- **Severity:** should-fix
- **Problem:** The "does not build / teach / grade / certify" contract is already declared once at
  profile level (`outputs.modes`, `forbidden_behaviours`); restating it in full 13 times spends
  token budget that could carry skill-specific content.
- **Fix:** Trim the repeated Output/References paragraph in each skill to a short pointer.

### F8 — Orphan-field carve-out is a package-local reading of a repo-wide rule
- **Where:** `provenance-ledger.md:13-26`
- **Severity:** should-fix
- **Problem:** The ledger exempts two profile clauses (part of
  `source_of_truth_policy.canonical_owner`, half of `forbidden_behaviours[0]`) from the "no orphan
  field values" requirement in `.claude/rules/rights-and-quotation-policy.md`, on the sound reasoning
  that they state authority policy rather than a domain claim (the alternative — false citation to
  P107/P134 — was tried and reverted). But the shared rule carries no such provision; the exemption
  lives only in this package's ledger.
- **Fix:** Propose the exemption as a change to `.claude/rules/rights-and-quotation-policy.md` or a
  cross-package factory decision doc, so future reviewers of any package need not accept a
  self-declared exception.

### F9 — Imprecise citation fit on two `forbidden_behaviours` clauses
- **Where:** `profile.yaml:80-81` (`forbidden_behaviours[0]`, cites P107); `profile.yaml:87-88`
  (`forbidden_behaviours[3]`, cites P093)
- **Severity:** nice
- **Problem:** P107 ("Make the teaching theory shaping the learning environment explicit, then use
  evidence and a coherent framework to diagnose problems and adapt responses…") is adjacent to, not
  a match for, "the practitioner makes the teaching theory their own." P093 ("Do not add seductive
  details… they reliably reduce learning") is a design instruction, not a statement about mistaking
  interest for evidence of learning. Both were adjudicated at v1.5.0 (`verify2`) as non-must-fix —
  these are self-restricting boundaries, so the direction of claim rules out a strength over-claim.
  Citation-fit only.
- **Fix:** Re-point or drop the two citations on a future pass.

### F10 — Adapter role verb "judge" sits close to the certification boundary
- **Where:** `.claude/agents/generated/instructional-design-advisor.md:19`
- **Severity:** nice
- **Problem:** The Role paragraph reads "…and judge transfer and impact," which standing alone could
  be misread as rendering a final verdict, in tension with the ban on "Certifying a design
  effective… in advance." The next sentence disclaims authority, so risk is low.
- **Fix:** Reword to "…and assess transfer and impact against evidence," keeping every role verb
  advisory. (Edit `profile.yaml`, then re-export.)

### F11 — Read-only tool boundary never stated in the adapter body
- **Where:** `.claude/agents/generated/instructional-design-advisor.md` (whole body)
- **Severity:** nice
- **Problem:** The Read/Grep/Glob-only boundary is enforced structurally by the `tools:` frontmatter
  (line 4) and implied by the ban on building deliverables, but never spelled out in prose. Low risk
  for a text-advice role, but ambiguous if a caller hands the agent a file to "just fix."
- **Fix:** Add one line under Role or Forbidden behaviours: "This agent can only read and search
  files (Read/Grep/Glob) — it never edits, writes, or runs anything."

### F12 — Two large skill procedures are flat lists
- **Where:** `skills/assessment-design-and-authentic-tasks/SKILL.md:68-92` (23 steps);
  `skills/evaluation-transfer-and-impact/SKILL.md:64-84` (19 steps)
- **Severity:** nice
- **Problem:** Both present one long flat numbered list, while
  `instructional-strategy-and-events/SKILL.md` (35 steps) groups its list under thematic subheadings
  for scannability.
- **Fix:** Add thematic subheadings to the two large lists.

### F13 — Trigger-level phrasing near the grading boundary
- **Where:** `skills/assessment-design-and-authentic-tasks/SKILL.md:64`
- **Severity:** nice
- **Problem:** The "When to use" bullet "Grades, standards, or pass marks must be set, calibrated,
  or defended" reads close to the forbidden "Assigning a grade… to a learner's work." The body
  itself correctly stays on the criteria side.
- **Fix:** Reword to "Grading schemes, standards, or pass marks must be set, calibrated, or
  defended."

### F14 — `multisource_synthesis: deferred` across topically overlapping sources
- **Where:** `profile.yaml:2`
- **Severity:** nice
- **Problem:** No cross-source reconciliation ran across the eleven sources, two of which are
  companion volumes by the same author pair (Mayer 2009 *Multimedia Learning*; Clark & Mayer 2016
  *e-Learning and the Science of Instruction*) and two more covering closely related sequencing
  theory (Gagné et al. 1992; Reigeluth 1999). The 200-principle spine may carry near-duplicate
  principles under separate IDs. Flagged in the ledger as intentional.
- **Fix:** None now; candidate for a future `multisource_synthesis` pass.

## Verified clean (no finding)

- **Subagent independence:** no sibling-subagent routing anywhere in `profile.yaml`,
  `router_description`, `when_not_to_use`, `handoff_rules`, or the adapter. `handoff_rules` name only
  generic human roles (teacher of record, institution, qualified content expert).
- **Capability coverage:** `router_description` claims map 1:1 onto all 13
  `knowledge_partition.skills` entries — no capability gap or over-reach.
- **Forbidden behaviours:** cover all three domain disclaimers (accreditation/certification, grading,
  subject-matter correctness), non-overlapping with `when_not_to_use`, enforceable.
- **Version consistency:** ledger history 1.0.0 → 1.5.0 matches `profile.yaml:4 agent_version:
  1.5.0`; three specific 1.5.0-claimed edits were spot-checked against the ledger and matched.
- **Faithfulness:** no `CONTRADICTED`, `SCOPE_BROADENED`, or `HEDGING_REMOVED` verdict applies to any
  current profile rule. ~26 inline P-citations spot-checked (P001, P004, P011, P021, P041, P042,
  P062, P067, P092, P093, P096, P107, P109, P122, P134, P140, P148, P152, P153, P157, P163, P165,
  P172, P187, P191, P193) all resolve to principles that exist and say what the citing rule claims —
  the known map→reduce renumbering failure mode did not occur. Prior repairs still intact: P153
  "alone" hedge, P163 "solely from prior attainment", P157 system-paced scope bound, P165 conditional
  framing, P067 degree/complexity hedge in `examples[0]`.
- **Skills:** all 13 have a complete, order-consistent 1:1 mapping between frontmatter
  `provenance.principles` and numbered `## Procedure` steps (e.g. `instructional-strategy-and-events`
  — all 35 principles appear exactly once); both referenced files exist (no dead links); no
  TODO/placeholder text, no truncated bodies, no empty headings; all names and descriptions within
  the 64-char and 1024-char limits; every skill restates the non-build/non-grade/non-certify boundary.
- **Agent design:** role coherence is clean throughout — pure advisor identity, no drift into
  builder/judge/grader framing; disclaimers reinforced consistently across Role, Forbidden
  behaviours, Handoff rules, and both worked examples. `source_of_truth_policy` correctly directs
  uncited P-IDs to `references/instructional-design-principles-index.md` rather than memory — a
  deliberate, well-designed use of the Read grant. All other profile fields render faithfully into
  the adapter with no contradiction.

MUST_FIX_COUNT: 0
