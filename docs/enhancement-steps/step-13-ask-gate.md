# Step 13 — Ask-Gate (calibrated Answer / Ask / Abstain)

> Folds `docs/Research/calibration-abstention/` (31 papers, validated PASS 1.0) into an executable
> spec. This is the **F-track** of `research-integration-plan.md`. It gives a generated advisor a
> principled gate for *when to answer vs ask for missing context vs abstain*, instead of confidently
> committing on underspecified input — the behaviour Step-11 `missing_context_tests` already probe and
> `behaviour_replay`'s `must_ask_for` already scores.

**Goal** — A two-stage **Answer / Ask / Abstain** gate: a cheap **deterministic** calibrated pre-filter
on every request, escalating only flagged-uncertain cases to an LLM three-action planner — so the
advisor asks *one specific* question when a decision-relevant input is missing, abstains when it
genuinely cannot help, and otherwise answers.

## Why (the measured failure this fixes)

Default LLMs **almost never ask or abstain and are overconfident**, and retrieved context *suppresses*
asking further (calibration findings #3). So the property must be **imposed by an explicit gate**, not
hoped for. The gate's core can be deterministic: selective prediction = a **threshold on a calibrated
scalar risk score** (act iff risk ≤ τ, τ tuned on held-out data) — not entropy/log-prob or verbalized
confidence alone, which have a confidently-wrong failure mode (#1, #2).

## Relationship to existing steps (this is mostly refinement, not a new pipeline)

| Existing | Step-13 adds |
|---|---|
| Step-11 `missing_context_tests` (slot-ablation) | **answerable-twin pairing** — pair each missing-context test with an *answerable* variant; grade on two axes (silent-commit vs over-ask). Closes the open E follow-on; the *method* is calibration finding #5. |
| `behaviour_replay` `must_ask_for` grading | **information-gain / one-specific-question** scoring — reward naming the missing variable, **penalize over-asking** (over-asking hurts, nonmonotonic — #5). |
| Step-12 optimize objective | the ask-gate behaviour becomes a first-class optimization target (it already is, via missing-context tests). |
| adapter behaviour | a **three-action** Answer/Ask/Abstain rule with **uncertainty attribution** (data-uncertain → ask; model-uncertain → abstain/escalate) — #4. |

## Status (2026-06-14)

- **F4 answerable-twin generation — BUILT.** `gen_behaviour_tests` now pairs each `missing-context`
  cell with an **answerable twin** (a golden test whose context IS sufficient, `twin_of` linking it
  back), so the suite catches **over-asking**, not just silent-commit. Schema gained `twin_of`. Proven
  on api-security (14 missing → 14 twins, coverage PASS).
- **F3 two-axis grading — realized via existing graders.** The missing-context test rewards asking
  (`must_ask_for`); the twin rewards answering (`minimum_output`) and forbids over-asking
  (`must_not_do: "Ask for more information when the context is already sufficient"`). No new grader
  needed — the two axes fall out of the existing `behaviour_replay` components.
- **F1 / F2 / F5 (runtime calibrated risk gate + 3-action planner + two-stage escalation) — spec
  only.** Single-turn: blocked on black-box missing-context detection (open ACADEMIC, below).
  **Multi-turn: now BOUNDED** (round 3, 2026-06-23) — a compose-from-validated-parts adapt-path is
  named with only 2 small novel residuals (see Caveats); the build is de-risked, just not yet built.

## New files (proposed)

| Path | Kind | Purpose |
|---|---|---|
| `tools/subagent_factory/ask_gate.py` | tool | Deterministic pre-filter: a calibrated risk score + threshold → {answer, escalate}; plus the answerable-twin grading helpers. |
| `.claude/skills/ask-gate/SKILL.md` | skill (LLM) | The escalated three-action planner: classify Answer/Ask/Abstain + uncertainty source; emit the single highest-info clarification question. |
| extend `gen_behaviour_tests.py` | tool | Emit answerable-twin pairs for missing-context cells (the answerable variant should NOT trigger asking). |
| extend `behaviour_replay.py` | tool | Two-axis `must_ask_for` scoring: silent-commit penalty + over-ask penalty (reward one specific question). |
| `tests/subagent_factory/test_ask_gate.py` | fixtures | Threshold/escalation + answerable-twin + over-ask scoring tests. |

## LLM ↔ deterministic split (the headline recommendation, #9)

**Two-stage gate.** A cheap deterministic calibrated/probe/conformal pre-filter runs on *every*
request; only requests it flags uncertain escalate to the LLM three-action planner (cascaded
Trust-or-Escalate). Pre-generation gating is cheaper and safer than output refusal (#10). Deterministic
owns the threshold + the answerable-twin grading; the LLM owns the Ask/Abstain decision + the
clarification wording (the "Ask" action is the hardest and needs the LLM).

## Research inputs (findings → spec, with paper IDs)

1. **Selective prediction = deterministic threshold on a calibrated risk score** (act iff risk ≤ τ).
   [2603.21172], [2310.11689], [2410.02173], [2508.07556], [2307.09254]
2. **Don't gate on entropy/verbalized confidence alone** (confidently-wrong) — fuse a supervised
   correctness probe. [2603.21172], [2310.11689], [2509.24988], [2604.17274]
3. **LLMs rarely ask/abstain + retrieved context suppresses asking** → impose an explicit gate; tests
   must include ambiguous-prompt-**with-helpful-context** adversarial cases. [2605.25284], [2605.25831],
   [2604.04565], [2604.03904]
4. **Three-action Answer/Ask/Abstain + uncertainty attribution** (data → ask; model → abstain).
   [2604.04565], [2605.25831], [2604.17293]
5. **Clarify by information gain; over-asking hurts (nonmonotonic)** → reward one specific
   missing-variable question, penalize generic/over-asking; pair with an answerable twin.
   [2606.03135], [2603.26233], [2605.25284]
9. **Two-stage gate** — deterministic pre-filter → escalate uncertain to an LLM planner. [2410.02173],
   [2601.10398], [2604.04565], [2407.18370]
10. **Pre-generation gating > output refusal** (decide before generating). [2601.10398], [2604.04565],
    [2603.26233]

## Gate wiring

The answerable-twin tests + two-axis `must_ask_for` scoring slot into the existing Step-11 validator +
`behaviour_replay`; no new package-validity gate. The runtime `ask_gate` is an opt-in adapter behaviour
(a profile-level capability), measured by the missing-context tests it must pass.

## Exit criteria

- `gen_behaviour_tests` emits answerable-twin pairs; the answerable twin scores high *without* asking,
  the ablated one requires asking.
- Two-axis `must_ask_for` scoring penalizes both silent-commit and over-ask (unit-tested with fakes).
- `ask_gate` deterministic threshold + escalation unit-tested.
- `make verify` green; Tier-0 packages untouched.

## Caveats (open gaps from the research)

- **ACADEMIC (open):** purely deterministic missing-context detection for **black-box (API-only)**
  models is unsolved — white-box latent answerability probes don't transfer; the deterministic
  pre-filter for hosted models leans on calibrated scalar scores + correctness probes, not internals.
- **ACADEMIC (bounded — round 3, 2026-06-23):** **multi-turn** ask-gates over long evolving context.
  A 17-paper round confirmed **no validated end-to-end multi-turn advisory ask-gate exists**, but all
  four required functions (required-slot tracking, anti-re-ask, per-turn calibration, sufficiency
  detection) are individually validated → **compose from validated parts**, don't invent. Two residual
  novelties: (1) calibration that *updates as context grows* (conformal CICC is single-shot/frozen
  [2403.18973]); (2) a *schema-free* required-context ontology (validated slot trackers assume a typed
  schema). Eval the gate with ASK-F1 + InfoECE/Kendall-τ monotonicity + the VivaBench failure taxonomy.
  Choose *what* to ask by information-gain / EVPI. See `docs/Research/calibration-abstention/` (48
  papers, round-3 converged). Black-box single-turn detection (above) is the only HIGH-friction residual.
- **ENGINEERING (resolved inline):** deterministic-vs-LLM threshold choice + which calibration metric
  the eval optimizes — the two-stage split + held-out τ tuning are the recipe.
- **Judge tie-in (#6/#7):** the *same* calibration math governs trusting an LLM-judge verdict —
  consensus ≠ human alignment; a single verdict needs a conformal/human-anchored guarantee. This
  strengthens **B4 (human gold)** and tempers the Step-12 `--judge-samples` median (necessary, not
  sufficient). Captured in the D-track + `output-quality-eval` notes, not re-specced here.

## Risks

- *Over-asking regression* — the answerable-twin + over-ask penalty are the guard (don't optimize the
  ask-gate into an always-ask agent).
- *Mis-calibrated τ* — tune on held-out data per package; monitor; conformal where data is exchangeable.
