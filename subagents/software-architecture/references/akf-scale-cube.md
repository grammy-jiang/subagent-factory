---
name: akf-scale-cube
kind: reference
status: ready
provenance:
  principles:
  - P003
  - P017
  - P057
  claims:
  - C01875
  - C01882
  - C02235
  - C02236
  - C02360
  - C02361
  evidence:
  - E00259
  - E00260
  - E00316
  - E00317
  - E00395
  - E00396
  source_anchors:
  - 760c81171459-c0017
  - 760c81171459-c0019
  - a6c7e769c072-c0000
  - a6c7e769c072-c0002
  authored_from_digest: 94899d51d05036a1bdb97dd7b9dca29e94e8b691628237f71b60921460e4a2c2
---

# The AKF Scale Cube

A system scales out — across many machines — along three independent axes. Scaling *up* (a bigger
machine) is the alternative, and it eventually runs out of larger/faster hardware to buy. The cube
names the three ways to split load so you can pick the one that relieves the actual bottleneck.

## The three axes

| Axis | Name | What it splits | Mechanism | Buys |
|------|------|----------------|-----------|------|
| **X** | Clone / horizontal duplication | The *same* thing | Duplicate the whole service or database; identical copies share the transaction load | Fast transaction scale; usually the easiest split |
| **Y** | Split different things | By function / resource | Separate services and their data along responsibility lines (verbs = services, nouns = resources) | Scales transactions *and* large data sets; fault isolation |
| **Z** | Split similar things | By a customer / data attribute | Shard or pod by ID, name, geography, device, etc. | Scales very large similar data sets / customer bases; fault isolation between groups |

## How to choose an axis

- **Start at X.** Cloning is the simplest move. If duplicating identical copies still relieves load,
  prefer it — on many small commodity nodes rather than a few high-end servers.
- **Go to Y when cloning stops helping.** When the limit is transaction *mix*, data-set size, or
  scaling engineering teams by specialization, split different responsibilities apart.
- **Go to Z for huge similar data sets.** When one kind of data/customer base grows faster than the
  rest, partition it by an attribute you know about the customer or record. Shards may be unequal —
  a small shard first limits the blast radius of a rollout.
- **Combine axes.** Real systems use more than one axis at once (e.g. clone each shard).

## The trade-off

Every axis duplicates or partitions data and functionality, adding operational surface and (for Y/Z)
cross-partition complexity. Scaling out buys throughput and fault isolation at the cost of that
duplication and complexity — there is no cost-free scalability. Choose the axis whose cost the
prioritized characteristics can bear.

## Provenance

Distilled from principle(s) **P003/P013/P032**, claims **C00395/C00402/C00755/C00756/C00880/C00881**, evidence **E00079/E00080/E00120/E00121/E00174/E00175**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
