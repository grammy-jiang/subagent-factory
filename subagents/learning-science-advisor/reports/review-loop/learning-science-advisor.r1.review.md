# Review — learning-science-advisor (round r1)

Package: `subagents/learning-science-advisor/` · profile `agent_version: 1.3.1` · status `ready`
Date: 2026-07-27 · Mode: review only — no file changed except this report.
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer
(release-readiness) + faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design).

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL. 1 `[WARN] quote-scan` (rights NOT verified — 12 restricted sources, no source text available), 1 `[OK] phase8: Phase 8 self-check WARNING` |
| `quote_scan` (standalone) | **PASS** — no potential verbatim quotation found (but see F2: it ran with no source text to scan) |
| truncation gate — `…` ellipsis in 15 SKILL.md + adapter | clean, 0 hits |
| truncation gate — severed invariant parenthetical in adapter | clean, 0 hits |

Deterministic FAILs: **0**.

---

## Findings

### must-fix

**F1 · stray generation artifact in a skill body**
`skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:119` · **must-fix**

Problem: the file's last content line is a bare, unmatched `</content>` tag — an unstripped
tool-output wrapper left by the generation pipeline. Not inside a code block, not valid Markdown.
Verified by grep across all 15 skills and both references: this is the **only** occurrence in the
package, so it is a one-off leak rather than a template defect.

Fix: delete line 119 so the file ends after the Provenance paragraph. Re-run
`validate_generated_package` afterwards — grounding digests are content-hashed, so confirm
`stale-maintenance: skill:cognitive-load-worked-examples-and-scaffolding` still reports "grounding
unchanged" and re-stamp if it does not.

**F2 · `status: ready` while the rights gate is on record as unexercised**
`profile.yaml:5` vs `provenance-ledger.md:173-177` · **must-fix** (dedups with the validator's
`[WARN] quote-scan` and with the `phase8 self-check WARNING`)

Problem: all 12 sources are `rights_status: distillation-only` (paraphrase-only, no verbatim
quotation permitted). The validator warns `rights NOT verified — 12 restricted source(s) but no
source text available (no sources/markdown/, no warm cache module); verbatim-quote gate could not
run`, which means the standalone `quote_scan` PASS above is vacuous — it had nothing to compare
against. The ledger's own 1.3.0 entry says so explicitly: "**S3 remains open and unclosed** … the
rights gate is still unexercised and must be run once in an environment holding the source markdown
before release." The 1.3.1 entry never closes it, yet `status: ready` asserts release-readiness.
This is precisely what the Phase 8 self-check WARNING marks.

Note for the fixer: **this is not fixable by editing package files.** It needs either (a) an
environment holding the source markdown, or (b) an explicit decision to keep `status: ready` with S3
deferred, recorded in the ledger. A prior review round classified it as an environment limitation and
did not count it; it is counted here because `status: ready` + the ledger's own "must be run before
release" wording are in direct conflict, and that conflict is a package-level statement, not an
environment fact.

Fix: rehydrate `sources/markdown/` (or the warm MAP cache module), re-run
`python -m tools.subagent_factory.quote_scan subagents/learning-science-advisor` for real, and add a
Version History entry recording the result. If that is not possible in this worktree, add a ledger
entry that states the deferral and its owner, so `status: ready` stops silently contradicting S3.

**F3 · authored-field exception table is incomplete and self-contradicting**
`provenance-ledger.md:12-22` · **must-fix**

Problem: the ledger claims every profile field cites the principle it restates, then lists
"**Six fields**" as authored exceptions (`quality_bar[6]`, `forbidden_behaviours[5]`, `[6]`, `[7]`,
`handoff_rules[2]`, `source_of_truth_policy.canonical_owner`). But `forbidden_behaviours[0]`
(`profile.yaml:92-93`) and `forbidden_behaviours[2]` (`profile.yaml:96-97`) also carry zero P-codes —
the ledger's own 1.2.1 entry (`provenance-ledger.md:183`, `:189`) records superseding their citations
`(P010, P077)` and `(P128, P087)` with `(authored scope boundary)` and never added the table rows.
There are therefore **eight** uncited fields, two of them undocumented — an orphan-field gap against
`.claude/rules/rights-and-quotation-policy.md` ("Every profile field must be traceable to a source and
QID. No orphan field values").

Fix: add table rows for `forbidden_behaviours[0]` and `forbidden_behaviours[2]` (same
authored-scope-boundary rationale already used for `[6]`/`[7]`) and change "Six fields" → "Eight
fields". While there, state the table's inclusion rule precisely — *fully* authored (zero citations
anywhere) belongs in the table; *mixed* fields (partial citation + partial authored tag, e.g.
`handoff_rules[0]`, `[1]`) correctly stay out — so future audits are mechanical rather than manual.
That missing rule is the root cause of this recurrence.

---

### should-fix

**F4 · adapter Operating Invariant P100 licenses individual clinical assessment, contradicting the role boundary**
`.claude/agents/generated/learning-science-advisor.md:102` vs `:3`, `:153`, `:219` · **should-fix**

Problem: P100 sits in *Operating Invariants* — a layer the adapter itself says "take[s] precedence
over the softer guidance below" — and reads "When advising on assessment for a persistent reading
difficulty, recommend real-word reading, spelling ability and word attack skills as the diagnostic
measures to collect…". That is imperative individual-learner diagnostic advice, sitting directly
against `router_description` ("Not for diagnosing a learning disability or clinical condition"),
`when_not_to_use` ("The caller wants a learner assessed, diagnosed, or labelled") and
`forbidden_behaviours` ("Diagnosing a learner … is forbidden"). Only the precedence clause at line 23
("the role's stated boundary and Forbidden behaviours always win") resolves it — a resolution a model
can misapply under a plausible framing ("what should we test my child's reading difficulty for?").

Fix: rescope P100's statement at the source (profile / principle text) so no override is needed, e.g.
"When a school or curriculum team designs what a *reading-intervention programme* screens for, cite
real-word reading, spelling, and word-attack skill as the evidence-supported measures — refer an
individual learner's diagnosis to a qualified assessor." Re-export the adapter after the edit.

**F5 · P100 is charter-orphaned and lens-misfit in its skill**
`skills/expertise-development-and-transfer/SKILL.md:15` (frontmatter `provenance.principles`) and
`:79-80` (Procedure step 2) · **should-fix**

Problem: the skill's lens is matching support to growing expertise and validating transfer claims,
but step 2 recommends a foundational-literacy diagnostic (real-word reading / spelling / word attack).
`profile.yaml`'s `knowledge_partition.always_on` bullet for this skill lists
P005/P009/P018/P039/P104/P108/P117/P122/P128/P131 — **P100 is absent**, and P100 appears nowhere else
in `profile.yaml` (`quality_bar`, `forbidden_behaviours`, `examples` all clean). Charter and skill
disagree on scope. Same root cause as F4.

Fix: relocate the P100-grounded content to a skill whose lens covers prerequisite/diagnostic
assessment (`prior-knowledge-prediction-and-misconceptions` or
`cognitive-load-worked-examples-and-scaffolding` are the closer fits), or — if it truly belongs here —
add a matching clause to the profile's `always_on` synthesis for this skill. Relocation is preferred:
it also removes F4's adapter contradiction at the source.

**F6 · `handoff_rules[1]` omits "promotion", breaking a three-way parallel clause**
`profile.yaml:112-114` · **should-fix**

Problem: `when_not_to_use[2]` (`profile.yaml:39`) and `forbidden_behaviours[2]` (`profile.yaml:96`)
both enumerate "placement, grading, admission, promotion, or employment". `handoff_rules[1]` — the
clause assigning that decision set to the responsible body — lists only "placement, grading,
admission, and employment" (verified: `grep -n promotion profile.yaml` hits only lines 39 and 96).
Promotion decisions are forbidden and out of scope, but no rule names who owns them.

Fix: add "promotion" to `handoff_rules[1]` so all three parallel clauses enumerate the same set.
PATCH version bump + re-export the adapter.

**F7 · no defined fallback when a cited principle code cannot be looked up**
`.claude/agents/generated/learning-science-advisor.md:171` (Required inputs) vs `:199-211` (Quality
bar) and `:26-133` (Operating invariants) · **should-fix**

Problem: `quality_bar` and `forbidden_behaviours` cite codes (P013, P126, P107, P028, P067, P047,
P136, P053, P033, P140, P070, P099) that are **not** in the rendered Operating Invariants list. Line
171 correctly instructs the agent to read the statement in the matching skill file or
`references/learning-science-principles-index.md` before citing — but specifies no behaviour if that
lookup fails (package deployed standalone via `cli export-deployable` without its `skills/` siblings,
file moved, read denied). Silent failure is then the only defined outcome, which makes those
safeguards uncheckable from the adapter text alone.

Fix: append to that instruction — "If the code's source text cannot be located, state the point in
plain language without the citation; never cite from memory, and never drop the safeguard."

**F8 · shared boilerplate duplicated verbatim across all 15 skills**
all `skills/*/SKILL.md`, `## Output` and `## Provenance` sections (e.g.
`retrieval-practice-and-low-stakes-quizzing/SKILL.md:91-93`,
`collaborative-and-peer-learning/SKILL.md:95`) · **should-fix**

Problem: (a) the entire `## Output` paragraph and the second `## Inputs` bullet are byte-for-byte
identical in all 15 files and duplicate `profile.yaml`'s `outputs.primary_format` / `quality_bar`
output floor; (b) every `## Provenance` restates the full 12-source bibliography verbatim (~100 words),
already carried by `provenance-ledger.md` and `references/learning-science-evidence-notes.md`. In the
5–6-principle skills this boilerplate rivals the substantive procedure in length. DRY violation and
pure context cost at every invocation.

Fix: keep only the skill-specific first `Inputs` bullet plus any skill-specific output nuance, and let
the profile carry the shared output contract. Collapse each `## Provenance` to "Derived from P0xx,
P0yy…; full source grounding in `provenance-ledger.md` and
`references/learning-science-evidence-notes.md`."

**F9 · 1.3.1 ledger entry drops the body-size confirmation**
`provenance-ledger.md:67-113` · **should-fix**

Problem: every prior version entry closes with the measured body word count against the ≤1000-word
`phase8 check 14` threshold ("Final body: 991 words" at 1.3.0, `:149`; "Final body: 998 words" at
1.2.1, `:210`). The 1.3.1 entry reworded two clauses and dropped a citation but records no word
count — no on-record confirmation that this version clears the gate. Given the 1.3.0 margin was 9
words, that is a real audit regression, not a formality.

Fix: append the current body word count to the 1.3.1 entry and keep the convention for every future
entry.

**F10 · faithfulness report does not cover `outputs.modes[*].trigger`**
`reports/faithfulness-report.yaml` · **should-fix**

Problem: the report has `rule_ref` entries for all three `outputs.modes[*].output` values but none for
the three `.trigger` values, which the faithfulness-review skill names as in-scope. Reading the trigger
text directly: none over-claims (plain routing prose, no source-attributed content), so this is an
audit-trail completeness gap rather than a live over-claim.

Fix: add three `rule_ref` entries for the triggers, graded the way the authored boundary fields are
(no source-attributed claim → not gradable as over-claim).

---

### nice

**F11 · skill slug sits exactly on the 48-char limit** —
`skills/development-diversity-and-individual-differences/SKILL.md:2`. 48 chars, zero margin; the only
one of the 15 at the boundary (next-longest is 46). Consider
`development-diversity-individual-differences` (45) for margin.

**F12 · only 1 of 15 skill descriptions states a "not X" boundary** — only
`evidence-appraisal-and-learning-myths` disambiguates itself. Surface vocabulary collides across
`cognitive-load-worked-examples…` / `elaboration-examples…` ("examples") and across the four
practice/study skills ("study", "practice"). Not observed to misfire — the descriptions are
substantively distinct — but a trailing "not …" clause on the highest-collision pairs would harden
triggering.

**F13 · `router_description` is a ~165-word single paragraph** —
`.claude/agents/generated/learning-science-advisor.md:3` / `profile.yaml:8-18`. Accurate, and its
exclusions are load-bearing for correct decline behaviour, but the 15-clause "covers" enumeration works
against the router-matching purpose of front matter. Consider collapsing the covers list to ~5 category
names and letting `when_to_use` carry the detail. Keep the exclusions verbatim.

**F14 · faithfulness report omits `router_description` / `role` / `inputs.required` entries** — no
empirical claims in them, so risk is negligible; one-line "not gradable as over-claim" entries would
complete the audit trail.

---

## Lens summary

| Lens | must-fix | note |
|------|----------|------|
| deterministic gates | 0 FAIL | 1 WARN + 1 phase8 WARNING, escalated into F2 |
| agent-skills-advisor (skills) | 1 | F1. Otherwise unusually disciplined: one strict template across all 15, `## Procedure` numbered everywhere, bodies well inside budget, 15-way `knowledge_partition` maps 1:1 onto the skills with no principle-ID overlap |
| profile-reviewer (release-readiness) | 2 | F2, F3. Role, `when_to_use`/`when_not_to_use` (no sibling-routing language anywhere), `forbidden_behaviours` domain coverage, `outputs`, and version-history/`agent_version` consistency all PASS |
| faithfulness-reviewer (over-claim) | 0 | Every checked rule restates its cited principle at or below source strength. Numerics match verbatim with hedges intact (modality effect sizes 0.18 / 0.09 / 0.18 vs P103; P061's "one tenth to one fifth" kept as a "provisional planning heuristic"). Conditional principles keep their qualifiers (P125, P143, P091, P072, P039, P134). Report is current, not stale |
| ai-agent-engineering-reviewer (adapter) | 0 | Tools correctly `Read, Grep, Glob` only; no Write/Edit/Bash/network language in the body; no routing to sibling subagents (handoffs go to humans/institutions, per the standing independence rule); advise-not-do framing holds |

Dedup: F2 absorbs the validator `quote-scan` WARN and the `phase8 self-check WARNING`. F4 and F5 share
one root cause (P100) but are separate edits in separate files, so each is listed once at should-fix.

MUST_FIX_COUNT: 3
