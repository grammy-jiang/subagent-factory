---
name: microservice-testing-strategy
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P049
  - P013
  - P017
  - P020
  - P027
  - P111
  claims:
  - C00010
  - C00076
  - C00356
  - C00357
  - C00373
  - C00374
  - C00365
  - C00366
  - C00384
  - C00392
  - C00386
  - C00387
  - C00397
  - C00398
  source_anchors: []
  authored_from_digest: 95a1e28a979131ceaac6fdaf36e081bca355508e491e847a6b0e4915d0e108f0
---

# Microservice Testing Strategy

## Purpose

Guide a caller designing how to test services and their interactions so breaking API
changes between services are caught cheaply, without relying on a large end-to-end
suite. This is the specialised walkthrough for the **Testing** group.

## When to use

Use when the caller is deciding how to test services, how to guarantee inter-service
API compatibility, or how to reduce a slow/brittle end-to-end burden. Do not use for
runtime/production behaviour concerns (route to `production-readiness-review`).

## Procedure

1. **Rely on automated tests.** Manual testing is inefficient and happens too late;
   automated tests give fast feedback and force a testable application — skipping them
   is the fast track to monolithic hell (C00356, C00357, P049). The microservice
   architecture both improves testability and demands automated tests.

2. **Prefer unit tests for small units.** A full-service test is slower and more
   brittle than a unit test for a small unit; choose the unit-test type by class role
   — solitary tests that mock dependencies for domain services, controllers, and
   message gateways; sociable tests for entities, value objects, and sagas (C00373,
   C00374, P013).

3. **Verify inter-service interactions with contract tests, not end-to-end tests.**
   The complexity of a microservice architecture lies in the interactions, each a
   contract; use consumer-driven contract testing — the consumer writes example-based
   contracts contributed to the provider's pipeline that verify the provider's API
   shape (not its business logic), testing both sides for REST, publish/subscribe, and
   asynchronous request/response (C00010, C00365, C00366, P007, P017).

4. **Test each service in isolation.** Use the Service Component Test pattern: a
   black-box acceptance test of a whole service in isolation that stubs its
   dependencies, written as business-facing given-when-then specifications (e.g.
   Gherkin run by Cucumber), choosing in-process (fast) or out-of-process (the
   production-format container against real infrastructure) (C00384, C00392, P020).

5. **Test persistence against a real database.** Write persistence integration tests
   that exercise the real database (run in Docker, not mocked) for a service's
   database-access logic (C00386, C00387, P027).

6. **Minimise end-to-end tests.** They are slow, brittle, and time-consuming; keep
   the few you retain as user-journey tests that exercise a whole slice of
   functionality in a business-readable DSL (C00397, C00398, C00076, P111).

7. **Hand off.** The architecture/engineering owner decides and implements; this
   skill informs.

## Inputs

- **Required:** the services and inter-service dependencies to test, and the current
  testing pain (e.g. slow end-to-end suite, missed breaking changes).

## Output

A recommended test strategy: automated tests, unit tests by class role,
consumer-driven contract tests for inter-service compatibility, service component
tests for isolation, persistence integration tests, and a reduced end-to-end
footprint — each tied to the caller's situation.

## References

- `references/microservice-pattern-language-map.md` — the Testing-group patterns.

## Provenance

Tier 2. Grounded in principles P049 (rely on automated tests), P013 (prefer unit
tests by class role), P007/P017 (consumer-driven contract tests for interactions),
P020 (service component tests), P027 (persistence integration tests), and P111
(minimise end-to-end tests), from `chris-richardson-mic-19016f24` (Microservices
Patterns, Chris Richardson, Manning 2018, `distillation-only`). No verbatim
quotation.
