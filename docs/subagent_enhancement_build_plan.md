# Subagent Factory Enhancement — Consolidated Build Plan

**Date:** 2026-06-10
**Status:** Implementation-ready. This is the single source of truth for the quality-enhancement work.
**Supersedes for planning purposes:**
- `docs/subagent_workflow_quality_enhancement_plan.md` (original direction; 12 enhancements)
- `docs/subagent_workflow_quality_enhancement_feasibility.md` (feasibility vs code)
- `docs/subagent_feasibility_review_comments.md` (external review; doc-only, not code-grounded)

**Goal:** Move the factory from *"generates structurally valid subagents"* to *"manufactures evidence-grounded expert subagents"* — without redesigning the core workflow, and without breaking the 15 existing packages.

> Note on lineage: the external review comments were written against the feasibility document, not the source code. Where those comments use placeholder notation that does not match the implementation (e.g. anchor IDs, a v2 provenance-ledger schema), this plan corrects them against the actual code. Corrections are folded in silently below; the build plan here is the authoritative version.

---

## 1. Grounding — how the factory actually executes

There is no phase-orchestrator or DAG engine. The Phase 1–12 lifecycle in `docs/subagent-authoring-process-cycle.md` is realized by three mechanisms:

1. **Deterministic CLI / tools** (`tools/subagent_factory/`), chained as
   `ingest → score → selfcheck → export → validate` (+ `extract-sample`, `search`, `stubs`, `doctor`, `bootstrap`).
2. **LLM judgment as skills + agents** — `source-interrogation` (Q1–Q18) → `profile-deriver` → `profile-reviewer`.
3. **One composite gate** — `validate_generated_package.py` chains every deterministic check and is the place new gates attach.

**Therefore "add a phase" = add an LLM skill/agent (judgment) + a schema (artifact shape) + a deterministic validator (enforcement) + a wire into the composite gate.** Never a new engine.

### 1.1 Existing machinery this plan reuses (verified in code)

| Capability | Location | Reused for |
|---|---|---|
| Importance ranking: 9 dims × 5 = `/45`, keep ≥ 32 rule | `score_extracted_units.py` | Scoring **claims** (object change only — see §4.5) |
| Source-text load + verbatim match (40-word) | `quote_scan.py` (`_load_source_texts`, `_normalize_ws`, `_is_verbatim`) | Shared source-text loader for injection scan + faithfulness-v0 |
| Deterministic/LLM split via INFO-delegate | `profile_self_check.py` (#4, #12, #17 → `profile-reviewer`) | Template for `faithfulness-reviewer`, `source-safety-reviewer` |
| Tool/permission leak guard on core | `profile_self_check.py` #15 (`mcpservers`, `permissionmode`, `disallowedtools`, `.claude`…) | Baseline for adapter-policy scan (additive, not duplicated) |
| Tool gating by mode | `export_claude_agent.py` `_determine_tools` (read-only default; `produce`/`patch-suggest` → `Edit`,`Write`) | Patch-safety contract foundation |
| `may_edit_canonical` enforcement | `profile_self_check.py` #10 | Patch-safety contract |
| Field → source/QID traceability | `provenance-ledger.md` (Distillation Log table) | Narrative backbone; evidence records reference it |
| Anchors `source_anchor_v1` | `inject_anchors.py` → `sources/anchors/<id>.anchors.jsonl` | `source_anchors` references in claims/evidence |
| Q1–Q18 + `evidence_gaps:` | `source-interrogation` skill, `interrogation-records.yaml` | Upstream input to claim extraction |
| Test harness + counting | `golden-tests.yaml`, `negative_routing_tests`, self-check #18, `run_tests.py` | Principle-to-behaviour coverage |
| HTML/URL ingest | `fetch_url.py`, `convert_html.py` | Hook point for source sanitisation |

### 1.2 Code facts that correct the external review

- **Anchor IDs are `<source_id>-hNNNN` / `-fNNNN` / `-cNNNN` / `-pNNNN`** (heading/figure/code/page). They are **not** `S1#chapter-03` slugs. All `source_anchors` fields must reference real anchor IDs or page numbers so validators can cross-check them against the anchor index.
- **`provenance-ledger.md` is Markdown prose, and `provenance-ledger-v1.schema.json` is currently unenforced** (no validator wires it; the gate only checks the file exists + size > 200, plus a sha256 cross-check). So "extend the ledger schema to v2 to hold evidence cards" does not work as written — there is nothing machine-readable to extend. **Decision in §4.1: evidence records live in a new schema-validated sibling file, not in the Markdown ledger.**
- **`quote_scan` already holds the full source text in-repo** (`sources/markdown/<id>.md`). Rights restrict *emitted* quotation, not internal comparison — so faithfulness checking has the source it needs today.

---

## 2. Design principles (hard rules)

1. **LLM judgment lives in skills/agents; deterministic enforcement lives in tools/schemas/validators/gate.** Extraction, classification, semantic strength comparison, conflict reasoning, and test-case authoring are LLM. Schema validation, parsing, score arithmetic, coverage counting, regex/substring scanning, referential-integrity checks, and gate wiring are deterministic.
2. **No new quality artifact without: a versioned schema, a deterministic validator, composite-gate wiring, and at least one fixture.** A file with no validator is documentation, not enforcement.
3. **Extend existing artifacts before forking new ones.** Prefer `score_extracted_units`, `quote_scan`, the provenance ledger, and the composite gate over parallel machinery.
4. **Tier by source complexity.** Short single-source packages take a light path; long books and multi-source packages take the full claim/principle path (§7).
5. **Safety before intelligence.** Prompt-injection scanning and faithfulness checking land before principle graphs, advanced merge, or any direct-patch automation.
6. **Validators are referential, not just structural.** They check ID cross-references (claim ↔ evidence ↔ principle ↔ test, source_ids ↔ manifest, source_anchors ↔ anchor index), not only that fields are present. This is what gives schemas teeth.
7. **Never break existing packages.** New gate checks are *present-gated and tier-gated*: validate an artifact if present; fail only if the package's tier requires it and it is absent. The 15 current packages are Tier 0 and must keep passing untouched.

---

## 3. Component pattern

Every enhancement decomposes into the same four parts:

```text
LLM skill/agent      → produces the judgment artifact (claims, principles, faithfulness report)
schema               → schemas/<artifact>-vN.schema.json defines its shape + enums
deterministic validator → tools/subagent_factory/validate_<artifact>.py  (structural + referential)
composite gate wiring → one block in validate_generated_package.py (present-gated, tier-gated)
```

Two enhancements are **scans, not artifacts** (they follow the `quote_scan` precedent — a deterministic function returning findings straight into the gate, with no produced file and no schema): `prompt_injection_scan.py`, `adapter_policy_scan.py`.

---

## 4. Resolved design decisions

### 4.1 Evidence records — sibling file, not ledger-v2
Create `subagents/<slug>/evidence/evidence-records.yaml` with `schemas/evidence-records-v1.schema.json` + `validate_evidence_records.py`. The human-readable `provenance-ledger.md` stays as the narrative/Distillation-Log backbone (required by rights policy and depended on by existing packages). Evidence records are the machine layer that binds claims → source → strength.

### 4.2 Anchor granularity — accept coarse now
`source_anchors` reference real `source_anchor_v1` IDs (heading/figure/code/page). Each claim/evidence record carries `support_granularity: section | page | heading`. Sentence/paragraph anchors (`paragraph_anchor_v1`, `sentence_anchor_v1`) are deferred until claim extraction and faithfulness are useful at section/page level.

### 4.3 Faithfulness — two tiers
- **v0 (Step 1):** profile rule vs **raw source text** (reuse the `quote_scan` source loader; LLM strength-compare). No claims required, so it ships in the safety step.
- **v1 (after Step 3):** profile rule vs **evidence record / claim**, for precise "rule stronger than its evidence" findings.

### 4.4 Adapter-policy scan — additive to self-check #15
#15 already fails on tool/permission tokens in the neutral core. The new `adapter_policy_scan.py` targets the **exported adapter file** (`adapters/claude-code/<slug>.md` and the installed copy): explicit tool-grant lines, instruction-injection patterns, and permission escalations. It must not re-implement #15.

### 4.5 Scoring — change the producer, not the scorer
`score_extracted_units.py` is object-agnostic: it validates per-item dimension scores and applies the fixed rule. Claims carry the same nine dimensions, so claim scoring needs no new scorer — only the LLM producer changes (units → claims). Keep the tool; optionally add a thin `score_claims` alias for clarity.

### 4.6 Tiering source
A deterministic `classify_tier.py` computes tier from the manifest (source count) and conversion reports (length), recorded as `tier:` in `profile.yaml`. Default **Tier 0**. The gate reads `tier` to decide which artifacts are required.

---

## 5. Target package layout (tiered)

```text
subagents/<slug>/
├── profile.yaml                     # + tier: field
├── provenance-ledger.md             # unchanged (narrative backbone)
├── source-pack.manifest.yaml
├── CHANGELOG.md
├── sources/ … (original, markdown, anchors, metadata, reports)   # unchanged
├── evidence/
│   └── evidence-records.yaml        # NEW (Tier 1+)  schema: evidence-records-v1
├── analysis/
│   ├── claims.jsonl                 # NEW (Tier 1+)  schema: claims-v1
│   └── claim-importance-scores.yaml # NEW (Tier 1+)  reuses score_extracted_units
├── principles/
│   ├── principles.yaml              # NEW (Tier 1+)  schema: principles-v1
│   ├── conflict-log.md              # existing pattern (merge-conflict-log.md), Tier 2
│   └── principle-graph.json         # NEW (Tier 2 only)  deferred
├── policy/
│   └── patch-policy.yaml            # NEW  schema: patch-policy-v1
├── reports/
│   └── faithfulness-report.yaml     # NEW  schema: faithfulness-report-v1
├── evidence-protocol.yaml           # NEW (optional per-pkg override of global rule)
├── adapters/claude-code/<slug>.md   # unchanged
└── tests/
    ├── golden-tests.yaml            # unchanged
    ├── principle-behaviour-tests.yaml  # NEW (Tier 1+)
    ├── patch-safety-tests.yaml      # NEW (if patch modes)
    └── test-results.md              # unchanged
```

Tier 0 packages (current 15) gain **none** of these and continue to pass.

---

## 6. New components catalog

### 6.1 Skills (LLM)
| Skill | Produces | Notes |
|---|---|---|
| `claim-extraction` | `analysis/claims.jsonl` | Builds on Q1–Q18 + source text |
| `principle-promotion` | `principles/principles.yaml` | Selects high-value scored claims |
| `faithfulness-review` | `reports/faithfulness-report.yaml` | v0 vs source text; v1 vs evidence |
| `principle-test-generation` | `tests/principle-behaviour-tests.yaml` | Maps principles → tests |
| (later) `source-structure-mapping` | `sources/maps/<id>.source-map.yaml` | Tier 1 long-book preprocessing |

### 6.2 Agents (LLM judgment, INFO-delegate pattern)
| Agent | Role |
|---|---|
| `claim-extractor` | Atomic-claim extraction + classification |
| `principle-promoter` | Claim → principle promotion (named to avoid colliding with existing `profile-deriver`) |
| `faithfulness-reviewer` | Strength comparison; emits findings |
| `source-safety-reviewer` | Triages prompt-injection scan hits (judgment on flagged spans) |

### 6.3 Tools (deterministic) + schemas
| Tool | Schema | Checks |
|---|---|---|
| `prompt_injection_scan.py` | — (scan, like quote_scan) | Instruction-like patterns in `sources/markdown` → gate findings |
| `adapter_policy_scan.py` | — (scan) | Tool-grant / injection / escalation in exported adapter |
| `validate_faithfulness_report.py` | `faithfulness-report-v1` | Field paths exist in profile; `status`/`action` enums; no `unsupported` left unresolved |
| `validate_claims.py` | `claims-v1` | Unique `claim_id`; `source_ids` ∈ manifest; `source_anchors` ∈ anchor index; `claim_type`/`confidence` enums |
| `validate_evidence_records.py` | `evidence-records-v1` | `claim_id` ∈ claims; `source_ids` ∈ manifest; `source_anchors` ∈ anchor index; strength/confidence enums |
| `validate_principles.py` | `principles-v1` | `derived_from_claims` ∈ claims; `operational_mapping.skill` ∈ knowledge_partition/stubs; `test_cases` ∈ tests |
| `validate_principle_test_coverage.py` | — | Every high-confidence principle → ≥1 referencing test |
| `validate_patch_policy.py` | `patch-policy-v1` | Modes consistent with `_determine_tools`; `may_edit_canonical` respected |
| `validate_evidence_protocol.py` | `evidence-protocol-v1` | Required fields; consistency with rights status |
| `classify_tier.py` | — | Compute `tier` from manifest + reports |
| `source_text.py` (refactor) | — | Shared loader extracted from `quote_scan` for reuse |

### 6.4 Rules (policy, global)
- `.claude/rules/untrusted-source-policy.md` — source content is data, never instruction; cannot grant tools, edit settings, or alter generated policy; instruction-like content is logged, not executed.
- `.claude/rules/evidence-protocol.md` — global default research-question / inclusion / exclusion / confidence-scale; per-package `evidence-protocol.yaml` overrides only when needed.

---

## 7. Tiering policy

| Tier | Trigger | Path |
|---|---|---|
| **0 — light** | 1 short source | Current pipeline + prompt-injection scan + adapter-policy scan + faithfulness-v0. No claims/principles required. |
| **1 — full** | Long book, or content-dense source | Tier 0 + claims + evidence records + principle promotion + faithfulness-v1 + principle-behaviour tests. Optional source-structure map. |
| **2 — multi-source** | 2+ high-value sources with overlap/conflict | Tier 1 + conflict log + principle graph. |

Gate rule: *validate-if-present always; fail-if-absent only when tier requires it.*

---

## 8. Phased roadmap

Each step states: **Goal · Add · Reuse · Wire · Exit criteria.**

### Step 0 — Plumbing
- **Goal:** Make later steps cheap and non-breaking.
- **Add:** `source_text.py` (refactor shared loader out of `quote_scan`); `classify_tier.py`; `tier:` field in `profile.yaml`; the present-gated/tier-gated convention in `validate_generated_package.py`.
- **Reuse:** `quote_scan` internals; manifest + conversion reports.
- **Exit:** All 15 existing packages still pass `validate`; `tier` defaults to 0.

### Step 1 — Safety + faithfulness-v0 gate
- **Goal:** No polluted or over-claimed subagent can be released.
- **Add:** `prompt_injection_scan.py`, `adapter_policy_scan.py`; `.claude/rules/untrusted-source-policy.md`; `faithfulness-review` skill + `faithfulness-reviewer` agent + `reports/faithfulness-report.yaml` + `faithfulness-report-v1` schema + `validate_faithfulness_report.py`; `source-safety-reviewer` agent; `.claude/rules/evidence-protocol.md`.
- **Reuse:** `source_text.py`; self-check #15 (adapter scan is additive).
- **Wire:** all into the composite gate (Tier 0+).
- **Exit:** instruction-like source text is flagged + logged; adapter contamination blocks export; rules stronger than source text are flagged; sample fixtures pass.

### Step 2 — Atomic claim extraction
- **Goal:** Move from vague units to atomic, traceable claims.
- **Add:** `claim-extraction` skill + `claim-extractor` agent; `analysis/claims.jsonl`; `claims-v1` schema; `validate_claims.py` (referential).
- **Reuse:** Q1–Q18 + `evidence_gaps`; `score_extracted_units` for claim scoring → `analysis/claim-importance-scores.yaml`.
- **Wire:** gate (Tier 1+).
- **Exit:** claims validate referentially; importance scoring runs on claims.

### Step 3 — Evidence records + faithfulness-v1
- **Goal:** Bind claims and rules to source-backed evidence.
- **Add:** `evidence/evidence-records.yaml`; `evidence-records-v1` schema; `validate_evidence_records.py`. Upgrade faithfulness to compare rules against evidence records.
- **Reuse:** anchor index for `source_anchors`; provenance ledger narrative.
- **Wire:** gate (Tier 1+).
- **Exit:** every promoted claim has ≥1 evidence record; faithfulness-v1 catches rules exceeding evidence strength.

### Step 4 — Principle promotion
- **Goal:** Promote high-value claims into operational principles.
- **Add:** `principle-promotion` skill + `principle-promoter` agent; `principles/principles.yaml`; `principles-v1` schema; `validate_principles.py` (referential).
- **Reuse:** keep/review/discard pattern; `knowledge_partition` for `operational_mapping`.
- **Wire:** gate (Tier 1+).
- **Exit:** every principle traces to claims + evidence; `operational_mapping` resolves to real skills/tests.

### Step 5 — Principle-to-behaviour test coverage
- **Goal:** Principles change runtime behaviour, not just docs.
- **Add:** `principle-test-generation` skill; `tests/principle-behaviour-tests.yaml`; `validate_principle_test_coverage.py`.
- **Reuse:** existing test harness + self-check #18.
- **Wire:** gate (Tier 1+).
- **Exit:** each high-confidence principle maps to ≥1 of {positive routing, negative routing, output-contract, forbidden-behaviour, patch-safety} test.

### Step 6 — Patch safety contract
- **Goal:** A review agent never silently becomes a code-modifying agent.
- **Add:** `policy/patch-policy.yaml`; `patch-policy-v1` schema; `validate_patch_policy.py`; `tests/patch-safety-tests.yaml`.
- **Reuse:** `_determine_tools`; self-check #10 (`may_edit_canonical`); `forbidden_behaviours`.
- **Wire:** gate (all tiers with patch modes).
- **Exit:** default `patch_suggest_only`; direct patch requires explicit-request + bounded scope + validation command; canonical artifacts never silently edited.

### Step 7 — Multi-source (deferred)
- **Goal:** Synthesis when the source base is large enough.
- **Add:** source-structure mapping (Tier 1 long-book preprocessing), candidate-unit formalisation, `principles/conflict-log.md`, `principles/principle-graph.json` (Tier 2 only), clustering/alias/conflict detection (LLM).
- **Defer until:** multi-source packages are common; `principles.yaml` stable; safety + faithfulness gates enforced.

---

## 9. Acceptance criteria for a generated subagent

```text
1.  Every source has metadata, rights status, and a conversion report.        [Tier 0+]
2.  Source content is treated as untrusted: injection scan run + logged.       [Tier 0+]
3.  Adapter is free of tool-grant / instruction contamination.                 [Tier 0+]
4.  No generated rule is stronger than its source support (faithfulness).       [Tier 0+ v0]
5.  tier is set; required artifacts for that tier are present and valid.        [all]
6.  Long sources have a source map.                                            [Tier 1]
7.  Important content is represented as atomic, referential claims.             [Tier 1]
8.  Every promoted principle has ≥1 evidence record.                            [Tier 1]
9.  Every core profile rule maps to a principle or explicit policy.            [Tier 1]
10. Core principles are covered by behavioural tests.                           [Tier 1]
11. Multi-source conflicts are logged, not silently resolved.                   [Tier 2]
12. Patch behaviour is read-only by default unless explicitly authorised.       [all]
13. Phase 8 self-check + composite validation + runtime smoke tests pass.       [all]
14. Maintenance cadence assigned from source volatility.                        [all]
```

---

## 10. Risks & open decisions

- **LLM pass cost** (Tier 1 multiplies passes per source). Mitigated by tiering; revisit budget when the hardening campaign hits long books.
- **Anchor coarseness** limits faithfulness/claims to section/page localisation until paragraph/sentence anchors are added. Accepted for now.
- **Open:** exact `tier` thresholds (page/word counts) — set empirically once `classify_tier.py` runs over the existing corpus.
- **Open:** whether `evidence-protocol.yaml` is ever needed per-package, or the global rule suffices for all current domains.

---

## 11. Two non-negotiable constraints (carry into every step)

1. **LLM judgment belongs in skills/agents; deterministic enforcement belongs in tools + schemas + validators + the composite gate.**
2. **Every new artifact requires a versioned schema, a referential validator, composite-gate wiring, and a fixture — or it does not ship.**
