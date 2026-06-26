---
name: review-special-methods-and-data-model
kind: skill
status: ready
provenance:
  principles:
  - P01
  claims:
  - C001
  - C002
  evidence:
  - E001
  - E002
  source_anchors:
  - luciano-ramalho-flue-ca307a52-h0033
  authored_from_digest: 1ad0bb35de8e29421fd7a4aa974c2ea2c8757854a5721a0fe29b8d08f1720dc5
---

# Review special methods and the data model

## Purpose

Check that a class integrates with core Python constructs — iteration, operators,
`len()`, subscripting, `with`-blocks, string representation — through the *documented*
special (dunder) methods, and that the interpreter and built-in functions are left to
dispatch to them, rather than the class exposing ad-hoc method names or inventing its
own double-underscore names. (P01)

## When to use

- A class needs to support iteration, operator use, `len()`, subscripting, context
  management, or its own string/`repr` form.
- A class reimplements a standard operation under a non-standard name (`size()`,
  `length()`, `getItem`) instead of the protocol the language already defines.
- Code defines a custom `__name__` that is not an explicitly documented special method.

Do not apply when the code is only plain functions that need no integration with a
language protocol — there is nothing for a dunder to hook into.

## Procedure

1. **Identify the protocols the object should participate in.** Map the object's intended
   behaviour to the data-model categories: collections/containers, attribute access,
   iteration (including `async for`), operator overloading, function/method invocation,
   string representation and formatting, `await`, object creation and destruction, and
   managed contexts via `with`/`async with`.
2. **Confirm each protocol is implemented via its documented dunder.** For every category
   in use, check the matching special method is present (see the
   [special-methods reference](../../references/python-special-methods-reference.md)). The
   payoff: callers reach the behaviour through the standard built-in or syntax
   (`len(obj)`, `obj[key]`, `for x in obj`, `with obj:`) and can reuse the standard
   library instead of memorising bespoke names.
3. **Flag a standard operation hidden behind a non-standard name.** A `.size()` /
   `.length()` that should be `__len__`, a `get(i)` that should be `__getitem__`, an
   `equals()` that should be `__eq__`. Recommend implementing the dunder so the built-in
   and operator syntax dispatch to it.
4. **Flag invented double-underscore names.** Any `__custom__` name that is not an
   explicitly documented special method is subject to breakage without warning; recommend
   a normal name (a single leading underscore if it is internal). (C002)
5. **Do not over-prescribe.** If the object exposes no language protocol, do not demand
   dunders; recommend them only where a built-in or syntax should dispatch to the class.

## Inputs

- The Python class or module under review and its intended behaviour (what built-ins,
  operators, or `with`/iteration syntax callers are expected to use on it).
- The target Python version, where it affects which special methods exist (e.g. async
  protocols).

## Output

A `review`/`advise` finding per issue: the protocol involved, the missing, misused, or
invented special method, and the minimal fix — implement the documented dunder, or rename
the invented name — each traced to P01.

## References

- [python-special-methods-reference](../../references/python-special-methods-reference.md)
  — the dunder names grouped by data-model category.

## Provenance

Derived from principle **P01** (claims **C001**, **C002**; evidence **E001**, **E002**),
grounded in the Fluent Python data-model section (anchor
`luciano-ramalho-flue-ca307a52-h0033`). Distillation-only source: paraphrased, no verbatim
quotation. Dunder method names are public Python-language facts.
