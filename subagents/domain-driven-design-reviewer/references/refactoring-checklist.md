---
name: refactoring-checklist
kind: reference
status: ready
provenance:
  principles:
  - P006
  - P048
  - P024
  - P020
  - P021
  - P030
  - P003
  - P029
  - P050
  - P035
  claims:
  - C00210
  - C00211
  - C00212
  - C00215
  - C00217
  - C00218
  - C00202
  - C00203
  - C00204
  - C00205
  - C00412
  - C00413
  evidence:
  - E00126
  - E00127
  - E00128
  - E00129
  - E00130
  - E00131
  - E00122
  - E00123
  - E00124
  - E00125
  - E00228
  - E00229
  source_anchors:
  - 9e0c1e6c6dd6-c0010
  - 9e0c1e6c6dd6-c0011
  - 9e0c1e6c6dd6-c0022
  authored_from_digest: a1619faef6ec52ba754a1f06b1be3a42522bf4c3a47614c0b509dd0d0fae3f23
---

# Refactoring Checklist

A checklist for domain-insight-driven refactoring. Use alongside the
`refactoring-toward-deeper-insight` skill to assess whether a proposed or completed
refactoring is safe, grounded in the model, and moving toward a deeper understanding
of the domain.

---

## Safety discipline

Before starting any change:

- [ ] The goal is to redesign without altering externally observable behaviour — confirm
      this is true and not a feature change in disguise.
- [ ] The change is broken into small, controllable steps rather than a single large
      rewrite; each step leaves the system in a passing state.
- [ ] An automated test suite exists and covers the affected behaviour. If no tests
      exist, record that absence as a finding and estimate the risk explicitly before
      proceeding.
- [ ] Any change that cannot be done incrementally (a "breakthrough" rework) is flagged
      as high-risk, with estimated time and cost communicated to stakeholders before work
      begins.
- [ ] The existing design is flexible enough to absorb the change; note any stiff
      coupling that resists the move.

---

## Does this refactoring cross a Bounded Context boundary?

Answer before touching code:

- [ ] Identify which Bounded Context(s) the affected classes belong to.
- [ ] If the change touches more than one context, pause: concepts from different
      contexts must not be silently merged. Each context has its own model; a name
      collision is not the same concept.
- [ ] If cross-context translation is required, route through the existing
      Anticorruption Layer or Context Map relationship — do not introduce direct
      dependencies between domain layers of separate contexts.

---

## Signs that a deeper model or missing concept may be warranted

Review the code and conversations for these signals:

- [ ] A term appears frequently in team conversation or domain-expert language but has
      no corresponding class, relationship, or method in the model.
- [ ] A computation path is hard to follow, or a procedure does something convoluted —
      awkwardness often signals a hidden concept doing invisible work.
- [ ] An existing object has accumulated behaviour that does not belong to it; something
      is shouldering responsibility for a concept that should stand on its own.
- [ ] Domain experts use the same term in inconsistent ways, or two requirements appear
      to contradict each other — reconciling the contradiction often reveals a
      distinction the model has not yet made.
- [ ] Published domain literature, established patterns, or prior deep designs in the
      same field contain concepts not yet present in the model.
- [ ] The model started from nouns and verbs only and has never been revisited; shallow
      starter models seldom remain adequate as understanding grows.

---

## What explicit construct to introduce

When a missing concept is confirmed, select the appropriate form:

- [ ] **Constraint** — if the concept is an invariant or business rule that a class must
      satisfy, extract it into a dedicated method or object so it is visible, testable,
      and has room to grow independently.
- [ ] **Process** — if the ubiquitous language names a process and that process is a
      significant domain concept (not merely application orchestration), model it as a
      stateless domain Service. Where the process has interchangeable algorithms, a
      Strategy pattern is appropriate. Do not make every internal process explicit;
      apply this only where the language calls it out as meaningful.
- [ ] **Specification** — if the concept is a complex yes/no business rule used in
      selection, validation, or construction, extract it from the Entity into a
      Specification object in the domain layer. Compose simple specifications into
      composite ones for complex rules.
- [ ] **New class or relationship** — for any other implicit concept that has become a
      key domain idea, give it an explicit class or relationship in the model. Making
      an implicit concept explicit is the primary mechanism through which a design
      breakthrough occurs.

---

## Model-code correspondence check (after the change)

- [ ] The modified code still literally reflects the domain model; any reviewer who
      knows the model can trace the mapping without inference.
- [ ] Developers who changed the code have maintained responsibility for the model's
      integrity — not just the code's cleanliness.
- [ ] Analysis and implementation decisions were made together, not handed off between
      separate roles in isolation; if a handoff occurred, verify the model was kept in
      sync.
- [ ] Refactoring code to a state that is technically cleaner but no longer expresses
      the model is treated as a design failure, not an improvement.

---

## After the change

- [ ] All automated tests pass; behaviour is unchanged.
- [ ] The ubiquitous language in code (class names, method names, module names) still
      corresponds to the language domain experts use.
- [ ] Domain experts, when shown the revised design, agree it reads true to the domain
      and is simpler or more expressive than before.
- [ ] If a new explicit concept was introduced, the team has agreed on the name and
      added it to the shared vocabulary.
- [ ] The change has been incorporated into the model and communicated — it is not
      treated as a local implementation detail.

---

## Provenance

Grounded in principles P006, P048, P024, P020, P021, P030, P003, P029, P050, P035 of this package, derived from Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003). Representative chunk anchors: `9e0c1e6c6dd6-c0010`, `9e0c1e6c6dd6-c0011`, `9e0c1e6c6dd6-c0022`. Source rights: `distillation-only` — all content is paraphrased; no verbatim quotation.
