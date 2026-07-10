---
name: dependency-breaking-techniques
kind: reference
status: ready
provenance:
  principles:
  - P038
  - P020
  - P135
  - P035
  - P015
  - P086
  - P111
  - P016
  - P052
  - P054
  - P112
  - P087
  - P098
  - P107
  claims:
  - C00523
  - C00526
  - C00527
  - C00528
  - C00529
  - C00564
  - C00565
  - C00566
  - C00567
  - C00568
  source_anchors:
  - 1d83dc6f489c-c0023
  - 1d83dc6f489c-c0026
  authored_from_digest: 60bd2817aaf749fd4f42df9282d0e5bbbb5652f20193b5f0cf58c273b85720c2
---

# Dependency-breaking techniques

A selection catalog for getting hard-to-test legacy code into a harness. First classify *why*
the dependency blocks the test — **sensing** (cannot observe a computed value) or
**separation** (cannot instantiate/run in a harness) — then pick the technique. Faking a
collaborator is the dominant *sensing* move; there are many *separation* techniques. Look
ahead to the resulting aftermath before choosing an approach, and treat these as
behaviour-preserving refactorings applied — exceptionally — before tests exist, so keep each
incision conservative and signature-preserving.

## Technique table

| Technique | Use when | What it does |
|-----------|----------|--------------|
| **Extract Interface** (P038) | You can modify the class you depend on. | Create an interface with the methods you use and depend on it; substitute a fake/testing implementation under test. One of the safest techniques — the compiler catches missteps. |
| **Subclass and Override Method** (P020, P135) | A localized method call must be neutralized for a test. | Override the offending method in a testing subclass to nullify or sense it — but only when the override does not change the behaviour you must preserve. The core technique many others are variants of. |
| **Extract and Override Factory Method** (P035) | A constructor creates an object you cannot depend on under test. | Move the hard-coded creation into a factory method and override it in a testing subclass (where the language allows overriding from a constructor). |
| **Extract and Override Call** (P086) | A single static, global, or object-method call blocks the test. | Extract the call into a local method and override it in a testing subclass. |
| **Parameterize Constructor** (P015) | A constructor allocates a collaborator you cannot reach under test. | Pass the object in through the constructor while keeping the original signature delegating, so existing clients do not change. |
| **Parameterize Method** (P098) | A method creates an object internally that you must replace. | Pass the object in through a new method while keeping a no-argument forwarding method named after the parameter type. |
| **Replace Global Reference with Getter** (P111) | A class reaches globals or class-static methods directly. | Introduce a protected getter for each global (a call to a static method counts as a global) and override it in a testing subclass. |
| **Adapt Parameter** (P016, P052) | A parameter's type is a sealed/final library class you cannot Extract Interface on. | Wrap the parameter behind your own interface the class under test uses, so a fake can be supplied. |
| **Expose Static Method** (P054) | A method uses little or no instance data but its class is hard to construct. | Make the method static so it can be tested without instantiating the class. |
| **Push Down Dependency** (P112) | Problematic dependencies are pervasive throughout a class. | Make the current class abstract and push the troublesome dependencies down into a concrete production subclass, testing a testing subclass. |
| **Pull Up Feature** (P087) | The dependencies blocking a class are unrelated to the methods you want to test. | Move the testable cluster of methods up into an abstract superclass, then subclass it for testing. |
| **Object seam via parameter** (P107) | A hard-coded call should become substitutable. | Pass the collaborator in as a parameter (the enabling point is the argument list), turning the call into an object seam. |

## Discipline (applies to all)

- **Conservative incisions before tests exist:** make minimal, signature-preserving changes
  first, even if the code temporarily looks worse; heal the "scar" once tests cover the area.
- **Prefer Extract Interface and object seams** in object-oriented code — the compiler helps
  and the substitution stays explicit and local (see `seam-model`).
- **Do not extract an interface for every parameter dependency** (P037-adjacent guidance): a
  near one-to-one class-to-interface ratio clutters the design — ask why the dependency hurts
  first.

## Provenance

Derived from the named dependency-breaking principles P038, P020/P135, P035, P086, P015,
P098, P111, P016/P052, P054, P112, P087, and P107. Source is distillation-only; the technique
names are the source's; descriptions are paraphrased, not quoted.
