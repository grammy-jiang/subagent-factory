# Review — `instructional-design-advisor` (round 1)

Package: `subagents/instructional-design-advisor/` (agent_version 1.1.0, 11 sources, 200 principles, 13 skills)
Date: 2026-07-27
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer (release readiness)
+ faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design)

## Deterministic gate results

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL, 1 WARN |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate: `…` ellipsis in skills/adapter | no hits |
| truncation gate: severed invariant parenthetical in adapter | no hits |

WARNs (not must-fix, carried below as should-fix): `quote-scan: rights NOT verified` (11
restricted sources, no `sources/markdown/` and no warm cache module — the verbatim-quote gate
could not actually run); `phase8: Phase 8 self-check WARNING`.

**Note — the truncation gate has a blind spot.** It found nothing, yet 10+ genuine truncations
exist (findings 1 and 2). The generator truncates at a *clean sentence boundary* with a
terminal period and no ellipsis, so neither `…` nor an unterminated `(` is emitted. The gate as
written cannot see this class. See finding 3.

---

## Findings

### 1 — MUST-FIX · Procedure steps truncated mid-clause in 4 skills

**Where:**
- `skills/multimedia-and-elearning-design/SKILL.md:74` — "…and remember that the three demands (P158)." — the three demands are never named.
- `skills/multimedia-and-elearning-design/SKILL.md:75` — "Contiguity principle 1 (P159)." — a bare label, not an instruction; zero operational content.
- `skills/instructional-strategy-and-events/SKILL.md:88` — "…so the definition labels something already seen and the new content is (P032)." — cut after "is".
- `skills/instructional-strategy-and-events/SKILL.md:91` — "…and ensure (P037)." — cut after "ensure".
- `skills/instructional-strategy-and-events/SKILL.md:96` — "…and several sequences are (P054)." — cut after "are".
- `skills/needs-and-context-analysis/SKILL.md:62` — "…job analysis, and authoritative (P095)." — noun missing; `profile.yaml` `always_on` has the complete form ("authoritative procedures").

**Problem:** These are load-bearing `## Procedure` steps that terminate before their clause
completes. A model reading step 15 of the multimedia skill gets the string "Contiguity
principle 1" and no procedure at all. All six verified by direct read.

**Fix:** Regenerate each step from the full source claim / the matching complete prose in
`profile.yaml` `knowledge_partition.always_on` (which holds the untruncated versions), rather
than from a length-capped prefix.

---

### 2 — MUST-FIX · "Anti-patterns to flag" bullets truncated mid-clause across all 13 skills

**Where:** every `## Anti-patterns to flag` section; 90 bullets total (7 per skill, 6 in
`feedback-and-formative-practice` and `motivation-and-learner-engagement`). Verified samples:
- `skills/learning-outcomes-and-taxonomy/SKILL.md:95` — "…require recognition of the problem type, selection or construction." — cut before "of a fitting method, adaptation, and execution".
- `skills/assessment-design-and-authentic-tasks/SKILL.md:108` — "…are valid but less consistently reliable, and separate." — dangling verb, no object.
- `skills/needs-and-context-analysis/SKILL.md:86` — "…through self-performance." — list cut before the remaining four evidence sources.
- `skills/evaluation-transfer-and-impact/SKILL.md:101` — "…and sample the differences most." — cut after "most".

**Problem:** Same root defect as finding 1 (length-capped prefix, terminal period added), but
in the section whose whole job is to state a checkable failure mode. A truncated anti-pattern
is not checkable. Systemic — not a one-off.

**Fix:** Same as finding 1 — take the complete clause. Then add a post-generation assertion
that no `## Procedure` step and no anti-pattern bullet ends on a dangling conjunction,
preposition, or transitive verb before its `(Pxxx)` citation.

---

### 3 — MUST-FIX · `always_on` multimedia rule drops the source's pacing boundary condition (SCOPE_BROADENED)

**Where:** `profile.yaml:170-171`, `knowledge_partition.always_on[5]`
(multimedia-and-elearning-design).

**Rule as written:** "…routes words away from the visual channel by preferring narration to
concurrent on-screen text when a graphic must be processed at the same time."

**Source support:** P157 (`principles/principles.yaml:3486-3491`) states "Prefer narration over
concurrent onscreen text **in a system-paced presentation**", and its own `applies_when` repeats
the same bound. Learner-paced presentation is a documented condition where the modality effect
weakens or reverses.

**Level:** SCOPE_BROADENED — a pacing-conditioned rule rendered unconditioned.

**Why it matters here specifically:** this profile's own `forbidden_behaviours[2]` prohibits
"stating a design principle more strongly than its source supports — omitting the conditions
that make a rule hold". The line violates the profile's own stated prohibition.

**Fix:** append the condition — "…when a graphic must be processed at the same time **in a
system-paced presentation**." Note this text is mirrored into the skill body and the adapter, so
re-export after the profile edit.

---

### 4 — MUST-FIX · `faithfulness-report.yaml` never reviewed the `knowledge_partition.always_on` block

**Where:** `reports/faithfulness-report.yaml` (whole file) vs `profile.yaml:114-283`.

**Problem:** The report covers 19 rule locations — `quality_bar[0-5]`,
`forbidden_behaviours[0-3]`, `when_to_use[0-4]`, `outputs.primary_format`, `handoff_rules[0-1]`,
`source_of_truth_policy.precedence` — and **zero** entries for `knowledge_partition.always_on`.
That block is 13 dense paragraphs compressing all 200 principles, and it is by far the densest
place for a dropped hedge. Finding 3 lives there and was invisible to the report. The block's
apparent "clean" status is *unverified*, not confirmed — this is a coverage gap in the gate,
not merely a mis-verdict.

**Fix:** extend the faithfulness pass to emit a per-entry verdict for
`knowledge_partition.always_on[0]`–`[12]` (per-clause for the denser ones) before the report is
treated as covering the package.

**Independently confirmed clean:** a spot-check of ~34 cited principles across the region the
report *did* cover (P013, P008, P172, P077, P115, P153, P001, P016, P017, P098, P199, P167,
P196, P056, P198, P067, P093, P159, P157, P053, P042, P092, P148, P152, P140, P004, P193, P107,
P096, P109, P011, P122, P100, P090) matched every `WITHIN_SCOPE` verdict. No disagreement in the
reviewed region.

---

### 5 — SHOULD-FIX · Two role-level prohibitions absent from `forbidden_behaviours`

**Where:** `profile.yaml:83-93` vs `:21-22` (role) and `:36-38` (when_not_to_use).

**Problem:** "grades learners" and "rules on subject-matter correctness" are stated in the role
paragraph and in `when_not_to_use`, but — unlike the two other boundaries named in the same
breath ("building the deliverable", "certifying effective/accredited", which *do* get
principle-cited `forbidden_behaviours` entries at `:84-88`) — they never reach the enforcement
list. Asymmetric gap in exactly the two prohibitions this domain most needs enforced.

**Fix:** add two entries mirroring the existing pattern: (a) never assigns a grade or score to a
learner's work — that belongs to the teacher of record; (b) never rules on subject-matter
correctness — refer to a qualified content expert. Cite the principles already used in
`handoff_rules` (P107, P021, P134, P193).

---

### 6 — SHOULD-FIX · `outputs.primary_format` and `minimum_useful_output` never render into the adapter

**Where:** `profile.yaml:47-50` and `:81-82` vs `.claude/agents/generated/instructional-design-advisor.md` (whole file).

**Problem:** Sibling fields at the same level (`inputs.required`, `outputs.modes`) do get
template slots and appear in the adapter at `:202-228`, so this reads as an incomplete render,
not a deliberate omission. Most of the content is redundantly covered by Forbidden behaviours
(`:249, :251`), but the "never a bare good/bad verdict" constraint is unique to the dropped
field and appears nowhere in what the model actually sees.

**Fix:** add a template slot rendering `outputs.primary_format` and `minimum_useful_output`, or
strike the fields from `profile.yaml` so canonical and adapter don't drift.

---

### 7 — SHOULD-FIX · `quote-scan` rights gate could not actually run

**Where:** validator WARN — "rights NOT verified — 11 restricted source(s) but no source text
available (no `sources/markdown/`, no warm cache module)".

**Problem:** All 11 sources are `distillation-only`, meaning no verbatim quotation is permitted
anywhere in generated artifacts (`.claude/rules/rights-and-quotation-policy.md`). The
`quote_scan PASS` above is vacuous: it had no source text to compare against. The rights
obligation is currently unverified for the highest-risk source class.

**Fix:** warm the source-markdown cache (or restore `sources/markdown/`) and re-run
`python -m tools.subagent_factory.quote_scan subagents/instructional-design-advisor` so the
40-consecutive-word gate actually executes before release.

---

### 8 — SHOULD-FIX · Adapter always-on layer is ~90 invariant bullets loaded on every invocation

**Where:** `.claude/agents/generated/instructional-design-advisor.md:21-174`.

**Problem:** ~3,000+ words of principle bullets load regardless of which of the 13 skills the
task touches — a rubric review pulls in multimedia-channel invariants (P157-P160) just as a
needs-analysis task pulls in motor-skill sequencing (P028). It is by far the largest adapter
section and duplicates material the 13 progressively-disclosed SKILL.md files already carry in
more depth. Undercuts the progressive-disclosure design the package otherwise implements well.

**Fix:** tier it — promote only the ~15-20 genuinely cross-cutting invariants (backward-design
order, evidence-of-learning standard, taxonomy discipline, the "conditions bound the rule"
caveat) to always-on; leave the rest in their owning skill file, loaded on demand.

---

### 9 — SHOULD-FIX · Anti-pattern lists capped at 7 bullets regardless of skill size

**Where:** `skills/instructional-strategy-and-events/SKILL.md:127-133` (7 of 35 principles,
20%); `skills/assessment-design-and-authentic-tasks/SKILL.md:103-109` (7 of 23, 30%);
`skills/active-learning-and-group-formats/SKILL.md:91-97` (7 of 17, 41%).

**Problem:** A fixed cap means the largest, most-used skills get the *thinnest* anti-pattern
checklist, while small skills reach near-full coverage by accident of size.

**Fix:** either cover all principles in the skill, or deliberately curate the highest-impact
subset — don't truncate at a constant.

---

### 10 — SHOULD-FIX · Three Procedure steps restate a principle label with no operational detail

**Where:** `skills/active-learning-and-group-formats/SKILL.md:70` ("Design PBL from its intended
outcomes (P139)."), `:74` ("Align the whole PBL system (P175)."), `:76` ("Teach research as
distinct judgments and procedures (P177).").

**Problem:** Distinct from the truncation defect — these are complete sentences that carry no
procedure. Neighbouring steps run 3–4 clauses; these say what to do without saying how.

**Fix:** expand from the source claim text to match neighbouring density.

---

### 11 — SHOULD-FIX · `source_of_truth_policy.canonical_owner` carries no principle citations

**Where:** `profile.yaml:102-106` vs `provenance-ledger.md:7-8`.

**Problem:** The ledger claims *every* `source_of_truth_policy` value cites the principle it
restates, carving out only `role`/`when_to_use`/`inputs`/`outputs`. `canonical_owner` cites
nothing, while its sibling `precedence` (`:108-113`) cites P013, P172, P011, P122, P107, P193.
Either an orphan field value (against the rights-and-quotation-policy "no orphan field values"
rule) or an overstated ledger claim.

**Fix:** add citations to `canonical_owner`, or narrow the ledger's carve-out at
`provenance-ledger.md:9-10` to also exclude it as a real-world-authority statement.

---

### 12 — SHOULD-FIX · No `description` in SKILL.md frontmatter (all 13 files)

**Where:** frontmatter of every `skills/*/SKILL.md` — carries `name`, `kind`, `status`,
`provenance` only.

**Problem:** Triggering rests entirely on the in-body `## When to use` prose. Fine if these are
subagent-internal, but it diverges from the Agent Skills discovery contract, where `description`
is the load-time triggering signal.

**Fix:** add `description` if the skills are meant to be portable/standalone-loadable; otherwise
record explicitly that they are subagent-internal, so a future reviewer doesn't read it as an
oversight.

---

### 13 — SHOULD-FIX · `instructional-strategy-and-events` bundles 35 principles into one skill

**Where:** `skills/instructional-strategy-and-events/SKILL.md` — 35 procedure steps spanning
nine-events checklist, concept/rule/verbal-information/attitude/motor-skill technique matching,
scaffolding, spaced retrieval, and time budgeting. 5–6× the size of most siblings (which cover
6–23 principles around one coherent sub-topic).

**Fix:** split into e.g. `instructional-events-and-sequencing` + `outcome-type-technique-matching`,
or at minimum add `###` sub-headers grouping the 35 steps by theme.

---

### 14 — NICE · Full 11-source citation list repeated verbatim in all 13 skill Provenance sections

**Where:** e.g. `skills/feedback-and-formative-practice/SKILL.md:82` lists all 11 book titles for
a skill drawing on 6 principles; the identical ~130-word block appears in every file, directly
after a `## References` section that already points to the shared index.

**Fix:** reduce Provenance to the principle-id list plus a pointer to
`references/instructional-design-principles-index.md`.

---

### 15 — NICE · Duplicate step inside `teaching-scholarship-and-quality`

**Where:** `skills/teaching-scholarship-and-quality/SKILL.md:61` (step 8, P162) vs `:60` (step 7,
P134) — step 7 already fully describes the iterative evidence cycle.

**Fix:** merge, or differentiate what P162 adds beyond P134.

---

### 16 — NICE · `when to use` overlap between two sibling skills

**Where:** `skills/learning-outcomes-and-taxonomy/SKILL.md:57` vs
`skills/teaching-for-understanding-and-transfer/SKILL.md:56` — both lead on "transfer".
Distinguishable on close read (outcome-statement wording vs instruction evaluation), but a model
skimming triggers could hesitate.

---

### 17 — NICE · Role paragraph verb reads as build authority

**Where:** `.claude/agents/generated/instructional-design-advisor.md:19` / `profile.yaml:19` —
"helps… prototype materials". Defused by the immediately-following override clause and by
`forbidden_behaviours` (`:249`), so low risk.

**Fix:** reword to "advises on prototyping materials".

---

### 18 — NICE · `multisource_synthesis: deferred` unexplained

**Where:** `profile.yaml:7`. No note anywhere says what "deferred" signals for an 11-source
fold-in-built package. A later reviewer can't tell stale template field from intentional flag.

**Fix:** add a one-line note in the ledger, or drop the field if no downstream tool reads it.

---

## Confirmed clean

- **Deterministic:** validator 0 FAIL; adapter-sync, adapter-fresh, adapter-quality, injection-scan, tier-consistency, all 11 anchor files, all 13 skills + 2 references authored, all 15 stale-maintenance checks (grounding unchanged).
- **Agent design (adapter):** role coherence; tool boundary (`Read, Grep, Glob` at `:4`, no instruction in the body requires a tool the agent lacks); authority creep well defended — `forbidden_behaviours` at `:246-256` blocks building deliverables, certifying effectiveness/accreditation/competence, and treating enrolment/satisfaction/engagement as evidence of learning; when-to-use / when-not-to-use routable at `:176-199`; DO-NOT-EDIT header present at `:8-15`; no contradiction between always-on and mode/skill layers.
- **Profile release readiness:** role crisp and single; `agent_version 1.1.0` matches ledger Version History; 200-principle / 7860-claim / 13-skill figures consistent across profile and ledger; `always_on` has exactly 13 entries matching the 13 skill slugs; all 11 sources `rights_status: distillation-only`, matching the ledger 1:1 including the documented `mayer-multimedia-lea-*` rename; supersession rule respected. `quality_bar` bullets all checkable and principle-cited. Modes advise/review/plan each give trigger + output shape.
- **STANDING subagent-independence rule:** clean — no sibling subagent is named in `router_description`, `when_not_to_use`, or `handoff_rules`; every exclusion is stated by capability.
- **Skill lens-fit:** clean — every skill's `## Output` restates the advise-don't-build boundary matching `forbidden_behaviours`; no Procedure step instructs the agent to author a deliverable.
- **No placeholder text:** TODO / PLACEHOLDER / TBD / FIXME / XXX — zero matches across all 13 skills.
- **Skill partition:** maps cleanly to `knowledge_partition` with non-overlapping principle sets.

MUST_FIX_COUNT: 4
