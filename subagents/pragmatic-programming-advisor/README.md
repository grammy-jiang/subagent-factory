# Pragmatic Programming Advisor

**Slug:** `pragmatic-programming-advisor`
**Version:** 0.1.0
**Tier:** 1
**Status:** draft

## Purpose

A software craftsmanship advisor grounded in The Pragmatic Programmer (Hunt &
Thomas, 1999). Reviews code, designs, and development practices against 14
promoted principles and 70 numbered tips. Guides developers and teams on DRY,
orthogonality, tracer-bullet vs prototyping trade-offs, defensive programming,
ruthless automated testing, disciplined refactoring, build automation,
debugging discipline, and realistic estimation.

## Supported modes

| Mode | Trigger | Deliverable |
|------|---------|-------------|
| advise | Design question or trade-off without an artefact | Prescriptive guidance with principle citation |
| review | Existing code/design/practice submitted for evaluation | Annotated list of principle violations with corrective actions |
| compare | Two or more approaches submitted (e.g., tracer vs prototype) | Structured comparison with context-specific recommendation |
| patch-suggest | Bounded corrective change identified during review | Minimal refactoring suggestion with rationale and risk explanation |

## When to use

- DRY violation detected in code, docs, or config.
- Design review reveals coupled components (orthogonality / Law of Demeter).
- Team deciding between tracer-bullet development and throwaway prototyping.
- Code accumulating broken windows or deferred technical debt.
- Team lacks automated test strategy.
- Estimate needs units and uncertainty framing.

## When NOT to use

- Selecting a universally best language, OS, or tool.
- Writing or implementing production application code.
- Rubber-stamping auto-generated code the developer cannot explain.

## Source

The Pragmatic Programmer: From Journeyman to Master, Andrew Hunt and David
Thomas, Addison-Wesley, 1999.
Rights status: distillation-only.

## Package layout

```
profile.yaml                   Canonical profile (Tier 1)
principles/principles.yaml     14 promoted principles (ppa-p001..p014)
policy/patch-policy.yaml       Patch-suggest mode policy
analysis/claims.jsonl          60 extracted claims
evidence/evidence-records.yaml 40 evidence records
tests/golden-tests.yaml        3 golden tests (1 negative routing)
provenance-ledger.md           Full distillation log
CHANGELOG.md                   Version history
```
