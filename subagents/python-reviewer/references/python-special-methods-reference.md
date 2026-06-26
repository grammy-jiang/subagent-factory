---
name: python-special-methods-reference
kind: reference
status: ready
provenance:
  principles:
  - P003
  - P016
  - P020
  - P034
  - P035
  - P038
  - P056
  - P059
  - P060
  claims:
  - C00430
  - C00431
  - C00432
  - C00433
  - C00839
  - C00840
  - C00841
  - C00489
  - C00490
  - C00491
  - C00842
  - C00843
  evidence:
  - E00180
  - E00181
  - E00182
  - E00183
  - E00246
  - E00247
  - E00248
  - E00192
  - E00193
  - E00194
  - E00249
  - E00250
  source_anchors:
  - 5c81071aa988-c0038
  - 2bf219904a5b-c0006
  - 5c81071aa988-c0045
  authored_from_digest: d9a1cd098e78cf256627ba484d1a584ad5e069d3ec18f75fca2714738717ab7d
---

# Python special methods reference

A lookup of the documented special (dunder) methods grouped by the data-model categories
they serve. Use it with [review-special-methods-and-data-model](../skills/review-special-methods-and-data-model/SKILL.md):
implement the special method for a category and let the built-in or syntax dispatch to it,
instead of inventing a bespoke method name. Method names below are public Python-language
facts.

## Special methods by data-model category

| Category | Built-in / syntax that triggers it | Special method(s) |
|----------|-----------------------------------|-------------------|
| String representation & formatting | `repr(x)`, `str(x)`, `bytes(x)`, `format(x, spec)` / f-strings | `__repr__`, `__str__`, `__bytes__`, `__format__` |
| Collections / containers | `len(x)`, `x[k]`, `x[k] = v`, `del x[k]`, `k in x` | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__` |
| Iteration | `iter(x)`, `next(it)`, `reversed(x)` | `__iter__`, `__next__`, `__reversed__` |
| Asynchronous iteration | `async for` | `__aiter__`, `__anext__` |
| Operator overloading — arithmetic | `+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`; in-place (`+=`, …); unary (`-x`, `+x`, `abs(x)`) | `__add__`/`__radd__`/`__iadd__` (and peers per operator), `__neg__`, `__pos__`, `__abs__` |
| Operator overloading — comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` |
| Truth value & hashing | `bool(x)`, `hash(x)` | `__bool__`, `__hash__` |
| Attribute access | `x.attr`, `x.attr = v`, `del x.attr`, `dir(x)` | `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__dir__` |
| Function / method invocation (callable) | `x(...)` | `__call__` |
| Object creation & destruction | instance creation, initialization, finalization | `__new__`, `__init__`, `__del__` |
| Managed contexts | `with x:` | `__enter__`, `__exit__` |
| Asynchronous managed contexts | `async with x:` | `__aenter__`, `__aexit__` |
| Awaitables | `await x` | `__await__` |

## Review rules

- **Implement, don't reinvent.** When a class should support a category above, implement
  its special method so callers reach it through the standard built-in or syntax — not via
  a custom name like `size()` or `getItem`. (P01)
- **Never invent dunder names.** Any `__name__` that is not an explicitly documented
  special method is subject to breakage without warning; use a normal name (a single
  leading underscore if internal) instead. (C002)

## Provenance

Categories are drawn from the Fluent Python data-model section (anchor
`luciano-ramalho-flue-ca307a52-h0033`; principle **P01**, claims **C001**, **C002**,
evidence **E001**, **E002**). The source is distillation-only: this table paraphrases the
category structure and lists language-defined method names; it contains no verbatim
quotation.
