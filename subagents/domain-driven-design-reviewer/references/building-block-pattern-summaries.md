---
name: building-block-pattern-summaries
kind: reference
status: ready
provenance:
  principles:
  - P043
  - P044
  - P045
  - P015
  - P008
  - P046
  - P047
  - P004
  - P007
  claims:
  - C00085
  - C00086
  - C00087
  - C00088
  - C00096
  - C00099
  - C00100
  - C00101
  - C00102
  - C00103
  - C00104
  - C00106
  evidence:
  - E00048
  - E00049
  - E00050
  - E00051
  - E00059
  - E00060
  - E00061
  - E00062
  - E00063
  - E00064
  - E00065
  - E00066
  source_anchors:
  - 9e0c1e6c6dd6-c0004
  - 9e0c1e6c6dd6-c0005
  authored_from_digest: 7907beb87aff35cd9d88455baec2dcf4f0c38f986bb72849abf3f1dcc839427b
---

# Building Block Pattern Summaries

Quick-reference catalogue of the seven tactical building blocks of model-driven design.
Use it to classify a domain element, recall the governing rule, and spot review red-flags.

## Pattern Catalogue

| Pattern | Intent | Identity / Equality | When to use | Review red-flags |
|---------|--------|---------------------|-------------|-----------------|
| **Entity** | A domain object defined by who or what it is rather than by its attributes; it has a thread of continuity across state changes. | Has a unique identity; mutable over its lifetime. Two objects sharing the same identity are the same object regardless of attribute differences. | When the domain object must be tracked individually across transactions or time (e.g. a customer, an order). | Equality implemented by comparing attribute values rather than identity; no unique identity operation defined; class carries no life-cycle behavior. |
| **Value Object** | An object that describes an aspect of the domain purely through its attributes and carries no individual identity. | No identity; equality is purely attribute-based. Must be immutable: a new instance is created whenever a different value is needed. | When only the measurements or descriptors matter, not which instance holds them (e.g. a money amount, a postal address). | Mutation methods on a Value Object; shared Value Object that can be modified in place; class has an unnecessary surrogate key. |
| **Service** | A stateless domain operation that does not naturally belong to any single Entity or Value Object. | No internal state between calls. | When a significant domain behavior spans several domain objects and has no natural home on any one of them. The three-criteria test: (1) the operation refers to a domain concept not housed in an Entity or Value Object; (2) it operates on other domain objects; (3) it is stateless. | Service that stores state; Service that replaces an operation properly belonging on an Entity; Service placed in the Application layer when it contains domain logic. |
| **Aggregate** | A cluster of associated domain objects treated as a single unit for data changes, with one root Entity controlling all access and enforcing invariants. | Root Entity has global identity; interior Entities have local (Aggregate-scoped) identity only; Value Objects have no identity. External references must target the root exclusively. | When a group of objects must change together under a single transactional invariant. | External code holding a direct reference to an internal (non-root) object; a Repository for a non-root object; invariants asserted in client code rather than inside the root. |
| **Factory** | An encapsulation of the knowledge needed to construct complex Aggregates or objects, producing them atomically and fully valid. | The Factory itself may have no domain role beyond creation. | When constructing an Aggregate requires significant knowledge of its internals, many invariants must be satisfied, or multiple related objects must be created together. Simple construction does not need a Factory. | Complex multi-step construction scattered across constructors or client code; partially-created objects returned without raising an exception on failure; Factory used for reconstitution of persisted objects (that is a Repository concern). |
| **Repository** | An object that presents the illusion of an in-memory collection of all persisted objects of a given type, encapsulating all retrieval logic. | The interface is a pure domain concept; the implementation may contain infrastructure details. | Provide one for each Aggregate root that requires global access. Operations include add, remove, and criteria-based selection. | Domain-layer code calling an ORM, SQL builder, or raw data store directly; Repository exposing storage-technology terms in its interface; Repository provided for a non-root internal object; a Repository used to create new objects (that is Factory's role). |
| **Module** | A named grouping of cohesive domain concepts and tasks that organizes the model and reduces cognitive load. | Not an object; a structural container. | When related concepts and behaviors can be grouped under a meaningful domain name, reducing coupling between groups while keeping cohesion within. | Module names that reflect technical layers (e.g. "utils", "helpers") rather than domain concepts; modules that split concepts that belong together; module names not part of the ubiquitous language. |

## Classification Decision Aid

When classifying a new domain element, apply the following order:

1. Does the domain require tracking this object individually over time or across transactions? If yes, it is an **Entity**.
2. Does only the value of its attributes matter, with no need for individual tracking? If yes, it is a **Value Object**.
3. Does a domain behavior span multiple objects and carry no natural home on any one of them? If yes, it is a **Service** (provided it is stateless and operates on domain concepts).
4. Must a cluster of objects change together under shared invariants? Define an **Aggregate** with a single root Entity.
5. Is construction complex enough to require domain knowledge or to span multiple invariants? Encapsulate it in a **Factory**.
6. Must a client obtain references to pre-existing Aggregate roots? Provide a **Repository** for the root.

Prefer Value Objects over Entities: unnecessary entities add tracking overhead and complicate equality semantics.

## Provenance

Grounded in principles P043, P044, P045, P015, P008, P046, P047, P004, P007 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0004`, `9e0c1e6c6dd6-c0005`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
