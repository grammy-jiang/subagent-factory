---
name: v6-procedure-call-cross-reference
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# V6 Procedure Call Cross-Reference

Caller → callee relations among the core kernel routines, so a reviewer can move
"up" to callers or "down" to callees while tracing. Line numbers are the V6
source listing references. Read as: the **routine** typically **calls** the
listed callees, and is reached from the listed callers.

## Scheduling / context switch

| Routine (line) | Calls | Called from |
|----------------|-------|-------------|
| `sleep` (2066) | `savu`, `swtch`, `setpri`, `spl` adjust | any blocking kernel path |
| `swtch` (2178) | `savu` (2189), `retu` (2193), `aretu` | `sleep`, scheduler, `newproc` path |
| `wakeup` (2113) | `setrun` | I/O completion, event signallers |
| `setrun` (2134) | `wakeup(&runout)` (swapper) | `wakeup`, `psignal`, `newproc` |
| `setpri` (2156) | — | `sleep`, `swtch` |
| `savu` (0725) / `retu` (0740) / `aretu` (0734) | (assembly, no C callees) | `swtch`, `sleep` |

## Memory / segmentation / swap

| Routine (line) | Calls | Called from |
|----------------|-------|-------------|
| `malloc` (2528) | — (scans `coremap`/`swapmap`) | `exec`, `grow`, swap-in |
| `mfree` (2556) | — | `exit`, swap-out, `grow` shrink |
| `estabur` (1650) | `sureg` | `exec`, `grow` |
| `sureg` (1739) | — (loads APRs) | `estabur`, `swtch` resume |
| `grow` (4136) | `malloc`/`mfree`, `estabur` | `sbrk`, signal handler setup |
| `xswap` (4368) | `swap`, `malloc`/`mfree` | swapper |

## File system / buffer cache

| Routine (line) | Calls | Called from |
|----------------|-------|-------------|
| `namei` (7518) | `iget`, `bread` (directory blocks) | `open`, `creat`, `link`, `exec` |
| `bread` (4754) | `getblk`, `sleep` (on `B_DONE`) | `readi`, `namei` |
| `bwrite` (4809) | `getblk` path, `sleep` | `writei`, sync |
| `brelse` (4869) | `wakeup` (on `B_WANTED`) | end of every buffer use |
| `getblk` (4921) | `sleep` (on `B_BUSY`), `brelse` of reused buf | `bread`, `bwrite`, alloc |
| `physio` (5259) | device strategy, `sleep` | raw read/write |

## Signals

| Routine (line) | Calls | Called from |
|----------------|-------|-------------|
| `psignal` (3963) | `setrun` (wake interruptible sleeper) | `kill`, traps, hardware events |
| `issig` (3991) | — (tests pending signal) | syscall/trap return, `sleep` |
| `psig` (4043) | `core`, `grow` (handler stack), `exit` | after `issig` reports pending |
| `core` (4094) | `bwrite`/file write path | `psig` on dumping signal |

## Usage notes

- Relations are the principal ones from the captured material; some routines have
  additional minor callers not listed.
- Dashes mean "no significant C callee" (assembly leaf or pure table scan).
- Confirm any call edge against the source listing before asserting it as fact;
  label inferred edges as such per the profile speculation rule.

## Provenance

Tier 0. Derived from the profile `quality_bar` (cross-references must be
explicit, e.g. "swtch calls retu") and `always_on` lifecycle/file-system/signal
rules, plus the source markdown (e.g. `swtch` calling `savu` at 2189 and `retu`
at 2193; `wakeup`→`setrun`; line anchors as listed). No principle/claim layer;
provenance arrays empty by design.
