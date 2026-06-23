---
name: scale-out-and-axis-decomposition
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P017
  - P057
  - P005
  claims:
  - C01875
  - C01882
  - C02235
  - C02236
  - C02360
  - C02361
  - C00242
  - C00243
  evidence:
  - E00259
  - E00260
  - E00316
  - E00317
  - E00395
  - E00396
  - E00059
  - E00060
  source_anchors:
  - 705fce793a41-c0000
  - 745dee448a5d-c0000
  - 745dee448a5d-c0003
  - 6b15bd8cd9ba-c0005
  authored_from_digest: 98197644a546acb91a0ece88fad44b3dd22c0a77a225dfa5a8ae12f2c1836406
---

# Scale out, and decompose load along the AKF Scale Cube

## Purpose

Guide a system toward horizontal scale-out and pick the right way to partition that load. Scaling
up (buying ever-larger hardware) hits a ceiling — eventually there is no faster or larger machine
to buy — so growth-bearing systems should be designed to scale out across many commodity nodes.
Once scaling out, the AKF Scale Cube names the three independent axes of partition; this skill
chooses the axis that relieves the actual bottleneck.

## When to use

- A system is expected to grow and the team must choose between scaling up and scaling out.
- Cloning identical copies (the easy first move) no longer relieves the bottleneck — data size,
  transaction mix, or team scaling has become the limit.
- A scaling plan assumes growth will be met by a bigger server.

Do not invoke for a small, fixed workload that one node serves comfortably for its whole lifetime.

## Procedure

1. **Confirm the growth assumption.** Establish that the system must grow. If load is bounded and
   stable, scale-out machinery is overhead (hand off to `economical-scalability-and-tooling`).
2. **Reject the scale-up reflex.** If the plan is "buy a bigger box", name the ceiling: scale-up
   runs out of larger/faster hardware, while scale-out duplicates work across commodity nodes. Prefer
   many small inexpensive systems over a few high-end servers for fast, cost-effective growth.
3. **Start on the X axis.** The easiest split is horizontal cloning — duplicate the whole service or
   database so identical copies share the transaction load. Check this is exhausted before moving on.
4. **Move to Y when cloning stops helping.** Split *different* things by function or resource
   (verbs/nouns): separate services and their data along responsibility lines. This scales
   transactions *and* large data sets and gives fault isolation.
5. **Move to Z for very large similar data sets.** Split *similar* things by a customer or data
   attribute (ID, name, geography) — sharding/podding. Use it when customer growth outpaces other
   growth or when fault isolation between customer groups matters; shards may be unequal to limit
   rollout risk.
6. **State the trade-off.** Scaling out buys fast transaction scale at the cost of duplicated data
   and functionality and added operational surface. Name that cost in the recommendation.

## Inputs

- The system's growth expectation, the current bottleneck (transactions, data size, customers), and
  the present partitioning (if any).

## Output

A scale-out recommendation that names the chosen AKF axis (X/Y/Z) and why it fits the bottleneck,
the scale-up ceiling being avoided, and the duplication/complexity cost accepted.

## References

- [AKF Scale Cube](../../references/akf-scale-cube.md) — the X/Y/Z axes and how to pick one.

## Provenance

Distilled from principle(s) **P003/P013/P032/P045**, claims **C00395/C00402/C00755/C00756/C00880/C00881**, evidence **E00079/E00080/E00120/E00121/E00174/E00175**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
