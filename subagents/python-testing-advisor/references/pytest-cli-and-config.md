---
name: pytest-cli-and-config
kind: reference
status: ready
provenance:
  principles:
  - P013
  - P014
  - P024
  - P043
  - P044
  - P061
  - P062
  - P064
  - P065
  - P025
  - P066
  claims:
  - C00006
  - C00009
  - C00025
  - C00026
  - C00029
  - C00030
  evidence:
  - E00006
  - E00009
  - E00022
  - E00023
  - E00026
  - E00027
  source_anchors:
  - 44deffe96b40-c0000
  - 44deffe96b40-c0001
  - 44deffe96b40-c0007
  - 44deffe96b40-c0008
  - 44deffe96b40-c0002
  - 44deffe96b40-c0003
  authored_from_digest: 03b8bc3f2b93ebe192e87d18610a58a9b37a5dbf2f3faf4de94869abb6ee7129
---

# Reference: pytest command-line and configuration

A catalog of the pytest command-line options and configuration mechanisms this advisor recommends.
Recommend only documented mechanisms; each row is tied to a governing principle id.

## Output and diagnostics [P013]

| Need | Mechanism |
|------|-----------|
| More / less detail | `-v`/`--verbose`, `-q`/`--quiet` |
| Traceback style | `--tb=<style>` (`auto`/`long`/`short`/`line`/`native`/`no`) |
| Show local variables | `-l` |
| Surface `print` output | `-s` (disable capture) |
| Find the slowest tests | `--durations=<N>` |

## Test selection and scoping [P043] [P044]

| Need | Mechanism |
|------|-----------|
| Discover everything | implicit recursive discovery from the rootdir |
| Run explicit targets | pass files/directories, or a `file::Class::test` node id |
| Select by name substring | `-k <expr>` |
| Run any subset | by directory, file, class, method, node id, name expression, or marker |
| Discover the exact node id | run `pytest -v` on the target |
| Preview a selection | `--collect-only` before running |

## Run control [P061]

| Need | Mechanism |
|------|-----------|
| Stop early | `-x`, `--maxfail=<N>` |
| Rerun only failures | `--lf` (last-failed) |
| Prioritize failures first | `--ff` (failed-first) |

## Skipping and expected failures [P024]

| Marker | Meaning |
|--------|---------|
| `@pytest.mark.skip(reason=...)` | skip unconditionally (always give a reason) |
| `@pytest.mark.skipif(expr, reason=...)` | skip on a Python expression |
| `@pytest.mark.xfail(reason=...)` | run but expect failure |
| `xfail_strict` (ini) | an unexpected pass becomes a failure |
| `-rs` | surface skip/xfail reasons in the summary |

## Interactive debugging [P065]

| Need | Mechanism |
|------|-----------|
| Break at the failure point | `--pdb` |
| Jump to the first previous failure | combine `--pdb` with `--lf -x` (and `-l`/`-v`/`--tb`) |
| Inspect in pdb | `p`/`pp` (print), `l` (list), `a` (args), `u`/`d` (frames), `q` (quit) |

## Configuration files [P014]

- Store configuration in `pytest.ini`, `tox.ini`, or `setup.cfg` (the format is largely the same).
- Enable `xfail_strict` so an unexpected pass fails.
- Override discovery with `python_files`/`python_classes`/`python_functions` only for a strong reason
  such as migrating a large existing suite — and do it gradually by listing both old and new patterns.

## Local customization and introspection [P062]

- Customize pytest locally through `conftest.py` and ini files.
- Introspect with `-h`, `--markers`, and `--fixtures`.
- Available options, markers, and fixtures depend on the target path, because `conftest.py` files
  are loaded along it.

## Custom command-line options [P064]

- Register options with the `pytest_addoption` hook — only in a plugin or the **top-level**
  `conftest.py`, never a test subdirectory.
- Read them with `pytestconfig.getoption(...)`; `pytestconfig` (a shortcut to `request.config`) can
  also be requested from other fixtures.

## Continuous integration [P025]

- Emit results with `--junit-xml` (the only flag required; `--junit-prefix` and `junit_suite_name`
  refine naming).
- Run inside a virtual environment that installs the project first.
- Keep build logic in a version-controlled script.
- Cover multiple environments via separate CI jobs or by calling `tox`.

## Environment [P066]

- Install and run pytest inside a per-project virtual environment.
- Because pytest is versioned separately from the interpreter, you can run the latest pytest against
  legacy Pythons; on Windows activate with `venv\Scripts\activate.bat`.

## Provenance

Derived from principles P013, P014, P024, P043, P044, P061, P062, P064, P065, P025, P066 and their
evidence records over *Python Testing with pytest* (source `python-testing-with-44deffe9`).
Distillation-only source: paraphrased, no verbatim quotation.
