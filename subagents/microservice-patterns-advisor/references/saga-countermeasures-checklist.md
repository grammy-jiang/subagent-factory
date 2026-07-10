---
name: saga-countermeasures-checklist
kind: reference
status: ready
provenance:
  principles:
  - P014
  - P070
  - P071
  - P047
  claims:
  - C00210
  - C00211
  - C00212
  - C00213
  - C00214
  - C00254
  - C00255
  - C00197
  - C00198
  source_anchors: []
  authored_from_digest: 163d7385d4e45364633e4114b4c87abefdb4eca5847e2e93863cd2e55e7319ec
---

# Saga Countermeasures Checklist

Sagas are ACD — they have Atomicity, Consistency, and Durability but lack the
Isolation of ACID transactions, so each local transaction's updates become visible to
other sagas as soon as it commits and concurrent sagas can interleave and produce
anomalies (C00197, C00210, P070). Those anomalies are lost updates, dirty reads, and
fuzzy/nonrepeatable reads (C00211). Because there is no isolation and no automatic
rollback (a failed step is undone by compensating transactions in reverse order,
C00198, P047), the design must apply **countermeasures** — techniques that prevent or
reduce the business impact of the concurrency anomalies (C00212, C00213, P014). Use
this checklist when recommending a saga.

## The six countermeasures

| Countermeasure | What it does |
|---|---|
| Semantic lock | Set an application-level `*_PENDING` flag on a record a saga is operating on, cleared by a later retriable or compensating transaction, so other sagas see it is in progress and fail-and-retry or block-until-released (C00214). |
| Commutative updates | Design updates so they can be applied in any order (e.g. add/subtract), so interleaving does not corrupt the result. |
| Pessimistic view | Reorder a saga's steps so the most consequential update happens where a dirty read would do the least damage. |
| Reread value | Re-read a record before updating it and verify it is unchanged since it was read (optimistic offline lock), aborting the saga step if it changed. |
| Version file | Record the operations applied to a record so out-of-order operations can be reordered or detected. |
| By value | Choose the concurrency mechanism per request by its business risk — use sagas for low-risk requests and stricter concurrency control for high-risk ones. |

## Structuring the aggregate for a saga

For an operation that requires a saga, first move the aggregate to a `*_PENDING`
state (a semantic lock), group the aggregate's methods per saga (a start method moves
it to pending; end methods confirm or reject), and have the service create and persist
the aggregate and then create the saga rather than updating the aggregate directly, so
the aggregate stays transactionally consistent with data owned by other services
(C00254, C00255, P071).

## Review checklist

When advising on a saga, confirm:

- [ ] Each step has a defined **compensating transaction** for the compensatable
      steps that precede the pivot (C00198).
- [ ] The **isolation anomalies** that apply (lost updates, dirty reads, fuzzy
      reads) have been considered for the data the saga touches (C00211).
- [ ] At least one **countermeasure** above is applied to each anomaly that
      matters, chosen by the anomaly and the business risk (C00213, P014).
- [ ] The design **accepts eventual consistency** across the participating
      services and the caller has been told so.

## Provenance

Tier 2 reference. Grounded in principles P070 (the saga's lack of isolation and its
anomalies), P014 (the documented countermeasures), P071 (the semantic-lock aggregate
structure), and P047 (compensating transactions), and in claims C00197–C00198,
C00210–C00214, C00254–C00255 from `chris-richardson-mic-19016f24` (Microservices
Patterns, Chris Richardson, Manning 2018, `distillation-only`). The six countermeasure
names are the source's established terminology; the explanations are paraphrased — no
verbatim quotation.
