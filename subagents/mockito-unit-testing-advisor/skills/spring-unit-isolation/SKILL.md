---
name: spring-unit-isolation
kind: skill
status: ready
provenance:
  principles:
  - PRP-006
  claims:
  - CL021
  - CL023
  - CL025
  - CL041
  - CL042
  source_anchors: []
  authored_from_digest: 8d2d0ca1063b56b21e650644329aa2d66689f9eeea55479911a3bcb19cb802b2
---

# Spring Unit Isolation

## Purpose

Unit-test one layer of a layered Spring web application (controller / service / DAO) by mocking
only the layer directly below it and constructing the class under test directly — never loading a
Spring `ApplicationContext` (PRP-006). Each layer's test stays independent of Spring DI and of real
infrastructure.

## When to use

- Unit-testing any class in a layered Spring MVC application (web / service / DAO).
- The goal is to test a single layer in complete isolation from Spring wiring and the database.

## Procedure

1. **Mock the layer directly below, only that layer (CL041, PRP-006).** The controller test mocks
   the service, the service test mocks the DAO interface, the DAO test mocks `JdbcTemplate`. No
   layer's unit test starts the real implementation of another layer.
2. **Introduce a DAO interface for service isolation (CL042).** Put an interface (e.g.
   `RegistrationDao`) between the service and its data-access implementation. Mockito mocks the
   interface, decoupling the service test from any database. Without that interface Mockito cannot
   isolate the service.
3. **Controller layer (CL021):** create a `@Mock` for each service dependency, instantiate the
   controller directly in `@Before` setup, inject the mock via the controller's setter, and run with
   `MockitoJUnitRunner`. The servlet container is not started.
4. **Service layer (CL023):** create a `@Mock` for the DAO interface, instantiate the service in
   `@Before`, inject the mock DAO via the service's setter; the service is then tested with no real
   database.
5. **DAO layer (CL025):** declare `@Mock JdbcTemplate`, construct the DAO with the mock template in
   `@Before`, and use `ArgumentCaptor` to verify SQL parameters are passed in the correct order (see
   interaction-verification).
6. **Confirm isolation is falsifiable:** no `@ContextConfiguration`, no real `DataSource` wiring,
   and no `ApplicationContext` loaded. A full-context, real-database, or MockMvc-with-WebApplicationContext
   test is an integration or slice test, not a plain unit test (`does_not_apply_when`).

## Inputs

- The class under test and which Spring layer it belongs to (controller / service / DAO).
- Its immediate-below collaborator (service, DAO interface, or `JdbcTemplate`) and setter/constructor seams.

## Output

A single-layer unit test that mocks only the layer below, constructs the subject directly, loads no
Spring context, and runs without a database.

## References

- (none — this package declares no reference docs.)

## Provenance

Principle PRP-006; claims CL021 (controller-layer pattern), CL023 (service-layer pattern), CL025
(DAO-layer pattern), CL041 (per-layer independence), CL042 (DAO interface for isolation).
Distillation-only source; paraphrased, no verbatim quotation.
