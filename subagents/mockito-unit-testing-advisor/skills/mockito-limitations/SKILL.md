---
name: mockito-limitations
kind: skill
status: ready
provenance:
  principles:
  - PRP-005
  claims:
  - CL010
  - CL011
  source_anchors: []
  authored_from_digest: 4bcb514c239df28842d040f562684c96ca1527cb80ae9be44094454dd3e7a726
---

# Mockito Limitations

## Purpose

Recognise what plain Mockito cannot mock and respond by refactoring the production code to remove
the constraint rather than reaching for PowerMockito (PRP-005). Mocking static or private members
violates encapsulation and produces brittle tests.

## When to use

- Using standard Mockito without the `mockito-inline` mock maker (Mockito 3 and earlier, or when
  the inline module is not on the classpath).
- The dependency to mock is declared `final`, `static`, or `private`.

## Procedure

1. **Check the type against the limit list (CL010).** Plain Mockito cannot mock or spy on: final
   classes and final methods, static methods, enums, private methods, `equals()`/`hashCode()`,
   primitive types, or anonymous classes. If the dependency falls into one of these, plain Mockito
   will not isolate it.
2. **Prefer a refactor over PowerMockito (CL011, PRP-005).** PowerMockito can mock static and
   private members, but doing so violates encapsulation and yields fragile tests. The preferred fix
   is to refactor the offending code so it becomes testable: extract an interface, introduce an
   indirection, or replace a static call with instance delegation, then mock the new seam.
3. **Note the modern escape hatch.** When `mockito-inline` (Mockito 4+) is on the classpath,
   final-class mocking is supported natively without PowerMockito (`does_not_apply_when`). Confirm
   the Mockito version in use before assuming the limit applies.
4. **State the limit honestly.** Do not claim plain Mockito can mock final/static/private/enum
   members. Recommend the refactor and name the constraint; if the team has explicitly accepted the
   PowerMockito dependency after weighing the refactor cost, that is their call to record, not a
   default to suggest.

## Inputs

- The dependency to be mocked and its declaration (final/static/private/enum/etc.).
- The Mockito version and whether `mockito-inline` is on the classpath.

## Output

A determination of whether plain Mockito can mock the dependency, and — when it cannot — a
refactoring recommendation (extract interface / indirection / instance delegation) rather than a
PowerMockito workaround.

## References

- (none — this package declares no reference docs.)

## Provenance

Principle PRP-005; claims CL010 (what plain Mockito cannot mock), CL011 (PowerMockito vs refactor,
encapsulation cost). Distillation-only source; paraphrased, no verbatim quotation.
