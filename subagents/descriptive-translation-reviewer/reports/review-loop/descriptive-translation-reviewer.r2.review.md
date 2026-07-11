# descriptive-translation-reviewer — Review Loop r2

Consolidated review pass. Seven reviewer lenses (agent-skills, profile, faithfulness,
ai-agent-engineering + 3 domain: equivalence / quality / technical) plus deterministic gates.

## Deterministic gates (STEP 1)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). One WARNING: Phase 8
  self-check `body-size` (profile body ≈931w > 800-word soft budget; < 1000 FAIL threshold).
  WARN, not a hard FAIL → not counted as must-fix (see should-fix S1).
- `quote_scan` → PASS (no verbatim quotation).
- Truncation grep (ellipsis / severed invariant) → clean.

**Deterministic FAIL count: 0.**

---

## MUST-FIX

### M1 — Chaume signifying-code count is self-contradictory (1+4+6 = 11, not "ten")
- **Where:** `principles/principles.yaml` P019 line 506 ("Chaume's ten, only one linguistic,
  four acoustic and six visual"); echoed in
  `skills/register-discourse-and-audiovisual-constraints/SKILL.md:63` Procedure step 1.
- **Problem:** P019 states "ten" then breaks the total into 1 linguistic + 4 acoustic + 6
  visual = **11**. Chaume's actual taxonomy is 1 linguistic + 3 other acoustic + 6 visual = 10.
  A reviewer following the principle literally miscounts. Flagged independently by two domain
  reviewers (quality-reviewer must-fix; technical-advisor should-fix).
- **Fix:** In P019 change "four acoustic" → "three acoustic" so the components sum to ten.
  Reword the SKILL step to a non-contradictory breakdown (e.g. "one linguistic code, three
  further acoustic codes, and six visual codes" — or, if counting the linguistic code as one
  of the acoustic-channel codes, "four acoustic (incl. linguistic) plus six visual"). Make
  both files agree on one reading.

### M2 — `quality_bar[2]` states functionalist skopos as settled fact (SCOPE_BROADENED, self-contradiction)
- **Where:** `profile.yaml` `quality_bar[2]` — "Translation **is** driven by an explicit brief
  and the text's predominant function…" (cites P009, P038, P060, P062, P108).
- **Problem:** Every cited principle is functionalist/skopos machinery (Vermeer/Nord/Reiss) —
  one school in a corpus that also carries Toury descriptive-norms, Nida dynamic-equivalence,
  Newmark semantic/communicative. Stating it as a flat descriptive fact ("Translation **is**
  driven by…") converts a school's prescription into settled fact — the exact anti-pattern
  `forbidden_behaviours[2]` itself forbids ("presenting one school's prescription as settled
  fact"). Because `quality_bar` items are always-applied review criteria, this affects every
  review, including non-functionalist-framed ones.
- **Fix:** Hedge/scope, e.g. "Where a brief and predominant function are in play, translation
  is judged against them; a fulfilled skopos never excuses micro-level neglect."

### M3 — Adapter frontmatter `description` truncated mid-clause + dropped sibling-routing cue; ledger falsely claims fix
- **Where:** `.claude/agents/generated/descriptive-translation-reviewer.md:3` (and canonical
  `adapters/claude-code/descriptive-translation-reviewer.md` — in sync).
- **Problem:** `description` (the sole routing signal the orchestrator reads) ends on the broken
  clause "…the team wants its **equivalence** — Not for:" — verb with no object. Source
  `when_to_use[0]` continues "…orientation, strategy, and losses reviewed against the source and
  the brief," none of which survived. Worse, with four near-identical "translation reviewer"
  siblings live in the repo, the highest-value disambiguator — the sibling-routing
  `when_not_to_use` bullet (`profile.yaml:35-37`, names translation-equivalence-advisor /
  translation-quality-reviewer / technical-translation-advisor) — is entirely absent from the
  description. `provenance-ledger.md:35-36` (v1.1.0) claims "Re-exported the adapter to repair
  the truncated … frontmatter description" — untrue of the shipped file (process-integrity gap).
  Same defect confirmed in sibling adapters → shared generator/template bug.
- **Fix:** Regenerate `description` to complete each borrowed clause as a full sentence and to
  preserve (a compressed form of) the sibling-routing bullet; re-export; verify rendered
  frontmatter reads as complete prose; correct the v1.1.0 ledger entry (or add v1.1.1 recording
  the actual fix). Tool grant (`Read, Grep, Glob`) is correct — no change.

**LLM must-fix (deduped): 3.**

---

## SHOULD-FIX

- **S1 — Profile body over soft budget.** `profile.yaml` body ≈931w > 800-word Phase 8 soft
  budget (WARNING source). CHANGELOG v1.1.0 "trimmed toward the word budget" overstates — the
  round-1 trim was offset by the added `handoff_rules[2]`. Heaviest: `quality_bar` (160w),
  `when_not_to_use` (108w). Note `when_not_to_use[4]` and `handoff_rules[2]` are near-duplicate
  sibling-routing content (~65w overlap). Trim to ≤800w, re-run `profile_self_check`, fix the
  CHANGELOG wording. *(profile)*
- **S2 — Stale test metadata.** `tests/golden-tests.yaml:4-5` say `profile_version: 1.0.0`,
  `tier: 1`; profile is `agent_version: 1.1.0`, `tier: 2`. Re-stamp to 1.1.0 / tier 2. *(profile)*
- **S3 — quote_scan not re-verified after v1.1.0 re-author.** All 12 SKILL bodies were
  re-authored in v1.1.0 after the recorded quote_scan PASS → that PASS is stale for current
  content. Re-run and record the result in `provenance-ledger.md` (v1.1.0 entry) and
  `tests/test-results.md`. (Current run PASSes, so this is hygiene, not a blocker.) *(profile)*
- **S4 — `quality_bar[1]` mis-cited.** "does not mistake an illusory equivalent effect for a
  real one" cites P004/P105/P106/P118/P159 — none mention illusory effect; P059 does (and the
  profile's own knowledge_partition already cites P059 for identical language). Add P059. *(faithfulness)*
- **S5 — `forbidden_behaviours[0]` mis-cited.** The "never produce a translation / never sign
  off" boundary is a product-scope decision, not a TS claim; P070/P100 don't ground it. Drop
  the citations (leave it an uncited scope boundary, as done for `handoff_rules[1]`) or
  re-anchor the sign-off half to P029. *(faithfulness)*
- **S6 — Adapter invariant list omits 39 cited principles with no note.** The exported
  invariants render the 141/180 high-confidence subset; but `forbidden_behaviours[0]` cites
  P100 and `quality_bar[3]` cites P091, both in the excluded 39 → they appear nowhere in the
  adapter body. Add a one-line note in the "Operating invariants" intro that this is the
  high-confidence subset and citations may resolve via linked skill/reference files. *(ai-agent-eng)*
- **S7 — Koller's five relations framed as a sequential escalation ladder.**
  `principles.yaml` P106 / `skills/equivalence-orientations-and-effect` step 6 say "escalate
  through… trying denotative… then connotative…". Koller's *Äquivalenzrahmen* are simultaneous,
  competing frames weighed together, not a fixed-order gate. Reword to "weigh… against each
  other by the communicative situation." *(equivalence)*
- **S8 — Newmark mis-dated.** `principles.yaml` P121 folds Newmark's semantic/communicative pair
  into "1960s-70s equivalence theory"; Newmark introduced it in 1981. Drop the decade qualifier
  or split the claim. *(equivalence)*
- **S9 — Skill description hygiene (agent-skills).** (a) `meaning-signification-and-equivalence-
  critique` description repeats the same clause verbatim twice — trim. (b)
  `translation-quality-and-applied-studies` sits closest to the sibling
  `translation-quality-reviewer` boundary but carries no tie-breaker sentence like its three
  equivalence-adjacent peers — add one routing "corpus-based QA scoring" to the sibling.
  (c) Four "bundle" skills (`culture-ideology-power-and-rewriting` 21 steps, `hermeneutics…` 19,
  `literal-free-strategy-history…` 17, `translation-quality-and-applied-studies` 15) are flat
  unrouted procedures spanning independent sub-frameworks — add a short "route by concern"
  sub-list so an agent narrows before reading the full checklist. *(agent-skills)*

---

## NICE

- **N1** — Skill description lead-sentence pattern inconsistent across the 12 skills
  ("Use when…" vs "Reviews…" vs imperative). Normalize to one template. *(agent-skills)*
- **N2** — Residual producer-voiced imperatives in invariants (P036, P045, P058 "…or producing
  a translation") rely on one top-of-file override; optional per-line parenthetical
  "(criterion for judging, not an instruction to translate)" on the most action-phrased few. *(ai-agent-eng)*
- **N3** — `quality_bar[5]` cites P014 whose `applies_when` is scoped to literary prose but the
  bullet states loss-naming unconditionally; P115/P138 already carry the general claim → scope
  or drop P014. `quality_bar[4]` leans partly on medium-confidence P020 for a flat rule (P088/
  P040 independently support it). *(faithfulness)*
- **N4** — Domain precision points (all correctly hedged already, optional tightening):
  Catford's paired term "textual equivalence" never named alongside "formal correspondence"
  (P006); P105 genre→F-E/D-E reads more binary than Nida's continuum; P047 explicitation
  "tends always to increase" vs its own contested-support hedge; P150 "principle of charity"
  more standardly Wilson/Davidson than Quine; P107 translatorial action unattributed to
  Holz-Mänttäri; P056 "neutrinos lack mass" is a now-outdated Quine illustration presented
  unframed. *(quality + technical + equivalence)*
- **N5** — `tests/test-results.md` Phase 8 section points at the command rather than recording
  the actual verdict/body-size WARNING line. Inline the output. *(profile)*

MUST_FIX_COUNT: 3
