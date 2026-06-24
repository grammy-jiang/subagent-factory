---
name: gof-pattern-selection-guide
kind: reference
status: ready
provenance:
  principles:
  - P008
  - P025
  - P009
  - P013
  claims:
  - C00250
  - C00252
  - C00253
  - C00259
  - C00260
  - C00532
  - C00536
  - C00537
  - C00538
  - C00539
  - C00560
  - C00561
  - C00562
  - C00563
  - C00742
  - C00814
  source_anchors:
  - 0574f24ece08-c0002
  - 0574f24ece08-c0006
  - 5b1b9ca368a5-c0002
  - 5b1b9ca368a5-c0003
  - 5e67c59e0e18-c0003
  authored_from_digest: 01b376ec497ee54f270ae2d9fd89b37269084ae4af04e53080a034e4cb38ee56
---

# GoF Pattern-Selection Guide

A guide for locating a candidate design pattern once a real, recurring structural problem has
been confirmed. Use with `skills/select-design-pattern/`. A pattern is **not free**: applying
one that does not fit its problem adds needless indirection and complexity rather than removing
it, so confirm a recurring problem and prefer the simpler direct design before consulting this
guide (clm-079; PRC-023; PRC-007).

## What a pattern is

A design pattern names and abstracts the key aspects of a common design structure, making it a
reusable solution to a recurring problem within a particular context (clm-073; PRC-023). Every
pattern is fully characterised by four elements; evaluate a candidate against all four
(clm-074):

1. **Name** — the shared vocabulary for the structure.
2. **Problem and context** — the situation in which it applies.
3. **Solution** — the general arrangement of collaborating roles (interfaces, abstract classes,
   concrete implementations, and their relationships), not a concrete implementation.
4. **Consequences** — the trade-offs applying it entails.

## The three decoupling moves

Any pattern recommendation must satisfy these structural principles first; often they resolve
the problem on their own, with no named pattern required (clm-076; clm-077; clm-078; PRC-022):

- **Program to an interface, not an implementation** — clients depend on an abstract type so the
  concrete type can vary without affecting callers.
- **Favour object composition over class inheritance** — compose behaviour from objects to keep
  each class encapsulated and allow substitution at runtime.
- **Encapsulate the concept that varies** — identify what changes and isolate it behind a stable
  interface so the rest of the system is insulated.

## The catalogue: purpose × scope

The catalogue is organised along two axes that narrow the search before individual patterns are
examined (clm-075):

- **Purpose** — what the pattern does:
  - *Creational* — decouples clients from the classes they instantiate; controls which concrete
    type is created and how complex objects are assembled.
  - *Structural* — composes classes and objects into larger structures; adapts, wraps, or
    connects interfaces.
  - *Behavioural* — distributes responsibility and defines how objects collaborate; controls the
    flow of requests or which algorithm runs.
- **Scope** — *class* patterns fix relationships through inheritance at compile time; *object*
  patterns fix them through composition at runtime. When favouring composition over inheritance,
  prefer object-scope candidates (clm-077).

Use the grid to pick the one or two families whose purpose matches the confirmed problem, then
examine individual patterns within them. The canonical catalogue members, by family:

| Purpose | Catalogue members (by name) |
|---|---|
| **Creational** | Abstract Factory, Builder, Factory Method, Prototype, Singleton |
| **Structural** | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **Behavioural** | Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor |

> For the full problem/context, solution, and consequences of any member not detailed below,
> consult the source catalogue directly (`erich-gamma-richard-80cb534a`, `distillation-only` —
> read, do not quote). Match each candidate against its four elements as described above before
> recommending it.

## Worked pattern cards

Detailed cards for the patterns with direct grounding in this package's evidence. Each names the
variation point it encapsulates — the standard test for whether the pattern fits.

| Pattern | Family | Problem it addresses | Variation encapsulated | Grounding |
|---|---|---|---|---|
| **Strategy** | Behavioural / object | A family of interchangeable algorithms is needed and the algorithm should vary independently of the clients that use it | *Which algorithm runs*, placed behind a common interface | clm-080; PRC-022 |
| **Decorator** | Structural / object | Responsibilities must be added to an individual object dynamically, without subclassing every combination | *Which responsibilities wrap an object*, composed at runtime as a flexible alternative to subclassing | clm-081; PRC-022 |
| **Observer** | Behavioural / object | When one object changes state, an open-ended set of dependents must be notified and updated automatically | *Who depends on a subject's state*, via a one-to-many link that decouples subject from observers | clm-082; PRC-022 |

Each card illustrates the same rule: the pattern earns its place only when it encapsulates a
variation that is real and recurring in the present design. If no such variation exists, the
three decoupling moves — or a direct fix — are preferable (clm-079; PRC-023).

## Selection gate

Recommend a pattern only when the problem is confirmed and recurring (Step 1 of
`select-design-pattern`), the pattern's problem/context is a strong match, the solution fits
within a scope proportionate to the problem, and the structural benefit outweighs the
indirection it adds. Otherwise recommend direct decoupling or issue a refusal — never add a
pattern for sophistication or anticipated future extensibility (clm-079; PRC-023; PRC-007).

## Provenance

Derived from *Design Patterns: Elements of Reusable Object-Oriented Software* (Gamma, Helm,
Johnson, Vlissides, source `erich-gamma-richard-80cb534a`, `distillation-only`) via principles
PRC-022 and PRC-023 and their supporting claims (clm-073–clm-082), grounded in source anchors
`erich-gamma-richard-80cb534a-h0010`, `-h0012`, `-h0015`–`-h0019`, `-h0315`, `-h0629`, and
`-h0681`, as recorded in `principles/principles.yaml` and `analysis/claims.jsonl`. The catalogue
member names are the catalogue's own organisation by purpose and scope (clm-075); per-pattern
detail beyond the worked cards must be read from the source, not reproduced here. All content is
paraphrased; no verbatim source wording appears in this file.
