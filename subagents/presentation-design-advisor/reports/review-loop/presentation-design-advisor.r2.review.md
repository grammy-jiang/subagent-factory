# Review — presentation-design-advisor (round r2)

Package: `subagents/presentation-design-advisor/` (14 skills, 2 references, 3 sources: Alley
*Craft of Scientific Presentations*, Duarte *Resonate*, Duarte *slide:ology*).

Review only — no package file was modified by this pass.

## 1. Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL, 2 WARN |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| Truncation gate — `…` ellipsis in skills / adapter | clean (no hits) |
| Truncation gate — invariant severed inside a parenthetical (`(e.g`) | clean (no hits) |

Both validator WARNs are non-blocking (not FAILs), recorded for the record:

- `quote-scan: rights NOT verified` — 3 `distillation-only` sources but no `sources/markdown/` and
  no warm cache module, so the verbatim-quote gate could not run. A *coverage* gap in the gate, not
  evidence of a quotation problem; expected for a rights-clean export. The standalone `quote_scan`
  over package artifacts passed, and `reports/quote-scan-verified.md` documents the manual check.
- `phase8: Phase 8 self-check WARNING` — check 14 only (body-size): profile body ≈950 words against
  an 800-word **soft** budget, hard fail at 1000. Not a coverage gap. Disclosed at
  `provenance-ledger.md` lines 93–96. Little headroom left — see F5.

**Deterministic must-fix count: 0.**

## 2. Reviewer panel

| Lens | Agent | MUST_FIX |
|------|-------|----------|
| Skill authoring quality | agent-skills-advisor | 0 |
| Profile release-readiness | profile-reviewer | 0 |
| Faithfulness / over-claim | faithfulness-reviewer | 0 |
| Agent design (adapter) | ai-agent-engineering-reviewer | 0 |

No lens found a blocking defect. Findings below are deduped across lenses, most-severe first.

## 3. Consolidated findings

### F1 — Ledger asserts a 1:1 principle partition that P120 violates
- **Where** | `provenance-ledger.md` "Distillation" (lines 46–53) vs `profile.yaml` lines 214–215 and 236
- **Severity** | should-fix
- **Problem** | The ledger claims "118 of the 120 principles are partitioned across 14 skills, each
  owned by exactly one skill," disclosing only P036 and P048 as exceptions. P120 is in fact cited in
  **two** `knowledge_partition.always_on` paragraphs — audience-analysis (lines 214–215) and
  persuasion (line 236) — and is not disclosed as a third exception. The content is defensible
  (P120's head/heart/gut/groin calibration genuinely informs both), but the ledger's accuracy claim
  is false as written. Note: the *skill frontmatter* `provenance.principles` partition is clean (the
  skill lens confirmed zero cross-skill duplicates) — the defect is confined to the `always_on` prose
  and the ledger's claim about it.
- **Fix** | Either disclose P120 as a third cross-cutting exception alongside P036/P048, or drop the
  citation from whichever paragraph does not independently need it.

### F2 — Sibling trigger boundary lives in the body, not the description, for two overlap-prone skills
- **Where** | `skills/audience-analysis-and-persona-design/SKILL.md:3-5`,
  `skills/persuasion-ethos-pathos-and-logos/SKILL.md:3-5`
- **Severity** | should-fix
- **Problem** | The rehearsal / in-room-delivery / questions-composure trio each carry an explicit
  "for X, use skill-Y instead" clause in the frontmatter `description` — the only tier read before a
  skill is judged relevant. The equally overlap-prone audience-analysis ↔ persuasion pair bury their
  mutual disambiguation in the body's "When to use", which loads only *after* description matching.
  Result: ambiguous triggering between the two.
- **Fix** | Append a boundary clause to each description, mirroring the proven trio pattern — e.g. on
  audience-analysis: "For building or auditing the persuasive case itself (appeals, prior bias,
  reward), use persuasion-ethos-pathos-and-logos instead," plus the mirror clause on the other.

### F3 — Three faithfulness-report verdicts are stale, contradicting their own notes
- **Where** | `reports/faithfulness-report.yaml` — `knowledge_partition.always_on[4]`
  (SCOPE_BROADENED / medium / `add_condition`), `always_on[6]` (SCOPE_BROADENED / low /
  `add_condition`), `skills[6]` (SCOPE_BROADENED / medium / `downgrade`)
- **Severity** | should-fix
- **Problem** | Each entry's note says the drift was fixed in 1.3.0, and the fix is verified live:
  `profile.yaml:186-192` carries all three P087/P116/P059 conditions; `profile.yaml:226-233` carries
  the P092/P115/P040/P117 conditions; `skills/persuasion-ethos-pathos-and-logos/SKILL.md:58` already
  restricts P006 to its own scientist population with an explicit anti-generalisation instruction.
  These are the *only* recorded verdicts for their `rule_ref`, so a reader who trusts the
  `verdict`/`severity`/`action` fields without the note concludes the package still over-claims and
  still owes work that already shipped. A wrong verdict, in the conservative direction.
- **Fix** | Set the three verdicts to `WITHIN_SCOPE` (matching sibling `skills[4]`, which correctly
  records the fixed state), drop the satisfied `action`, or restructure the report so historical
  findings are visibly separated from the current verdict.

### F4 — No instructed fallback when a *required* input is missing
- **Where** | `profile.yaml` lines 42–49 → adapter lines 284–289
- **Severity** | should-fix
- **Problem** | Both required inputs (the artifact/account; who the audience is) are said to "gate the
  advice," and the *optional*-inputs sentence tells the agent exactly what to do when they are absent
  ("proceed without them, naming what each would change") — but nothing says what to do when a
  **required** input is missing. Given a deck with no audience named, the agent may invent an
  audience, silently refuse, or advise ungrounded: three behaviours, none instructed.
- **Fix** | Add one sentence to `inputs.required`: "If either required input is missing, ask for it
  before advising; do not assume an audience or artifact." Re-export the adapter.

### F5 — Phase-8 body-size WARNING carried across rounds with no terminal decision
- **Where** | `profile.yaml` (body ≈950w vs 800w soft budget); `provenance-ledger.md` lines 93–96
- **Severity** | should-fix
- **Problem** | Honestly disclosed and non-blocking (hard fail is 1000w; v1.0.0 shipped 1083w→941w,
  content regrew as fixes landed). Two consequences: headroom to the hard FAIL is now small, so any
  further profile growth flips the gate red; and the item has recurred across review rounds, so each
  round re-argues the same trade-off.
- **Fix** | Record a terminal decision — either state in the ledger that the overrun is permanently
  accepted and no longer tracked, or make one bounded trim pass (best candidates: `inputs`/`outputs`
  prose, lowest citation density; the heaviest blocks `quality_bar`/`forbidden_behaviours`/
  `when_to_use` are citation-dense and should not be cut) to buy headroom once.

### F6 — ~2–3k words of verbatim boilerplate duplicated across all 14 skills
- **Where** | all 14 `skills/*/SKILL.md` (e.g. `assertion-evidence-slide-structure/SKILL.md:77-79`,
  `slide-density-and-signal-to-noise/SKILL.md:112-119`)
- **Severity** | should-fix
- **Problem** | The whole "Output" paragraph and the second `Inputs` bullet are word-for-word
  identical in all 14 files, and the body `## Provenance` section re-states in prose the principle-ID
  list already carried in frontmatter `provenance.principles`. ≈150–250 duplicated words × 14. Works
  against progressive disclosure once several skills load in one session.
- **Fix** | Move the generic output contract and generic input clause into
  `references/presentation-design-evidence-notes.md` (already linked from every skill); shorten each
  skill's Output/Inputs to the skill-specific part plus a pointer. Trim the body `## Provenance`
  section to a one-line pointer to the frontmatter block.

### F7 — Two story-structure procedure steps read as "do the work", not "advise"
- **Where** | `skills/story-structure-and-the-big-idea/SKILL.md:59` and `:62`
- **Severity** | should-fix
- **Problem** | Step 1 ("Write the big idea … as a complete sentence…") and step 4 ("Settle the story
  … by writing the main message and each supporting assertion on separate sticky notes…") are bare
  subjectless imperatives. A literal reading is "draft the presenter's big idea," colliding with the
  same file's Output line ("it does not write the talk") and the profile's forbidden behaviour
  "Writing the talk, building the deck." Risk is bounded — every skill's Output section restates the
  advice-only boundary — but these verbs are ambiguous where siblings' are not.
- **Fix** | Re-frame with an explicit advisory subject: "Check whether the presenter has written the
  big idea as a complete sentence…" / "Guide the presenter to settle the story before opening slide
  software, by…", matching the "Diagnose / Recognise / Apply" verbs used elsewhere.

### F8 — `router_description` has no row in the field-grounding table
- **Where** | `provenance-ledger.md` field-grounding table (lines 18–28); field at `profile.yaml:8-18`
- **Severity** | nice
- **Problem** | `router_description` carries its own content (a fuller topic enumeration than `role`,
  plus its own "Advises and reviews… Not for…" clause) but has no table row — only a parenthetical
  inside the `role` row. Even the purely structural `multisource_synthesis` earned its own row. The
  rights-and-quotation policy requires every profile field traceable, no orphan values.
- **Fix** | Add a brief `router_description` row: "mirrors `role`'s grounding plus
  `when_not_to_use`/`forbidden_behaviours[0]` for its exclusion clause; no independent claims."

### F9 — Worked example 4 closes with cross-agent routing phrasing
- **Where** | `profile.yaml` lines 411–427 → adapter lines 384–388
- **Severity** | nice
- **Problem** | `ideal_response` ends "your methods reviewer rules on whether the claim is true." No
  tool-boundary violation (this agent has no Task tool), but it echoes the sibling-routing phrasing
  the factory's subagent-independence rule avoids, and could be copied into a package that does carry
  routing metadata.
- **Fix** | Reword to capability language: "whether the claim is true is not this advisor's call."

### F10 — P082's occasion condition not restated inline
- **Where** | `profile.yaml` `knowledge_partition.always_on[7]` ("…delivers real depth inside a
  deliberately broad talk…")
- **Severity** | nice
- **Problem** | P082's `applies_when` is "the occasion calls for a big-picture talk or the scope is
  large through sheer number of topics." Unlike every other conditioned clause in that paragraph
  (P089's "why it matters" gate is stated inline), this one omits its condition. It reads as
  descriptive rather than as a universal command, so it stays WITHIN_SCOPE — a consistency issue only.
- **Fix** | Restate P082's occasion condition inline, matching the paragraph's other clauses.

### F11 — Nine of 14 skills have no worked example anywhere in the package
- **Where** | `skills/typography-colour-and-slide-layout`, `story-structure-and-the-big-idea`,
  `opening-closing-and-framing-slides`, `rehearsal-and-memorisation`, `in-room-delivery-and-composure`,
  `questions-challenge-and-composure`, `equipment-venue-and-contingency`,
  `format-choice-and-preparation-planning`, `talk-organisation-transitions-and-emphasis`
- **Severity** | nice
- **Problem** | Every skill illustrates incorrect states in "Anti-patterns to flag", but none carries
  a positive worked example of the procedure applied correctly. The profile's 4 examples only exercise
  the assertion-evidence / density / visual-evidence / persuasion / audience cluster. Cosmetic rather
  than functional — Procedure and Anti-pattern steps already embed concrete inline illustrations
  (exact point sizes, per-assertion-type graphic choices).
- **Fix** | Add one brief worked example per uncovered skill, or extend the profile-level example set
  to cover the delivery/logistics cluster.

## 4. Verified clean (checked, no defect)

- Tool grant is exactly Read/Grep/Glob; nothing in the adapter body instructs writing, editing, or
  running commands.
- Adapter is a faithful render of the profile — a full side-by-side of role, when_to_use /
  when_not_to_use, inputs, modes, quality_bar, forbidden_behaviours, handoff_rules,
  source_of_truth_policy, and examples shows no drift.
- `when_to_use` / `when_not_to_use` are mutually exclusive with no dead zone; no boundary names a
  sibling agent (subagent-independence rule holds).
- No rule in the current `profile.yaml` sits at HEDGING_REMOVED or CONTRADICTED, and no orphan rule
  claims source support. Hedges (P046, P028, P054/P094/P105, P016/P066), conditions (P087/P116/P059,
  P092/P115/P040/P117, P098, P111) and numeric figures (120–140 wpm, 28 pt, two-line/four-item bounds,
  P047's controlled-comparison framing) all reproduce at source strength.
- The adapter body never claims authority to certify, guarantee, approve, or decide — every such
  phrase appears only inside a negation or a worked-example refusal.
- Skill frontmatter valid across all 14: kebab-case names, no XML tags, no reserved words, concise
  trigger-rich descriptions; the principle-ID partition across skill frontmatter is clean.
- Version History satisfies the supersession rule — explicit supersession entries, withdrawn
  faithfulness grades, "not a defect" callouts.

MUST_FIX_COUNT: 0
