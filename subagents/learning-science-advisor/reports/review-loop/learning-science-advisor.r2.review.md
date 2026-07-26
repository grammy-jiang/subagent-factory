# Review report — learning-science-advisor (round 2)

Package: `subagents/learning-science-advisor/`
Date: 2026-07-27
Mode: REVIEW ONLY (no fixes applied)
Lenses: deterministic gates + agent-skills-advisor, profile-reviewer, faithfulness-reviewer,
ai-agent-engineering-reviewer (parallel, scope-partitioned).

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL, 1 WARN |
| `quote_scan` | PASS (vacuous — see F1) |
| truncation gate: `…` in skill bodies / adapter | no hits |
| truncation gate: severed invariant parenthetical in adapter | no hits |

Only WARN: `quote-scan: rights NOT verified — 12 restricted source(s) but no source text
available (no sources/markdown/, no warm cache module); verbatim-quote gate could not run`.

**Deterministic FAIL count: 0.**

## Findings

### F1 — Rights/quote gate is vacuous in this worktree (release-gate, not fixable by editing the package)

- **where** — validator WARN `quote-scan`; `provenance-ledger.md:125-129` (item S3 "remains open
  and unclosed"); `profile.yaml:5` (`status: ready`); all 12 sources `distillation-only`
  (`profile.yaml:413-487`)
- **severity** — should-fix *(profile-reviewer raised this as must-fix; downgraded here because no
  edit to any package file can clear it — it requires an environment holding `sources/markdown/`.
  It is a standing environmental condition of this worktree, not a package defect, so it must not
  block review-loop convergence. It DOES block external release.)*
- **problem** — `.claude/rules/rights-and-quotation-policy.md` makes `quote_scan` a hard
  pre-release requirement. Both the standalone run and the in-validator run reported PASS, but with
  zero source text present the check is vacuous: a missing corpus produces the same PASS as a clean
  one. `status: ready` is asserted while the rights gate has never actually executed against source
  bytes.
- **fix** — before external release, rehydrate `sources/markdown/` (or the warm cache module) in an
  environment holding the source text, re-run
  `python -m tools.subagent_factory.quote_scan subagents/learning-science-advisor`, and record the
  non-vacuous PASS in a new `provenance-ledger.md` version entry. Until then treat `status: ready`
  as "content-ready, rights-gate pending".

### F2 — `always_on[9]` cites P109 outside its scoped domain (SCOPE_BROADENED)

- **where** — `profile.yaml:264-265`, clause *"and refuses to infer truth from familiarity,
  vividness, confidence, or consensus"*, citation block ending `... P109, P130)`; grounding
  `principles/principles.yaml:2513-2533` (P109)
- **severity** — should-fix
- **problem** — P109's `applies_when` is scoped to consequential personal/eyewitness recollection
  ("Recollection or subjective certainty is being treated as factual evidence"; "…used in an
  investigation, decision, or evaluation") — the memory-accuracy domain. `always_on[9]` is the
  *technique-evidence-appraisal* block, so P109 is stretched to license an unscoped rule in a
  domain its own `applies_when` does not cover. `reports/faithfulness-report.yaml` graded this
  block WITHIN_SCOPE and discussed P072/P011/P084/P103/P130 but never examined P109's domain
  mismatch — a genuine miss, not a stale re-check.
- **fix** — either (a) drop P109 from this citation block and ground the clause only in principles
  that address technique-evidence epistemics (e.g. P053/P007), or (b) narrow the clause to
  consequential-recollection contexts as P109 requires and relocate it to the
  memory-mnemonics-and-recall-accuracy `always_on[11]` block, where P045's uncertainty-preserving
  language already lives.

### F3 — Canonical package pointers are repo-root-relative, but `Read` needs absolute paths

- **where** — adapter `.claude/agents/generated/learning-science-advisor.md:169` and the
  `Canonical package` section (lines 274-315); `profile.yaml:50-51`
- **severity** — should-fix
- **problem** — the agent has only `Read, Grep, Glob` (no Bash to resolve cwd). The adapter's one
  instruction for turning a relative pointer into something readable ("locate it with Glob and Grep
  before Read") is scoped explicitly to *caller-named* files, never extended to the subagent's own
  skill/reference pointers. Those pointers are load-bearing: the adapter requires reading a
  principle's statement in its skill file before citing it. If cwd ≠ repo root the `Read` fails
  silently and the agent falls back to citing from memory — exactly the failure the rule exists to
  prevent.
- **fix** — render canonical package pointers as absolute paths at export time (the generator knows
  the repo root), or extend the "locate with Glob/Grep before Read" instruction to cover the
  package's own pointers.

### F4 — Boundary sections buried behind a ~110-line "non-negotiable" invariants block

- **where** — adapter lines 21-132 (`Operating invariants (must hold)`, ~78 bullets) precede
  `When NOT to use` (148-159) and `Forbidden behaviours` (214-232)
- **severity** — should-fix
- **problem** — precedence is stated correctly (Role line 19 and the invariants intro line 23 both
  say Forbidden behaviours override), but the block labelled "non-negotiable / must hold" is the
  largest and most front-loaded section while the sections carrying the real hard limits arrive
  ~150 principle-dense lines later. Primacy plus volume skews adherence. The profile already
  applies progressive disclosure to the 15 `knowledge_partition.always_on` paragraphs; the
  invariants block does not get the same treatment.
- **fix** — move `When NOT to use` / `Forbidden behaviours` to immediately after Role, or shrink the
  inlined invariants to the boundary-critical subset and route the rest through the existing
  skill-file / reference-index pointers.

### F5 — Procedure step numbering restarts per subsection in one skill

- **where** — `skills/expertise-development-and-transfer/SKILL.md:62-81`
- **severity** — should-fix
- **problem** — `## Procedure` restarts at "1." in each of its four `###` subsections, producing
  four "step 1"s and four "step 2"s. Every other skill numbers continuously (e.g.
  `retrieval-practice-and-low-stakes-quizzing/SKILL.md` runs 1–13 straight through four
  subsections). Step references become ambiguous.
- **fix** — renumber continuously 1–11 across all four subsections.

### F6 — Bare imperatives break the advise-only lens in four skill steps

- **where** — `skills/course-design-technology-and-online-teaching/SKILL.md:63,68,69`;
  `skills/feedback-assessment-and-error-correction/SKILL.md:69`
- **severity** — should-fix
- **problem** — these steps drop the "Recommend the designer…" / "Have the instructor…" framing used
  by the surrounding steps and read as instructions for the advisor to build the artifact itself
  ("Start course design with…", "Build high-structure courses that…", "Apply universal design as
  the default framework…", "Build task-specific analytic rubrics that…"). This conflicts with the
  same skill's own Purpose line ("It recommends what to build and choose; the design owner carries
  out the resulting course") and with the package's forbidden-behaviour boundary against writing
  materials or delivering the course.
- **fix** — reframe as "Recommend the designer start…", "Recommend building a high-structure course
  that…", "Recommend applying universal design as the default framework…", "Recommend building
  task-specific analytic rubrics that…".

### F7 — Router-ambiguous triggers between evidence-appraisal and expertise-transfer

- **where** — `skills/evidence-appraisal-and-learning-myths/SKILL.md:58` vs
  `skills/expertise-development-and-transfer/SKILL.md:55`
- **severity** — should-fix
- **problem** — near-identical trigger wording for the same surface question ("a brain-based,
  far-transfer, or 'works for everything' claim is being made" vs "a transfer claim is being made").
  A request like "is this far-transfer claim credible?" gives a router no textual signal for which
  fires. The real distinction (appraising a technique's marketed general transfer claim vs
  validating transfer within an already-running practice regime) only surfaces deep in each
  Procedure, not in the description or when-to-use text.
- **fix** — add a one-clause disambiguator to each when-to-use bullet, stating the lens by
  capability (marketed/general claim vs existing practice regime) without naming the sibling skill.

### F8 — Profile body at 991/1000 words — no margin against the hard gate

- **where** — `provenance-ledger.md:94-101` (1.3.0, "Final body: 991 words"); `phase8` check 14
  FAIL threshold is 1000
- **severity** — should-fix
- **problem** — third consecutive version trimmed purely to stay under the gate (1.2.0→998,
  1.2.1→998, 1.3.0→991). Any future principle addition, restored hedge, or new forbidden-behaviour
  clause collides with the gate immediately, forcing another compression pass under pressure — and
  the ledger's own supersession history records a hedge being cut that way and later caught.
- **fix** — do a deliberate compression pass now (fold `outputs.modes` triggers/outputs more
  tersely, or push `knowledge_partition.always_on` prose fully into the skill files and shorten the
  profile's restatement) to buy real margin. Note: `phase8` body-size excludes `always_on`,
  `examples`, and `sources`.

### F9 — Descriptive-field provenance exemption is self-granted

- **where** — `provenance-ledger.md:9-10` ("`role`, `when_to_use`, `inputs`, `outputs`,
  `minimum_useful_output` carry no inline tags, per repo convention") vs
  `.claude/rules/rights-and-quotation-policy.md` ("Every profile field must be traceable to a
  source and QID… No orphan field values.")
- **severity** — nice
- **problem** — the policy states no exception; the ledger asserts a convention that is not
  established in any rule file. Defensible in practice (these fields restate cited rule fields
  rather than adding independent claims), but as written the package grants itself an exception to
  a hard rule.
- **fix** — either document the exception in `.claude/rules/rights-and-quotation-policy.md`
  (repo-level, out of package scope), or add a one-line traceability pointer on each of the five
  fields ("derived from quality_bar/forbidden_behaviours below").

### F10 — Two profile fields have no dedicated rendered anchor in the adapter

- **where** — `profile.yaml:55-57` (`outputs.primary_format`), `profile.yaml:89-90`
  (`minimum_useful_output`) vs the adapter
- **severity** — nice
- **problem** — no behaviour is lost (each mode's `Output:` line covers `primary_format`;
  quality-bar item 7 "Output floor…" covers `minimum_useful_output`), but the content is present in
  the canonical profile and silently absent from the render rather than deliberately folded in.
- **fix** — confirm in the export template that the merge is intentional, or add a one-line render
  for a literal anchor.

### F11 — Adapter provenance header names only `profile.yaml` as its source

- **where** — adapter lines 8-15 ("Source profile: subagents/learning-science-advisor/profile.yaml")
  vs the Operating invariants block, lines 21-132
- **severity** — nice
- **problem** — the ~78-item invariants list (over half the adapter body) has no corresponding
  `invariants`/`principles` field in `profile.yaml`; it is assembled at export time from another
  canonical file. `generated-artifact-policy.md` says "profile.yaml is canonical. Adapter is
  derived", implying 1:1; here the adapter's dominant section derives from a file its own
  provenance comment does not name.
- **fix** — have the provenance header list every canonical input the exporter consumes, or stamp a
  pointer to the invariants' true source into `profile.yaml`.

### F12 — Undeclared complementary overlap on "feedback framing"

- **where** — `skills/feedback-assessment-and-error-correction/SKILL.md:3-5` vs
  `skills/motivation-belonging-and-classroom-climate/SKILL.md:3-5`
- **severity** — nice
- **problem** — both descriptions claim "feedback framing". Plausibly intentional (content-gap lens
  vs motivational-attribution lens) and consistent with the profile's worked examples citing both
  together, but neither description signals the split is deliberate.
- **fix** — add a distinguishing clause to each ("the instructional content of feedback" vs "the
  motivational framing and tone of feedback").

### F13 — Bare imperative in one metacognition step

- **where** — `skills/metacognition-study-habits-and-self-regulation/SKILL.md:77` (step 9)
- **severity** — nice
- **problem** — same pattern as F6 but lower risk (object is a learner capability, not a deliverable
  artifact): "Build self-regulation by giving learners…" in a skill whose steps 4, 6, 7, 8, 10, 11,
  12 all use "Recommend…"/"Have the instructor…".
- **fix** — reframe as "Recommend building self-regulation by…".

### F14 — Description frontmatter formatting inconsistency

- **where** — `skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:3`
- **severity** — nice
- **problem** — cosmetic: description is one unwrapped line while every sibling folds across 2-3
  lines. Valid, in-limit YAML; source-readability only.
- **fix** — wrap to match siblings.

### F15 — NASEM rights classification may be needlessly restrictive

- **where** — `profile.yaml:482-487` (NASEM *How People Learn II*, `rights_status:
  distillation-only`)
- **severity** — nice
- **problem** — National Academies Press titles are frequently open-access; the conservative
  classification is not wrong but may over-restrict. Not a compliance issue either way.
- **fix** — one-time rights re-check on NASEM's actual licence; reclassify to `open` only if
  confirmed.

## Clean lenses (no finding)

- **Cross-subagent routing (standing rule)** — `router_description`, `when_to_use`,
  `when_not_to_use`, `handoff_rules`, `source_of_truth_policy` scanned: no sibling advisor named,
  no "routes to"/"hand off to" language. All exclusions stated by capability/authority.
- **Hazard coverage** — clinical/LD diagnosis (`profile.yaml:37,94`), placement/grading/
  admission/employment (`:39,96`), subject-matter content questions (`:41,106`) all excluded in
  both `when_not_to_use` and `forbidden_behaviours`.
- **Tool boundary** — no instruction in the adapter implies write, execute, or web-fetch; the
  Glob/Grep-before-Read workflow is correctly scoped to Read/Grep/Glob.
- **Authority creep** — "diagnosing a learner" forbidden while "diagnosing the study design" is
  explicitly in scope (worked example 3); every forbidden item is paired with an adjacent
  operational handoff naming who owns the decision instead.
- **Numeric-claim guardrail** — the 0.18/0.09/0.18 effect sizes in `examples[1].ideal_response` are
  carried verbatim from P103's own statement, so `forbidden_behaviours[5]` (no invented statistics)
  holds; correctly-exercised exception, not a contradiction.
- **Citation integrity** — all ~150 principle IDs cited inline in `profile.yaml` resolve to real
  entries in `principles.yaml`; no orphan citations, no wholly ungrounded empirical rule
  (citation-free entries are all labelled "authored scope boundary" self-restrictions).
- **Preserved hedges** — distributed practice (P125), interleaving (P028/P142/P064),
  self-explanation (P143), far transfer (P039), group-to-individual inference (P134) all retain
  their source conditions in profile text.
- **Skill corpus shape** — all 15 skills share one disciplined structure (Purpose → When to use →
  Procedure → Inputs → Output → Anti-patterns to flag → Worked example → References → Provenance);
  bodies under ~130 lines with bulk deferred to `references/`; anti-patterns paired 1:1 with
  principles; no truncation, no malformed frontmatter, no placeholder text.
- **Role coherence** — single bounded advisor persona, three non-overlapping modes
  (advise/review/plan), consistent between profile and adapter.

## Per-lens must-fix counts (pre-dedup)

| Lens | MUST_FIX_COUNT |
|------|----------------|
| deterministic gates (FAILs) | 0 |
| agent-skills-advisor | 0 |
| profile-reviewer | 1 (F1 — downgraded here, see F1 rationale) |
| faithfulness-reviewer | 0 |
| ai-agent-engineering-reviewer | 0 |

MUST_FIX_COUNT: 0
