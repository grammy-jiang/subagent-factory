---
name: designing-schemas-keys-and-normalization
kind: skill
status: ready
provenance:
  principles:
  - P043
  - P044
  - P024
  - P032
  - P045
  - P041
  - P025
  - P034
  - P031
  - P030
  - P023
  claims:
  - C00031
  - C00032
  - C00106
  - C00107
  - C00803
  - C00804
  - C00064
  - C00099
  - C00083
  - C00084
  - C00131
  - C00132
  - C00229
  - C00230
  - C00067
  - C00068
  - C00182
  - C00255
  - C00020
  - C00050
  - C00243
  - C00244
  evidence:
  - E00002
  - E00003
  - E00030
  - E00031
  - E00204
  - E00205
  - E00017
  - E00027
  - E00025
  - E00026
  - E00036
  - E00037
  - E00061
  - E00062
  - E00018
  - E00019
  source_anchors:
  - 82a20f5886e3-c0001
  - 82a20f5886e3-c0002
  - 9aa0ce19c36d-c0001
  - 82a20f5886e3-c0003
  - 82a20f5886e3-c0006
  authored_from_digest: 61e1da6624b549aaff1c5daffe3d4e48a6905faf0995cccde737c9dce738ffdb
---

# Designing schemas, keys, and normalization

## Purpose

Turn information requirements into a sound relational schema — tables, primary and foreign keys, normalized structure, views, and the business rules that govern them.

## When to use

When designing a new relational schema or reviewing an existing one for keys, relationships, and normalization.

## Procedure

1. Begin every design by defining a mission statement (the database's purpose) and mission objectives (single-task statements the data must support), and let them drive the table, field, relationship, view, integrity, and business-rule decisions. (P043)
2. Keep the logical design separate from and prior to physical implementation, and design it without regard to any specific RDBMS so the structure is driven by information requirements rather than tool constraints. (P044)
3. Give every relation a primary key that uniquely identifies its rows (no duplicate rows) and normalize to remove duplication - 1NF atomic values, 2NF dependence on the whole key, 3NF no transitive dependencies - decomposing tables so implicit relationships become explicit and enforceable. (P024)
4. Give every table a primary key chosen from candidate keys that conform to the Elements of a Candidate Key (no multipart, unique, non-null, no privacy breach, non-optional, minimal fields, exclusively identifies each record, rarely changes). (P032)
5. Establish relationships explicitly: a copied primary key as a foreign key for one-to-one and one-to-many, and a linking table (composite primary key) for many-to-many — never embed repeated or single copies of one table's fields in the other. (P045)
6. Name each table with a unique, descriptive, single-subject, plural name, avoiding physical-characteristic words, acronyms/abbreviations, data-restricting proper names, and multi-subject names. (P041)
7. Define business rules from how the organization uses its data; establish database-oriented rules in the logical design (field-specific via field-spec elements, relationship-specific via relationship characteristics) and record every rule on a Business Rule Specifications sheet. (P025)
8. Understand the four types of data integrity (table-, field-, relationship-level, and business rules) and the three relationship characteristics (type, participation type, degree) as the integrity framework the whole methodology builds. (P034)
9. Perform a final modular data-integrity review against the table-, field-, relationship-, and business-rule checklists, then assemble the RDBMS-independent design documentation as the implementation blueprint. (P031)
10. Conduct the design interviews deliberately: prepare questions, favour open-ended questions, interview users and management separately, keep the group small, maintain control, and record each interview. (P030)
11. Define views to work with related tables, reflect current data, customize output, enforce integrity (validation view), and restrict access; a multitable view requires its base tables to be related, and views may carry calculated fields, filters, and must be documented. (P023)

## Grounding

Distilled (no verbatim) from this package's principles (P043, P044, P024, P032, P045, P041, P025, P034, P031, P030, P023) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
