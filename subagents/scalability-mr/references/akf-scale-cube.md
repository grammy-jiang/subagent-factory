---
name: akf-scale-cube
kind: reference
status: ready
provenance:
  principles: [P001, P004, P037]
  claims: [C00030, C00031, C00032, C00033, C00049, C00203]
  evidence: [E00023, E00024, E00025, E00026, E00033, E00166]
  source_anchors: [67c60e378753-c0000, a6c7e769c072-c0000]
---

# Reference: The AKF Scale Cube

A compact map of the three independent axes for scaling a system, service, or database. Use it to
name *how* load is being partitioned and to choose the axis that relieves the actual bottleneck.
Grounded in principles **P001** (scale out, not up), **P004** (the AKF Scale Cube), and **P037**
(autonomous, independently scalable components).

## The three axes

| Axis | Split | What it scales | Use when |
|------|-------|----------------|----------|
| **X** | Clone identical copies | Transactions / request volume | The easiest first move; duplicate the whole service or database behind a balancer. |
| **Y** | Split *different* things by function or resource (verbs/nouns) | Transactions **and** large data sets; also gives fault isolation | Cloning no longer helps; responsibilities and their data can be separated. |
| **Z** | Split *similar* things by a data or customer attribute (ID, geography) — shard/pod | Very large *similar* data sets; per-customer fault isolation | Customer or data growth outpaces other growth; shards may be unequal to limit rollout risk. |

## How to choose

1. Confirm the system must grow and identify the bottleneck (transactions, data size, customers).
2. Exhaust **X** (cloning) first — it is cheapest and simplest.
3. Move to **Y** when cloning stops relieving the bottleneck or when fault isolation between
   functions is needed.
4. Move to **Z** when a single *similar* data set is too large or per-customer isolation matters.

## Trade-off

Every axis duplicates data, functionality, or both, and adds operational surface. Scale-out buys
fast, cost-effective growth on commodity nodes at the cost of that duplication and complexity — name
the cost in any recommendation (P001).

## Related

- Skill: [scale-out-and-akf-decomposition](../skills/scale-out-and-akf-decomposition/SKILL.md)
- Reference: [Scalability Rules index](scalability-rules-index.md)

## Provenance

Distilled from principles **P001/P004/P037** and their claims/evidence in `analysis/claims.jsonl` +
`evidence/evidence-records.yaml`, anchored in `sources/anchors/`. Sources are `distillation-only`:
paraphrased, never quoted verbatim.
