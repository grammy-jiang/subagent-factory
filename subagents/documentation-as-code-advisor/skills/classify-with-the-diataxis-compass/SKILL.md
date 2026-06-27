---
name: classify-with-the-diataxis-compass
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P003
  - P020
  - P021
  - P008
  claims:
  - C00001
  - C00002
  - C00003
  - C00008
  - C00009
  - C00010
  - C00011
  - C00012
  - C00101
  - C00102
  - C00080
  - C00081
  source_anchors:
  - 7065cb6e73a0-c0000
  - 7065cb6e73a0-c0003
  - 7065cb6e73a0-c0004
  authored_from_digest: cc8db46c8431b9bab4bb2a61bfff1495ad02879b1bfabbbcbe86ae2416a04876
---

# Classify with the Diátaxis compass

## Purpose

Decide which one of the four Diátaxis types a piece of documentation is — tutorial, how-to
guide, reference, or explanation — by reading it against the two axes of the compass, then split
out any material that belongs to a different type. The four types exist because documentation
serves two independent axes of need: whether the content serves **action** or **cognition**, and
whether it serves **acquisition** (study) or **application** (work). Crossing the axes yields
exactly four quadrants, so there are exactly four types (P003, P006).

## When to use

- A page feels confused — part walkthrough, part option list, part opinion — and needs sorting.
- A team is planning a documentation set and must decide what each page should be.
- A reviewer must say whether a page is being held to a single type.
- A writer is unsure whether something is a tutorial or a how-to guide, or reference or
  explanation.

Do not use this skill to write the content itself — once the type is settled, hand to
`write-the-four-documentation-types`.

## Procedure

### Step 1 — Read the two compass axes

1. **Action vs cognition.** Ask: is this content about *doing* (practical steps, commands,
   actions) or about *knowing* (concepts, facts, theory)? (P006)

2. **Acquisition vs application.** Ask: does it serve *study* — the user is learning, acquiring
   skill — or *work* — the user is already competent and applying it to a task? (P006)

### Step 2 — Place the content in a quadrant

3. **Action + acquisition → tutorial.** Learning by doing, under guidance, toward a meaningful
   first achievement.

4. **Action + application → how-to guide.** A competent user achieving a specific real-world
   goal. (P020)

5. **Cognition + application → reference.** Theory the user consults while working: austere,
   product-led description. (P021)

6. **Cognition + acquisition → explanation.** Theory the user studies to understand: a bounded
   discussion of a "why". (P021)

### Step 3 — Separate study from work, theory from theory

7. **Do not split tutorials from how-to guides by "basic vs advanced".** The distinction is the
   need served — study vs work — not difficulty. A hard lesson is still a tutorial; an easy task
   recipe is still a how-to guide. (P020)

8. **Tell reference from explanation by what the theory serves.** Both are cognition; reference
   serves application (consult while working), explanation serves acquisition (study to
   understand). (P021)

### Step 4 — Name the type and split the muddle

9. **State the single type the page belongs to**, with the two-axis reason.

10. **Identify any material that belongs to another quadrant** — teaching prose inside a
    reference, an option dump inside a tutorial, an opinion inside a how-to guide. (P008)

11. **Recommend splitting muddled material into its own page** of the correct type, linked rather
    than blended, so each page is held to one type and the forms never muddle together. (P008)

## Inputs

- **Required:** the page or content to classify, and ideally who its reader is and what they are
  trying to do.
- **Optional:** the surrounding documentation set, so cross-links can be proposed.

## Output

A compass reading naming the one Diátaxis type the content is (with the action/cognition and
acquisition/application reasons), plus a list of any material to split out into another type.

## References

- [diataxis-compass-reference](../../references/diataxis-compass-reference.md) — the quadrant
  lookup for the two axes and the four types.

## Provenance

Derived from the compass principle **P006** and the four-types principle **P003**, with the
type-distinction principles **P020** (study vs work) and **P021** (reference vs explanation) and
the keep-distinct principle **P008** (claims **C00001**, **C00008**, **C00101**, **C00080**),
grounded in Daniele Procida, *Diátaxis*, at chunk anchors `7065cb6e73a0-c0000`,
`7065cb6e73a0-c0003`, and `7065cb6e73a0-c0004`. Distillation-only source: paraphrased
throughout, no verbatim quotation.
