# Subagent Workflow Quality Enhancement — Feasibility Assessment

**Date:** 2026-06-10
**Companion to:** `docs/subagent_workflow_quality_enhancement_plan.md`
**Purpose:** Evaluate each proposed enhancement against the actual implementation in this repository, and state what must change in the plan before it is built.

---

## 1. Summary

All twelve proposed enhancements are feasible against the current codebase. Nothing in the code blocks the plan. Two of them are already largely built, several are low-cost wire-ins onto existing machinery, one should be deferred, and the plan is feasible **after two structural fixes** (Section 4).

The plan's main weakness is not its direction — it is that it (a) treats roughly half its proposed `tools/*.py` modules as deterministic when they are LLM judgment, and (b) lists new artifacts as files rather than schema-plus-validator, which is how enforcement actually works here.

---

## 2. How the factory actually runs

There is no phase-orchestrator. The "phases" in `docs/subagent-authoring-process-cycle.md` (Phase 1–12) are realized as three separate mechanisms:

- **Deterministic `tools/` commands**, chained through the CLI:
  `ingest → score → selfcheck → export → validate` (plus `extract-sample`, `search`, `stubs`, `doctor`, `bootstrap`).
- **LLM work as skills + agents:** `source-interrogation` (Q1–Q18) → `profile-deriver` → `profile-reviewer`.
- **One composite gate:** `validate_generated_package.py` chains every deterministic check — schema validators (metadata, manifest, anchor index), the source-provenance cross-check, the Phase-8 self-check, and `quote_scan`. New gates attach with import + call + append-finding.

**Consequence for feasibility:** "add a phase" means add a skill/agent (for judgment), add a deterministic validator + schema (for enforcement), and wire the validator into the composite gate. It does **not** mean extending a DAG engine — there is none, and none is needed. This makes most enhancements cheap to attach.

### Existing machinery the plan can reuse

| Capability | Where it lives | What it already does |
|---|---|---|
| Importance ranking | `score_extracted_units.py` | 9 dimensions × 5 = `/45` total, with a fixed keep/review/discard decision rule (keep ≥ 32, or strong risk/actionability/authority). |
| Field → source traceability | `provenance-ledger-v1.schema.json` (`distillation_log`) | Maps each profile field → `source_ids` + `qids` + notes. |
| Source-text comparison | `quote_scan.py` | Loads restricted source Markdown (`sources/markdown/<id>.md`), whitespace-normalizes it, and substring-matches generated output against it (40-word threshold). The source text is present in-repo; rights restrict *emitted* quotation, not internal comparison. |
| Deterministic / LLM split | `profile_self_check.py` | 18 checks; judgment-heavy ones (mode evidence #4, forbidden-behaviour traceability #12, unresolved-conflict #17) are emitted as INFO and **delegated to the `profile-reviewer` agent**. |
| Platform/instruction leak guard | `profile_self_check.py` check #15 | Fails the gate if the neutral core contains `mcpservers`, `permissionmode`, `disallowedtools`, `.claude`, `claude-code`, etc. — a partial adapter-policy / injection guard. |
| Tool-permission gating | `export_claude_agent.py` `_determine_tools` | Read-only roles default to `Read, Grep, Glob`; only `produce`/`patch-suggest` modes add `Edit, Write`. |
| Mode-by-mode evidence + gaps | `source-interrogation` Q1–Q18, `interrogation-records.yaml` | `rights_status` header, per-mode evidence rule, and an `evidence_gaps:` field. |
| Multi-source conflict log | `merge-conflict-log.md` (e.g. `java-concurrency-reviewer`) | Records merge conflicts when 2+ sources are combined. |
| Test harness | `golden-tests.yaml`, `negative_routing_tests`, self-check #18, `run_tests.py` | Counts and requires 3+ golden tests and 1+ negative routing test. |
| HTML/URL ingestion | `fetch_url.py`, `convert_html.py` | Entry point where a sanitize step would hook. |
| Anchoring | `inject_anchors.py` (`source_anchor_v1`) | Emits heading / figure / code-block / page anchors. **No sentence-span granularity.** |

---

## 3. Per-enhancement feasibility

| # | Enhancement | Code reality | Verdict |
|---|---|---|---|
| 1 | Evidence Protocol | Partly exists: `ingest --rights`, `.claude/rules/rights-and-quotation-policy.md`, interrogation `rights_status` + `evidence_gaps:`. Missing: research_question / inclusion / exclusion / confidence-scale as a structured artifact. | **Feasible, low cost** — one repo rule + thin per-package file + validator. Most of it is global, not per-subagent. |
| 2 | Source Structure Mapping | None today, but `inject_anchors` heading/page anchors already give a skeleton to derive a map from. Density classification is LLM judgment. | **Feasible, medium** — new skill + map schema + validator. Value is real only for long books. |
| 3 | Candidate Unit Extraction | Conceptually present: Phase 2.5 and `score_extracted_units` already operate on "candidate units"; the extraction step is currently implicit inside interrogation. | **Feasible, medium** — formalize as an LLM step producing `units.jsonl` + a schema validator. |
| 4 | Atomic Claim Extraction | None. This is the core new layer. Pure LLM judgment. | **Feasible** — must be a skill/agent, not a deterministic `.py` (see Section 4, fix 1). |
| 5 | Evidence Card Construction | Redundant with `provenance-ledger` `distillation_log` (field → source/qid). `quote_allowed` is derivable from `rights_status`. | **Feasible — extend the ledger schema, do not fork `evidence-cards.yaml`.** |
| 6 | Improve Importance Ranking | Already built: `score_extracted_units` is a 9-dimension `/45` scorer with a decision rule. The plan's nine dimensions match the existing ones. | **Largely done** — the only change is the scored object (unit → claim). |
| 7 | Principle Promotion | None, but maps cleanly onto the existing keep/review/discard pattern and `knowledge_partition`. | **Feasible, medium** — LLM selection step + deterministic promotion-criteria validator + `principles.yaml`. |
| 8 | Principle Graph Merge | `merge-conflict-log.md` exists (manual). Graph + alias-clustering is heavy LLM/ontology work, and almost every package is single-source today. | **Feasible but high cost, lowest ROI — defer** until multi-source packages are common. |
| 9 | Evidence Faithfulness Check | Source text is available at gate time (`quote_scan` already loads it); the composite gate is the wire-in point; the INFO-delegate pattern is the implementation template. | **Feasible, high value** — LLM strength-compare (profile field vs source span) + deterministic recorder + gate wire. Localization is section-level until anchors go finer. |
| 10 | Prompt-Injection / Untrusted-Source Defense | Partly exists: self-check #15 already blocks tool-grant/instruction tokens in the core; `fetch_url`/`convert_html` are the sanitize hook; the scan itself is a `quote_scan`-shaped regex pass over `sources/markdown`. | **Feasible, low cost** — should land early, not late, because the factory ingests arbitrary documents. |
| 11 | Principle-to-Behaviour Evaluation | Test harness already exists and is enforced (self-check #18, `run_tests.py`). | **Feasible** — same pattern: LLM generates cases, deterministic coverage validator. Depends on #7. |
| 12 | Patch Safety Contract | Partly exists: `_determine_tools` gates tools by mode; `may_edit_canonical` is enforced (self-check #10); `forbidden_behaviours` is required. | **Feasible, low-medium** — add `patch-policy.yaml` + validator + patch-safety tests. |

**Buckets:** already built or near-done — #6, and parts of #5, #10, #12. Low-cost wire-ins — #1, #9, #10, #11. New but feasible subsystems — #2, #3, #4, #7. High-cost / defer — #8.

---

## 4. Structural fixes the plan needs before build

### Fix 1 — Re-home the LLM modules out of `tools/`

Roughly half the modules listed in the plan's tooling section are LLM judgment, not deterministic Python: claim extraction, candidate/claim classification, conflict detection, principle clustering, faithfulness checking, unsupported-rule finding, eval-case generation, and density classification. Repository law (`CLAUDE.md`) is that `tools/` holds deterministic scripts; LLM work runs as **skills and agents**.

The correct pattern already exists in `profile_self_check.py`: do the deterministic part in `tools/`, emit judgment items as INFO, and delegate them to an agent (`profile-reviewer`). Every proposed module must be split the same way:

- **Deterministic `tools/` half** — schema validation, deduplication, score arithmetic, coverage counting, regex/substring scanning, gate wiring.
- **LLM skill/agent half** — extraction, classification, semantic strength comparison, conflict reasoning, test-case authoring.

Without this split the plan's `tools/` list is mis-architected and would stall on the first "deterministic" module that cannot be made deterministic.

### Fix 2 — Express every new artifact as schema + validator, wired into the gate

Every artifact in the repo has a `vN.schema.json` and a `validate_*.py`, and is chained into `validate_generated_package.py`. An artifact with no schema is unenforced and therefore dead weight. For each new artifact the plan must name: the schema, the validator, and the line in the composite gate where it is checked — and it should **extend existing artifacts** (`provenance-ledger`, `score_extracted_units`, `quote_scan`) rather than fork parallel machinery.

---

## 5. Additional constraints to respect

- **Anchoring is coarse.** Anchors are heading/figure/code/page level only. Any enhancement that wants exact-sentence source pinning (faithfulness spans, claim → exact line) is limited to section granularity unless `inject_anchors` is extended to sentence anchors — feasible, at the cost of a larger anchor index.
- **Cost is real.** Most packages have a single source; the hardening campaign runs 165 PDFs at five per round. Adding claims + evidence + principles (+ graph + faithfulness) per source multiplies LLM passes. The work is technically feasible but should be **tiered**: single short sources take a light path (current pipeline + injection scan + faithfulness); multi-book sources take the full claim/principle/graph path.

---

## 6. Bottom line

The enhancement plan is sound and feasible. Recommended order, adjusted for risk-weighted value:

1. **Now:** prompt-injection scan + adapter-policy scan (#10), faithfulness check anchored to source text (#9). Both are low-cost wire-ins onto existing gate/source-comparison machinery and address safety and the main LLM failure mode (rules stronger than evidence).
2. **Next:** formalize claim extraction (#4) on top of the existing candidate-unit scoring (#3, #6); extend the provenance ledger to carry evidence-card fields (#5); add principle promotion (#7) and the evidence protocol (#1).
3. **Later, multi-source only:** principle graph and conflict merge (#8); principle-to-behaviour tests (#11) once principles exist; patch-safety contract (#12).

Apply Fix 1 and Fix 2 throughout, and the project moves from "generates structurally valid subagents" to "manufactures evidence-grounded expert subagents" without redesign.
