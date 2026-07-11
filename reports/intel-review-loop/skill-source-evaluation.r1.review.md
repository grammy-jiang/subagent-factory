# Review — `source-evaluation` SKILL.md (round 1)

**Target:** `intelligence-analysis-agent/.claude/skills/source-evaluation/SKILL.md` (83 lines)
**Grounding:** `subagent-factory/docs/intelligence-analysis/PIPELINE-grounded.md` (Step 3 row + store legs)
**Kind:** METHOD skill — the grading method the intel-analysis agent *runs* at Step 3 of `structured-analysis`. Not a reviewer.
**Reviewers:** `agent-skills-advisor` (authoring quality) + `ai-agent-engineering-reviewer` (method design). Consolidated + de-duped below.

---

## MUST-FIX

### MF1 — `get_source_history` gate lives in trailing prose, not the executable Procedure
`SKILL.md:66-71` vs numbered Procedure `:27-53`. The one gate the pipeline explicitly cares about — read the source's prior grade trend and the *direction of its most recent change* before grading a repeat source (Masterman C044) — appears only in the "Persistence" narration, disconnected from the ordered Procedure. An agent executing steps 1–7 mechanically has no step telling it to check history first, so the gate is silently skippable.
**Fix:** promote to an explicit Procedure step (e.g. new Step 2: "Before grading a repeat source, call `get_source_history(source_id)` and read the prior grade trend"), renumber the rest.

### MF2 — Numeric credibility grade is finalized *before* corroboration and deception checks, with no revisit
`SKILL.md:32-51` (Steps 2, 5, 6). Step 2 emits the final A–F / 1–6 grade; Steps 5 (corroboration) and 6 (plantability) run *after* and never instruct revising Step 2's output. Under FM 2-22.3's Admiralty scale, independent corroboration is a *primary input* to the credibility rating and a plantability finding should discount it — so the agent commits to the grade before it has the information needed to set it.
**Fix:** reorder to classify → corroborate → check deception → *then* grade A–F / 1–6 (weighted by diagnosticity); OR, keeping current order, append to Step 6: "Revise the Step 2 grade now if corroboration or plantability changes it — do not treat the Step 2 grade as final until this step completes."

### MF3 — Delegation/tool error: `get_source_history` is billed under the wrong MCP store
`SKILL.md:66-73`. The Persistence section frames `get_source_history` as an `evidence-ledger` function, but the pipeline of record (`PIPELINE-grounded.md:22` Step-3 row: ⟲ store-read = **source-trust-registry**, ⟳ store-write = **evidence-ledger**; `:47-49` per-case evidence-ledger vs cross-case source-trust-registry) makes it a **cross-case source-trust-registry read**. Conflating two stores under one heading is a right-tool-for-the-job error — an agent may call the wrong server or assume one MCP does both.
**Fix:** split into two labeled subsections — `evidence-ledger` (`add_evidence`, `grade_evidence`) and `source-trust-registry` (`get_source_history`) — and state call order: `get_source_history` first, then `add_evidence`, then `grade_evidence`. (PLAUSIBLE pending confirmation that the two stores are in fact separate servers in the shipped MCP; grounded in the pipeline doc.)

### MF4 — "Grounding" section is dead-weight duplication of inline citations
`SKILL.md:75-82`. Restates, near-verbatim, every provenance tag already attached to Procedure steps 1–7 (`:29-53`: Heuer ACH Step 2, FM 2-22.3 C428, method P009/P010/P013/P014, bias P001/P022/P073, Masterman C044/C002). Zero new execution content — pure audit/traceability material loaded on every invocation, against progressive-disclosure discipline.
**Fix:** move to `skills/source-evaluation/references/grounding.md`; replace `:75-82` with a one-line pointer.

### MF5 — Absence-of-evidence action is split across Step 1c and Step 7 with ambiguous relationship
`SKILL.md:29-31` (Step 1c) vs `:52-53` (Step 7). Both cite Heuer ACH Step 2 and describe recording the "dog that did not bark," with no signal whether Step 7 *finalizes* a provisional Step-1 note or simply repeats it. An agent can't tell if this is one action done twice or two distinct actions.
**Fix:** either merge, or differentiate explicitly — e.g. Step 1c "note *candidate* absences while classifying" → Step 7 "after grading/corroboration/deception, *finalize* the per-hypothesis absence note and write it into the matrix."

---

## SUGGESTIONS

- **S1 — Step 3 is a cross-cutting constraint, not a sequential step** (`:36-38`). "Grade consistently regardless of fit" governs *how* Steps 1–2 are done throughout; numbering it as peer Step 3 risks an agent applying it only after Step 2. Reframe as a standing guardrail callout.
- **S2 — Corroboration-seeking is passive** (`:44-46`). Step 5 evaluates whatever is already in Inputs; it never says to actively pull more corroboration. Add: "If fewer than N independent sources exist, invoke the sibling `osint-investigation` skill (or query `evidence-ledger` for related items on this target) before finalizing corroboration status."
- **S3 — Collection-vs-grading boundary unstated** (`:22-25`). "When not to use" distinguishes only the reviewer subagents, not `osint-investigation` (co-owner of pipeline Step 3, `PIPELINE-grounded.md:22`). Add: "Collecting the OSINT material itself is `osint-investigation`'s job; this skill only grades evidence once gathered." (Pairs with S2.)
- **S4 — Item-level deception flag should be marked provisional** (`:47-51`, `:63`). It partially duplicates the case-level D&D review the pipeline assigns to the deferred Step-8 deception-reviewer (`PIPELINE-grounded.md:27`). Reword Output to "a deception flag if warranted (provisional — confirmed by the Step-8 deception-reviewer once available)" so it isn't read as a closed verdict.
- **S5 — Evidence-type taxonomy is unnamed** (`:29-31`, `:61-64`). Step 1 says "classify the evidence type" and Output treats it as a fixed field, but no value-set is enumerated → inconsistent labels across items. Name the values, e.g. concrete reporting / own assumption-deduction / hypothesis-conditioned expectation / noted absence.
- **S6 — Frontmatter description over-enumerates** (`:3`). Restates nearly the whole Procedure, ~1:1 with Purpose (`:8-14`), and is always loaded. Trim to the trigger clause + keyword phrases; let Purpose (loaded on trigger) carry the full enumeration.

---

## Verdict

The method is substantively well-grounded and the two-axis / diagnosticity / absence-of-evidence core is sound. Blockers are structural: one load-bearing gate (source history) is non-executable narration (MF1) and mis-delegated to the wrong store (MF3); the grade is committed before its own inputs are gathered (MF2); and two housekeeping defects (MF4 dead weight, MF5 duplicate action) hurt clarity. No over-reach of authority found — the skill correctly keeps the grade as the analyst's judgment and defers source vetting to HUMINT and critique to the reviewer subagents.

MUST_FIX_COUNT: 5
