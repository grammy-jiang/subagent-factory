---
name: context-map-pattern-catalogue
kind: reference
status: ready
provenance:
  principles:
  - P011
  - P012
  claims:
  - C070
  - C072
  - C077
  - C079
  - C080
  - C081
  - C082
  - C083
  - C084
  - C085
  - C086
  - C087
  source_anchors:
  - domaindrivendesignqu-20260612231910-h0049
  - domaindrivendesignqu-20260612231910-h0050
  - domaindrivendesignqu-20260612231910-h0054
  - domaindrivendesignqu-20260612231910-h0056
  - domaindrivendesignqu-20260612231910-h0058
  - domaindrivendesignqu-20260612231910-h0059
  - domaindrivendesignqu-20260612231910-h0060
  - domaindrivendesignqu-20260612231910-h0062
  authored_from_digest: d4ede0dbf2fc03cfa6573b05840f45742a90c9ba34c2773cc365776d8dd0c32d
---

# Context Map Pattern Catalogue

A **Context Map** names all Bounded Contexts in a project and documents the
relationship between each pair of contexts (C077). It must be shared and
understood by every team member so that integration boundaries are unambiguous.
Use the table below to select the integration pattern that fits the team and
organisational situation. Framing rules follow the table.

## Pattern Catalogue

| Pattern | Team relationship | Intent | When to apply | Review red-flags |
|---------|------------------|--------|---------------|-----------------|
| **Shared Kernel** | Two teams agree to co-own a named subset of the domain model, code, and database design (C079). | Avoid duplication between closely related teams while keeping full continuous integration of the whole model impractical. | Teams are tightly coupled organisationally; the shared subset is clearly bounded and small. | Changes to the kernel made unilaterally without consulting the partner team; integration less frequent than weekly; no shared automated test suite covering the kernel (C080). |
| **Customer-Supplier** | One context (supplier) feeds another (customer) in a one-way dependency; supplier sets the delivery schedule but the interface must meet customer requirements (C081). | Give the customer team a defined interface and a voice in the supplier's roadmap, protected by jointly authored automated acceptance tests in the supplier's CI pipeline (C082). | The two models differ; a Shared Kernel is technically or conceptually inappropriate; teams are under shared management. | Supplier changes the API without running customer acceptance tests; no automated contract tests in supplier CI; supplier team has no organisational incentive to serve the customer, and no escalation path exists (C083). |
| **Conformist** | Customer team fully adopts the supplier's model with no modifications. | Eliminate translation cost when the supplier's model is sound and the supplier has no motivation to serve the customer specially. | Supplier model quality is high enough to build on without corruption; customer team accepts loss of model independence. | Conformist adopted to avoid translation work when the supplier model is poor — this leaks a bad model into the customer context; prefer Anticorruption Layer or Separate Ways in that case (C083). |
| **Anticorruption Layer** | Client builds a translating layer that presents external or legacy concepts in the client's own terms (C084). | Keep the client model pure and self-consistent when integrating with a system whose model would otherwise corrupt it. | Integration with a legacy or external system is required; absorbing that system's terminology or structure would degrade the client model's clarity and consistency. | Direct use of external model types or terminology in the client domain layer; Facade, Adapter, and Translator objects missing or conflated; layer grows so large it becomes a second domain model (C085). |
| **Separate Ways** | No integration; each context maintains a fully independent model and implementation (C086). | Allow teams to work freely with their own technology and design choices when integration costs exceed the benefits. | The requirements handled by each context overlap minimally; coordination overhead outweighs any value of integration. | Decision made to avoid integration effort without analysing future recombination risk; models developed separately are extremely difficult to re-integrate later (C086). |
| **Open Host Service** | One subsystem exposes a published, stable protocol as a set of Services that any client can consume (C087). | Avoid per-client translation layers when many contexts must integrate with a single provider; keep the shared protocol simple by routing idiosyncratic needs through one-off translators rather than widening the core protocol. | One context serves many downstream clients; per-client translation would duplicate effort and slow the provider team. | Idiosyncratic special-case needs are added to the shared protocol instead of handled by a dedicated translator, causing protocol bloat (C087). |

## Framing Concepts

**Bounded Context** (P011, C072): the explicitly delimited scope within which a
single domain model applies, defined in terms of team organisation, application
boundaries, code bases, and database schemas. Within those bounds the model
must remain strictly consistent; the same term used in two different contexts is
not assumed to carry the same meaning across the boundary.

**Multi-team projects** (C070): in large projects with multiple teams, attempting
to maintain one unified enterprise-wide model is unworkable. The model must be
consciously divided into well-integrated smaller models, each with clear
boundaries and precisely specified relationships — recorded in the Context Map
(C077).

**Continuous Integration** applies *within* a Bounded Context to keep the model
unified inside its bounds (not between neighbouring contexts). It requires
frequent merges, an automated build, and a test suite run on every build.

## Provenance

Derived from "Domain-Driven Design Quickly" (Avram & Marinescu, InfoQ 2006),
"Preserving Model Integrity" chapter, source
`domaindrivendesignqu-20260612231910`, anchors h0049-h0050, h0054, h0056,
h0058-h0060, h0062. Rights status: `distillation-only` — paraphrased
throughout; no verbatim passages. Grounded in principles P011 and P012 and
evidence records E035, E036, E043, E044, E045.
