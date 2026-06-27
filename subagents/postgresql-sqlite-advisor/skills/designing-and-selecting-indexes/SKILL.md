---
name: designing-and-selecting-indexes
kind: skill
status: ready
provenance:
  principles:
  - P040
  - P002
  - P012
  - P014
  - P004
  - P010
  - P011
  - P019
  - P018
  - P001
  - P006
  - P046
  claims:
  - C01330
  - C01353
  - C00337
  - C00338
  - C00313
  - C00320
  - C00331
  - C01574
  - C00344
  - C00345
  - C01402
  - C01403
  - C01404
  - C01405
  - C00332
  - C00333
  - C00638
  - C00639
  - C00330
  - C01346
  - C01333
  - C01339
  - C01429
  - C01430
  evidence:
  - E00336
  - E00341
  - E00109
  - E00110
  - E00101
  - E00103
  - E00106
  - E00381
  - E00114
  - E00115
  - E00349
  - E00350
  - E00351
  - E00352
  - E00107
  - E00108
  source_anchors:
  - 163dcf344261-c0000
  - b1c9b849675c-c0001
  - b1c9b849675c-c0000
  - 78ffa02280d3-c0000
  - b86b08dae66e-c0002
  authored_from_digest: 94b142fb74386e9d3441ec1a8f30bf3dc39ca6b2e2b2c213b8ef162a488810bb
---

# Designing and selecting indexes

## Purpose

Choose the right index type and shape for a query workload — driven by the data types and operators the queries use — and keep the index set lean.

## When to use

When deciding whether and how to index for a known set of queries, or reviewing an existing index.

## Procedure

1. Drive index design from the query workload in order: evaluate the required data types and operators first, then pick the index type, then decide whether an advanced index (multi-column, expression, partial) is warranted. (P040)
2. Select the index method to fit the data and operators: B-Tree as the general default, GiST for spatial/full-text/exclusion (lossy), GIN for jsonb/full-text (faster reads, slower writes), and avoid legacy hash indexes (not WAL-logged, unusable in replication). (P002)
3. Treat missing or wrong indexing as the first suspect for bad PostgreSQL performance; verify the expected indexes exist before tuning memory or hardware, and watch for over-indexing that slows writes. (P012)
4. Order the columns of a concatenated (multi-column) index by how the queries use them: a column can serve as an access predicate only if all preceding index columns are constrained by equality. (P014)
5. Support LIKE searches with an index only up to the first wildcard: a leading wildcard cannot use the B-tree access predicate, so route such searches to a full-text or trigram index instead. (P004)
6. Create an expression index on the function/expression a query filters by (e.g. lower(column)) when the query applies a function to the column, since an index on the bare column cannot serve such a query. (P010)
7. Use a partial index (an index with a WHERE clause) for workloads that consistently filter on the same constant predicate to get a smaller, faster index, but do not create hundreds or thousands of partial indexes because that slows down planning. (P011)
8. Use functional indexes for case-insensitive or expression searches (always querying with the same function) and partial indexes for hot subsets (WHERE must be IMMUTABLE and the query's WHERE must be a superset of the index condition). (P019)
9. Prefer jsonb (binary, faster, GIN-indexable, key-deduping) over json unless you must preserve exact text, whitespace, key order, or duplicate keys; index containment queries with @> plus a GIN index. (P018)
10. Add columns to an index to enable index-only scans that avoid table access, but weigh the gain against the index's clustering factor and the maintenance cost of the wider index. (P001)
11. Keep the number of indexes minimal: every index must be maintained on each insert/update/delete and adds WAL writes, so unused or redundant indexes are a write-performance tax to be consolidated away. (P006)
12. When reading an EXPLAIN plan, run it with ANALYZE and BUFFERS and focus on the most expensive node; a Sequential Scan with a high 'Rows Removed by Filter' and large buffer reads signals a missing index. (P046)

## Grounding

Distilled (no verbatim) from this package's principles (P040, P002, P012, P014, P004, P010, P011, P019, P018, P001, P006, P046) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
