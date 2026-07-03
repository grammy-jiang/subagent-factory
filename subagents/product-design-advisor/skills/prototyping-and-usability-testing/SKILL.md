---
name: prototyping-and-usability-testing
kind: skill
status: ready
provenance:
  principles:
  - P030
  - P031
  - P033
  - P036
  - P090
  - P099
  - P053
  claims:
  - C01811
  - C01812
  - C01813
  - C01814
  - C01815
  - C01816
  - C01817
  - C01818
  - C01819
  - C01820
  - C00241
  - C00242
  - C00243
  - C00244
  - C00247
  - C00301
  evidence:
  - E00557
  - E00558
  - E00559
  - E00560
  - E00561
  - E00562
  - E00563
  - E00564
  - E00565
  - E00566
  - E00097
  - E00098
  - E00099
  - E00100
  - E00101
  - E00128
  source_anchors:
  - 6124b61e4fbf-c0004
  - 4c877a0e12f8-c0006
  - 4c877a0e12f8-c0007
  - 4c877a0e12f8-c0008
  authored_from_digest: 8f9c8b77b2ef22b68a3dd74e7546d12e474ccdfe31d576b4aa83f340fc21757b
---

# Prototype at the right fidelity and test with real users

## Purpose

Guide teams to retire product risk with prototypes and usability tests *before* committing
to build, instead of discovering the flaws only after a solution ships. This skill matches
prototype fidelity to the risk being retired, treats a tested high-fidelity prototype as the
product spec, and grounds every judgement in watching real users pursue a real goal. It
advises, reviews, and compares options; it does not produce the visual/UI design or the
production build.

## When to use

- The caller is planning how to prototype an idea and wants the fidelity chosen to retire the
  biggest risk as cheaply as possible.
- A spec, prototype, or "minimal product" definition needs reviewing for big-design-up-front,
  paper-spec comfort, or scope creep before the team starts building.
- The caller is designing or critiquing a usability test — who to recruit, how to run the
  session, and what to observe.
- The caller is weighing prototype fidelities or test formats (for example, in-person vs.
  remote) for the same goal and wants the trade-offs contrasted.
- Do not invoke when the caller wants the finished UI/visual design, production code, or a
  prototyping tool/vendor selected — those are out of scope; hand them to the owning product
  and engineering team.

## Procedure

Work through the steps in order. Each step names the principle(s) it rests on and states the
trade-off the caller must accept, because every practice here buys one thing at the cost of
another.

1. **Validate before you build, not after (P031).** Resolve feasibility and value risk with a
   prototype and a test *before* design and implementation begin; the fatal flaw of a
   build-first (Waterfall) sequence is that validation arrives too late to act on cheaply. When
   the team chooses to defer a change to a later release, weigh the follow-on-release cost of
   that deferral. **Trade-off:** front-loading prototyping and testing spends time and effort
   before any code is written, but it buys down the risk of expensive late rework — and treat
   any up-front schedule as only roughly reliable, since its predictability is illusory except
   on very small projects (P031).

2. **Choose prototype fidelity by the trade-offs of each level (P030).** Pick the *lowest*
   fidelity that still retires the risk you framed in step 1, using what each level gives and
   costs:
   - **Paper** — fast and cheap, but conveys only high-level flow; well suited to touch
     interactions.
   - **Clickable wireframes** — give real click/tap insight into workflow and findability, but
     read to users as unfinished.
   - **Mid- and high-fidelity** — near-final visuals and interactions, but limited versus a
     native build and costly to keep in sync as the design changes.
   - **Coded prototypes** — the highest realism and, in live-data form, real analytics and A/B
     testing, but slow to build and tempting to over-perfect.

   Trial several prototyping tools rather than committing to one, since no list of tools is
   comprehensive. **Trade-off:** higher fidelity buys more realistic feedback and sharper
   workflow/findability insight at the cost of build time, sync burden, and the temptation to
   polish instead of learn (P030).

3. **Make the tested high-fidelity prototype the spec — not a paper document (P036).** Once a
   high-fidelity prototype has been tested, use *it* as the product spec rather than a written
   paper spec, because paper specs are slow to produce, go unread, and give false comfort. A
   good spec covers the full user experience, serves everyone who consumes it, keeps one master
   representation, prototypes everything, simulates the backend, and is supplemented with the
   details a prototype cannot show. **Trade-off:** a prototype-as-spec communicates the real
   experience far better than prose, but you must still add written supplements for what the
   prototype cannot express (P036).

4. **Define the minimal product as a validated high-fidelity prototype, then stop cutting
   (P033).** Define the minimal product up front as a high-fidelity prototype with engineers'
   estimates, validate it with real users, and then do *not* cut further. If a feature runs
   long, slip the schedule rather than drop scope; stop adding requirements once the work is
   underway; and deliver the validated spec as one whole product. **Trade-off:** holding scope
   fixed and slipping the date protects the validated product's integrity but sacrifices date
   certainty — name that trade explicitly so the caller can weigh it against their appetite
   (P033).

5. **Take the software to real users and watch them pursue a real goal — not show-and-tell
   (P099).** Because the people building the product are usually not its users, put the working
   software (or prototype) in front of *real* users and test it, rather than merely
   demonstrating it to them. Watch users accomplish a *real* goal on a regular cadence: let no
   more than roughly a couple of weeks pass without observing a genuine user. Not everyone need
   attend, but watching builds empathy, so those who do watch should retell what they saw to the
   rest of the team. **Trade-off:** a steady testing cadence costs recurring time, but skipping
   it lets the builders' assumptions stand in for real user behaviour (P099).

6. **Administer the session for honest use, not performance (P053).** Run each session so you
   get truthful behaviour: get the user to the prototype quickly; tell them you are testing the
   prototype, not them; keep them in *use-mode* rather than critique-mode; stay quiet and avoid
   leading questions; record each task's result using the three task-outcome categories; parrot
   the user's words back to check understanding; and look for where the software's model
   conflicts with the user's mental model. **Trade-off:** staying quiet and unleading yields
   truer signal but demands discipline — the urge to explain or rescue the user corrupts the
   result (P053).

7. **Keep test logistics light (P090).** Run tests wherever is convenient; a formal usability
   lab is not required. Have the product manager attend every test, staffed simply with one
   administrator and one note-taker, and treat remote testing as a *supplement* to in-person
   observation, not a substitute for it. A good product manager can test their own product
   objectively, so PM attendance is the default rather than a conflict. **Trade-off:** informal,
   PM-run testing is cheap and builds team empathy, but leans on the team's discipline to stay
   objective, and remote-only testing trades convenience for lost observational richness (P090).

## Inputs

- The artifact or decision under review: a prototype or its plan, a spec, a proposed "minimal
  product," or a usability-test plan.
- The outcome the work should serve and the specific assumption or feasibility/value risk to
  retire.
- Constraints: which real users are reachable, the appetite or timeline, the current prototype
  fidelity, and what is already known versus still assumed.

## Output

A prototyping / usability-testing recommendation or critique that:

- names the risk or assumption being retired and the outcome it serves;
- states the fidelity (or test format) chosen and *why it is the lowest that retires that risk*;
- makes each recommendation's trade-off explicit — what is gained and what is sacrificed;
- flags the anti-patterns it finds (big design up front, paper-spec comfort, scope creep past
  the validated minimal product, show-and-tell instead of real-user testing, leading the user);
  and
- ends with a concrete next step tied to the caller's appetite.

In **review** mode this is a findings list with remediations; in **compare** mode it is a
side-by-side of the fidelity/format options ending in an appetite-weighted pick. The final
build, the visual/UI design, and the decision itself stay with the owning product and
engineering team.

## References

- `references/product-principles-index.md` — index of the product-design principles cited here
  (P030, P031, P033, P036, P053, P090, P099) and the sources they trace to.

## Provenance

Distilled and paraphrased from the product-design principles cited in the frontmatter (P030,
P031, P033, P036, P053, P090, P099), which draw on Marty Cagan, *Inspired* (2017), and Jeff
Gothelf & Josh Seiden, *Lean UX* (2016). Both are distillation-only sources: paraphrased here
with no verbatim text.
