---
name: enterprise-and-integration-patterns-map
kind: reference
status: ready
provenance:
  principles:
  - P051
  - P052
  - P053
  - P027
  - P007
  - P024
  claims:
  - C01485
  - C01486
  - C01663
  - C01675
  - C01622
  - C01624
  - C01500
  - C01503
  evidence:
  - E00234
  - E00235
  - E00251
  - E00252
  - E00246
  - E00247
  - E00238
  - E00239
  source_anchors:
  - be84e4ec4c9d-c0000
  - be84e4ec4c9d-c0003
  - be84e4ec4c9d-c0004
  - be84e4ec4c9d-c0002
  authored_from_digest: 05f5b2bbce91c3a00997d8087086f1d9da2319e07d9f0ce9784b1fd7ccdadd38
---

# Enterprise and integration patterns map

A map of the enterprise-application structure patterns (from *Patterns of Enterprise Application
Architecture*, Fowler) and the application-integration trade-off (from *Enterprise Integration
Patterns*, Hohpe & Woolf), with the rule of thumb for choosing each.

## Enterprise application layering

| Layer | Responsibility |
|-------|----------------|
| **Presentation** | Handle interaction with users or external systems. |
| **Domain** | The business logic — the reason the application exists. |
| **Data source** | Talk to the database, messaging, and other infrastructure. |

**Rule of thumb:** Layering localizes change and lets each layer be reasoned about on top of a
coherent layer below — at the **cost of added indirection**. Use it where localized change is worth
that cost.

## Domain-logic organization — choose by complexity

| Pattern | Fits when business logic is… | Trade-off |
|---------|------------------------------|-----------|
| **Transaction Script** | Simple, mostly procedural, per use case. | Cheap to start; cost and duplication rise as logic grows. |
| **Domain Model** | Rich and interrelated. | Higher up-front cost; scales with complexity. |
| **Table Module** | Table/record-set oriented (one class per table). | A middle option that fits table-centric logic and tooling. |

**Rule of thumb:** Pick by the **complexity of the business logic**, because each pattern's
cost-benefit shifts as the logic grows — not by habit.

## Domain ↔ relational mapping (structural patterns)

Isolate the in-memory domain from the relational schema with a mapping layer so the two evolve
independently.

| Pattern | Role |
|---------|------|
| **Data Mapper** | A layer that moves data between objects and tables, keeping the domain ignorant of the database. |
| **Identity Field** | Carry the database primary key in the object to tie object identity to a row. |
| **Foreign Key Mapping** | Map object references to foreign-key relationships between tables. |

**Rule of thumb:** Specific pattern choice is situational; the goal is that the domain is **not
shaped by the schema**.

## Application integration trade-off (asynchronous messaging)

| Side | Factors |
|------|---------|
| **Benefits** | Loose coupling (applications need not be available at the same instant); reliable delivery (the message persists until consumed). |
| **Costs** | Loss of simple synchronous call semantics; harder debugging across the async boundary; must reason about eventual delivery and ordering. |

**Rule of thumb:** Choose the integration style **deliberately** for the context — do not default
to synchronous calls or to messaging — and name the residual consequence (e.g. eventual
consistency, ordering handling, or temporal coupling).

## Provenance

Distilled from principle(s) **P038/P039/P049/P021/P005/P019**, claims **C01367/C01368/C01545/C01557/C01504/C01506**, evidence **E00238/E00239/E00251/E00252/E00246/E00247**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
