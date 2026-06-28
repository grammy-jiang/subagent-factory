---
name: test-type-taxonomy
kind: reference
status: ready
provenance:
  principles:
  - P014
  - P019
  - P013
  claims:
  - C00329
  - C00330
  - C00331
  - C00332
  - C00333
  - C00334
  - C00335
  - C00351
  source_anchors: []
  authored_from_digest: 9f50f22f464a7f036142b7154f663519126eeb1dd0a510fc372c6f19e08097f5
---

# Test Type Taxonomy

A complete testing strategy covers all of the following types. Unit testing is the
foundation; each subsequent type builds on modules that have already passed it. No
single type is sufficient on its own (P014, C00329).

## Test types

| Test type | What it checks | Key point |
|---|---|---|
| **Unit testing** | A single module behaves to its specification in isolation. | The required foundation. Require every module to pass its unit tests before it enters integration (P014, C00330). |
| **Integration testing** | Modules work together correctly across their interfaces and contracts. | Often the single largest source of bugs; good contracts make integration defects easy to detect and localise (P014, C00331). |
| **Validation and verification** | The system meets the user's actual need (validation) and was built correctly (verification). | A bug-free system that answers the wrong question is still a failure; account for how real access patterns differ from developer test data (P014, C00332). |
| **Resource exhaustion and recovery** | Behaviour as memory, disk, CPU, or bandwidth run out, and graceful recovery afterwards. | Test explicit exhaustion of each limited resource; the system should save state rather than crash in the user's face (P014, C00333). |
| **Performance and load testing** | The system meets its performance and scalability requirements under realistic load. | Run against realistic or simulated load, not only a clean development machine; use tooling to simulate when needed (P014, C00334). |
| **Usability testing** | Real users can accomplish their goals under real conditions. | Evaluate in terms of human factors; a usability failure is as serious a bug as a divide-by-zero; test as early as possible while correction is still cheap (P014, C00335). |

## Ordering rule

- Modules pass **unit** tests before entering **integration** testing.
- Treat **integration** as the highest-risk layer and rely on contracts to localise defects.
- **Validation and verification** happen against the real requirement, not just the stated one.

## Testing quality and state coverage

Code coverage tools track executed lines but executing a line is not the same as
covering a state. The metric to optimise is **state coverage**: the data used and the
order in which code is traversed drive the number of program states that are actually
exercised. Use both real-world and synthetic test data because they expose different
classes of bugs; synthetic data covers volume, boundary conditions, and statistical
edge cases that real data may never hit (P019, C00351).

Additional practices that improve test effectiveness:

- Decouple application logic from the GUI so logic can be tested without a running
  interface; this also makes the remaining UI bugs easier to locate (P019, C00348).
- Use saboteurs to verify the tests actually catch bugs: deliberately introduce a
  known defect in a copy and confirm the test suite detects it (P019, C00349).
- Analyse design metrics (cyclomatic complexity, coupling ratios, response set,
  inheritance fan-in/fan-out) comparatively across modules to flag outliers before
  they become test failures (P019, C00345).

## Harness and discoverability

Ship the tests with the code so field problems can be diagnosed with the same suite
(P013, C00272). Run tests often — running them is not optional (P013, C00273). Build
a composable test harness (reusing an xUnit-style framework) with tests that return
exit codes so they compose in automated pipelines (P013).

## Provenance

Derived from P014 (the six major testing types), P019 (state coverage, real and
synthetic data, GUI decoupling, saboteurs, design metrics), and P013 (ship tests with
code, run often, composable harness). Primary claims: C00329 (perform all major types),
C00330 (unit testing is the foundation), C00331 (integration is the largest bug source),
C00332 (validate against actual need), C00333 (resource-exhaustion and graceful
recovery), C00334 (performance and load under realistic conditions), C00335 (usability
with real users), C00351 (test state coverage not code coverage). Source is
distillation-only; all wording is paraphrased.
