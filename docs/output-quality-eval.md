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
- **Cross-family judge check (B3, Claude + Codex/gpt-5.5, 6 swapped passes):** the verdict is
  **judge-family-dependent.** Claude split 3–3 (its own tie); **Codex went 6–0 for 2-source**;
  cross-family agreement **3/6 = chance** (self-audit: unstable). Twist — Claude *built* both
  subagents yet is the skeptic, while the *independent* Codex prefers the richer/2× longer 2-source
  (likely a length/detail bias, matching the cost-parity flag). Pooled leans 2-source (0.75) but CIs
  still overlap → no robust separation. The research's "judges of different families disagree" is now
  demonstrated on our own data — a single-family verdict can't be trusted alone.
- **Net:** multi-source synthesis's only **robust, judge-independent** win is **grounding/
  faithfulness** (2-source: 4 vs 8 cross-source borrows). Advice quality is **unresolved and
  judge-dependent** (Claude: tie; Codex: 2-source, possibly on length). "Add a source" is justified
  for grounding + coverage, not for a proven advice-quality gain. It took four rounds (qualitative →
  n=6 → n=20 → cross-family) for the harness to surface this — exactly its purpose.

## Finding (2026-06): the invariant layer changes behaviour; the coarse `must_not_do` grader inverts

A/B of the **A3/A5 operating-invariant adapter layer** (with vs without the
`## Operating invariants` section) on `software-design-simplicity-advisor` (22 invariants, 8
behaviour-tests), scored by the deterministic `behaviour_replay` engine:

| component | WITH | WITHOUT | Δ |
|---|---|---|---|
| overall score | 0.549 | 0.533 | +0.016 (tie) |
| route (engage/decline) | 0.750 | 0.750 | 0 |
| `minimum` (coverage) | 0.425 | 0.355 | **+0.070** |
| `must_not_do` | 0.583 | 0.771 | **−0.188** |

1. **The layer demonstrably changes behaviour.** WITH-invariant outputs cite the rule IDs
   (`[PRC-009]`, `[PRC-016]`…) and *explicitly name and reject* the anti-patterns — e.g. GT-002
   opens "**No. Reject.**" and condemns "'complexity now, fix later' = tactical programming
   [PRC-016], debt rarely repaid." Coverage rises (+0.070).
2. **But the coarse `must_not_do` grader is *invertible*.** That same condemnation lexically overlaps
   the forbidden item "Endorse accruing complexity now to fix later" (overlap 0.67 → flagged a
   violation). So the −0.188 is an **artifact**: the grader scores the *best* (rule-citing,
   anti-pattern-rejecting) answers as *violators*, because a lexical detector cannot tell "does X"
   from "names X to reject it." Verified on a captured output.
3. **Verdict (coarse grader):** ≈behaviour-neutral on the number but positive in substance — and the
   instrument itself is flawed. Needs a semantic grader. *(Resolved below.)*

### Resolution (2026-06-14): semantic grader confirms the invariant layer helps

Built `make_llm_grader` (`behaviour_replay`) — an LLM scores route/coverage/ask/`must_not_do`
semantically, with the explicit instruction that *naming a forbidden behaviour to reject it is not
doing it*. Re-ran the same A/B with **claude running the adapter, codex (gpt-5.5) grading**
(cross-family, no self-grading):

| component | WITH | WITHOUT | Δ (semantic) | Δ (coarse, before) |
|---|---|---|---|---|
| overall score | 0.858 | 0.774 | **+0.084** | +0.016 (tie) |
| `must_not_do` | 0.875 | 0.750 | **+0.125** | **−0.188 (inverted)** |
| `minimum` | 0.850 | 0.725 | +0.125 | +0.070 |
| `ask` | 0.500 | 0.000 | +0.500 (n=1, MC-001) | 0 |
| route | 0.875 | 0.875 | 0 | 0 |

The `must_not_do` artifact **reverses** (−0.188 → +0.125): once the grader can tell "rejects X" from
"does X," the invariant layer is **measurably positive on this package** (overall +0.084; MC-001
adherence WITH 1.0 vs WITHOUT 0.0). The build→measure loop closed end-to-end: built the layer → coarse
grader couldn't see it (and inverted) → built the semantic grader → layer validated. Takeaway: **the
semantic grader (`grader=make_llm_grader(llm)`) is the instrument for adherence/advice deltas; the
coarse `must_not_do` is for relative regressions only.**

### Broadened (2026-06-14, n=3 packages, 2 graders): the benefit is package-dependent

Re-ran the WITH/WITHOUT A/B on two more packages, capturing each output once and grading with **both
codex and claude** (a second grader to test robustness):

| package | baseline (WITHOUT score) | codex Δscore | claude Δscore |
|---|---|---|---|
| software-design-simplicity | 0.774 (mid) | +0.084 | — |
| domain-driven-design | 0.880 (strong) | −0.066 | −0.231 |
| mysql-at-scale-operations | 0.366 (weak) | +0.537 | +0.642 |

- **Grader-robust:** codex and claude **agree on the sign** of the delta for both packages (DDD both
  negative, mysql both large-positive). Magnitudes differ (claude is more extreme) but the *direction*
  is not a single-grader artifact — the method holds.
- **Package-dependent benefit, ≈ inverse of baseline strength (n=3 hypothesis):** the invariant layer
  gives a *huge* lift to the weak adapter (mysql 0.366 → ~0.9), a mild lift mid-range
  (software-design +0.084), and a *slight regression* to the already-strong DDD (0.880, near ceiling).
  So the single-package "proven win" is **withdrawn**: the layer **helps some packages, especially
  weak-baseline ones, and can mildly hurt an already-strong adapter** — apply it where a package's
  behaviour-test baseline is weak, not blanket. (Same pattern of the harness tempering an
  over-confident first read as the multi-source arc.)

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

## Finding (2026-06-20): incremental update ≫ full re-author for "strengthening" (deterministic)

A/B of two ways to add a source to an existing package, measured by **grounding-richness**
(claims / principles / grounded bigrams — deterministic, run-independent, `cli grounding-richness`):

| package | v0.2.0 | full re-author | incremental (add-source) |
|---|---|---|---|
| software-architecture | 24 cl / 12 p / 697 bi | 29 / 12 / 631 (Claude) | **42 / 20 / 1295** |
| devops-sre-advisor | 72 / 14 / 1346 | 50 / 14 / 1062 (Copilot) | **101 / 18 / 2072** |

- **Incremental wins on every metric, both packages.** It preserves existing claims/principles and
  appends the new source's → grounding strictly grows.
- **Full re-author does NOT reliably strengthen** — it regenerates everything (non-deterministic),
  so adding sources can leave grounding flat or *worse* (arch claims 24→29 but bigrams 697→**631**,
  principles unchanged; devops 72→50 under Copilot's 2a cap).
- **The inferiority is the METHOD, not just the engine.** Even **full-Claude** re-author (arch, no
  cap) lost to incremental (29 vs 42 claims; 631 vs 1295 bigrams). Re-author regenerates; incremental
  preserves+adds.
- **Reliable gate = `cli grounding-richness` (deterministic), not review-coverage.** Review coverage
  is stochastic (LLM review × doc) — it flagged the devops drop but can't be trusted alone; richness
  showed the real signal cleanly.
- **Recipe:** strengthen via `subagent-maintenance` "add a new source" (`campaign/add-source.sh`) on
  Claude — never a full re-author. Gate on grounding-richness growing. (See the auto-memory
  `incremental-add-source-recipe` for the claim-append flow + validator gotchas.)

## Finding (2026-06-20): per-run extraction dilution — smaller source-sets extract deeper

Side-observation from the incremental A/B: **claims extracted per book rises as the number of
sources in one author run falls** — and it holds **on Claude (no Copilot cap)**, so it is not only
an engine artifact:

| run | engine | books | claims | claims/book |
|---|---|---:|---:|---:|
| arch v0.2.0 (batch) | Claude | 7 | 24 | 3.4 |
| arch incremental add | Claude | 2 | +18 | **9.0** |
| devops batch re-author | Copilot | 7 | 50 | 7.1 |
| devops incremental add | Claude | 2 | +29 | **14.5** |

**Mechanism (hypothesis):** a single author pass has finite per-run extraction attention/budget;
over many sources it extracts shallower per book, over few it goes deeper. Copilot's ~27-request 2a
cap is an extreme case, but the dilution shows on Claude too (arch 3.4 vs 9.0 claims/book).

**Implication:** for **grounding coverage**, feed books in **small increments**, not one mega-batch.
Limits: it maximises grounding *richness*, **not proven advice quality**; past a point more claims
risk a **bloated/unfocused** package; pure one-at-a-time costs N× runs and may cross-link principles
less globally than a batch.

**Practical rule:** *create* with a focused core (≤~5 books/run so the engine extracts fully; Claude
tolerates more than Copilot), then *grow* by adding 1–3 books incrementally (`add-source.sh`), gated
on `grounding-richness`; stop when richness plateaus. Not one mega-batch; not strictly one-by-one.

**Caveat:** N=2 packages, 1 run/method — deterministic but small. A clean controlled test (same N
books as 1 batch vs N incremental adds, richness compared) would confirm.
