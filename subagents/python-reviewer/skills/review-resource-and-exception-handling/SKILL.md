---
name: review-resource-and-exception-handling
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P009
  - P012
  - P021
  - P025
  - P031
  - P033
  - P044
  - P046
  claims:
  - C00173
  - C00174
  - C00175
  - C00176
  - C01008
  - C01009
  - C00183
  - C00184
  - C00185
  - C00186
  - C01047
  - C01048
  evidence:
  - E00076
  - E00077
  - E00078
  - E00079
  - E00287
  - E00288
  - E00084
  - E00085
  - E00086
  - E00087
  - E00297
  - E00298
  source_anchors:
  - 5c81071aa988-c0012
  - 2bf219904a5b-c0014
  - 5c81071aa988-c0013
  - 2bf219904a5b-c0017
  authored_from_digest: d87d45d31c66fc97bb9094b664e6c17e9c0d814c425d950a10fda2bb03a11099
---

# Review resource and exception handling

## Purpose

Hold resource management and exception handling to source discipline: manage resources
with `with`, and apply three exception rules — propagate when there is no local recovery,
keep `except` narrow, and define custom exception types for intentional errors.
(P14, P15)

## When to use

- Code acquires a file, lock, socket, connection, or other resource that must be released.
- Code catches, raises, or re-raises exceptions, or uses `try/except` for control flow.

Do not flag a resource already managed by a `with`-statement/context manager, and do not
flag a deliberate top-level boundary that intentionally catches broadly to log and shut
down cleanly.

## Procedure

1. **Require context managers for resources.** Flag manual `open()`/`close()` (and the
   lock/connection equivalents) and recommend a `with`-statement / context manager, so
   cleanup runs on every path — including when an error is raised — and an explicit
   `close()` cannot be forgotten. (C015)
2. **Propagate when there is no local recovery.** Flag a `try/except` that catches an
   exception it cannot meaningfully handle at that point. If there is no sensible local
   recovery, let it propagate to a caller that can handle it, rather than defensively
   checking every return value. (C016)
3. **Keep `except` clauses narrow.** Flag a blanket `except Exception` (or bare `except:`)
   used where a specific exception is meant; it also swallows legitimate programming errors
   and makes debugging hard. Recommend the narrowest reasonable exception type. (C017)
4. **Preserve the boundary exception.** Do not flag a deliberate top-level handler that
   catches broadly on purpose to log and shut down cleanly — that is a legitimate boundary.
5. **Require custom exception types for intentional errors.** Where the code raises its own
   errors, recommend defining custom exception types (subclassing `Exception`) so
   intentional application-level errors are distinguishable from genuine programming
   mistakes. (C018)

## Inputs

- The Python code under review: which resources it acquires, and where it catches, raises,
  or re-raises exceptions.

## Output

A `review`/`patch-suggest` finding per issue: the resource or exception construct at fault,
which rule it breaks (manual cleanup; caught-but-unrecoverable; over-broad `except`;
generic raise), and the minimal fix (`with`; let it propagate; narrow the clause; custom
type) — with the top-level-boundary exception preserved. Traced to P14 or P15. A genuine
defect such as a swallowed exception is distinguished from a stylistic preference.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the resource
  and exception rows.

## Provenance

Derived from principles **P14** (claim **C015**, evidence **E015**) and **P15** (claims
**C016**, **C017**, **C018**; evidence **E016**, **E017**, **E018**), grounded in Python
Distilled's resource-management and exception sections (anchors
`python-distilled-pea-1baf485f-h0018`, `python-distilled-pea-1baf485f-h0101`).
Distillation-only source: paraphrased, no verbatim quotation.
