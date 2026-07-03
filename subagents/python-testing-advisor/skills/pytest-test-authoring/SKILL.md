---
name: pytest-test-authoring
kind: skill
status: ready
provenance:
  principles:
  - P060
  - P018
  - P037
  - P045
  - P048
  - P019
  - P021
  - P035
  - P063
  - P082
  - P069
  claims:
  - C00001
  - C00002
  - C00003
  - C00011
  - C00242
  - C00243
  evidence:
  - E00001
  - E00002
  - E00003
  - E00010
  - E00198
  - E00199
  source_anchors:
  - 44deffe96b40-c0000
  - 44deffe96b40-c0011
  - 44deffe96b40-c0002
  - 44deffe96b40-c0003
  - 44deffe96b40-c0004
  - 44deffe96b40-c0005
  authored_from_digest: ac6afd4abca6863b84ae51d9359d144fdb617e1fba8c9def46ef913e5ea7c504
---

# Skill: pytest-test-authoring

## Purpose

Guide the authoring of well-structured pytest tests: choosing the framework, writing plain
`assert` statements, and organizing fixtures, parametrization, and shared setup so that a FAIL
points at the behaviour under test rather than at broken plumbing. Grounded in principles P060,
P018, P037, P045, P048, P019, P021, P035, P063, P082, P069.

## When to use

- The caller is writing new pytest tests and asks how to structure them.
- Setup or teardown is duplicated, brittle, or leaking state between tests.
- The same logic must be exercised against many inputs or several backends.
- The caller is unsure which fixture scope or activation style to use, or where to put shared
  fixtures.

## Procedure

1. **Adopt pytest and follow its discovery conventions.** Recommend pytest as the framework: it
   discovers, runs, and reports tests from the command line, signals failure with a plain `assert`,
   works for unit through system/functional levels, and can even run existing unittest/nose suites
   (P060). Name files `test_<x>.py` or `<x>_test.py`, functions and methods `test_<x>`, and classes
   `Test<X>` so tests are auto-discovered (P082).
2. **Prefer normal fixtures over xUnit setup/teardown.** Use pytest fixtures rather than xUnit
   `setup`/`teardown`, and do not mix the two: xUnit fixtures do not appear in
   `--setup-show`/`--setup-plan`, have no session scope, apply to every test in a class regardless of
   need, cannot be parametrized, and nest at most three levels (P018).
3. **Separate get-ready from clean-up with `yield` fixtures.** In a `yield` fixture the code before
   the `yield` is setup and the code after it is guaranteed teardown; `autouse=True` applies a fixture
   without naming it, and fixtures may be consumed by tests or composed by other fixtures (P037).
4. **Choose fixture scope deliberately.** The `scope` (function/class/module/session, default
   function) is fixed at the fixture definition and sets setup/teardown frequency; a fixture may
   depend only on same-or-wider-scoped fixtures. Do expensive setup once at session scope and reset
   state per test with a small function-scoped fixture (P045).
5. **Activate fixtures appropriately.** Request a fixture by parameter when you need its return
   value; use `@pytest.mark.usefixtures` on a class when you do not; reserve `autouse=True` for
   always-run work the test data does not depend on; otherwise prefer named fixtures, and rename with
   `name=` for clarity (P048).
6. **Push the GIVEN into fixtures.** Move as much setup as possible into fixtures so a FAIL means the
   behaviour under test broke — an error inside a fixture is reported as ERROR, not FAIL, preserving
   that distinction; add GIVEN/WHEN/THEN comments when intent is not obvious (P069).
7. **Get a temp directory the safe way.** Use `tmpdir` for a per-test, auto-cleaned directory (a
   `py.path.local`; wrap in `str()` for a path string). Because it is function-scoped, use
   `tmpdir_factory` with `.mktemp` for class/module/session scope; `--basetemp` overrides the location
   (P019).
8. **Multiply coverage without duplication.** Use `@pytest.mark.parametrize(argnames, argvalues)` to
   run one test across many data sets, each reported separately, with readable `ids` or
   `pytest.param(id=...)` (P021). To run the *whole* dependent suite against several options,
   parametrize a *fixture* with `params=[...]` read via `request.param`; remember fixture
   parametrization multiplies all dependent tests while test parametrization multiplies only that
   test (P035).
9. **Locate shared fixtures correctly.** pytest resolves a requested fixture by name in the test
   module first, then in `conftest.py`; a lower-level `conftest.py` serves its directory and
   subdirectories. Never import `conftest.py` — pytest loads it automatically as a local plugin
   (P063).

## Inputs

- The Python code or behaviour under test.
- The existing test layout and any `conftest.py` / ini configuration.
- The scopes and data sets the tests must cover.

## Output

Concrete test-structure recommendations: which fixtures to define and at what scope, how to activate
and parametrize them, where to place shared fixtures, and how to name files/functions for discovery
— each tied to a principle id.

## References

- `references/pytest-cli-and-config.md` — running and configuring the tests you author.
- `references/pytest-plugin-catalog.md` — plugins that extend fixtures and execution.

## Provenance

Derived from principles P060, P018, P037, P045, P048, P019, P021, P035, P063, P082, P069 and their
evidence records over *Python Testing with pytest* (source `python-testing-with-44deffe9`).
Distillation-only source: paraphrased, no verbatim quotation.
