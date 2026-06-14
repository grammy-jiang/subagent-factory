# Enhancement Steps — Detailed Build Specs

Per-step, implementation-ready specifications that expand the 8-step roadmap in
**`docs/subagent_enhancement_build_plan.md`** (the master plan).

- **Master plan** = architecture, rationale, hard rules, resolved design forks.
- **These docs** = the concrete, executable spec for each step (exact files, schema
  fields, validator checks, gate wiring, fixtures, exit tests). They reference the
  master plan for *why*; they add only the *what/where/how*.
- **Research** from the 3 topics (`docs/Research/`) is merged **into Steps 1–3**
  (there is no separate `INTEGRATION.md`; the method specs live where they are used).

## Source lineage

```
subagent_workflow_quality_enhancement_plan.md      (original 12 enhancements)
  → subagent_workflow_quality_enhancement_feasibility.md (vs code)
  → subagent_feasibility_review_comments.md         (external review)
  → subagent_enhancement_build_plan.md              (MASTER — 8 steps)
  → docs/Research/{prompt-injection-defense, argument-mining-claim-extraction,
                   factual-consistency-faithfulness}/  (method grounding for Steps 1–3)
  → docs/enhancement-steps/                          (THIS — detailed per-step specs)
```

## Status

| Step | Doc | Depth | Status | Depends on | Research input |
|------|-----|-------|--------|------------|----------------|
| 0 | `step-0-plumbing.md` | full | **implemented (merged)** | — | — |
| 1 | `step-1-safety-faithfulness.md` | full | **implemented** | 0 | prompt-injection + factual-consistency |
| 2 | `step-2-claims.md` | full | **implemented** | 0 | argument-mining |
| 3 | `step-3-evidence-faithfulness-v1.md` | full | **implemented** | 0,2 | factual-consistency + argument-mining |
| 4 | `step-4-principle-promotion.md` | full | **implemented** | 2,3 | (argument-mining, light) |
| 5 | `step-5-principle-tests.md` | full | **implemented** | 4 | — |
| 6 | `step-6-patch-safety.md` | full | **implemented** | 5 | (prompt-injection, light) |
| 7 | `step-7-multisource.md` | full | **implemented (Phase A–D; proven on a 2-source pkg)** | 4 | argument-mining + knowledge-fusion-conflict-detection |
| 8 | `step-8-skill-authoring.md` | full | **implemented** | 0,2–5 | (factual-consistency guards the bodies) |
| 9 | `step-9-stale-maintenance.md` | full | **implemented** | 8 | — |
| 10 | `step-10-source-structure-mapping.md` | full | **spec (research done; scaffolding built)** | 0,2 | long-document-structure-mapping |
| 11 | `step-11-behaviour-test-generation.md` | full | **implemented (det core + gate; LLM ideation follow-on)** | 0,4,5 | behaviour-test-generation |
| 12 | `step-12-optimize-adapter.md` | full | **implemented (driver + proposer skill + live CLI)** | 11 + A-track | prompt-optimization-eval |
| 13 | `step-13-ask-gate.md` | full | **partial (F4 twins + F3 two-axis grading built; runtime gate spec)** | 11, 12 | calibration-abstention |
| 20 | `step-20-document-ai-pdf-parsing.md` | full | **implemented (merged)** | 0,1,2,10 | (Step-10 A/B finding) |

Depth: **full** = implementation-ready; **medium** = goal + file sketch + dependencies;
**stub** = goal + defer trigger only.

> **Steps 8–9 were added after the original 0–7 roadmap.** Step 8 closes the **Phase 6 authoring
> gap** (factory scaffolds skill/reference *stubs* but nothing authors their *bodies*, so packages
> are stuck at `status: draft`). Step 9 closes the **Phase 12 maintenance gap** (the `stale` status
> exists but nothing detects drift or sets it). Both spec'd **full** because their upstream is
> merged. See `step-8-skill-authoring.md`, `step-9-stale-maintenance.md`.

> **Steps 11–12 are the measure→optimize loop** (Phase 10+). Step 11 generates a high-coverage
> adversarial behaviour-test suite (golden / negative-routing / missing-context) from the
> profile+principles — the *objective*. Step 12 then tunes the adapter to maximize that objective via
> the existing replay engine + replay-gate (propose→score→keep-winner), with faithfulness as a hard
> pre-merge gate. They fold `docs/Research/{behaviour-test-generation, prompt-optimization-eval}/`
> (the **E** and **D** tracks in `research-integration-plan.md`). Spec'd **full** — upstream (Step 5
> tests + the A-track replay primitives) is merged. See `step-11-behaviour-test-generation.md`,
> `step-12-optimize-adapter.md`.

## Promotion rule (medium → full)

Promote a doc to **full just-in-time**, when the step becomes the *next to implement* —
i.e. when **every step it depends on is merged + validated (its schemas frozen)**. A
full spec must reference real upstream IDs/schemas, so it cannot be written correctly
before those exist.

| Doc | Promote to full when… |
|-----|------------------------|
| Step 4 | Step 3 merged + `claims-v1` and `evidence-records-v1` schemas frozen |
| Step 5 | Step 4 merged + `principles-v1` frozen |
| Step 6 | Step 5 merged, **or** earlier if a subagent needing patch modes is requested |
| Step 7 | Multi-source packages are common + `principles.yaml` stable + safety/faithfulness gates enforced |

Upgrading a doc is the **first task** of starting that step.

## Per-step template

```
# Step N — <name>

Goal            one sentence — the property this step guarantees.
New files       exact paths: schema / validator / skill / agent / tool.
Reuse           existing code/artifacts this builds on (cite file).
Gate wiring     where it attaches in validate_generated_package.py; FAIL vs WARN.
LLM ↔ deterministic split   which parts are skills/agents vs tools.
Research inputs [Steps 1–3 only] findings → concrete spec, with paper IDs.
Fixtures        sample inputs the validator/tests run against.
Exit criteria   how we know it's done + how to verify (commands).
Caveats         validate-ourselves flags, open gaps, domain limits.
Risks           what could break; mitigation.
```

## Execution rules (carry into every step)

1. **Never break the 15 Tier-0 packages.** New gate checks are present-gated + tier-gated.
   Step 0 exit criteria = all 15 still pass `python -m tools.subagent_factory.validate_generated_package subagents/<slug>`.
2. **LLM judgment → skills/agents; deterministic enforcement → tools/schemas/validators/gate.**
3. **No artifact without schema + referential validator + gate wiring + fixture.**
4. **Validate after each step**; one step = one reviewable change set.
