# Step 8 — Skill & Reference Body Authoring

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 8. Depth: **full**.
> Closes the **Phase 6 authoring gap** (`docs/subagent-authoring-process-cycle.md` Phase 6):
> the factory scaffolds stubs (`cli stubs`) but nothing authors their bodies, so every
> package is stuck at `status: draft`. This step is the missing producer.

## Goal
Author the **bodies** of every `skills/<name>/SKILL.md` and `references/<name>.md` that a
profile's `knowledge_partition` declares — grounded in that package's principles / evidence /
source, not invented — so a package can legitimately reach `status: ready`.

## Problem this fixes (the gap)
- Phase 6's *stated output is "stubs"* (`subagent-authoring-process-cycle.md:30,356`) and
  `generate_stubs.py` only writes `STATUS: STUB` placeholders.
- **No milestone, agent, skill, or tool authors the bodies** (impl-plan §6,§7,§8,§14); it is
  not even in the post-v0 deferral list (§2.0). The cycle silently assumed a human fills the
  bodies between Phase 6 and Phase 10. The factory automated everything *around* that step.
- Result: ~100% of generated skills/references across the corpus are stubs; the principle layer
  (Steps 2–5) never reaches a shipped artifact. This step is where principles finally change
  content a runtime agent reads.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `.claude/skills/author-skills/SKILL.md` | skill (LLM) | Orchestrate body authoring for one package: enumerate stubs → gather grounding → author each → flip `status` → re-validate. |
| `.claude/agents/skill-author.md` | agent (LLM) | Author **one** skill body or **one** reference body from supplied grounding. Read-mostly; `Write` restricted to the single target stub file. |
| `schemas/authored-doc-v1.schema.json` | schema | Frontmatter contract for both doc kinds: `name`, `kind: skill\|reference`, `status: stub\|ready\|stale`, `provenance` (claim/principle/source IDs). |
| `tools/subagent_factory/validate_skill_authoring.py` | tool (validator) | Referential + structural + status-gated FAIL. |
| `tests/fixtures/skill-authoring/` | fixtures | authored-ready pass; ready-with-stub FAIL; draft-with-stub pass(WARN). |
| `generate_stubs.py` (edit) | tool | Emit `authored-doc-v1` frontmatter on **both** skills and references (references currently have none) so status is machine-readable for both kinds. |

## `authored-doc-v1` frontmatter (both kinds carry it)
```yaml
name: cache-performance-break-even      # == knowledge_partition slug
kind: skill                             # skill | reference
status: ready                           # stub | ready | stale
provenance:                             # what the body is built FROM (referential, master §6)
  principles: [P009, P001]              # ∈ principles/principles.yaml ids        (Tier 1+)
  claims: [C-0007]                      # ∈ analysis/claims.jsonl ids             (Tier 1+, optional)
  source_anchors: ["<sid>-h0042"]       # ∈ anchor index                         (all tiers)
```
Markdown bodies cannot be fully schema-validated; the **frontmatter** is the schema'd surface,
and the **body** is checked structurally (sections + size + not-a-stub + provenance present) —
substance is guarded by faithfulness + quote-scan, not by this schema. This satisfies the
"no artifact without a versioned schema" rule (master §2.2) honestly: schema the frontmatter,
gate the structure, defer substance to the existing safety layer.

## Authoring contract (what the agent must produce)
**Skill body** (`SKILL.md`, ≤ 500 lines / 5,000 tokens — Phase 6 limit):
`Purpose` · `When to use` · `Procedure` (the repeatable/branching steps that justified
extraction) · `Inputs` · `Output` · `References` (link sibling reference docs) · `Provenance`
(the claim/principle/source IDs the steps derive from).
**Reference body** (`<name>.md`): the actual table / taxonomy / rubric / checklist the entry
names + a `Provenance` line. No `Procedure` (that is what makes it a reference, not a skill —
triage tree, process-cycle Phase 4).

## Grounding inputs (the quality crux — body is derived, not invented)
| Tier | Grounding the skill-author reads |
|------|----------------------------------|
| **1+** | `principles/principles.yaml` entries whose `operational_mapping.skill` == this slug → their `derived_from_claims` → `evidence/evidence-records.yaml` → `source_anchors` → source markdown (`source_text.py`). Plus profile `always_on` rules citing the same principle IDs (e.g. `P005`). |
| **0** | profile `always_on` + `when_to_use` + the source markdown directly (no principle layer). Lower evidence density; accepted. |
| **all** | profile `supported_modes`, `quality_bar`, `forbidden_behaviours` (the skill must not contradict them); rights status (distillation-only ⇒ no verbatim). |

This wires Step 8 to Steps 2–5: a Tier-1 skill body is authored *from the principle(s) mapped
to it and their evidence*, closing the source → claim → evidence → principle → **skill body**
loop. `operational_mapping.skill` in `principles-v1` is the join key (already validated by
`validate_principles.py` to resolve to a real skill/stub — Step 4).

## Reuse
- `generate_stubs.py` — scaffolds the files Step 8 fills (slug mapping is the contract).
- `principles-v1` `operational_mapping` + `validate_principles.py` — principle↔skill join (Step 4).
- `evidence-records-v1`, `claims-v1`, anchor index, `source_text.py` — grounding chain (Steps 0,2,3).
- `quote_scan.py` — re-run after authoring: distillation-only bodies must stay non-verbatim.
- `faithfulness-review` (Steps 1/3) — authored body is a new surface to check "stronger than source".
- profile `status` field (already present, `draft` on all 15) + `agent_version`/CHANGELOG (release rule).

## `validate_skill_authoring.py` (structural + referential + status-gated)
- **Referential:** every `knowledge_partition.skills[]` slug → a `skills/<slug>/SKILL.md`;
  every `references[]` slug → a `references/<slug>.md` (via `generate_stubs` slug rule). Missing → FAIL.
- **Frontmatter:** each file validates against `authored-doc-v1`; `provenance.principles/claims`
  ∈ the package's `principles.yaml`/`claims.jsonl` (Tier 1+); `source_anchors` ∈ anchor index.
- **Structural body:** required sections present for its `kind`; size ≤ 500 lines / 5k tokens
  (skills); no residual `STATUS: STUB` / `TODO: author` marker in a `status: ready` file.
- **Status gate (the non-breaking core):**
  - profile `status: ready` ⇒ **every** listed skill/reference must be `status: ready` →
    any remaining `stub` is **FAIL**. This is what makes `draft → ready` mean "authored".
  - profile `status: draft` ⇒ stubs allowed → **WARN** with `authored N / total M` count only.
  - ⇒ the 15 current packages (all `status: draft`) keep passing untouched.

## Gate wiring
Dedicated block in `validate_generated_package.py` (not a `_TIER_ARTIFACTS` row — the check
spans many files keyed on profile `status` + `knowledge_partition`, like the scan blocks).
Present-gated; **FAIL only when `status: ready`**, else WARN. Runs all tiers.

## LLM ↔ deterministic split
- **LLM:** `author-skills` skill (orchestration, grounding assembly, status flip decision),
  `skill-author` agent (writes the actual procedure / table — judgment).
- **Deterministic:** `validate_skill_authoring.py` (referential map, frontmatter schema,
  stub-vs-authored count, status-gated FAIL), `generate_stubs.py` (scaffold), `quote_scan`.

## Wiring into `author-subagent`
- New optional terminal step after Step 9 validate: `author-skills <slug>` fills stubs; on a
  clean validate + quote-scan + faithfulness, flip profile `status: draft → ready`, bump
  `agent_version`, add CHANGELOG entry, re-export adapter.
- Default run still stops at `draft` (authoring is opt-in / on release) — keeps per-PDF
  campaign cost bounded (master §10 LLM-pass cost). Step 10 summary already reports the
  unauthored list; it gains "run `author-skills <slug>` to author + promote to ready".

## Fixtures
- A package with all skills/refs authored + valid provenance → passes at `status: ready`.
- Same package set to `status: ready` with one stub remaining → FAIL (status gate).
- A `status: draft` package with stubs → passes with WARN (count).
- Bad frontmatter / dangling `provenance.principles` id / residual TODO in a ready file → fail.

## Exit criteria + verify
1. `validate_skill_authoring` passes a fully-authored ready package; FAILs ready-with-stub;
   WARNs (passes) draft-with-stub.
2. All 15 Tier-0 packages still pass `validate` (they are `draft`; status gate is WARN).
3. **One real package taken `draft → ready` end-to-end** as proof — e.g.
   `caching-strategy-advisor` (7 skills + 5 references) authored from its `principles.yaml` +
   evidence, then `quote_scan` + faithfulness green, `status: ready`, adapter re-exported.
4. `author-subagent` can author + promote a freshly generated package.

## Caveats (validate ourselves)
- **Body substance is LLM-bounded.** The validator proves *shape, mapping, and not-a-stub*, not
  correctness. faithfulness-v1 + quote_scan are the substance guards; neither is authored by
  this step's agent. A `ready` package is "authored + non-over-claiming + non-verbatim", not "expert-verified".
- **Tier 0 bodies are thinner** — grounded on profile `always_on` + source, no principle/evidence
  chain. Acceptable; flagged in provenance (empty `principles`).
- **Markdown ≠ fully schema-able.** Section/size/marker/provenance are the deterministic proxies.
- **`stale` status** (source drift, Phase 12 maintenance) is in the enum but its re-author
  trigger is out of scope here — set by the maintenance cycle, re-cleared by re-running Step 8.

## Risks
- **Scope creep by the author agent** (edits profile / other files) → restrict its `Write` to the
  single target stub path; the `status` flip is done by the orchestrating skill under the gate,
  never by the per-file agent.
- **Premature `draft → ready` flip** → gate FAILs `ready`-with-stub, so a flip without authoring
  is blocked by validation.
- **Authored skill drifts from profile `always_on`** → `Provenance` line + faithfulness check the
  body against the same principle/source IDs the profile cites.
- **Cost** (N skills + M refs LLM passes per package) → opt-in / release-time, not per campaign run.

## Dependencies
Builds on Step 0 (`source_text`, `tier`, gate convention) and Steps 2–5 (claims/evidence/
principles = Tier-1 grounding inputs; `operational_mapping` join). Independent of Steps 6/7.
All upstream steps are merged + validated, so **full** depth is correct now (promotion rule).
