# Review Loop — research-writing-advisor r2

One review pass. REVIEW ONLY. Package version 1.3.0.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** (0 FAIL) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation (`…` ellipsis) | clean — 0 hits in skills + adapter |
| truncation (severed parenthetical) | clean — 0 hits |

Injection-scan emitted WARNs (`role-override/body/medium` on `science-research-wri-*.md` "You are now ready to begin building a model...", plus reversed/detagged normalization hits). Benign textbook prose in an untrusted source — per `.claude/rules/untrusted-source-policy.md` a lexical hit **quarantines/triages, not blocks**; validation still PASSED. **Not a must-fix.**

## LLM reviewer panel (4 lenses, all returned MUST_FIX_COUNT: 0)

Consolidated, deduped, most-severe first. No must-fix survived any lens.

### should-fix

1. **Ungrounded "domain-science correctness" boundary — mis-cited to P140**
   *Where:* `profile.yaml` `forbidden_behaviours[3]` (`(P140)`), plus restatements in `handoff_rules[1]`, `source_of_truth_policy.canonical_owner`, `when_not_to_use[1]` (uncited); `reports/faithfulness-report.yaml` note mislabels P140 as covering domain-science.
   *Problem:* P140 covers only legal-rights/plagiarism ("copyright, patents, publication agreements, plagiarism standards"), **not** scientific/methodological correctness. Grep of the 4,964-line principles file for "domain-science"/"scientifically correct" = 0 hits; none of the 9 sources is a domain-methodology text. The "domain-science correctness rests with the researcher" boundary is sound **agent-design policy** but has no principle support, yet is presented with the same principle-cited framing as the properly-grounded legal-rights half. *(faithfulness-reviewer; overlaps profile-reviewer note on bundled grounding in `forbidden_behaviours[3]`.)*
   *Fix:* Drop the domain-science clause from the principle-citation apparatus and state it plainly as advice-only design policy (like the existing `(an advice-only boundary)` tag); split `forbidden_behaviours[3]` into a policy-tagged bullet + a `(P140)` legal/ethics bullet; correct the faithfulness-report note.

2. **Acceptance-authority boundary over-cited to P083/P135**
   *Where:* `profile.yaml` `forbidden_behaviours[1]` (`(P083, P135)`), restated in `when_not_to_use[2]` and `examples[1]`.
   *Problem:* P083 is guidance for *writing a peer review*; P135 is the *author's* response to a decision. Neither allocates acceptance authority to editors/reviewers, and "declaring a draft 'publishable'" has no anchor (grep for "editors and reviewers"/"acceptance rests" = 0 hits). Restraint is correct but citation implies stronger grounding than exists. *(faithfulness-reviewer.)*
   *Fix:* Recite as advisor-scope design policy, or soften citation framing so P083/P135 aren't claimed to establish acceptance-authority allocation.

3. **Per-skill Output section written for `review` mode only**
   *Where:* all 13 `skills/*/SKILL.md` `## Output` sections.
   *Problem:* `profile.yaml:47-60` declares 3 modes (`advise`/`review`/`plan`) with distinct output shapes; every skill body hard-codes the `review` findings-list shape, so a skill invoked under `advise`/`plan` carries an output contract mismatched to the mode. *(agent-skills-advisor.)*
   *Fix:* Make each `## Output` mode-neutral or branch on mode (single recommendation / findings list / ordered plan).

4. **DRY boilerplate repeated across all 13 skills**
   *Where:* all 13 `skills/*/SKILL.md` `## Output` disclaimer (~70w) + `## Provenance` bibliography (~90w).
   *Problem:* Near-verbatim disclaimer + full 9-source bibliography restated in every file; already stated once at profile level (`forbidden_behaviours`, `sources:`). Inflates every triggered body. NOTE: ledger records this (S4) as a re-deferred design decision across 1.2.0→1.3.0. *(agent-skills-advisor; ledger S4.)*
   *Fix:* Shrink Provenance to `Derived from <IDs>; bibliography in profile.yaml`; collapse disclaimer to one clause. Or convert the ledger deferral to a permanent accepted-design note.

5. **Profile body word-count at ~997/1000 — 3 words from FAIL**
   *Where:* `profile.yaml` whole body (Phase-8 check 14).
   *Problem:* Ledger self-reports ~997w; any future one-line addition silently trips the >1000w hard-FAIL. *(profile-reviewer.)*
   *Fix:* Trim 50–100w headroom now (tighten `role` — it restates the 9-source count/domain list already in the ledger; or condense `source_of_truth_policy.precedence`).

6. **`when_to_use[4]` drops the "research" qualifier its siblings carry**
   *Where:* `profile.yaml` `when_to_use[4]` / adapter line 135 ("preparing a talk or slide deck...").
   *Problem:* Only trigger without a "research"/"academic" anchor; reads as generic presentation coaching, inviting off-domain routing (business pitch, non-research talk) into a research-anchored agent. *(ai-agent-engineering-reviewer.)*
   *Fix:* Reword to "preparing a **research** talk or academic/technical slide deck..." in both profile and adapter; optionally add a `when_not_to_use` line excluding general public-speaking/slide coaching.

### nice

7. **Voice-choice lens overlap without cross-reference** — `clarity-and-sentence-style` (step 7, P008) and `academic-english-for-non-native-writers` (steps 7-8, P137/P169) both cover active/passive voice with no disambiguating cross-reference (the corpus already uses that pattern for Methods). Add a one-line handoff in each. *(agent-skills-advisor.)*
8. **`evidence-integrity-and-claims` step 16 (P105)** is an experiment-scoping decision, not a writing one — lens-fit outlier vs siblings; reframe to the writing/reporting angle or drop. *(agent-skills-advisor.)*
9. **Adapter forbidden/quality-bar cite principle IDs absent from the visible "Operating invariants" block** — highest-priority guardrail references IDs resolvable only via a `Read` detour; prose is self-explanatory so behavioral impact is nil. Fold IDs in or add a one-line resolution pointer. *(ai-agent-engineering-reviewer.)*
10. **Three skill descriptions (~900-1000+ chars)** near the 1024 hard cap — trim for margin. *(agent-skills-advisor.)*
11. **`outputs.modes` carry no inline principle IDs** — the one rule-bearing field group without citation (matches `research-career-advisor` convention). Accept explicitly or cite. *(profile-reviewer.)*
12. **No per-skill worked example** — only 2 profile-level examples; add compact before/after to high-traffic skills (clarity, figures, slides). *(agent-skills-advisor.)*
13. **Ledger accumulating re-deferred items (M2, S4)** across two rounds — convert to permanent accepted-design notes or scheduled follow-ups. *(profile-reviewer.)*

## Verdict

Package validates clean, quote-scan clean, no truncation, tool boundary correct (Read/Grep/Glob only), adapter/profile fidelity verbatim-consistent, no authority creep. All 4 LLM lenses returned zero must-fix. Findings 1–6 are should-fix (grounding-citation accuracy + mode/DRY/word-count/scope hygiene) — worth a fix round but non-blocking. Findings 1 and 2 are highest-value: two restraint boundaries carry principle citations that don't actually ground them (fix = re-label as design policy, not weaken the restraint).

MUST_FIX_COUNT: 0
