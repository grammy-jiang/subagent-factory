---
name: pattern-forces-and-tradeoffs-table
kind: reference
status: ready
provenance:
  principles:
  - P018
  - P069
  - P126
  - P054
  - P107
  claims:
  - C00021
  - C00022
  - C00066
  - C00067
  - C00037
  - C00057
  - C00058
  - C00302
  - C00303
  source_anchors: []
  authored_from_digest: e60bf3441fe8292976511bf7aff68ab80ae1454991547fc67989f702807c4d1e
---

# Pattern Forces and Trade-offs Table

A bare pattern name is not advice. For every recommendation, state the problem the
pattern solves, the forces it resolves, AND the drawback / residual consequence it
carries, then weigh it against the caller's forces (P069, P018). This table is the
quick-reference for that discipline across the catalogue's most-asked patterns.

## How to read

- **Problem / forces** — the recurring situation and the competing pressures the
  pattern addresses.
- **Benefit** — what choosing it buys.
- **Drawback / residual** — what it costs or the consequence the design must accept.

## Architecture-level

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| Microservice architecture | A large, complex app strains a single deployable | Independent deployability, scalability, fault isolation, tech diversity | A distributed system: harder IPC, transactions, queries, ops |
| Monolithic architecture | Small/simple app, low overhead wanted | Simple to build, test, deploy | Becomes "monolithic hell" as it grows large/complex |

## Data — consistency

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| Database per service | Loose coupling vs. shared access | Each service owns its data; independent evolution | Forces sagas, API composition / CQRS; eventual consistency |
| Shared database | Simplicity vs. coupling | Simple, ACID across services | Tight build/runtime coupling; generally an anti-pattern |
| Saga | Cross-service consistency without 2PC | Consistency via local transactions + messaging | ACD (no isolation) → needs countermeasures; eventual consistency |

## Data — queries

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| API composition | Query spans services; simplicity wanted | Simplest cross-service query | Overhead; reduced availability; inefficient large in-memory joins |
| CQRS | API composition too slow / event-sourced store | Efficient, diverse queries | Added complexity; replication lag → eventually consistent view |

## Communication

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| Remote procedure invocation | Immediacy vs. coupling | Simple, familiar request/response | Couples caller availability to callee (caller blocks) |
| Messaging | Availability and decoupling | Sender/receiver need not both be up | Messaging-infra complexity; delivery semantics to handle |
| Circuit breaker | A dependency may be slow/down | Stops cascading failure | Extra moving part; tuning thresholds/timeouts |

## External API

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| API gateway | External clients vs. many services | Single entry point; routing, composition, auth offload | Can become a shared development bottleneck |

## Deployment

| Pattern | Problem / forces | Benefit | Drawback / residual |
|---|---|---|---|
| Service per Container | Isolation vs. overhead | Most VM isolation; faster startup, lower overhead | Container platform to operate |
| Service per VM | Strong isolation | Strongest isolation; full stack encapsulation | Heavyweight; slower startup, higher overhead |
| Serverless deployment | No infra mgmt; bursty/low-idle load | Scales to zero; no servers to manage | Cold starts; constrained runtime/execution model |

## Provenance

Tier 2 reference. Grounded in principles P069/P018 (state forces and drawbacks, never
a bare name), P126 (evaluate by quality attributes), P054 (the costs of
microservices), and P107 (API composition drawbacks), and in claims C00021–C00022,
C00066–C00067, C00037, C00057–C00058, C00302–C00303 from
`chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson, Manning
2018, `distillation-only`). No verbatim quotation.
