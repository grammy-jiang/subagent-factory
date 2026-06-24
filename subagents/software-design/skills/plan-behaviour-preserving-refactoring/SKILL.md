---
name: plan-behaviour-preserving-refactoring
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P016
  - P001
  - P010
  - P026
  claims:
  - C00256
  - C00450
  - C00493
  - C00542
  - C00573
  - C00574
  - C00575
  - C00592
  - C00593
  - C00594
  - C00597
  - C00598
  - C00609
  - C00643
  - C00644
  - C00645
  source_anchors:
  - 0574f24ece08-c0000
  - 5b1b9ca368a5-c0000
  - 5b1b9ca368a5-c0001
  - 5b1b9ca368a5-c0003
  - 5b1b9ca368a5-c0004
  - 5b1b9ca368a5-c0005
  - 5b1b9ca368a5-c0006
  - 5e67c59e0e18-c0003
  authored_from_digest: 944eb8d8724631afd8bd590d6501921f40dc990aa9c964a7c20ce0af83d38f29
---

# plan-behaviour-preserving-refactoring

## Purpose

Plan and sequence the smallest safe structural change that improves a codebase's internal
organisation without altering its observable behaviour (clm-057, PRC-010). Refactoring is
worth doing because it keeps the internal design sound, makes code easier to follow, helps
surface latent bugs, and allows future work to proceed more quickly (clm-059, PRC-011). The
skill walks a reviewer through six ordered steps: confirming the goal is genuinely
behaviour-preserving; gating progress on a self-testing suite; ruling out the cases where
refactoring should not proceed; naming each triggering smell; scheduling atomic moves that
individually keep every test green; and verifying that no step inadvertently carries a
behaviour change (PRC-012, PRC-013).

This skill produces a written plan and design sketch only. The reviewer recommends and
describes; it makes no autonomous code changes.

## When to use

Use this skill when:

- A code smell has been named (PRC-013, clm-063) and the question is how to remove it
  without altering observable behaviour.
- A feature or defect fix is being blocked by the current structure, making preparatory
  refactoring worthwhile before proceeding (clm-060, PRC-011).
- The Rule of Three has fired — a similar construct has appeared for the third time and
  duplication is no longer coincidental (clm-060, PRC-011).
- A caller requests the **patch-suggest** mode: the smallest change that removes a named
  flaw without opening a broader rewrite.
- An ongoing change is conflating restructuring with behaviour change and the two
  activities need to be disentangled before continuing (clm-058, PRC-010).

Do **not** use this skill when:

- The code is so comprehensively broken that no sequence of behaviour-preserving moves
  will reach a sound design; a targeted rewrite is then more appropriate (clm-061,
  PRC-011).
- The affected code is stable, is not being modified, and its internal complexity is
  fully hidden behind a clean interface; noting the smell for the record is then
  sufficient (clm-061, PRC-011).
- The goal is a behaviour change, a new feature, or a performance improvement — those
  belong to the feature hat and must not be conflated with refactoring (clm-058,
  PRC-010).

## Procedure

> **Reviewer note.** Every step produces findings, recommendations, and design sketches.
> This reviewer recommends and plans; it does not make or approve autonomous code changes.
> A significant restructuring may feed a design-it-twice or incremental-change plan before
> implementation begins.

---

### Step 1 — Confirm the goal is behaviour-preserving and identify the hat

Before any structural analysis, answer two questions explicitly:

1. **Is this purely a structural improvement?** The proposed change must alter only how
   the code is internally organised, not what it does externally. If observable behaviour
   would change — even beneficially — that is feature work, not refactoring (clm-057,
   PRC-010).

2. **Which hat is being worn right now?** The refactoring hat means no new capability is
   added in this session. The feature hat means no structural cleanup is folded in. The
   two hats must not be worn simultaneously (clm-058, PRC-010).

**Output:** a brief statement — *"goal is behaviour-preserving structural improvement"* or
*"goal mixes feature change with restructuring (flag: separate the two before
proceeding)."*

If the goal mixes both activities, record it as a finding, recommend the activities be
separated into distinct passes, and do not proceed further until the scope is clarified.

---

### Step 2 — GATE: verify the self-testing suite

Refactoring is only safe when a fast, automatically-reported test suite that catches any
behaviour change is already in place and passing before work starts (clm-062, PRC-012).
Automated tests are what keep production code flexible, maintainable, and reusable; without
them, restructuring carries an unacceptable risk of silent regression (clm-051, PRC-012).

Assess the state of automated tests over the affected code:

| Test-suite condition | Reviewer action |
|---|---|
| Fast self-testing suite present and covering the affected behaviour | **Gate passes** — proceed to Step 3 |
| Tests exist but do not cover the affected behaviour adequately | **Gate fails** — record as **top finding**, characterise the gap, recommend extending tests before proceeding, and stop planning the refactoring |
| No automated tests exist over the affected code | **Gate fails** — record as **top finding**, require a test suite be put in place first, and stop |

**If the gate fails, the primary finding is the missing or insufficient test suite, not
the structural smell.** The reviewer's lead recommendation becomes "write the tests
first." Do not proceed to Steps 3–6 until the gate is confirmed to pass.

---

### Step 3 — Check the "do not refactor now" conditions

Even when the gate passes, two conditions indicate that refactoring should be deferred or
abandoned (clm-061, PRC-011):

1. **Rewrite-instead condition.** The code is so structurally compromised — fundamentally
   incorrect logic or severely broken data models — that no series of behaviour-preserving
   moves will reach a sound design. Recommending a bounded rewrite within a clean interface
   is more appropriate than planning an incremental refactoring.

2. **Stable-behind-a-clean-interface condition.** The internal complexity is real, but the
   code is not being modified and callers see only a stable, clean interface. Under these
   circumstances the smell is worth noting for the record but does not warrant immediate
   action.

**Output:** either *"neither condition applies — proceed"* or a specific finding naming
which condition holds, with the appropriate recommendation (rewrite scope, or note-only).

---

### Step 4 — Identify the triggering smell(s) and match each to a refactoring

Consult the code smell catalogue (PRC-013, clm-063) to name every smell present in the
affected code. For each smell, select the most appropriate behaviour-preserving refactoring
move.

**Common smell → refactoring pairings**

| Smell | Indicator | Recommended refactoring move |
|---|---|---|
| Long function / needs a comment | A fragment requires a comment to explain what it does | **Extract Function** — give the fragment its own well-named function (clm-072) |
| Duplicated code | The same logic appears in two or more places; Rule of Three has fired | Extract into a single authoritative location (clm-060, PRC-009) |
| Long parameter list | A function takes so many parameters that call sites are hard to read | Introduce a parameter object or preserve the whole object |
| Divergent change | One module is modified for several unrelated reasons | Split by responsibility (PRC-015) |
| Shotgun surgery | One logical change forces edits scattered across many modules | Consolidate the scattered logic into one place (PRC-001) |
| Feature envy | A method is more interested in another module's data than its own | Move the method closer to the data it uses |
| Data clumps | Several data items always travel together across boundaries | Encapsulate them into a value or parameter object |
| Primitive obsession | Domain concepts are represented by raw primitive types | Introduce a dedicated value object |

> This table covers the most commonly triggered smells. The full catalogue is in
> `../../references/fowler-code-smell-catalogue.md` (PRC-013).

For each smell identified, record: (a) the smell name, (b) the specific location, (c) the
chosen refactoring move, and (d) the principle or claim that grounds the choice.

---

### Step 5 — Sequence the work as small, green-keeping steps

Break the chosen refactoring(s) into the smallest atomic moves where each move individually
leaves the test suite green (PRC-012, PRC-010). Smaller steps are safer: when a step
causes a test failure, it reveals exactly one narrow move as the cause (PRC-008).

**Sequencing heuristics:**

1. **Prepare before moving.** Extract a fragment into a well-named function first, then
   move or consolidate it — each step is independently verifiable.
2. **One smell, one session.** Plan each distinct smell as a separate pass rather than
   addressing all smells simultaneously.
3. **Prefer the simplest move.** The goal is the minimum structurally sound change that
   removes the smell, not a comprehensive redesign (PRC-007, PRC-019).
4. **State the expected test outcome for each step.** All existing tests must continue
   to pass after every individual move; no new failures are acceptable.

**Output:** an ordered list of named moves — for example, *"Move A: Extract Function
`computeDiscount` from the block at lines 42–58 of `OrderProcessor`; expected result: all
tests pass. Move B: …"* — with a brief rationale for each.

---

### Step 6 — Verify the entire sequence stays behaviour-preserving

Review the complete planned sequence for any step that would — even incidentally — change
observable behaviour:

- A renamed public symbol that callers depend on changes the visible interface.
- Reordered evaluation where any step has side-effects changes behaviour.
- A deleted branch that appeared dead but was exercised at runtime is a behaviour change.

Flag any such step explicitly. If a step cannot be made behaviour-preserving, remove it
from the refactoring plan and record it separately as a candidate behaviour change to be
scheduled under the feature hat in a distinct session (clm-058, PRC-010).

**Output:** a final, reviewed sequence of planned moves, each confirmed as
behaviour-preserving, plus a list (possibly empty) of deferred steps and the reason each
was removed from the refactoring plan.

---

### Consolidated output structure

After completing all six steps, assemble the finding under these headings:

1. **Goal verdict** — behaviour-preserving / mixed-hat (recommend separation).
2. **Test-gate verdict** — pass / fail (with gap description and remedy if fail).
3. **Refactoring eligibility** — proceed / defer-rewrite / defer-stable (with reason).
4. **Named smells** — smell name, location, grounding claim or principle for each.
5. **Planned move sequence** — ordered, named atomic moves, each confirmed green-keeping.
6. **Behaviour-change flags** — deferred steps and the reason each was removed.

## Inputs

| Input | Required? | Notes |
|---|---|---|
| The code or design artefact to be refactored | Required | A code listing, file reference, or design description sufficient to identify the structure in question |
| The triggering context | Required | Which hat is being worn and why — e.g., smell found during review, Rule of Three fired, preparing for a feature |
| Evidence that a self-testing suite exists and covers the affected behaviour | Required for gate | Test file references or a description of coverage; absence triggers the gate finding and stops the plan |
| The specific smell or flaw already named | Recommended | Pre-identified smells from the detect-code-smells skill accelerate Steps 3–4 |
| Scope constraints | Optional | Any boundary on which code may be touched in this refactoring session |

## Output

A structured refactoring plan comprising:

- **Goal verdict** — confirms the scope is purely behaviour-preserving, or flags the
  mixed-hat problem.
- **Test-gate verdict** — pass or fail, with a gap description and recommended remedy if
  the gate fails.
- **Refactoring eligibility verdict** — proceed, defer-rewrite, or defer-stable, each
  with a named reason grounded in a principle or claim.
- **Smell catalogue** — each smell identified, its location, the chosen refactoring move,
  and the grounding principle or claim.
- **Ordered move sequence** — a numbered list of atomic, named refactoring moves, each
  expected to leave the existing test suite fully green.
- **Behaviour-change flags** — any steps removed from the plan, deferred to the feature
  hat, with a brief rationale.

The output is a plan and design sketch only, not replacement code. A significant
structural change may feed a design-it-twice comparison (PRC-020) before implementation
is handed to the engineer or tech lead who owns the affected code.

## References

- **Smell catalogue:** `../../references/fowler-code-smell-catalogue.md` — the named
  smell-to-refactoring index used in Step 4 (PRC-013).
- **Principles:** `../../principles/principles.yaml` — PRC-010 (behaviour-preserving
  discipline and the two hats), PRC-011 (opportunistic triggering conditions), PRC-012
  (test-gate prerequisite), PRC-013 (smell-driven refactoring heuristics).

## Provenance

Source rights: **distillation-only**. All content in this file is paraphrased from the
grounded sources; no verbatim text from any source is reproduced. Claims and principles
are cited by ID inline throughout. Evidence strength is not exceeded: no grounding that
states a preference is upgraded to an absolute rule. Primary grounding sources: Fowler,
*Refactoring: Improving the Design of Existing Code* (anchors
`martin-fowler-refact-0574f24e-h0102` through `martin-fowler-refact-0574f24e-h0185`) and
Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (anchor
`clean-code-a-handboo-5b1b9ca3-h0195`).
