# Review — learning-science-advisor (round r1)

Package: `subagents/learning-science-advisor/` · profile `agent_version: 1.2.1` · status `ready`
Date: 2026-07-27 · Mode: review only — no file changed except this report.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL, 1 WARN (`quote-scan: rights NOT verified — 12 restricted source(s), no source text available`) |
| `quote_scan` (standalone) | **PASS** — no potential verbatim quotation found |
| truncation gate — `…` ellipsis in 15 SKILL.md + adapter | clean, 0 hits |
| truncation gate — severed invariant parenthetical in adapter | clean, 0 hits |

Deterministic FAILs: **0**. The single WARN is an environment limitation (raw source markdown not
present in the worktree, no warm cache module), not a package defect — the standalone `quote_scan`
run over the package passed. Recorded as S3 below, not counted as must-fix.

## Findings

### MUST-FIX

**M1 — `reports/faithfulness-report.yaml:457` | must-fix | index off-by-one leaves the numeric-claim guardrail unreviewed**
`profile.yaml` has 7 `forbidden_behaviours` (indices 0–6). Index 5 is the numeric guardrail ("Citing an
effect size, statistic, or numeric benchmark not carried in the invoked principle's own statement…",
`profile.yaml:103-104`); index 6 is the law/accreditation boundary (`profile.yaml:105-106`). The report's
entry labelled `rule_ref: forbidden_behaviours[5]` reviews the **law/accreditation** rule — i.e. index 6's
content. Verified: the report contains `forbidden_behaviours[0..5]` and no `[6]` entry, so the real index 5
— the one rule that polices over-claim by invented precision, exactly this review's own failure mode — has
zero faithfulness coverage. `provenance-ledger.md` (authored-fields table) correctly distinguishes [5] from
[6], which confirms the report, not the profile, is wrong.
*Fix:* relabel the existing line-457 entry to `rule_ref: forbidden_behaviours[6]`, and add a new
`forbidden_behaviours[5]` entry grading the numeric/effect-size citation ban `WITHIN_SCOPE` as a
self-limiting authored evidence guardrail (same grading pattern as the other authored boundaries).

**M2 — `profile.yaml:117-121` / `provenance-ledger.md:6-21` | must-fix | `source_of_truth_policy.canonical_owner` is an orphan field value**
The ledger's opening asserts "every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s) it
restates," with exactly four documented authored exceptions (`quality_bar[6]`, `forbidden_behaviours[5]`,
`forbidden_behaviours[6]`, `handoff_rules[2]`). Verified: `canonical_owner` (profile.yaml:118-121) carries
**zero** P-codes and is not in that exception table. It is therefore an orphan field value under
`.claude/rules/rights-and-quotation-policy.md` ("No orphan field values") and falsifies the ledger's own
completeness claim. (Its sibling `precedence`, profile.yaml:123-127, is properly cited — P072, P010, P009,
P143, P125, P105, P134.)
*Fix:* add `source_of_truth_policy.canonical_owner` as a fifth row in the authored-fields table (kind:
authored scope boundary — it is the same authority statement as `handoff_rules[2]`, already listed), or tag
it inline if a principle actually grounds authority ownership.

**M3 — `profile.yaml:92-106` vs `profile.yaml:40-41` | must-fix | no `forbidden_behaviours` entry mirrors `when_not_to_use[3]` (subject-matter rulings)**
Every other `when_not_to_use` boundary has a mirrored, enforceable `forbidden_behaviours` entry —
teaching-performed ↔ `[0]`, diagnosis/labelling ↔ `[1]`, placement/grading/admission/employment ↔ `[2]`,
law/accreditation ↔ `[6]`. `when_not_to_use[3]` ("The question is about the subject matter itself — the
correct answer, not how to teach, practise, or assess it") is the only one with no forbidden-behaviour
counterpart, so the routing boundary exists but nothing forbids the agent from answering the subject-matter
question once invoked. Subject-matter rulings are a named release-readiness failure mode for this advisor
class.
*Fix:* add a `forbidden_behaviours` item, e.g. "Ruling on or supplying the subject-matter answer itself —
the correct chemistry, translation, or legal position — rather than how to teach, practise, or assess it
(authored scope boundary)." Add the matching row to the ledger's authored-fields table. **Blocking
constraint:** the ledger records the final profile body at 998 words against a 1000-word hard-fail gate, so
this addition MUST be paired with a trim elsewhere in the same pass (trimming precedent is documented in the
1.2.0 ledger entry), then re-export the adapter and re-run `validate`.

### SHOULD-FIX

**S1 — `reports/faithfulness-report.yaml:~394-399` | should-fix | stale justification on the `always_on[13]` finding.**
The note claims P115's caveat "is compressed from 'an average age trend in speeded reasoning' to 'an average
age trend'". Current `profile.yaml:319` retains the full qualifier `in speeded reasoning` verbatim. The
`WITHIN_SCOPE` verdict stays correct; the reasoning describes text no longer in the package and would lead a
future reviewer to believe an accepted hedge-drop exists. *Fix:* rewrite the note to state the qualifier is
retained verbatim.

**S2 — `provenance-ledger.md:65-99` | should-fix | 1.2.1 records the grounded fix but no independent re-verify.**
The repo pipeline is review → grounded fix → independent re-verify → converge to zero must-fix; `validate`
PASS is a structural check, not that re-verify. `status: ready` was asserted before the loop closed (the
prior `.CLEAN` marker is deleted in the working tree). **This r1 pass is that independent re-verify** — it
found M1–M3, so the correct close-out is: fix M1–M3, re-verify, then record the must-fix=0 result and report
path in the ledger before restoring `ready` / `.CLEAN`.

**S3 — validator WARN | should-fix | verbatim-quote gate could not run.**
`quote-scan` could not verify the 12 `distillation-only` sources because neither `sources/markdown/` nor a
warm cache module is present in this worktree. The standalone `quote_scan` over the package passed, so there
is no evidence of a leak, but the rights gate is unexercised this round. *Fix:* run the gate once in an
environment with the source markdown (or a warm cache) available before release, and note the result.

**S4 — all 15 `skills/*/SKILL.md` (`## Purpose`) | should-fix | Purpose duplicates Procedure ~1:1.**
E.g. `cognitive-load-worked-examples-and-scaffolding/SKILL.md:47` vs `:61-69`;
`retrieval-practice-and-low-stakes-quizzing/SKILL.md:50` vs `:61-73`;
`motivation-belonging-and-classroom-climate/SKILL.md:51` vs `:62-75`. The Purpose paragraph is a prose
restatement of every Procedure line, same content and order, minus the citations — roughly a third of each
body carries no information Procedure doesn't carry better. *Fix:* cut Purpose to 1–3 sentences (what, for
whom, at what grain) and let Procedure carry the cited detail.

**S5 — all 15 `skills/*/SKILL.md` (`## Procedure`) | should-fix | flat principle-id-ordered checklist, not a decision sequence.**
E.g. `motivation-belonging-and-classroom-climate/SKILL.md:62-75` (14 flat items),
`evidence-appraisal-and-learning-myths/SKILL.md:61-74` (14 flat items). Steps are emitted in
`provenance.principles` order with no phase grouping or priority.
`interleaving-variation-and-discrimination/SKILL.md:57` shows the right pattern (embedded if/then) but is the
exception. *Fix:* cluster each Procedure into 2–4 named phases (e.g. `### Diagnose` / `### Correct` /
`### State the trade-off`).

**S6 — `feedback-assessment-and-error-correction/SKILL.md:55`, `prior-knowledge-prediction-and-misconceptions/SKILL.md:61` | should-fix | body voice performs the pedagogical act instead of advising the instructor.**
"Support problem solving with the least help needed…" and "Open learning with a relevant stimulus and ask
what learners notice and wonder…" read as the agent teaching. Disambiguated only by the boilerplate
disclaimer at the end of each `## Output`. *Fix:* reframe toward the design owner — "Recommend the instructor
support…", "Have the instructor open with…".

**S7 — `.claude/agents/generated/learning-science-advisor.md:3` | should-fix | router-facing `description` is one dense sentence enumerating ~16 topic clusters before the exclusion clause.**
Accurate, and it does carry a "does not / not for" boundary, but the density works against fast router
matching against sibling packages. *Fix:* shorter lead identity clause + trailing "covers: …" fragment;
meaning unchanged. (Change `profile.yaml` and re-export — never edit the adapter.)

**S8 — all 15 `skills/*/SKILL.md` (`## Output`) | should-fix | charter clause duplicated verbatim ×15.**
"…it does not teach the subject matter, deliver the course, mark the work, or diagnose a learning disability
or clinical condition" restates `profile.yaml` `forbidden_behaviours` verbatim in every skill; the parent
session already holds the charter as always-on context. *Fix:* keep per-skill output-format guidance; shorten
the boundary clause to a pointer.

### NICE

- **N1** — adapter `:173` vs `:201,209,225,237`: the Required-inputs rule says "never cite a code from memory"
  for codes absent from Operating invariants, yet the governance sections cite ~15 such codes (P013, P107,
  P028, P067, P047, P136, P053, P033, P140, P070, P099, P143, P105, P010, P039). Almost certainly intentional
  (pre-verified governance text vs the agent's own live citations) but unstated. Add: "applies to codes you
  introduce in your own response, not to codes already cited in this profile's governance sections."
- **N2** — adapter `:19`: role text points at "the twelve distillation-only sources listed under `sources`", a
  `profile.yaml` key never rendered in the adapter body. Point at the canonical package, or render a short
  source list.
- **N3** — `evidence-appraisal-and-learning-myths/SKILL.md:3-4`: description doesn't exclude appraisal of a
  technique that has its own dedicated skill; "is spaced repetition worth using?" could route here instead of
  to `spacing-distributed-practice-and-consolidation`.
- **N4** — `memory-mnemonics-and-recall-accuracy/SKILL.md:48`: trigger "A recollection is being elicited where
  accuracy matters and the questioning itself could distort it (P045)" has no educational-context qualifier
  and could fire on pure forensic/witness-interview requests outside the charter's audience.
- **N5** — `motivation-belonging-and-classroom-climate/SKILL.md:56`: P141 (structured comparison, evidence
  standards) is filed under the exclusion/threat-climate trigger but fits a "designing a discussion/debate"
  trigger better.
- **N6** — `principles/principles.yaml` P100 (reading-diagnostic measures) is cited by
  `knowledge_partition.always_on[10]`, whose prose covers goal-directed practice, motor/perceptual expertise,
  and analogy-transfer boundaries — the citation has no matching prose. Not an over-claim; fold in a clause or
  move the citation.
- **N7** — `profile.yaml:318-321`: `always_on[13]` has an irregular line wrap (breaks after ~20 chars vs the
  ~100-char wrap used file-wide), suggesting an un-reflowed hand-edit. Cosmetic.
- **N8** — `collaborative-and-peer-learning/SKILL.md:71,73`: a few anti-patterns are near-pure negations of the
  matching Procedure line; one concrete observable symptom each would raise diagnostic value (`:69` shows the
  good pattern).

## Clean

Checked and found sound: 0 deterministic FAILs; no truncated skill bodies or severed adapter invariants; no
broken cross-references (both `references/*.md` exist and every skill links them correctly); skill→principle
partition sums to exactly 150 with no principle in two skills; no skill instructs an action outside
Read/Grep/Glob; adapter tool boundary clean (no write/edit/fetch/bash instruction anywhere in the body); no
authority creep — grading, diagnosis, and placement consistently forbidden and redirected to a human role;
**no cross-subagent routing language anywhere** (every "handoff" names a human role, per the standing
subagent-independence rule); DO-NOT-EDIT header present within the first 20 lines; canonical and installed
adapters in sync and matching a fresh render of `profile.yaml`; profile and adapter both 1.2.1; version
history 1.0.0→1.2.1 present with supersession recorded; all 12 sources match between `profile.yaml` and the
ledger with valid sha256 digests and `distillation-only` rights; when_to_use / when_not_to_use partition with
no dead zone found; all `quality_bar`, `when_to_use`/`when_not_to_use`, `outputs`, `handoff_rules`,
`precedence`, `minimum_useful_output`, all 15 `always_on` blocks and all 3 `examples` checked against cited
principles — no `SCOPE_BROADENED`, `HEDGING_REMOVED`, or `CONTRADICTED` rule, and no orphan rule beyond M2.

## Dedup note

M1 (faithfulness report labelling defect at `forbidden_behaviours[5]`) and M3 (missing profile rule mirroring
`when_not_to_use[3]`) touch adjacent indices but are distinct defects in distinct files; both retained.
Profile-reviewer's "no independent re-verify recorded" must-fix was downgraded to S2 — this r1 pass *is* that
re-verify, so it is a process state to close out, not a package defect. The validator's `quote-scan` WARN is a
WARN, not a FAIL, and the standalone scan passed — recorded as S3, not counted as must-fix.

MUST_FIX_COUNT: 3
