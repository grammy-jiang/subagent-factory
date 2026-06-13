# Output-quality evaluation of generated subagents

Structural validation (`cli validate`) proves a package is internally consistent, anchored,
grounded, and faithful — it proves the *pipe is clean*. It does **not** prove the *water is good*:
whether a generated expert, when actually used on a real task, gives expert, correct, non-obvious
advice. This doc is the method for measuring that, plus the first finding it produced.

## Method

1. **Pick a built subagent** (clean, validated). Read its adapter to know its modes + lens.
2. **Choose a suitable real input** the subagent's expertise actually covers (don't force a
   mismatch — a security reviewer on a UX doc tells you nothing).
3. **Run it, read-only, output outside the target tree:**
   ```bash
   RUN_TIMEOUT=1200 MODEL=claude-opus-4-8 bash examples/review-with-subagents.sh \
     <doc> --reviewers <slug> --out /tmp/<slug>-review.md
   ```
   The reviewer's tools are read-only (Read/Grep/Glob); output goes to `/tmp`, never the input.
4. **Judge the review against a rubric** (1–5 each): in-domain fidelity (its lens, not generic),
   groundedness (no hallucination — every finding traceable to the doc), concreteness
   (issue→why→recommendation, anchored), coverage (caught the obvious issues), scope discipline
   (declined out-of-lane parts), actionability (prioritized, present-time).
5. **Grounding check (the non-obvious axis) — automated:**
   ```bash
   python -m tools.subagent_factory.cli grounding-check <slug> <review.md> <reviewed-doc.md>
   ```
   It excludes vocabulary quoted from the reviewed doc, then scores the reviewer's own concept
   bigrams against the subagent's grounded vocab (`principles.yaml` + `claims.jsonl`). Crucially it
   flags **cross-source borrows** — concept terms grounded in *another* subagent's source — and
   names the source(s) to add. That operationalises the recipe below: the borrow names its own fix.
6. **Deterministic content complement:** `tools/subagent_factory/claim_recall.py` scores how many of
   one claim set another recalls (token-F1, no ML) — for comparing extraction arms on content.

## Finding (2026-06): quality is high; grounding fidelity scales with source vocabulary

Across 5 reviews (3 subagents on a real multi-doc system design):

1. **Output is consistently excellent.** Expert-grade, doc-anchored, ~zero hallucinations across
   ~28 findings, strong scope discipline (each declined out-of-lane parts and handed off). The
   factory makes genuinely useful experts — confirmed by use, not just by structural checks.
2. **Grounding fidelity varies, and tracks how distinctive/named the source's vocabulary is.**
   - DDD reviewer (rich named pattern language: bounded context, aggregate, anticorruption layer)
     → tightest grounding; even caught a term collision instead of conflating.
   - api-security reviewer (one sharp principle — *identity-first: authn before authz*) → strong;
     it *pruned* inapplicable source specifics (OAuth/OIDC) rather than force-fit.
   - software-simplicity reviewer (abstract laws, thin distinctive vocab) → loosest: the base model
     filled expression with general / *A Philosophy of Software Design* vocab (deep module, change
     amplification, information hiding) **not in its source** (0 hits in its principles).
   - So the "leak" is a property of the **source**, not a pipeline defect. It is **stable in
     direction** (the same out-of-source term recurs across docs/runs), variable in magnitude.

## Recipe: eval-driven multi-source grounding

The leak **names its own fix** — the borrowed vocabulary identifies the missing source.

1. Output-eval surfaces the grounding leak (step 5 above).
2. Identify the source the borrowed vocab comes from.
3. Re-author as a **multi-source** subagent including that source:
   ```bash
   /author-subagent <source-A> <source-B> --slug <new-slug> --topic "..."
   ```
   (Keep the single-source version as the A/B baseline.)
4. Re-run the same eval; confirm the formerly-leaked terms now resolve to the new principles, and
   that quality held or improved.

**A/B (software-simplicity → software-design-simplicity), two halves — state them separately.**
Adding *A Philosophy of Software Design* to the *Code Simplicity* subagent:
- **Grounding (measured, deterministic, solid):** the 6 leaked terms went from 0 → grounded in its
  principles (`grounding_check`, judge-independent); findings 8 → 10; tier 1 → 2. Also exercised the
  multi-source authoring path (claims split across both books, validates).
- **Advice quality (rigorously judged — STATISTICALLY EQUAL):** under `eval_report` (`judge_ab`
  **20** position-swapped passes + `rank_versions`), the two versions split **10–10** with identical
  Bradley-Terry strength 0.5, CI [0.3, 0.7] each (`separated: false`). The n=6 4–2 lean was noise;
  at n=20 advice quality is **indistinguishable** — and the 2-source review is **2× longer** (221 vs
  105 lines, parity flag 110%) yet no better, so the extra length/findings did **not** translate to
  measurably better advice under a blind, length-neutral judge. The original qualitative "more
  capable" read is **withdrawn**.
- **Net:** multi-source synthesis's measured value is **grounding/faithfulness** (2-source: 4 vs 8
  cross-source borrows — deterministic, judge-independent), **not** better advice. "Add a source"
  is justified for grounding + coverage, not for advice quality per se. This counter-intuitive,
  measured result is exactly what the harness exists to produce — and it took *three* rounds
  (qualitative → n=6 → n=20) to land on the truth.

## Caveats

Small N (a few docs, mostly one run each). Magnitude of any leak is doc- and run-dependent; confirm
stability with 2–3 runs across different docs before investing in a re-author. Rubric scoring of
"good advice" is judgement-based (human or LLM-judge) — it is not a deterministic gate, unlike the
structural validators.

**Known method flaws (from the agent-benchmarking research — see
`enhancement-steps/agent-benchmarking-findings.md`).** The *grounding* half of the eval is sound
(deterministic). The *advice-quality* half as run so far is biased and should be hardened before its
verdicts are stated as measured: (1) it was self-judged by a base model of the candidates →
self-preference bias — use a 3-judge ensemble of non-candidate models; (2) the 1-source-vs-2-source
A/B did not control cost/compute parity or include a strong simple baseline → the richer variant can
win merely for spending more; (3) no independent gold set → circular evaluation inflates scores;
(4) no uncertainty on the verdict → accept a ranking only when conformal/bootstrap intervals don't
overlap. The grounding-leak → multi-source-grounding finding is unaffected (it rests on the
deterministic `grounding_check`, not on the judge).
