# Step 12 — Optimize-Adapter (tune the adapter against the behaviour-test objective)

> Folds `docs/Research/prompt-optimization-eval/` (29 papers, validated PASS 1.0, IMPLEMENTATION_READY)
> into an executable spec. This is the **D-track** of `research-integration-plan.md`. It runs *after*
> build (Steps 1–9) and *after* the Step-11 suite exists, and automatically improves the adapter to
> maximize that suite's score — keeping only variants that pass the replay gate.

**Goal** — Given a built package and its Step-11 behaviour-test suite, **automatically propose →
score → keep-winner** edits to the adapter's induced-guidance rules and worked examples, maximizing
the behaviour-test score under a fixed eval budget, **never merging a variant that regresses any test
or breaks faithfulness**.

## Core insight (finding #1)

This is **not a novel mechanism** — it is the standard `propose → score → keep-winner` loop, and the
factory **already owns every primitive**:

| Loop part | Existing primitive |
|---|---|
| objective *f* | the Step-11 behaviour-test suite |
| scorer | `behaviour_replay.replay_suite` (live runner + grader) |
| selection / assess-before-merge | `behaviour_replay.replay_gate` (flip ≥1 fail→pass, **zero** pass→fail) |
| relative ranking + critique | `behaviour_replay.make_llm_grader` |
| example axis | `behaviour_replay.rank_examples_by_utility` |

So Step 12 = **a driver that wires these into a budgeted loop + an LLM variant proposer**. No new
scoring or gating science.

## New files

| Path | Kind | Purpose |
|---|---|---|
| `tools/subagent_factory/optimize_adapter.py` | tool (driver) | The budgeted propose→score→keep loop; pure orchestration over existing primitives + a proposer callable + a pool. |
| `.claude/skills/adapter-optimization/SKILL.md` | skill (LLM) | The variant-proposer meta-prompt: given failing tests + grader critique + scored history + the **faithfulness constraint**, emit candidate rule/example edits. |
| `cli optimize-adapter` (new `@main.command`) | CLI | **(D8, done)** Run the loop for a slug with `--budget`/`--variants`/`--minibatch`/`--pool`/`--patience`/`--runner`/`--proposer`/`--dry-run`. Writes the winner to `<slug>.optimized.md` for review; never overwrites canonical. |
| `examples/optimize-proposer.sh` + `optimize_adapter.shell_proposer` / `make_policy_gate` | live wiring | **(D8, done)** Additive proposer (model emits `===VARIANT===`-delimited guidance blocks via `claude -p`) + a text-level pre-merge gate (no tool-grant widening / escalation tokens). |
| `tests/subagent_factory/test_optimize_adapter.py` | fixtures | Loop unit tests with a **fake** proposer + fake runner (deterministic, no live model) + pure tests for the D8 prompt-build / variant-parse / policy-gate. |

## Reuse

- `replay_suite`, `replay_gate`, `make_llm_grader`, `rank_examples_by_utility`, `shell_runner`
  (all in `behaviour_replay.py`).
- `cli export` to re-render an adapter from a candidate profile; `cli replay-score` / `replay-gate`.
- `compile_invariants` — the **enforced-invariant layer is frozen**; Step 12 only edits the
  *induced-guidance* rules + worked examples, never the must-hold invariants (A3/A5 boundary).
- Faithfulness + quote + adapter-policy scans as the **hard pre-merge gate** (see guardrails).

## The loop (deterministic skeleton, LLM only at "propose")

```
baseline = replay_suite(adapter, tests)            # current score
pool = [baseline_variant]                           # small beam / Pareto pool, not just "current best"
for t in range(T):                                  # budget = T rounds
    failing = tests where pool.best fails
    cand[] = PROPOSE(failing, grader_critique, scored_history, faithfulness_constraint)  # LLM, N variants
    cand[] = cand where det_pre_merge_gate(cand) passes        # faithfulness/quote/policy — HARD
    screen = replay on a MINIBATCH (cheap)                     # finding #5: minibatch-screen
    keep top-k by minibatch score → CONFIRM on full suite      # then full-confirm
    for c in confirmed:
        if replay_gate(pool.best, c) == pass:  pool.add(c)     # assess-before-merge: 0 regressions
    if no improvement for `patience` rounds:  break            # early stop
winner = pool.best;  if winner.score > baseline.score: export winner
```

## LLM ↔ deterministic split

| Deterministic | LLM |
|---|---|
| budget loop, minibatch screen, full confirm | propose N variant rule/example edits |
| `replay_gate` merge decision (0 pass→fail) | emit *why a test failed* critique (grader) |
| faithfulness/quote/policy pre-merge gate (FAIL ⇒ discard) | relative **ranking** of close variants |
| pool/beam management, early stop, budget accounting | — |
| keep-winner + `cli export` | — |

## Research inputs (findings → spec, with paper IDs)

1. **Standard propose→score→keep loop; replay+grader is the scorer, behaviour-test score is *f*,
   keep-winner-behind-replay-gate is selection.** *[2502.16923], [2309.03409], [2211.01910],
   [2406.11695], [2507.19457], [2606.13317]*
2. **Split the objective det-vs-LLM** — deterministic behaviour-tests = **hard merge gate**; LLM
   grader only for **targeted critique** + **relative ranking**, never as raw-magnitude reward.
   *[2606.13317], [2606.13221], [2306.05685], [2401.10020]*
3. **Assess-before-merge on outcome transitions** — merge iff ≥1 fail→pass with **zero** pass→fail;
   gate empirically calibratable (monotone accuracy buckets). *[2606.13317], [2606.13449]* →
   this *is* `replay_gate`.
4. **Rich criterion-referenced feedback >> a bare scalar** — feedback specificity is the cheapest
   quality lever; the grader must emit *why* a test failed to condition the proposer. *[2305.03495],
   [2406.07496], [2507.19457], [2303.17651]*
5. **Cost = eval calls; stack levers** — minibatch-screen→full-confirm, N-variants-per-call,
   cheap-propose/expensive-verify, surrogate/best-of-N prefilter, bandit budget allocation, closed-form
   budget **N×T×(1+|D|)**. *[2405.18369], [2406.11695], [2402.09723], [2309.08532], [2606.13598]*
6. **Diversity-preserving selection beats greedy at equal budget (+6–11%)** — keep a small
   Pareto/beam/bandit pool of per-test winners, don't always edit the current best. *[2507.19457],
   [2305.03495], [2402.09723]*
7. **Joint instruction+demonstration optimization is the blueprint** — MIPRO (LM proposer + TPE
   Bayesian surrogate + minibatch trials then full-suite confirm); DSPy bootstraps demos from passing
   traces; KATE adds near-free demo retrieval. *[2406.11695], [2310.03714], [2101.06804]* → maps to
   editing **rules** *and* **worked examples** (the A4 examples slot) jointly.
8. **Sample-efficiency on two axes** — *allocation* (TRIPLE best-arm beats uniform by 3–16% / 10–56%
   at equal budget) + *information* (Trace's rich trace, GEPA ≤35× fewer rollouts). *[2402.09723],
   [2406.16218], [2507.19457]*
9. **LLM-judge as objective, with guardrails** — ~85% judge–human agreement, but guard
   reward-hacking: judge pairwise **both orders**, count only **consistent** wins, penalize verbosity,
   **never same-family self-judge**, periodically re-validate judge↔behaviour-test agreement.
   *[2306.05685], [2401.10020], [2606.13221]*
10. **Keep variants human-readable; avoid white-box/RL token methods** (RLPrompt/AutoPrompt/
    Prompt-Tuning produce gibberish or need white-box gradients — conflicts with a faithfulness-bound,
    black-box authoring factory). *[2205.12548], [2010.15980], [2104.08691]*

## Guardrails (hard, deterministic — the factory's non-negotiables)

- **Every kept variant must pass `faithfulness-review` + `quote_scan` + `adapter_policy_scan`** before
  the replay gate even runs. Optimization can make an adapter *score* higher by over-claiming; the
  faithfulness gate forbids that (a variant whose rule is stronger than its source support is
  discarded, no matter its behaviour-test score). This is the load-bearing anti-reward-hacking control.
- **Behaviour-tests are the merge gate; the LLM grader never is** (finding #2). The grader's number is
  used only for *ranking close candidates*, with the finding-#9 judge guards.
- **Invariant layer is frozen** — Step 12 edits induced guidance + examples only.
- **Determinism of the objective** — Step 11 golden tests are typed-template/fixed-wording, so *f* is
  stable across rounds.

## Gate wiring

Step 12 is an **opt-in maintenance/release tool**, not a package-validity gate — it *produces* a new
profile version. Its output re-enters the normal pipeline: bump `agent_version`, changelog entry,
`cli validate`, re-export (per `generated-artifact-policy.md`). Optionally record an eval row
(`eval_report.py`, B-track) showing before→after behaviour-test score for the version-history ledger.

## Fixtures

- Fake proposer that returns one strictly-better variant → loop merges it, winner.score > baseline.
- Fake proposer returning a regressing variant → `replay_gate` rejects, baseline retained.
- Faithfulness-failing variant → discarded **before** scoring (guardrail proven).
- Budget exhaustion / no-improvement → early stop fires; closed-form budget accounting asserted.

## Exit criteria

- `python -m tools.subagent_factory.optimize_adapter subagents/<slug> --budget N` (with a fake
  runner/proposer in tests) returns a winner ≥ baseline and never a regressor.
- `cli optimize-adapter <slug>` wired; `--dry-run` prints proposed diffs without exporting.
- A real end-to-end run on one package improves (or holds) its behaviour-test score with **zero**
  faithfulness regressions; recorded as a version-history eval row.
- `make verify` green.

## Caveats

- **Gap 3 (open, ACADEMIC LOW):** in-loop judge drift / self-preference under optimization pressure —
  mitigated by using the grader only for ranking + finding-#9 guards + periodic judge↔test
  re-validation; a dedicated in-loop-drift study was not retrievable (recency-lock).
- **Gap 4 (open, ACADEMIC LOW):** multi-objective (score vs faithfulness vs token cost) — shipped as
  single-objective with faithfulness as a **hard constraint**, not a Pareto term; NSGA-II/Pareto is an
  optional later upgrade.
- **Mechanism at small budgets (ENGINEERING, resolved inline):** default textual-gradient-style
  proposer + minibatch→full-confirm; escalate to evolutionary/Bayesian only if it plateaus.
- Live runs cost real model calls (Claude spend cap, [[arxiv-index-recency-locked]] notes the cap can
  kill batched runs rc=0) — budget loop + early stop are the cost controls; default `--budget` small.

## Risks

- *Reward-hacking the grader* → behaviour-tests (not grader) are the gate + faithfulness hard-gate
  (finding #2, guardrails).
- *Overfitting the suite* → held-out confirm split + the Step-11 suite is adversarial/diverse by
  construction (coverage loop) so "teaching to the test" still requires genuinely better behaviour.
- *Cost blowups* → closed-form budget cap + minibatch screen + early stop (finding #5).
