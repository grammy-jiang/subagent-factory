---
name: malloc-mfree-algorithm
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# malloc mfree algorithm

## Purpose

Explain the V6 resource-map allocator: `malloc` (2528) and `mfree` (2556) in
`malloc.c`, which manage two arrays — `coremap` (main memory) and `swapmap`
(swap space) — as ordered lists of free (size, address) extents. The points that
trip readers are that the *same* two procedures serve both maps (the map is a
parameter), that addresses and sizes are reckoned in units appropriate to the
map (clicks for core), and that `mfree` must coalesce a returned area with
adjacent free extents.

## When to use

- A caller asks how main memory or swap space is allocated and freed in V6.
- A caller asks what `coremap`/`swapmap` entries mean or why a returned value of
  zero from `malloc` matters.
- A caller asks how free-list coalescing works on `mfree`.

## Procedure

1. **Frame the data structure.** Each map (`coremap`, `swapmap`) is an array of
   (size, address) entries kept sorted by address, listing the *free* extents.
   The map to operate on is passed in, so describe the chosen map explicitly.
2. **Walk `malloc` (2528).** It scans the map for the first entry large enough
   (first-fit). On a match, it carves the requested amount off that entry —
   reducing the entry's size and advancing its base, or removing the entry
   entirely when it is consumed exactly. It returns the base address of the
   allocated area.
3. **Handle exhaustion.** A return value of zero means "no area available"; make
   clear this is the sentinel the caller must test, since zero is not a valid
   allocated address here.
4. **Walk `mfree` (2556).** It inserts the returned (size, address) area back
   into the sorted map. Describe the three coalescing cases: merge with the
   preceding extent, merge with the following extent, or both (closing a gap and
   collapsing two entries into one). A freed area that is adjacent to none
   becomes a new entry.
5. **State the unit discipline.** Sizes and addresses are in the map's natural
   unit (e.g. 32-word / 64-byte clicks for `coremap`); never mix byte and click
   reckoning when explaining an entry.
6. **Note fragmentation behaviour.** First-fit plus coalescing keeps the list
   short but can still fragment; say so without overstating, and label any claim
   the source does not support.

## Inputs

- The map in question (`coremap` or `swapmap`) and the `malloc`/`mfree` call
  site or scenario, with line references if available.

## Output

A walkthrough of the chosen map's state across a `malloc`/`mfree` pair: the
first-fit scan and carve, the zero-return sentinel, and the coalescing insertion
— with the unit discipline stated and speculation labelled.

## References

- `references/v6-source-file-index.md` — locate `malloc.c`.
- `references/v6-procedure-call-cross-reference.md` — callers of `malloc`/`mfree`
  (process creation, swapping, growth).

## Provenance

Tier 0. Derived from the profile `always_on` rules on V6 memory management /
segmentation and click units, the `advise`/`review`/`extract` modes, and the
source markdown (`malloc.c` discussion; `malloc` 2528, `mfree` 2556; `coremap` /
`swapmap` arrays). No principle/claim layer; provenance arrays empty by design.
