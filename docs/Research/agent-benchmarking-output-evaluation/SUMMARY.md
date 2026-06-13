# Research Run Summary

## 1. Final report

`agent-output-quality-llm-as-judge-evaluation-research-report.md` (validated PASS, score 1.00, 12-section check).

> Note: the runner prints a long topic-slug filename, but that path exceeds the 255-byte
> filesystem limit (`OSError 36 File name too long`) and cannot be created. The canonical
> deliverable is the friendly-slug report above. Validation + completion gates were run
> against it and pass.

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | `20260613T102451Z` | Original topic: LLM-as-judge, rubric, pairwise/Elo, reference-free, free-form advisory evaluation | 347 searched → 10 analyzed | Initial shortlist + full synthesis | 4 academic (2 HIGH, 2 MEDIUM), 4 engineering, 1 out-of-scope |
| 2 | `round2-foundational` | Close HIGH academic gaps — foundational LLM-as-judge bias literature (MT-Bench, G-Eval, AlpacaEval, Chatbot Arena/Elo, position/verbosity bias) | 0 relevant (181 candidates, **all dated 2026-06-11**, 0 canonical, 0 pre-2026) | HIGH academic gaps **reclassified** as environment-limited | 2 academic (MEDIUM), 4 engineering, 1 out-of-scope |

**Stop reason**: Round-2 gap-closure search returned **0 relevant foundational papers** — the only
reachable source (arXiv) is recency-locked to a single day (2026-06-11); auxiliary sources failed
(Semantic Scholar `429` no-key; OpenAlex `400`). The two HIGH academic gaps are therefore
**un-closeable in this environment** and reclassified as environment-limited (import out-of-band).
Loop stopped at round 2 (below the 4-round cap) per the "new search returned 0 relevant papers"
stopping condition. `convergence.should_continue = false`, `reason = no_new_papers`.

## 3. Remaining open gaps (`gaps.json`)

| ID | Class | Severity | One line |
|----|-------|----------|----------|
| AC1 | ACADEMIC (env-limited) | HIGH | No paper validates LLM-judge calibration/bias quantification on long-form **expert advisory/review** output specifically. Reclassified — import canonical bias literature out-of-band. |
| AC2 | ACADEMIC (env-limited) | HIGH | No quantified study of judge-bias **mitigation effectiveness** (residual position/verbosity/self-preference bias after mitigation) on free-form advisory text. Reclassified — import out-of-band. |
| AC3 | ACADEMIC | MEDIUM | No reference-free scorer validated for the advisory failure mode (ungrounded / over-claimed recommendations) — a faithfulness scorer tuned for advisory claims, not literal-match QA. |
| AC4 | ACADEMIC | MEDIUM | No sample-size / statistical-power guidance for a STABLE Elo/win-rate verdict between two close versions (1-source vs 2-source). |
| EN1 | ENGINEERING | HIGH | Implement consensus judging protocol (multi-dim rubric, 3-judge ensemble @temp0, blind position-swapped pairwise, BT/Elo + bootstrap CIs, Score-Alignment, conformal intervals). Resolved inline. |
| EN2 | ENGINEERING | HIGH | Build held-out independent gold/human authority set + IAA pipeline to break circular evaluation. Resolved inline (data work). |
| EN3 | ENGINEERING | MEDIUM | Wire cost/compute-parity accounting + strong simple baseline into the comparison harness. Resolved inline. |
| EN4 | ENGINEERING | MEDIUM | Contamination / prompt-sensitivity controls + regenerable eval set to keep harness discriminative. Resolved inline. |
| OOS1 | OUT_OF_SCOPE | LOW | Generalizing these methods beyond the factory's targets (multimodal UX, German public-sector law) is out of scope. |

No HIGH academic gap remains *open*: both were genuinely attempted in Round 2 and reclassified
environment-limited. Engineering gaps are resolvable inline by the Phase-10 harness build.

## 4. Findings most relevant to DOWNSTREAM USE (Phase-10 output-quality harness)

1. **Multi-dimension reference-free rubric is the consensus way to operationalize "good advice"** — score orthogonal axes (e.g. Actionability / Grounding / Verifiability / Technical Depth), not one scalar. *(2606.13349, 2606.12984, 2606.13192, 2606.13111)*
2. **Compare subagent versions with pairwise Bradley-Terry/Elo against a DIVERSE opponent pool**, carrying explicit uncertainty — not win-rate vs a single fixed baseline (fragile under non-transitive judge preference). Accept a 1-source-vs-2-source ranking only when intervals don't overlap. *(2606.13221, 2606.13349, 2606.13598)*
3. **Judge rankings are systematically biased (position, verbosity, self-preference, intransitivity); proven mitigations are a multi-judge ensemble whose members are NOT base models of any candidate, plus calibration** — and self-audit the judge (within-judge stability + inter-judge agreement) before trusting it. *(2606.13221, 2606.13349, 2606.13111)*
4. **Reference-free judging is unreliable exactly for genuinely open-ended advice with no single ground-truth** — judge quality degrades there; anchor with a rubric where possible and keep human spot-checks. *(2606.12984, 2606.13111, 2606.13192)*
5. **Evaluation validity is a system-level governance property, not neutral measurement** — co-generating judge labels with the system under test inflates scores circularly; they collapse under an independent gold/human authority (Micro-F1 ~0.54 silver → ~0.03 gold). Hold out an independent gold set. *(2606.13436, 2606.13111)*
6. **A fair version comparison must control cost/compute parity and include a strong simple baseline** — else an expensive multi-source variant wins merely for spending more (single-agent CoT-SC beat automated MAS at <10% cost). *(2606.13003, 2606.13436)*
7. **Separate CONTENT quality from RATING calibration**, and give rankings honest distribution-free uncertainty: convert graded scores to calibrated soft win-probabilities + split-conformal intervals (≈90% coverage, 30–73% narrower than hard-label; 17.9 Elo MAE vs human). *(2606.13349, 2606.13221)*
8. **Report inter-annotator agreement for judge↔human meta-evaluation** (Krippendorff α, Fleiss/Cohen κ) over an overlap set, with a high-trust labeling pipeline (independent annotation, cross-validation, expert QC). *(2606.13349, 2606.13192, 2606.13111)*
9. **Hedge any single scorer with an independent signal** (deterministic grounding/faithfulness check + a ranking metric) since saturating/collapsing metrics mask each other; process-level + additive-ablation scoring makes verdicts diagnostic (WHERE a version fails). *(2606.13111, 2606.13436, 2606.13192, 2606.12984, 2606.13020)*
10. **Decouple judge logic from subject implementation behind a standardized protocol** so one harness evaluates heterogeneous subagent versions reproducibly head-to-head; a "judge-as-agent" can provision tools and run the task rather than scoring a static transcript. *(2606.13608)*

---

RESEARCH RUN COMPLETE: agent-output-quality-llm-as-judge-evaluation-research-report.md
