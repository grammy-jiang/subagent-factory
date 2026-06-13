# Instruction Induction / Agent Distillation — research findings → factory integration

Source: `docs/Research/instruction-induction-agent-distillation/` (validated report, PASS 1.00,
2026-06-13). Output-quality research topic (§20). This doc distils the actionable findings and maps
each to the factory's Phase 5 (principle→behaviour tests), Phase 8 (skill/reference authoring), and
Phase 9 (adapter export). It is a **spec for implementation**, not yet built.

## Core thesis
Turning declarative principles into a good agent persona is *compile + gate*, not *prose*: mine
candidate rules/examples with the LLM, then **type, dedup, compile, and replay-gate them
deterministically** before anything enters the adapter. Mirrors SkillCAT assess-before-merge and
Trace compile-to-check.

## Recommendations (each → factory mapping)

1. **Atomic, typed rules with machine-checkable triggers**, not prose paragraphs — compile
   "must-hold" principles into checks the adapter/validator enforces. *Trace: 100%→2% OOD violation.*
   → extends Phase 9 adapter (an **enforced invariant layer**) + a validator check.
2. **Gate every generated rule/example through deterministic assessment** — keep only those that do
   not regress the package's behaviour tests. → the existing `tests/principle-behaviour-tests.yaml`
   is the natural **replay harness** (Phase 5). *SkillCAT: induced > human-written by +45.8 pts.*
3. **Type the rule store** — syntactic/format invariants → deterministic rules; semantic/judgement
   guidance → conflict-aware structured schema; detect conflicts deterministically, resolve wording
   with the LLM. → feeds Step 7 conflict-log + a typed principle/rule schema.
4. **Select/author few-shot examples by expected task utility, not similarity** — prefer examples
   that demonstrably change behaviour on the package eval. → upgrades the **adapter-quality gate**
   from "examples EXIST" toward "examples are GOOD".
5. **Include failure-and-recovery worked examples, not only happy-path.** → adapter example contract.
6. **Express decision policies explicitly + auditably** (decision tables / ordered rules), reserving
   free LLM judgement for open-ended steps. Split the adapter into a *fixed enforced invariant
   layer* + an *induced improvable guidance layer*.
7. **Rubric-conditioned exemplar generation** — condition a strong model on the principle to draft
   the example, then strip the conditioning (RGSD); also curbs over-claiming (aligns with faithfulness).
8. **Validate grounding of every generated instruction/example against its source principle**
   (closed-evidence check) — the literature analogue of the repo's faithfulness / quote-scan gates.
9. **Cross-model transfer**: author rules/examples with a strong model even if the adapter runs on a
   smaller one — distilled artifacts lift weaker targets.

## Deterministic vs LLM split (engineering recipe)
- **LLM owns:** mining candidate atomic rules from principles, drafting worked examples,
  conflict-resolution prose.
- **Deterministic owns:** typing, normalisation, dedup, conflict detection, compiling checks, and
  the replay gate (behaviour tests) + grounding/quote scan. Every LLM output passes a deterministic
  gate before entering the adapter.

```
principle → [LLM: mine rules + draft examples] → [deterministic: type/dedup/conflict/compile]
          → [deterministic: replay vs principle-behaviour-tests + grounding scan] → adapter
                                                                       (fail/regress → back to LLM)
```

## Open gaps (carry to a budget-unlocked / non-sandbox session)
- **Foundational canon unreachable (HIGH, environment-limited):** the in-sandbox arXiv index is
  recency-locked to 2026-06, so Honovich *Instruction Induction*, APE, Self-Instruct, Constitutional
  AI, OPRO, KATE were not retrievable. Re-run with a full-history index / Semantic Scholar key to
  ground the recipe in its primary literature. (See [[arxiv-index-recency-locked]].)
- **Direct *principle → behavioural-rule-for-persona* transform (HIGH):** covered only by analogy
  in the 2026 index.
- **Worked-example *generation* (vs selection) for a persona (MEDIUM):** the factory must author
  examples, not just retrieve them.

## Build priority when implementing (highest output-quality leverage first)
1. Rec 2 + 4 — wire the **replay gate** (behaviour-tests) over generated rules/examples and switch
   example selection to utility (both lean on existing deterministic infra).
2. Rec 1 + 6 — split the adapter into enforced-invariant vs induced-guidance layers; compile
   must-hold principles to checks.
3. Rec 5 + 8 — failure-recovery examples + per-example grounding check.
