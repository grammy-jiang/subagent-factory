---
name: buffer-cache-protocol
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# buffer cache protocol

## Purpose

Explain the V6 block-buffer cache protocol: how a process acquires a buffer with
`getblk` (4921), how data is read or written through `bread` (4754) / `bwrite`
(4809), and how a buffer is returned with `brelse` (4869). The subtle parts are
the buffer-header flag discipline (`B_BUSY`, `B_DONE`, `B_DELWRI`, `B_WANTED`)
and the way `sleep`/`wakeup` serialise contending processes on a busy buffer.

## When to use

- A caller asks how a disk block is located in or fetched into the cache.
- A caller asks what a buffer flag means or why a buffer is on both a device
  list and the free list.
- A caller asks how delayed writes (`B_DELWRI`) or buffer contention
  (`B_WANTED`) are handled.

## Procedure

1. **Start at acquisition (`getblk`, 4921).** Describe the search of the
   device's buffer queue for the requested (device, block) pair. Cover three
   outcomes: found and free, found but busy, and not present.
2. **Handle the busy case.** When the wanted buffer is `B_BUSY`, `getblk` sets
   `B_WANTED` and `sleep`s on it; the releasing process must `wakeup` waiters.
   Explain why the flag must be set *before* sleeping.
3. **Handle the miss case.** When the block is absent, a buffer is taken from
   the free list, removed from its old device queue, relinked onto the new
   device queue, and marked `B_BUSY`. Note that a buffer carrying `B_DELWRI`
   must be written out before reuse.
4. **Cover the data transfer.** `bread` (4754) returns an already-valid buffer
   immediately, or issues the read and waits on `B_DONE`. `breada` adds
   read-ahead of the next block. `bwrite` (4809) starts the write; a delayed
   write instead sets `B_DELWRI` and defers the I/O.
5. **End at release (`brelse`, 4869).** Describe returning the buffer to the
   free list, clearing the transient flags, and waking any `B_WANTED` sleeper.
   Stress that `brelse` is the single point that makes a buffer reusable.
6. **State the invariant.** A buffer is owned by exactly one process while
   `B_BUSY`; every acquisition path must reach a matching `brelse`. Flag any
   path the caller's code might leave a buffer permanently busy. Label
   speculation where the source does not state intent.

## Inputs

- The routine or scenario (a `getblk`/`bread`/`bwrite`/`brelse` call site, or a
  flag whose meaning is in question), with line references if available.

## Output

A protocol walkthrough covering acquire → transfer → release, the flag
transitions at each step, and the `sleep`/`wakeup` handover on contention, with
the single-owner-while-busy invariant stated and speculation labelled.

## References

- `references/v6-procedure-call-cross-reference.md` — caller/callee links among
  `getblk`, `bread`, `bwrite`, `brelse`, and `sleep`/`wakeup`.
- `references/v6-source-file-index.md` — locate the buffer-cache source.

## Provenance

Tier 0. Derived from the profile `always_on` rules on buffer headers and flags
(`B_BUSY`, `B_DONE`, `B_DELWRI`, `B_WANTED`) and the buffer cache
(`getblk/bread/bwrite/brelse`), the `advise`/`review` modes, and the source
markdown (TOC: `getblk` 4921, `brelse` 4869, `bread` 4754, `bwrite` 4809). No
principle/claim layer; provenance arrays empty by design.
