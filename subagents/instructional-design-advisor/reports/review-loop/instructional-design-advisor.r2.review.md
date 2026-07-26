# Review — instructional-design-advisor (round 2)

Package: `subagents/instructional-design-advisor/` (agent_version 1.2.0)
Mode: review-only. No package file was edited by this pass.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** — 81 OK checks, 0 FAIL. One informational `phase8: Phase 8 self-check WARNING` (see S-1). |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate — `…` ellipsis in skill bodies / adapter | **PASS** — no hits |
| truncation gate — adapter invariant severed inside a parenthetical | **PASS** — no hits |

Deterministic FAILs: **0**.

## Reviewer panel

| Lens | Scope | must-fix |
|------|-------|----------|
| agent-skills-advisor | 13 `skills/*/SKILL.md` + profile as charter | 0 |
| profile-reviewer | `profile.yaml`, `provenance-ledger.md` | 0 |
| faithfulness-reviewer | profile rules vs `principles/principles.yaml` + prior report | 0 |
| ai-agent-engineering-reviewer | installed adapter + profile | 0 |

## Findings — most severe first

### must-fix

None.

---

### should-fix

**S-1 — profile body is 987 words: 13 words below the hard-FAIL ceiling**
`subagents/instructional-design-advisor/profile.yaml` (aggregate of the body-size fields: `role` L16-22, `when_to_use` L23-32, `when_not_to_use` L33-40, `inputs.required` L41-45, `outputs.primary_format` L47-49, `outputs.modes` L50-64, `quality_bar` L65-79, `minimum_useful_output` L80-81, `forbidden_behaviours` L82-97, `handoff_rules` L98-104, `source_of_truth_policy.precedence` L115-119)

*Problem.* This is the source of the `phase8` WARNING the validator reports. Field-by-field the body totals **987 words** (role 91 + when_to_use 82 + when_not_to_use 81 + inputs 37 + primary_format 36 + modes 128 + quality_bar 163 + minimum_useful_output 19 + forbidden_behaviours 199 + handoff_rules 70 + precedence 81), matching the ledger's own "~987 words" claim (`provenance-ledger.md:123`). That is 187 over the 800-word WARN threshold and only 13 under the 1000-word hard FAIL. The next fold-in or any wording addition flips a currently-green gate to blocking. A named driver of the bloat: `outputs.primary_format` (L47-49) and `outputs.modes[0].output` (L53-54) both carry the identical 12-word clause "never a bare good/bad verdict, a built deliverable, or a promise of effectiveness" — the ledger's 1.2.0 entry (L107-111) records that this duplication was deliberate because `primary_format` / `minimum_useful_output` have no adapter-template rendering slot.

*Fix.* De-duplicate the repeated constraint clause: state it once in `primary_format` and have each mode's `output` refer to it briefly rather than restate it. Then tighten the two heaviest sections, `forbidden_behaviours` (199w) and `quality_bar` (163w), whose citation-heavy sentences carry the most compressible prose. Target comfortably under 800 words to restore real margin. Note the interaction with S-2: the correct fix for S-2 is to give `minimum_useful_output` a real adapter slot, which also removes the motive for the copy-paste that inflates this count.

**S-2 — `minimum_useful_output` never reaches the model; the adapter has no stated floor for underspecified requests**
`subagents/instructional-design-advisor/profile.yaml:80-81` vs. `.claude/agents/generated/instructional-design-advisor.md` (whole body)

*Problem.* The profile defines the fallback bar `minimum_useful_output: At least one finding that names an instructional-design practice, its principle, and the residual trade-off or referral to make.` The adapter template renders no slot for it, so the system prompt the agent actually runs on states no floor for a thin or underspecified request — the ask/abstain/answer decision has no textual anchor in the adapter at all. Same root cause as the duplication in S-1.

*Fix.* Render `minimum_useful_output` into the adapter as its own short heading (or fold it into "Supported modes and outputs"), so the constraint reaches the model instead of living only in the canonical profile. This is an adapter-template change plus re-export, not a hand edit of the adapter.

**S-3 — `when_not_to_use` omits the "deliver / facilitate / teach the session" exclusion that `role` and `router_description` both promise**
`subagents/instructional-design-advisor/profile.yaml:33-40` vs. `:14-15` (`router_description` "Not for: … teaching or grading learners…") and `:22` (`role` "never builds the course, teaches it, grades learners, or certifies a programme")

*Problem.* `role` and `router_description` name three exclusions — building, teaching/delivering, grading/certifying. The enumerated `when_not_to_use` list covers only two: bullet 1 excludes building the deliverable, bullet 3 excludes grading/certifying. Nothing matches a caller asking the advisor to *deliver or facilitate* the session ("run this workshop for us"), even though two other fields promise it is out of scope. Check 3 of the deterministic self-check only counts bullets (≥2), so the content gap is not caught structurally.

*Fix.* Add a `when_not_to_use` bullet: "The caller wants the session delivered, facilitated, or taught by the advisor — that is the instructor's role; this advisor designs and reviews the instruction, it does not deliver it." Keep it short given S-1's word budget.

**S-4 — the shared output/boundary paragraph is copy-pasted verbatim into all 13 skill bodies**
`subagents/instructional-design-advisor/skills/*/SKILL.md`, the `## Output` paragraph and the second `## Inputs` bullet in every file — e.g. `backward-design-and-constructive-alignment/SKILL.md:84`, `learning-outcomes-and-taxonomy/SKILL.md:86`, `assessment-design-and-authentic-tasks/SKILL.md:100`, `feedback-and-formative-practice/SKILL.md:65`, `teaching-for-understanding-and-transfer/SKILL.md:89`, `multimedia-and-elearning-design/SKILL.md:86`, `instructional-strategy-and-events/SKILL.md:138`, `motivation-and-learner-engagement/SKILL.md:66`, `needs-and-context-analysis/SKILL.md:78`, `iterative-prototyping-and-development/SKILL.md:72`, `evaluation-transfer-and-impact/SKILL.md:92`, `active-learning-and-group-formats/SKILL.md:88`, `teaching-scholarship-and-quality/SKILL.md:72`

*Problem.* The identical sentence ("Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on instructional design; it does not build the course, materials, or item bank for the caller, teach or grade learners, or certify a programme or its subject-matter content.") appears in all 13 skills, and it restates what `profile.yaml` already carries once in `outputs.primary_format`, `outputs.modes`, and `forbidden_behaviours`. The profile's `review` mode (`profile.yaml:57`) is explicitly designed to span several areas at once, so a real review loads several of these bodies together and the agent sees the same paragraph N times with zero new signal after the first. Classic "skill restates the profile" anti-pattern; costs context for nothing.

*Fix.* Replace the duplicated closing paragraph in each skill with a one-line pointer ("Output format and scope boundary: see the agent's charter."), leaving `profile.yaml`'s `outputs` / `forbidden_behaviours` as the single home for the shared boundary language. Keep only genuinely skill-specific output nuance inline. Same treatment for the duplicated `## Inputs` bullet.

**S-5 — Quality bar / Forbidden behaviours / Handoff rules cite principle IDs the adapter never defines**
`.claude/agents/generated/instructional-design-advisor.md:233-243`, `:246-260`, `:262-267`

*Problem.* These sections cite P008, P077, P098, P167, P148, P152, P140, P100, P021, P172, P107, P193, P096, P109, P191, P187, P062, P134 — none of which appear in the adapter's own "Operating invariants" section, which renders only a curated subset. The prose around each citation is self-contained, so nothing breaks at runtime, but the system prompt asserts traceability to principle text the agent has never seen and cannot resolve from context; resolving it would require reading a package file that may not exist on a deployment target.

*Fix.* Either promote the principles cited downstream into the "Operating invariants" list so every ID used is defined once upstream in the same context window, or drop the bare P-numbers from those three sections since the prose already carries the operative instruction. Prefer the second given S-1's word pressure. Either way this is a template/profile change followed by re-export.

---

### nice

**N-1 — `role`'s "judge transfer and impact" reads as certifying**
`.claude/agents/generated/instructional-design-advisor.md:19`

In isolation the clause implies the agent pronounces whether transfer/impact occurred, colliding with Forbidden behaviours (`:251`, impact is evaluated only after target learners perform in context) and the Handoff rule (`:267`, impact judgments wait on evaluation evidence). The following sentence resolves it, but the verb invites a naive misread of the role's first paragraph. Reword to "review whether transfer and impact are validly assessed" (fix in `profile.yaml` `role`, then re-export).

**N-2 — `instructional-strategy-and-events` has a broader triggering surface than any sibling**
`subagents/instructional-design-advisor/skills/instructional-strategy-and-events/SKILL.md:1-167`

~2× the size of any sibling: 35 principles / 35 procedure steps over four distinct sub-topics under their own `###` headings (nine-events framing, sequencing/prerequisite order, technique-by-outcome-type matching, scaffolding/practice/retrieval). Still inside the body budget and internally well organised, but one `description` must cover all four sub-scopes. If it grows further, split along the existing `###` boundaries into two or three narrower skills with sharper descriptions.

**N-3 — template inconsistency in one anti-patterns intro**
`subagents/instructional-design-advisor/skills/assessment-design-and-authentic-tasks/SKILL.md:104`

Only this skill uses the markdown link form `[Procedure](#procedure)`; the other 12 use plain `## Procedure` (e.g. `backward-design-and-constructive-alignment/SKILL.md:88`, `learning-outcomes-and-taxonomy/SKILL.md:90`). No functional impact. Normalise to the plain-text form.

---

## Verified clean (no finding)

- **Faithfulness / over-claim.** Every principle ID cited by `quality_bar[0-5]`, `forbidden_behaviours[0-5]`, `handoff_rules`, `source_of_truth_policy`, `outputs.modes`, and all 13 `knowledge_partition.always_on` paragraphs exists in `principles.yaml` and is supported at equal or narrower strength — checked individually, not sampled. No SCOPE_BROADENED, HEDGING_REMOVED, or CONTRADICTED. The four v1.1.0→v1.2.0 hedge repairs recorded in `reports/faithfulness-report.yaml` were independently re-verified as actually present in the v1.2.0 text: P153 "retention evidence *alone*" (`profile.yaml:135`), P165 conditioned on formative evidence exposing a relevance/fairness problem (`:159-161`), P163 "*solely* from prior attainment" (`:170`), P157 narration-over-onscreen-text bounded to a *system-paced* presentation (`:178-180`). The usual over-claim sites (Mayer effects, Gagné nine events as "checklist… not a mandatory script", Merrill method-situation pairing, Hattie-style synthesis) all retain their source hedges.
- **Subagent independence (standing rule).** No sibling-routing language anywhere in `profile.yaml` or the adapter. Every handoff targets a *human* role (teacher of record, institution, content expert), not another generated subagent.
- **Tool boundary.** Adapter grants exactly Read/Grep/Glob. No Bash/Write/Edit, and no "implement" / "apply the fix" / "commit" authority-creep language.
- **Adapter integrity.** Installed adapter matches canonical and matches a fresh render of `profile.yaml`. Operating invariants lead with the precedence statement before the list, so the load-bearing constraint is not buried. Both worked examples correctly refuse to build the deliverable or certify effectiveness and return ownership to the caller.
- **Skill structure.** All 13 skills: valid frontmatter (unique lowercase-hyphen name, within length limits, no reserved words, no XML tags); all required sections present (Purpose, When to use, Procedure, Inputs, Output, Anti-patterns to flag, References, Provenance); each skill's frontmatter principle-id list maps 1:1 to its numbered Procedure steps and to the count stated in its anti-patterns intro; bodies are procedural ("when X, do Y, because Z (Pnnn)") not fact dumps; the principle catalogue and evidence notes live in `references/` rather than inlined. `knowledge_partition.skills` matches the 13 discovered directories exactly — no orphans. The multimedia/e-learning skill is in-lens, not drift: Mayer and Clark & Mayer are declared sources (`profile.yaml:383-394`).
- **Provenance.** `agent_version: 1.2.0` (`profile.yaml:4`) is recorded in `provenance-ledger.md`'s Version History (`:67`); every load-bearing rule field carries inline P-citations traceable to the 200-principle spine; no orphan field values.

MUST_FIX_COUNT: 0
