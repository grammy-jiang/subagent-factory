---
name: getting-to-green-strategies
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P007
  - P019
  claims:
  - C00042
  - C00043
  - C00044
  - C00045
  - C00046
  - C00160
  - C00161
  - C00162
  - C00163
  - C00157
  - C00158
  - C00159
  source_anchors:
  - e619fe9a0394-c0001
  - e619fe9a0394-c0006
  authored_from_digest: 4bcd5088a229a7de9a373e087d04576f23d0d64f0167905cfdc1f3f825aac97d
---

# Getting-to-green strategies

## Purpose

Guide the developer in choosing and applying one of three distinct strategies for moving
from a failing test to a passing bar: Obvious Implementation, Fake It, or Triangulation.
The choice is deliberate and depends on confidence and evidence — not instinct. This skill
also covers turning a design objection into a concrete failing test instead of debating it
in the abstract. (P005, P007)

## When to use

- A failing test exists and the developer is deciding how to make it pass.
- The developer is unsure whether to write the real implementation now, return a constant
 and generalise later, or wait for a second example before abstracting.
- A reviewer or developer dislikes something about a design but cannot tie the concern to
 any specific observable behaviour.
- A developer has just hit an unexpected red bar while using Obvious Implementation and
 needs to recover.

Do not apply when the bar is already green — strategy selection belongs to the make-it-run
step only. Once every test passes, hand off to the refactoring step.

## Procedure

### Step 1 — Confirm a failing test is in place

Before choosing any strategy, verify that a single small failing test exists and that the
failure is for the expected reason. If no failing test exists, stop and direct the developer
to write one first (see **red-green-refactor-cycle**).

### Step 2 — Choose a strategy

Use the decision below. Apply the chosen strategy in Step 3; do not blend strategies in a
single pass. 

#### Obvious Implementation

**Choose when:** the correct code is clear in your mind and you are confident it will make
the test pass without surprises.

Type in the real implementation directly. Run all tests immediately. If the bar turns green,
you are done with this step. If it turns red unexpectedly — any failure you did not
anticipate — do not debug the implementation; back up to Fake It (Step 2, branch below) and
work in smaller steps until confidence returns. 

#### Fake It — return a constant, then generalise

**Choose when:** the real implementation is not yet clear, or a previous Obvious
Implementation attempt produced an unexpected red bar.

1. Return the simplest hardcoded value that makes the current failing test pass — often a
 literal constant.
2. Run all tests; confirm the bar is green.
3. Identify any duplication between the constant in the test assertion and the constant in
 the production code. That duplication is the signal to generalise.
4. Replace each constant with a variable or expression, one substitution at a time, running
 all tests after each change. Stop when no duplication remains.

If another test is needed to justify the next generalisation step, add it to the to-do list
and write it in the next cycle rather than generalising speculatively now. 

#### Triangulation — drive an abstraction from two or more examples

**Choose when:** you are uncertain whether the generalisation is correct and want the test
suite itself to force the abstraction rather than relying on your judgment.

1. Keep the current test passing (which may mean keeping a fake return value for now).
2. Write a second test that exercises the same behaviour with a different input value and
 asserts a different expected output.
3. Run all tests; both should now fail (or the second should fail while the first passes on
 the fake).
4. Now generalise the implementation — replace the hardcoded value with the general
 expression — so that both tests pass.
5. With two concrete examples in the test suite, the abstraction is triangulated: the
 implementation must be genuinely general to satisfy both. 

Reserve Triangulation for cases where uncertainty is real. If the general solution is
already obvious, Obvious Implementation is faster and Triangulation adds ceremony for no
benefit.

### Step 3 — Apply the chosen strategy and reach green

Execute the selected strategy. The goal of this step is only to get the bar green as fast as
possible — correctness of design comes in the refactoring step that follows. A temporarily
ugly or duplicated solution is acceptable here, provided duplication is removed promptly
afterwards. Do not clean up during this step.

### Step 4 — Handle an unexpected red bar

If any test that was previously passing now fails, stop immediately:

1. Do not continue implementing.
2. Undo the last change (or revert to the last green state).
3. Switch to Fake It if you were using Obvious Implementation.
4. Work in smaller increments until every test passes again.

An unexpected failure is a signal that the step was too large, not a reason to debug
production code while the bar is red. 

### Step 5 — Turn a design objection into a test (optional)

When a reviewer or developer objects to something about the implementation — for example an
unwanted side effect, an unexpected return value, or a behaviour they find harmful — but
cannot identify a currently failing test that captures the concern:

1. Ask: what concrete behaviour would a test assert if the objection is valid?
2. Express the objection as a specific input and a specific expected (or forbidden) output.
3. Write that failing test and add it to the active failing test slot.
4. Return to Step 2 and choose a strategy to make it pass.

This converts an abstract design debate into a testable case. If no concrete assertion can
be formed, the objection may be about naming or formatting rather than behaviour, and is
outside the scope of the get-to-green step. (P008)

### Step 6 — Confirm green, then hand off

Once every test passes:

- Do not refactor during this step.
- Record any duplication noticed, and any follow-on tests or refactorings identified, on the
 to-do list (see **tdd-to-do-list**).
- Hand off to the refactoring step — see **get-to-green-then-refactor**.

## Inputs

- The current failing test (name, assertion, and expected value).
- The current production code or interface, or confirmation that none exists yet.
- The developer's stated confidence: whether the correct implementation is clear or not.
- Any design objection to be translated into a test (for Step 5).

## Output

One of:

- A strategy recommendation (Obvious Implementation / Fake It / Triangulation) with the
 rationale — which condition was met — and the concrete next action for that strategy.
- A recovery instruction when an unexpected red bar is encountered.
- A concrete failing test derived from a design objection, ready to add to the cycle.

Each output names the strategy applied, the step it belongs to (make-it-run), and why the
choice fits the developer's current confidence and the evidence available.

## References

- [red-green-refactor-cycle](../red-green-refactor-cycle/SKILL.md) — the enclosing cycle
 this skill operates within; confirms a failing test exists before strategy selection.
- [get-to-green-then-refactor](../get-to-green-then-refactor/SKILL.md) — the step that
 immediately follows: remove duplication after the bar is green.
- [tdd-to-do-list](../../references/tdd-to-do-list.md) — record follow-on tests and
 refactorings discovered during the get-to-green step so nothing is lost.

## Provenance

Derived from the choose-a-strategy principle **P005** (Fake It / Obvious Implementation /
Triangulation), the conservative-Triangulation principle **P007**, and the Fake-It principle
**P019** (claims **C00042**, **C00160**, **C00157**), grounded in Kent Beck, *Test-Driven
Development By Example* (Addison-Wesley, 2002) at chunk anchors `e619fe9a0394-c0001`
(the strategies and the Obvious-Implementation/Fake-It shift) and `e619fe9a0394-c0006`
(Triangulation demonstrated).
Distillation-only source: paraphrased throughout, no verbatim quotation.
