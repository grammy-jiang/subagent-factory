# Domain-Driven Design Reviewer

**Slug:** `domain-driven-design-reviewer`
**Version:** 0.3.0
**Tier:** 1
**Status:** ready

## What this subagent does

Reviews, critiques, and guides domain models, ubiquitous language, bounded
contexts, and the seven tactical building-block patterns so that software
accurately reflects the business domain it serves. Grounded in Avram &
Marinescu (2006), a condensed summary of Eric Evans' canonical DDD text.
Principles P001–P013 are evidenced from real section-heading anchors recovered
by Docling PDF conversion (70 headings).

## When to invoke

- A domain model needs review for correct application of Entity, Value Object,
  Service, Aggregate, Factory, and Repository patterns.
- Entity/Value Object classification is unclear — identity-based versus
  attribute-only semantics need adjudication.
- Domain logic is leaking into UI or infrastructure layers.
- A multi-team project needs Bounded Context boundaries drawn, a Context Map
  produced, and inter-context integration patterns evaluated.
- Ubiquitous language is inconsistent between code and domain experts.
- Implicit domain concepts (Constraints, Processes, Specifications) need to be
  surfaced and made explicit.

## When NOT to invoke

- Pure DevOps / infrastructure concerns with no domain-modeling dimension.
- Greenfield projects with no model artifact yet to critique.
- Trivial CRUD applications where a Smart UI is the explicitly acknowledged
  approach.

## Supported modes

| Mode | Purpose |
|------|---------|
| `review` | Critique a submitted domain model or code artifact for DDD correctness |
| `validate` | Pass/fail check of specific DDD conformance rules |
| `advise` | Guide a modeling decision before or during implementation |
| `extract` | Identify implicit domain concepts and recommend making them explicit |

## Required inputs

1. Domain model artifact (diagram, code, or written design document)
2. Business domain context sufficient to judge model accuracy

## Primary output

Structured review report with prioritised findings, each naming the affected
model element, the DDD principle at issue (with principle ID), a severity
grade, and at least one actionable corrective step.

## Grounding principles

13 operational principles (P001–P013) evidenced from Docling-recovered section
headings of the source PDF. All quality_bar items, forbidden_behaviours, modes,
and always_on knowledge reference principle IDs inline.

## Source

Derived from: Abel Avram & Floyd Marinescu, "Domain-Driven Design Quickly"
(InfoQ/C4Media, 2006). Rights status: distillation-only. No verbatim quotation.

Ultimate authority: Eric Evans, "Domain-Driven Design: Tackling Complexity in
the Heart of Software" (Addison-Wesley, 2004).

## Package layout

```
subagents/domain-driven-design-reviewer/
  profile.yaml                          canonical source of truth (v0.3.0, tier 1)
  provenance-ledger.md                  field-level traceability; version 0.3.0 supersession recorded
  CHANGELOG.md
  README.md
  principles/
    principles.yaml                     13 principles P001–P013 (principles-v1)
  analysis/
    claims.jsonl                        extracted claims from Docling-converted source
  evidence/
    evidence-records.yaml               evidence records grounded to 70 heading anchors
  tests/
    golden-tests.yaml                   GT-001, GT-002, GT-003, NR-001, NR-002, MC-001
  skills/
    ubiquitous-language-session/
    refactoring-toward-deeper-insight/
    aggregate-design/
    repository-and-factory-design/
    anticorruption-layer-design/
    domain-distillation/
  references/
    building-block-pattern-summaries.md
    context-map-pattern-catalogue.md
    layered-architecture-layer-responsibilities.md
    refactoring-checklist.md
  policy/
    patch-policy.yaml                   patch-policy-v1, patch_suggest_only
```
