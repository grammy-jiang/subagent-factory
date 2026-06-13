# Research → factory integration plan (3 output-quality topics)

How to turn the three output-quality research reports into factory changes. Each report is already
captured as a findings doc; this is the **implementation roadmap** — what to build, the
deterministic-vs-LLM split, priority, and current status.

## Status snapshot
| research | report | captured spec | implemented so far |
|---|---|---|---|
| instruction-induction / agent-distillation | ✅ | `instruction-induction-findings.md` | none yet (Phase 5/9 build) |
| agent-benchmarking / LLM-as-judge | ✅ | `agent-benchmarking-findings.md` | `rank_versions.py`, `judge_ab.py` (Phase-10 core) |
| knowledge-graph / ontology construction | ⏳ running | (pending) | target already built: Step-7 `principle-graph.json` |

---

## A. instruction-induction → Phase 5/9 (principles → adapter rules + examples)
Highest output-quality leverage: it shapes the deliverable (the adapter). Lean on existing infra
(`principle-behaviour-tests.yaml` is the replay harness; `validate_adapter_quality` is the examples
gate).

| # | change | det / LLM | leans on |
|---|---|---|---|
| A1 | **Example selection by utility** — when authoring adapter examples, prefer ones that measurably change behaviour on the package's behaviour-tests, not embedding similarity | det: replay-score candidates; LLM: draft | principle-behaviour-tests, run_tests |
| A2 | **Replay gate on generated rules/examples** — keep only those that don't regress behaviour-tests (SkillCAT assess-before-merge) | det | run_tests, validate gate |
| A3 | **Compile must-hold principles → machine-checkable checks** (adapter enforced-invariant layer) | det check + LLM mine | export_claude_agent, a checks artifact |
| A4 | **Require ≥1 failure-and-recovery example** per adapter (not only happy-path) | det gate | validate_adapter_quality (extend) |
| A5 | **Split adapter into enforced-invariant + induced-guidance layers** | det structure + LLM author | export_claude_agent |

## B. agent-benchmarking → Phase 10 (output-quality harness) = the **#1** build
| # | change | det / LLM | status |
|---|---|---|---|
| B1 | Bradley-Terry + bootstrap-CI version ranking | det | ✅ `rank_versions.py` |
| B2 | Position-swapped pairwise judging | det core + LLM judge | ✅ `judge_ab.py` (injectable judge) |
| B3 | **3-judge ensemble** (members not base models of a candidate) + within/inter-judge self-audit | LLM | todo — extend judge_ab |
| B4 | **Independent gold/human set + IAA** (Krippendorff α) to break circular eval | data + det | todo |
| B5 | **Cost/compute-parity accounting + strong simple baseline** in every comparison | det | todo — extend judge_ab/report |
| B6 | Wire the deterministic hedge (`grounding_check` + `claim_recall`) into the harness report | det | tools exist; wire |

## C. knowledge-graph → Phase 7A (refine the principle graph)
Lowest urgency — the graph already exists (Step-7 Phase C). When the report lands:
| # | change | det / LLM |
|---|---|---|
| C1 | Taxonomy/alias induction methods → improve `seed_principle_clusters` recall + relation typing | det seed + LLM |
| C2 | Edge/relation vocabulary + provenance refinements to `principle-graph-v1` | det schema |

---

## Prioritized roadmap (output-quality first)
1. **A1 + A2** — example-by-utility + replay gate. Biggest direct adapter-quality lift; reuses the
   behaviour-test harness; mostly deterministic.
2. **B3 + B5 + B6** — finish the eval harness (#1): judge ensemble + cost-parity + deterministic
   hedge wiring. Lets every future change be *measured*, not hand-judged.
3. **A4 + A3 + A5** — recovery-example gate, compiled invariant checks, layered adapter.
4. **B4** — independent gold set (data work; the rigorous-eval capstone).
5. **C1 + C2** — graph refinement, after the kg report.

## Cross-cutting constraints (from the research)
- Every LLM step passes a deterministic gate before entering the adapter (factory discipline).
- Multi-truth on conflicts (Step 7) — never force one winner.
- Foundational canon for instruction-induction + LLM-as-judge bias is **environment-limited**
  (arXiv recency-lock, [[arxiv-index-recency-locked]]); do a manual lit pull before productionising
  B3/B4 and A3.
