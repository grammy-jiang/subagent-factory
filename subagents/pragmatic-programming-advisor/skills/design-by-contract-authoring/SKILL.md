---
name: design-by-contract-authoring
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P044
  - P055
  claims:
  - C00163
  - C00164
  - C00165
  - C00166
  - C00167
  - C00168
  - C00171
  - C00177
  source_anchors: []
  authored_from_digest: 2197004cea0af1f3d751c2cf97a37fe7c7b7f613fb7863b2bb5b235bfe818ea0
---

## Purpose

Author or review the contract of a routine — its preconditions, postconditions, and the
class invariants it preserves — so that responsibilities between caller and callee are
explicit, substitutability holds, and contract breaches are treated as bugs rather than
ordinary runtime events.

## When to use

- Specifying a new non-trivial routine or public method whose correct use is not obvious
  from its signature.
- Reviewing a routine that conflates user-input validation with internal correctness
  checks.
- Designing a class hierarchy where subclasses must be safely substitutable for their base.
- Hardening a module boundary where silent acceptance of bad input would corrupt state.
- Designing any piece of software — contract design belongs alongside software design,
  not after it (P055, C00177).

## Procedure

1. **State the preconditions.** Write down exactly what must be true *before* the routine
   may be called — the caller's obligation. Express the routine's valid input domain
   here; this shifts the burden of correctness to the caller where it belongs and lets
   the routine assume valid input (P008, C00163, C00174).

2. **State the postconditions.** Write down what the routine *guarantees* on exit — the
   callee's promise. Keep promises modest: guarantee as little as you can get away with.
   This "lazy" stance (strict in, modest out) keeps contracts honest and easy to satisfy
   (P008, C00166). If a postcondition references a passed-in parameter, prevent the
   routine from modifying that parameter so the contract cannot be circumvented (C00173).

3. **State the class invariants.** Identify the conditions that must hold from a caller's
   perspective throughout the object's observable lifetime, and confirm that each routine
   preserves them on entry and exit (C00163).

4. **Keep the contract abstract.** A postcondition that assumes a particular
   implementation — referencing internal indices or data structure details — is a bad
   contract. Express each clause in terms of the routine's observable behaviour, not its
   internals (P008, C00362).

5. **Separate contract from error handling.** Do not use preconditions to validate
   user input. A precondition violation is a bug, not an expected runtime condition; user
   input is an expected runtime condition handled by normal error handling. Mixing the two
   blurs responsibility (P008, C00165).

6. **Treat a breach as a bug.** The contract reads: if the caller meets every
   precondition, the routine guarantees all postconditions and invariants on completion.
   Any failure to meet this is a program defect. Decide the failure response — fail fast
   or terminate — accordingly rather than quietly continuing (C00164, P031).

7. **Check Liskov substitutability for subclasses.** A subclass must be usable through
   its base-class interface without the caller knowing the difference. It may widen what
   it accepts (weaken preconditions) and strengthen what it guarantees (strengthen
   postconditions), but not the reverse. Specify the contract once in the base class so
   it propagates automatically to every subclass; without this, the compiler can check
   only method signatures, not that methods preserve their meaning (P044, C00167, C00168).

8. **Pin boundary conditions with loop and semantic invariants.** For every significant
   loop, identify a loop invariant — a statement of the loop's goal that holds before
   the loop and after every iteration — to get boundary conditions right and to serve as
   a design and documentation aid (P055, C00177). For inviolate system requirements,
   capture them as semantic invariants and distinguish them clearly from policies that
   may change (C00178, C00179).

9. **Record the contract where it is enforceable.** Express each clause as an assertion,
   a documented invariant, or a contract annotation so it can be checked, not just hoped
   for. Recognize that assertions only partially emulate Design by Contract: they do not
   propagate down an inheritance hierarchy and lack a built-in concept of entry values
   (P044, C00171). In languages without native DBC support, write the contract as
   comments at minimum; DBC is fundamentally a design technique that still provides a
   starting point when trouble strikes (C00170). Prefer languages or preprocessors with
   real DBC support when available (C00172). See `assertion-programming-patterns` for
   enforcement mechanics.

## Inputs

- The routine signature and its intended behaviour.
- The class invariants the routine participates in.
- The class hierarchy, if substitutability is in scope.
- Any loop structures in the routine, to derive loop invariants.

## Output

- A written contract per routine: preconditions, postconditions, invariants.
- A note on which clauses are enforced as assertions vs documented.
- A substitutability check result for any subclass in the hierarchy.
- Loop invariants for significant loop structures, where applicable.

## References

- `skills/assertion-programming-patterns/SKILL.md` — enforcing contract clauses at runtime.
- `references/pragmatic-tips-70-cheatsheet.md` — Design with Contracts; Crash Early.

## Provenance

Derived from P008 (Design with contracts: preconditions, postconditions, invariants;
keep contracts abstract; be strict in what you accept and promise as little as possible;
do not use preconditions for user-input validation), P044 (Honor the Liskov Substitution
Principle; put a contract once in the base class; assertions only partially emulate DBC),
and P055 (Use loop and semantic invariants; design a contract whenever you design
software). Key claims: C00163 (specify each clause), C00164 (a breach is a bug),
C00165 (preconditions are not input validation), C00166 (lazy style: strict in / modest
out), C00167 (LSP substitutability), C00168 (contract once in the base class), C00171
(assertions partially emulate DBC), C00177 (loop invariants for boundary conditions).
Source is distillation-only; all wording is paraphrased.
