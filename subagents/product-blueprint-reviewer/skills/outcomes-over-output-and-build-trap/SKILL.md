---
name: outcomes-over-output-and-build-trap
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P006
  - P007
  - P010
  - P020
  - P021
  - P022
  - P023
  - P024
  - P025
  - P026
  - P027
  - P034
  - P035
  - P036
  - P037
  - P038
  - P039
  - P040
  - P041
  - P042
  - P043
  - P044
  - P045
  - P046
  - P047
  - P048
  - P062
  - P063
  - P064
  - P065
  - P066
  - P067
  - P068
  - P069
  - P070
  - P071
  - P072
  - P073
  - P074
  - P075
  - P076
  - P077
  - P078
  - P079
  - P080
  - P081
  - P082
  - P083
  - P084
  - P085
  - P086
  - P087
  - P088
  - P089
  - P103
  - P105
  - P106
  - P107
  - P108
  - P109
  - P110
  - P111
  - P112
  - P113
  - P114
  - P115
  - P116
  - P117
  - P118
  - P119
  - P120
  - P121
  - P179
  - P180
  - P181
  - P182
  - P183
  - P184
  - P185
  - P186
  - P187
  - P188
  - P189
  - P190
  - P191
  claims:
  - C00240
  - C00241
  - C00242
  - C00243
  - C00244
  - C00245
  - C00246
  - C00249
  - C00250
  - C00251
  - C00152
  - C00153
  - C00159
  - C00160
  - C00183
  - C00381
  - C00382
  - C00385
  - C00341
  - C00342
  - C00343
  - C00344
  - C00345
  - C00347
  - C00348
  - C00349
  - C00230
  - C00231
  source_anchors:
  - 8707406d317e-c0000
  - 8707406d317e-c0001
  - 2a049107e960-c0000
  - 2a049107e960-c0001
  authored_from_digest: 2ed336df763fb2183534d2b204952e9d425c611b3e1a3c13dfabc43c3fa71c87
---

# Outcomes over output — escaping the build trap

## Purpose

Reviews a product blueprint for build-trap output-thinking: roadmaps, initiatives, and success
criteria framed around what ships rather than the customer or business outcome reached. Turns
each output-shaped item back into an outcome plus the assumption it tests, checks whether the
surrounding organization and its strategy are structured to support that reframing, and holds
"done" to reaching the outcome rather than shipping. Grounded in Escaping the Build Trap
(Perri, 2018) and the accompanying product-strategy and lean-startup source material in this
package.

## When to use

- The blueprint's scope section reads as a feature list, backlog, or roadmap of things to ship
  rather than outcomes to reach.
- The reviewer needs to judge whether the sponsoring product organization looks product-led
  (versus sales-, technology-, or visionary-led, or a feature-factory / project-management shop).
- The blueprint's strategy section needs checking for whether it deploys as intents and problems
  the team can adapt to, or as a committed, detailed feature plan handed down.
- The MVP, release, or success-metric language needs checking for whether "done" means reaching a
  pre-set outcome or simply shipping, and whether the stated metrics are true metrics or vanity /
  output counts.
- Use together with, not instead of, `blueprint-altitude-and-neutrality` (implementation
  neutrality) and `lean-startup-hypothesis-discipline` (hypothesis mechanics): this skill owns the
  outcome-versus-output judgment, not wording neutrality or probe design.

## Procedure

Work the five checks below in the order given — later checks (validated bets, metrics and
funding) presuppose the outcome reframing done in check 1. In `advise` or `compare` mode, apply
only the check(s) relevant to the caller's specific decision rather than the full sequence. Close
every finding the way the package's quality bar requires: name the outcome at stake, the
assumption behind it, and the trade-off of the fix — never flag output-thinking without offering
the outcome-shaped replacement.

### 1. Reframe roadmap items as outcomes, not outputs

Check every feature, epic, or roadmap line for the customer or business outcome it is meant to
move and the assumption it rests on (P034, P067, P068). Red flags: success is measured by what
ships — features, releases, velocity — rather than value delivered (P034, P080); a listed
"feature" is really a mis-stated problem, where the real underlying need was never asked (P081);
incentives or scorecards reward shipping counts rather than outcomes and learning (P020);
objectives are phrased as deliverables or dates ("ship v2 by Q3") instead of outcomes (P185).
Recommend rewriting each item as an outcome goal plus its testable assumption, tracing it back to
a structured problem statement rather than the requested solution (P038, P081, P067).

### 2. Check the organization is product-led, not a feature factory

Check the blueprint's framing (and any stated context about how the team operates) against the
signs of a product-led organization: ideas originate from the team and connect why to what, the
organization is able to kill ideas, goals are outcome-oriented, and product management spends more
time on problems than solutions (P021, P006). Red flags: product management reduced to
order-taking — implementing every request without pushing back on the underlying problem (P026);
strategy led by sales, a single visionary, or the technology rather than by outcomes (P036); a
product manager cast as sole owner or mini-CEO instead of leading by influence while the team owns
the "what" (P025); the work organized around projects or technical components instead of products
and value streams (P024, P003); a product manager acting as an order-taker instead of investigating
the known unknowns (P069) and leading experiments that connect research, market data, and results
into direction (P108), or terminating bad ideas (P089). Recommend naming the specific pattern and
its outcome-oriented fix — reframe a committed request as the problem it stands in for (P026),
reorganize scope around the product or value stream (P003, P024) — and flag organization-level
causes (reward structure, leadership composition) as outside the blueprint's content but relevant
to why the build trap persists (P006), rather than trying to compensate for them in the blueprint
text.

### 3. Check strategy is deployed as outcomes and intents, not a feature list

Check for a visible chain from vision to a few concrete strategic intents to product initiatives
(the customer problems to solve) to options (the bets teams explore), each stated as an outcome or
problem rather than a prescribed solution, with goals sized to the time scale of whoever must act
on them (P042, P043, P037). Red flags: the strategy reads as a fixed, detailed plan rather than a
deployable decision framework — exactly what creates the Knowledge, Alignment, and Effects gaps
(P066, P022); teams receive committed feature requests instead of aligned intent, which cuts off
their ability to course-correct (P023); the roadmap is presented as a fixed-date Gantt chart
instead of a living explanation of stage (P086); there is no North Star tying the problem, the
proposed solution, the success factors, and the outcome together — only an action plan (P047).
Recommend restating the strategy across the four levels (vision, strategic intent, initiatives,
options) and checking each initiative traces to a stated intent (P042, P043); replace a
Gantt-style roadmap with staged terminology (Experiment, Alpha, Beta, Generally Available)
communicated by audience (P086); flag a missing strategy-execution communication cadence as an
organizational gap to raise, not a wording fix (P048, P182).

### 4. Check validated bets and the real definition of "done"

Check that every initiative or option is framed as a testable belief tied to a quantified outcome,
run through the Product Kata's repeating direction, current-state, obstacle, experiment, and
learning loop and its six-question checklist (P042, P044, P070); that the MVP is defined as the
minimum effort needed to learn rather than the first shippable release (P078); and that "done"
means the feature reached its pre-set success criteria, not that it shipped (P085). Red flags: a
vision or feature set committed without validation, including trusting an external roadmap without
evidence (P103); a solution adopted before the problem is understood or before a cheap experiment —
a concierge test, or a concept test that requires a real commitment of money, time, or effort — has
tested it (P073, P082, P007); no rollback or pre-set success criteria attached to the release
(P085); a nearly-complete project kept running even though it no longer serves the strategy
(P183); experimentation applied at the wrong phase — understanding direction, problem exploration,
solution exploration, and optimization each need a different tool, and a known problem with a known
solution needs only careful shipping and measurement, not a heavy experiment (P079, P188).
Recommend requiring every MVP or option to state its hypothesis, its cheapest validating
experiment, and its pre-set success criteria before build (P070, P082, P085); where the blueprint
already assumes a solution, ask for the underlying problem statement and the riskiest-assumption
test first (P007, P073); treat an unwillingness to kill a failing or off-strategy initiative as a
red flag in itself (P183).

### 5. Check metrics are true metrics, and funding matches an outcome cadence

Check that stated success metrics tie to business or customer outcomes — retention, activation,
problem resolution — rather than vanity counts that only ever grow (signups, downloads) or output
counts (features shipped, story points) (P080), and that they come in a balanced, leading/lagging
pair rather than one gameable number (P117, P116). Check whether funding is framed as continuous,
staged investment tied to reaching the next stage, rather than a fixed annual allocation that must
be spent or lost (P088, P113). Red flags: the only stated metric is a count of features, releases,
or story points (P080); a single metric with no leading counterpart to check it against (P117);
the funding or staffing model assumes an annual cycle regardless of stage progress, or treats
innovation as an isolated, under-resourced side project instead of continuously funded work (P088,
P114). Recommend replacing vanity or output metrics with a paired true-metric set — for example
Pirate Metrics for the funnel, HEART for a feature or product — time-boxed against a baseline
(P116, P118); recommend staged, bet-sized funding tied to reaching the next stage instead of a
fixed yearly figure (P088, P113).

Close by restating the trade-off of every recommended fix (more validation work now versus less
wasted build later; less roadmap certainty versus more course-correction room), and hand the
actual rewrite and funding or organizational decisions back to the product team and its
leadership — this skill reviews and advises, it does not author the blueprint's content or make
the team's call (P021). Escaping the build trap in full is a whole-organization change led from
the top, not something this review substitutes for (P077).

## Inputs

- The blueprint section(s) under review — roadmap or feature list, strategy statement, MVP or
  release criteria, success metrics, funding or staffing model — or the research synthesis being
  converted into a blueprint.
- Any stated organizational context (how product management operates, incentive structure,
  funding cadence), if available; sharpens the product-led diagnostic in check 2 but is not
  required to run checks 1, 3, 4, or 5.
- The caller's outcome and MVP appetite (profile `inputs.required`), to weight which red flags
  matter most for this review rather than surfacing all five checks with equal weight.

## Output

A findings list, one entry per red flag found, each entry naming: the outcome at stake, the
build-trap pattern found and its principle ID(s), a concrete outcome-shaped remediation, and the
trade-off the remediation carries. In `review` mode this feeds the larger blueprint critique; in
`advise` or `compare` mode it grounds one MVP-scoping, prioritization, or roadmap-framing decision
in outcome terms rather than a feature comparison.

## References

- `../../references/blueprint-principles-index.md` — full principle index and citations for this
  and its sibling skills.

## Provenance

Grounded primarily in Escaping the Build Trap (Perri, 2018), via the claims and principles derived
from `sources/markdown/escaping-the-build-t-8988bab5.md`, with supporting material from the
lean-startup source (`sources/markdown/lean-startup-katila-2a049107.md`) and the package's own
blueprint-contract source. All cited sources are `distillation-only`, so this body paraphrases
throughout and never quotes verbatim. See the frontmatter `provenance` block above for the exact
principle, claim, and source-anchor IDs this skill is derived from.
