---
name: clean-architecture-dependency-rule
kind: reference
status: ready
provenance:
  principles:
  - P040
  - P041
  - P016
  - P042
  - P043
  - P044
  claims:
  - C00473
  - C00477
  - C00359
  - C00394
  - C00364
  - C00442
  - C00374
  - C00375
  evidence:
  - E00105
  - E00108
  - E00079
  - E00086
  - E00080
  - E00100
  - E00081
  - E00082
  source_anchors:
  - 91e37e1ca511-c0006
  - 91e37e1ca511-c0001
  - 91e37e1ca511-c0002
  - 91e37e1ca511-c0004
  authored_from_digest: b6a94cb6f41308561979e338a799ec5b05bbd92440445a348daa1782f663d214
---

# Clean Architecture: the Dependency Rule and details-as-plugins

The dependency-direction rules a reviewer checks, and the checklist for keeping infrastructure at
the edges. From *Clean Architecture* (Robert C. Martin).

## The two dependency rules

| Rule | Statement | Violation looks like |
|------|-----------|----------------------|
| **The Dependency Rule** | Source-code dependencies must point **only inward** — from lower-level mechanisms toward higher-level policy. Inner business-rule layers know nothing of the outer layers that use them. | A business-rule module that imports or names a concrete outer detail (DB, UI, framework). |
| **Dependency Inversion (DIP)** | High-level policy must **not** depend on low-level detail; both depend on **abstractions**, so volatile implementations can change without disturbing stable business rules. | Policy depending directly on a concrete class instead of an abstraction it owns. |

## Details belong at the edges as plugins

The architecture treats infrastructure as detail to be kept outside boundaries, so business rules
do not depend on it and the decision can be deferred or changed.

| Detail | Stance | Why |
|--------|--------|-----|
| **The database** | A **detail**; treat the data store as a plugin behind a boundary. | So business rules do not depend on a particular database engine or schema. |
| **Frameworks** | **Details**; keep them at arm's length, do not "marry" a framework. | Marrying a framework couples durable business rules to a third party's volatile decisions. |
| **The web / delivery mechanism** | A **detail** at the edge. | So business rules do not depend on how they are delivered. |

## Reviewer checklist

- [ ] Are business rules (policy) separated from mechanisms (detail)?
- [ ] Do all dependencies crossing that line point **inward** toward policy?
- [ ] Where policy uses detail, does policy depend on an **abstraction it owns** (DIP)?
- [ ] Is the database a **plugin behind a boundary**, not embedded in domain classes?
- [ ] Are frameworks kept **at arm's length**, not inherited/imported throughout the rules?
- [ ] For each violation: is the **coupling consequence** named and an **abstraction** proposed to
      flip the arrow inward, with the indirection trade-off stated?

## Provenance

Distilled from principle(s) **P034/P035/P022/P036/P037/P044**, claims **C01246/C01250/C01132/C01167/C01215/C01216**, evidence **E00228/E00229/E00207/E00213/E00225/E00226**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
