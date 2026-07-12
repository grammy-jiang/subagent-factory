# descriptive-translation-reviewer — Review Loop r4

Package: `subagents/descriptive-translation-reviewer/` (agent_version 1.11.0, Tier 2)
Date: 2026-07-12

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** — 0 FAIL (Phase 8 self-check WARNING only) |
| `quote_scan` | **PASS** — no verbatim quotation |
| ellipsis truncation grep | clean |
| adapter invariant severed-parenthetical grep | clean |

No deterministic must-fix.

## Reviewer panel (STEP 2)

7 reviewers spawned; every one returned `MUST_FIX_COUNT: 0`.

| Lens | Reviewer | must-fix | should-fix | nice |
|------|----------|:-:|:-:|:-:|
| Skill authoring | agent-skills-advisor | 0 | 3 | 3 |
| Profile readiness | profile-reviewer | 0 | 3 | 2 |
| Faithfulness (over-claim) | faithfulness-reviewer | 0 | 1 | 1 |
| Agent design | ai-agent-engineering-reviewer | 0 | 2 | 1 |
| Domain: equivalence | translation-equivalence-advisor | 0 | 0 | 2 |
| Domain: quality | translation-quality-reviewer | 0 | 0 | 1 |
| Domain: technical | technical-translation-advisor | 0 | 1 | 2 |

Domain accuracy verdict across all 3 domain reviewers: **no misattributions, no reversed
definitions, no garbled procedure names** in 180 principles / 12 skills. Package repeatedly keeps
commonly-conflated frameworks distinct (House's two overt/covert axes; Nida vs Newmark vs House;
Frawley third-code vs Blum-Kulka explicitation; Newmark vocative vs Reiss operative; Schleiermacher
direction correct).

## Consolidated findings (STEP 3) — dedup, most-severe first

### should-fix

1. **skills/*/SKILL.md `description` fields — overlong, tie-breaker-dense** | agent-skills-advisor.
   Worst: `meaning-signification-and-equivalence-critique/SKILL.md:3-15` (~140w, 3 sibling-routing
   clauses); same pattern in domestication-foreignization, translation-procedures-and-shifts,
   hermeneutics, equivalence-orientations, translation-quality-and-applied-studies. Description is the
   sole always-loaded trigger; multi-way routing prose buries the primary trigger and pushes toward the
   1024-char ceiling. **Fix:** trim each to terse what+when with trigger keywords first; move detailed
   tie-breaker routing into When-to-use / Purpose.

2. **Systemic intra-file duplication (all 12 skills)** | agent-skills-advisor. Review-only disclaimer
   stated twice (Purpose + Output, e.g. `culture-ideology-power-and-rewriting/SKILL.md:60,102`);
   principle-id list restated in Provenance prose (`:133`) though already machine-readable in frontmatter
   (`:13-33`). **Fix:** state review-only constraint once per file; replace Provenance prose id-list with
   pointer to frontmatter + source titles/authors.

3. **Three densest skills near 1:1 procedure-step/anti-pattern per principle** | agent-skills-advisor.
   `culture-ideology-power-and-rewriting` (20 princ, 134 lines), `descriptive-method-and-translational-norms`
   (21 princ, 134 lines), `hermeneutics-and-the-limits-of-translatability` (19 princ, 132 lines). ~1
   trigger loads 2000-2800w. **Fix:** fuse each step + mirrored anti-pattern into one "check X / flag Y"
   line, or split culture-ideology-power (5 sub-lenses) into two tighter skills.

4. **Frontmatter `description` "Not for" clause weak for orchestrator routing** | ai-agent-eng.
   Adapter line 3 (from `profile.yaml when_not_to_use[0]`) ends "Not for: This reviewer critiques
   translation decisions, not the text itself" — a role restatement, not an actionable exclusion. The
   real boundary (don't produce/certify a translation, don't route corpus QA scoring) is truncated out.
   **Fix:** regenerate description compression to preserve the actionable exclusion.

5. **Scope overlap vs sibling `translation-equivalence-advisor` unresolved on paper** | ai-agent-eng.
   `when_to_use` bullet 6 + `translation-procedures-and-shifts` skill keep Vinay-Darbelnet/Catford
   procedure review here, but `when_not_to_use` bullet 2 routes "the equivalence mechanism (word,
   collocation, grammar)" to the sibling — same VD ladder operates at that level in both. **Fix:** add a
   disambiguating clause: this agent judges whether the *procedure type / macro-strategy* is right;
   word/collocation rendering value routes to `translation-equivalence-advisor`. (Overlaps profile SF-10.)

6. **`minimum_useful_output` orphan-field audit gap** | profile-reviewer. `profile.yaml:81-83` is a
   top-level field in neither the ledger's cite-required list nor its descriptive-exempt list
   (`provenance-ledger.md:6-17`); no inline citation. rights-and-quotation-policy requires every field
   traceable. **Fix:** add it to one side of the ledger's citation-convention sentence.

7. **SF-10 aged >2 cycles with no owner/ticket/target** | profile-reviewer. `provenance-ledger.md:63`
   register-discourse boundary vs `translation-quality-reviewer` deferred across ≥3 rounds. **Fix:** land
   the reciprocal fix or convert to explicit `owner-decide` naming who closes it and by when.

8. **Profile body ~985/1000w — thin margin vs hard-FAIL cap** | profile-reviewer
   (`provenance-ledger.md:97`). Redundant review-only restatement in role + when_not_to_use[0] +
   forbidden_behaviours[0]. **Fix:** proactively trim ~30-50w of restatement to restore margin before the
   next required edit.

9. **faithfulness-report.yaml missing `when_to_use[5]` verdict** | faithfulness-reviewer. Profile
   `when_to_use` has 6 bullets (0-5); report covers only 0-4. Coverage gap, not over-claim (bullet is
   WITHIN_SCOPE). **Fix:** add `rule_ref: when_to_use[5]` verdict WITHIN_SCOPE / accept_with_note.

10. **Subtitling limits stated as hard universal thresholds** | technical-translation-advisor.
    `principles.yaml P069` + `register-discourse-and-audiovisual-constraints` step 10 / anti-patterns:
    "38 Roman / 13-15 CJK chars / ~6s" flagged as pass/fail. These are platform-specific (Netflix ~42
    Latin/16 CJK, BBC, ITC differ). A literal reviewer could flag correctly-specced work. **Fix:**
    reframe as illustrative guideline; check against commissioning platform spec first, fall back to cited
    figures only when no spec supplied.

### nice

- **P089 grounding-hygiene inconsistency** | faithfulness-reviewer. `knowledge_partition.always_on[11]`
  cites P089, the only principle flagged `operational_mapping.profile_rule: false`. Profile text does not
  over-claim it. **Fix:** drop the P089 citation or flip its flag to `true`.
- **Reviewer-voice override carried by single sentence** | ai-agent-eng. ~120 first-person-imperative
  invariants held in check by one role-paragraph override. **Fix (optional hardening):** repeat a
  one-line reviewer-voice reminder at top of `forbidden_behaviours` or near the invariants block.
- **`role` "operating invariant" refers to unlabelled `knowledge_partition.always_on`** | profile-reviewer.
  Mapping only explained in ledger. **Fix:** reword role's closing clause to name the section, or gloss in
  ledger.
- **`when_to_use` theory-of-meaning trigger for meaning-signification skill loosely covered** |
  profile-reviewer. Ledger MF-2 claims full 12-skill coverage; that skill reachable only via generic
  equivalence framing. **Fix:** fold explicit theory-of-meaning clause into when_to_use[0]/[1] if bullet
  gate allows.
- **P105 Nida formal-equivalence over-extended to legal texts** | technical-translation-advisor +
  translation-equivalence-advisor. `principles.yaml P105` ties formal equiv to "academic or legal texts";
  Nida's paradigm case is interlinear/footnoted scholarly text — legal precision rationale is Newmark's
  (P162). **Fix:** cross-ref P105 → P162 so legal reviewers route to the precision-driven rationale.
- **P010 "governed at the base by the initial norm" base/top ambiguity** | translation-equivalence-advisor.
  Toury's initial norm is superordinate. **Fix:** reword to "governed overall by the initial norm."
- **P150 "principle of charity" more Davidson than Quine** | translation-quality-reviewer. Substance
  accurate to Word and Object. **Fix (optional):** soften to "a charity-of-interpretation move."
- **description skill-names in backticks; H1 wording drift; exclusion bullet inside When-to-use** |
  agent-skills-advisor. `meaning-signification .../SKILL.md:8` backticks;
  `domestication-foreignization .../SKILL.md:52` H1 adds "Translator";
  `translation-quality-and-applied-studies/SKILL.md:63` exclusion in When-to-use diverges from 11
  siblings. Cosmetic/structural consistency.
- **MQM/DQF not named even as out-of-scope inside quality skill** | technical-translation-advisor.
  Boundary disclosed at profile `when_not_to_use` but not visible at skill-read time. **Fix:** add a "not
  this skill" line naming MQM/DQF → route to `translation-quality-reviewer`.

## Verdict

All deterministic gates PASS. All 7 reviewers `MUST_FIX_COUNT: 0`. No domain errors, no over-claim, no
tool over-grant (Read/Grep/Glob only), no authority creep. Remaining items are should-fix polish
(description trimming, intra-file dedup, sibling-scope disambiguation, audit-trail completeness) and
nice-to-have refinements. Package is release-ready; the should-fix items are quality/hygiene, not
correctness blockers.

MUST_FIX_COUNT: 0
