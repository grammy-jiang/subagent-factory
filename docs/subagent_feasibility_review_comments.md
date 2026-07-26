# Review Comments on Subagent Workflow Quality Enhancement Feasibility Assessment

> **Historical — superseded.** These are review comments on the (also superseded)
> feasibility assessment; the current plan is
> [`subagent_enhancement_build_plan.md`](subagent_enhancement_build_plan.md). Kept for provenance.
> See [`docs/README.md`](README.md) for the full doc map.

**Date:** 2026-06-10  
**Reviewer:** ChatGPT  
**Input reviewed:** `subagent_workflow_quality_enhancement_feasibility.md`  
**Purpose:** Capture review comments on the local AI agent's feasibility assessment and turn them into actionable guidance for updating the enhancement plan.

---

## 1. Executive Summary

The feasibility assessment is sound and useful.

It does **not** reject the previous quality-enhancement direction. Instead, it corrects the implementation strategy so that the plan matches the actual repository architecture.

The key conclusion is:

> The core workflow is valid, and the quality-enhancement direction is valid.  
> However, implementation must respect the repository's execution model:  
> LLM judgment belongs in skills/agents; deterministic enforcement belongs in tools, schemas, validators, and the composite validation gate.

This is an important correction. The previous enhancement plan was conceptually right, but some proposed modules were described as `tools/*.py` even though they require semantic judgment, extraction, classification, or reasoning. Those should not be implemented as deterministic Python tools.

---

## 2. What the Feasibility Assessment Gets Right

The feasibility assessment correctly identifies that the repository does not operate through a formal phase orchestrator or DAG engine.

Instead, the workflow is implemented through three mechanisms:

1. **Deterministic CLI / tools**
   - Examples: ingestion, scoring, export, validation, quote scanning.
   - These should perform repeatable, testable, non-semantic operations.

2. **LLM skills and agents**
   - Examples: source interrogation, profile derivation, profile review.
   - These should handle semantic extraction, judgment, comparison, classification, and reasoning.

3. **Composite validation gate**
   - `validate_generated_package.py` chains schema checks, self-checks, quote scan, provenance checks, and other deterministic validation steps.
   - New quality gates should attach here.

Therefore, when the plan says “add a phase,” the implementation should usually mean:

```text
add a skill/agent for LLM judgment
add a schema for the output artifact
add a deterministic validator
wire the validator into the composite package gate
```

It should **not** mean building a separate phase engine.

---

## 3. Key Correction 1 — Do Not Put LLM Judgment into `tools/`

The feasibility assessment's first structural fix is correct.

The previous plan listed modules such as:

```text
extract_claims.py
classify_claims.py
detect_conflicts.py
cluster_principles.py
grade_confidence.py
generate_eval_cases_from_principles.py
faithfulness_check.py
```

Some of these names are still useful, but their responsibilities must be split.

Many of these tasks are not deterministic:

| Task | Correct location |
|---|---|
| Atomic claim extraction | LLM skill/agent |
| Claim classification | LLM skill/agent |
| Principle promotion | LLM skill/agent |
| Semantic conflict detection | LLM skill/agent |
| Faithfulness comparison | LLM skill/agent |
| Evaluation case generation | LLM skill/agent |
| Source density classification | LLM skill/agent |

The deterministic `tools/` layer should only handle:

| Task | Correct location |
|---|---|
| Schema validation | `tools/` |
| JSON/YAML parsing | `tools/` |
| Score arithmetic | `tools/` |
| Coverage counting | `tools/` |
| Regex-based prompt-injection scanning | `tools/` |
| Quote scanning | `tools/` |
| Adapter-policy scanning | `tools/` |
| Composite gate wiring | `tools/` |

The correct design pattern is:

```text
LLM skill/agent:
  produce judgment artifact

schema:
  define artifact structure

deterministic validator:
  check required fields, IDs, references, coverage, allowed values

composite gate:
  block release if required checks fail
```

### Recommended implementation shape

```text
.claude/skills/
  claim-extraction/
  principle-promotion/
  faithfulness-review/
  evidence-protocol/
  principle-test-generation/

.claude/agents/
  claim-extractor.md
  principle-deriver.md
  faithfulness-reviewer.md
  safety-reviewer.md

tools/subagent_factory/
  validate_claims.py
  validate_principles.py
  validate_evidence_protocol.py
  validate_faithfulness_report.py
  prompt_injection_scan.py
  adapter_policy_scan.py
  validate_patch_policy.py
```

This split is not optional. Without it, the project risks becoming “Python-shaped LLM judgment,” which is brittle and misleading.

---

## 4. Key Correction 2 — Every Artifact Needs Schema + Validator + Gate Wiring

The feasibility assessment's second structural fix is also correct.

A new artifact should not be added merely as a file. In this repository, an artifact only becomes enforceable when it has:

1. A schema.
2. A validator.
3. Composite validation gate wiring.

For example, if the plan adds:

```text
claims.jsonl
```

then it should also add:

```text
schemas/claims-v1.schema.json
tools/subagent_factory/validate_claims.py
```

and wire it into:

```text
tools/subagent_factory/validate_generated_package.py
```

Otherwise, the artifact is only documentation. It will not reliably improve output quality.

### Hard rule to add to the plan

```text
No new quality artifact may be introduced without:
- a versioned schema,
- a deterministic validator,
- validation-gate integration,
- and at least one fixture or sample test.
```

---

## 5. Evidence Cards — Keep the Concept, But Integrate It into the Ledger

The feasibility assessment says that separate `evidence-cards.yaml` may duplicate the existing provenance ledger. That engineering point is valid.

However, the **concept** of an evidence card should still be preserved.

The better approach is:

```text
Do not create a parallel evidence-cards.yaml file by default.
Extend the provenance ledger schema to include evidence-card-like records.
```

Recommended structure:

```yaml
evidence_cards:
  - evidence_id: E-001
    claim_id: C-001
    source_ids:
      - S1
    source_anchors:
      - S1#chapter-03-section-02
    evidence_type: argument
    evidence_strength: medium
    confidence: medium
    limitations:
      - "Source provides rationale but no empirical validation."
```

This preserves the evidence model while respecting the repository's existing artifact architecture.

Recommended change:

```text
schemas/provenance-ledger-v2.schema.json
tools/subagent_factory/validate_provenance_ledger.py
```

---

## 6. Importance Ranking — Mostly Done, But Change the Scored Object

The feasibility assessment correctly notes that importance ranking is already largely implemented.

The existing scorer already uses nine dimensions and a `/45` total score, with keep / review / discard decision rules.

Therefore, the improvement should not be to redesign scoring. The improvement should be:

```text
score evidence-backed claims, not vague content units
```

Current weak version:

```text
source text → candidate unit → score
```

Improved version:

```text
source text → atomic claim → evidence card / ledger evidence record → score
```

This makes the ranking more meaningful because the scored item is now:

- atomic,
- traceable,
- evidence-backed,
- classifiable,
- promotable into an operational principle.

---

## 7. Prompt-Injection and Faithfulness Should Be Done Early

The feasibility assessment correctly recommends doing these first:

1. **Prompt-injection / untrusted-source scan**
2. **Evidence faithfulness check**

These are high-value because the factory ingests arbitrary source material: PDFs, ePUBs, web pages, Markdown, and potentially repository documents.

The factory must assume:

```text
all source content is untrusted input
```

Source content must never be allowed to:

- override system, developer, repository, or user instructions;
- grant tool permissions;
- modify `.claude/settings.json`;
- define adapter permissions;
- instruct the factory to ignore previous rules;
- silently rewrite generated policy.

### Recommended immediate additions

```text
tools/subagent_factory/prompt_injection_scan.py
tools/subagent_factory/adapter_policy_scan.py
tools/subagent_factory/validate_faithfulness_report.py
schemas/faithfulness-report-v1.schema.json
.claude/skills/faithfulness-review/SKILL.md
.claude/agents/faithfulness-reviewer.md
```

### Acceptance criteria

```text
- suspicious instruction-like text in source documents is detected and logged;
- generated profile rules stronger than source evidence are flagged;
- unsupported or overgeneralized rules cannot pass release validation;
- adapter-policy contamination is blocked before export or release.
```

---

## 8. Anchoring Limitation — Accept Coarse Anchors for Now

The feasibility assessment correctly points out that the current anchor system is coarse.

It supports heading, figure, code-block, and page-level anchors, but not exact sentence-span anchors.

This affects:

```text
claim → exact supporting sentence
faithfulness check → exact span comparison
principle → exact phrase-level source support
```

For now, the plan should accept section-level or page-level support.

Recommended v0.1 structure:

```yaml
claim_id: C-001
source_anchors:
  - S1#page-42
support_granularity: section
```

Do not implement sentence anchors immediately. That would expand the anchor index and increase implementation complexity.

Possible later enhancement:

```text
paragraph_anchor_v1
sentence_anchor_v1
```

But this should wait until faithfulness checks and claim extraction are already useful at section/page granularity.

---

## 9. Principle Graph Merge Should Be Deferred

The feasibility assessment is correct that Principle Graph Merge is high cost and lower immediate ROI.

A full graph layer requires:

- alias clustering,
- concept normalization,
- ontology alignment,
- principle relation extraction,
- conflict relation modelling,
- multi-source reconciliation.

This is valuable, but premature if most generated subagents are single-source.

Recommended policy:

```text
v0 / v0.1:
  no full principle graph

v0.2 / v0.3:
  principles.yaml + conflict-log.md

v0.4+:
  principle-graph.json only for multi-source packages
```

A principle graph should be activated only when:

```text
a subagent package has 2+ high-value sources
and the sources produce overlapping or conflicting principles
```

---

## 10. Revised Roadmap

### Step 1 — Safety and Faithfulness Gate

Goal:

```text
Prevent polluted or unsupported subagents from being released.
```

Add:

```text
tools/subagent_factory/prompt_injection_scan.py
tools/subagent_factory/adapter_policy_scan.py
tools/subagent_factory/validate_faithfulness_report.py
schemas/faithfulness-report-v1.schema.json
.claude/skills/faithfulness-review/SKILL.md
.claude/agents/faithfulness-reviewer.md
```

Wire into:

```text
tools/subagent_factory/validate_generated_package.py
```

---

### Step 2 — Formalize Atomic Claim Extraction

Goal:

```text
Move from vague source units to atomic, traceable claims.
```

Add:

```text
.claude/skills/claim-extraction/SKILL.md
.claude/agents/claim-extractor.md
schemas/claims-v1.schema.json
tools/subagent_factory/validate_claims.py
```

Output:

```text
claims.jsonl
```

Minimum claim structure:

```yaml
claim_id: C-001
statement: "Explicit module boundaries reduce hidden coupling."
claim_type: design_principle
source_ids:
  - S1
source_anchors:
  - S1#chapter-03
conditions:
  - "Applies to shared module boundaries."
exceptions:
  - "May be overkill for throwaway prototypes."
confidence: medium
```

---

### Step 3 — Extend Provenance Ledger with Evidence Records

Goal:

```text
Bind claims and generated rules to source-backed evidence.
```

Add or update:

```text
schemas/provenance-ledger-v2.schema.json
tools/subagent_factory/validate_provenance_ledger.py
```

Recommended fields:

```yaml
evidence_cards:
  - evidence_id
  - claim_id
  - source_ids
  - source_anchors
  - evidence_type
  - evidence_strength
  - confidence
  - limitations
```

---

### Step 4 — Add Principle Promotion

Goal:

```text
Promote high-value claims into operational principles.
```

Add:

```text
.claude/skills/principle-promotion/SKILL.md
.claude/agents/principle-deriver.md
schemas/principles-v1.schema.json
tools/subagent_factory/validate_principles.py
```

Output:

```text
principles.yaml
```

Minimum principle structure:

```yaml
principle_id: P-001
statement: "Prefer explicit interfaces at stable module boundaries."
derived_from_claims:
  - C-001
confidence: medium
applies_when:
  - "public API design"
  - "multi-team dependency"
does_not_apply_when:
  - "throwaway prototype"
operational_mapping:
  profile_rule: true
  skill: api-boundary-review
  test_cases:
    - GT-003
```

---

### Step 5 — Principle-to-Behaviour Test Coverage

Goal:

```text
Ensure principles affect runtime behaviour, not just documentation.
```

Add:

```text
.claude/skills/principle-test-generation/SKILL.md
tools/subagent_factory/validate_principle_test_coverage.py
```

Rule:

```text
Each high-confidence principle should map to at least one of:
- positive routing test,
- negative routing test,
- output-contract test,
- forbidden-behaviour test,
- patch-safety test.
```

---

### Step 6 — Patch Safety Contract

Goal:

```text
Prevent review-oriented subagents from silently becoming unsafe code-modification agents.
```

Add:

```text
patch-policy.yaml
schemas/patch-policy-v1.schema.json
tools/subagent_factory/validate_patch_policy.py
```

Minimum policy:

```yaml
default_mode: patch_suggest_only
direct_patch_allowed_when:
  - user_explicitly_requests_patch
  - target_files_are_supplied
  - validation_command_exists
  - patch_scope_is_bounded
must_not:
  - silently_edit_canonical_artifacts
  - rewrite_architecture_without_approval
  - patch_without_risk_explanation
```

---

### Step 7 — Principle Graph Merge Later

Goal:

```text
Support multi-source synthesis when the source base becomes large enough.
```

Defer until:

```text
- multi-source packages are common;
- principles.yaml is stable;
- conflict-log quality is reliable;
- faithfulness and safety gates are already enforced.
```

---

## 11. Updated Planning Rules

The enhancement plan should be updated with these hard rules:

### Rule 1 — LLM Judgment Placement

```text
LLM judgment must live in skills/agents, not deterministic tools.
```

Examples of LLM judgment:

```text
claim extraction
semantic classification
principle promotion
faithfulness comparison
conflict reasoning
test-case authoring
```

### Rule 2 — Artifact Enforcement

```text
Every new artifact must have schema + validator + composite gate wiring.
```

### Rule 3 — Extend Existing Artifacts First

```text
Prefer extending provenance-ledger, score_extracted_units, quote_scan, and validation gates
before introducing parallel files.
```

### Rule 4 — Tier by Source Complexity

```text
Short single-source packages should use a light path.
Long books and multi-source packages should use the full claim/principle path.
```

### Rule 5 — Safety Before Intelligence

```text
Prompt-injection scanning and faithfulness checking should land before principle graph,
advanced merge, or direct patch automation.
```

---

## 12. Final Recommendation

The feasibility assessment should be accepted.

It strengthens the previous plan by making it implementation-realistic.

The next action should be to update the enhancement plan with two structural constraints:

1. **LLM judgment belongs in skills/agents.**
2. **Every new artifact requires schema, validator, and composite gate wiring.**

After that, implement in this order:

```text
1. prompt-injection scan
2. adapter-policy scan
3. faithfulness review gate
4. atomic claim extraction
5. provenance-ledger evidence extension
6. principle promotion
7. principle-to-behaviour tests
8. patch safety contract
9. principle graph merge only for multi-source packages
```

This moves the project from:

```text
structurally valid subagent generation
```

to:

```text
evidence-grounded expert subagent manufacturing
```

without redesigning the core workflow.
