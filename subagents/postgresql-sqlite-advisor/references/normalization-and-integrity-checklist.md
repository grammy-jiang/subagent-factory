---
name: normalization-and-integrity-checklist
kind: reference
status: ready
provenance:
  principles:
  - P024
  - P032
  - P033
  - P034
  - P026
  - P031
  - P045
  claims:
  - C00803
  - C00804
  - C00064
  - C00099
  - C00101
  - C00102
  - C00067
  - C00068
  - C00807
  - C00808
  - C00182
  - C00255
  - C00083
  - C00084
  evidence:
  - E00204
  - E00205
  - E00017
  - E00027
  - E00028
  - E00029
  - E00018
  - E00019
  - E00206
  - E00207
  - E00050
  - E00083
  - E00025
  - E00026
  source_anchors:
  - 9aa0ce19c36d-c0001
  - 82a20f5886e3-c0001
  - 82a20f5886e3-c0002
  - 9aa0ce19c36d-c0002
  - 82a20f5886e3-c0004
  authored_from_digest: 42680af8b727938e110d2ed6af9d8094b99813529da966978af58266781aee89
---

# Normalization and integrity checklist

A modular checklist for keys, normalization, and the four kinds of data integrity.

- **P024** — Give every relation a primary key that uniquely identifies its rows (no duplicate rows) and normalize to remove duplication - 1NF atomic values, 2NF dependence on the whole key, 3NF no transitive dependencies - decomposing tables so implicit relationships become explicit and enforceable.
- **P032** — Give every table a primary key chosen from candidate keys that conform to the Elements of a Candidate Key (no multipart, unique, non-null, no privacy breach, non-optional, minimal fields, exclusively identifies each record, rarely changes).
- **P033** — Set the logical specification elements to enforce value integrity: no nulls for keys/required fields (never blanks for meaning), required value yes for primary keys, meaningful default values only, an explicit range of values (never Other/Miscellaneous), an edit rule, and allowed comparisons/operations.
- **P034** — Understand the four types of data integrity (table-, field-, relationship-level, and business rules) and the three relationship characteristics (type, participation type, degree) as the integrity framework the whole methodology builds.
- **P026** — Enforce data integrity through schema constraints, not application code - cover domain, entity, referential, and user-defined integrity using NOT NULL (paired with DEFAULT), UNIQUE, CHECK, and COLLATE on columns or tables, defined once in the database.
- **P031** — Perform a final modular data-integrity review against the table-, field-, relationship-, and business-rule checklists, then assemble the RDBMS-independent design documentation as the implementation blueprint.
- **P045** — Establish relationships explicitly: a copied primary key as a foreign key for one-to-one and one-to-many, and a linking table (composite primary key) for many-to-many — never embed repeated or single copies of one table's fields in the other.

## Grounding

Distilled (no verbatim) from this package's principles (P024, P032, P033, P034, P026, P031, P045) and their anchored claims. Verify version-specific availability against current official PostgreSQL or SQLite documentation.
