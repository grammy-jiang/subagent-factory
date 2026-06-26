---
name: context-map-pattern-catalogue
kind: reference
status: ready
provenance:
  principles:
  - P041
  - P001
  - P010
  - P011
  - P023
  - P032
  - P031
  - P038
  - P039
  claims:
  - C00329
  - C00330
  - C00331
  - C00332
  - C00196
  - C00197
  - C00200
  - C00351
  - C00352
  - C00353
  - C00354
  - C00355
  evidence:
  - E00184
  - E00185
  - E00186
  - E00187
  - E00119
  - E00120
  - E00121
  - E00199
  - E00200
  - E00201
  - E00202
  - E00203
  source_anchors:
  - 9e0c1e6c6dd6-c0017
  - 9e0c1e6c6dd6-c0009
  - 9e0c1e6c6dd6-c0010
  - 9e0c1e6c6dd6-c0019
  authored_from_digest: 4d1e3399f1bcca8f04185a463a1022e4dc8cb755c6f05dbe285c801c8c57e9e5
---

# Context Map Pattern Catalogue

A **Context Map** names all Bounded Contexts in a project and documents the
relationship between each pair of contexts. It must be shared and
understood by every team member so that integration boundaries are unambiguous.
Use the table below to select the integration pattern that fits the team and
organisational situation. Framing rules follow the table.

## Pattern Catalogue

| Pattern | Team relationship | Intent | When to apply | Review red-flags |
|---------|------------------|--------|---------------|-----------------|
| **Shared Kernel** | Two teams agree to co-own a named subset of the domain model, code, and database design. | Avoid duplication between closely related teams while keeping full continuous integration of the whole model impractical. | Teams are tightly coupled organisationally; the shared subset is clearly bounded and small. | Changes to the kernel made unilaterally without consulting the partner team; integration less frequent than weekly; no shared automated test suite covering the kernel. |
| **Customer-Supplier** | One context (supplier) feeds another (customer) in a one-way dependency; supplier sets the delivery schedule but the interface must meet customer requirements. | Give the customer team a defined interface and a voice in the supplier's roadmap, protected by jointly authored automated acceptance tests in the supplier's CI pipeline. | The two models differ; a Shared Kernel is technically or conceptually inappropriate; teams are under shared management. | Supplier changes the API without running customer acceptance tests; no automated contract tests in supplier CI; supplier team has no organisational incentive to serve the customer, and no escalation path exists. |
| **Conformist** | Customer team fully adopts the supplier's model with no modifications. | Eliminate translation cost when the supplier's model is sound and the supplier has no motivation to serve the customer specially. | Supplier model quality is high enough to build on without corruption; customer team accepts loss of model independence. | Conformist adopted to avoid translation work when the supplier model is poor — this leaks a bad model into the customer context; prefer Anticorruption Layer or Separate Ways in that case. |
| **Anticorruption Layer** | Client builds a translating layer that presents external or legacy concepts in the client's own terms. | Keep the client model pure and self-consistent when integrating with a system whose model would otherwise corrupt it. | Integration with a legacy or external system is required; absorbing that system's terminology or structure would degrade the client model's clarity and consistency. | Direct use of external model types or terminology in the client domain layer; Facade, Adapter, and Translator objects missing or conflated; layer grows so large it becomes a second domain model. |
| **Separate Ways** | No integration; each context maintains a fully independent model and implementation. | Allow teams to work freely with their own technology and design choices when integration costs exceed the benefits. | The requirements handled by each context overlap minimally; coordination overhead outweighs any value of integration. | Decision made to avoid integration effort without analysing future recombination risk; models developed separately are extremely difficult to re-integrate later. |
| **Open Host Service** | One subsystem exposes a published, stable protocol as a set of Services that any client can consume. | Avoid per-client translation layers when many contexts must integrate with a single provider; keep the shared protocol simple by routing idiosyncratic needs through one-off translators rather than widening the core protocol. | One context serves many downstream clients; per-client translation would duplicate effort and slow the provider team. | Idiosyncratic special-case needs are added to the shared protocol instead of handled by a dedicated translator, causing protocol bloat. |

## Framing Concepts

**Bounded Context**: the explicitly delimited scope within which a
single domain model applies, defined in terms of team organisation, application
boundaries, code bases, and database schemas. Within those bounds the model
must remain strictly consistent; the same term used in two different contexts is
not assumed to carry the same meaning across the boundary.

**Multi-team projects**: in large projects with multiple teams, attempting
to maintain one unified enterprise-wide model is unworkable. The model must be
consciously divided into well-integrated smaller models, each with clear
boundaries and precisely specified relationships — recorded in the Context Map
.

**Continuous Integration** applies *within* a Bounded Context to keep the model
unified inside its bounds (not between neighbouring contexts). It requires
frequent merges, an automated build, and a test suite run on every build.

## Provenance

Grounded in principles P041, P001, P010, P011, P023, P032, P031, P038, P039 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0017`, `9e0c1e6c6dd6-c0009`, `9e0c1e6c6dd6-c0010`, `9e0c1e6c6dd6-c0019`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
