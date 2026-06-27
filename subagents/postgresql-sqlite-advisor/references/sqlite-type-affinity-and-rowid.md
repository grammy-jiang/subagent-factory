---
name: sqlite-type-affinity-and-rowid
kind: reference
status: ready
provenance:
  principles:
  - P022
  - P048
  - P050
  - P029
  claims:
  - C00766
  - C00826
  - C00791
  - C00877
  - C00810
  - C00864
  - C00779
  - C00821
  evidence:
  - E00200
  - E00218
  - E00203
  - E00241
  - E00209
  - E00235
  - E00202
  - E00217
  source_anchors:
  - 9aa0ce19c36d-c0000
  - 9aa0ce19c36d-c0002
  - 9aa0ce19c36d-c0001
  - 9aa0ce19c36d-c0003
  authored_from_digest: 0a07e8355d47d4e579ee33543669a015ae2daf7cdd60b42fcd891a8aa56e434c
---

# SQLite type affinity and ROWID

How SQLite stores, converts, compares, and sorts values, and how its ROWID/INTEGER PRIMARY KEY behaves.

- **P022** — Understand storage classes and type affinity - SQLite has five storage classes, a column may hold mixed classes across rows, sort order is NULL then numbers then TEXT then BLOB, and each column has NUMERIC/INTEGER/TEXT/NONE affinity derived from its declared type (an unrecognized type defaults to NUMERIC, no type gives NONE).
- **P048** — Declaring a column INTEGER PRIMARY KEY makes it an alias for the table's 64-bit ROWID with auto-generated keys and is the one column whose type is enforced; default ROWIDs may be recycled and non-monotonic after deletes, so add AUTOINCREMENT only when the application truly needs never-reused, strictly increasing keys.
- **P050** — Handle NULL deliberately - NULL is the absence of a value (not zero, empty string, true, or false); test it with IS NULL / IS NOT NULL (never = NULL), expect it to propagate through expressions and three-valued logic, know that it is dropped by WHERE and ignored by aggregates, and use COALESCE to supply defaults in nullable expressions.
- **P029** — Prefer explicit JOIN ... ON syntax with table-qualified column names, avoid NATURAL JOIN (whose results silently change when columns are added or removed), and remember SQLite implements no RIGHT or FULL OUTER JOIN - rewrite them with a reversed LEFT JOIN or compound queries.

## Grounding

Distilled (no verbatim) from this package's principles (P022, P048, P050, P029) and their anchored claims. Verify version-specific availability against current official PostgreSQL or SQLite documentation.
