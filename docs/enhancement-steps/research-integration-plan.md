# Research → factory integration plan (output-quality topics)

How to turn the output-quality research reports into factory changes. Each report is captured as a
findings doc / step spec; this is the **implementation roadmap** — what to build, the
deterministic-vs-LLM split, priority, and current status. Tracks **A–C** are the measure-and-shape
layer (build the adapter well, judge it rigorously); tracks **D–E** are the measure→optimize loop
(generate the test objective, then tune against it).

## Status snapshot
| research | report | captured spec | implemented so far |
|---|---|---|---|
| instruction-induction / agent-distillation | ✅ | A-track (below) | ✅ A1–A5 (`behaviour_replay`, `compile_invariants`, examples slot) |
| agent-benchmarking / LLM-as-judge | ✅ | B-track (below) | ✅ B1–B3,B5,B6 (`rank_versions`,`judge_ab`,`eval_report`); B4 gold = human-gated |
| knowledge-graph / ontology construction | ✅ | C-track (below) | ✅ C1–C3 (`seed_principle_clusters`,`prov.py`,`hearst_isa` opt-in) |
| **behaviour-test-generation** | ✅ PASS 1.0 (41 papers) | **E-track + `step-11-behaviour-test-generation.md`** | spec folded; impl pending |
| **prompt-optimization-eval** | ✅ PASS 1.0 (29 papers) | **D-track + `step-12-optimize-adapter.md`** | spec folded; primitives exist (A-track replay engine) |

---

## A. instruction-induction → Phase 5/9 (principles → adapter rules + examples)
Highest output-quality leverage: it shapes the deliverable (the adapter). Lean on existing infra
(`principle-behaviour-tests.yaml` is the replay harness; `validate_adapter_quality` is the examples
gate).

| # | change | det / LLM | status |
|---|---|---|---|
| A1 | **Example selection by utility** — when authoring adapter examples, prefer ones that measurably change behaviour on the package's behaviour-tests, not embedding similarity | det: replay-score candidates; LLM: draft | ✅ `behaviour_replay.rank_examples_by_utility` (+ `cli replay-score`) |
| A2 | **Replay gate on generated rules/examples** — keep only those that don't regress behaviour-tests (SkillCAT assess-before-merge) | det | ✅ `behaviour_replay.replay_gate` (+ `cli replay-gate`, exit-1 on regression) |
| A3 | **Compile must-hold principles → machine-checkable checks** (adapter enforced-invariant layer) | det check + LLM mine | ✅ `compile_invariants` (high-confidence profile-rule principles → PRP-tagged invariants) + `validate_invariant_coverage` gate |
| A4 | **Require ≥1 failure-and-recovery example** per adapter (not only happy-path) | det gate | ✅ `validate_examples` + `examples` profile slot + adapter template section |
| A5 | **Split adapter into enforced-invariant + induced-guidance layers** | det structure + LLM author | ✅ `## Operating invariants (must hold)` adapter section (above the guidance), rendered from A3's compiled invariants |

**A4 + examples-slot status:** added an optional `examples` block to `profile.yaml`
(`{title, kind, scenario, ideal_response}`, `kind ∈ {happy-path, failure-recovery}`), rendered into a
`## Worked examples` adapter section, wired into the export context. `validate_examples` is
**validate-if-present** (registered on `profile.yaml`, min_tier 99): the 23 example-less packages pass
trivially, but the moment a package ships examples the **A4 rule bites — ≥1 must be
`failure-recovery`** (else FAIL) and each must be well-formed. This also **completes A1's wiring**:
A1 ranks example candidates by utility and they now have a real slot to land in. 8 new tests.

**A1+A2 status:** built on one shared **replay engine** (`tools/subagent_factory/behaviour_replay.py`)
— the execution counterpart to structural-only `run_tests`. It runs each `tests/*.yaml` prompt
through an adapter (as system prompt) via an **injectable runner** (real: `examples/replay-runner.sh`
→ `claude -p --append-system-prompt`; tests: a fake) and scores it with an **injectable grader**
(default = coarse *deterministic* proxy: route engage/decline + `minimum_output` token-recall +
`must_ask_for` + `must_not_do`; swap an LLM grader in for absolute scoring). A1 ranks candidate
examples by measured marginal utility (not similarity); A2 is the SkillCAT assess-before-merge gate
(FAIL on any per-test regression). Proven end-to-end on a real model (advertising-effectiveness
GT-001 → score 0.72). The grader's value is *relative consistency* (deltas/regressions), documented
as such. **Open follow-on:** wire an LLM grader option, and add an `examples` slot to the profile/
adapter template so A1's selected examples actually land in the exported adapter.

## B. agent-benchmarking → Phase 10 (output-quality harness) = the **#1** build
| # | change | det / LLM | status |
|---|---|---|---|
| B1 | Bradley-Terry + bootstrap-CI version ranking | det | ✅ `rank_versions.py` |
| B2 | Position-swapped pairwise judging | det core + LLM judge | ✅ `judge_ab.py` (injectable judge) |
| B3 | **judge ensemble + self-audit** (mean inter-judge agreement, `stable` flag) | LLM | ✅ `judge_ab.run_ab_ensemble` + **independent judge via `examples/codex-judge.sh` (codex / gpt-5.5)** — real cross-family ensemble, not just same-family variance |
| B4 | **gold-set + IAA** (Cohen's κ, judge-vs-gold, trust flag) to break circular eval | det math | ✅ `gold_eval.py` — *harness done; gold DATA must be human-authored (not LLM)* |
| B5 | **Cost/compute-parity accounting** (review length + disparity flag) | det | ✅ `eval_report.py` |
| B6 | Wire the deterministic hedge (`grounding_check` + `claim_recall`) into the harness report | det | ✅ `eval_report.py` |

**B status:** harness functional end-to-end (`eval_report` = judge[+ensemble] → rank → grounding +
cost), used to reach the conclusive 1-vs-2-source verdict (advice EQUAL, grounding the only win).
**Independence now real:** `codex` (gpt-5.5) on this machine is wired as a non-Claude judge
(`examples/codex-judge.sh`), so the ensemble can measure genuine cross-family agreement, not just
same-family variance. Only **B4 gold DATA** stays human-gated (the κ harness is built). A strong
simple baseline (B5) is optional — add a generic non-grounded reviewer to the pool when needed.

## C. knowledge-graph → Phase 7A (refine the principle graph)
Research **done** (report in `docs/Research/knowledge-graph-ontology-construction/`). It **validates
the Step-7 graph design already shipped**: typed-triple multigraph, closed edge vocab
`{refines, supports, specialises, alias}`, directed edges (never symmetric-score refines/
specialises), and "LLM proposes / deterministic decides + provenance gate" — all match
`principle-graph-v1` + the seed→LLM-confirm→validate flow. So C is low-urgency *refinement*, not new
build:
| # | refinement (from the report) | det / LLM | status |
|---|---|---|---|
| C1 | **3-stage dedup cascade** — add (b) distributional cosine + (c) graph-structural similarity to the current (a) lexical `seed_principle_clusters`; closes its known paraphrase-blindness | det + embeddings | ✅ (a)+(b)+(c) done. `seed_clusters(embedder=…, cos_threshold=…, margin=…)` + validated `embed_minilm` + **C1(c) margin-above-baseline** discrimination (below) that fixes the C1(b) over-merge. (Hearst is-a is the separate C3.) |

**C1(b) → C1(c) (measured 2026-06-14).** `embed_minilm` is validated (identical → 1.0; distinct-topic
paraphrase ~0.5 vs unrelated ~0.05). **C1(b) raw cosine over-merged:** on `software-design-simplicity`
(2 books, one topic) every pair sits ~0.4–0.5, so an absolute threshold cannot separate "same
concept" from "same topic" — lowering it collapsed the package into one blob (0.45 → 10-member;
0.35 → all 19). **C1(c) fixes it with a structural signal from the similarity graph**: a pair merges
only if its cosine *stands out* above each principle's **leave-one-out mean cosine to its cross-source
peers** (`margin`), subtracting that same-topic floor. Measured on the same package: the 19-blob
becomes **tight 2-member candidate pairs** at every threshold (0.45 → 1 pair, 0.35 → 2), never a blob.
Leave-one-out keeps it correct on small principle sets (a principle with one cross-source peer has no
floor to clear). Defaults: `cos_threshold=0.5`, `margin=0.15` (set `margin=0` for the old raw
behaviour). So C1 is a genuine win — the third measured arc, but this time the structural refinement
*resolved* the over-merge rather than just tempering it.
| C2 | **PROV-O provenance** — `wasDerivedFrom`/`wasAttributedTo` on nodes/edges (current graph has cluster_id/method/confidence — a subset) | det schema | ✅ `prov.py` (`prov_record`) + `was_derived_from`/`was_attributed_to`/`was_generated_by` on graph-edge & cluster provenance; populated by `seed_principle_clusters` + `hearst_isa`. Clean win (pure schema enrichment, no measurement gamble). |
| C3 | **Hearst dependency-path patterns** for `specializes` (is-a) induction, hybrid with distributional | det + LLM | ⚠️ built + **measured low-yield on factory data** (below). `hearst_isa.py`: spaCy-parse Hearst (+ flat-regex fallback) + nltk WordNet confirmation + `seed_specializes`; opt-in `nlp` extra. Correct on clean text; **noisy on real PDF domain source** → opt-in, not auto-wired. |

**C3 finding (measured 2026-06-14).** Built the hybrid: spaCy snaps Hearst spans to noun-chunk
boundaries (clean heads), nltk WordNet *confirms* a pair (transitive hypernym ⇒ `confidence: high`),
flat regex is the dependency-free fallback. **Correct on clean enumerative text** (unit-tested:
"authentication methods such as OAuth, SAML" → the right is-a pairs). **But on real factory packages
it is low-precision** — run on the api-security source book it produced spurious is-a from PDF noise
("'security bers' is-a 'personal data'") and a common term ("security") exploded to 33 edges, while
**WordNet confirmed none** (domain jargon — OAuth, mirroring, modules — is not in WordNet, so the
hybrid's precision filter is inert). An over-common-term guard cuts 33 → 1, but the survivor is still
noisy ("network tions"). So C3 ships as an **opt-in candidate generator, not auto-wired** into the
graph; `require_wordnet=True` gives high precision at ≈0 recall on domain terms. Third measured arc —
and unlike C1(c) it is **not resolved in-environment**: the real fix is a *domain* hypernym lexicon
(or LLM is-a judging), not general-English WordNet. Honest negative result, capability shipped.

## E. behaviour-test-generation → Step 11 (profile-spec → high-coverage adversarial test suite)
Research **done** (`docs/Research/behaviour-test-generation/`, 41 papers, PASS 1.0). Full spec:
`step-11-behaviour-test-generation.md`. Generates the *objective* the D-track optimizes against, so it
lands first. The three test categories are **encodings of the existing `golden-tests-v1` field set** —
golden ⇒ `expected_route: invoke`, negative-routing ⇒ `expected_route: decline`, missing-context ⇒
`must_ask_for` non-empty — so generated tests are immediately runnable by `behaviour_replay`. Builds
on Step 5 (which stays the per-principle coverage *floor*).

| # | change | det / LLM | status |
|---|---|---|---|
| E1 | **Capability × test-type matrix** — rows=principles, cols={golden, negative-routing, missing-context}; Cartesian-expand to emit `tests/*.yaml` | det scaffold + LLM ideate | spec |
| E2 | **`golden-tests-v1` JSON schema + validator** — close the current schema-exempt gap; add `test_type`/`principle_ref` | det schema | spec |
| E3 | **Hybrid generation** — LLM ideates inputs, deterministic typed templates instantiate reproducible oracles | det + LLM | spec |
| E4 | **Negative-routing = in-scope/OOS hard-negatives** (`expected_route: decline`, OOS-recall-first) | LLM gen + det check | spec |
| E5 | **Missing-context = slot-ablation + answerable twin** (`must_ask_for`; grade silent-commit vs over-ask) | LLM gen + det check | spec |
| E6 | **Coverage-guided keep-if-new + embedding dedup** (`embed_minilm`, rare-weighted, anti-collapse) | det | spec |
| E7 | **Coverage gate** in `validate_generated_package` — every principle exercised per required type; present+tier-gated | det gate | spec |

## D. prompt-optimization-eval → Step 12 (tune the adapter against the E-track objective)
Research **done** (`docs/Research/prompt-optimization-eval/`, 29 papers, PASS 1.0, IMPLEMENTATION_READY).
Full spec: `step-12-optimize-adapter.md`. **Key finding: not a novel mechanism** — it is the standard
`propose → score → keep-winner` loop, and the A-track already shipped every primitive (`replay_suite`
= scorer, `replay_gate` = assess-before-merge, `make_llm_grader` = critique/ranking,
`rank_examples_by_utility` = example axis). So D = **a budgeted driver + an LLM variant proposer** over
existing parts — low new-code, high leverage.

| # | change | det / LLM | status |
|---|---|---|---|
| D1 | **`optimize_adapter.py` driver** — budgeted propose→score→keep loop over the existing primitives | det orchestration | spec |
| D2 | **Variant proposer skill** — gets failing tests + grader critique + scored history + faithfulness constraint | LLM | spec |
| D3 | **Hard pre-merge gate** — faithfulness + quote + adapter-policy scan **before** the replay gate (anti-reward-hacking) | det | spec |
| D4 | **Behaviour-tests = merge gate; grader = ranking only** (never raw reward); finding-#9 judge guards | det gate + LLM rank | spec |
| D5 | **Cost control** — minibatch-screen→full-confirm, N-variants/call, closed-form budget N×T×(1+\|D\|), early stop | det | spec |
| D6 | **Diversity pool** — small beam/Pareto of per-test winners (+6–11% vs greedy at equal budget) | det | spec |
| D7 | **Joint rule+example optimization** (MIPRO/DSPy blueprint) — edits induced guidance *and* worked examples; invariant layer frozen | det + LLM | spec |
| D8 | **`cli optimize-adapter`** — produces a new profile version (bump+changelog+validate+re-export), optional eval row | det | spec |

**Sibling dependency.** D scores against E's suite; the loop is only as good as the tests. Build order:
**E first (objective), then D (optimizer).** Both are single-turn for now (E's G2 multi-turn coverage
gap is deferred). Foundational canon (APE/OPRO/DSPy/TextGrad/GEPA/MIPRO) was assembled by direct
arXiv-ID injection under the recency-lock ([[arxiv-index-recency-locked]]) — a discovery limit, not a
literature gap.

---

## Prioritized roadmap (output-quality first)
1. ✅ **A1 + A2** — example-by-utility + replay gate (`behaviour_replay.py`). Done: shared replay
   engine, injectable runner/grader, CLI, 12 tests, live-proven.
2. ✅ **B3 + B5 + B6** — eval harness (#1): judge ensemble (+ cross-family codex judge) + cost-parity
   + deterministic hedge wiring. Every future change is now *measurable*, not hand-judged.
3. ✅ **A4** recovery-example gate + examples slot. ✅ **A3 + A5** compiled must-hold invariant layer
   (`compile_invariants` → `## Operating invariants` + non-breaking coverage gate).
4. ✅ **C1 + C2** — graph dedup cascade + PROV-O provenance (`seed_principle_clusters`, `prov.py`);
   ⚠️ **C3** Hearst is-a shipped opt-in (measured low-yield on domain source).
5. **E (Step 11)** — behaviour-test generator: the *objective*. **← next build (folds the E-track).**
6. **D (Step 12)** — optimize-adapter loop over the existing replay primitives. **After E** (D scores
   against E's suite).
7. **B4** — independent gold set (human data work; the rigorous-eval capstone). **← resource-gated**

**A-track (A1–A5) + C-track (C1–C3) are built; B-track is built except B4 (human gold data).** The
research is now *folded* for D + E (specs `step-12-optimize-adapter.md`, `step-11-behaviour-test-
generation.md`); next is **implementing E then D**. Follow-ons (small): LLM-grader option already
exists (`make_llm_grader`); an LLM wording-refinement pass over compiled invariants; **bulk re-export**
of the existing packages so they adopt the invariant + examples layers (non-breaking until
re-exported).

## Cross-cutting constraints (from the research)
- Every LLM step passes a deterministic gate before entering the adapter (factory discipline).
- Multi-truth on conflicts (Step 7) — never force one winner.
- Foundational canon for instruction-induction + LLM-as-judge bias is **environment-limited**
  (arXiv recency-lock, [[arxiv-index-recency-locked]]); do a manual lit pull before productionising
  B3/B4 and A3.
