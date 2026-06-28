---
name: law-of-demeter-coupling-review
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P001
  - P062
  - P063
  - P072
  claims:
  - C00205
  - C00206
  - C00203
  - C00204
  - C00207
  - C00054
  - C00068
  - C00065
  source_anchors: []
  authored_from_digest: 71e9262b3b4d4f759dfa581060588946145657533de3650c2673432f7c7039ab
---

## Purpose

Review a module, class, or interaction path for excessive coupling and Law of Demeter
violations, then recommend the minimum decoupling that removes the violation without
incurring more wrapper overhead than the benefit is worth. Grounds the orthogonality
goal (changes in one component do not ripple into unrelated ones) in a concrete,
repeatable inspection.

## When to use

- A design or code review surfaces call chains of the form `a.getB().getC().doWork()`,
  where a caller reaches *through* one object to drive a third.
- A small change in one module forces edits in modules that look unrelated — a symptom of
  a high coupling / low orthogonality design (P001).
- A class has a large response set (it can invoke a wide fan-out of other classes'
  methods) and is becoming error-prone or frightening to change.
- Before integration, to confirm modules talk only to their immediate collaborators so
  integration defects stay localised.
- Unit-test setup for a module requires linking or instantiating large portions of the
  rest of the system — the unit-test-difficulty signal described in P062 (C00068).

Do **not** mechanically eliminate every delegation: the Law of Demeter has a real cost
(see Procedure step 5). Apply it where coupling risk dominates, not as an absolute.

## Procedure

1. **Map the collaborators.** For the unit under review, list the objects it is *directly*
   handed (parameters, fields it owns, objects it creates). These are its legitimate
   immediate collaborators under the Law of Demeter. Under P015 / C00371, only these
   objects' methods may be called directly; structural knowledge of their internals must
   not leak through the unit's contract.

2. **Flag reach-through chains.** Find any expression that obtains an object from a
   collaborator and then invokes a method on *that* returned object (`a.getB().doWork()`).
   Each extra link is a dependency on a class the unit was never given — a Law of Demeter
   violation. Per C00204, traversing object hierarchies directly produces a combinatorial
   growth of dependency relationships, with concrete symptoms: a unit-test link command
   longer than the test itself, simple changes propagating through unrelated modules, and
   developers becoming afraid to touch the code.

3. **Score the coupling.** Estimate the unit's response set — the distinct set of methods
   on other classes it can ultimately trigger. Per C00206, classes with larger response sets
   are empirically more error-prone; a large response set is therefore the review's primary
   risk signal.

4. **Check for global data and structural near-duplicates.** Per P063 / C00065, each
   reference to a global (including Singletons used as globals) couples the unit to every
   other component sharing that global and makes the code fragile under threading and other
   change. Per C00066, near-identical functions also signal a structural problem; flag both
   for removal or refactoring (e.g., via the Strategy pattern).

5. **Propose the decoupling.** For each violation, prefer one of:
   - **Tell, don't ask** — give the immediate collaborator a method that performs the work
     so the caller asks it to act rather than fetching a subobject and acting on it
     (C00203: ask an object to perform a service on your behalf).
   - **Delegating wrapper** — add a method on the immediate collaborator that forwards to
     its own subcontractor, hiding the third object from the caller.
   - **Restructure ownership** — if the chain reveals a misplaced responsibility, move the
     behaviour to the object that holds the data.
   - **Eliminate global** — pass required context explicitly as a parameter rather than
     reading a global or Singleton.

6. **Weigh the cost before mandating the fix.** Per P072 / C00207, applying the Law of
   Demeter requires writing many forwarding wrapper methods, which carries real runtime and
   space overhead. Recommend the change only where the reduction in coupling risk outweighs
   that overhead; record the trade-off explicitly. Deliberately reversing the rule to allow
   tighter coupling is acceptable only when the coupling is well known and the performance
   benefit is measurable and acceptable.

7. **Re-check orthogonality.** Confirm the proposed design keeps components self-contained
   with a single well-defined purpose (P001 / C00054: eliminate effects between unrelated
   things; high cohesion). Apply the orthogonality test from P001: a single requirement
   change should ideally require a change in only one module. If the decoupling fixes do not
   satisfy this test, more restructuring is needed. Per P062 / C00068, re-running the
   unit-test-build after the fix is a practical probe: if the test still drags in most of
   the system, the module is still poorly decoupled.

## Inputs

- The code, class, or interaction diagram under review.
- The unit's declared collaborators and dependency surface (imports, constructor arguments,
  fields).
- Any prior change-impact evidence (a recent change that rippled unexpectedly into unrelated
  modules).

## Output

- A list of flagged reach-through chains with file and line locations.
- A coupling assessment (response-set size, ripple risk) per reviewed unit.
- A concrete decoupling recommendation per violation, **each annotated with its wrapper
  cost** so the caller can decide where the rule pays for itself.
- Global-data and near-duplicate flags with recommended replacements.

## References

- `references/refactoring-checklist.md` — when a coupling fix is also a refactoring trigger.
- `references/pragmatic-tips-70-cheatsheet.md` — tips covering minimize coupling between
  modules and eliminate effects between unrelated things.

## Provenance

Derived from P015 (Law of Demeter and shy code, claims C00205/C00206/C00203/C00204/C00371),
P001 (orthogonality and single-responsibility, claims C00054/C00061), P062 (unit-test
difficulty as decoupling probe, claim C00068), P063 (global data and near-duplicate
functions increase coupling, claims C00065/C00066), and P072 (balance Law of Demeter against
wrapper overhead, claim C00207). Source is distillation-only; all wording is paraphrased.
