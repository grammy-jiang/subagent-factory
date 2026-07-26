# Adversarial verify — instructional-design-advisor (verify1)

Gate: Step 6 of `/review-subagent`. The review→fix loop reported must-fix=0; this pass
re-derived everything independently and did **not** read or trust the loop's reports,
the authored faithfulness grades, or any prior verdict.

Panel run in parallel:

- **faithfulness re-derivation** — every rule-bearing field of `profile.yaml` re-graded
  against the quoted `statement` of its cited principle in `principles/principles.yaml`
  (five-level scale). ~100 of 200 principle statements cross-checked; all of
  `quality_bar`, `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy`,
  both worked examples, and a sample across all 13 `always_on` blocks.
- **adapter safety / invariant integrity** — `compile_invariants` re-run from
  `principles.yaml` and diffed against the installed adapter; programmatic truncation
  sweep over all 75 invariants; all 97 inline `PNNN` citations resolved; tool grant,
  header, and role-boundary check.

Both agent verdicts were then re-verified by hand against the source lines before being
admitted here.

---

## MUST-FIX 1 — invariant P157 drops the scope condition that bounds it (adapter, non-negotiable tier)

**Where:** `.claude/agents/generated/instructional-design-advisor.md:158`
(root cause: `principles/principles.yaml` P157 statement shape + `compile_invariants._to_invariant`
first-sentence reduction)

**Adapter text, exact:**

```
- **[P157]** Route words away from the visual channel when a graphic is present: pictures load the
  visual/pictorial channel and spoken words the auditory/verbal channel, but printed and onscreen text
  enters through the eyes first and competes with the graphic for the same limited channel
```

**Principle P157, full statement** (`confidence: high`):

> Route words away from the visual channel when a graphic is present: pictures load the
> visual/pictorial channel and spoken words the auditory/verbal channel, but printed and onscreen
> text enters through the eyes first and competes with the graphic for the same limited channel.
> **Prefer narration over concurrent onscreen text in a system-paced presentation.**

**Grade: SCOPE_BROADENED.** The second sentence carries the boundary condition
(*system-paced*). `_to_invariant` reduces the statement to its first sentence, so the
condition is dropped **only in the invariant layer** — every other artifact keeps it:

- `profile.yaml:179` — "...when a graphic must be processed at the same time in a **system-paced** presentation"
- `skills/multimedia-and-elearning-design/SKILL.md:51, 74, 93` — all three carry **system-paced**
- adapter — `grep system-paced` returns **zero** hits

This is the tier the adapter itself labels "Non-negotiable" and says "take precedence over
the softer guidance below" (`:23`), and the adapter does not render `knowledge_partition.always_on`
at all — so an agent reading the adapter (the runtime artifact) has the modality prescription at
its **highest** precedence with **no pacing condition**.

**Self-contradiction:** this directly trips the package's own Forbidden behaviour #3
(`profile.yaml:88-90`, adapter `:253`) — "Stating a design principle more strongly than its source
supports — omitting the conditions that make a rule hold... (P011, P122, P042, P092)" — and P011 is
itself an invariant (`adapter:42`): "state the conditions with the rule."

**Failure scenario:** caller submits a **learner-paced / self-paced** e-learning module with
on-screen text beside diagrams. The advisor applies P157 as a must-hold and prescribes converting
text to narration. The modality effect is not established for learner-paced presentation — which is
why the source hedged it — so the advisor issues an unsupported prescription while its own Forbidden
behaviours claim it never does.

**Minimal fix:** do not edit the adapter. In `principles/principles.yaml`, make P157's **first
sentence self-sufficient** (as `_to_invariant`'s contract requires), e.g. open with
`"In a system-paced presentation, route words away from the visual channel when a graphic is
present: ..."`. Then MINOR-bump `agent_version`, add a CHANGELOG entry, re-run `cli export`, and
confirm with `python -m tools.subagent_factory.compile_invariants subagents/instructional-design-advisor | grep P157`.

**Systemic scope, checked:** all 75 adapter invariants were scanned for a multi-sentence statement
whose dropped tail carries a scope/condition term. Exactly **two** hits — P157 (above) and P092,
whose dropped tail ("Say which criterion is missing when only one holds.") adds an action rather
than narrowing scope, so the retained clause is not broadened. **P157 is the only real instance.**

---

## MUST-FIX 2 — P107 (and P134) cited to ground ownership/authority claims they do not state

**Grade: SCOPE_BROADENED (mis-citation), four sites, one root cause.**

**P107, full statement** (`confidence: medium`):

> Make the teaching theory shaping the learning environment explicit, then use evidence and a
> coherent framework to diagnose problems and adapt responses to local learners and constraints.

**P134, full statement** (`confidence: medium`):

> Improve teaching through repeated, systematic action-research cycles grounded in disciplinary
> knowledge, learning theory, local evidence, and triangulation across students and trusted colleagues.

Neither says anything about **who owns** the course, the grades, the subject matter, or the decision
to run it. The advice-only ownership boundary is legitimate factory policy — but it is cited as if
principle-derived, which makes it an orphan field value dressed as sourced (`.claude/rules/rights-and-quotation-policy.md`,
Provenance requirement: "No orphan field values"). A rule asserting authority with no source behind
it is, by the letter of the faithfulness rule, stronger than its support.

Sites, most-load-bearing first:

1. **`profile.yaml:115-119` (`source_of_truth_policy.precedence`)** —
   "...the teacher of record, the content expert, and the institution own the course, the subject
   matter, and the grades, **which overrides every design invariant** (P107, P193)."
   P193 grounds only the subject-matter-expert clause ("Give a qualified content expert validated
   goals and skill frameworks as explicit review standards..."), and even that stops short of
   "owns". P107 grounds nothing here. This is the highest-severity site because it is the clause
   that claims to override the entire invariant layer.
   *Fix:* drop `P107`; keep `P193` on the subject-matter clause only; leave the ownership clause
   unmarked as factory policy.

2. **`profile.yaml:98-101` (`handoff_rules[0]`)** —
   "The teacher of record, the design team, and the institution own the course, the grades, and the
   decision to run it... (P107, P021, P134)."
   P021 legitimately grounds the criterion-based-judgement clause. P107 and P134 ground neither
   ownership nor "the decision to run it".
   *Fix:* drop `P107, P134`; keep `P021` on the outcome-judgement clause.

3. **`profile.yaml:106-113` (`source_of_truth_policy.canonical_owner`)** —
   "The teacher of record and the design team hold final authority over the course, its materials,
   and what is taught, making the teaching theory that shapes it explicit and adapting it to local
   learners and constraints (P107, P134)."
   Compound sentence: the **second** clause is genuinely P107/P134. The citation sits at the end,
   implying both clauses are sourced.
   *Fix:* split so the citation attaches only to the clause it supports — e.g. "...the design team
   makes the teaching theory that shapes the course explicit and adapts it to local learners and
   constraints (P107, P134). Final authority over the course and its materials rests with the teacher
   of record and the institution."

4. **`profile.yaml:93-95` (`forbidden_behaviours[4]`)** —
   "Assigning a grade... stay with the teacher of record and the institution (P021, P172, P107)."
   `P021` (protect criterion-based outcome judgement) and `P172` (convert the judgement through
   defensible grading rules) already ground this fully. `P107` is a spurious extra citation.
   *Fix:* remove `P107`.

**Direction note (for triage):** all four sites *restrict* the advisor rather than expanding what it
claims about instructional design, so blast radius on output quality is low. It is still a real
provenance defect and the fix is one mechanical pass over four lines + MINOR bump + re-export.

---

## Not must-fix (recorded, no action required at this gate)

- **Invariant-preamble carve-out is incomplete** (`templates/claude-agent-adapter.md.j2:23` →
  `adapter:23`). The "except..." clause names only Role and Forbidden behaviours; it omits
  `When NOT to use`, `Handoff rules`, and `Source of truth policy`, which also carry advice-only
  boundaries. Read literally, invariants outrank them. Already neutralised in practice by the Role
  paragraph (`adapter:19`), which states forbidden behaviours "override every invariant, so the
  advisor never builds the course, teaches it, grades learners, or certifies a programme".
  Template-wide, not this package's defect.
- **`minimum_useful_output` and `outputs.primary_format` never render.** `profile.yaml:46-49, 80-81`
  have no corresponding template block, so no generated adapter carries them. Systemic across every
  package; neither is part of the must-hold layer.
- **P092's dropped second sentence** ("Say which criterion is missing when only one holds.") — adds
  an action, does not narrow scope; retained clause is not broadened.

## Checks that PASSED

- **Truncation sweep:** 0/75 invariants show `…`/`...`, a dangling `(e.g` / `such as` / `including`,
  an unbalanced paren or quote, or an incomplete terminal clause. The historical
  `compile_invariants` 160-char truncation bug is not present; verified independently rather than
  by trusting `validate_invariant_coverage`.
- **Invariant fidelity:** `compile_invariants` output vs adapter — byte-identical; 0 missing,
  0 extra, 0 reworded.
- **Citation resolution:** all 97 inline `PNNN` references resolve in `principles.yaml`; 0 dangling.
  The known post-rebuild renumbering hazard for this package did not bite.
- **Profile→adapter fidelity:** when_to_use 5/5, when_not_to_use 4/4, inputs 1/1, modes 3/3,
  quality_bar 6/6, forbidden_behaviours 6/6, handoff_rules 2/2, source_of_truth 3/3 — verbatim.
- **Role boundary:** no mode, output spec, invariant, or example directs the agent to build, teach,
  grade, certify, or rule on subject-matter correctness. ~15 invariants use the instructional-design
  imperative voice ("Teach…", "Give students…") — that is the domain's design-criterion register,
  bounded twice (`adapter:19`, `:23`); the failure-recovery example (`:280-284`) actively declines both.
- **Tool grant:** `tools: Read, Grep, Glob` (`adapter:4`). No Write/Edit/Bash/MCP. PASS.
- **Header:** `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY.` at `adapter:8`, within first 20 lines. PASS.
- **Installed vs package adapter:** identical modulo the `Generated:` timestamp.
  `validate_generated_package` → VALIDATION PASSED.
- **Absolutist language spot-check:** every "never / refuses / requires / only" in the profile traces
  to an equally absolute or correctly-conditioned source statement (e.g. "refuses retention evidence
  alone as proof a design worked" ← P153's own "do not accept retention evidence alone").

MUST_FIX_COUNT: 2
