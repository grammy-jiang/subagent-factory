---
name: continuous-discovery-and-research
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P013
  - P018
  - P025
  - P029
  - P037
  - P043
  - P046
  - P061
  - P072
  - P083
  - P084
  claims:
  - C00003
  - C01342
  - C01343
  - C01344
  - C01345
  - C01346
  - C01375
  - C01376
  - C01377
  - C01752
  - C01753
  - C01754
  - C00725
  - C00734
  - C00958
  - C00959
  evidence:
  - E00001
  - E00437
  - E00438
  - E00439
  - E00440
  - E00441
  - E00447
  - E00448
  - E00449
  - E00537
  - E00538
  - E00539
  - E00227
  - E00228
  - E00320
  - E00321
  source_anchors:
  - 4c877a0e12f8-c0000
  - eaae3b395dea-c0009
  - eaae3b395dea-c0010
  - 6124b61e4fbf-c0002
  - 95f398b45f1f-c0011
  - 37d2b8d97a65-c0007
  authored_from_digest: 8673518b970d91a496dbadc0491e529832f4e15cac83adeaf74ab4490a702cd1
---

# Run continuous discovery with direct customer contact

## Purpose

Continuous discovery keeps the product team learning directly and regularly from real users, so decisions about what to build rest on observed behaviour and a clear outcome rather than opinion, market research, or a feature wish-list. This skill guides how to set up that contact, interview for what people actually do, structure and assess opportunities, and keep synthesizing — before and after launch. Use it to critique or plan a discovery approach; every recommendation should name the outcome at stake and the trade-off the choice carries.

## When to use

- The caller is deciding what to build and wants it grounded in real user needs and a business outcome, not intuition or market research.
- A team is about to build a feature or product but has not validated the underlying opportunity or talked to users directly.
- The caller is setting up or reviewing discovery mechanics — user interviews, personas/orgzonas, a charter user program, or synthesis habits.
- A startup or new product needs to figure out the right product before committing an engineering team and burning through funding.
- The caller wants a post-launch feedback and customer-intelligence loop critiqued or designed.
- Do not invoke when the caller instead needs prototype-fidelity or usability-test mechanics (use `prototyping-and-usability-testing`), MVP or experiment design (use `assumptions-hypotheses-and-mvp-experiments`), or outcome/strategy framing itself (use `product-strategy-and-outcomes`) — and remember this skill advises discovery; the team and its leadership still own the build and the decision.

## Procedure

Work these steps as a continuous loop, not a one-time gate. Order them to fit the caller's stage and outcome, and name the trade-off each choice carries.

1. **Insist on direct, personal contact with real users.** Have the product manager and discovery team attend every interview, site visit, and usability test themselves; second-hand summaries are no substitute, because hands-off research yields data, not empathy (P088, P084). If the organization forbids talking to users, treat that as a blocker to fix first — the principle is blunt that you either get the policy changed or leave (P088). Trade-off: firsthand contact costs the team's calendar time and feels slower than reading a report, but it builds the empathy every later product choice depends on.

2. **Assemble a small cross-functional discovery team (the "triad").** Keep it to two-to-four people led by a product owner, including someone who knows users and can prototype the UI and a senior engineer who knows the architecture; together they hunt for the intersection of valuable (to company and customers), usable, and feasible, coordinating with the wider development team, stakeholders, subject-matter experts, and users (P010). Trade-off: giving an engineer real business and user insight often produces the most innovative solutions, but a standing triad ties up senior people — keep it small, named for the three concerns rather than three head-count.

3. **In a startup or new product, run discovery first, and separate discovery from execution.** Before hiring a full engineering team, line up product management, interaction design, and prototyping and validate a high-fidelity prototype — figure out the right product before burning through seed funding (P083). Treat the work as two stages, discovery (find what to build) and execution (build it right), and once engineering starts, shift decisively into an execution mindset or the product manager becomes the source of churn (P087). Trade-off: discovery-first delays the visible act of "building," which can unsettle investors or execs, but it is far cheaper than staffing up to build the wrong thing.

4. **Interview for actual behaviour, not stated preference.** Be wary of what people say they want — showing lots of cool ideas makes them love everything, and stated preferences are only guesses; the real proof is whether they choose to use the product every day (P025). Avoid direct, factual, or generalized questions, because people report their ideal or perceived behaviour and construct coherent-but-untrue stories; instead ask for specific stories about recent, concrete instances, which memory reports far more reliably (P079). Trade-off: story-based interviewing is slower and takes more skill than a preference survey, but it trades cheap, misleading answers for evidence you can act on.

5. **Reach hard-to-reach customers creatively, and charter a user program for depth.** When customers are hard to reach, get creative — trace the real decision rule, use friends-of-friends, or enlist sales and account managers as research proxies — and in interviews back up from any proposed solution to ask "why," because asking the right questions is your job, not the customer's (P018). For sustained, deep insight, run a charter user program: recruit only from your true target market, aim for at least six live, happy reference customers, refuse prepayment, and cap it at about ten; if you cannot recruit them, treat that as a signal the problem may not matter (P037). Trade-off: proxies and friends-of-friends are easier to reach but less representative than true target users, so weight their input accordingly, and a charter program buys depth at the cost of breadth.

6. **Synthesize continuously with a one-page interview snapshot.** Because continuous interviewing has no natural stopping point and memory is unreliable, capture one visual snapshot per interview: a participant photo (with permission), a memorable verbatim quote that acts as a memory key, and quick facts about the customer's segment and behavioural traits (P055). Trade-off: a snapshot per interview is ongoing overhead, but it is far cheaper than trying to reconstruct dozens of conversations from memory later.

7. **Build lightweight personas (and orgzonas) as a team, and use them for the hard choices.** Assemble personas together from facts and honestly labeled assumptions, filtering out noise — do not just shout guesses; involve people with firsthand user experience and bring in any real research, and build "orgzonas" for organizational buyers (P013). Then use them to make product choices: co-create and prioritize personas early, focus each release on a single primary persona, and verify personas against real users while testing with a range of users (P043). Trade-off: personas built from assumption can mislead if you forget which parts are guessed — label the assumptions and verify them — but done honestly they create shared empathy that speeds later decisions.

8. **Do not let market research decide what to build.** No winning product is conceived from market research; winning products come from a deep understanding of user needs combined with what is only now newly possible. Use research to refine an existing product, not to conceive a new one (P046). Trade-off: market research looks authoritative and is easy to defend to stakeholders, but leaning on it to choose what to build trades genuine insight for false confidence.

9. **Structure discovery with an opportunity solution tree.** A useful way to organize the work is a tree with the desired outcome as the root, the opportunity space beneath it, the solution space below that, and assumption tests at the bottom; filter the opportunity space to only customer opportunities that can drive the business outcome, and break large opportunities into smaller ones solved one at a time, so small continuous solutions add up to the bigger opportunity (P040). Trade-off: mapping the tree is up-front effort and can feel bureaucratic, but it keeps every solution tied to an outcome and stops the team committing to the first idea.

10. **Frame opportunities cleanly; watch for the anti-patterns.** Reframe company-perspective statements in the customer's voice (and check you actually heard them in interviews); dedup vertical single-child chains or fill in missing siblings; make broad, multi-parent opportunities specific to a moment; reject vague themes, guidelines, or sentiment; spot "solutions in disguise" — an opportunity with only one way to address it is really a solution, so find the implied opportunity that admits more than one solution — and capture the underlying cause behind a feeling rather than the feeling itself, since feelings cannot be fixed directly (P078). Trade-off: this discipline slows down capture, but sloppy framing quietly locks the team into one solution or an un-actionable wish.

11. **Target the users' most acute frustration.** High latent frustration and anger mark the best opportunities; the intense early-adopter "Irrationals" reveal true value and carry a product across the chasm, while technology-loving "Lovers" can mislead. Tap deep human emotions and treat emotional groups as distinct from demographics (P061). Trade-off: chasing the most acute pain may mean serving a small, intense group before the broad average, but that intensity is what proves real value.

12. **Run a lightweight opportunity assessment before building.** Do not decide by intuition or by one customer's special request: answer the ten problem-focused questions, size the opportunity conservatively, and get an explicit go or no-go from management even when the product is mandated from above (P029). For a richer collaborative view, use an opportunity canvas — a big spatial layout the group fills with sticky notes covering the problem and solution ideas, users and customers, how users solve it today, user value and metrics, adoption strategy, the business problem, business metrics, and budget, recording assumptions where answers are missing — treating it as a set of topics to discuss, not a form, with the go/no-go resting with the product owner leveraging the team (P102). Trade-off: an assessment adds a gate before building, but it is far cheaper than discovering after launch that the opportunity was too small or the bet was wrong.

13. **Move validated opportunities through the design-thinking arc.** Apply design thinking end to end: empathize (the direct contact of step 1), define and focus (make sense of the learnings and choose a few specific problems), ideate (generate multiple solutions past the obvious first, using a pains-and-joys map as backdrop), prototype (simple or paper, with only enough fidelity to evaluate), and test with real users doing a real task — not bug-checking, selling, or show-and-tell — expecting to iterate (P084). Hand the detailed prototype-fidelity and usability-test mechanics to `prototyping-and-usability-testing`, and assumption/MVP experiment design to `assumptions-hypotheses-and-mvp-experiments`. Trade-off: pushing past the first idea and iterating costs cycles, but the obvious first solution is rarely the best one.

14. **After launch, harness organization-wide customer intelligence.** Keep discovery running by mining the whole organization: customer-service agents (ask what they hear, hold monthly trend meetings, include them in design, and embed hypotheses in call scripts); onsite feedback channels (forms, forums, and communities — noting they skew toward already-engaged customers); search logs (findability signals, validated with test pages); and site analytics and funnel analyses (usage, drop-off, and unbiased measurement of a launched experiment's outcome) (P072). Trade-off: each channel is biased in its own way — feedback channels over-represent the engaged, agents mostly hear the frustrated — so triangulate across them rather than trusting any single stream.

## Inputs

- The product decision, idea, opportunity, or artifact under discovery, and the customer or business outcome it is meant to serve.
- What is already known versus assumed about the users, their real behaviour, and their most acute frustrations.
- Access — direct or proxied — to real target users, plus any existing interview notes, personas, analytics, or research.
- Constraints: the stage (startup/new product versus post-launch), the appetite or timeline, and whether the team is allowed to talk to users.

## Output

- A discovery plan or critique that names the outcome and the opportunity or assumption at stake, recommends how to secure direct user contact and interview for behaviour, structures the opportunity space (e.g., an opportunity solution tree) while flagging framing anti-patterns, and proposes a lightweight opportunity assessment with an explicit go/no-go.
- In review mode, findings keyed to the discovery principles — no direct user contact, preference-based interviewing, market-research-driven decisions, or unframed/unassessed opportunities — each with a concrete remediation.
- Each recommendation names the trade-off it carries, and the output ends with a next step tied to the caller's outcome and stage; the build and the decision itself are handed back to the team and its leadership.

## References

- [`product-principles-index`](../../references/product-principles-index.md) — the catalogue of product-design principles cited in this skill.
- Related skills for hand-off: [`prototyping-and-usability-testing`](../prototyping-and-usability-testing/SKILL.md), [`assumptions-hypotheses-and-mvp-experiments`](../assumptions-hypotheses-and-mvp-experiments/SKILL.md), and [`product-strategy-and-outcomes`](../product-strategy-and-outcomes/SKILL.md).

## Provenance

Distilled and paraphrased — no verbatim quotes — from this package's continuous-discovery cluster principles (P010, P013, P018, P025, P029, P037, P040, P043, P046, P055, P061, P072, P078, P079, P083, P084, P087, P102), which summarize distillation-only sources (Cagan, *Inspired*; Torres, *Continuous Discovery Habits*; Perri, *Escaping the Build Trap*; Gothelf & Seiden, *Lean UX*; Patton, *User Story Mapping*); see the frontmatter block for the exact principle, claim, evidence, and source-anchor IDs.
