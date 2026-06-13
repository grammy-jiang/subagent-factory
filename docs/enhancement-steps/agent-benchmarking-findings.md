# Agent benchmarking / output-quality evaluation — research findings → harness design

Source: `docs/Research/agent-benchmarking-output-evaluation/` (validated report, PASS 1.00,
2026-06-13). Output-quality research topic (§20), Phase 10. This distils the findings into the
target eval-harness design **and flags the concrete flaws in the current ad-hoc method**
(`docs/output-quality-eval.md`). Spec, not yet built.

## What the current method got right (validated)
- **Multi-dimension reference-free rubric** (score orthogonal axes — Actionability / Grounding /
  Verifiability / Technical depth — not one scalar). Our rubric already does this.
- **Hedge the LLM judgement with an independent deterministic signal** — exactly the
  `grounding_check` + `claim_recall` combo. Keep it; it makes verdicts diagnostic (WHERE a version
  fails), and saturating metrics mask each other.
- **Anchor open-ended advice with a rubric + human spot-checks** — reference-free judging is least
  reliable precisely for open-ended advice with no ground truth.

## What the current method got WRONG (fix before trusting verdicts)
1. **Self-preference bias:** I (a base model of the candidates) was the judge. Finding: judge
   rankings are systematically biased (position, verbosity, self-preference, intransitivity). Fix:
   a **multi-judge ensemble whose members are NOT base models of any candidate**, + calibration, +
   self-audit (within-judge stability + inter-judge agreement) before trusting the judge.
2. **No cost/compute parity:** the 1-source vs 2-source A/B let the 2-source win partly for having
   more content/cost. Finding: a fair comparison must control cost/compute parity and include a
   strong simple baseline (a single-agent CoT-SC beat an automated multi-agent system at <10% cost).
   Re-run the A/B with parity + a baseline before claiming 2-source "wins".
3. **Circular / self-generated evaluation:** self-judged, no independent authority. Finding:
   evaluation validity is a governance property; co-generating judge labels with the system inflates
   scores (Micro-F1 ~0.54 silver → ~0.03 gold). Hold out an **independent gold/human authority set**.
4. **No uncertainty on the verdict:** accept a 1-source-vs-2-source ranking only when intervals
   don't overlap. Finding: pairwise **Bradley-Terry/Elo against a diverse opponent pool** with
   calibrated soft win-probabilities + **split-conformal intervals** (≈90% coverage), not win-rate
   vs a single fixed baseline.

## Target harness (Phase 10)
- **Judging:** multi-dim rubric → 3-judge ensemble @temp0 (none a base model of a candidate) →
  blind position-swapped pairwise → Bradley-Terry/Elo + bootstrap/conformal CIs → Score-Alignment.
- **Authority:** held-out independent gold/human set + IAA pipeline (Krippendorff α / Fleiss κ over
  an overlap set) to break circular evaluation.
- **Fairness:** cost/compute-parity accounting + a strong simple baseline in every comparison.
- **Robustness:** contamination / prompt-sensitivity controls + a regenerable eval set.
- **Independent signal:** keep the deterministic `grounding_check` + `claim_recall` as the hedge.
- **Protocol:** decouple judge from subject behind a standard protocol so one harness compares
  heterogeneous subagent versions reproducibly (judge-as-agent can run the task, not just score a
  transcript).

## Open gaps (environment-limited — arXiv recency-locked, see [[arxiv-index-recency-locked]])
- AC1/AC2 (HIGH): no paper validates judge calibration/bias **on long-form expert advisory output**
  specifically, nor bias-mitigation residual effectiveness there — import the canonical LLM-as-judge
  bias literature (MT-Bench, G-Eval, AlpacaEval, Chatbot Arena/Elo, position/verbosity bias) out of
  band before production.
- AC3 (MED): a reference-free scorer tuned for the advisory failure mode (ungrounded/over-claimed
  recommendations), not literal-match QA.
- AC4 (MED): sample-size / statistical-power guidance for a stable Elo verdict between close versions.

## Implication
The eval *finding* that the 2-source subagent is better (Step 7 / multi-source) still holds on
grounding (deterministic `grounding_check`: leak→grounded is not judge-dependent), but the *advice-
quality* half of that A/B should be re-run under this harness (judge ensemble + cost parity +
intervals) before stating it as a measured win rather than a qualitative read.
