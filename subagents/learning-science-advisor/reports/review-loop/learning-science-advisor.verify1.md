# Adversarial verify — learning-science-advisor (verify1)

Gate: Step 6 of `/review-subagent`. Package `subagents/learning-science-advisor/` at `agent_version: 1.2.0`.
The review loop reported must-fix = 0 at r3; this gate re-derived independently and did **not** read or
trust `reports/faithfulness-report.yaml` or any `reports/review-loop/*.review.md` verdict.

Two independent reviewers ran in parallel:

1. **faithfulness re-derivation** — every profile rule re-graded against the cited principle's own
   `statement` in `principles/principles.yaml` (all 150 principles read; no dangling `P###`).
2. **adapter safety / invariant integrity** — `.claude/agents/generated/learning-science-advisor.md`
   invariant layer recompiled with `compile_invariants` and diffed byte-for-byte against the installed
   adapter; frontmatter parsed; whole file scanned for truncation signatures.

Both reviewers independently landed on the same defect class. All three loci below were re-confirmed by
hand from `principles.yaml` before being recorded here.

---

## MUST-FIX

### MF1 — `forbidden_behaviours[0]` cites two principles that do not state it (`profile.yaml:94-95`)

RULE:

> `- Teaching the content, delivering the course, writing the materials, or marking the work for the caller (P010, P077).`

CITED:

- **P010** — *"Translate a general learning principle through its underlying mechanism, then adapt the
  implementation to the local learners, course format, workload, and institution."* (confidence: medium)
- **P077** — *"Treat personal educational experience as practical context rather than proof: adapt
  disciplinary expertise and prior teaching methods using evidence about the actual students and
  setting instead of projecting one's own learning experience."* (confidence: medium)

GRADE: **SCOPE_BROADENED (mis-citation)**

WHY: Neither statement is about *who performs* teaching, delivery, authoring, or marking. P010 is
mechanism-first translation into a local implementation; P077 is not treating one's own learning history
as evidence. The boundary itself is correct and load-bearing — the defect is that it is dressed as a
distilled corpus principle, asserting grounding the statements do not carry. This violates the repo's
"no orphan field values / every field traceable to its QID" rule from the other direction: a citation
that resolves to the wrong content is worse than no citation. The profile already knows the honest
convention — `forbidden_behaviours[5]` is tagged `(authored evidence guardrail)` and `[6]` `(authored
scope boundary)`. The same two IDs are used *correctly* at `profile.yaml:306-308` in the course-design
always_on block, which is why the error is invisible to an ID-existence check.

MINIMAL FIX:

```yaml
- Teaching the content, delivering the course, writing the materials, or marking the work for the caller
  (authored scope boundary).
```

### MF2 — `forbidden_behaviours[2]` cites two principles that do not state it (`profile.yaml:98-99`)

RULE:

> `- Making or predicting a placement, grading, admission, promotion, or employment outcome, or guaranteeing a named learner's result (P128, P087).`

CITED:

- **P128** — *"Assess analytical reasoning, creative adaptation, practical execution, and
  context-developed expertise instead of inferring total competence from one school-centered static
  score."* (confidence: medium)
- **P087** — *"Match expectations and supports responsively to the learner's emerging competencies and
  demonstrated developmental readiness — treating timing as variable rather than a rigid age schedule —
  while still providing supported challenge and time for growth."* (confidence: high)

GRADE: **SCOPE_BROADENED (mis-citation)**

WHY: P128 is about *what to assess* (plural competence dimensions, not one static score); P087 is about
*pacing expectations* to demonstrated readiness. Neither says the advisor must not make or predict a
placement, grading, admission, promotion, or employment outcome. That is an authored authority boundary.
Note the adjacent `forbidden_behaviours[1]` (`P134, P132, P115`) *is* genuinely grounded — P134 states
"use group categories for bounded population inference without converting them into individual capacity
judgments" — so this is a localised provenance error, not a systemic one.

MINIMAL FIX:

```yaml
- Making or predicting a placement, grading, admission, promotion, or employment outcome, or guaranteeing
  a named learner's result (authored scope boundary).
```

### MF3 — `handoff_rules[0]` carries the MF1 mis-citation into the ownership rule (`profile.yaml:109-110`)

RULE:

> `- The teacher, designer, or institution owns curriculum, materials, delivery, and marks; this advisor informs the design reasoning and names the residual trade-off (P010, P077).`

CITED: P010 and P077 (statements as quoted in MF1).

GRADE: **SCOPE_BROADENED (mis-citation)**

WHY: "owns curriculum, materials, delivery, and marks" is an authority allocation present in neither
statement. P010's mention of "institution" is a *context to adapt to*, not an ownership claim; P077 is
silent on ownership. Same root cause as MF1.

MINIMAL FIX (keeps P010 attached only to the clause it actually supports, drops P077):

```yaml
- The teacher, designer, or institution owns curriculum, materials, delivery, and marks; this advisor
  informs the design reasoning, translating each principle through its mechanism before adapting it to
  the local learners, format, workload, and institution (P010), and names the residual trade-off
  (authored scope boundary).
```

**Blast radius of MF1–MF3:** all three are exported verbatim into the installed adapter at
`.claude/agents/generated/learning-science-advisor.md:219`, `:223`, `:237` — the runtime agent reads the
false provenance. Fix is profile-only + MINOR/PATCH version bump + `cli export` + `validate`. No
behavioural text changes, so no re-review of the boundary semantics is needed.

---

## ADVISORY (real, below the must-fix bar — not counted)

- **`handoff_rules[1]` (`profile.yaml:111-112`, `P134, P128`)** — P134 genuinely grounds the
  "don't convert group evidence into an individual capacity judgment" half; P128 grounds neither
  "belongs to a qualified specialist" nor "decisions to the responsible body". Partial mis-citation, but
  the core clause is grounded, so it does not gate. Fix alongside MF2 if touching the file.
- **`operational_mapping.profile_rule: false` on two cited principles** — P092 (closed-resource exit
  prompt) is cited in the retrieval always_on block (`:139`) and P098 (notice-and-wonder opening) in the
  prior-knowledge block (`:187`), yet both carry `profile_rule: false` in `principles.yaml`. The profile
  text matches those statements exactly; this is mapping metadata drift, not over-claim.
- **Orphan citations (under-claim, not over-claim)** — `:280` cites P100 and P104 in the
  expertise/transfer block with no corresponding clause; `:260-261` states the far-transfer rule that
  P039 supports without citing P039 there (P039 *is* cited for the identical clause at `:103` and `:278`).
- **P100 invariant voice (`adapter :102`)** — "Collect real-word reading, spelling ability and word
  attack skills as the diagnostic measures…" reads, in isolation, close to the forbidden "diagnosing a
  learner". Not scored: all 54 invariants are in practitioner-imperative voice addressed to the teacher,
  and the adapter disambiguates three times (Role line, invariants preamble, Precedence: "the invariants
  below are advisory criteria, not authority to act; the advice-only boundary and forbidden behaviours
  override them"). Optional hardening: reframe as "Advise that reading-comprehension screening collect…".
- **Validator WARN** — `quote-scan: rights NOT verified — 12 restricted source(s) but no source text
  available`. All 12 sources are `distillation-only`; the verbatim-quote gate could not run because this
  worktree has no `sources/markdown/` or warm cache. The no-quotation rule is therefore unverified for
  this package. Outside this gate's scope; run quote-scan where the source text is present.

---

## PASSED (independently re-derived)

**Adapter integrity**

- **No truncation.** 54 invariant lines, zero hits for `…`/`...`, unbalanced `(`/`[`/`"`/backtick/`**`,
  or a trailing `(e.g`. Each invariant re-derived from its source principle statement: every must-hold
  statement renders as a complete single sentence, no dropped tail on any of the 54. (The uniform absence
  of a terminal period is `_to_invariant`'s deliberate `rstrip(" .;,")` rule-head style, not a cut.)
- **No invariant drop.** `compile_invariants` yields 54; the adapter carries 54; set difference empty in
  both directions; all 54 texts match character-for-character. `attach_invariants` is not set to `false`
  anywhere in `profile.yaml` — the known "green but the whole must-hold layer is gone" failure mode is
  absent here.
- **Profile → adapter coverage.** `role`, `router_description`, `when_to_use` (5), `when_not_to_use` (5),
  `inputs.required` (5), all 3 modes' trigger+output, `quality_bar` (7), `forbidden_behaviours` (7),
  `handoff_rules` (3), `canonical_owner`, `precedence`, and all 15 skill + 2 reference pointers appear
  verbatim. Nothing dropped. (`knowledge_partition.always_on` is not rendered by the adapter template at
  all — factory-wide behaviour; its 15 entries map 1:1 to the 15 listed skill files.)
- **Advice-only role holds.** No instruction, invariant, mode, example, or skill reference authorises
  teaching content, delivering the course, writing materials, grading, diagnosing a condition, or making
  placement/admission/employment calls. The three worked examples reinforce it ("You own the revision plan
  and the materials", "The purchase decision stays with you", plus a full refusal-and-redirect in the
  failure-recovery example). Plausible invariant conflicts checked pairwise (P008 vs P084; P130 vs
  P011/P103) — each scope-distinct, none contradictory.
- **Numeric guardrail holds.** Every effect size in the adapter (invariants P084 `d = 0.19`, P103
  `0.18/0.09/0.18`; worked example 2) is carried in the invoked principle's own statement — compliant
  with `forbidden_behaviours[5]`, not a breach.
- **Generated-file header** present at line 8, within the first 20 lines (factory's multi-line form,
  matching `templates/claude-agent-adapter.md.j2` and the repo gate at
  `validate_adapter_quality.py:106`).
- **Frontmatter sanity.** Valid YAML; `name: learning-science-advisor` matches slug and package dir;
  `tools: Read, Grep, Glob` — read-only, not widened; no `patch_policy` rendered; description names no
  other subagent and carries no routing/handoff language (subagent-independence rule holds).
- **Adapter/package parity.** `.claude/agents/generated/learning-science-advisor.md` is byte-identical to
  `subagents/learning-science-advisor/adapters/claude-code/learning-science-advisor.md` — a true export
  of profile v1.2.0, not hand-edited drift.
- **Repo validator re-run independently:** `VALIDATION PASSED`, 0 FAIL, 1 WARN (the quote-scan WARN above).

**Faithfulness — re-derived clean**

- `quality_bar` QB1–QB6 (P085/P013/P126 · P059/P060/P107/P050 · P125/P061/P142/P028 · P009/P101/P067/P047/P136
  · P053/P007/P011/P103/P033 · P140/P070/P023/P088/P099); QB7 authored floor; `minimum_useful_output`
  structural. P125's "complex structured / higher-order uncertain" hedge is preserved, not stripped.
- `forbidden_behaviours` [1] (P134/P132/P115), [3] (P072/P125/P143/P105), [4] (P011/P103/P074/P039 —
  P011's "stable crossover" hedge preserved at `:255-256`), [5] and [6] honestly tagged authored.
- `handoff_rules[2]` authored scope boundary. `source_of_truth_policy.precedence`
  (P072/P010/P009/P143/P125/P105/P134) is a hedge-preserving directive.
- All 15 `knowledge_partition.always_on` blocks (AO1 retrieval → AO15 collaborative), every cited `P###`
  resolved and re-graded against its statement — no SCOPE_BROADENED, HEDGING_REMOVED, or CONTRADICTED.
- `modes` advise/review/plan; `router_description`, `when_to_use`, `when_not_to_use`, `inputs`, `outputs`
  (no principle citations; they mirror the forbidden/handoff boundaries). Examples EX1–EX3 — every inline
  citation re-derived and consistent.

---

## Verdict

The package is structurally and behaviourally sound: the invariant layer is complete and untruncated, the
advice-only role is enforced consistently, and the substantive advice rules are faithfully within their
principles' scope. The surviving defect is a **provenance** defect — three boundary rules carry principle
codes that do not state them. Because those citations ship in the installed adapter and the repo requires
every field to be traceable to what it cites, they gate.

MUST_FIX_COUNT: 3
