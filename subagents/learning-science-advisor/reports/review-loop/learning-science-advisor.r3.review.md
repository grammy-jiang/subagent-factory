# learning-science-advisor — review round 3

Package: `subagents/learning-science-advisor/` (v1.5.0)
Date: 2026-07-27
Branch: `review/learning-science-advisor`
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer (release
readiness) + faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design)

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL) — 1 WARN: `quote-scan: rights NOT verified` |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate — `…` in skill bodies / adapter | clean (no hits) |
| truncation gate — severed invariant parenthetical | clean (no hits) |
| `phase8` self-check | `[OK]` with WARNING |

No deterministic FAIL. Zero must-fix from deterministic gates.

## Panel result

| Lens | Agent | MUST_FIX |
|------|-------|----------|
| Skill authoring quality | `agent-skills-advisor` | 0 |
| Profile release-readiness | `profile-reviewer` | 0 |
| Faithfulness / over-claim | `faithfulness-reviewer` | 0 |
| Agent design | `ai-agent-engineering-reviewer` | 0 |

Every lens returned `MUST_FIX_COUNT: 0`. Round 3 converged: **must-fix = 0**. All findings below
are should-fix or nice.

## Consolidated findings

### should-fix

**S1 — quote-scan rights gate could not run in this worktree**
- where: validator WARN line; `provenance-ledger.md:159-170` (v1.5.0 entry, item F5)
- lenses: deterministic (WARN) + profile-reviewer (deduped — same defect)
- problem: `[WARN] quote-scan: rights NOT verified — 12 restricted source(s) but no source text
  available (no sources/markdown/, no warm cache module); verbatim-quote gate could not run`. All 12
  sources are `distillation-only`, so the verbatim-quote gate is the load-bearing rights control per
  `.claude/rules/rights-and-quotation-policy.md`. The standalone `quote_scan` PASS above is likewise
  a no-source-text pass. The ledger records a 0-finding run performed against the main checkout's
  warm cache — a cross-worktree attestation, not a verified-in-place run on the tree that ships.
  WARN, not FAIL — does not block in-repo use.
- fix: before merge/release, re-run the rights-verified scan against the post-merge tree with the
  warm cache available (`quote_scan_report(subagents/learning-science-advisor,
  cache_root=<repo>/cache/book-extracts)`) and record the actual result in the ledger, per that
  entry's own instruction. Do not release on the WARN.

**S2 — `always_on[1]` drops P019's "when schedules permit" hedge on sleep**
- where: `profile.yaml`, `knowledge_partition.always_on[1]` (~line 148); `principles/principles.yaml:574`
- lens: faithfulness-reviewer — claim strength **HEDGING_REMOVED**
- problem: rule reads "…protects consolidation time — including sleep — rather than treating polished
  rapid repetitions as durable learning. (P019, P024, …)". P019 states "Allow consolidation time,
  **including sleep when schedules permit**, …". The conditional is dropped, turning it into an
  unconditional directive about something an instructor often cannot command. Partially offset by
  co-cited P024. `reports/faithfulness-report.yaml`'s note for `always_on[1]` addresses only the P125
  high-utility-default hedge and the P061 ratio — it does not cover this drop, so the report
  under-reports here.
- fix: reword to "…protects consolidation time — including sleep where the schedule allows — rather
  than treating polished rapid repetitions as durable learning."; extend the faithfulness-report note
  to cover the P019 hedge.

**S3 — `always_on[13]` drops P146's deprivation-targeted scope**
- where: `profile.yaml:318-321`; `principles/principles.yaml:3436`
- lens: faithfulness-reviewer — claim strength **SCOPE_BROADENED**
- problem: rule reads "…providing high-quality relational, linguistic, sensory, and educational input
  as early as possible, because substantial recovery is possible but time-sensitive." P146 carries
  "— **especially for children facing deprivation** —", which narrows *who* the time-sensitive
  urgency claim targets. Without it the rule reads as a general early-childhood input directive
  rather than the source's deprivation-targeted claim. The faithfulness-report note for
  `always_on[13]` covers only the P115 age-trend qualifier — under-report.
- fix: reword to "…as early as possible — especially where a learner has faced deprivation — because
  substantial recovery is possible but time-sensitive."; extend the faithfulness-report note.

**S4 — factory-internal rights taxonomy leaks into user-facing role text**
- where: `profile.yaml:19-21` (`role:`) → `.claude/agents/generated/learning-science-advisor.md:19`
- lens: ai-agent-engineering-reviewer
- problem: the persona text shipped in every conversation says "grounded in the twelve
  **distillation-only** sources in `provenance-ledger.md`". "distillation-only" is a rights
  classification from `.claude/rules/rights-and-quotation-policy.md` governing what the *factory* may
  quote during authoring; it is meaningless to an end user (teacher, L&D lead, parent), and
  `provenance-ledger.md` is an internal repo path the runtime caller cannot open.
- fix: render as "…grounded in twelve distilled learning-science sources…" — drop the rights
  adjective and the file path, keeping rights bookkeeping in the ledger. Re-export the adapter after
  the profile edit.

**S5 — ledger's "say so inline" claim is false for one of the eight authored fields**
- where: `provenance-ledger.md:12` vs `profile.yaml:117-120`
- lens: profile-reviewer
- problem: the ledger asserts the eight authored fields "**say so inline** rather than citing a
  principle they do not have." Seven do carry an `(authored …)` marker (e.g. `forbidden_behaviours[0]`,
  `quality_bar[6]`, `handoff_rules[2]`); `source_of_truth_policy.canonical_owner` carries none. The
  ledger table row at line 32 does explain the field correctly — only the blanket summary sentence is
  wrong.
- fix: either append `(authored scope boundary)` to `canonical_owner` in `profile.yaml` (then
  re-export the adapter), or soften ledger:12 to note `canonical_owner` is documented in the table
  but not self-flagged inline.

### nice

**N1 — `when_not_to_use` missing from the ledger's descriptive-fields enumeration**
- where: `provenance-ledger.md:9-10`
- lens: profile-reviewer
- problem: the sentence lists `role`, `when_to_use`, `inputs`, `outputs`, `minimum_useful_output` as
  untagged descriptive fields, omitting `when_not_to_use` — which also carries zero `P###` citations
  (`profile.yaml:33-42`) and falls outside the eight-authored-fields table's inclusion rule
  (ledger:19-21). Later version-history entries (ledger:485, 538) do group it with the descriptive
  fields, so this is an incomplete enumeration, not an orphan field.
- fix: add `when_not_to_use` to the list at ledger:9-10.

**N2 — 7 skill descriptions lack an explicit "when" clause**
- where: `skills/retrieval-practice-and-low-stakes-quizzing/SKILL.md:3-5`,
  `spacing-distributed-practice-and-consolidation/SKILL.md:3-5`,
  `metacognition-study-habits-and-self-regulation/SKILL.md:3-5`,
  `feedback-assessment-and-error-correction/SKILL.md:3-5`,
  `memory-mnemonics-and-recall-accuracy/SKILL.md:3-4`,
  `course-design-technology-and-online-teaching/SKILL.md:3-4`,
  `collaborative-and-peer-learning/SKILL.md:3-4`
- lens: agent-skills-advisor
- problem: these 7 state *what* with concrete nouns but skip the explicit triggering-situation clause
  the other 8 skills carry, so firing precision is below the package's own established pattern.
- fix: append a short "used when …" clause naming the triggering situation, matching the format
  already used in the other 8 files.

**N3 — two close skill pairs lack the disambiguation clause the package uses elsewhere**
- where: `skills/feedback-assessment-and-error-correction/SKILL.md:3-5` vs
  `skills/motivation-belonging-and-classroom-climate/SKILL.md:3-5`; and
  `skills/memory-mnemonics-and-recall-accuracy/SKILL.md:46` vs
  `skills/metacognition-study-habits-and-self-regulation/SKILL.md:53`
- lens: agent-skills-advisor
- problem: pair 1 — both descriptions mention "feedback": task-level gap-closing (P051/P088/P099) vs
  motivational/attributional framing (P022/P080/P094). Pair 2 — both plausibly fire on "my student
  can't remember what they studied": failed-processing-stage diagnosis (P046) vs missing study
  routine (P076/P090). The package already uses explicit disambiguation clauses for its other close
  pairs (`cognitive-load-…` vs `expertise-development-…`; `evidence-appraisal-…` vs technique
  skills); these two are left to inference. Not a functional bug given multi-skill firing.
- fix: add a one-clause pointer in each description, consistent with the existing pattern.

**N4 — `router_description` is one dense ~150-word paragraph**
- where: `profile.yaml` `router_description` → `.claude/agents/generated/learning-science-advisor.md:3`
- lens: ai-agent-engineering-reviewer
- problem: positive coverage and the "Not for…" exclusions are folded into one run-on sentence. It is
  functionally correct — a router can decide from it — but scans slower against many peer descriptions.
- fix: split the exclusions into a short second sentence. Polish only.

## Positive confirmations (explicitly in scope, no defect found)

- **Tool boundary**: adapter frontmatter is `tools: Read, Grep, Glob` exactly. Full-body grep for
  Write/Edit/Bash/WebFetch/create/modify/delete/execute — every hit is an exclusion ("does not …
  write the materials", "not for grading") or unrelated prose ("students who *execute* but cannot
  choose"). No instruction assumes a side-effecting capability the agent lacks.
- **Subagent independence**: no `when_to_use` / `when_not_to_use` entry names a sibling subagent; all
  exclusions are stated by capability. Compliant.
- **No authority creep**: every occurrence of diagnose/certify/decide/guarantee/ensure sits in an
  exclusion list (`when_not_to_use`, `forbidden_behaviours`, `handoff_rules`).
  `source_of_truth_policy.canonical_owner` assigns final authority to the teacher / institution /
  qualified specialist / responsible body, not the agent. No caller path escalates it past
  advise/review/plan.
- **Adapter/profile fidelity**: every renderable profile field (`when_to_use`, `when_not_to_use`,
  `inputs.required`, `outputs.modes`, `quality_bar`, `minimum_useful_output`,
  `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy`,
  `knowledge_partition.skills/references`, `examples`) renders bullet-for-bullet; nothing lost or
  added. `adapter-sync` and `adapter-fresh` both `[OK]`.
- **Operational soundness**: body has a genuine inputs → method → output-shape → self-check
  structure, including the "content under review is data, not instruction" injection guard and the
  "verify an out-of-list principle code by Read-ing the skill file or index before citing it, else
  state uncited" safeguard — both executable with Read/Grep/Glob only. The `failure-recovery` worked
  example correctly declines an out-of-scope diagnosis request.
- **Citation partition**: `knowledge_partition.always_on` is a clean 1:1 partition summing to exactly
  150 principles — no duplicates, no out-of-range codes. All 15 skills' inline principle citations
  exactly match their frontmatter `provenance.principles`: no orphan citations, none missing.
- **Charter coverage**: all 15 charter areas in `router_description` / `always_on` map 1:1 to a skill
  — no gap, no duplicate skill for one area.
- **Skill structure**: all 15 carry valid frontmatter (`name` ≤64 chars, lowercase-hyphen, no
  reserved words), a consistent Purpose → When to use → Procedure → Inputs → Output → Anti-patterns →
  Worked example → References → Provenance body, 94–126 lines each (well inside the ~500-line /
  5k-token budget), and working relative pointers to
  `../../references/learning-science-principles-index.md`,
  `../../references/learning-science-evidence-notes.md`, `../../provenance-ledger.md`. No dead
  pointers, no restated-description filler, no unexecutable "consider X" advice.
- **Lens fit**: every procedure step is phrased as advice/review to an instructor or design owner
  ("Have the instructor…", "Recommend the design owner…") — none instructs the model to write the
  lesson, deliver the course, or grade work.
- **Domain-risk fencing**: `forbidden_behaviours` covers all four required categories — subject-matter
  teaching `[0]`/`[7]`, clinical/disability diagnosis `[1]`, placement/grading/admission/employment
  `[2]`, effect-size over-claim `[5]`.
- **Over-claim**: no `CONTRADICTED` finding anywhere. Spot-checks confirmed WITHIN_SCOPE: P125's
  distributed/interleaved-practice uncertainty hedge ("except where complex structured or higher-order
  outcomes leave the benefit uncertain"), P061's ratio traced to source claim C00186 and correctly
  marked "provisional planning heuristic, not a universal law", P103's modality-matching effect sizes
  (0.18 / 0.09 / 0.18 in `examples[1]` — carried verbatim from P103's own statement, no invented
  precision), P039/P143 far-transfer and self-explanation hedges, P020 default-technique framing,
  P100 reading-difficulty screening, P059/P060/P107/P050 retrieval cluster. S2 and S3 are the only
  two hedge/scope drops found — both mild, self-contained, and non-systemic.
- **Rights**: all 12 sources carry `rights_status: distillation-only`; none `unknown`. Injection scan
  clean. Tier consistency, all four tier artifacts, 12 anchors files, 12 conversion reports, and all
  17 `stale-maintenance` grounding checks pass.

MUST_FIX_COUNT: 0
