# Step 3 — Evidence Records + Faithfulness-v1

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 3. Depth: **full**.
> Research: `docs/Research/factual-consistency-faithfulness/` (full) + `argument-mining-claim-extraction/` (evidence linking).

## Goal
Bind each high-value claim to **source-grounded evidence records**, and upgrade faithfulness
from "rule vs raw source text" (Step 1 v0) to **"rule vs evidence record"** — catching rules
that are *stronger than the evidence supports* with claim-strength precision.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `subagents/<slug>/evidence/evidence-records.yaml` | artifact | Claim → source → strength records. |
| `schemas/evidence-records-v1.schema.json` | schema | Evidence-record shape + enums. |
| `tools/subagent_factory/validate_evidence_records.py` | tool (validator) | Structural + referential. |
| `.claude/skills/faithfulness-review/SKILL.md` | skill (LLM, **upgrade**) | v1: rule vs evidence record. |
| `.claude/agents/faithfulness-reviewer.md` | agent (LLM, **upgrade**) | Claim-strength comparison vs evidence. |

(`faithfulness-report-v1` schema + `validate_faithfulness_report.py` already exist from Step 1;
Step 3 changes the *comparison target*, not the report shape.)

## `evidence-records-v1` schema
```yaml
schema_version: evidence-records-v1
evidence_records:
  - evidence_id: E-0001
    claim_id: C-0001                   # ∈ analysis/claims.jsonl
    source_ids: ["<sid>"]              # ∈ manifest
    source_anchors: ["<sid>-p0042"]    # ∈ anchor index
    support_granularity: section       # section | page | heading
    evidence_type: research            # explanation|case|research|expert|other (AQE 5-way)
    evidence_strength: moderate        # strong | moderate | weak
    support_level: partially_supported # entailed | partially_supported | not_supported  (WiCE 3-way)
    confidence: medium                 # high | medium | low
    quote_allowed: false               # derived from source rights_status
    limitations: "Author gives rationale + example, no empirical data."
```

## Faithfulness-v1 rubric (factual full report)
The reviewer compares each **profile rule** against its **evidence record(s)** and emits a
`faithfulness-report-v1` finding using the **5-level claim-strength ordering**:

`EXACT_SUPPORT → WITHIN_SCOPE → SCOPE_BROADENED → HEDGING_REMOVED → CONTRADICTED`

Method, grounded in the report:
- **WiCE Partially-Supported** [2303.01432] = the only existing 3-way overclaim proxy → maps to
  `SCOPE_BROADENED`/`HEDGING_REMOVED`.
- **Janus Specificity + Framing** [2606.10852]: Specificity = numeric-precision inflation;
  Framing = hedge removal (`may/often` → `always`). Both are direct overclaim dimensions.
- **RefChecker triplet, 3-way verdict** [2405.14486]: extract `(head, relation, tail)`, check each
  vs evidence; Neutral + stronger-than-source = overclaim.
- **Granularity**: sentence/triplet, never document-level [2111.09525] (doc-level NLI rates
  inconsistent summaries as entailed).
- **Per-claim score** (report Methodology Comparison):
  `S = w_support·P(entail) + w_partial·P(partial)`, `w_support=1.0`, `w_partial∈[0,0.5]`.
- **Provenance-grounded** [2606.11127]: check against **exact source spans** (our `source_anchors`),
  not post-hoc retrieval — exact provenance outperforms retrieval.
- **Faithfulness ≠ factuality** [2005.00661]: we check *grounded-in-source*, not world-truth.
- **Do not use model uncertainty** as a faithfulness proxy [2605.27016] (near-zero correlation).

## Reuse
- `analysis/claims.jsonl` (Step 2) — `claim_id` target.
- `inject_anchors.py` index — `source_anchors`.
- `provenance-ledger.md` — narrative backbone; evidence records are the machine layer beside it (master §4.1).
- `source_text.py` — source access; rights_status → `quote_allowed`.

## `validate_evidence_records.py` (structural + referential)
- unique `evidence_id`; `claim_id` ∈ claims; `source_ids` ∈ manifest; `source_anchors` ∈ anchor index.
- enums (`evidence_type`, `evidence_strength`, `support_level`, `confidence`) valid.
- `quote_allowed` consistent with the source's `rights_status` (distillation-only/restricted ⇒ false).
- **Coverage**: every claim marked promotable (top importance tier) has ≥1 evidence record.

## Gate wiring
Tier 1+ (present-gated). Faithfulness-v1 finding severity unchanged from Step 1
(`CONTRADICTED`/unresolved `unsupported` ⇒ FAIL; over-claim ⇒ WARN with `action`).

## LLM ↔ deterministic split
- LLM: `faithfulness-reviewer` (claim-strength comparison vs evidence).
- Deterministic: `validate_evidence_records.py`, `validate_faithfulness_report.py`.

## Fixtures
- Paired (claim, evidence record, profile rule) per verdict level — incl. the canonical
  `HEDGING_REMOVED` (`source: "prefer X in context"` → `rule: "always X"`).
- A claim with no evidence record (promotable) → coverage failure.
- A `quote_allowed: true` on a distillation-only source → rights inconsistency failure.

## Exit criteria + verify
1. `validate_evidence_records` passes good records; fails referential/rights/coverage violations.
2. Every promotable claim has ≥1 evidence record.
3. Faithfulness-v1 catches a planted over-claim against its evidence record (not just raw text).
4. All 15 Tier-0 packages still pass `validate`.

## Caveats (research limits — validate ourselves)
- **Overclaim detector is original engineering** (factual gap-1): no validated model exists; we
  *compose* WiCE + Janus + RefChecker via an LLM agent. **Calibrate** against WiCE-style examples;
  the report recommends targeting **≥ AlignScore accuracy on WiCE** before trusting it.
- **Domain mismatch** (factual gap-4): all metrics validated on news/Wikipedia, not short
  imperative subagent rules → thresholds tentative; recalibrate.
- **MiniCheck/AlignScore are model-based.** We use an LLM agent + their *rubric*; integrating the
  actual models (DeBERTa MiniCheck as a cheap pre-filter) is an optional later optimization, not v1.
- **Anchors coarse** (section/page) — `support_granularity` records the limit.

## Risks
- LLM reviewer leniency → mitigate with explicit 5-level few-shots + deterministic refusal of
  unresolved `CONTRADICTED`.
- Evidence records authored by the same LLM that extracted claims → risk of self-confirmation;
  faithfulness compares against the *source spans* (provenance), not just the paraphrase, to break the loop.
