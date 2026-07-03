---
name: assumptions-hypotheses-and-mvp-experiments
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P012
  - P073
  - P085
  - P092
  - P093
  - P100
  - P107
  claims:
  - C00968
  - C00969
  - C00970
  - C00971
  - C00972
  - C01686
  - C01706
  - C01707
  - C01708
  - C01801
  - C01802
  - C01803
  - C01809
  - C01810
  - C01045
  - C01046
  evidence:
  - E00322
  - E00323
  - E00324
  - E00325
  - E00326
  - E00521
  - E00527
  - E00528
  - E00529
  - E00552
  - E00553
  - E00554
  - E00555
  - E00556
  - E00342
  - E00343
  source_anchors:
  - 37d2b8d97a65-c0008
  - 6124b61e4fbf-c0000
  - 6124b61e4fbf-c0001
  - 6124b61e4fbf-c0003
  - 37d2b8d97a65-c0011
  authored_from_digest: 84b971cb772e62204e9d32066a616546ecd54f722d618b7b56fe28ef0054c848
---

# Frame work as testable hypotheses and validate with the smallest MVP

## Purpose

Convert requirements, feature requests, and stakeholder opinions into explicitly declared
assumptions and testable hypotheses about outcomes, then validate the riskiest of them as cheaply
as possible before committing to a build. This skill scopes the minimum viable product as the
smallest release that achieves the desired outcome, chooses an experiment that reveals what people
actually do, and treats early disproof as valuable learning rather than failure. Every
recommendation names the assumption, the outcome it serves, and the trade-off the chosen experiment
carries.

## When to use

- The caller has requirements, a spec, or a feature list and wants it reframed as declared
  assumptions and testable hypotheses about outcomes (P093).
- The caller is about to invest in building and wants to validate the direction cheaply first, to
  decide whether to pursue, refine, or abandon it (P003).
- The caller is scoping an MVP or a "minimum" release and needs to define the smallest version that
  achieves the outcome rather than the cheapest thing to ship (P085).
- The caller is planning an experiment and wants help choosing a technique — a lightweight
  non-prototype test or a small build — that observes real behaviour in a realistic moment
  (P073, P092).
- The caller finds a validated solution too expensive or too large and wants to step back to the
  problem or slice the work into smaller deliverable increments (P100).
- Do not invoke when the caller wants the hypotheses turned into production code or UI/visual
  assets, or wants the go/no-go decision made for them — hand that to the owning product team and
  its leadership; for direct user contact and interview technique use
  `continuous-discovery-and-research`, and for choosing prototype fidelity and running usability
  tests use `prototyping-and-usability-testing`.

## Procedure

1. **Name the outcome and declare the assumptions (P093).** Refocus the conversation away from
   artifacts and requirements toward the specific customer or business outcome the work should move.
   List the beliefs that must hold for that outcome to be reached, and write each as an explicit
   assumption rather than a fixed requirement. Expressing beliefs this way removes much of the
   subjective, political argument from the decision. Trade-off: declaring assumptions makes
   uncertainty visible that stakeholders may have preferred to leave implicit.

2. **Restate each assumption as a testable hypothesis (P093, P003).** For each assumption, state
   what you believe, the outcome you expect if it is true, and the observable signal that would
   confirm or disprove it. This turns a design from an opinion to defend into a hypothesis you can
   validate with customer feedback before investing further.

3. **Rank by risk and label build-to-learn vs build-to-deliver (P003).** Order the hypotheses so
   the belief that would most damage the outcome if it were wrong is tested first. For each piece of
   work, make explicit whether it is built to learn (a disposable probe) or built to deliver value,
   because the two carry different expectations for rigour, quality, and reuse. Trade-off:
   front-loading the riskiest test can feel like delaying "real" progress, but it avoids sinking
   weeks into an unvalidated direction.

4. **Define what you want to learn before designing the test (P092).** Do not rush into an
   experiment. First state precisely what you are trying to learn, then plan to collect data about
   what people actually do in a specific context — not what they say they do in general. Design the
   test to simulate the minimal right moment that gives a participant a genuine chance to behave in
   line with the assumption, or not, so you can iterate quickly.

5. **Scope the MVP as the smallest release that achieves the outcome (P085, P003).** Define the
   minimum viable product as the smallest release that achieves its desired outcome — not the
   crappiest thing you could ship — and treat "minimum" as subjective to the customers and users:
   ask what is minimal to *them*, rather than letting the highest-paid person's opinion decide.
   Remember the MVP need not be code; sketches, prototypes, copy, or visual design can all serve as
   the probe inside a build-measure-learn loop, and it remains a disposable learning tool.
   Trade-off: a smaller MVP retires the target risk sooner but deliberately leaves other questions
   unanswered — name which ones.

6. **Prefer lightweight, non-prototype experiments when they can retire the risk (P073).** To test
   demand and value without building the product, reach for techniques such as: an email test
   (measuring open, click-through, and completion rates); ad copy (to see which language resonates
   and how much click interest exists); a landing-page facade with a single clear call-to-action
   (each completed action counts as validation); or a "button to nowhere" (a click signals desire,
   after which you explain and capture feedback). Trade-off: these measure expressed interest at one
   moment, not sustained use or technical feasibility — choose the technique whose signal genuinely
   matches the assumption under test (P092).

7. **Run the build-measure-learn loop and treat early disproof as good news (P003, P012).** Run the
   experiment, read the outcome against the signal you defined, and let it tell you whether to
   pursue, refine, or abandon the direction. Learning you were wrong after a couple of days is
   excellent news compared with discovering it after weeks of building, so celebrate the learning
   rather than fear being wrong — failing to learn is often the bigger failure. Work fast and
   informally in discovery (prototypes in hours, code prototypes in days) and expect most ideas to
   fail or need adjustment. Trade-off: speed and informality trade polish and predictability for
   faster learning.

8. **If the solution is too expensive or too big, step back or slice it (P100).** When a validated
   solution turns out too expensive, step back to the problem and look for a cheaper alternative.
   When it is affordable but large, still break it into small, deliverable "cupcakes" with small
   plans — not a big frontend-then-backend sequence — so you can taste, measure, and learn sooner.
   Trade-off: thin slices deliver learning and value earlier but demand more integration discipline
   than one large release.

9. **Fold the loop into the team's cadence (P107).** Where the team works in Scrum, use its events
   as mileposts so the whole team works on the same thing at once: write user stories as end-user
   benefits, actively groom the prioritized backlog as the primary tool for staying agile, and run
   end-of-sprint retrospectives to iterate the process as much as the product. Trade-off: aligning
   experiments to sprint boundaries adds shared focus and rhythm but can constrain a test that would
   be better run on its own timing.

## Inputs

- The product decision, idea, spec, or feature request under review.
- The customer or business outcome it is meant to serve.
- Constraints: the users/customers involved, the appetite or timeline, cost sensitivity, and what
  is already known versus merely assumed.
- The team's working cadence (e.g., Scrum) if experiments must fit an existing process.

## Output

A structured hypothesis-and-experiment plan that:

- names the outcome at stake and restates the key beliefs as declared assumptions and testable
  hypotheses;
- ranks them by risk and labels each as build-to-learn or build-to-deliver;
- defines the MVP as the smallest release that achieves the outcome, in terms meaningful to
  customers;
- recommends the cheapest experiment that observes real behaviour, stating explicitly what it will
  and will not prove;
- ends with a next step tied to the caller's outcome and appetite, together with the trade-off that
  step carries.

The shape follows the advisor's modes: a findings list keyed to the principles above in *review*, a
single recommendation in *advise*, and a side-by-side of experiment options in *compare*.

## References

- [`references/product-principles-index.md`](../../references/product-principles-index.md) — full
  statements for the principles this skill applies (P003, P012, P073, P085, P092, P093, P100, P107)
  and their claim/evidence trail.
- Related skills for hand-off:
  [`continuous-discovery-and-research`](../continuous-discovery-and-research/SKILL.md) for direct
  user contact and interviewing, and
  [`prototyping-and-usability-testing`](../prototyping-and-usability-testing/SKILL.md) for choosing
  prototype fidelity and running usability tests.

## Provenance

Distilled and paraphrased from this package's principles P003, P012, P073, P085, P092, P093, P100,
and P107 (all distillation-only sources — no verbatim text), which synthesise build-measure-learn
and MVP-experiment guidance from works including *Escaping the Build Trap* and *Lean UX*. Full
principle statements and their claim/evidence trail live in
`references/product-principles-index.md` and the package provenance ledger.
