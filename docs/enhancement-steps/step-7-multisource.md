# Step 7 — Multi-Source Synthesis (Principle Graph)

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 7. Depth: **stub** (deferred).
> **Promote to full when:** multi-source packages are common AND `principles.yaml` is stable AND
> the safety + faithfulness gates (Steps 1, 3) are enforced.

## Goal
For subagents built from 2+ high-value sources, merge **principles** (not just profiles): cluster
aliases, detect cross-source conflicts, and record a principle graph — so the agent has a real
knowledge model instead of a pile of summaries.

## Scope (deferred — do not build yet)
- `subagents/<slug>/principles/conflict-log.md` — existing pattern (`merge-conflict-log.md`).
- `subagents/<slug>/principles/principle-graph.json` — Tier 2 only.
- LLM clustering / alias detection / conflict detection; deterministic graph validator.

## Why deferred
- Almost all current packages are **single-source** → near-zero ROI now.
- The schema depends on `principles-v1` (Step 4) being stable.
- Highest-cost, lowest-immediate-value of the roadmap (master §3 feasibility).

## Research input (future)
- **Argument-mining** provides the relation vocabulary for the graph: AM relation types
  (`support`, `attack`, `agreement`, `rebuttal`, `undercutter`) and AZ zones — directly usable
  for conflict/relationship edges between principles.
- Factual-consistency contributes nothing here.
- A dedicated **knowledge-fusion / conflict-detection** literature spike (original plan §20) should
  precede full implementation.

## Trigger checklist (before promoting to full)
- [ ] ≥1 real Tier-2 (multi-source) package exists.
- [ ] `principles.yaml` schema frozen + ≥2 single-source packages using it.
- [ ] Steps 1 + 3 gates enforced (safety + faithfulness).
- [ ] Knowledge-fusion research spike done.
