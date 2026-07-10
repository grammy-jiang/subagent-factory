---
name: saga-transaction-design
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P036
  - P047
  - P070
  - P014
  - P060
  - P133
  - P120
  claims:
  - C00005
  - C00072
  - C00073
  - C00197
  - C00198
  - C00200
  - C00201
  - C00206
  - C00210
  - C00211
  - C00213
  - C00214
  - C00202
  - C00203
  - C00217
  source_anchors: []
  authored_from_digest: 984e09a81a542f2ef0f9d59e30c46aff5778143300a25ab7688b14c14ccba52a
---

# Saga Transaction Design

## Purpose

Guide a caller who must keep data consistent across services without a distributed
transaction. Covers the Database-per-service decision that creates the problem, the
Saga pattern that solves it, the ACD / lack-of-isolation hazard and its
countermeasures, the choice between choreography and orchestration, and how to
sequence a monolith migration into sagas. This is the specialised walkthrough for the
**Data / transactions** group.

## When to use

Use when an operation or update must span more than one service and must remain
consistent, or when the caller proposes a distributed two-phase commit. Do not use
for cross-service *queries* (route to `cross-service-query-design`) or for an
operation fully contained within one service/aggregate.

## Procedure

1. **Confirm the data ownership.** Each service keeps its data private and other
   services reach it only through its API, so you cannot run a distributed query or
   transaction across service databases (C00073, P120). Choosing private data is
   exactly what makes cross-service consistency hard and forces a saga.

2. **Recommend a Saga, not 2PC.** A distributed two-phase-commit transaction is not
   a viable option across microservices — it is unsupported by much modern
   technology and reduces availability (C00072). Recommend a Saga: a sequence of
   local ACID transactions, each updating one service and triggering the next,
   coordinated by asynchronous messaging (C00005, P001).

3. **Design the compensations.** A saga is ACD and each local transaction commits
   immediately, so there is no automatic rollback; a failed step is undone by running
   the earlier steps' compensating transactions in reverse order (C00197, C00198,
   P047). Classify each step as compensatable, the single pivot (the go/no-go point),
   or retriable; read-only steps and steps followed only by steps that succeed need
   no compensation (C00200).

4. **Address the lack of isolation.** Warn that because a saga is ACD it lacks the
   Isolation of ACID, so concurrent sagas can interleave and cause lost updates,
   dirty reads, and fuzzy/nonrepeatable reads (C00210, C00211, P070). Recommend the
   relevant countermeasures — semantic lock, commutative updates, pessimistic view,
   reread value, version file, by value — chosen by the anomaly and business risk
   (C00213, C00214, P014), using the `saga-countermeasures-checklist` reference.

5. **Choose the coordination style.** Choreography has participants exchange events
   with no central coordinator; each must update its database and publish its
   triggering event atomically via transactional messaging and correlate received
   events back to its own data (C00202, C00203, P060). Orchestration has a central
   orchestrator send command messages and is best modelled as a state machine
   (C00201, C00206). Prefer orchestration for all but the simplest sagas because it
   avoids cyclic dependencies, reduces coupling, and localises the coordination logic
   (P036).

6. **Sequence a monolith migration.** When extracting sagas from a monolith, order
   the extractions so the monolith only ever executes *retriable* transactions, which
   never need a compensating transaction — this minimises changes to the hard-to-test
   monolith (C00217, P133).

7. **State the residual trade-off.** Make explicit that the design must accept
   eventual consistency across the participating services (P001).

8. **Hand off.** The architecture owner decides and implements; this skill informs.

## Inputs

- **Required:** the operation that must span services, the services/aggregates it
  touches, and the consistency and concurrency constraints.

## Output

A recommended saga (its local transactions and compensations), the coordination
style with justification, the countermeasures for the isolation anomalies that
apply, the extraction ordering if migrating a monolith, and an explicit statement of
the eventual-consistency consequence.

## References

- `references/saga-countermeasures-checklist.md` — the six countermeasures.
- `references/microservice-pattern-language-map.md` — the Data-group patterns.

## Provenance

Tier 2. Grounded in principles P001 (Saga not 2PC; eventual consistency), P047
(compensating transactions), P070 (lack of isolation), P014 (countermeasures), P036
(choreography vs. orchestration), P060 (choreography atomicity), P133 (retriable-only
monolith), and P120 (database per service), and in claims from
`chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson, Manning
2018, `distillation-only`). No verbatim quotation.
