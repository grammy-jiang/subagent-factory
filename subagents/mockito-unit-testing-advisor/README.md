# mockito-unit-testing-advisor

**Display name:** Mockito Unit-Testing Advisor for Spring
**Version:** 0.1.0
**Tier:** 1
**Status:** draft

## Purpose

Guides Java developers on unit-testing Spring applications with Mockito. The advisor
covers designing test doubles (mocks, stubs, spies), stubbing and verifying interactions
across the web, service, and DAO layers, and keeping unit tests fully isolated from
external dependencies so they run in milliseconds.

## When to use

- Unit testing a Spring controller, service, or DAO in isolation from the database,
  SMTP, or other external infrastructure.
- Getting millisecond-fast test feedback by replacing real infrastructure with Mockito
  mocks.
- Verifying void-method calls with `verify()` and `ArgumentCaptor`.
- Setting up `@Mock` / `MockitoJUnitRunner` / `MockitoAnnotations.initMocks()` correctly.

## When NOT to use

- Full Spring integration tests with a real DataSource and `@Transactional/@Rollback`.
- Mocking final classes, static methods, or private methods with plain Mockito.
- Advanced Mockito topics not covered by the source (BDDMockito, Mockito inline,
  full Answers API).

## Supported modes

| Mode | Trigger |
|------|---------|
| `advise` | Which API to use, how to choose between runners, when to use which verify mode |
| `produce` | Draft a new JUnit 4 test class for a described Spring class |
| `review` | Identify anti-patterns, missing isolation, or wrong verify usage in existing tests |
| `patch-suggest` | Minimal bounded fix to a specific defect in an existing test |

## Required inputs

1. The Java class under test and its collaborator interfaces/dependencies.
2. The Spring layer being tested (controller, service, or DAO).

## Principles grounding

All quality-bar items and forbidden behaviours are grounded in `principles/principles.yaml`
(PRP-001 through PRP-007, principles-v1).

## Source

Sujoy Acharya, *Mockito for Spring*, Packt Publishing, 2015.
Rights: `distillation-only`. SHA-256: `e5f0853c...`.

See `provenance-ledger.md` for full field traceability and `CHANGELOG.md` for version
history.
