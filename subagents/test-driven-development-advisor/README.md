# test-driven-development-advisor

A subagent that advises on and reviews **test-driven development** practice, grounded in
Kent Beck, *Test-Driven Development By Example* (Addison-Wesley, 2002).

## What it does

Guides a developer through the **red/green/refactor** cycle: which small failing test to
write next, the smallest change to get every test to green, and the refactoring that
removes duplication. It helps choose a get-to-green strategy (**Fake It**, **Obvious
Implementation**, **Triangulation**), keeps work in small increments, and grows the
design one decision at a time.

## Modes

- **advise** — guide the next test-first step with rationale.
- **review** — critique whether a change was driven by tests and refactored cleanly.
- **compare** — contrast get-to-green strategies for a situation.

## When not to use

- Greenfield architecture / technology selection with no unit-level test loop.
- Choosing or configuring a specific test framework's tooling.
- Performance, security, or other concerns with no test-first design dimension.

## Scope note

The ingested source is a **66-page partial** (Introduction + Part I, the Money Example).
Part II (the xUnit Example) and Part III (Patterns for TDD) are not in the source, so the
finer Part III pattern catalogue is out of scope for this package.

## Authority

The developer owns the code and the final decision. Beck's *TDD By Example* is the
authority for the cycle, the two rules, and the strategies this advisor teaches.

## Status

`draft` — `agent_version` 0.1.0. Skill and reference bodies are stubs; run
`Skill("author-skills") test-driven-development-advisor` (Step 8.7) to author them and
promote to `ready`.
