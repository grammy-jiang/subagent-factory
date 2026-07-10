# Legacy Code Change Advisor

A generated Claude Code subagent that guides developers in **safely changing
untested or hard-to-test legacy code**, grounded in *Working Effectively with
Legacy Code* (Michael C. Feathers, 2005).

## What it does

Given a piece of legacy code that must change, the advisor:

- drives the change through the **Legacy Code Change Algorithm** (identify change
  points → find test points → break dependencies → write tests → change & refactor);
- diagnoses whether a dependency must be broken for **sensing** or **separation**;
- finds and exploits **seams** (preprocessing / link / object) via their enabling point;
- specifies **characterization tests** that pin actual behaviour (not intended);
- selects the right dependency-breaking technique — **Sprout / Wrap Method or
  Class, Extract Interface** — and keeps pre-test refactoring conservative.

## Modes

`advise` · `review` (test-coverage adequacy) · `extract` (effect sketch / seam
classification) · `patch-suggest` (bounded, suggest-only).

## When NOT to use

Greenfield design, exploratory bug-hunting QA, or full re-architecture/rewrite.

## Canonical source of truth

`profile.yaml` is canonical. The installed adapter
(`.claude/agents/generated/legacy-code-change-advisor.md`) is generated — do not
edit it by hand. Re-export after any profile change:

```bash
python -m tools.subagent_factory.cli export legacy-code-change-advisor
python -m tools.subagent_factory.cli validate legacy-code-change-advisor
```

## Status

`draft` (v0.1.0) — skill and reference bodies are stubs. Run with
`--author-skills` to author them and promote to `ready`.

## Rights

Source is `distillation-only` (© 2005 Pearson Education / Prentice Hall PTR).
No verbatim quotation appears in generated artifacts.
