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
| **behaviour-test-generation** | ✅ PASS 1.0 (41 papers) | **E-track + `step-11-behaviour-test-generation.md`** | ✅ det core (`gen_behaviour_tests`, schema, coverage gate); LLM ideation = follow-on |
| **prompt-optimization-eval** | ✅ PASS 1.0 (29 papers) | **D-track + `step-12-optimize-adapter.md`** | ✅ driver + proposer skill + live CLI (`cli optimize-adapter`) |
| **calibration-abstention** | ✅ PASS 1.0 (31 papers) | **F-track + `step-13-ask-gate.md`** | ✅ F3+F4 built (answerable-twins + two-axis grading); F1/F2/F5 runtime gate spec (black-box gap) |
| **rag-graphrag** (§20 #10) | ✅ PASS 1.0 (20+ papers) | **G-track + `step-14-runtime-retrieval.md`** | spec folded (post-v0 runtime layer); 3 inherent HIGH gaps → ships behind measurement |
| **table-extraction** (§20 #2) | ✅ PASS 1.0 | **H-track + `step-20` table-preservation section** | ✅ COMPLETE — opt-in TSR → `<table>` HTML → `-t` anchors + caption assoc (H2) + degeneracy gate (H3); flag-gated, default byte-unchanged |
| **automated-program-repair** (§20 #13) | ✅ PASS 1.0 (41 papers, 3 rounds, reviewer-accepted) | **I-track + `step-6` patch-generation section** | ✅ engine built — `validate_patch` ladder (I1/I3/I5/I6 done, I4 partial); I2 oracles carried (LLM/academic) |
| **domain-adaptation-regulated-advice** | ✅ PASS 1.0 (25 papers, 2 rounds) | **J-track + `step-15-domain-adaptation-policy.md`** | spec folded; answers Q1 (finance/legal/medical) — hybrid det-template + LLM-interrogation method |
| **systematic-review-evidence-synthesis** (§20 #1) | ✅ PASS 1.0 (30 sources) | **K-track + `step-16-evidence-grading.md`** | spec folded; GRADE-style confidence + judge discipline; ties calibration + judge-replication + Step-7 |

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
lands first. The three test categories are **the existing `golden-tests-v1` top-level sections**
(`_TEST_SECTIONS`) — golden_tests ⇒ `expected_route: invoke`, negative_routing_tests ⇒
`expected_route: do_not_invoke`, missing_context_tests ⇒ `must_ask_for` non-empty — so generated tests
are graded by `behaviour_replay` the moment they are written (round-trip test proves it). Builds on
Step 5 (which stays the per-principle coverage *floor*).

| # | change | det / LLM | status |
|---|---|---|---|
| E1 | **Capability × test-type matrix** — rows=principles, cols={golden, negative-routing, missing-context}; Cartesian-expand to emit the three sections | det scaffold + LLM ideate | ✅ `gen_behaviour_tests` |
| E2 | **`golden-tests-v1` JSON schema + validator** — close the schema-exempt gap; `principle_coverage` linkage | det schema | ✅ `schemas/golden-tests-v1.schema.json` + `validate_behaviour_test_coverage` (gate-wired) |
| E3 | **Hybrid generation** — LLM ideates inputs (injectable `ideator`), deterministic typed templates instantiate reproducible oracles | det + LLM | ✅ template-mode default + `ideator` hook |
| E4 | **Negative-routing = in-scope/OOS hard-negatives** (`expected_route: do_not_invoke`, OOS-recall-first) | LLM gen + det check | ✅ section + oracle gate (LLM hard-negatives = follow-on) |
| E5 | **Missing-context = slot-ablation + answerable twin** (`must_ask_for`; grade silent-commit vs over-ask) | LLM gen + det check | ✅ section + oracle gate (answerable-twin pairing = follow-on) |
| E6 | **Coverage-guided keep-if-new + embedding dedup** (`embed_minilm`, rare-weighted, anti-collapse) | det | ✅ embedding dedup + **rare-weighted multi-candidate selection** (`n_candidates`/`_choose_prompt` + `cli --candidates`): ideate N per cell, keep the most novel (lowest max-cosine to the accepted set) |
| E7 | **Coverage gate** in `validate_generated_package` — every high-conf principle has a golden test; present+tier-gated (min_tier 99, keyed on `tests/behaviour-tests.yaml`) | det gate | ✅ wired; non-breaking proven (Tier-0 + Tier-1) |

**E-track status (built 2026-06-14).** The deterministic core is **implemented + gate-wired**:
`gen_behaviour_tests.py` (matrix → three sections → typed templates, injectable `ideator`/`embedder`),
`schemas/golden-tests-v1.schema.json`, `validate_behaviour_test_coverage.py` (schema + oracle-shape +
per-principle golden coverage), wired into `validate_generated_package` present+tier-gated. Proven
end-to-end (api-security-reviewer: 14 principles → 42 tests, coverage PASS) and **non-breaking** (15
Tier-0 packages + the Tier-1 package both still validate). 16 unit tests including a **round-trip
through the real `behaviour_replay` engine** (proves the routes grade correctly — this caught a
contract bug: negative routing is `do_not_invoke`, not `decline`).

**LLM ideator DONE (2026-06-14):** `gen_behaviour_tests.shell_ideator` + `examples/behaviour-test-
ideator.sh` + `cli gen-behaviour-tests --ideator` wire an LLM to write realistic prompts and
**hard-negative out-of-scope** requests (vs the template-mode restatement of `does_not_apply_when`);
template-mode stays the free default, the ideator falls back to it on any failure. **Both former E
follow-ons are now DONE:** answerable-twin pairing (Step-13 F4) and the **rare-weighted multi-candidate
selection** (E6 — `n_candidates`/`_choose_prompt`: ideate N per cell, keep the most novel by lowest
max-cosine to the accepted set).

## D. prompt-optimization-eval → Step 12 (tune the adapter against the E-track objective)
Research **done** (`docs/Research/prompt-optimization-eval/`, 29 papers, PASS 1.0, IMPLEMENTATION_READY).
Full spec: `step-12-optimize-adapter.md`. **Key finding: not a novel mechanism** — it is the standard
`propose → score → keep-winner` loop, and the A-track already shipped every primitive (`replay_suite`
= scorer, `replay_gate` = assess-before-merge, `make_llm_grader` = critique/ranking,
`rank_examples_by_utility` = example axis). So D = **a budgeted driver + an LLM variant proposer** over
existing parts — low new-code, high leverage.

| # | change | det / LLM | status |
|---|---|---|---|
| D1 | **`optimize_adapter.py` driver** — budgeted propose→score→keep loop over the existing primitives | det orchestration | ✅ `optimize_adapter` |
| D2 | **Variant proposer skill** — gets failing tests + grader critique + scored history + faithfulness constraint | LLM | ✅ `.claude/skills/adapter-optimization/` (injectable `Proposer`) |
| D3 | **Hard pre-merge gate** — faithfulness + quote + adapter-policy scan **before** the replay gate (anti-reward-hacking) | det | ✅ injectable `AcceptGate` seam (rejects pre-scoring; default permissive — production injects the scans) |
| D4 | **Behaviour-tests = merge gate; grader = ranking only** (never raw reward); finding-#9 judge guards | det gate + LLM rank | ✅ gate = assess-before-merge on replay scores; grader injectable |
| D5 | **Cost control** — minibatch-screen→full-confirm, N-variants/call, early stop, `eval_calls` accounting | det | ✅ minibatch + budget + patience + eval_calls |
| D6 | **Diversity pool** — small beam of per-test winners (+6–11% vs greedy at equal budget) | det | ✅ `pool_size` beam |
| D7 | **Joint rule+example optimization** (MIPRO/DSPy blueprint) — edits induced guidance *and* worked examples; invariant layer frozen | det + LLM | ✅ proposer contract (skill); driver text-agnostic |
| D8 | **`cli optimize-adapter`** — live loop; writes the winner to `<slug>.optimized.md` for review (never overwrites canonical — human folds edits into profile.yaml + re-export) | det | ✅ `cli optimize-adapter` + `shell_proposer` + `examples/optimize-proposer.sh` + `make_policy_gate`; `--dry-run` |

**D-track status (built 2026-06-14).** The driver + proposer skill are **implemented**:
`optimize_adapter.py` is the budgeted propose→score→keep loop over the A-track primitives — finding #1
held exactly (the only new code is orchestration + an injectable `Proposer`/`AcceptGate`). 7 unit
tests (fakes, no live model) prove: improving variant kept, regressing variant rejected
(assess-before-merge), faithfulness pre-merge gate blocks **before** scoring (zero wasted eval calls),
minibatch screen prefilters cheaply, early-stop on patience, no-candidates→baseline. **D8 live CLI
DONE (2026-06-14):** `cli optimize-adapter <slug>` wires `shell_runner` (live model) +
`shell_proposer`/`examples/optimize-proposer.sh` (additive v1 — the model emits short guidance blocks,
cheap + safe) + `make_policy_gate` (text-level pre-merge: no tool-grant widening, no escalation tokens
in added text); `--dry-run` scores the baseline + lists failing tests. The winner lands in
`<slug>.optimized.md` for **human review** — never overwrites the canonical adapter/profile (the human
folds the winning edits into `profile.yaml` and re-exports, so the full faithfulness+quote+policy gate
runs there). +5 pure unit tests (prompt-build, variant-parse, policy gate).

**Live-proven (2026-06-14, advertising-effectiveness-advisor):** `--dry-run` scored the baseline live
(0.59 / 5 tests, NR-001 weakest at 0.19) and a `--budget 1 --variants 2` run executed the full loop
end-to-end (15 eval calls = 5 baseline + 2×5 candidates, proposer via `claude -p`), gate kept the
baseline → "no gain". That surfaced a real live-usability bug — a **stochastic runner vs a
zero-regression gate**: sampling noise reads as a regression. Fix shipped: **`--tol` (default 0.05)**
absorbs noise-level dips (use 0.0 for a deterministic runner). **`--grader llm` DONE (2026-06-14):**
`cli optimize-adapter --grader llm` wires `make_llm_grader(shell_llm(--judge))` so the loop optimizes
*meaning*, not token-overlap; default `--judge examples/codex-judge.sh` is **cross-family**
(codex/gpt-5.5) because a Claude judge scoring Claude output carries a same-family self-preference
(finding #9). `shell_llm` (a `(prompt)->reply` shell callable) added next to `shell_runner`. Costs one
extra judge call per test — use the coarse grader for cheap smoke runs, the semantic judge for a real
gain verdict.

**Live IMPROVED, end-to-end (2026-06-14, advertising-effectiveness-advisor, `--grader llm`):** the
semantic judge scored the baseline **0.82** (vs the lexical proxy's 0.59 — the proxy was under-scoring
good paraphrased answers) and exposed a *real* gap: **NR-001 = 0.11** (the adapter failed to decline
an out-of-scope "write finished ad creative" request). A `--budget 1 --variants 2` run then went
**0.80 → 0.97 IMPROVED** (15 runner + 15 judge calls): the proposer (claude) appended a *"Scope
refusal and required-inputs gate"* block — refuse finished creative, don't judge advertising blind —
that lifted NR-001 with **zero regressions** (replay gate, tol 0.05) and passed the policy gate; the
codex/gpt-5.5 judge (cross-family) confirmed the win. **This is the contrast that proves the loop:**
the same run under the coarse lexical grader returned "no gain" — only the semantic grader both found
the real failure and rewarded the real fix. Winner landed in `<slug>.optimized.md` for review (the
edit is faithful — matches the adapter's stated scope; next step is the human fold into `profile.yaml`
+ re-export, where the full faithfulness/quote/policy gate runs).

**Round-trip closed + a measured-honesty arc (2026-06-14).** The winning block was folded into the
canonical `profile.yaml` (two `forbidden_behaviours` made procedural; agent_version 0.2.0→0.3.0;
CHANGELOG + provenance entries), re-exported, **validate PASS + quote-scan PASS**. Then the
empirical re-measure bit back: a **single-sample** semantic re-measure of the new v0.3.0 adapter read
**0.27** (NR-001 still 0.11) — a scary contradiction of the in-loop 0.97. Diagnosis via the
**deterministic coarse grader** (no judge): it read **0.56**, ≈ the pre-fold 0.59 — so the *runner did
not regress*; the fold was safe and the swing was **judge variance**. Confirmed: a single cross-family
judge call is **high-variance** (it scored equivalent output 0.82 then 0.27). **Fix:**
`make_llm_grader(llm, samples=K)` aggregates K judge calls (route=majority, components=median) +
`cli optimize-adapter --judge-samples`. Re-measuring v0.3.0 with **`--judge-samples 3`** gave a clean
**0.99** (NR-001 **0.11→1.00**) — the fold's gain is real and the round-trip is empirically confirmed.
**Lesson (load-bearing for D8):** n=1 live grading is not trustworthy; use the coarse grader for cheap
in-loop screening and **`--judge-samples ≥3` for any verdict**. The harness kept the result honest —
the "win" only survived once the *measurement* was made reproducible. **Tempered by F6 (calibration
research):** `--judge-samples` median is a *consensus*, and **consensus ≠ human alignment** — it cuts
variance but does not prove the judge tracks humans. The trustworthy verdict still needs a
**human-anchored** guarantee (**B4 gold**) and conformal/soft reliability reporting. A second k6
optimize run (2026-06-14) underlined the *other* axis of variance: baseline stable (0.72/0.73 at
samples-3) but the **per-run optimization yield is variable** — run 1 found a keeper (0.72→0.97), run 2
found none (no variant beat baseline without regression at budget-1/variants-2). The capability is
real; a single small run is not guaranteed to hit, so treat one "no gain" as a miss, not a ceiling.

**Sibling dependency.** D scores against E's suite; the loop is only as good as the tests. Build order:
**E first (objective), then D (optimizer).** Both are single-turn for now (E's G2 multi-turn coverage
gap is deferred). Foundational canon (APE/OPRO/DSPy/TextGrad/GEPA/MIPRO) was assembled by direct
arXiv-ID injection under the recency-lock ([[arxiv-index-recency-locked]]) — a discovery limit, not a
literature gap.

## F. calibration-abstention → Step 13 (the ask-gate)
Research **done** (`docs/Research/calibration-abstention/`, 31 papers, PASS 1.0). Full spec:
`step-13-ask-gate.md`. Gives the *method* for when an advisor answers vs asks vs abstains — the
behaviour Step-11 `missing_context_tests` already probe and `behaviour_replay` `must_ask_for` already
scores. Mostly **refinement of existing steps**, not a new pipeline.

| # | change | det / LLM | status |
|---|---|---|---|
| F1 | **Deterministic ask-gate core** — selective prediction = threshold τ on a calibrated risk score (act iff risk ≤ τ); not entropy/verbalized-confidence alone (confidently-wrong) | det | spec |
| F2 | **Three-action Answer/Ask/Abstain + uncertainty attribution** (data→ask, model→abstain) | LLM planner | spec |
| F3 | **Two-axis `must_ask_for` scoring** — reward ONE specific missing-variable question; penalize over-asking (nonmonotonic) | det grader ext | ✅ **realized via existing graders** — MC test rewards asking, twin rewards answering + `must_not_do` forbids over-asking |
| F4 | **Answerable-twin tests** — pair each missing-context cell with an answerable variant; twin must NOT trigger asking | det gen ext | ✅ `gen_behaviour_tests` twins + `twin_of` (schema); closes the open E follow-on |
| F5 | **Two-stage gate** — cheap deterministic pre-filter on every request → escalate only flagged-uncertain to the LLM planner (Trust-or-Escalate); pre-generation, not output-refusal | det + LLM | spec |
| F6 | **Judge-trust tie-in** — the SAME calibration math governs trusting an LLM-judge verdict: consensus ≠ human alignment; a single verdict needs a conformal/human-anchored guarantee | (analysis) | ✅ folded into the judge note below + B4 |

**F6 is the load-bearing cross-link.** calibration finding #6/#7 says inter-judge **consensus ≠ human
alignment** and a single judge verdict is trustworthy only under a calibrated/conformal or
**human-anchored** guarantee. So Step-12's `--judge-samples` median (a consensus) is **necessary but
not sufficient** — it cuts variance, it does not prove the judge tracks humans. This **promotes B4
(human gold) from "capstone" to "the missing anchor"** and points the eval at proper reliability
reporting (sensitivity/specificity, Youden's J, conformal/soft Elo). It also means a separate
*judge-eval-reliability* research run is now **largely redundant** (calibration covered it). Open
ACADEMIC gaps (non-blocking): deterministic missing-context detection for **black-box** models, and
**multi-turn** ask-gates.

## G. rag-graphrag → Step 14 (runtime retrieval) — §20 #10, post-v0
Research **done** (`docs/Research/rag-graphrag/`, 20+ papers, PASS 1.0). Full spec:
`step-14-runtime-retrieval.md`. The long-open §20 topic #10 (RAG/GraphRAG), and the answer to the
*distill-vs-retrieve* architecture question for `knowledge_partition`. **Post-v0 design capture** — a
runtime knowledge layer for generated agents; nothing built yet, and 3 core questions are open in the
literature.

| # | finding → factory direction | det / LLM | status |
|---|---|---|---|
| G1 | **knowledge_partition = deterministic routing**, not either/or — distill stable/high-reuse/non-citable, retrieve volatile/long-tail/large/citable | det | spec |
| G2 | **Default retrieval spine is deterministic** — hybrid dense(λ≈0.8)+BM25 → distilled cross-encoder reranker; LLM only builds the index | det | spec |
| G3 | **Passage-grounded graph** — PPR traversal, **always return real source passages**, route global queries to a precomputed-summary path; graph aids retrieval, never replaces the corpus | det | spec |
| G4 | **Selective retrieval gate** — uncertainty/complexity threshold + hard ≤3-iter cap (same shape as the Step-13 ask-gate) | det | spec |
| G5 | **Generate-then-cite grounding**, scored on precision **AND** coverage with a deterministic verifier loop | det + LLM | spec |
| G6 | **Distill at index time** (precompute summaries/community reports) to keep runtime cheap | det + LLM | spec |

**Why it stays a spec (3 inherent gaps).** Unlike other topics, the literature does **not** contain
the factory's exact case, so these are unclosable by more rounds (round-3 was rate-limited on Copilot,
but the gaps are inherent): **no paper compares an agent's OWN distilled principle store vs runtime
retrieval** (G1), **principle/argument-graph retrieval is unstudied** (G2), **graph-native per-claim
citation is open** (G3). So any partition/retrieval policy ships **behind a per-package measurement**,
not as a global default — the factory would be charting new ground. Distinct from Step 7
(authoring-time graph build); this is *retrieval over that store at answer time*, and it pairs with the
Step-13 ask-gate (the retrieval gate is the same selective-prediction shape).

## H. table-extraction → Step-20 (table-structure preservation) — §20 #2 — ✅ COMPLETE
Research **done** (`docs/Research/table-extraction/`, PASS 1.0). Spec: the **table-structure
preservation** section in `step-20-document-ai-pdf-parsing.md`. The default fast path still flattens
tables to Markdown (born-digital speed), but the **opt-in** flag now preserves them end-to-end: TSR →
span-preserving `<table>` HTML → `-t` anchors → caption association → degeneracy quality gate. Folds
the measured win (structure-preserving conversion 94.1% vs 86.2% downstream QA; ~33 pp on
table-dependent questions). Especially load-bearing for quantitative domains (finance —
[[financial-domain-readiness]]). H1+H2+H3 shipped; H4 (route-by-table-type) / H5 are subsumed —
Docling's TSR already handles the routing internally.

| # | finding → factory direction | det / LLM | status |
|---|---|---|---|
| H1 | **Keep TableFormer TSR output; persist span-preserving (OTSL/HTML), Markdown as human view only** | det | ✅ **done + live-validated** — parts 1 (opt-in flag) + 2 (`_tables_to_html`) + 3 (`inject_anchors` `-t`); real Kafka-benchmark PDF: 11 tables → 11 `<table>` → 11 `-t` anchors, PASS. Flag-gated, default byte-unchanged |
| H2 | **Caption↔table/figure association** by proximity + reading order | det | ✅ **done** — `inject_anchors._table_caption` seeds a preceding `Table N`/`Figure N` caption into the `-t` anchor text (reading-order, no spatial coords — only linearized Markdown available); inert when absent. 4 tests |
| H3 | **Quality-gate** extracted tables; route low-confidence to review | det | ✅ **done** — `table_quality.table_quality` structural-degeneracy heuristic (no rows/cells, header-only, single column, ≥60% empty) + `convert_pdf._table_warnings` per-table WARN. **Not** TEDS/GriTS (need ground-truth grid); advisory, never blocks. 12 tests |
| H4 | **Route by table type** — line-based for clean ruled, deep TSR otherwise | det | spec |
| H5 | **(ENGINEERING-HIGH, buildable)** wire TableFormer's structured output into the converter contract so claim extraction reads tabular facts | det | spec — build first |

**Open gaps (carried, non-blocking):** caption↔table association lacks an accuracy benchmark
(ACADEMIC); TSR generalization to non-scientific technical books under-evaluated (ACADEMIC). Ships
behind a per-package table quality gate. This is the §20 #2 (Document AI) slice — the rest of #2 is
already shipped as Step 20.

## I. automated-program-repair → Step-6 (patch generation + validation) — §20 #13 — ✅ ENGINE BUILT
Research **done** (`docs/Research/automated-program-repair/`, **41 papers, 3 rounds, validation PASS
1.0, reviewer-accepted**). (The Copilot run hit the hourly rate limit *after* completing — an earlier
"provisional" read was off a stale `round_state.json`; the SUMMARY confirms it validated.) Spec: the
**patch generation + validation** section in `step-6-patch-safety.md`. Step 6 enforces patch *safety*
(mode-gated); this adds *generation + validation* for the produce/patch-suggest modes + the
patch-capable subagents (incl. the new `legacy-code-change-advisor`).

| # | finding → factory direction | det / LLM | status |
|---|---|---|---|
| I1 | **Deterministic validation ladder** — compile/parse → scope → reproduction(fail→pass) → regression(pass→pass) → CI | det | ✅ **done** — `validate_patch.validate_patch` runs the rungs in order, short-circuits, returns pass/fail/needs_human |
| I2 | **Reference-free oracle rungs** — intent oracle, behavioral-fingerprint diff, sound symbolic-equivalence for small in-scope changes | det + LLM | spec — only the structural over-edit proxy (→ I5) built; the oracles are LLM/academic |
| I3 | **LLM never overrides the deterministic verdict** — it only ranks passing candidates + raises abstain/needs-human | det gate + LLM rank | ✅ **done** — `select_patch` keeps only `pass` candidates; ranker only orders them, out-of-set pick ignored |
| I4 | **RED bug-reproduction test** — generate + protect (no-delete), reachability filter, flag fix↔test overfitting | det | ✅ **partial** — reproduce rung enforces fail→pass (`shell_runner`); generation/protection/overfitting-flag carried (live harness) |
| I5 | **Bound the diff by construction** — minimal-edit, function scope, reject over-edits | det | ✅ **done** — `check_scope` (allow/deny paths + max files/hunks/changed-lines); AST function-scope carried |
| I6 | **(ENGINEERING-HIGH)** a `validate_patch` ladder for produce/patch-suggest modes | det | ✅ **done** — `tools/subagent_factory/validate_patch.py` + CLI + 29 tests |

Load-bearing principle matches the factory: **deterministic gate decides, LLM proposes + ranks.**

## J. domain-adaptation-regulated-advice → Step-15 (domain-adaptation policy) — answers Q1
Research **done** (`docs/Research/domain-adaptation-regulated-advice/`, 25 papers, PASS 1.0, 2 rounds).
Full spec: `step-15-domain-adaptation-policy.md`. The concrete answer to **Q1** (can the factory author
finance/stock — and legal/medical?). See memory `financial-domain-readiness`.

| # | finding → factory design | det / LLM | status |
|---|---|---|---|
| J1 | **GRADED no-advice boundary** (safe-completion, not binary; per-domain-risk, reconfigurable) → `forbidden_behaviours` | det template | spec |
| J2 | **Target the safety↔over-refusal frontier** — max-refusal blocks legitimate Qs | det | spec |
| J3 | **Defer-to-professional = server-side τ uncertainty-abstention gate** → `handoff_rules` (same shape as Step-13 ask-gate) | det | spec |
| J4 | **Don't trust model self-confidence** (worst-calibrated on law/medicine) — externally grounded τ | det | spec |
| J5 | **Evidence norms = retrieval-from-authority + mandatory citations** → `source_of_truth_policy` (ties Step-14) | det + LLM | spec |
| J6 | **METHOD (Q1 answer): hybrid** — deterministic per-domain template for `forbidden_behaviours`/disclaimers + LLM interrogation ONLY for evidence norms; prompt-only scope control is unstable | det + LLM | spec |
| J7 | **Liability: human-in-loop "decision support, not replacement"** standing disclaimer/handoff default | det | spec |

**Open gaps (not in arXiv → manual regulatory review, not a round):** personalized-vs-general advice
*detection*, disclaimer legal efficacy / liability allocation, a finance/legal graded-scope benchmark.
Generalizes finance → legal/medical (same graded-boundary + τ-deferral + authority-grounding shape).
Ties: Step-13 (τ), Step-14 (authority retrieval), `evidence-protocol` per-domain override,
`untrusted-source-policy` (the deferral signal is an attack surface).

## K. systematic-review-evidence-synthesis → Step-16 (evidence grading) — §20 #1
Research **done** (`docs/Research/systematic-review-evidence-synthesis/`, 30 sources, PASS 1.0, round 1,
no open HIGH academic). Full spec: `step-16-evidence-grading.md`. Makes the factory's ad-hoc
`confidence: high|medium|low` a principled **GRADE-style** assignment. The connective-tissue track —
it generalises calibration + judge-replication + Step-7 into one confidence layer.

| # | finding → factory design | det / LLM | status |
|---|---|---|---|
| K1 | **Semantic-judgment / deterministic-arithmetic split** is the spine (= the factory's existing rule) | det + LLM | spec |
| K2 | **GRADE-style confidence** — baseline by source type, down for RoB/inconsistency/conflict, up for replication, clamp | det | ✅ `grade_confidence` fn + **wired**: optional `grade` block in principles-v1, `validate_confidence_grade` gate (confidence == grade level; validate-if-present, non-breaking), principle-promotion skill updated |
| K3 | **Inclusion gate** = numbered criteria → deterministic sum → keep/review/discard | det + LLM | ✅ **already satisfied** by `score_extracted_units` (Phase 2.5 importance ranking) — research confirms the existing design |
| K4 | **RoB = advisory weight, NOT a gate** (LLM RoB ~42% F1; human ceiling κ=0.40) | det | spec |
| K5 | **Conflict = reground + abstain, not average** (dual judges → verification label) = Step-7 multi-truth | det + LLM | spec |
| K6 | **Never raw single-model self-confidence** (ECE up to 0.79); ensemble + pin + verbatim provenance; calibrated abstention + an "insufficient evidence" grade | det + LLM | spec |

**The unifying lesson:** the headline negative — automated risk-of-bias is weak — keeps RoB advisory.
K6 explains *why* the n=1 judge was unreliable (Step-12 finding) and generalises `--judge-samples`
(ensemble/pin/repeat). Ties: `evidence-protocol`, Step-3 (verbatim span), Step-13 (abstention), Step-7
(conflict), claim-recall (source impact non-linear).

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
5. ✅ **E (Step 11)** — behaviour-test generator (det core + schema + coverage gate + LLM ideator). The *objective*.
6. ✅ **D (Step 12)** — optimize-adapter driver + proposer skill + **live CLI (D8)**
   (`cli optimize-adapter`, additive proposer, policy gate, winner→review file). Live-proven on 2 packages.
7. ✅ **F (Step 13) research folded** — calibration-abstention → ask-gate spec + judge-trust cross-link (F6).
8. **B4** — independent gold set (human data work). **Promoted to #1 priority by F6** (consensus ≠ human;
   the missing anchor for trusting any LLM-judge verdict). **← the highest-value remaining work.**

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
