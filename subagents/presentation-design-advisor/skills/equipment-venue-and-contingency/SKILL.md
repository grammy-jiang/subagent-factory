---
name: equipment-venue-and-contingency
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P028
  - P053
  - P104
  claims:
  - C00257
  - C00258
  - C00474
  - C00475
  - C00477
  - C00478
  - C00479
  - C00481
  - C00482
  - C00483
  - C00486
  - C00487
  - C00488
  - C00489
  - C00584
  - C01318
  evidence: []
  source_anchors: []
  authored_from_digest: fcbad91bf25666e5c0bb56aa91c0e8fab0aecd33d6118da64e9e6934917da293
---


# Equipment, Venue And Contingency

## Purpose

This skill removes the dependencies that fail in rooms the speaker does not control and plans for the failures that remain. It embeds every image and film in a local file with a backup on separate media rather than relying on internet access many organisations restrict, keeps a teleconferenced presentation simple because films lock up and sound clips feed back in transmission, and brings the speaker's own laptop where the deck needs unusual typefaces, settings, formats, or films. It never lets a live demonstration be attempted without rehearsal on the actual equipment, since an unpractised demonstration can injure the presenter, hijack the lesson, or cost a contract outright at the culminating moment of a bid — and it states plainly that rehearsal guarantees nothing, since practised demonstrations still fail, but greatly increases the odds. Once the structure and slides are set, it imagines the worst compound case and devises a plan for equipment failure, because disasters arise from chains of causes rather than single ones: where the equipment is unproven it designs the talk to be deliverable from handouts alone, and it carries a troubleshooting kit of video and audio cables and a small computer-powered speaker plus the knowledge of how to match the laptop's resolution to the projector. It also treats the screen itself as controllable, blanking it deliberately where a portion of the talk needs no visual support.

## When to use

- The presentation will be given in a room, or over a link, the speaker does not control (P104).
- The talk includes a live demonstration (P028).
- The structure and slides are set and a failure plan is still missing (P053).
- Part of the talk needs no visual support and the screen should go dark deliberately (P003).

## Procedure

1. Blank the screen deliberately with the black or white key, or with an inserted black slide when the keyboard is out of reach (P003).
2. Never attempt a live demonstration without rehearsing it on the actual equipment (P028).
3. Imagine the worst compound case once the structure and slides are set and devise a plan for equipment failure (P053).
4. Remove the dependencies that fail in an unfamiliar room (P104).

## Inputs

- The venue, its equipment and connectivity, what the deck depends on, whether a demonstration is planned, and how much setup access the speaker will get.
- The reasoning offered for the design or decision under review: what the presentation is meant to achieve, what is on the slides now, and any claim about why the current form works.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first, and mark where the source's guidance is conditional or context-bound rather than presenting it as settled. This skill advises on presentation design and delivery; it does not write the talk, build the deck, produce the graphics, deliver the presentation, or rule on whether the underlying result is correct.

## Anti-patterns to flag

- Overlooking P003: Blank the screen deliberately with the black or white key, or with an inserted black slide when the keyboard is out of reach.
- Overlooking P028: Never attempt a live demonstration without rehearsing it on the actual equipment.
- Overlooking P053: Imagine the worst compound case once the structure and slides are set and devise a plan for equipment failure.
- Overlooking P104: Remove the dependencies that fail in an unfamiliar room.

## References

See `../../references/presentation-design-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/presentation-design-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P003, P028, P053, P104, grounded in three distillation-only sources on presentation design and delivery (Alley's *The Craft of Scientific Presentations*, and Duarte's *Resonate* and *slide:ology*). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
