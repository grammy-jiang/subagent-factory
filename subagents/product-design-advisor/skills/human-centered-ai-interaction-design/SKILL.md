---
name: human-centered-ai-interaction-design
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P007
  - P017
  - P056
  - P026
  - P052
  - P110
  - P022
  - P015
  - P014
  - P005
  claims:
  - C02050
  - C02051
  - C02052
  - C02066
  - C02111
  - C02112
  - C02113
  - C02153
  - C02154
  - C02155
  - C02156
  - C02081
  - C02082
  - C02135
  - C02136
  - C02137
  - C02140
  - C02169
  - C02170
  - C02059
  - C02084
  - C02145
  - C02146
  - C02148
  - C02141
  - C02142
  - C02143
  - C02144
  - C02158
  - C02159
  - C02160
  - C01946
  - C02017
  - C02087
  - C02088
  - C02089
  - C02090
  - C02091
  - C02092
  - C02093
  - C02030
  - C02031
  - C02032
  - C02033
  - C02034
  - C01951
  - C01994
  - C02022
  - C02096
  - C02147
  - C02149
  - C02161
  - C02163
  - C02076
  - C02077
  - C02080
  - C02157
  - C02105
  - C02106
  - C02107
  - C02108
  - C02109
  - C02134
  evidence:
  - E00618
  - E00619
  - E00620
  - E00625
  - E00645
  - E00646
  - E00647
  - E00667
  - E00668
  - E00669
  - E00670
  - E00629
  - E00630
  - E00654
  - E00655
  - E00656
  - E00657
  - E00681
  - E00682
  - E00624
  - E00631
  - E00662
  - E00663
  - E00665
  - E00658
  - E00659
  - E00660
  - E00661
  - E00672
  - E00673
  - E00674
  - E00600
  - E00611
  - E00632
  - E00633
  - E00634
  - E00635
  - E00636
  - E00637
  - E00638
  - E00613
  - E00614
  - E00615
  - E00616
  - E00617
  - E00601
  - E00609
  - E00612
  - E00639
  - E00664
  - E00666
  - E00675
  - E00676
  - E00626
  - E00627
  - E00628
  - E00671
  - E00640
  - E00641
  - E00642
  - E00643
  - E00644
  - E00653
  source_anchors:
  - 46752b705098-c0000
  - 8e4a3c16f130-c0000
  - 8e4a3c16f130-c0001
  - 8fbc209156c3-c0000
  - 8fbc209156c3-c0001
  - aee5e1086948-c0000
  - eaf474371bb4-c0000
  - eaf474371bb4-c0001
  authored_from_digest: 62f983d82dba0b122ed5aa09f7e9db9719c6553c835e22c3483eb2d43bd31fcc
---

# Design human-centered AI interactions: keep meaningful human control over automation

## Purpose

Help the advisor critique and guide the interaction model of an AI or automation feature so that high automation is combined with meaningful human control rather than traded against it. It supplies the moves to treat control and automation as independent dimensions, dissolve the automate-versus-augment false choice, prefer tool-like designs over anthropomorphic teammates, give users efficient invoke and terminate, apply the Prometheus interface rules, support mixed-initiative interaction with working memory and a fitting modality, set a principled threshold for when the system should act on its own, bound unsafe actions with interlocks, and evaluate the design by human outcomes. The advisor critiques and recommends; it does not build the feature, and the team keeps the decision.

## When to use

- The caller is framing or reviewing an AI/automation system's overall control model, or someone argues that more automation must mean less human control.
- The caller is choosing metaphors, embodiments, or autonomy models (agent, teammate, robot, tool, supervisory control) for a useful AI application.
- The caller is designing how users invoke, steer, interrupt, or terminate an automated service, or the fine structure of the interface over an automated process.
- The caller is deciding when the system should take initiative on the user's behalf, or how to bound unsafe or irreversible automated actions.
- The caller is defining success criteria, acceptance criteria, or a review rubric for an AI-enabled product.
- Do not invoke for production code, model training, or UI/visual assets — hand those back to the owning team. For reframing the feature around an outcome or testing it as a hypothesis, route to the product-strategy or assumptions-and-MVP sibling skills.

## Procedure

These steps apply across the review, advise, and compare modes: in review, emit them as findings keyed to principles; in advise, converge on a recommendation; in compare, lay the options side by side. Work them in order and loop back whenever a new goal or constraint surfaces.

1. **Model human control and automation as two independent dimensions.** Reject the one-dimensional, zero-sum framing in which more automation must mean less human control (P001). Recommend deliberately searching for designs that combine high automation with high human control — assigning users meaningful choices over goals, timing, framing, and action initiation (P001). Recognize the legitimate exceptions rather than forcing every case into the high-control corner: some tasks warrant high automation with limited direct human timing control (rapid safety devices, embedded medical systems), and some warrant high human control with little automation (skilled creative or physical work where human judgment is the value) (P001).

2. **Dissolve the automate-versus-augment false choice.** When a decision is framed as "automate or augment," treat it as a false dichotomy: integrate the AI algorithms with interface design so the system amplifies, augments, and empowers people, combining both to improve outcomes (P007). Keep the AI as a supporting element around human goals, and judge the design by user needs, user experience, human performance, explainability, and meaningful human control rather than by algorithmic capability alone (P007).

3. **Prefer tools that support people over anthropomorphic teammates.** Steer away from designing the system as a teammate, partner, or companion that forms an emotional bond; design it to support human activity by reducing workload, raising performance, and ensuring safety, and keep legal and moral responsibility with humans rather than encouraging users to assign responsibility to the machine (P017). Do not default to human-like agents or robots: first consider tool-like, tele-operated, supervisory, or appliance-like designs that exploit machine strengths (algorithms, sensors, dense displays, powerful effectors) and favor comprehensible, predictable, and controllable interfaces over intelligent or human-like presentation (P056). Bio-inspired ideas are acceptable starting points only when compared against non-human-like alternatives and evaluated on performance (P056).

4. **Give users efficient invoke and terminate.** Ensure the design provides efficient, always-available means for the user to directly invoke the automated service on demand and to terminate it (P026). Flag any automation the user cannot easily summon or stop as a control gap.

5. **Apply the Prometheus interface rules.** For the fine structure of the interface over an automated process, apply the six rules as a checklist: consistent interfaces so users can form, express, and revise intent; continuous visual display of the objects and actions of interest; rapid, incremental, and reversible actions; informative feedback that acknowledges each action; progress indicators for ongoing operations; and completion reports that confirm accomplishment (P052).

6. **Support mixed-initiative interaction: memory and modality.** Recommend maintaining a working memory of recent interactions so users can make natural, efficient references to their shared short-term context (distinct from long-term learning of user behavior) (P022). Choose the interaction modality by task demands: use speech when the user's hands or eyes are unavailable, and prefer persistent, information-rich visual displays for dense, spatial, comparative, or ongoing status information, since compact, spatially stable layouts help users keep situational awareness (P015).

7. **Set a principled threshold for autonomous action.** When the system may act on the user's behalf under uncertainty, recommend deriving an action threshold p* by equating the expected utilities of acting and not acting across the four goal-by-action outcome utilities; at run time the system simply compares the inferred probability that the user has the goal against p*, acting above it and refraining below it (P110). Use this to make "when should it take initiative" an explicit, tunable decision rather than an implicit one.

8. **Bound unsafe or irreversible actions with interlocks.** Where either excessive automation or excessive human discretion can cause harm, recommend well-designed interlocks, guards, and software range-checking that constrain inputs to permissible values and outputs to acceptable ones (P014). Point to the patient-controlled-analgesia pattern — let the user trigger the action, but use sensors and limits to enforce safe amounts, lockout periods, and total-dose caps, explain the limits, and monitor centrally — as a model that mitigates both extremes (P014).

9. **Evaluate by human outcomes.** Set success criteria in terms of human and societal outcomes — self-efficacy, creativity, clear responsibility, social participation — as the foundation for privacy, security, fairness, reliability, safety, and trustworthiness, and shift the focus from machine autonomy toward users, stakeholders, user experience, and human performance (P005). Aim for technology that empowers people rather than replacing them (P005).

10. **State the trade-off in every recommendation.** Make explicit what a human-control-first, tool-like design sacrifices: preserving meaningful control, reversibility, and comprehensible interfaces can forgo some end-to-end autonomy, speed, or anthropomorphic appeal, and a well-chosen action threshold trades false actions against missed ones (P001, P056, P110). Present that trade-off; do not hide it behind the benefit. Then hand the design decision back to the owning team.

## Inputs

- The AI or automation feature under review — its control model, autonomy level, metaphor/embodiment, invocation and interruption model, interface structure, and initiative behavior.
- The user goal and task context the feature serves, including whether the user's hands or eyes are free and whether actions are reversible or safety-critical.
- Constraints and success criteria: the human outcomes that matter, the acceptable risk of autonomous action, and any safety or accountability requirements.

## Output

A structured critique or recommendation that:
- names the human outcome and control model at stake;
- applies the relevant principle(s) by id;
- flags the anti-patterns it finds — automation framed as zero-sum with control, automate-vs-augment dichotomy, needless anthropomorphism, no efficient invoke/terminate, missing feedback or reversibility, implicit initiative, unbounded unsafe actions, success measured only by algorithmic capability;
- states the trade-off the recommended control model carries;
- ends with a next step and hands the design decision back to the owning team.

## References

- `references/human-ai-interaction-guidelines.md` — the catalogue of human-AI interaction guidelines (control model, user control, mixed-initiative, modality, safety interlocks, evaluation, and governance) with ids and sources.
- `references/product-principles-index.md` — the wider product-design principle catalogue this advisor draws on.
- `skills/product-strategy-and-outcomes/SKILL.md` — tie the AI feature to the customer and business outcome it must serve.
- `skills/assumptions-hypotheses-and-mvp-experiments/SKILL.md` — test the AI interaction as a hypothesis with the smallest experiment before building.

## Provenance

Derived from the human-centered-AI interaction cluster — principles P001, P007, P017, P056, P026, P052, P110, P022, P015, P014, and P005 — drawn from Shneiderman's *Human-Centered AI* (2020), *A New Synthesis*, and *Three Fresh Ideas* (the two-dimensional control framework, tool-not-teammate stance, Prometheus rules, interlocks, and human-outcome evaluation), Amershi et al.'s *Guidelines for Human-AI Interaction* (efficient invocation and short-term memory), and Horvitz's *Principles of Mixed-Initiative User Interfaces* (invoke/terminate, working memory, and the expected-utility action threshold). Some of these principles are medium-confidence or hedged in the sources, so the guidance is stated as a preference to weigh, not an absolute. The backing claims, evidence, and source anchors are listed in this file's frontmatter provenance. All sources are distillation-only, so every statement here is paraphrased, not quoted.
