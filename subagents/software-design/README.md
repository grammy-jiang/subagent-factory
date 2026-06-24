# Software Design Reviewer (`software-design`)

A generated Claude Code subagent that reviews code and software designs for structural
complexity, modularity, simplicity, readability, and changeability — and recommends the
smallest safe structural improvement.

It fuses five canonical software-design texts into one review discipline:

- **A Philosophy of Software Design** (John Ousterhout) — complexity (dependencies +
  obscurity), deep vs. shallow modules, information hiding, pull complexity downward, red
  flags.
- **Code Simplicity** (Max Kanat-Alexander) — the Equation of Software Design, the three
  flaws, simplicity as the lever for maintainability.
- **Clean Code** (Robert C. Martin) — intention-revealing names, small single-purpose
  functions, the single-responsibility principle, clean tests.
- **Refactoring** (Martin Fowler) — the code-smell catalogue and behaviour-preserving,
  test-backed refactoring under the two hats.
- **Design Patterns** (Gamma, Helm, Johnson, Vlissides) — program to an interface, favour
  composition over inheritance, encapsulate what varies, apply patterns judiciously.

## When to use it

- Reviewing a class/module/function for shallow interfaces, doing-too-much, or leakage.
- Diagnosing change amplification / shotgun surgery (a small change touching many places).
- Getting a prioritised list of code smells and the refactorings that remove them.
- Comparing design alternatives (design it twice) by value over future maintenance effort.
- Gating new abstractions, configuration, generality, or patterns against speculative
  complexity.

## When not to use it

- Pure runtime performance tuning, product/roadmap decisions, runtime-failure debugging,
  or visual/UI design.

## Modes

`review` · `advise` · `compare` · `validate` · `patch-suggest` (design sketches only — it
never applies code changes autonomously).

## Status

`draft` (Tier 2). The canonical source of truth is `profile.yaml`. Skill and reference
bodies are stubs; run the Step 8.7 authoring pass (`--author-skills`) to promote the
package to `ready`. Do not edit the installed adapter under `.claude/agents/generated/`
directly — it is regenerated from `profile.yaml` via `cli export`.

## Provenance & rights

All five sources are copyrighted and classified `distillation-only`: paraphrase and
synthesis only, **no verbatim quotation**. See `provenance-ledger.md` for the full
distillation log, evidence chain, and the one logged cross-source conflict.
