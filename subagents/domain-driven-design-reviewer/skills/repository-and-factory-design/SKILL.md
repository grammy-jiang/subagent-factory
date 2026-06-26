---
name: repository-and-factory-design
kind: skill
status: ready
provenance:
  principles:
  - P046
  - P047
  - P028
  - P008
  claims:
  - C00165
  - C00166
  - C00167
  - C00168
  - C00150
  - C00151
  - C00152
  - C00153
  - C00154
  - C00155
  - C00158
  - C00159
  evidence:
  - E00108
  - E00109
  - E00110
  - E00111
  - E00099
  - E00100
  - E00101
  - E00102
  - E00103
  - E00104
  - E00105
  - E00106
  source_anchors:
  - 9e0c1e6c6dd6-c0008
  - 9e0c1e6c6dd6-c0007
  authored_from_digest: 843d5beb41fd20975c8070760a127e28a9efd01f81950820b7a198455f7e90db
---

# Repository and Factory Design

## Purpose

Apply the two life-cycle patterns that keep creation and retrieval concerns out of
the domain model. A Factory encapsulates the complex knowledge required to build a
valid Aggregate or object. A Repository encapsulates all logic needed to obtain
references to pre-existing domain objects. Together they ensure domain classes
express domain concepts rather than construction or persistence mechanics.

## When to use

- Reviewing creation logic for an Aggregate whose initialization involves multiple
  steps, inter-object wiring, or invariants that must hold from the very first
  moment — situations where a plain constructor would force clients to carry
  internal structural knowledge.
- Checking whether a partially-constructed object can escape creation: if the
  Factory does not raise an exception on failure it is defective.
- Reviewing domain-layer classes for direct calls to ORMs, SQL builders, or raw
  data stores instead of going through a Repository.
- Verifying that Repository interfaces are expressed in domain terms and that
  Repositories exist only for Aggregate roots, not for their internal members
 .
- Evaluating whether direct database access has caused domain logic to migrate
  into queries, degrading Entities and Value Objects into mere data containers
 .

## Procedure

### Step 1 — Decide whether a Factory is warranted

Examine the candidate creation site. A Factory is warranted when:

- Construction requires knowledge of the Aggregate's internal structure or wiring
  that no client should possess.
- The process involves building multiple related objects as a coordinated unit.
- There are invariants that must be satisfied at the moment the object first
  exists.

A plain constructor is sufficient when construction is not complex, creates no
other domain objects, and when the client legitimately needs to choose the
implementation or strategy (C052 is supporting context; guard against over-applying
Factories to simple cases).

### Step 2 — Check atomicity and invariant enforcement

Confirm that the Factory creates the object as a complete, valid unit in a single
logical operation. If any mandatory invariant cannot be satisfied during
construction, the Factory must raise an exception; it must never return a partial
or invalid object. Flag any creation path that could yield an object in an
incomplete state.

### Step 3 — Assess Factory placement

Distinguish the two placement options:

- **Factory Method on the Aggregate root**: suitable when the object being created
  is a member of that same Aggregate and creation is conceptually initiated by the
  root.
- **Standalone Factory class**: appropriate when the construction of the whole
  Aggregate involves a complex series of steps or the simultaneous creation of
  many related objects.

The Factory's interface must hide the concrete classes being assembled; clients
receive the product through its domain type, not its implementation type.

### Step 4 — Distinguish creation from reconstitution

Verify that the design distinguishes fresh-object creation from rebuilding a
persisted object. A reconstituted object already carries an identity; invariant
violations discovered during reconstitution should be repaired rather than thrown,
to prevent data loss. A brand-new object must fail loudly on any breach (C053 is
supporting context for this distinction).

### Step 5 — Check Repository scope

Confirm that a Repository exists only for Aggregate roots that genuinely require
direct access. Internal Aggregate objects must be reached by traversal
through the root, never by a dedicated Repository. A Repository for a non-root
object is a boundary violation and must be flagged.

### Step 6 — Verify domain-pure interface

Inspect the Repository interface. It must be expressed in domain terms — add,
remove, and criteria-based select operations that present the illusion of an
in-memory collection — regardless of how the implementation is wired to a
data store. Infrastructure types (ORM sessions, SQL builders,
connection strings) must not appear in the interface.

### Step 7 — Detect direct database access in the domain layer

Search for domain-layer classes that call persistence infrastructure directly. When
clients bypass the Repository and access the database themselves, domain logic
gravitates into queries and client code; Entities and Value Objects become data
containers and the model loses relevance. Each such call is a finding
requiring a corrective step.

### Step 8 — Confirm Factory/Repository separation

The two patterns must not be conflated. A Factory creates a new object; a
Repository retrieves an existing one. The correct collaboration is: a Factory
builds the object and then the caller hands it to the Repository for storage.
Any class that both constructs objects and manages their retrieval violates the
single-responsibility boundary.

## Inputs

- Aggregate and Entity class definitions, including their constructors and any
  builder or factory methods.
- The current mechanism by which domain objects are retrieved (Repository, direct
  ORM call, service locator, or other).
- Descriptions of the invariants that must hold for each Aggregate from the moment
  it exists.
- Persistence technology in use (to judge whether infrastructure detail is leaking
  into the domain interface).

## Output

Structured findings for the Factory and Repository review areas, each including:

- The affected model element (class name, method, or call site).
- The violated principle (P008 or P009) and the supporting claim ID.
- A severity assessment: whether the defect exposes invalid objects, degrades
  model relevance, or represents a boundary leak.
- One corrective step: introduce Factory / raise exception on failure / expose
  domain-only Repository interface / remove direct persistence call / split
  Factory from Repository responsibilities.

For conformant designs, enumerate which checks were applied and found passing.

## Provenance

Grounded in principles P046, P047, P028, P008 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0008`, `9e0c1e6c6dd6-c0007`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
