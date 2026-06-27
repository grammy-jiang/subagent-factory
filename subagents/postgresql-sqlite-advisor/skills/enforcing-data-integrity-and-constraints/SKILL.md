---
name: enforcing-data-integrity-and-constraints
kind: skill
status: ready
provenance:
  principles:
  - P026
  - P033
  - P034
  - P050
  claims:
  - C00807
  - C00808
  - C00101
  - C00102
  - C00067
  - C00068
  - C00810
  - C00864
  evidence:
  - E00206
  - E00207
  - E00028
  - E00029
  - E00018
  - E00019
  - E00209
  - E00235
  source_anchors:
  - 9aa0ce19c36d-c0002
  - 82a20f5886e3-c0002
  - 82a20f5886e3-c0001
  - 9aa0ce19c36d-c0003
  authored_from_digest: 35f9479187354d9084229260f3ddd71787f2044b352fbec179608309916e743c
---

# Enforcing data integrity with constraints

## Purpose

Push data validity into the schema — domain, entity, referential, and user-defined integrity — so the database, not application code, rejects invalid data.

## When to use

When deciding where and how to enforce data validity, required values, and allowed ranges.

## Procedure

1. Enforce data integrity through schema constraints, not application code - cover domain, entity, referential, and user-defined integrity using NOT NULL (paired with DEFAULT), UNIQUE, CHECK, and COLLATE on columns or tables, defined once in the database. (P026)
2. Set the logical specification elements to enforce value integrity: no nulls for keys/required fields (never blanks for meaning), required value yes for primary keys, meaningful default values only, an explicit range of values (never Other/Miscellaneous), an edit rule, and allowed comparisons/operations. (P033)
3. Understand the four types of data integrity (table-, field-, relationship-level, and business rules) and the three relationship characteristics (type, participation type, degree) as the integrity framework the whole methodology builds. (P034)
4. Handle NULL deliberately - NULL is the absence of a value (not zero, empty string, true, or false); test it with IS NULL / IS NOT NULL (never = NULL), expect it to propagate through expressions and three-valued logic, know that it is dropped by WHERE and ignored by aggregates, and use COALESCE to supply defaults in nullable expressions. (P050)

## Grounding

Distilled (no verbatim) from this package's principles (P026, P033, P034, P050) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
