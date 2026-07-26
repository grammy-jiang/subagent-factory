# Review — `instructional-design-advisor` (round r1)

Package: `subagents/instructional-design-advisor/` (agent_version **1.3.0**, tier 2, 11 sources, 200 principles, 13 skills)
Date: 2026-07-27
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer (release readiness)
+ faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design)

> This path previously held the round-1 report against **v1.1.0**; that content is superseded and
> overwritten here per the review instruction. Its findings (mid-clause truncation in 4 skills,
> etc.) were addressed by the 1.2.0/1.3.0 rounds — re-checked below and no longer present.

Every must-fix below was re-verified by the consolidator with direct greps, not accepted on the
reviewing agent's word.

## Deterministic gate results

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate: `…` ellipsis in skills/adapter | no hits |
| truncation gate: severed invariant parenthetical in adapter | no hits |
| adapter-sync / adapter-fresh / injection-scan / stale-maintenance | all OK |

Non-fatal: `phase8: Phase 8 self-check WARNING` — carried below as should-fix #4 (body-size 994w).

**Deterministic FAIL count: 0.**

Follow-up on the previous round's gate blind spot (truncation at a clean sentence boundary, which
emits neither `…` nor an unterminated `(`): re-probed with a dangling-connective pattern
(`such as|including|e.g.|rather than|so that|which|the` immediately before a terminal period)
across all 13 `SKILL.md` files — **no hits**. That class appears repaired. The gate's inability to
see it remains a factory-level weakness, not a package defect.

---

## must-fix

### 1 — MUST-FIX · 11 of 13 `SKILL.md` files end with a stray unmatched `</content>` tag

**Where:** `skills/*/SKILL.md`, final line of each —
`active-learning-and-group-formats:110`, `assessment-design-and-authentic-tasks:126`,
`backward-design-and-constructive-alignment:107`, `evaluation-transfer-and-impact:116`,
`feedback-and-formative-practice:87`, `iterative-prototyping-and-development:96`,
`learning-outcomes-and-taxonomy:109`, `motivation-and-learner-engagement:87`,
`multimedia-and-elearning-design:109`, `needs-and-context-analysis:99`,
`teaching-for-understanding-and-transfer:112`.

**Problem:** Verified — `grep -rln '</content>' skills/*/SKILL.md` returns 11 files. Each ends in a
closing `</content>` with no opening tag anywhere in the file: an unstripped authoring-wrapper
delimiter leaked from the skill-author step into the shipped skill body. `instructional-strategy-and-events`
and `teaching-scholarship-and-quality` are clean, so the post-processing ran but missed 85% of the
set. These bodies load verbatim into model context at trigger time, so a dangling XML-ish tag is
uninterpretable noise in every one of them. `validate_generated_package` does not catch it.

**Fix:** Strip the trailing `</content>` line from all 11 files so each ends at its "Derived from …"
provenance sentence. Add a generation-pipeline/validator check that FAILs on an unmatched
`<content>`/`</content>` (or any unmatched wrapper tag) in an exported `SKILL.md`, so the next
fold-in or regen cannot reintroduce it silently.

### 2 — MUST-FIX · `provenance-ledger.md` tail is a colorized-diff paste — 38 raw ANSI escape sequences

**Where:** `provenance-ledger.md:180-218` (file is 218 lines; ANSI runs from 180 to EOF).

**Problem:** Verified — `grep -c $'\x1b' provenance-ledger.md` → 38, all within 180-218, and it is the
only file in the package containing ANSI bytes. The block is a terminal-colorized `git`/`delta` diff
of the 1.3.0 edit pasted straight into the canonical ledger, producing a second, control-character-laden,
reworded restatement of the 1.3.0 Version History entry that already exists cleanly at lines 132-179.
The ledger is the canonical audit record under `.claude/rules/generated-artifact-policy.md`: ANSI bytes
break plain-text tooling (grep/diff/quote_scan) run against it, and the duplicate gives one version two
inconsistent histories — the corrupted copy also drops the precise `profile.yaml:179` locator the clean
copy carries.

**Fix:** Delete lines 180-218; the clean 1.3.0 entry at 132-179 already covers the content. Verify
`grep -c $'\x1b' provenance-ledger.md` → 0 before release. Root cause is the known ANSI-paste class
(colorized command output captured into file content) — compose ledger entries with the Write tool or
`git --no-color`.

### 3 — MUST-FIX · `reports/faithfulness-report.yaml` is stale — 4 entries describe citations v1.3.0 no longer has

**Where:** `reports/faithfulness-report.yaml:131-138` (`handoff_rules[0]`), `:148-156`
(`source_of_truth_policy.precedence`), `:344-355` (`forbidden_behaviours[4]`), `:366-377`
(`source_of_truth_policy.canonical_owner`) — vs `profile.yaml:98-101`, `:116-121`, `:93-95`, `:105-114`.

**Problem:** Verified by direct comparison of both files. The 1.3.0 adversarial-verify round removed
`P107`/`P134` from these sites; the report was last regenerated at 1.2.0 and still describes the pre-fix
state:

- report:137 — `handoff_rules[0]` "Restates **P107**/P021/**P134**"; profile:101 now cites `(P021)` only.
- report:154 — `precedence` "Restates P013/P172/P011/P122/**P107**/P193"; profile:116-121 has no `P107`.
- report:353 — `forbidden_behaviours[4]` "**P107** … is a weak, tangential citation here"; profile:95
  cites `(P021, P172)` — no `P107` is present to be tangential about.
- report:372-374 — quotes `canonical_owner` as *"The teacher of record and the design team hold final
  authority over the course…(P107, P134)"*; profile:106-109 now **splits** that: `(P107, P134)` attaches
  to the "makes the teaching theory explicit / adapts through evidence-grounded cycles" practice clause,
  and the authority sentence is deliberately uncited. The quoted sentence structure no longer exists.

The faithfulness report is the tier-2 artifact of record for whether shipped rules over-claim. A reader
trusting it would believe a mis-citation is still live at four sites when it was fixed, and would be
reading the wrong text for `canonical_owner`.

**Fix:** Regenerate the report against the current profile (or hand-edit these four entries), using the
`"REPAIRED in 1.x.0 … Now WITHIN_SCOPE"` note pattern already used for the
`knowledge_partition.always_on[1]/[3]/[4]` entries, so the 1.3.0 repair is recorded rather than leaving
pre-fix prose in place. Add "regenerate faithfulness report" to the version-bump checklist — a profile
citation edit that skips it is the recurring failure mode this finding represents.

---

## should-fix

### 4 — SHOULD-FIX · Profile body 994 words — 6 words below the hard-FAIL cap (the phase8 WARNING)

**Where:** `profile.yaml` (fields summed by `profile_self_check` check 14); heaviest —
`forbidden_behaviours` 198w, `quality_bar` 163w, `modes` 128w.

**Problem:** Confirmed by running the check directly:
`[WARNING] 14. body-size: profile body ~994 words (> 800); 194 over the 800-word budget`.
Soft budget 800, WARN band 801-1000, hard FAIL >1000. At 994 the package has a **6-word margin** — any
future citation or clause addition trips a hard FAIL and blocks validation. The ledger's 1.2.0 entry
records trimming to "~987 words to stay inside the budget" but never states that the residual WARNING is
a known, accepted release state, so the next reviewer must re-derive it.

**Fix:** Trim `forbidden_behaviours` and `quality_bar` (each bullet can shed a clause without losing a
`P`-id) to restore real headroom — ideally under 800. If the WARNING is accepted as-is, add one ledger
line saying so and why, and flag the 6-word margin as a maintenance hazard.

### 5 — SHOULD-FIX · Adapter cites ~30 principle IDs whose text never appears in the loaded prompt

**Where:** `.claude/agents/generated/instructional-design-advisor.md` — Quality bar `:233-243`,
Forbidden behaviours `:249-259`, Handoff rules `:265-267`, Worked examples `:277,:284`,
Source-of-truth policy `:289-291`.

**Problem:** Spot-verified against the bracket form `[Pnnn]` used by the printed invariants list: P096,
P109, P148, P187, P021, P193, P107 each appear 1-5× in the body and **0×** as a defined invariant. The
printed "Operating invariants (must hold)" list (`:26-174`) covers only a curated subset. So the two
highest-authority sections — Quality bar and Forbidden behaviours, the material defining what "good"
means and what the agent must never do — cite principle numbers whose content the model never sees, and
the worked examples model the behaviour of citing them ("per P096, P109"). At runtime the agent can
attach a fabricated or misremembered gloss to a real-looking citation. The "Canonical package" pointer
(`:293-331`) exists but is phrased as optional ("For deeper context, read…"). This is a citation-apparatus
completeness gap, not a content-faithfulness one — the plain-English rule text stands alone and stays
obeyable.

**Fix:** Either (a) add a compact one-line-gloss appendix covering every ID cited outside the invariants
list, or (b) — cheaper, and preferred given #4's body-size pressure — add one preamble line: *"If you cite
a principle ID not defined above, Read the principles-index reference first and quote its stated content;
never assert from memory what an ID says."* The change belongs in `profile.yaml` / the render template and
must be re-exported; never edit the generated adapter (`generated-artifact-policy.md`).

### 6 — SHOULD-FIX · `forbidden_behaviours[0]` stretches `P193` onto a clause it does not ground

**Where:** `profile.yaml:83-85` — *"…the advisor supplies review criteria and the practitioner makes the
teaching theory and the design their own **(P193, P107)**"*; cf. `faithfulness-report.yaml:52-58`.

**Problem:** `P193` is specifically about giving a **qualified content expert** validated goals and skill
frameworks as explicit review standards for **subject-matter correctness** — used correctly for exactly
that at `forbidden_behaviours[5]` and `handoff_rules[1]`. Here it is stretched to cover the general
"the advisor supplies review criteria rather than building the deliverable" boundary, which no current
principle states. Same category as the tangential-`P107` citations the 1.3.0 round removed at four other
sites; this instance was missed, and the report marks the entry `WITHIN_SCOPE` with no note on `P193`'s
fit. Not a strength over-claim (the clause is an advisory *restriction*, so a weak citation cannot make it
stronger than source), hence should-fix rather than must-fix.

**Fix:** Drop `P193` from `forbidden_behaviours[0]` — `P107` already grounds the "practitioner makes the
teaching theory their own" half — and let the advisor-boundary half stand as uncited factory policy,
consistent with how 1.3.0 treated the analogous `canonical_owner` ownership clause. Record the carve-out
in the ledger (see #7).

### 7 — SHOULD-FIX · Uncited ownership clause in `canonical_owner` is correct but not declared an accepted exception

**Where:** `profile.yaml:107-109` — *"final authority over the course, its materials, and what is taught
rests with the teacher of record and the institution"* (no `P`-id).

**Problem:** `.claude/rules/rights-and-quotation-policy.md` requires every profile field be traceable to a
source and QID ("No orphan field values"). This clause is deliberately uncited — 1.3.0 removed a wrong
`(P107, P134)` rather than substituting a false one, which was the right call — but the ledger explains it
only as inline changelog prose ("uncited as policy"), never declaring it an accepted structural-policy
exception. The next reviewer cannot distinguish "intentional carve-out" from "orphan gap". The same
ambiguity will apply to the #6 fix.

**Fix:** Add one ledger sentence declaring that advisor-boundary / ownership statements (the
`canonical_owner` authority clause, and `forbidden_behaviours[0]` once #6 is applied) are factory-level
structural policy — the same category as the advice-only boundary applied to every specialist package —
and therefore exempt from per-principle QID citation.

### 8 — SHOULD-FIX · `instructional-strategy-and-events` loads 35 principles on any trigger

**Where:** `skills/instructional-strategy-and-events/SKILL.md:80-161` (`## Procedure`, 35 numbered steps
across 5 `###` subsections).

**Problem:** ~2× the next-largest sibling (23 in `assessment-design-and-authentic-tasks`; package median
~15-17). The `###` structure (nine-events frame / sequencing / technique-matching / scaffolding / time
budgeting) helps scanability, but the whole body still loads on any trigger, including a request touching
only one subsection. Cuts against progressive disclosure, which the package's own P001/P003/P007/P022/P079
endorse.

**Fix:** Consider splitting along the existing `###` seams — e.g. `instructional-sequencing-and-events`
(nine-events + sequencing/prerequisites, ~17 principles) and `technique-matching-and-scaffolding`
(outcome-type matching + scaffolding/practice/retrieval + time budgeting, ~18 principles), each with its
own scoped description. **Caveat:** a split breaks the 13-skill ↔ 13 `knowledge_partition.always_on` 1:1
mapping and forces a profile edit under #4's body-size pressure — weigh against deferring to a later
version.

### 9 — SHOULD-FIX · `outputs.primary_format` and `minimum_useful_output` render nowhere in the adapter

**Where:** `profile.yaml:46-49`, `:80-81`.

**Problem:** Per the ledger's 1.2.0 entry (reaffirmed "recorded, no action" at 1.3.0), the adapter template
has no slot for these two fields; their distinctive "never a bare good/bad verdict" content was duplicated
into each `outputs.modes[*].output` so it would reach the model. They now exist mainly to satisfy phase8
checks 6 and 8 (non-empty) while consuming body-size budget (#4) for content the runtime never sees.
Correctly deferred — a factory-level template gap, not a package defect.

**Fix:** No package change required. Keep flagging it at every version bump until the shared adapter
template gains a slot, so it is not silently forgotten. If trimming for #4, this duplicated content is the
cheapest place to cut.

---

## nice

- `skills/assessment-design-and-authentic-tasks/SKILL.md:105` — the only skill whose curated-subset
  disclaimer uses a Markdown link `[Procedure](#procedure)`; the other 12 use plain-text `## Procedure`.
  Anchor is valid; purely stylistic. Normalize to the 12-file majority.
- Skill frontmatter `description` across all 13 skills — about half carry an explicit "use when / triggers
  when" clause, half rely on the capability verb phrase alone. None are vague and all fire correctly, but
  descriptions are the sole triggering signal, so uniformity is worth an eventual pass.
- `.claude/agents/generated/instructional-design-advisor.md:3` — routing description opens with twelve
  comma-separated topic nouns before any usage trigger. Coherent (all twelve map to this profile's own
  skills), but scenario-first framing routes task-shaped borderline requests better. Optional; the trailing
  "Use when / Not for" clauses already carry the operative signal. Any change goes in `profile.yaml` +
  re-export.
- `profile.yaml:332-335` (example 2) — paraphrase of P062 drops "learning" from its six-item list
  ("relevance, **learning**, permission, support, resources, adaptation opportunity"). An omission, not an
  over-claim.

---

## Checked clean (recorded so a later round need not re-derive)

- **Subagent independence** — verified across profile and adapter: `when_not_to_use`, `handoff_rules`,
  `router_description`, and adapter body name only human/institutional roles (teacher of record,
  institution, accrediting body, qualified content expert). No `routes to <other>-advisor`. The one
  `-advisor|route` grep hit in the adapter is domain content (P157, "route words away from the visual
  channel").
- **Tool boundary** — write/build/produce/edit verbs in the adapter body are all either the caller's
  deliverable (explicitly declined at `:193`, `:280-284`) or quoted domain content. Nothing implies a tool
  beyond `Read, Grep, Glob`.
- **Authority creep** — `forbidden_behaviours` bars building the deliverable, certifying
  effectiveness/accreditation, grading learners, and ruling on subject-matter correctness; matches the
  frontmatter "Not for" clause in substance, with no contradicting section elsewhere.
- **Adapter structural integrity** — `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->` present in the first
  20 lines with correct source-package / profile / regenerate-command / version / timestamp fields; no
  severed instruction lines on a full read; the "eleven sources" role claim matches the 11-entry `sources:`
  list.
- **Renumbering hazard (the known fold-in trap)** — every inline `(Pxxx)` group in `quality_bar`,
  `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy`, both worked examples, and the two
  densest `always_on` blocks was checked against the actual principle statements. **No wrong-principle
  citation survived the 1.1.0 renumber** — the re-derivation against P001–P200 was done correctly.
  (Findings #3 and #6 are citation *currency* and citation *fit*, not renumber drift.)
- **Skill ↔ principle integrity** — every skill's frontmatter `provenance.principles` matches its inline
  `(Pxxx)` citations exactly; no orphaned or invented IDs; no principle ID duplicated across skills.
- **Cross-references** — both `references/*.md` exist and are populated; the relative path resolves from
  every skill directory. No dead links.
- **Lens fit** — the 13 skills map 1:1 to the 13 `knowledge_partition.always_on` blocks in order; siblings
  with overlap risk disambiguate each other explicitly in "When to use".
- **Version consistency** — `agent_version: 1.3.0` matches the ledger Version History (1.0.0 → 1.1.0 →
  1.2.0 → 1.3.0, each substantive, none silently overwritten) and `CHANGELOG.md [1.3.0]`.

---

## Fix ordering note

#1, #2, #3 are mechanical and independent — none touches `profile.yaml`, so none re-triggers the 6-word
body-size margin in #4. Apply them first. #4 / #6 / #7 / #9 all edit `profile.yaml` and must be batched
into one MINOR-or-PATCH bump + `cli export` + `validate`; #8 rides that same bump if taken at all.

MUST_FIX_COUNT: 3
