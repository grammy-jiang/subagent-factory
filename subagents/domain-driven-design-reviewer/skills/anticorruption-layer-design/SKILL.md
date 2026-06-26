---
name: anticorruption-layer-design
kind: skill
status: ready
provenance:
  principles:
  - P012
  claims:
  - C084
  - C085
  source_anchors:
  - domaindrivendesignqu-20260612231910-h0059
  authored_from_digest: b558d9bf9a91653ff3340a98d134a7f855f3c28e16fa776c573ed8071736d989
---

# Anticorruption Layer Design

## Purpose

Guide and critique the design of an Anticorruption Layer (ACL) — the isolation boundary that
protects a client domain model from being distorted by an external or legacy system's model.
The ACL translates between the two models in both directions, presenting all external concepts
in the client's own terms so the client model stays coherent and internally consistent (P012,
C084).

## When to use

- A team is integrating with a legacy system or external service whose terminology, structures,
  or semantics differ from the client model and would alter it if absorbed directly (P012).
- A downstream team cannot influence or change the upstream supplier's API and must therefore
  shield its own model from upstream design decisions (P012).
- An existing integration shows signs of model leakage: external identifiers, external status
  codes, or external object structures appearing untranslated in domain-layer classes.

Do not apply this skill when:

- The two contexts share a Shared Kernel and their models are intentionally aligned — no
  translation boundary is needed (P012).
- The team has made a deliberate Conformist decision to adopt the upstream model as-is — the
  ACL would duplicate effort without adding isolation value (P012).

## Procedure

**Step 1 — Establish the need for an ACL.**

Confirm that the integration genuinely risks external-model concepts entering the client model.
Check whether the supplier model uses different names for equivalent concepts, different
granularity, or different invariants. If the external model is compatible and the team has
accepted a Conformist stance, redirect to Context Map pattern selection instead.

**Step 2 — Define the Service interface in client terms.**

Design the ACL surface that the client model will call. The interface must speak exclusively in
the client model's language: client-side entity identifiers, client-side value types, and
client-side operation names. No external identifier, type, or concept should appear in this
interface (C084).

**Step 3 — Place a Facade over the external system.**

Wrap the external system's interface in a Facade that simplifies and narrows the portion of
the external system the ACL needs to reach. The Facade has one responsibility: present a
clean, manageable view of the external system to the layer's internal components. When the
external interface is large or complex, the Facade also absorbs that complexity so downstream
components do not have to (C085).

**Step 4 — Add an Adapter between the Facade and the Service.**

The Adapter converts the simplified external interface (from the Facade) into the interface
the client-side Service implementation expects. Each Service in the ACL should have its own
Adapter; do not route multiple Services through a single shared Adapter, as that leads to
mixed and cluttered responsibilities (C085).

**Step 5 — Add a Translator for object and data conversion.**

Introduce a Translator component that converts between external data structures or objects and
the corresponding client-model types. The Translator handles the semantic mapping: it knows
what an external concept means in client terms and constructs the appropriate client-model
Value Objects or Entity references. It does not hold state (C085).

**Step 6 — Verify translation completeness.**

Walk each path through the ACL and confirm that no untranslated external concept crosses into
the client model. Checks to perform:

- No external identifier type appears in client-side method signatures or return types.
- No external enumeration or status code is used directly in domain logic.
- No external aggregate or data-transfer object is stored in or returned from a domain
  Repository.
- The client model compiles and its tests pass without any import of external-system types.

**Step 7 — Assess structural fit.**

Review the overall composition:

- Each client-facing Service is backed by exactly one Adapter and one Translator.
- A single Facade covers the external system; it is not bypassed.
- If multiple Services share a Facade, confirm the Facade does not leak cross-Service coupling.
- If the external interface is particularly volatile, note that the Facade insulates all
  internal components from churn; document the expected rate of external interface change.

**Step 8 — Record findings.**

Produce a structured output (see Output section) for the caller.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Client domain model | Yes | Class diagram, code, or written description of domain-layer types |
| External/legacy system interface | Yes | API contract, shared DB schema, or protocol specification |
| Integration requirements | Yes | Which concepts and operations must cross the boundary |
| Context Map | Recommended | Clarifies the relationship type (Customer-Supplier, Conformist, etc.) so the ACL decision is justified |

## Output

A structured review or design covering:

1. **ACL necessity verdict** — whether an ACL is warranted given the relationship type and
   integration risk; if not, the recommended alternative pattern.
2. **Service interface specification** — operation names and types in client-model terms.
3. **Component composition** — how the Service, Facade, Adapter, and Translator fit together;
   one Adapter per Service rule applied.
4. **Translation completeness findings** — any external concept found crossing the boundary
   untranslated, each accompanied by a corrective step naming the component that should absorb
   the translation.
5. **Risk notes** — external interface volatility, missing tests on the Facade boundary, or
   structural gaps in the current design.

## References

- `references/context-map-pattern-catalogue.md` — Anticorruption Layer in the full Context
  Map pattern catalogue; adjacent patterns (Customer-Supplier, Conformist, Separate Ways).
- `references/building-block-pattern-summaries.md` — Service definition (stateless, not on
  Entity/Value Object, refers to domain objects; P006) applicable to the ACL Service surface.

## Provenance

Grounded in Avram & Marinescu, "Domain-Driven Design Quickly" (InfoQ, 2006), section
"Anticorruption Layer" within the "Preserving Model Integrity" chapter.
Source anchor: `domaindrivendesignqu-20260612231910-h0059`.
Principle P012; claims C084 (evidence E036), C085 (evidence E045).
Source rights: `distillation-only` — all content paraphrased, no verbatim passages.
