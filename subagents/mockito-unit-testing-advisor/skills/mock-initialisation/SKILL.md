---
name: mock-initialisation
kind: skill
status: ready
provenance:
  principles:
  - PRP-002
  claims:
  - CL008
  - CL009
  - CL029
  source_anchors: []
  authored_from_digest: 2e0d789f142948d6edd8197b601d7935cd02d08f3c154f74ca4d05c916e7776b
---

# Mock Initialisation

## Purpose

Create and activate mock collaborators correctly so every `@Mock` field is a live proxy before the
test body runs (PRP-002). An unactivated `@Mock` is left null and the test fails with a
NullPointerException rather than exercising the intended path.

## When to use

- Any JUnit-based Mockito test class that needs one or more mock collaborators.
- Choosing between annotation-driven creation and programmatic `Mockito.mock()`.

## Procedure

1. **Pick the creation style (CL008).** Use the `@Mock` annotation on field declarations as the
   default, declarative style. Reserve the `org.mockito.Mockito.mock()` static factory for
   programmatic creation where the annotation style is inconvenient (e.g. a mock built inside a
   helper method).
2. **Activate annotated mocks (CL009, PRP-002).** `@Mock` fields are inert until initialised. Pick
   exactly one activation path:
   - JUnit 4: annotate the class with `@RunWith(MockitoJUnitRunner.class)`; or
   - call `MockitoAnnotations.initMocks(this)` (newer Mockito: `openMocks(this)`) in a `@Before`
     method; the JUnit 5 equivalent is `@ExtendWith(MockitoExtension.class)`.
3. **Do not combine the Mockito runner with the Spring runner (CL029, PRP-002).**
   `@RunWith(MockitoJUnitRunner.class)` and `@RunWith(SpringJUnit4ClassRunner.class)` cannot both
   sit on the same class — JUnit 4 allows only one runner. For a Spring TestContext integration
   test, drop the Mockito runner and inject mocks another way (`@MockBean` in Spring Boot, or
   reflection-based field injection); that is integration, not plain unit, testing.
4. **Verify activation is falsifiable:** every `@Mock` field must be non-null at test run. A null
   mock means no activation path was applied.

## Inputs

- The test class and its `@Mock` collaborator fields.
- The JUnit version (4 vs 5) and whether the class is a plain unit test or a Spring integration test.

## Output

A test class whose mocks are all activated by a single, correct mechanism, with the Mockito and
Spring runners kept separate.

## References

- (none — this package declares no reference docs.)

## Provenance

Principle PRP-002; claims CL008 (`Mockito.mock()` vs `@Mock`), CL009 (initMocks / MockitoJUnitRunner
activation), CL029 (Spring runner cannot be combined with the Mockito runner). Distillation-only
source; paraphrased, no verbatim quotation.
