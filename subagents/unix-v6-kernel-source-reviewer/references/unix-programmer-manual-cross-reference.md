---
name: unix-programmer-manual-cross-reference
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# UNIX Programmer's Manual ↔ Kernel Cross-Reference

Maps user-visible behaviour documented in the UNIX Programmer's Manual (UPM
section II system calls / IV special files) to the kernel routines that
implement it, so a reader moving between the manual and the source has an entry
point. Line numbers are the V6 source listing references.

| User-visible (UPM) | Implementing kernel routine(s) | Source line |
|--------------------|--------------------------------|-------------|
| `fork` (II)        | `newproc` + scheduler setup | (newproc) |
| `exec` (II)        | `exec`, with `estabur`/`grow` | 1650 / 4136 |
| `exit` / `wait` (II) | `exit`, `wait`, zombie reaping | — |
| `open`/`creat` (II) | `namei` + `iget`/`ialloc`, file-table alloc | 7518 |
| `read`/`write` (II) | `readi`/`writei` via buffer cache `bread`/`bwrite` | 4754 / 4809 |
| `pipe` (II)        | pipe inode handling (pipes as special disk files) | — |
| `signal`/`kill` (II) | `psignal` post, `issig` detect, `psig` act | 3963 / 3991 / 4043 |
| `nice` (II)        | priority adjust feeding `setpri` | 2156 |
| `sbrk` (II)        | `grow` (user address-space growth) | 4136 |
| `mount`/`umount` (II) | `smount` / `sumount`, mount table | — |
| block/char devices (IV) | driver `bdevsw`/`cdevsw` dispatch; `physio` for raw | 5259 |
| swapping (internal) | `xswap`, `swap`, `coremap`/`swapmap` via `malloc` | 4368 / 2528 |

## Usage notes

- The UPM describes *contract* (arguments, return values, errors); the kernel
  routine describes *mechanism*. When they appear to disagree, the V6 source
  listing is authoritative for what the code does (see profile precedence rule).
- Dashes mark routines present in the source but without a confirmed line number
  in the captured material; resolve against `references/v6-source-file-index.md`
  before quoting a number.

## Provenance

Tier 0. Derived from the profile `handoff_rules` (direct callers to the UPM for
system-call semantics), the `always_on` file-system / signal / segmentation
rules, and the source markdown (system-call dispatch via `sysent`; `namei` 7518,
`bread` 4754, `bwrite` 4809, `psignal` 3963, `issig` 3991, `psig` 4043, `setpri`
2156, `grow` 4136, `physio` 5259, `xswap` 4368, `estabur` 1650). No
principle/claim layer; provenance arrays empty by design.
