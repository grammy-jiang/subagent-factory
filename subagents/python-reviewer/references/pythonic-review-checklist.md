---
name: pythonic-review-checklist
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P005
  - P010
  - P011
  - P015
  - P017
  - P021
  - P023
  - P024
  - P025
  - P046
  - P047
  - P054
  - P055
  claims:
  - C00027
  - C00028
  - C00029
  - C00031
  - C00682
  - C00756
  - C00758
  - C00759
  - C00036
  - C00037
  - C00040
  - C00761
  evidence:
  - E00020
  - E00021
  - E00022
  - E00023
  - E00222
  - E00236
  - E00237
  - E00238
  - E00024
  - E00025
  - E00026
  - E00239
  source_anchors:
  - 5c81071aa988-c0004
  - 2bf219904a5b-c0001
  - 2bf219904a5b-c0003
  - 5c81071aa988-c0005
  authored_from_digest: 6c468d4cfdeeb171badd415f0004825818378609a4df7e85aa1ae47bd6402a59
---

# Pythonic review checklist

The gating checklist for an idiomatic-Python review. Each row names a pattern to look for,
the idiomatic verdict or fix, the principle it traces to, and the skill that handles it.

**Ordering rule.** Report findings by impact, not by personal preference: a correctness
defect (severity **Defect**) before a design issue (**Design**) before a stylistic or
targeted-optimization note (**Style/Opt**). A genuine defect (aliasing, a swallowed
exception, a subclassed built-in) must be distinguished from a stylistic preference.

**Hedge rule.** Rows marked *hedged* carry a condition or exception that must be preserved
— do not flatten them into an absolute.

## Correctness defects (report first)

| # | Look for | Idiomatic verdict / fix | Principle | Skill |
|---|----------|-------------------------|-----------|-------|
| 1 | Mutable default argument: `def f(x=[])`, `def g(o={})` | Default to `None`; build the object inside the body. The default is evaluated once and shared across calls. | P04 | review-mutable-default-arguments |
| 2 | `== None` / `!= None`, or `is` against a non-singleton | Use `is None` / `is not None`; use `==` for value comparison. Reserve `is` for singletons. *(hedged: `is` against a documented singleton is correct)* | P02 | review-equality-identity-and-copies |
| 3 | Shallow copy (`list(x)`, `x[:]`, `copy.copy`) of nested mutable data, then mutated | Use `copy.deepcopy` (or explicit deep clone) when nested items must be independent. *(hedged: harmless if all items immutable)* | P03 | review-equality-identity-and-copies |
| 4 | Subclassing built-in `dict`/`list`/`str` with overridden dunders | Use `collections.UserDict`/`UserList`/`UserString` or composition; C-level methods bypass the overrides. | P08 | review-inheritance-and-composition |
| 5 | Manual `open()`/`close()` for a file, lock, or connection | Use a `with`-statement / context manager so cleanup runs on every path, including errors. | P14 | review-resource-and-exception-handling |
| 6 | Catching an exception that cannot be handled locally | Let it propagate to a caller that can recover. *(hedged: applies when there is no sensible local recovery)* | P15 | review-resource-and-exception-handling |
| 7 | Blanket `except Exception` / bare `except:` where a specific type is meant | Narrow the clause; a blanket catch swallows programming errors. *(hedged: a deliberate top-level log-and-shutdown boundary is allowed)* | P15 | review-resource-and-exception-handling |
| 8 | Raising generic errors for intentional application failures | Define custom exception types (subclass `Exception`) so intentional errors are distinguishable from bugs. | P15 | review-resource-and-exception-handling |

## Design issues (report next)

| # | Look for | Idiomatic verdict / fix | Principle | Skill |
|---|----------|-------------------------|-----------|-------|
| 9 | A standard operation under a non-standard name (`size()`, `getItem`), or an invented `__name__` | Implement the documented special method so built-ins/operators dispatch; never invent undocumented dunder names. | P01 | review-special-methods-and-data-model |
| 10 | Inheritance used where the object merely *uses* another (uses-a) | Prefer composition and delegation for looser coupling. *(hedged: true is-a specialization keeps inheritance)* | P07 | review-inheritance-and-composition |
| 11 | A Data Class: fields + get/set, no behaviour, logic scattered elsewhere | Move the related behaviour into the class. *(hedged: deliberate scaffolding or immutable boundary IR is allowed)* | P05 | review-class-design-smells |
| 12 | `getX`/`setX` pairs; double-underscore used as general "private" | Expose plain attributes; `_name` for internal; add `@property` only for validation/computed values; `__name` only to avoid inheritance clashes. | P10, P11 | review-encapsulation-and-properties |
| 13 | `isinstance`/`type` checks gating behaviour the protocol could provide | Depend on the protocol (attributes/methods), not the concrete class. *(hedged: keep a genuine type guard; medium confidence)* | P09 | review-duck-typing-and-protocols |

## Style and targeted optimizations (report last)

| # | Look for | Idiomatic verdict / fix | Principle | Skill |
|---|----------|-------------------------|-----------|-------|
| 14 | Over-long or side-effect-only comprehension; `map`/`filter`/accumulation loop | Prefer a short, pure comprehension/genexp; rewrite a long or side-effect one as a loop or named generator. *(hedged: leave a short, pure, readable comprehension)* | P06 | review-comprehension-style |
| 15 | Metaclasses, descriptors, multiple inheritance, mixins where a plain class works; hard-to-test code | Prefer the simplest construct; treat un-observability as a signal to reorganise. *(hedged: keep an advanced construct genuinely required)* | P13 | review-class-design-smells |
| 16 | Reflex use of `__slots__` | Recommend only for large instance counts with a fixed attribute set; always state the inheritance/`__dict__` trade-offs. *(hedged; medium confidence)* | P12 | review-slots-and-memory |

## Out of scope

Pure runtime/algorithmic performance tuning, non-Python code, root-cause debugging of a
specific runtime failure, and product/architecture decisions are out of scope — hand off
rather than review.

## Provenance

Built from principles **P01–P15** (claims **C001–C018**, evidence **E001–E018**) over
Fluent Python and Python Distilled (anchors listed in frontmatter). Both sources are
distillation-only: this checklist paraphrases and restructures; it contains no verbatim
quotation. Each fix is the minimal behaviour-preserving change and traces to its principle.
