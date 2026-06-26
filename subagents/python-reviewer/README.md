# Python Code Reviewer

A generated subagent package that reviews **Python code for idiomatic
correctness and Pythonic design**. It names the most error-prone or
non-idiomatic pattern first and proposes the smallest behaviour-preserving fix.

- **Slug:** `python-reviewer`
- **Tier:** 2 (multi-source)
- **Status:** draft (skill/reference bodies are stubs)
- **Version:** 0.1.0

## Grounding

Distilled from two canonical Python references (both `distillation-only`, no
verbatim quotation):

- *Fluent Python*, 2nd ed. — Luciano Ramalho (2022): the data model, special
  methods, sequences, comprehensions, references and mutability.
- *Python Distilled* — David M. Beazley (2021): core semantics, object-oriented
  design, resource management, and exceptions.

## What it does

Five modes: `review`, `advise`, `compare`, `validate`, `patch-suggest`. Typical
findings include mutable default arguments, `==` versus `is`, shallow-copy
aliasing, data-class smells, subclassing built-in types, Java-style get/set
methods, manual resource handling, and over-broad `except` clauses — each traced
to one of 15 principles (`principles/principles.yaml`).

## What it is not

Not a performance/profiling tool, not a defect debugger, not a reviewer for
non-Python code, and not a product or architecture advisor.

## Canonical source of truth

`profile.yaml` is canonical. The runnable adapter is exported to
`.claude/agents/generated/python-reviewer.md` — do not edit that file by
hand. Re-run `python -m tools.subagent_factory.cli validate python-reviewer`
after any change.
