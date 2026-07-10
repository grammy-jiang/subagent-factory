---
name: legacy-code-change-algorithm
kind: skill
status: ready
provenance:
  principles:
  - P130
  - P047
  - P048
  - P073
  - P132
  - P133
  - P105
  claims:
  - C00047
  - C00001
  - C00002
  - C00003
  - C00004
  - C00027
  - C00028
  - C00029
  - C00031
  - C00044
  source_anchors:
  - 1d83dc6f489c-c0002
  - 1d83dc6f489c-c0001
  authored_from_digest: 9a726b8c1ae98a38ef7e7ebed3b8e917d92244687b72400676c5dcdce9c7db68
---

# Legacy Code Change Algorithm

## Purpose

Drive every change to an unfamiliar, untested legacy code base through one repeatable
five-step sequence, so that behaviour is sensed and protected before it is modified rather
than changed blind (P130). This is the spine of the advisor: the other skills are the
detailed moves invoked from individual steps. It resolves the Legacy Code Dilemma — you
should have tests to change code, but you must change code to get tests — by breaking
dependencies conservatively to get the first tests in place (P073).

## When to use

- Starting work on a feature, bug fix, or refactor in legacy code, especially code you do
  not know well and that lacks tests (P047). Dependency is the central obstacle to getting
  such code under test (P105).

Do **not** apply to greenfield code already being developed test-first — there is no
existing untested behaviour to protect, so the algorithm's purpose does not arise.

## Procedure

Run the five steps in order (P130):

1. **Identify change points.** Determine exactly where in the code the behaviour must
   change to accomplish the feature or fix.
2. **Find test points.** Determine where tests can be written to sense the effects of that
   change — i.e. where the change's effects can be observed. Use effect reasoning when the
   change ripples across several methods/classes (see `effect-reasoning`).
3. **Break dependencies.** Get the code into a test harness by breaking only the
   dependencies that block instantiation or observation — for sensing or for separation
   (see `sensing-and-separation`, `seam-model`). This is the deliberate exception to
   test-first: make these incisions conservatively, doing no extra cleanup (P134-adjacent
   discipline; primary rule P130).
4. **Write tests.** Write characterization tests that pin the current actual behaviour at
   the test points before changing anything (see `characterization-testing`).
5. **Make changes and refactor.** With the safety net in place, make the change and
   refactor, taking small steps — Cover and Modify, not Edit and Pray (P048).

If at step 3 the surrounding code cannot cheaply be brought under test, add the new
behaviour with a sprout/wrap technique instead of editing untested code inline (see
`sprout-and-wrap`), then resume.

## Framing the risk

Before a risky change, answer three questions: what changes must be made, how will we know
we made them correctly, and how will we know we did not break anything (P132). Steps 4–5
answer the second and third with tests. Make each programming episode deliver functional
value while bringing more of the system under test, so tested areas steadily grow (P133).

## Inputs

- The planned change (feature / fix / refactor) and the code unit involved.
- Known obstacles to instantiating or observing the code under test.

## Output

An ordered change plan: the identified change point(s), the chosen test point(s), the
dependencies to break and how, the characterization tests to write, and the change/refactor
to make last.

## References

- `sensing-and-separation`, `seam-model` — step 3 (break dependencies).
- `characterization-testing` — step 4 (write tests).
- `effect-reasoning` — step 2 (find test points).
- `sprout-and-wrap` — alternative when the area cannot cheaply be covered.

## Provenance

Derived from principle P130 (the five-step algorithm), with P047/P105 (legacy = untested
code, dependency the central obstacle), P048 (Cover and Modify), P073 (Legacy Code Dilemma),
P132 (three risk questions), and P133 (grow tested area). Source is distillation-only;
paraphrased, not quoted.
