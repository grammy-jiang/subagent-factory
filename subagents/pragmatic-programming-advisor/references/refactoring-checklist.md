---
name: refactoring-checklist
kind: reference
status: ready
provenance:
  principles:
  - P024
  - P051
  - P063
  claims:
  - C00260
  - C00261
  - C00262
  - C00263
  - C00264
  - C00370
  - C00373
  - C00374
  source_anchors: []
  authored_from_digest: fc0254bfd27c7228f835426db12489c169fd5bdbaa1a138a60208672c2f9895d
---

# Refactoring Checklist

Refactor as soon as a trigger appears — deferral costs more later because the number of
dependencies keeps growing.

## Triggers — refactor when you see any of these

Drawn from P024 / C00260.

- [ ] **DRY violation** — the same knowledge is represented in more than one place.
- [ ] **Nonorthogonal design** — a change in one component forces changes in unrelated ones.
- [ ] **Outdated knowledge** — the code no longer reflects reality (requirements, data, or
      understanding have drifted).
- [ ] **Performance need** — functionality must move (e.g. across a boundary) to meet a
      performance requirement.
- [ ] **Global data** — a piece of shared state couples every component that touches it
      (P063 / C00065); pass context explicitly instead.
- [ ] **Near-identical functions** — duplicated logic that differs only in minor detail
      signals a structural problem; refactor via Strategy or a shared abstraction
      (P063 / C00066).

## Coupling-reduction refactorings — do these when the trigger appears

Drawn from P051 / C00370, C00373, C00374.

- [ ] **Header includes pulling in the whole system (C++)** — replace a full-header include
      with a forward declaration in the interface file; include the full header only where
      the definition is actually needed (C00370).
- [ ] **Type-code switch or if-chain on variants** — replace enumerated type-codes with
      subclasses and polymorphic dispatch; the switch-on-type disappears (C00373).
- [ ] **Inheritance used only for reuse** — if a class merely uses another's functionality
      without truly being that type, prefer delegation (has-a); abstract the varying part
      into its own type so the compiler flags affected code (C00374).
- [ ] **Polling reports** — replace a report that scans all records with a listener or
      observer so entities push their own events; eliminates long batch runs and
      tight temporal coupling (P051 / C00372).

## Rules — how to refactor safely

Drawn from P024 / C00262, C00263, C00264.

- [ ] **Refactor early and track what you cannot fix now** — schedule deferred work and
      communicate the impact to affected parties; the cost only rises as dependencies
      accumulate (C00261, C00262).
- [ ] **Do not add functionality while refactoring.** Change behaviour and restructure in
      separate steps — never both at once (C00263).
- [ ] **Have good tests before you start, and run them often.** Ensure tests exist, and run
      them as frequently as possible so any regression surfaces immediately (C00263).
- [ ] **Take short, deliberate steps.** Each change — move a field, fuse two similar
      methods — must be small enough to verify independently; avoid prolonged debugging
      sessions (C00263).
- [ ] **Break the build on incompatible interface changes.** When a module's interface
      changes drastically, make old clients fail to compile so every dependent is found
      and updated quickly (C00264).

## Provenance

Derived from P024 (treat software as gardening; refactor early and often on the four
triggers, with tested steps and no simultaneous feature work), P051 (concrete
coupling-reduction refactorings: forward declarations, type-code subclasses, delegation
over inheritance, observer over polling), and P063 (avoid global data and near-identical
functions, refactoring the latter via Strategy). Claims C00260-C00264 (P024 trigger and
safety rules) and C00370, C00373, C00374 (P051 coupling refactorings) verified against
analysis/claims.jsonl. Source is distillation-only; all wording is paraphrased.
