# learning-science-advisor — review round 3

Package: `subagents/learning-science-advisor/` (v1.2.0)
Date: 2026-07-27
Lenses: deterministic gates + agent-skills-advisor (skill authoring) + profile-reviewer (release
readiness) + faithfulness-reviewer (over-claim) + ai-agent-engineering-reviewer (agent design)

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL) — 1 WARN: `quote-scan: rights NOT verified` |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| truncation gate — `…` in skill bodies / adapter | clean (no hits) |
| truncation gate — severed invariant parenthetical | clean (no hits) |
| `phase8` self-check | `[OK]` with WARNING (see S2) |

No deterministic FAIL. Zero must-fix from deterministic gates.

## Consolidated findings

Every lens returned `MUST_FIX_COUNT: 0`. All findings below are should-fix or nice.
Round 3 converged: **must-fix = 0**.

### should-fix

**S1 — quote-scan gate is vacuous for 12 `distillation-only` sources**
- where: `provenance-ledger.md:114-121`; validator WARN line; `.claude/rules/rights-and-quotation-policy.md`
- lenses: deterministic (WARN) + profile-reviewer (deduped — same defect)
- problem: package ships no `sources/markdown/` and no warm cache module, so the verbatim-quotation
  control the rights policy requires before release has never actually run against source text. The
  ledger self-discloses this rather than hiding it, and the profile text spot-checks as paraphrase,
  but the deterministic control did not execute. WARN, not FAIL — does not block in-repo use.
- fix: before any release beyond this repo's own `.claude/agents/generated/`, rehydrate
  `sources/markdown/` (or a warm cache module) and re-run `quote_scan` for real; record the actual
  result in the ledger, replacing the "PASS is vacuous" note.

**S2 — profile body ~1000 words: zero headroom under the hard-FAIL ceiling**
- where: `profile.yaml` — the fields `profile_self_check.py` check 14 sums (role, when_to_use,
  when_not_to_use, inputs.required, outputs, quality_bar, forbidden_behaviours, handoff_rules,
  source_of_truth_policy.precedence)
- lens: profile-reviewer
- problem: hand-recount lands ~1000w — in the 800–1000 WARNING band and touching the 1000w hard
  FAIL. This is the most plausible source of the reported `phase8 ... WARNING`; every other
  structural check passes. CHANGELOG 1.1.0 already records this profile sitting at 985w once. The
  next edit (fold-in, added forbidden behaviour, added quality_bar clause) tips it to hard FAIL.
- fix: trim ~150–250w of prose (**not** citations) from the heaviest sections — `quality_bar`
  (~208w), `forbidden_behaviours` (~147w), `inputs.required` (~131w) — to restore headroom below
  800, same technique used on presentation-design-advisor (1083w FAIL → 941w WARN).

**S3 — orphan citation: P100 cited but never restated**
- where: `profile.yaml:280` (`knowledge_partition.always_on[10]` citation list) vs
  `principles/principles.yaml:2335` (P100) and `reports/faithfulness-report.yaml:360-368`
- lens: faithfulness-reviewer
- problem: P100 (real-word reading / spelling / word-attack as reading-comprehension diagnostics)
  appears in the always_on[10] citation list, but no sentence in that block draws on it — the terms
  appear nowhere in the profile. Not an over-claim (nothing stated more strongly than source), but
  the faithfulness report's finding asserts P100 *is* restated, which makes the citation trail
  unreliable for anyone tracing P100's operational use.
- fix: either add a P100-grounded sentence to always_on[10], or drop P100 from the citation list;
  either way correct the faithfulness-report note so it no longer claims P100 is restated.

**S4 — no explicit fallback when a self-lookup of a principle code fails**
- where: `profile.yaml:52-56`; `.claude/agents/generated/learning-science-advisor.md:171-173`
- lens: ai-agent-engineering-reviewer
- problem: Required-inputs tells the agent to resolve package pointers against repo root (or Glob)
  and to verify any code absent from `Operating invariants` by reading the matching skill file or
  the principles index before citing it. Good anti-hallucination guardrail, but it has no stated
  fallback if that lookup fails — cwd not the factory root, package deployed standalone via
  `export-deployable` without the skills tree, or the code absent everywhere. The existing abstain
  path covers missing *user* context only, not missing *self* context. Agent could silently drop the
  citation, paraphrase from memory, or stall.
- fix: add one sentence to the Required Inputs block: "If a cited code cannot be located in
  Operating invariants, the matching skill file, or the principles index, say so and give the
  recommendation without that citation rather than paraphrasing from memory or guessing the path."

**S5 — no explicit self-check section in any of the 15 skill bodies**
- where: all 15 `skills/*/SKILL.md`, e.g. `retrieval-practice-and-low-stakes-quizzing/SKILL.md:80-82`
- lens: agent-skills-advisor
- problem: Output sections carry a generic "order findings highest-impact first, mark where evidence
  is uncertain" line, but no structured pre-finalization checklist. Weakens self-verification
  relative to the procedure / anti-pattern / worked-example rigour already present.
- fix: add a short `## Self-check` section (3–5 bullets) to the shared skill body template, reusing
  the existing advisory-boundary and output-floor language so it applies uniformly across all 15.

**S6 — trigger overlap: evidence-appraisal vs expertise-development (far-transfer claims)**
- where: `skills/evidence-appraisal-and-learning-myths/SKILL.md:3-5` vs
  `skills/expertise-development-and-transfer/SKILL.md:3-6`
- lens: agent-skills-advisor
- problem: "does this brain-training app's far-transfer claim hold up?" plausibly matches both
  descriptions; neither states which owns it.
- fix: add a differentiating clause to each — evidence-appraisal: "...for a technique, product, or
  myth proposed for adoption"; expertise-development: "...for a practice/training regime already in
  place whose own transfer claim needs checking."

**S7 — trigger overlap: motivation-belonging vs development-diversity (group→individual)**
- where: `skills/motivation-belonging-and-classroom-climate/SKILL.md:3-5` vs
  `skills/development-diversity-and-individual-differences/SKILL.md:3-4`
- lens: agent-skills-advisor
- problem: both touch stereotype/demographic territory (P023 climate mechanism vs P132/P134 not
  converting group statistics into individual capacity judgments); "may I use demographic data to
  differentiate for this group?" matches both.
- fix: boundary clause each — motivation-belonging: "...for climate and psychological-safety effects
  during instruction"; development-diversity: "...for design or assessment decisions that treat a
  group statistic as an individual verdict."

**S8 — expertise-development description is a dense single compound sentence**
- where: `skills/expertise-development-and-transfer/SKILL.md:3-6`
- lens: agent-skills-advisor
- problem: one long compound sentence, harder to scan for trigger vocabulary than its 14 siblings
  (contrast `memory-mnemonics-and-recall-accuracy/SKILL.md:3-5`).
- fix: split into two short clauses, front-loading the primary trigger: "Matches practice supports to
  a learner's expertise level as it develops... Requires objective untrained-outcome evidence before
  crediting a far-transfer claim." [P015]/[P061]

### nice

**N1 — two-tier invariant design is not self-evident in the adapter**
- where: `.claude/agents/generated/learning-science-advisor.md:21-133` vs `:198-266`
- lens: ai-agent-engineering-reviewer
- problem: `Operating invariants (must hold)` lists ~55 codes; quality_bar / forbidden_behaviours /
  handoff_rules / examples cite ~35 more (P013, P126, P107, P028, P067, …) that never appear there.
  All were traced to `knowledge_partition` skill prose — none orphaned — so this is a deliberate
  curated-subset-plus-wider-corpus split, but a maintainer reading only the adapter must
  reverse-engineer it.
- fix: one line under the `Operating invariants` heading: "Codes cited elsewhere in this profile that
  do not appear above are grounded in the matching skill file, not omitted from must-hold status."

**N2 — cognitive-load vs expertise-development: time-span boundary only in frontmatter**
- where: `skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:49-54` vs
  `skills/expertise-development-and-transfer/SKILL.md:51-56`
- fix: add one "When to use" bullet each restating the boundary explicitly (cognitive-load:
  "...within one lesson or task, not across a multi-week practice regime").

**N3 — three worked examples converge on the same reread-then-underperform scenario**
- where: `retrieval-practice-.../SKILL.md:100-104`, `metacognition-.../SKILL.md:100-104`,
  `evidence-appraisal-.../SKILL.md:102-106`
- fix: differentiate framing per skill — retrieval = quiz/format mechanics; metacognition =
  habit/self-regulation diagnosis; evidence-appraisal = technique-adoption decision.

**N4 — memory-mnemonics forensic content may under- or oddly trigger**
- where: `skills/memory-mnemonics-and-recall-accuracy/SKILL.md:48`, `:54`
- problem: forensic/consequential-interview vocabulary (neutral prompts, leading wording, repeated
  imagination) sits far from classroom mnemonic-cue vocabulary; a legal/interview query wouldn't
  obviously route to a "learning science advisor."
- fix: bridging clause in the description — the skill spans "classroom mnemonic systems and any
  high-stakes recollection whose accuracy must be judged."

**N5 — frontmatter `provenance` blocks may exceed the always-loaded budget**
- where: all 15 skill frontmatters, e.g. `retrieval-practice-.../SKILL.md:8-42`
- problem: each carries principle ids + 13–16 claim ids + digest, beyond a ~100-token
  always-loaded budget *if* the runtime parses full frontmatter rather than name+description only.
- fix: no action if this is confirmed factory-wide convention (sibling packages use the identical
  pattern); worth a one-time check of what the runtime actually loads at trigger time.

**N6 — development-diversity description is grammatically dense**
- where: `skills/development-diversity-and-individual-differences/SKILL.md:3-4`
- fix: simplify to "...when age, grade, or demographic averages are being used in place of a
  learner's demonstrated readiness."

**N7 — cross-package routing: course-design overlap with instructional-design-advisor**
- where: `.claude/agents/generated/learning-science-advisor.md:3` vs
  `.claude/agents/generated/instructional-design-advisor.md:3`
- problem: this package's when-to-use includes "course and online design" plus a full
  `course-design-technology-and-online-teaching` skill; the sibling is scoped to "instructional and
  course design." A generic "review my course" could match either. Both correctly state boundaries by
  capability (no sibling naming), so this is a catalog-level concern, out of this package's altitude.
- fix (not this pass): during a catalog routing audit, confirm the intended split (learner-cognition
  mechanism vs design-process/backward-design) is legible from the two descriptions alone.

## Positive confirmations (explicitly in scope, no defect found)

- **Subagent independence**: no `when_to_use` / `when_not_to_use` / `handoff_rules` entry names a
  sibling subagent; all exclusions are capability-stated; handoffs name generic responsible parties
  ("the teacher, designer, or institution", "a qualified specialist"). Compliant.
- **Tool boundary**: adapter is `Read, Grep, Glob` only; no write/execute grant or implied capability
  anywhere in the body (grep-verified — only hits are the DO-NOT-EDIT header, "execute" describing a
  *learner's* action, and "may edit canonical: False").
- **Domain-risk fencing**: clinical diagnosis (P134/P132/P115), placement/grading/admission/
  employment decisions (P128/P087), certainty/generality over-claim (P072/P125/P143/P105), and
  invented numeric precision are each fenced in `forbidden_behaviours`. The numeric effect sizes in
  `examples[1].ideal_response` (0.18/0.09/0.18) were verified to be carried directly from P103's own
  statement — no conflict with the no-invented-precision rule.
- **Over-claim**: ~90 of ~150 cited principle codes independently traced; **no CONTRADICTED,
  SCOPE_BROADENED, or HEDGING_REMOVED instance found**. Source hedges are preserved throughout
  (P125's "except complex structured/higher-order", P143's "far transfer explicitly uncertain",
  P011/P103's "unless evidence shows a stable crossover", P021's four joint difficulty conditions,
  P091's supervise-unless-independent-error-detection exception, P064's "can help", P134's
  group-to-individual bar). Every principle carrying a numeric effect size (P084, P103, P130)
  checked.
- **Faithfulness report not stale**: documents and corrects a prior HEDGING_REMOVED miss on
  `quality_bar[2]` and prior citation drift on `when_not_to_use[4]` / `outputs.primary_format` —
  consistent with the r1/r2 review-loop commits (`546c15c`, `a80b30e`).
- **Skill structure**: all 15 carry valid frontmatter within length/character limits, a consistent
  Purpose → When to use → Procedure → Inputs → Output → Anti-patterns → Worked example → References →
  Provenance body, working relative reference paths, and a repeated advisory-boundary sentence. The
  `provenance.principles` lists partition cleanly with **zero duplicate principle ownership** across
  the 15 files.
- **Provenance / supersession**: ledger and CHANGELOG carry full 1.0.0 → 1.1.0 → 1.2.0 entries,
  including the table of 4 authored (non-distilled) fields and the resolution note for P092/P098
  (cited in `always_on` while carrying `profile_rule: false`). No orphan profile field found.
- **Rights**: all 12 sources carry `rights_status: distillation-only`; none `unknown`.

MUST_FIX_COUNT: 0
