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
| 7 | `step-7-multisource.md` | stub | deferred | 4 | (argument-mining AM relations, future) |
| 8 | `step-8-skill-authoring.md` | full | **implemented** | 0,2–5 | (factual-consistency guards the bodies) |
| 9 | `step-9-stale-maintenance.md` | full | **spec — in progress** | 8 | — |

Depth: **full** = implementation-ready; **medium** = goal + file sketch + dependencies;
**stub** = goal + defer trigger only.

> **Steps 8–9 were added after the original 0–7 roadmap.** Step 8 closes the **Phase 6 authoring
> gap** (factory scaffolds skill/reference *stubs* but nothing authors their *bodies*, so packages
> are stuck at `status: draft`). Step 9 closes the **Phase 12 maintenance gap** (the `stale` status
> exists but nothing detects drift or sets it). Both spec'd **full** because their upstream is
> merged. See `step-8-skill-authoring.md`, `step-9-stale-maintenance.md`.

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
