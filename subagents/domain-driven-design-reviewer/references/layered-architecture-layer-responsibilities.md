---
name: layered-architecture-layer-responsibilities
kind: reference
status: ready
provenance:
  principles:
  - P017
  - P018
  - P027
  - P015
  - P003
  claims:
  - C00066
  - C00067
  - C00068
  - C00072
  - C00076
  - C00121
  - C00122
  - C00123
  - C00124
  - C00125
  - C00180
  - C00181
  evidence:
  - E00035
  - E00036
  - E00037
  - E00038
  - E00039
  - E00076
  - E00077
  - E00078
  - E00079
  - E00080
  - E00112
  - E00113
  source_anchors:
  - 9e0c1e6c6dd6-c0003
  - 9e0c1e6c6dd6-c0005
  - 9e0c1e6c6dd6-c0006
  - 9e0c1e6c6dd6-c0009
  authored_from_digest: 056804450e6903d065a979e11579d8a311e512633a34a1bcde18a94cbe6cfb6b
---

# Layered Architecture — Layer Responsibilities

A complex domain-driven application is partitioned into four conceptual layers. Each layer
has cohesive responsibilities and depends only on the layers below it. The Domain layer is
the load-bearing isolation boundary: all domain logic lives there and nowhere else.

## Layer summary table

| Layer | Core responsibility | Must NOT do | Review red-flags |
|---|---|---|---|
| **User Interface (Presentation)** | Present information to users; interpret and route user commands. | Contain business rules; couple directly to domain internals or infrastructure concerns. | Business conditions (`if order.status == ...`) in controllers or view models; domain objects constructed or mutated in UI handlers. |
| **Application** | Coordinate application activity; direct work to the Domain layer; track the progress of an application-level task. | Hold business logic; own or mutate the state of business objects. | Service methods that perform domain calculations rather than delegating to domain objects; transaction scripts that bypass the model. |
| **Domain** | Express the domain model: domain concepts, business rules, and the lifecycle state of business objects. Persistence of business objects is delegated outward to Infrastructure. | Perform infrastructure activities (database calls, network I/O, file access); import or depend on UI or application-layer concerns. | Domain classes that import ORM types, SQL builders, or HTTP clients directly; domain methods that trigger side-effects outside the model boundary. |
| **Infrastructure** | Support all other layers: inter-layer communication, persistence of business objects, libraries used by the UI, and external system adapters. | Embed domain rules or business decisions. | Persistence adapters that contain conditional business logic; infrastructure classes that manipulate domain invariants directly. |

## Dependency and isolation rules

- Layers depend downward only. Upper layers call lower layers; lower layers must not call
  upward.
- The Domain layer must be fully insulated from display logic, storage concerns, and
  application task-management duties. This isolation is what allows the domain model to
  evolve into a rich, knowledge-capturing design.
- Entangled layers — where domain code is mixed into UI, application, or infrastructure
  classes — make business logic hard to locate and change, allow superficial UI edits to
  accidentally alter business rules, and obstruct automated testing.
- The Application layer acts as a coordinator: it retrieves domain objects through
  Infrastructure (via Repositories), invokes the relevant domain methods, and then
  persists the updated state back through Infrastructure. Business decisions are made by
  domain objects, not by the Application layer.

## Compliance check cues

When a layer violation is found, name the specific element, the layer it currently occupies,
and the layer it belongs in. Common patterns:

- A business rule embedded in a REST controller or UI widget belongs in the Domain layer.
- A SQL query or ORM call inside a domain object should be delegated to Infrastructure via
  a Repository interface.
- Domain logic placed in an application service should be extracted to the appropriate
  domain Entity, Value Object, or Domain Service.
- Infrastructure code that makes domain decisions should have those decisions moved to
  the Domain layer, with the Infrastructure class receiving only the outcome.

## Provenance

Grounded in principles P017, P018, P027, P015, P003 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0003`, `9e0c1e6c6dd6-c0005`, `9e0c1e6c6dd6-c0006`, `9e0c1e6c6dd6-c0009`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
