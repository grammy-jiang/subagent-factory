# Review Loop — descriptive-translation-reviewer — Round r2

Consolidated review across deterministic gates + 7 reviewer lenses (agent-skills,
profile, faithfulness, ai-agent-engineering, translation-equivalence,
translation-quality, technical-translation). Deduped, most-severe first.

## Deterministic gates

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL; Phase 8 self-check WARN only).
- `quote_scan` → **PASS** (no verbatim quotation).
- Truncation grep (ellipsis + severed adapter invariant) → **clean**.

Deterministic FAILs = 0.

---

## MUST-FIX

### MF-1 — Koller five-relations inverted into a "fixed-order ladder" (contradicts the principle itself; baked into the test suite)
- **Where:** `principles/principles.yaml` P106 body (~L2354-2361) is correct
  ("weigh as **simultaneous competing frames, not a fixed-order ladder**"), but every
  condensed restatement inverts it:
  - `references/descriptive-translation-principles-index.md:248` — "**Escalate through**
    Koller's five equivalence relations … **trying denotative**"
  - `skills/equivalence-orientations-and-effect/SKILL.md:56` (Purpose) — "correctly
    **escalates through** the available equivalence relations"
  - `tests/principle-behaviour-tests.yaml:1566-1577` (PB-P106 `expected_behaviour`) —
    quotes the same "escalate through … trying denotative" line as the target behaviour.
- **Severity:** must-fix (found independently by translation-equivalence-advisor;
  self-contradictory within the package — Procedure step 6 gets it right).
- **Problem:** Mischaracterises Koller's typology as a mandatory sequential checklist
  starting from denotative equivalence. The test suite would *validate the wrong
  behaviour* — an agent that "starts denotative and escalates" passes PB-P106 while
  acting against the principle body and against Koller as presented in Munday.
- **Fix:** Replace "escalate through … trying denotative" in all three places (index
  summary, skill Purpose sentence, and PB-P106 `expected_behaviour`) with the principle's
  own framing: "weigh Koller's five equivalence relations against each other by the needs
  of the communicative situation, as simultaneous competing frames rather than a
  sequential checklist." Reframe the matching anti-pattern in
  `equivalence-orientations-and-effect/SKILL.md:103` to match.

### MF-2 — Two same-package skills overlap with no tie-breaker; ledger's "already resolved" claim is false
- **Where:** `profile.yaml:140-149` (`knowledge_partition.always_on[6]`/`[7]`);
  `skills/domestication-foreignization-and-visibility/SKILL.md` (desc + Purpose);
  `skills/culture-ideology-power-and-rewriting/SKILL.md` (desc + Purpose);
  `provenance-ledger.md:41-42` (v1.5.0 entry).
- **Severity:** must-fix (profile-reviewer; `status: ready` rests on it).
- **Problem:** Both skills cover fluency/invisibility + institutional/ideological framing
  (culture-ideology's own P018 judges "whether fluent invisibility masks an appropriative
  domestication" — territory domestication-foreignization owns). The r5 supersession record
  claims this was re-triaged/downgraded because the overlap "already carries tie-breaker/
  boundary language." Grep of both SKILL.md files + `profile.yaml` always_on[6]/[7]:
  **no such tie-breaker text exists** in either skill. The `ready` state rests on an
  unverified, incorrect self-triage.
- **Fix:** Add one boundary sentence to each skill's description/Purpose (mirrored in
  `always_on[6]`/`[7]`): domestication-foreignization owns the fluency-illusion +
  domesticating/foreignizing-axis judgment; culture-ideology-power owns the
  institutional/agent/reception/ideology judgment; on overlap, lead with one. Correct the
  `provenance-ledger.md` v1.5.0 entry to record the actual fix, not the false "already
  carries" claim.

### MF-3 — Progressive-disclosure index has ~20 truncated / ungrammatical one-line summaries
- **Where:** `references/descriptive-translation-principles-index.md` — L283, 299, 307,
  320, 322, 325, 335, 346, 360-362, 367, 371, 391, 417, 428, 430, 440, 447, 449, 450
  (~11% of 180 entries). Worst: L450 `- **P113** — Surface a translation's.` (bare
  possessive, no predicate); L299 ends "…and that the method depends on far more than.";
  L307 ends "…as a secondary sender, so some."; L447 (P093) drops the research-design
  checklist tail.
- **Severity:** must-fix (agent-skills-advisor). This is the file every SKILL.md's
  `## References` points to as the principle catalogue; readers following the disclosure
  path get garbled/misleading cues.
- **Fix:** Regenerate the index summaries snapping to a clause/sentence boundary (or lift
  the char cap); hand-repair the ~20 broken entries; add a generator lint rejecting any
  summary ending in an article/conjunction/preposition ("and", "the", "a", "to", "plus",
  "than", "some") so it can't regress silently.

---

## SHOULD-FIX

### SF-1 — AVT skill invites a "dubbing script" but carries only subtitling criteria
- **Where:** `skills/register-discourse-and-audiovisual-constraints/SKILL.md:6-7` (desc),
  `:51` (Purpose), `:80` (Inputs "…or dubbing script"). All 13 procedure steps + 12
  anti-patterns are subtitling-specific (char/line/second limits, ECR strategies); none
  cover isochrony/lip-sync, kinesic synchrony, or voice-over. `profile.yaml:25-26` is more
  honest (names only "subtitling constraints").
- **Severity:** should-fix (technical-translation-advisor).
- **Fix:** Either narrow desc/Inputs to subtitling only (match the profile), or add
  dubbing-specific steps/anti-patterns grounded in the source's dubbing claim
  (`analysis/claims.jsonl` C00320).

### SF-2 — House error-taxonomy mischaracterised as a severity gradient
- **Where:** `skills/register-discourse-and-audiovisual-constraints/SKILL.md:51` — "the
  overtly-/covertly-erroneous error taxonomy **grades an error's severity** (P065)".
- **Severity:** should-fix (profile-reviewer; flagged r4/r5, still present, untracked).
- **Problem:** House's overtly/covertly-erroneous distinction is error type/detectability,
  not a severity gradient; conflating cuts against `quality_bar[5]` ("errors that pass
  silently").
- **Fix:** Reword to "classifies an error's type/origin, not its severity." Log it in the
  ledger (fixed or deferred).

### SF-3 — P121 omits Koller's fifth (formal/expressive) equivalence relation
- **Where:** `principles/principles.yaml` P121 / `adapters/…/descriptive-translation-reviewer.md:218`.
- **Severity:** should-fix (profile-reviewer). Internal inconsistency: P106 lists all five,
  P121 lists four — matters for the literary/poetic equivalence critique.
- **Fix:** Add "formal (formal-aesthetic/expressive)" to P121 and its dependent step, or
  log the deferral with a reason.

### SF-4 — Provenance ledger "Deferred" bookkeeping incomplete
- **Where:** `provenance-ledger.md:53-73` (v1.5.0 Deferred lists only NICE N1-N5, N7-N9).
- **Severity:** should-fix (profile-reviewer). Open r4/r5 should-fix items (SF-2, SF-3,
  and r5 S7 P021) are neither applied nor named as deferred — a ledger-only reader can't
  tell if they were deprioritised or lost.
- **Fix:** Name every open r4/r5 should-fix/nice item by its original ID in the Deferred list.

### SF-5 — Skill routing: three same-package equivalence skills have no cross-cue
- **Where:** `equivalence-orientations-and-effect/SKILL.md`,
  `meaning-signification-and-equivalence-critique/SKILL.md`,
  `translation-procedures-and-shifts/SKILL.md` (descriptions).
- **Severity:** should-fix (agent-skills-advisor). All three disambiguate from the *sibling
  package* but not from *each other* though they share adjacent ground (P106 vs P121 both
  invoke Koller). Three plausible same-package entry points, cues buried in prose.
- **Fix:** Add a one-line same-package routing cue to each description (orientation/effect →
  here; theory-of-meaning premise → skill Y; procedure/shift naming → skill Z), or a small
  routing table in a reference file.

### SF-6 — Frontmatter `description` doesn't disambiguate from sibling reviewers
- **Where:** `.claude/agents/generated/descriptive-translation-reviewer.md:3` (router-visible
  frontmatter); overlaps `translation-quality-reviewer.md:3`.
- **Severity:** should-fix (ai-agent-engineering-reviewer). Three-way sibling routing lives
  only in the body `when_not_to_use`, which a selection pass over frontmatter may not read →
  generic "review my translation" may mis-route.
- **Fix:** Add a "Not for" clause to frontmatter naming the closest siblings + axis split,
  mirroring `translation-equivalence-advisor`'s pattern.

### SF-7 — Procedure items are paragraph-length single sentences (not scannable)
- **Where:** all 12 `skills/*/SKILL.md` `## Procedure` (e.g.
  `descriptive-method-and-translational-norms/SKILL.md:84`, 95-word step).
- **Severity:** should-fix (agent-skills-advisor). 40-100-word academic sentences resist
  live checklist use.
- **Fix:** Split each into a short imperative lead ("Check: X") with justification/citation
  demoted to a trailing clause; one check per line.

### SF-8 — Anti-patterns ≈ 1:1 negation of Procedure across all 12 skills
- **Where:** all 12 `skills/*/SKILL.md` (e.g.
  `descriptive-method-and-translational-norms/SKILL.md:71` vs `:105`).
- **Severity:** should-fix (agent-skills-advisor; ai-agent noted the same doubling). Nearly
  doubles body token cost for limited added signal.
- **Fix:** Keep the affirmative Procedure check; rewrite Anti-patterns as short concrete
  "smells" (one-line bad-example phrasings), not full restatements.

### SF-9 — Operating invariants phrased as translator-facing imperatives
- **Where:** `.claude/agents/generated/descriptive-translation-reviewer.md:26-306` (e.g. P045
  L104 "Prepare a verse translation…"; P069 L144 "Subtitle within…"; P174 L294 "prescribe…").
- **Severity:** should-fix (ai-agent-engineering-reviewer). Up-front "review criteria, not
  instructions to translate" disclaimer can dilute over a 94-item imperative list; skill
  loads may surface imperative phrasing without the adjacent disclaimer.
- **Fix:** Reframe highest-risk invariants with a review verb ("Check that a verse
  translation first maps…"), or insert a recurring review-only reminder every ~25-30 items;
  confirm each SKILL.md preamble repeats the review-only framing.

---

## NICE

- **N1** — `references/…principles-index.md:272` P121 gloss adds an unsourced "1960s-70s"
  date qualifier not in the principle. Drop or ground it. (translation-equivalence)
- **N2** — `principles/principles.yaml:283` (P010) "governed **at the base by** the initial
  norm" — Toury's initial norm is superordinate; reword to "governed overall by / at its
  head". (translation-quality)
- **N3** — `principles/principles.yaml:1144` (P047) "tends **always** to increase…" — drop
  "always" (a tendency isn't absolute; surrounding hedge already correct). (translation-quality)
- **N4** — `references/…index.md:411` heading uses en-dash `Literal–Free` vs the hyphen slug
  everywhere else; normalise. (agent-skills)
- **N5** — No skill carries a worked good/bad mini-example despite 15-21 principles each; add
  one to the densest skills. (agent-skills)
- **N6** — Skill H1 title-case capitalises function words ("And"/"The"); internally
  consistent, cosmetic. (agent-skills)
- **N7** — `profile.yaml:17-18` `when_to_use[0]` still a mild dangling construction. (profile)
- **N8** — `knowledge_partition` is all `always_on`; consider `load_on_demand` for rarely-used
  clusters (hermeneutics, culture-ideology) for context budget. (ai-agent)
- **N9** — `profile.yaml:28-32` `when_not_to_use` packs three sibling-routing clauses into one
  dense bullet; split into three for scan-ability. (ai-agent)
- **N10** — Verify body word-count via `profile_self_check.py` (manual recount lands ~790-800w,
  at the 800 WARN line); keep firmer margin under 800. (profile)
- **N11** — `forbidden_behaviours[0]` uncited-by-design; point the exception at the named
  review-vs-produce convention so traceability is self-contained. (profile)

MUST_FIX_COUNT: 3
