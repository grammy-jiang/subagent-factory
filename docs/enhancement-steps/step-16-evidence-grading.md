# Step 16 — Evidence Grading (formal confidence layer)

> Folds `docs/Research/systematic-review-evidence-synthesis/` (30 sources, validated PASS 1.0). This
> is the **K-track** of `research-integration-plan.md`, and the §20 #1 topic. Makes the factory's
> ad-hoc `confidence: high|medium|low` a **principled, GRADE-style** assignment with proper judge
> discipline. **Design capture; the method is HIGH-confidence + matches the factory's existing split.**

**Goal** — Replace ad-hoc confidence with a formal evidence-grading layer: a GRADE-style
start-then-up/down-grade confidence function, a numbered-criteria inclusion gate, risk-of-bias as
*advisory weight not gate*, conflict-by-reground-not-average, and judge discipline (pin + provenance +
ensemble; never raw self-confidence) — feeding `evidence-protocol` + Step-1/3 (faithfulness).

## Core split (confirms the factory's discipline)

**Semantic-judgment / deterministic-arithmetic split is the spine:** the LLM answers each *semantic*
call (per-criterion inclusion, RoB signalling); deterministic code owns *all* scoring, roll-up, and
calibration. Convergent across the corpus — and exactly the factory's existing "LLM proposes, code
decides" rule.

## Spec (findings → design; no code yet)

| mechanism | design | finding |
|---|---|---|
| **inclusion gate** | numbered binary criteria → per-criterion `{−1, 0, +1}` with explicit **abstain** → deterministic sum, keeping each rationale (CoT/numeric rubrics add nothing) | F3 |
| **confidence assignment** | **GRADE-style start-then-grade**: baseline by source type; *down*-grade for RoB-domain failures / inconsistency / conflict; *up*-grade for replication; clamp to high/med/low | F5 |
| **"medium"** | a reported **range** (low↔high) with its width surfaced — not a fixed 0.5 multiplier | F6 |
| **risk-of-bias** | **advisory, low-confidence — NOT a gate** (frontier LLMs ~42% Macro-F1; human ceiling κ=0.40); keep RoB qualitative, convert to weight only at aggregation | F4 |
| **conflict** | **return to the source + abstain, don't average** — dual judges; on disagreement re-ground → verification label (agree→high / one-wins→medium / both-wrong→withhold/human); expose contradictions | F7 |
| **source quality** | define as **impact on the distilled conclusion** — recall↔conclusion-fidelity is non-linear (~63% recall still leaves ~76% of conclusions unchanged); weight a missed source by influence | F9 |
| **judge discipline** | **never publish raw single-model self-confidence** (ECE up to 0.79; most-confident often least-reliable) — ensemble cuts ECE to ~0.05–0.27; self-report only to route/escalate; prefer **calibrated abstention** + an explicit "insufficient evidence" grade (optimise error *type*, not rate) | F2, F8 |
| **provenance** | **pin every LLM judge** (fixed prompt/temp, repeat runs, log inter-run agreement — non-deterministic even at temp 0) + require a **verbatim source span per principle**, reject if absent | F10 |

## Status (2026-06-15)

- **K2 GRADE confidence function — BUILT.** `tools/subagent_factory/grade_confidence.py`:
  `grade_confidence(source_type, downgrades, upgrades) -> {level, range, baseline, rationale}` —
  baseline by source type, ±1 step per factor, clamp to `insufficient|low|medium|high`; medium (and
  any adjusted grade) returns a **range** (K6); explicit **insufficient** floor (K8). Pure
  deterministic, 10 unit tests. The LLM supplies the semantic factors; this owns the arithmetic (K1).
- **K2 wiring — BUILT.** Optional `grade` block in `principles-v1` (`source_type`/`downgrades`/
  `upgrades`); `validate_confidence_grade` gate enforces `confidence == grade_confidence(grade).level`
  (validate-if-present → non-breaking; flags an `insufficient` grade as drop-don't-promote); the
  principle-promotion skill now sets confidence via GRADE. +4 tests.
- **K3 inclusion gate — already satisfied** by `score_extracted_units` (Phase 2.5 importance ranking,
  numbered criteria → deterministic sum → keep/review/discard); the research confirms that design.
- **K4 risk-of-bias = advisory weight, NOT a gate — BUILT.** `grade_confidence.rob_weight(domains)`
  rolls RoB2-style per-domain signals up (any `high` → overall high; else any `some-concerns`; else
  all-low → low; else unclear) and maps overall to **at most one capped `risk-of-bias` downgrade**,
  fired only by a clear overall-`high`. `is_gate: False` is explicit. `grade_with_rob(...)` folds it
  into a grade as advisory downgrades — RoB can only *lower* confidence, never drop a source (F4: RoB
  automation is weak, so it must not gate). **No package-validator gate by design.** +8 tests.
- **K5 conflict → verification label (reground, not average) — BUILT.**
  `grade_confidence.conflict_label(judgments, *, winner, both_wrong)`: agree → `high`; one judge
  vindicated by reground → `one_wins`/`medium`; all wrong or unresolved disagreement → `withhold`
  (route to human). Never averages disagreeing judges (2-of-3 "accept" still withholds). Same
  multi-truth rule as Step-7. +7 tests.
- **K-track complete** (K1 = existing split; K2/K3 built/satisfied; K4/K5 built; K6 = `--judge-samples`
  ensemble already shipped). The remaining items are LLM/authoring-time (supply the semantic RoB and
  conflict signals these functions score), not deterministic code.

## LLM ↔ deterministic split

- **LLM:** per-criterion inclusion judgments, RoB signalling, conflict re-grounding.
- **Deterministic:** the GRADE confidence function, the inclusion sum, RoB→weight, abstention
  thresholds, all roll-up + calibration.

## Reuse / ties (this is the connective tissue)

- **`evidence-protocol.yaml`** — the confidence scale (high/med/low) becomes the GRADE function output.
- **Step 3 faithfulness** — the verbatim-span-per-principle requirement + reject-if-absent.
- **calibration-abstention (Step 13)** — "don't trust self-confidence; abstain calibrated" is the same lesson; the inclusion/conflict abstain is the τ shape.
- **judge replication (`--judge-samples`)** — F2/F10 (ensemble, pin, repeat-runs) generalise it; F2 explains *why* the n=1 judge was unreliable.
- **Step 7 multi-source** — F7 conflict-by-reground-not-average = the multi-truth rule.
- **claim-recall (Step 10)** — F9 (source impact, non-linear recall) refines the recall metric.

## Research inputs (paper IDs)

split [2604.02678, 2406.17755, 2511.03048]; no-raw-self-confidence [2512.20022, 2512.11261]; inclusion
gate [2406.17755, 2411.02451]; RoB advisory [2411.18831, 2511.03048, 2204.10645]; GRADE function
[oa-W1247968195, oa-W2165010366]; medium-as-range [2204.10645]; conflict reground [2604.14165,
2603.28444]; calibrated abstention [2602.10380]; source impact [2306.17614]; pin+provenance [2604.27006,
2604.14165]. Canon: GRADE, PRISMA, RoB2, ROBINS-I, STROBE.

## Exit criteria (when built)

- A deterministic `grade_confidence` function (GRADE start-then-grade) replaces ad-hoc confidence; an
  inclusion-criteria rubric drives the deterministic sum.
- RoB is recorded as advisory weight, never a hard gate; "medium" carries a range.
- Judges pinned + repeat-run-logged; every principle carries a verbatim source span (reject if absent).
- `make verify` green; Tier-0 packages untouched.

## Caveats

- **RoB automation is weak** (the headline negative) — it stays advisory; do not gate on it.
- Open ENGINEERING: the `grade_confidence` function + inclusion rubric are the build targets; the
  research settles the *method*, not the code.
