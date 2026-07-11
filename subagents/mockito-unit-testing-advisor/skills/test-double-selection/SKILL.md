---
name: test-double-selection
kind: skill
status: ready
provenance:
  principles:
  - PRP-001
  claims:
  - CL004
  - CL006
  - CL007
  source_anchors: []
  authored_from_digest: e0f63230e5b376454154582b5b350403820573fdb0d8fef1ca5c3d77ba05856c
---

# Test Double Selection

## Purpose

Decide which collaborators of the class under test must be replaced by Mockito test doubles so the
test runs in isolation and in milliseconds, never touching a real external resource (PRP-001). A
test that acquires a database connection, talks to the Internet or an SMTP server, or does file
I/O is an integration test, not a unit test (CL004).

## When to use

- Writing a unit test for a class whose dependencies include a database, messaging, network
  service, or any other stateful external resource.
- The goal is fast, deterministic feedback (TDD inner loop, CI pre-merge gate).

## Procedure

1. **Inventory the collaborators** the class under test calls. For each, ask whether invoking it
   for real would acquire a DB connection, reach the network/SMTP, or do file I/O. Any "yes" marks
   it an external dependency that must be mocked (CL004).
2. **Replace each external collaborator with a mock** so the class's own logic is exercised in
   isolation from those resources (CL006). Mockito supplies the proxy that stands in for the real
   database or SMTP connection.
3. **Leave pure value objects and side-effect-free utilities as real instances.** Mocking adds no
   isolation value there; only stateful external collaborators need a double (`does_not_apply_when`).
4. **Reject real-resource coupling.** A unit test that reads the real database or makes a real
   Internet call is non-deterministic: the DB state can differ between runs and each network call
   may return a different value, so assertions on fixed values become unreliable (CL007). If such a
   call remains, the test is misclassified — convert it to a mock or move it to the integration suite.
5. **Confirm isolation is falsifiable:** the suite must pass with no network and no database
   available. If it does not, an unmocked external collaborator remains.

## Inputs

- The class under test with its collaborator interfaces and dependencies.
- For each collaborator, whether real invocation touches an external/stateful resource.

## Output

A list of collaborators classified mock-or-real, with every external dependency replaced by a
Mockito mock, leaving a test that runs without network or database access.

## References

- (none — this package declares no reference docs.)

## Provenance

Principle PRP-001; claims CL004 (integration vs unit boundary), CL006 (mock externals for fast
isolated tests), CL007 (real DB/Internet → non-deterministic assertions). Distillation-only
source; paraphrased, no verbatim quotation.
