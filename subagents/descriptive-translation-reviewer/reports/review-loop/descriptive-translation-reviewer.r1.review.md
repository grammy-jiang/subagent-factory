# Review Loop — descriptive-translation-reviewer (round 1)

Consolidated from deterministic gates + 7 reviewer lenses (agent-skills, profile, faithfulness,
ai-agent-engineering; domain: translation-equivalence, translation-quality, technical-translation).
Dedup applied; most-severe first. Each row: where | severity | problem | fix.

## Deterministic gates

- `validate_generated_package`: **1 FAIL** — tier-artifact adapter-invariant truncation (see MUST-FIX 1). Plus WARN: tier-consistency (profile `tier: 1` but classify computes `2`).
- `quote_scan`: PASS (no verbatim quotation).
- ellipsis/paren truncation grep: **101 `…` hits** in adapter invariant layer.

---

## MUST-FIX

### 1. Adapter invariant layer truncated — 101 `…` clauses + frontmatter `description` cut mid-clause
- **Where:** `adapters/claude-code/descriptive-translation-reviewer.md` (canonical) + `.claude/agents/generated/descriptive-translation-reviewer.md` (installed), "Operating invariants" lines 26–306; frontmatter `description` line 3. Deterministic FAIL + agent-design lens.
- **Problem:** `grep -c '…'` = **101** — nearly every invariant longer than ~20 words is severed mid-sentence (P001 "…compromise between two poetics in which the…", P002 "…when a literature is young and being established, when…"). Source `principles/principles.yaml` has **0** `…` (grounding intact), so the defect is the adapter `compile_invariants` step, NOT the source. These invariants are declared non-negotiable / precedence-over-soft-guidance, yet many state no rule — a hard constraint the agent cannot read in full. Same defect class already caught + fixed for sibling `technical-translation-advisor` (compile_invariants adapter-truncation gutting must-hold rules). Frontmatter `description` (the dispatcher's primary routing signal) is also cut: "…the team wants its equivalence — Not for:" — truncated before the predicate.
- **Fix:** Fix `compile_invariants` truncation length (reuse the technical-translation-advisor fix / generator-level cause), re-export adapter, verify **zero** invariant lines end in `…` and the frontmatter description ends at a sentence boundary from a complete `when_to_use[0]`.

### 2. Skill BODY procedure/anti-pattern steps truncated mid-clause (source SKILL.md, distinct from adapter)
- **Where:** `skills/*/SKILL.md` "Procedure" + "Anti-patterns to flag" bullets. Confirmed by grep (`\b(the|a|and|to|at|of|that)\s+\(P\d+\)\.`) — ~17 hits across 8 skills: `register-discourse-and-audiovisual-constraints`(6), `literal-free-strategy-history-and-retranslation`(3), `culture-ideology-power-and-rewriting`(2), `translation-quality-and-applied-studies`(2), + `domestication-foreignization-and-visibility`, `hermeneutics-and-the-limits-of-translatability`, `text-type-skopos-and-the-brief`, `translation-procedures-and-shifts`(1 each). Agent-skills lens.
- **Problem:** Steps end on a dangling article/preposition before the `(Pxxx)` cite, so the instruction has no predicate: e.g. `translation-quality-and-applied-studies/SKILL.md:72` "Surface a translation's (P113)." — subject-less, non-actionable. This is a body-structure defect in the authored source (independent of adapter), so it survives an adapter re-export.
- **Fix:** Re-run the digest→imperative-sentence authoring step (or hand-repair) so every Procedure/Anti-pattern bullet is a complete self-contained sentence before its `(Pxxx)` citation.

### 3. All 12 SKILL.md missing `description` frontmatter — routing undecidable
- **Where:** every `skills/*/SKILL.md` frontmatter (verified: 12/12 MISSING; sibling `technical-translation-advisor` HAS it). Agent-skills lens.
- **Problem:** Frontmatter carries only `name/kind/status/provenance`. `description` is the primary signal for routing/progressive-disclosure; with none, an agent must open every body to know when to load each skill. Regression vs sibling convention.
- **Fix:** Add a 1–2 sentence `description:` to each (front-load trigger + review boundary; compress existing `## Purpose` prose). Include a sibling-boundary clause for the 3 equivalence-adjacent skills (`equivalence-orientations-and-effect`, `meaning-signification-and-equivalence-critique`, `translation-procedures-and-shifts`) so routing has a tie-breaker.

### 4. Faithfulness report coverage gap + 2 mis-grounded handoff citations (SCOPE_BROADENED)
- **Where:** `reports/faithfulness-report.yaml` (17 findings, no entries for `handoff_rules[0]`/`[1]`); `profile.yaml` `handoff_rules[0]` (cites P070, P009), `handoff_rules[1]` (cites P162, P080). Faithfulness lens.
- **Problem:** Both citation-bearing handoff rules are unreviewed AND mis-grounded. `handoff_rules[0]` claims "commissioner holds the publication decision" but P070 = macro/micro decision split, P009 = commission negotiation — neither states publication authority (correct anchor is P029). `handoff_rules[1]` defers legal-validity/typesetting/commercial concerns citing P162 (which is legal-text *method* guidance, not a defer-to-specialist rule) + P080 (refraction, unrelated) — real citation mismatch.
- **Fix:** Re-anchor `handoff_rules[0]` to P029 (or soften), and drop/re-anchor `handoff_rules[1]` citations (legal-validity/typesetting is a defensible uncited scope boundary; commercial → P029). Add both rules to `faithfulness-report.yaml` with verdicts (SCOPE_BROADENED, action `add_condition`); note why `canonical_owner`/`when_not_to_use` are exempt or add them.

### 5. Cross-sibling routing disambiguation gap (4 concurrent translation reviewers)
- **Where:** `profile.yaml` `when_to_use[0]`, `when_not_to_use`, `handoff_rules`. Agent-design lens.
- **Problem:** `when_to_use[0]` ("…wants its equivalence orientation, strategy, register, and losses reviewed…") is near-verbatim to `translation-quality-reviewer`'s first trigger; neither `when_not_to_use` nor `handoff_rules` names the 3 siblings by slug/axis the way `translation-equivalence-advisor` reciprocally does. Genuine mis-routing risk across 4 co-installed reviewers.
- **Fix:** Add a `when_not_to_use` bullet + `handoff_rules` line naming the axis this package owns (descriptive method/norms, domestication–foreignization, ideology/rewriting, deforming tendencies, hermeneutics/translatability) vs. what routes to `translation-equivalence-advisor` / `translation-quality-reviewer` / `technical-translation-advisor` by slug.

---

## SHOULD-FIX

### 6. P047 overclaims the explicitation hypothesis as "confirmed" (3-lens convergence)
- **Where:** `principles/principles.yaml` P047. Flagged independently by translation-equivalence, translation-quality, AND technical-translation domain lenses.
- **Problem:** States Blum-Kulka's explicitation hypothesis was "later confirmed by corpus study." It is a *contested* candidate universal — corpus results are mixed (Øverås 1998, Pápai 2004) and critiqued (Becher 2010, Pym 2005). Unhedged "always/confirmed" is stronger than field consensus and internally inconsistent with the package's own hedged P041/P054/P110 — and self-contradicts this reviewer's own forbidden_behaviour against over-strong rules.
- **Fix:** Reword to "a translating-specific tendency found with varying/contested support across corpus studies," matching P041/P054 hedge level.

### 7. Anti-patterns section capped at exactly 7 bullets in all 12 skills (30–67% principle coverage lost)
- **Where:** every `skills/*/SKILL.md` "Anti-patterns to flag". Agent-skills lens.
- **Problem:** All 12 stop at 7 regardless of size (e.g. `descriptive-method-and-translational-norms` 7/21 = 33%; `culture-ideology-power-and-rewriting` 7/20). Reads as a generator length cap, not curation. Anti-patterns are the reviewer's working checklist — silent truncation is a completeness gap.
- **Fix:** Extend each Anti-patterns section to cover all principles in that skill's procedure, or document a deliberate top-N selection rule.

### 8. Mona Baker never named despite package encoding her translation-universals hypothesis
- **Where:** `principles/principles.yaml` P041, P047, P054 ("Baker" appears 0× across 180 principles). Translation-quality lens.
- **Problem:** The simplification/explicitation/normalization/levelling-out feature-set is Baker's foundational hypothesis (Baker 1993/1996); Munday credits her by name. Reader can't trace it or distinguish it from Toury's laws (P110) / Chesterman's S/T-universals (P054), which ARE named.
- **Fix:** Add/amend a principle crediting Baker's translation-universals hypothesis, distinguished from Toury's probabilistic laws and Chesterman's universals.

### 9. Anti-pattern bullets are mechanical negations, 3 ungrammatical
- **Where:** all 12 skills; broken instances `descriptive-method-and-translational-norms/SKILL.md:102`, `equivalence-orientations-and-effect/SKILL.md:90`, `meaning-signification-and-equivalence-critique/SKILL.md:80` ("The analysis fails to before…"). Agent-skills lens.
- **Problem:** Anti-patterns are "fails to " + verbatim procedure clause — no independent observable symptom; 3 are ungrammatical because the procedure step doesn't start with a bare verb.
- **Fix:** Fix the 3 grammar breaks; rewrite 2–3 bullets per high-traffic skill as concrete bad-finding symptoms, not negated instructions.

### 10. `tier: 1` inconsistent with 3-source manifest, siblings, and build record
- **Where:** `profile.yaml` line 6. Profile + agent-design lenses; validate WARN.
- **Problem:** Manifest has 3 sources → `classify_tier` = tier 2 (validate WARNs). All 3 siblings from the same corpus declare `tier: 2`; build memory records "Tier 2". `multisource_synthesis: deferred` already set, so no functional break, but WARN stands.
- **Fix:** Set `tier: 2`; keep `multisource_synthesis: deferred`.

### 11. P115 (Ortega/technical-text-ease) stated flatly, disputable + scope-leak
- **Where:** `principles/principles.yaml` P115. Technical-translation lens.
- **Problem:** "Technical/scientific texts translate more easily…" presented unqualified — a technical-translation expert disputes it (terminology precision, SI/units, safety-critical, false friends). It is Ortega's 1937 rhetorical contrast, not a modern practice finding.
- **Fix:** Keep as Ortega's historical comparative point; add a scope note that technical/scientific text difficulty/risk is out of remit → hand off to `technical-translation-advisor`.

### 12. Profile body ~870–880w (over 800 soft budget, under 1000 hard-fail)
- **Where:** `profile.yaml` role/quality_bar/forbidden_behaviours/modes. Profile lens.
- **Fix:** Trim redundant parenthetical restatement (quality_bar ~175w, forbidden ~113w repeat the "not stronger than source" idea) below 800w for headroom.

---

## NICE

- **P107** functionalist "translatorial action" not attributed to Holz-Mänttäri while siblings name Vermeer/Reiss/Nord — add "(Holz-Mänttäri's translatorial action)". (equivalence lens)
- **P150** "principle of charity" is Davidson's term, not Quine's — reword "Quine's maxim (sometimes glossed as a 'principle of charity')". (quality lens)
- **P019** "Chaume's ten, only one linguistic, four acoustic and six visual" reads as 1+4+6=11; Chaume = 4 acoustic (one linguistic) + 6 visual = 10 — reword to preserve 10-code total. (technical lens)
- **P056** neutrino "lack mass" example scientifically stale (mass confirmed 2015) — footnote as Quine's period example or swap. (equivalence lens)
- **Corpus currency** — sources predate NMT-era descriptive TS (post-editese, universals re-tested on NMT); add a scope note that norm/universals principles rest on human-translation corpora. (equivalence lens)
- **P014 vs P115** both introduce "normalization" from different lineages (Berman vs Ortega) without cross-ref — add one-line note. (technical lens)
- **`quote_scan` not recorded** in provenance-ledger/test-results though all 3 sources `distillation-only` — record the (passing) scan result before release. (profile lens)
- **`inputs.required`** is one run-on bullet bundling 5 elements — split into a checklist. (profile + agent-design lenses)
- **Output boilerplate** identical across all 12 skills — insert matching flaw-class tag per skill. (agent-skills lens)
- **`literal-free-strategy-history-and-retranslation/SKILL.md:46`** H1 uses en-dash vs plain hyphen elsewhere. (agent-skills lens)

MUST_FIX_COUNT: 5
