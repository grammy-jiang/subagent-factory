# Step 11 — Behaviour-Test Generation (profile-spec → high-coverage adversarial suite)

> Folds `docs/Research/behaviour-test-generation/` (41 papers, validated PASS) into an executable
> spec. This is the **E-track** of `research-integration-plan.md`. It generates the *objective* that
> Step 12 (optimize-adapter) tunes against — so it lands first.

**Goal** — From a package's `profile.yaml` + `principles.yaml`, generate a **high-coverage,
adversarial** behaviour-test suite (`tests/*.yaml`) spanning three categories — **golden** (the
expert does its job), **negative-routing** (out-of-scope inputs are refused/handed off), and
**missing-context** (underspecified inputs trigger ask/abstain, not a silent commit) — with a
deterministic coverage gate proving every principle is exercised across the matrix.

## Relationship to Step 5

Step 5 (`principle-behaviour-tests`) guarantees **referential coverage**: each principle maps to ≥1
test. Step 11 is the **adversarial breadth** layer on top: it instantiates a *capability × test-type
matrix* so each principle gets golden **and** negative-routing **and** missing-context probes, and it
adds a coverage-guided keep-if-new loop so the suite is diverse, not redundant. Step 5 stays the
floor; Step 11 raises the ceiling. They share the **same** runtime — `behaviour_replay` —
because the generated tests reuse the existing `golden-tests-v1` field set.

## New files

| Path | Kind | Purpose |
|---|---|---|
| `schemas/golden-tests-v1.schema.json` | schema | **Close the unschematized gap** — `golden-tests.yaml` / generated suites are currently schema-exempt. Type the fields (`test_id`, `prompt`, `expected_route ∈ {invoke,decline}`, `expected_mode`, `must_ask_for[]`, `minimum_output`, `must_not_do[]`) + a new optional `test_type ∈ {golden, negative-routing, missing-context}` and `principle_ref`. |
| `.claude/skills/behaviour-test-generation/SKILL.md` | skill (LLM) | The generation procedure: build the matrix, ideate inputs per cell, apply metamorphic relations, instantiate typed templates, run the coverage loop. |
| `tools/subagent_factory/gen_behaviour_tests.py` | tool (det + LLM-hook) | Deterministic scaffold: build the principle×type matrix, instantiate typed templates from LLM-ideated slots, dedup by embedding (reuse `embed_minilm`), emit schema-valid YAML. |
| `tools/subagent_factory/validate_behaviour_test_coverage.py` | tool (validator) | Coverage gate: every principle exercised by ≥1 of each required test_type (tier-gated); schema-valid; oracle well-formedness (a `negative-routing` test must set `expected_route: decline`; a `missing-context` test must populate `must_ask_for`). |
| `tests/subagent_factory/test_gen_behaviour_tests.py` | fixtures | Generator + validator unit tests. |

## Reuse (build on, do not duplicate)

- **`behaviour_replay.load_behaviour_tests` / `grade_output`** already score `expected_route`,
  `must_ask_for`, `minimum_output`, `must_not_do`. Generated tests are therefore **immediately
  runnable** by the existing engine and by Step 12 — no new runtime.
- **`embed_minilm`** (`seed_principle_clusters`) — reuse for the anti-collapse dedup (drop a candidate
  whose embedding is within cosine τ of an accepted one).
- **`golden-tests-v1` field set** — the three categories are *encodings of existing fields*, not new
  ones: golden ⇒ `expected_route: invoke` + `minimum_output`; negative-routing ⇒
  `expected_route: decline` + `must_not_do`; missing-context ⇒ `expected_route: invoke` +
  `must_ask_for` non-empty, paired with an answerable twin.
- **`principles-v1`** — the matrix rows are the promoted principles; `principle_ref` links back.

## LLM ↔ deterministic split

| Deterministic (tools/schema/gate) | LLM (skill) |
|---|---|
| Build principle×type matrix; enumerate empty cells | Ideate the test *input* per cell (hard-negative OOS prompt, slot-ablated underspecified prompt) |
| Typed-template instantiation → reproducible YAML | Expand a seed prompt into K diverse paraphrases |
| Schema validation + oracle well-formedness | Draft the instance-specific `minimum_output` / `must_not_do` checklist |
| Embedding dedup + coverage gate (FAIL) | Propose metamorphic perturbations (invariance / directional) |
| Coverage-guided keep-if-new (rare-weighted) | — |

Discipline (unchanged): the LLM only *proposes* candidates; a deterministic gate (schema + coverage +
dedup) decides what lands. Golden tests stay deterministic (typed templates, fixed wording) so the
objective Step 12 optimizes against is **stable**.

## Research inputs (findings → spec, with paper IDs)

1. **Capability × test-type matrix is the ideation scaffold** — rows = principles, cols = golden(MFT)/
   negative-routing(DIR)/missing-context; Cartesian-expand to emit `tests/*.yaml`. *[2005.04118],
   [2312.06056], [2307.05454], [2402.10899]*
2. **Hybrid generation** — LLM ideates/expands for scale; deterministic typed templates instantiate
   for reproducible, computable oracles. *[2307.05454], [2408.17437], [2605.25101], [2503.06648]*
3. **Metamorphic relations = label-free oracles** mapped to categories: invariance→golden-invariance,
   directional→negative-routing, set/distance→missing-context. *[2603.23611], [2312.06056],
   [1809.01266], [2005.04118]*
4. **Negative-routing = in-scope/OOS + hard-negative generation** — declare profile capabilities
   in-scope; generate hard-negative OOS via keyword-constrained generation + spec-structural
   negatives; golden behaviour = fallback/refuse; **score OOS-recall-first**. *[1909.02027],
   [2403.05640], [2507.01541]*
5. **Missing-context = spec-inversion / slot-ablation** — delete one decision-relevant element from a
   complete profile-derived item, pair with its answerable twin; golden behaviour = ask/abstain,
   graded on two axes (**silent-commit vs over-ask**). *[2605.09698], [2405.12063], [2308.13507],
   [2512.04597]*
6. **Coverage-guided keep-if-new with rare-weighting & anti-collapse** — keep only tests reaching a
   new behaviour bucket, weight toward rare behaviours (TF-IDF), early-stop; naive LLM mutation
   *without* coverage feedback **reduces** diversity. *[1809.01266], [2402.12222], [1911.01952],
   [2402.19464], [2406.08665]*
7. **Oracle = instance-specific, atomic-binary, independently-judged, evidence-grounded, locked
   checklist** — generic rubrics can score *below* no rubric; instance-specific binary checklists let
   a cheap judge match a frontier judge; validate on a human-majority subset. *[2503.05142],
   [2602.05125], [2601.08654], [2402.04249]*
8. **For agents, grade the trajectory pre-execution** — fail any run emitting a tool call on an
   unanswerable/underspecified input even if it executes; answerability-gating beats sampling-based
   uncertainty; release tests behind a context-ablation/shortcut-validation gate. *[2410.13886],
   [2601.10398], [2605.09698], [2512.04597]*

## Gate wiring

`validate_behaviour_test_coverage.py` registers in `validate_generated_package.py`, **present-gated +
tier-gated**: WARN if absent; once a package ships a Step-11 suite, FAIL on (a) schema-invalid test,
(b) a principle with no golden test, (c) an oracle-shape violation (negative-routing without
`expected_route: decline`, missing-context without `must_ask_for`). Tier-0's 15 packages keep passing
(they have no Step-11 suite → WARN only). Mirrors the A4/Step-5 present-gate discipline.

## Fixtures

- A 2-principle profile → expect 6 cells (2 × {golden, neg-routing, missing-context}); generator emits
  ≥6 schema-valid tests; coverage validator PASS.
- A suite missing the negative-routing cell for one principle → validator FAIL with that principle id.
- A missing-context test lacking `must_ask_for` → oracle-shape FAIL.
- A redundant candidate (cosine within τ of an accepted test) → dropped by dedup.

## Exit criteria

- `python -m tools.subagent_factory.gen_behaviour_tests subagents/<slug>` emits a schema-valid suite.
- `python -m tools.subagent_factory.validate_behaviour_test_coverage subagents/<slug>` PASS on a
  matrix-complete suite, FAIL on a hole.
- All 15 Tier-0 packages still validate (present-gate proven non-breaking).
- `make verify` green.

## Caveats (validate-ourselves)

- **G2 (open, ACADEMIC MED):** no coverage notion over *multi-turn / trajectory* tests — Step 11 is
  single-turn. Multi-turn deferred.
- **G3 (open, ACADEMIC MED):** no validated persona-rule *mutation score*; adequacy is proxied by
  matrix-cell fill + embedding diversity, not a true adequacy metric.
- **Oracle reliability:** metamorphic-relation false-positive rates run 0–70% in the literature →
  keep golden tests on typed templates, use MR only as *candidate* generator, gate with the
  instance-specific binary checklist.
- arXiv recency-lock: corpus assembled by relevance-repaired search + ID injection ([[arxiv-index-recency-locked]]).

## Risks

- *LLM ideation drifts off-spec* → typed templates + schema + coverage gate bound it; LLM never writes
  YAML directly.
- *Generated suite is redundant* → coverage-guided keep-if-new + embedding dedup (finding 6).
- *Over-ask regression* (missing-context tests reward asking, could teach over-asking) → the
  answerable twin (finding 5) penalizes asking when context **is** sufficient; both axes graded.
