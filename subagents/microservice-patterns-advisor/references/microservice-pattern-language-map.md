---
name: microservice-pattern-language-map
kind: reference
status: ready
provenance:
  principles:
  - P094
  - P096
  - P118
  - P069
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00108
  - C00021
  - C00022
  source_anchors: []
  authored_from_digest: 1df7404d6907fc0327bd19f14eafd9c8b6dd96dd30de7c81da9594f81f77c55a
---

# Microservice Pattern Language Map

The full pattern catalogue from the microservices pattern language (Chris
Richardson), organised into its groups. Each pattern is a named solution to a
recurring problem under specific forces; a pattern is chosen by matching the
caller's forces, not applied universally. Use this map to locate the group that
covers a stated concern, then read across to the candidate patterns in that
group. No pattern outside this map is part of the language — do not invent
names.

## Concern → group index

Start from the decision at hand and jump to the group that owns it.

| If the concern is about… | Go to group |
|---|---|
| Splitting an application into services; how big a service is; who owns it | Application architecture |
| Keeping data consistent across services, or querying data that spans services | Data |
| How services talk to each other and to external clients | Communication |
| How a service instance is located at runtime | Discovery |
| How service instances are packaged, placed, and run | Deployment |
| Seeing what a running system is doing; finding failures | Observability |
| Authenticating and authorising requests across services | Security |
| Verifying services in isolation and at their boundaries | Testing |

## Pattern catalogue by group

### Application architecture

The starting decisions: whether to use a microservice architecture at all, and
how to carve the application into services.

| Pattern | Concern it addresses |
|---|---|
| Monolithic architecture | Baseline alternative: one deployable unit |
| Microservice architecture | Structure the application as a set of independently deployable services |
| Decompose by business capability | Define service boundaries from business capabilities |
| Decompose by subdomain | Define service boundaries from DDD subdomains |
| Self-contained service | A service handles a request without synchronous calls to others |
| Service per team | Align a service's ownership with one team |

### Data

Managing data when each service owns its data and no distributed transaction
spans them — both keeping data consistent and querying across services.

| Pattern | Concern it addresses |
|---|---|
| Database per service | Each service keeps its data private |
| Shared database | Alternative: services share one database |
| Saga | Maintain consistency across services without a distributed transaction |
| API composition | Query data spanning services by querying each and joining in memory |
| CQRS | Query across services with a separate read model |
| Domain event | A service publishes an event when its data changes |
| Event sourcing | Persist state as a sequence of events |
| Aggregate | The consistency boundary a service updates atomically |
| Transactional outbox | Publish events as part of the local database transaction |
| Transaction log tailing | Derive events to publish by tailing the database log |
| Polling publisher | Derive events to publish by polling the outbox |

### Communication

How services communicate internally and how external clients reach them, plus
reliability of those calls.

| Pattern | Concern it addresses |
|---|---|
| Messaging | Communicate asynchronously via messages |
| Remote procedure invocation | Communicate via request/response (e.g. REST, gRPC) |
| API gateway | Single entry point for external clients |
| Backends for frontends | A separate gateway per client type |
| Circuit breaker | Stop cascading failures from an unresponsive dependency |
| Service mesh | Route inter-service traffic through an infrastructure layer |
| Sidecar | Run cross-cutting concerns in a process beside the service |

### Discovery

Locating a service instance's network location at runtime.

| Pattern | Concern it addresses |
|---|---|
| Client-side discovery | The client queries the registry and load-balances |
| Server-side discovery | A router queries the registry on the client's behalf |
| Service registry | A database of available service instances |
| Self registration | A service instance registers itself |
| 3rd-party registration | A separate registrar registers instances |

### Deployment

Packaging, placing, and running service instances.

| Pattern | Concern it addresses |
|---|---|
| Service per host | One service instance per host |
| Service per VM | Package a service as a VM image |
| Service per Container | Package a service as a container image |
| Serverless deployment | Run a service on a serverless platform |
| Service deployment platform | Deploy via an automated platform (e.g. orchestrator) |
| Microservice chassis | A framework handling cross-cutting concerns for a service |
| Externalized configuration | Supply configuration to a service at runtime |

### Observability

Understanding the behaviour of a running system and locating failures.

| Pattern | Concern it addresses |
|---|---|
| Health check API | An endpoint reporting instance health |
| Log aggregation | Centralise logs from all instances |
| Distributed tracing | Trace a request across the services it touches |
| Exception tracking | Aggregate and deduplicate exceptions |
| Application metrics | Collect and expose runtime metrics |
| Audit logging | Record user actions for audit |
| Log deployments and changes | Record deployments and changes for correlation |

### Security

Propagating caller identity across services.

| Pattern | Concern it addresses |
|---|---|
| Access token | Carry verified caller identity between services |

### Testing

Verifying services in isolation and at their interaction boundaries.

| Pattern | Concern it addresses |
|---|---|
| Consumer-driven contract test | Verify a service meets its consumers' expectations |
| Service component test | Test a service in isolation from its dependencies |

## How to use this map

1. Identify the concern and the forces at stake (consistency vs. coupling,
   latency vs. availability, ownership, failure isolation).
2. Use the concern → group index to pick the group.
3. List the candidate patterns in that group.
4. For alternatives that solve the same problem (e.g. Saga vs. distributed
   transaction, Database per service vs. Shared database, Client-side vs.
   Server-side discovery), weigh the forces each resolves and the trade-offs
   each carries against the caller's constraints.

## Provenance

Tier 2 reference. The grouped catalogue is the pattern map
`microservicepatternl-a51cf685` (Microservice Pattern Language, Chris
Richardson, 2020); the pattern-language groups, the decomposition patterns, and the
three-step definition method are grounded in principles P094, P096, P118, P069 and
claims C00001–C00004, C00108, C00021–C00022 from `chris-richardson-mic-19016f24`
(Microservices Patterns, Chris Richardson, Manning 2018). Both sources are
`distillation-only`: pattern
names are reproduced as the established taxonomy of the field, not as quoted
prose; no verbatim quotation.
