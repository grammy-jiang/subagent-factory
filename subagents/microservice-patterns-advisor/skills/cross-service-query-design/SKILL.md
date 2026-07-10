---
name: cross-service-query-design
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P024
  - P107
  - P136
  - P010
  - P034
  claims:
  - C00008
  - C00073
  - C00302
  - C00303
  - C00304
  - C00305
  - C00301
  - C00309
  - C00310
  - C00314
  source_anchors: []
  authored_from_digest: a8a1efd496a433da1ee39fd2c93e6c34c410ba2987c63e5cf793ae122b2903e0
---

# Cross-Service Query Design

## Purpose

Guide a caller who must implement a query whose data is owned by more than one
service, choosing between API composition and CQRS. This is the specialised
walkthrough for the **Data / queries** group.

## When to use

Use when a query needs data from several services, or when a read view must be
maintained from events. Do not use for cross-service *writes/consistency* (route to
`saga-transaction-design`) or for a query satisfiable from one service's own data.

## Procedure

1. **Recognise the query as a distributed-data challenge.** Because a service's data
   is reachable only through its API, you cannot run a distributed query against its
   database; queries that span services use one of two patterns — API composition or
   CQRS (C00008, C00073, P002).

2. **Start with API composition.** A composer invokes each data-owning service and
   combines the results; it is the simplest approach and preferred whenever possible
   (P002). Invoke independent providers in parallel (sequentially only when one
   result feeds another) using a reactive design such as CompletableFuture to
   minimise response time (C00301, P136).

3. **Name its drawbacks.** API composition adds overhead, reduces availability (which
   declines with the number of services), and lacks transactional consistency
   (C00302, P107). Improve availability by returning cached, possibly stale data or by
   omitting an unavailable non-critical provider so the client still gets a useful
   response (C00303).

4. **Switch to CQRS when composition is inefficient or insufficient.** Use CQRS —
   event-maintained read-only view databases — when API composition would require an
   expensive in-memory join, the owning service's store cannot efficiently support the
   query, or separation of concerns means the data owner should not implement a
   high-volume critical query; never build a query engine inside an API composer
   (C00304, C00305, P024).

5. **Structure CQRS as command and query sides.** The command side handles
   create/update/delete and publishes domain events; the query side is query-only and
   stays synchronised by subscribing to those events, optionally as query-only
   services for multi-service views (C00309, C00310, P034). A CQRS view module is a
   view database plus event handlers, a query API, and a data-access module (C00314,
   P010).

6. **State the CQRS trade-off.** The view is updated asynchronously, so it is
   eventually consistent and the design must tolerate replication lag; handle lag by
   returning a version token the client polls on, or by updating the UI from the
   command's result (P034). CQRS also adds moving parts and complexity — so use API
   composition whenever possible.

7. **Hand off.** The architecture owner decides and implements; this skill informs.

## Inputs

- **Required:** the query (what data, from which services), its volume/latency needs,
  and the freshness/consistency the caller can tolerate.

## Output

A recommended query approach (API composition or CQRS) with its drawback stated, a
parallel-invocation note for composition, and the eventual-consistency consequence
where CQRS applies — each tied to the caller's forces.

## References

- `references/microservice-pattern-language-map.md` — the Data-group query patterns.
- `references/pattern-forces-and-tradeoffs-table.md` — API composition vs. CQRS.

## Provenance

Tier 2. Grounded in principles P002 (queries as a distributed-data challenge; API
composition preferred), P024 (when to use CQRS), P107 (API composition drawbacks),
P136 (parallel composition), P010/P034 (CQRS view module and command/query sides),
from `chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson,
Manning 2018, `distillation-only`). No verbatim quotation.
