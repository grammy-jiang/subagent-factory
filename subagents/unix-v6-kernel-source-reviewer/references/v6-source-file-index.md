---
name: v6-source-file-index
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# V6 Kernel Source File Index

Index of the permanently-resident kernel source files as presented in the V6
source listing, with the subsystem each covers and the anchor routines (with
listing line numbers) to start from. Use this to locate where a topic lives
before tracing it.

| File | Subsystem | Anchor routines (line) |
|------|-----------|------------------------|
| `m40.s` | PDP-11/40 assembly support: traps, interrupts, context save, low-level mode switching (sheets 06..14) | `savu` 0725, `aretu` 0734, `retu` 0740 |
| `l40.s` | low-level / interrupt-vector assembly support | (vectors) |
| `malloc.c` | resource-map allocator for `coremap` / `swapmap` | `malloc` 2528, `mfree` 2556 |
| `slp.c` (scheduling) | process states, sleep/wakeup, swtch, swapping | `sleep` 2066, `wakeup` 2113, `setrun` 2134, `setpri` 2156, `swtch` 2178 |
| `prf.c` / memory mgmt | user address-space layout | `estabur` 1650, `sureg` 1739 |
| signal / process control | signal post/detect/act, core dump, growth | `psignal` 3963, `issig` 3991, `psig` 4043, `core` 4094, `grow` 4136 |
| swapping | swap in/out of process images | `xswap` 4368 |
| `bio.c` (block I/O) | buffer cache + block device I/O | `bread` 4754, `bwrite` 4809, `brelse` 4869, `getblk` 4921 |
| raw I/O | character/raw device transfer | `physio` 5259 |
| `nami.c` (file system) | pathname → inode resolution | `namei` 7518 |

## Header (`.h`) files

The `.h` includes act as global declarations shared across the C files: the
`proc` array and process states (`SRUN`/`SSLEEP`/`SSTOP`/`SZOMB`), the per-
process `user` structure, `buf` headers and flags (`B_BUSY`/`B_DONE`/
`B_DELWRI`/`B_WANTED`), the `inode`, `mount`, and `file` tables. Read the
relevant `.h` before a `.c` so structure layouts are in hand.

## Usage notes

- Line numbers are the V6 source listing references and are the definitive
  citation per the profile source-of-truth policy.
- File-to-subsystem grouping above reflects the commentary's chapter ordering;
  a few routine homes are grouped by subsystem where the captured material did
  not name the exact `.c` file.

## Provenance

Tier 0. Derived from the profile `always_on` rules (data structures, lifecycle,
file system, segmentation, assembler conventions) and `source_of_truth_policy`,
plus the source markdown TOC and "Source Code Files" / "Assembly Language Files"
sections (line anchors as listed above). No principle/claim layer; provenance
arrays empty by design.
