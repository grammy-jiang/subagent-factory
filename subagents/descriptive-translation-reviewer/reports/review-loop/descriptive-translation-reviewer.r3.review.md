# descriptive-translation-reviewer — review loop r3

Consolidated review pass. Seven reviewer lenses (skill-authoring, profile-readiness,
faithfulness/over-claim, agent-design, + three domain cross-checks: equivalence, quality,
technical) plus deterministic gates. Findings deduped, most-severe first.

## Deterministic gates (STEP 1)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). Tier-2 consistency, all
  tier artifacts valid, 12 skills + 2 references authored, adapter-quality OK, all
  stale-maintenance grounding unchanged.
- `quote_scan` → **PASS** (no potential verbatim quotation).
- Truncation gate (ellipsis `…` + severed invariant parenthetical) → **no hits**.

Deterministic FAILs = 0.

---

## MUST-FIX

### M1 — Orphan/stale citation in `examples[1]` contradicts the v1.2.0 provenance decision
- **where:** `profile.yaml` L204 (`examples[1].ideal_response`) vs `provenance-ledger.md` L46
- **severity:** must-fix
- **problem:** `examples[1].ideal_response` reads `…it does not translate or make the sign-off
  (forbidden behaviours, P070, P100).` But the v1.2.0 ledger entry explicitly records
  **"P070, P100 dropped"** for `forbidden_behaviours[0]` (never-translate/never-sign-off is a
  product-scope boundary, deliberately uncited). `forbidden_behaviours[0]` is now uncited,
  matching the ledger — but the example was never updated, so it still asserts source grounding
  the package's own provenance record says does not exist. Verified: **P100 appears nowhere else
  in `profile.yaml`** — it is a dangling citation with no owning field, violating the "no orphan
  field values" hard rule (`rights-and-quotation-policy.md`).
- **fix:** In `examples[1].ideal_response`, drop the stale citation to match the
  uncited-by-design `forbidden_behaviours[0]` — change `(forbidden behaviours, P070, P100)` to
  `(forbidden behaviours)`. Bump `agent_version`, add a Version-History entry, re-export adapter.

---

## SHOULD-FIX

### S1 — Faithfulness report does not cover the 12 `knowledge_partition.always_on` bullets
- **where:** `reports/faithfulness-report.yaml` (20 `rule_ref` entries) vs
  `profile.yaml` `knowledge_partition.always_on[0..11]`
- **severity:** should-fix
- **problem:** The report audits `quality_bar`, `forbidden_behaviours`, `when_to_use`,
  `outputs`, `source_of_truth_policy`, `handoff_rules` — but zero entries for the 12
  `always_on` bullets, each of which compresses 8–20 principle IDs into one paragraph. These are
  the profile's highest structural risk for `SCOPE_BROADENED` (a compression silently dropping a
  source hedge). Manual spot-checks found no over-claim, but the guarantee was never run.
- **fix:** Add `rule_ref` entries for `knowledge_partition.always_on[0..11]` (ideally also
  `when_not_to_use`, `minimum_useful_output`) with per-rule verdict/distortion/severity/action.

### S2 — Ledger's provenance-accounting sentence omits `examples` (root cause of M1)
- **where:** `provenance-ledger.md` L6–12
- **severity:** should-fix
- **problem:** The audit-surface sentence lists `quality_bar`/`forbidden_behaviours`/
  `handoff_rules`/`knowledge_partition.always_on`/`source_of_truth_policy` but never mentions
  `examples`, which carry ~15 inline citations. No declared policy on whether example citations
  are audited or exempt — which is how M1 survived two prior review rounds.
- **fix:** Add `examples` to the citation-accounting sentence (audited, or explicitly exempt),
  and re-check example citations whenever a cited field's grounding changes on a version bump.

### S3 — `minimum_useful_output` only gates the `review` mode, not `advise`/`compare`
- **where:** `profile.yaml` L74–75 vs modes L53–60
- **severity:** should-fix
- **problem:** The bar is phrased entirely in "finding/flaw/correction/trade-off" terms
  (review mode). `advise` output is a recommendation naming principle(s)+orientation+trade-off
  (no "flaw"); `compare` is a brief-weighted side-by-side. Two of three declared modes are not
  obviously gated by the self-check.
- **fix:** Broaden wording to cover all three output shapes (or one bar sentence per mode).

### S4 — `when_to_use[2]` is a garden-path/comma-spliced trigger that seeds the adapter routing
- **where:** `profile.yaml` L21–22
- **severity:** should-fix
- **problem:** "A translation is praised for fluency and the team wants that criterion, and the
  translator's visibility, interrogated." Ambiguous trailing clause — unlike the other four
  triggers. This list seeds the exported adapter routing `description`, so wording quality has
  direct routing consequences.
- **fix:** Reword, e.g. "A translation is praised for fluency, and the team wants both that
  criterion and the translator's visibility interrogated."

### S5 — Sibling handoff boundary overlaps the package's own P106/P109 in identical vocabulary
- **where:** `profile.yaml` `when_not_to_use` L27–30 vs invariants P106/P109 (L113–117)
- **severity:** should-fix
- **problem:** `when_not_to_use` routes "the linguistic equivalence mechanism itself (word,
  collocation, grammar, information structure)" away to `translation-equivalence-advisor`. Yet
  P109 instructs this reviewer to "analyse equivalence at multiple levels (word, above word,
  grammar, thematic structure, cohesion, pragmatics)" and P106 has it weigh Koller's relations.
  Near-identical vocabulary in the exclusion clause and in P106/P109 → a caller/agent cannot
  tell which sibling owns word/grammar-level equivalence analysis.
- **fix:** Narrow the exclusion to a disjoint scope (e.g. corpus-evidence/collocation-frequency
  scoring specifically), or reframe P106/P109 as orientation-level judgment ("does the chosen
  orientation fit the purpose") so the two packages' stated scopes stop overlapping.

### S6 — Adapter frontmatter `description` drops the highest-value routing signal
- **where:** `.claude/agents/generated/descriptive-translation-reviewer.md` L3 (frontmatter)
- **severity:** should-fix
- **problem:** The routing-critical description collapses the five-bullet `when_to_use`/
  `when_not_to_use` lists to one example each, dropping the three-way sibling exclusion
  (`translation-equivalence-advisor` / `translation-quality-reviewer` /
  `technical-translation-advisor`) and the review-only boundary. Those exist in the body but not
  where the invoke-or-not decision is made.
- **fix:** Expand the frontmatter description to name the sibling routing and the review-only
  boundary explicitly. (Re-export from profile after adjusting the source description.)

### S7 — Skill bodies are heavy for progressive disclosure (always-loaded footprint)
- **where:** `skills/*/SKILL.md` (all 12; worst: `culture-ideology-power-and-rewriting` 20
  principles ×2 restatements, `descriptive-method-and-translational-norms` 21,
  `hermeneutics-and-the-limits-of-translatability` 19)
- **severity:** should-fix
- **problem:** Skills bundle 15–21 principles, each restated as a dense 40–80-word sentence in
  *both* Procedure and Anti-patterns — paid on every trigger, working against the
  small-context-footprint goal of three-tier progressive disclosure.
- **fix:** For skills >~10–12 principles, keep SKILL.md to the 5–8 highest-impact checks the
  routing description promises; move remaining principle-level detail into the already-wired
  `descriptive-translation-evidence-notes.md` / `-principles-index.md` references.

### S8 — House's two same-named axes (overt/covert type vs overtly-/covertly-erroneous) are conflated
- **where:** `skills/register-discourse-and-audiovisual-constraints/SKILL.md` steps 2 & 6;
  principles P021, P065
- **severity:** should-fix (domain accuracy)
- **problem:** House has two independent constructs sharing near-identical labels: the
  overt/covert **translation-type** typology (P021) and the overtly-/covertly-**erroneous**
  **error taxonomy** (P065). The skill places them in one procedure with no note the terminology
  is coincidental → risk of conflating translation-type with error-severity.
- **fix:** Add one clarifying sentence (Purpose, or in P021/P065) stating the two labels name
  different axes and are not the same judgment.

### S9 — Theorists dropped where their coined concepts are used (documentation-fidelity gap)
- **where:** principles P009/P062 (skopos → **Vermeer** unnamed), P002 (polysystem →
  **Even-Zohar** unnamed), P001/P050 (refraction/rewriting/patronage → **Lefevere** unnamed);
  echoed in `text-type-skopos-and-the-brief` and `culture-ideology-power-and-rewriting` skills
- **severity:** should-fix (domain accuracy)
- **problem:** These frameworks are stated correctly but attributed to no one, while Reiss,
  Nida, Newmark, Catford, Toury are named at point of use. Same root cause: principles derived
  from a named chapter in Venuti's *Reader* strip the chapter-author's name. Prior r2 review
  (M2) already had to reconstruct "Vermeer/Nord/Reiss" from context.
- **fix:** Name Vermeer in P009/P062, Even-Zohar + "polysystem theory" in P002, Lefevere in
  P001/P050, so the reviewer can check a caller's attribution against the actual originator.

---

## NICE

- **N1 — no stated multi-lens composition rule.** `profile.yaml` review mode spans all seven
  flaw classes (needs several of 12 skills together), but each SKILL.md is scoped to its own
  lens with no note on combining, and no routing skill exists → risk of all-12 load or single-
  lens partial review. *Fix:* short "composing with sibling skills" note per skill, or a small
  routing reference. (skill lens)
- **N2 — "Procedure" label implies sequencing** the unordered checklists don't have. *Fix:*
  rename to "Checks" or add a one-line "independent checks, not execution order" note. (skill)
- **N3 — inconsistent trigger-description phrasing** across the 12 sibling `description` fields
  ("Use when…" vs "Reviews…" vs "Review a translation's…"). *Fix:* standardize one opening.
- **N4 — "Purpose" restates the frontmatter `description`** near-verbatim in most skills,
  spending body tokens on Level-1 content. *Fix:* trim Purpose to the added nuance only.
- **N5 — disclaimer distance / authority-creep risk.** The "review criteria, not instructions
  to translate" reframing sits once in Role, far above a ~180-line imperative-toned invariants
  block → drift risk toward how-to-translate coaching. *Fix:* move the disclaimer to immediately
  before "Operating invariants", or repeat a short parenthetical framing in the list. (adapter)
- **N6 — meta-authoring note leaked into agent-facing text.** `handoff_rules[1]` ends
  "Sibling-axis routing is stated once under when_not_to_use" — a structure comment, not
  behaviour. *Fix:* remove or fold into rule 1's routing list. (`profile.yaml` L91 / adapter L397)
- **N7 — `quality_bar[3]` citation-completeness.** "audiovisual shortening… re-coding, not
  omission" is most precisely grounded by P052 (cited in `always_on` bullet 6, not here). Not
  an over-claim. *Fix:* add P052 to `quality_bar[3]`'s citation list. (faithfulness)
- **N8 — `examples` coverage thin.** Only 2 examples (both review-mode-ish), touching 2 of 12
  skills; no `advise`/`compare` example. *Fix:* add one each, from an underrepresented skill.
- **N9 — `inputs` has no `optional` key.** Cosmetic schema-consistency. *Fix:* add
  `optional: []` if factory convention does so. (profile)
- **N10 — P142 merges Dolet's five rules (1540) + Tytler's three laws (1791)** into one
  anonymous "classic ranked prescriptions" bloc. *Fix:* split, or name both Dolet and Tytler.
  (domain)
- **N11 — P105 pairs Nida formal equivalence with "legal texts"** as a native use case; Nida's
  own framing is gloss/academic, and the package's own P162 hedges legal as only "close to"
  formal equivalence. *Fix:* align P105 wording with P162's hedge. (domain)
- **N12 — P090 implies Grice's maxims are "suited/validated" for technical/legal genres.**
  More accurate: those genres deliberately minimize implicature, so such frameworks are more
  *tractable* there, not validated on them. *Fix:* reword to "more tractable in conventionalized
  genres where pragmatic ambiguity is deliberately minimized." (domain)
- **N13 — DTS-vs-functionalism methodological tension unflagged.** Profile fuses Toury's
  descriptive/non-prescriptive norm-reconstruction with prescriptive functionalist skopos
  without naming the epistemic tension. Not a factual error. *Fix (optional):* a short clause in
  `source_of_truth_policy` framing them as complementary review lenses. (domain)
- **N14 — P047 gloss of Blum-Kulka's explicitation hypothesis imprecise** ("a translating-
  specific discourse type" — closer to Frawley's third code, already named). Actual claim is a
  process tendency (rising explicitness/redundancy/cohesion). Existing hedge is fine. *Fix:*
  reword to "a proposed process tendency of translation." (domain)

---

MUST_FIX_COUNT: 1
