# Review — research-writing-advisor (round 1)

Package: `subagents/research-writing-advisor/`
Reviewers: deterministic gates + 4 LLM lenses (agent-skills, profile, faithfulness, ai-agent-engineering).
Findings deduped across lenses; most-severe first.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL) — WARNs are injection-scan only |
| `quote_scan` | **PASS** — no verbatim quotation |
| ellipsis `…` truncation grep | clean |
| adapter invariant severed-paren grep | clean |

Injection-scan WARNs (`english-writing-rese-*`, `science-research-wri-*` "You are now ready to begin…") are **benign** — writing-textbook instructional prose in a frozen distillation-only source; recorded in project memory. Not a finding.

No deterministic FAIL → 0 deterministic must-fix.

---

## MUST-FIX

### M1 — Procedure/anti-pattern lines truncated mid-clause, dropping operative content
- **Where:** ≥5 SKILL.md bodies. Confirmed:
  - `skills/research-argument-and-contribution/SKILL.md:79` — "…label application as tentative rather (P130)."
  - `skills/paper-sections-and-organization/SKILL.md:84` — "…while using (P050)."
  - `skills/paper-sections-and-organization/SKILL.md:91` — "…delaying your true central characters when (P094)."
  - `skills/revision-editing-and-peer-review/SKILL.md:58` — "…formatting, and paired (P054)."
  - `skills/narrative-structure-and-paragraphs/SKILL.md:51` — "Choose between point-first (P002)." (names only one side of a binary → incoherent instruction).
  - Same class of over-summarization drops operative content in `presenting-and-public-speaking` (P089 "four essentials" never named, P170 drops every concrete format option), `slide-and-visual-design` (P056 drops equipment-testing), `note-taking-and-thinking` (steps 4/7/8/9).
- **Severity:** must-fix. Same defect class the truncation gate targets ("silently-truncated skill body"), but severed mid-clause without an ellipsis so the `…` grep missed it. The full principle text renders correctly in the adapter, proving the loss is in the skill summarizer. A step that ends "…while using (P050)" gives the agent nothing to act on.
- **Fix:** Regenerate Procedure/anti-pattern lines from the full principle statement (same text the adapter renders). Add a generator lint flagging any procedure/anti-pattern line ending in a preposition/conjunction ("rather/when/and/using") immediately before its `(Pxxx)` citation.

---

## SHOULD-FIX

### S1 — All 13 skills lack `description:` frontmatter (routing signal)
- **Where:** every `skills/*/SKILL.md` frontmatter (only `name/kind/status/provenance`).
- **Note:** NOT universal factory convention — sibling `descriptive-translation-reviewer` has `description:` on all 12 skills (siblings `research-career` / `research-integrity` also omit it). Genuine gap, shared with two same-batch siblings; downgraded from the agent-skills lens's must-fix because the skill body carries "When to use" and these are internal partition skills, not orchestrator-exposed Agent Skills.
- **Fix:** Add `description:` per skill (≤1024 chars) synthesized from the body's Purpose + "When to use".

### S2 — Adapter frontmatter `description` truncated/malformed
- **Where:** `.claude/agents/generated/research-writing-advisor.md:3`.
- **Problem:** Composed from only the first `when_to_use` + first `when_not_to_use` bullet, both cut mid-clause, ending on a dangling unpunctuated list. Drops the "…this advisor guides the work, it does not perform it" disambiguator and omits 3 of 5 use-case classes (presentation, non-native English, note-taking) → router under-invokes.
- **Fix:** Regenerate the adapter `description` from a complete composite of role + full `when_to_use` set, ending on a complete clause. Generator/template concern (`templates/claude-agent-adapter.md.j2`), not hand-edit.

### S3 — Anti-patterns hard-capped at 7 → largest skills worst-covered
- **Where:** every skill's "Anti-patterns to flag". Coverage: `paper-sections-and-organization` 7/29 (24%), `clarity-and-sentence-style` 7/21, `research-argument-and-contribution` 7/19, `evidence-integrity-and-claims` 7/19; skills with ≤7 principles get full coverage.
- **Fix:** Remove the fixed cap; emit one anti-pattern per principle in `provenance.principles`, matching the 1:1 procedure-step pattern.

### S4 — Anti-pattern entries mirror their procedure step, no diagnostic value
- **Where:** e.g. `skills/paper-sections-and-organization/SKILL.md:115-121` — "Overlooking PXXX: `<same clause>`".
- **Fix:** Rewrite each as an observable failure signature in a draft (e.g. "Introduction opens with 'little is known about X' and never narrows to a question"), distinct from the paired procedure step.

### S5 — Profile body near the word-budget FAIL ceiling
- **Where:** `profile.yaml`. Manual sum of gated fields ≈960w (WARN >800, hard FAIL >1000). Heaviest: `quality_bar` (~154w), `role` (~144w), `when_to_use` (~121w), `forbidden_behaviours` (~104w).
- **Fix:** Run `python -m tools.subagent_factory.profile_self_check subagents/research-writing-advisor` for the authoritative count; if >800, split/shorten compound `quality_bar` bullets and tighten `role` sentence 3.

### S6 — `forbidden_behaviours` has no fabricated-citation / plagiarism mirror
- **Where:** `profile.yaml:76-84`. The literature-integrity `quality_bar` bullet (P007/P026/P138/P016/P168) has no negative mirror barring the advisor from producing/endorsing a fabricated citation or copied passage presented as the caller's own.
- **Fix:** Add a `forbidden_behaviours` bullet grounded in the same IDs.

### S7 — Provenance ledger doesn't record the Phase-8 self-check verdict
- **Where:** `provenance-ledger.md`. `profile.yaml:5` asserts `status: ready` but nothing records the self-check PASS/date/test counts that earned it.
- **Fix:** Append self-check verdict + date + golden/negative-routing test counts to Version History.

### S8 — Faithfulness over-claim: P080 stretched into a governance/override authority
- **Where:** `profile.yaml source_of_truth_policy.precedence` — "…author's ownership of the science and the final wording overrides every stylistic invariant (P080)".
- **Problem:** SCOPE_BROADENED. P080 = "author must submit correct English / owns language, not the science." Nothing supports "final wording overrides every stylistic invariant" — as written an author could invoke it to justify overstating a claim, defeating the evidence-integrity invariant.
- **Fix:** Narrow to language/wording-correctness + science substance; explicitly carve out that it does NOT override the no-over-claim invariant.

### S9 — Faithfulness over-claim / mis-cite: `forbidden_behaviours[3]` cites P150
- **Where:** `profile.yaml:76-84` — "Ruling on domain-science correctness… (P150, P140)".
- **Problem:** P150 = methodology-fitness ("treat every method as good when done well"), says nothing about domain-science authority; only P140 (legal/plagiarism) partly fits. "Domain-science correctness belongs to the researcher" is ungrounded in the cited IDs.
- **Fix:** Drop/replace P150; or record in the ledger that the domain-science-authority boundary is a factory-standard advice-only design decision, not principle-derived.

### S10 — Faithfulness over-claim: `handoff_rules[0]` cites P022 for claim-authority
- **Where:** `profile.yaml handoff_rules[0]` — "…the decision of what to claim… (P080, P022)".
- **Problem:** P022 is structural ("organize the paper around its developed claim"), not about who decides what to claim → SCOPE_BROADENED.
- **Fix:** Re-ground "decision of what to claim" in a claim-authority principle, or mark as a design decision.

### S11 — Faithfulness hedge-drop: `always_on` P135
- **Where:** `profile.yaml knowledge_partition.always_on` (~lines 156-161) — "…an editorial decision is read and acted on promptly (…P135…)".
- **Problem:** HEDGING_REMOVED. P135 = "revise and resubmit promptly **unless the required changes are genuinely impossible or unacceptable**", and "identify whether a revision path is open" — both dropped → unconditional "act promptly" could advise complying with unreasonable demands.
- **Fix:** Restore the condition + exception clause.

---

## NICE

- **N1** `profile.yaml quality_bar` (~L68-69) attributes P159 to narrative-structure openings, but P159 is owned by `paper-sections-and-organization` provenance, not narrative-structure. Correct the citation or mark as cross-skill. (agent-skills #6)
- **N2** Fuzzy boundary between `research-argument-and-contribution` (P065) and `paper-sections-and-organization` (P159/P003) on "problem → question"; add a one-line cross-reference in each skill's "When to use". (agent-skills #5)
- **N3** Identical byte-for-byte "Output" boilerplate across all 13 skills; optionally hint each skill's own deliverable shape. (agent-skills #7)
- **N4** `role` verb list "plan, draft, revise, and present" — "draft" momentarily reads as authoring; disclaimer sentence + forbidden_behaviours resolve it. Optional: "plan, shape, revise, and prepare to present". (ai-agent #2)
- **N5** Broad multi-domain identity (writing + slides + speaking + note-taking) under one advisor; not authority creep now, but re-verify forbidden_behaviours covers every sub-domain if extended. (ai-agent #3, profile #4)
- **N6** `forbidden_behaviours[0]` (no ghostwriting) cites P080/P024 loosely — sound advice-only boundary but under-grounded; note as factory-standard design decision. Under-claims (safe direction). (faithfulness #5)
- **N7** `inputs.required` is one dense catch-all bullet; split for skimmability on a future revision. (profile #5)

---

Tool boundary confirmed correct: adapter `tools: Read, Grep, Glob`; `mcp: []`, `caller_supplied: []` — no write/exec/MCP grant despite an available `research-pipeline` server. Advisor/no-deliverable boundary, source-of-truth policy, and escalation owners all coherent.

MUST_FIX_COUNT: 1
