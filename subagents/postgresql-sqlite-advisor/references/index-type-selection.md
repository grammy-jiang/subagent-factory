---
name: index-type-selection
kind: reference
status: ready
provenance:
  principles:
  - P002
  - P012
  - P018
  - P011
  - P040
  - P004
  - P010
  claims:
  - C00337
  - C00338
  - C00313
  - C00320
  - C00638
  - C00639
  - C01404
  - C01405
  - C01330
  - C01353
  - C00344
  - C00345
  - C01402
  - C01403
  evidence:
  - E00109
  - E00110
  - E00101
  - E00103
  - E00170
  - E00171
  - E00351
  - E00352
  - E00336
  - E00341
  - E00114
  - E00115
  - E00349
  - E00350
  source_anchors:
  - b1c9b849675c-c0001
  - b1c9b849675c-c0000
  - b86b08dae66e-c0002
  - 163dcf344261-c0000
  authored_from_digest: 3cc3fe66bdb90fa531d9d1ed9558795e88619b8f502b3d7bd78254d0353418b2
---

# Index-type selection

Pick the index type and access path from the operators and data the queries use.

- **P002** — Select the index method to fit the data and operators: B-Tree as the general default, GiST for spatial/full-text/exclusion (lossy), GIN for jsonb/full-text (faster reads, slower writes), and avoid legacy hash indexes (not WAL-logged, unusable in replication).
- **P012** — Treat missing or wrong indexing as the first suspect for bad PostgreSQL performance; verify the expected indexes exist before tuning memory or hardware, and watch for over-indexing that slows writes.
- **P018** — Prefer jsonb (binary, faster, GIN-indexable, key-deduping) over json unless you must preserve exact text, whitespace, key order, or duplicate keys; index containment queries with @> plus a GIN index.
- **P011** — Use a partial index (an index with a WHERE clause) for workloads that consistently filter on the same constant predicate to get a smaller, faster index, but do not create hundreds or thousands of partial indexes because that slows down planning.
- **P040** — Drive index design from the query workload in order: evaluate the required data types and operators first, then pick the index type, then decide whether an advanced index (multi-column, expression, partial) is warranted.
- **P004** — Support LIKE searches with an index only up to the first wildcard: a leading wildcard cannot use the B-tree access predicate, so route such searches to a full-text or trigram index instead.
- **P010** — Create an expression index on the function/expression a query filters by (e.g. lower(column)) when the query applies a function to the column, since an index on the bare column cannot serve such a query.

## Grounding

Distilled (no verbatim) from this package's principles (P002, P012, P018, P011, P040, P004, P010) and their anchored claims. Verify version-specific availability against current official PostgreSQL or SQLite documentation.
