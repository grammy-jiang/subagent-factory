---
name: production-readiness-review
kind: skill
status: ready
provenance:
  principles:
  - P127
  - P003
  - P091
  - P066
  - P076
  - P009
  - P065
  - P032
  - P130
  claims:
  - C00399
  - C00014
  - C00075
  - C00421
  - C00422
  - C00424
  - C00428
  - C00400
  - C00401
  - C00085
  source_anchors: []
  authored_from_digest: b189b7865dec972852ef3d41cba7e8485550229b819420a3a02566b4e6dd436a
---

# Production Readiness Review

## Purpose

Guide a caller making services production-ready: the security, configurability, and
observability quality attributes every service should satisfy, the cross-cutting
patterns that provide them, and the deployment style to run them on. This is the
specialised walkthrough for the **Observability / Security / Deployment** groups and
cross-cutting concerns.

## When to use

Use when the caller is preparing services for production operation, designing
observability, configuration, or security, or choosing how to package and run
instances. Do not use for prototypes with no operational requirement, or for domain
modelling (route to `service-decomposition-advice`).

## Procedure

1. **Cover the three production quality attributes.** Beyond functional requirements,
   a production-ready service must satisfy security, configurability, and
   observability (C00399, P127). Review each.

2. **Make each service observable.** Diagnosing a microservice application is harder
   than a monolith because a request bounces across services with no single log file
   (C00075). Apply the observability patterns, each with a developer and an operations
   component (C00014, P003):
   - **Health check API** — expose an endpoint the platform polls so it routes around
     a not-ready or failed instance.
   - **Log aggregation** — have each service log to stdout and let the infrastructure
     ship all instances' logs to a centralized, searchable, alertable store (C00421,
     C00422, P091).
   - **Distributed tracing** — assign each external request a unique id and record its
     span tree across services in a central server (e.g. Zipkin), propagating trace
     state via a per-service instrumentation library (C00424, P066).
   - **Application metrics** — instrument the service to collect behavioural metrics and
     expose them to a central metrics server that aggregates, visualises, and alerts
     (C00428, P076); plus Exception tracking and Audit logging.

3. **Externalize configuration.** Supply configuration to a service at runtime via the
   Externalized Configuration pattern so one artifact runs unchanged across
   environments (P065).

4. **Secure the service.** Authenticate clients at the API gateway (never in the
   individual services), pass the principal's identity and roles downstream via a
   transparent token (prefer a short-lived signed JWT over an opaque token needing a
   synchronous validation call), use a proven security or OAuth 2.0 framework rather
   than building your own, and cover authentication, authorization, auditing, and
   TLS-secured IPC (C00400, C00401, P009).

5. **Provide cross-cutting concerns once.** Recommend a Microservice chassis or
   service template that handles externalized configuration, health checks, logging,
   metrics, and exception tracking so each new service does not re-implement them
   (P032); a Service mesh / Sidecar can move these out of service code.

6. **Choose the deployment style and track delivery.** Choose the deployment pattern
   by isolation, overhead, and scaling using the `deployment-options-comparison`
   reference, and assess delivery with the four metrics — deployment frequency, lead
   time, mean time to recover, and change failure rate (C00085, P130).

7. **Hand off.** The architecture/operations owner decides and implements; this skill
   informs.

## Inputs

- **Required:** the services to operationalise, the existing
  observability/config/security gaps, and the scaling/isolation constraints for
  deployment.

## Output

A production-readiness recommendation: the observability patterns to add, externalized
configuration, an edge-authentication/security approach, a chassis or service-mesh
approach for cross-cutting concerns, a justified deployment style, and the delivery
metrics to track — each tied to the caller's forces.

## References

- `references/deployment-options-comparison.md` — VM vs. container vs. serverless
  vs. service mesh.
- `references/microservice-pattern-language-map.md` — Observability, Security, and
  Deployment groups.

## Provenance

Tier 2. Grounded in principles P127 (three production quality attributes), P003
(observability patterns), P091/P066/P076 (log aggregation, distributed tracing,
application metrics), P009 (microservice security), P065 (externalized
configuration), P032 (microservice chassis), and P130 (four delivery metrics), from
`chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson, Manning
2018, `distillation-only`). No verbatim quotation.
