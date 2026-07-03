---
name: pytest-plugin-catalog
kind: reference
status: ready
provenance:
  principles:
  - P017
  - P023
  - P032
  - P033
  - P041
  - P047
  - P046
  - P067
  - P022
  - P034
  claims:
  - C00167
  - C00168
  - C00169
  - C00170
  - C00171
  - C00172
  evidence:
  - E00138
  - E00139
  - E00140
  - E00141
  - E00142
  - E00143
  source_anchors:
  - 44deffe96b40-c0007
  - 44deffe96b40-c0006
  - 44deffe96b40-c0008
  - 44deffe96b40-c0010
  - 44deffe96b40-c0009
  - 44deffe96b40-c0001
  authored_from_digest: 53163d91c3a6fb074a650991cc714b7392db8a4a8010cfb481e807025af77b98
---

# Reference: pytest plugin and extension catalog

A catalog of the pytest plugins and extension mechanisms this advisor recommends, grouped by need.
Recommend only documented plugins; each group is tied to a governing principle id.

## Finding and installing plugins [P023]

- A top-level `conftest.py` is already a local plugin — prototype a hook-based behaviour change there
  before packaging it.
- Find third-party plugins on PyPI, the pytest docs, and `pytest-dev` on GitHub.
- Install with `pip`; pin with `==`, install offline via `--find-links`, or install from a Git repo.

## Coverage [P033]

- Measure coverage with `coverage.py` via the **pytest-cov** plugin: `pytest --cov=<src>`,
  `--cov-report=html` for line detail.
- Treat 100% coverage as a heuristic, not a goal — untested code may mean a missing test or dead
  code, and coverage does not replace thinking.

## Execution and reliability [P041]

| Plugin | Use |
|--------|-----|
| **pytest-repeat** (`--count`) | reproduce flaky failures |
| **pytest-xdist** (`-n`) | parallelize independent tests (overhead → not a linear speedup; run sequentially when a resource is single-access) |
| **pytest-timeout** | bound tests that may hang |

## Reporting and static analysis [P047]

| Plugin | Use |
|--------|-----|
| **pytest-instafail**, **pytest-sugar** | live failure output |
| **pytest-html** | filterable session reports |
| **pytest-pycodestyle**/`--pep8`, **pytest-flake8**/`--flake8`, **flake8-docstrings** | surface style/lint failures as test failures |

## Test doubles and mocking [P046]

- `monkeypatch` plus the `mock` package (`unittest.mock` since Python 3.3, with **pytest-mock** as a
  convenient interface) cover test-double needs.
- Mock-based tests are white-box: decide up front what to mock and where — e.g. test functionality at
  the API layer and mock that layer when testing the CLI.

## Framework-specific plugins [P067]

- **pytest-selenium**, **pytest-django** (replaces Django's unittest-based support), **pytest-flask**
  for web testing.
- Share your own code with the built-in packaging tools (a pip-installable project via a minimal
  `setup.py`, a source distribution, and a wheel) rather than emailing zipped directories.

## Selecting subsets with markers [P034]

- Build runnable subsets such as smoke tests with markers: a test may carry many markers and a marker
  may tag many tests, and marked tests are selectable together (even across files) with `-m`.

## Migrating a legacy unittest suite [P022]

- pytest runs unittest tests, and both styles can run in one session.
- pytest markers can be applied to unittest tests; rewriting to fixtures shrinks the files.
- Watch for session-scope resource conflicts between a unittest `tearDownModule` and a pytest session
  fixture; resolve by sharing the pytest session fixture on the `TestCase` via
  `@pytest.mark.usefixtures` (needed only for shared session-scope resources).

## Testing your own plugin [P017]

- Test plugins like any other code using the bundled **pytester** plugin: enable it
  (`pytest_plugins='pytester'`), generate example tests with `testdir.makepyfile`, run them via
  `testdir.runpytest`, and assert on `result.stdout.fnmatch_lines` and `result.ret` (0 pass / 1 fail).
- Follow the make-example → run → examine-output → check-exit-code pattern, keep each test checking
  one thing, and install the plugin before running its tests.

## Packaging a plugin [P032]

- Package a plugin as a minimal module plus `setup.py`, registered via the setuptools
  `entry_points` `pytest11` group.
- Implement behaviour through hook functions (e.g. `pytest_addoption`, `pytest_report_header`,
  `pytest_report_teststatus`); include the required setup fields, use `py_modules` (or `packages`),
  and provide a README.

## Provenance

Derived from principles P017, P023, P032, P033, P041, P047, P046, P067, P022, P034 and their evidence
records over *Python Testing with pytest* (source `python-testing-with-44deffe9`).
Distillation-only source: paraphrased, no verbatim quotation.
