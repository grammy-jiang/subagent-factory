---
name: data-tier-scaling-and-storage
kind: skill
status: ready
provenance:
  principles: [P002, P018, P015, P020, P049, P032]
  claims: [C00068, C00069, C00121, C00122, C00130, C00126, C00452, C00176]
  evidence: [E00052, E00098, E00107, E00103, E00234, E00146]
  source_anchors: [67c60e378753-c0001, 67c60e378753-c0002, 67c60e378753-c0003, 67c60e378753-c0004]
---

# Scale the data tier: right tool, sound model, no lock-and-wait

## Purpose

Keep the database from becoming the bottleneck by choosing the right storage tool, modelling
relationships up front, and removing locking patterns that serialize throughput.

## When to use

- A team is introducing new data or data structures, or the database is "too slow".
- A relational database runs under high transaction volume, distributed transactions, or cursors.
- A read tier must scale out, or corporate and product systems must exchange data.

Do not invoke to choose a specific database product (out of scope) or to write the schema/migration
code (hand off).

## Procedure

1. **Use the right storage tool (P002).** Reserve an RDBMS for genuine ACID/relationship needs;
   choose a file system or NoSQL store otherwise. "Too slow" usually means the wrong tool, not a
   need for more hardware — the cost of the wrong tool is paid on every query.
2. **Design the data model up front (P018).** Relationships dictate how the database can later be
   split (the AKF Y/Z axes), and fixing the model after the fact can cost ~100x. Model before adding
   tables, columns, or queries.
3. **Avoid lock-and-wait patterns (P015).** Do not use multiphase commits, and minimize
   `SELECT ... FOR UPDATE` cursors; both serialize work and cap concurrency.
4. **Manage locking for concurrency (P020).** Tune lock granularity, let the optimizer choose and
   then correct it, and pick an engine with flexible lock types.
5. **Limit distinct products; scale reads with replicas (P049).** Use the same product for the same
   job unless the new demand genuinely differs. For a horizontally scaled read tier, place cheaper
   replicas around the proven core and avoid changing what works.
6. **Separate BI from transaction processing (P032).** Keep stored procedures out of the database and
   move data between corporate and product systems asynchronously, so reporting load never competes
   with live transactions.
7. **State the trade-off.** Splitting and replicating the data tier buys read/write throughput and
   isolation at the cost of duplicated data, eventual consistency, and operational complexity. Name
   it.

## Inputs

- The data's transactional/relationship needs, the read/write profile, the current model, and the
  contention symptoms.

## Output

A data-tier recommendation naming the storage tool, the model or split required, the locking pattern
to remove, and the consistency/complexity cost accepted.

## References

- [AKF Scale Cube](../../references/akf-scale-cube.md) — how the model constrains Y/Z splits.
- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P002/P018/P015/P020/P049/P032** and their claims/evidence, anchored in
`sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
