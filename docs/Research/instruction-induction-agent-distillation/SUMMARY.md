# Research Run Summary

## 1. Final report
`instruction-induction-agent-distillation-research-report.md` — validated **PASS, score 1.00**.

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | 20260613T094916Z | Original topic; broad query + 20 variants, `--source arxiv` | 13 | Initial shortlist (rule/skill induction, hint distillation, exemplar selection, decision policies) | 2 HIGH academic, 1 MEDIUM academic, 1 engineering |
| 1b (probe) | 20260613T095628Z | Recall probe naming Honovich / self-instruct / APE | 0 on-topic | Proved index is recency-locked to 2026; foundational canon unreachable | same |

**Stop reason**: new search returned 0 relevant pre-2026 papers; the arXiv index is recency-locked to 2026-06 (556/556 main-run candidates dated 2026-06; the foundational-named probe also returned only 2026 papers). The HIGH foundational-literature gap is **environment-limited** — not closeable by additional rounds in this sandbox — so rounds 2–4 were not run (they would re-query the same index). Engineering gap resolved inline.

## 3. Open gaps

| # | Gap | Type | Severity | One-liner |
|---|-----|------|----------|-----------|
| 1 | Foundational instruction-induction canon (Honovich, APE, Self-Instruct, Constitutional AI, OPRO, KATE) | ACADEMIC (environment-limited) | HIGH | Index only serves 2026 papers; re-run outside sandbox with full-history index/S2 key. |
| 2 | Direct *principle → behavioural rule for persona* transform | ACADEMIC | HIGH | Only covered by analogy (correction→rule [2606.13174]); no direct paper in 2026 index. |
| 3 | Worked-example *generation* (vs selection) for a persona | ACADEMIC | MEDIUM | Factory must author examples, not just retrieve them. |
| 4 | Deterministic-vs-LLM split for Phase 5/9 | ENGINEERING | MEDIUM | RESOLVED inline (see report Practical Recommendations recipe + Mermaid). |

## 4. Findings most relevant to the DOWNSTREAM USE (Phase 5/9: principles → adapter rules + worked examples)

1. **Compile principles into atomic, typed rules + machine-checkable enforcement**, not prose. Compiling user corrections into atomic rules + runtime checks cut repeated preference violations **100% → 2% out-of-distribution**. — [2606.13174]
2. **Induce rules/skills, then assess-before-adopt; do not trust hand-written skill text.** Contrastively-induced, replay-verified skill documents beat **human-written skills by +45.8 points** verified-task-rate. The factory's `principle-behaviour-tests.yaml` is the natural replay gate. — [2606.13317]
3. **Type the rule store**: deterministic rule-based form for syntactic/format invariants, conflict-aware structured schema for semantic/judgement guidance; distilled "hint banks" transfer across models. +17.5 pts pass-rate. — [2606.12387]
4. **Select/author few-shot examples by task *utility/feedback*, not embedding similarity** — upgrades the existing "examples EXIST" gate toward "examples are GOOD". GRIP (+2.1 pts) and RA-RFT (+7.1 pts) both beat similarity retrieval. — [2606.12744], [2606.13680]
5. **Include failure-and-recovery worked examples, not only happy-path**: small-corpus distillation teaches format but misses recovery behaviour. — [2606.12674]
6. **Keep decision policies explicit and auditable** (linear scores / decision tables / FSM) for must-hold behaviour; reserve free LLM judgement for open-ended steps. Split adapter into a fixed *enforced-invariant* layer and an induced *improvable-guidance* layer. — [2606.12945], [2606.12369]
7. **Condition a strong-model teacher on the principle/rubric to draft the worked example, then strip the conditioning** (RGSD pattern); also curbs over-claiming (false-claim 35% vs 45%), aligning with the repo faithfulness rule. — [2606.12507]
8. **Validate that every generated instruction/example is grounded in its source principle** via a closed-evidence check — the literature analogue of the repo's faithfulness/quote-scan gates (96.5% grounded under strict generation). — [2606.12767]
9. **Deterministic vs LLM split (engineering recipe)**: LLM mines candidate rules + drafts examples; deterministic steps type/normalize/dedup/detect-conflicts/compile-checks and replay against behaviour tests + grounding scan; only passing artifacts enter the adapter. — synthesis of [2606.13317] + [2606.13174]

## 5. Method / environment notes
- BM25 screen tool hit a v0.28.0 `datetime not JSON serializable` bug → replaced with deterministic topical scoring + manual abstract-level screen (556 → 13).
- CLI summarize ran in heuristic-fallback mode (no LLM); per-paper quantitative evidence was re-derived directly from the docling-converted Markdown.
- Scholar / Semantic Scholar / OpenAlex / DBLP returned 0 (not configured in this environment).

RESEARCH RUN COMPLETE: instruction-induction-agent-distillation-research-report.md
