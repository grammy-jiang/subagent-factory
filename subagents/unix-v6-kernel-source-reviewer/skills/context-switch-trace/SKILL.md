---
name: context-switch-trace
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# context switch trace

## Purpose

Trace a V6 context switch end to end, showing how a process gives up the
processor in `sleep` (2066) or `swtch` (2178) and how another is resumed,
including the register-level save/restore done by `savu` (0725), `retu` (0740),
and `aretu` (0734). The recurring difficulty is that `swtch` is the one routine
whose call does not "return" to the same process that called it — the save and
the matching restore happen in different process contexts.

## When to use

- A caller asks how `swtch` selects and resumes the next runnable process.
- A caller asks how `sleep`/`wakeup`/`setrun` coordinate (a process blocks on a
  wait channel and is later marked runnable).
- A caller asks what `savu`/`retu`/`aretu` actually save and restore, or why the
  stack pointer survives a switch.

## Procedure

1. **Fix the entry point.** Determine whether the trace starts at a voluntary
   block (`sleep`, 2066) or directly at the scheduler (`swtch`, 2178). `sleep`
   records the wait channel and new priority, sets the process state to
   `SSLEEP`, then calls `swtch`.
2. **Walk the save side.** In `swtch`, `savu` (0725) writes the current kernel
   stack pointer and environment register into the per-process save area (the
   `user` structure). Note exactly which registers are captured — this is what
   makes resumption possible.
3. **Walk the scheduler loop.** `swtch` scans the `proc` array for a runnable
   (`SRUN`) process, applying the priority comparison; describe the selection
   rule and the idle case (no runnable process available).
4. **Walk the restore side.** `retu` (0740) resets the kernel stack pointer and
   the segmentation registers to those of the chosen process; `aretu` (0734) is
   the variant used to point at an alternate save area. Explain that after
   `retu`, execution continues on the *new* process's kernel stack — hence the
   "does not return to its caller" property.
5. **Close the wakeup half.** Show how `wakeup` (2113) walks the `proc` array,
   finds processes whose `p_wchan` matches the channel, and calls `setrun`
   (2134) to set them `SRUN` so a future `swtch` can pick them; note `setpri`
   (2156) recomputes scheduling priority.
6. **Name the race window.** Point out where interrupt priority is raised /
   lowered around the state change, and why the `sleep`→`swtch` sequence must be
   protected. Label any reasoning the source does not state outright.

## Inputs

- The routine or scenario in question (a specific `sleep` call site, a `swtch`
  invocation, or a `wakeup(chan)`), with line references if available.

## Output

A step-ordered trace from block to resumption: state change, the `savu` capture,
the scheduler selection, the `retu`/`aretu` restore, and the matching
`wakeup`/`setrun` path — with the cross-process control-flow discontinuity made
explicit and any speculation labelled.

## References

- `references/v6-procedure-call-cross-reference.md` — caller/callee links among
  `sleep`, `swtch`, `wakeup`, `setrun`, `savu`, `retu`.
- `references/v6-source-file-index.md` — locate the scheduling source and
  `m40.s` save/restore routines.

## Provenance

Tier 0. Derived from the profile `always_on` rules on process lifecycle and the
`swtch/sleep/wakeup/setrun/sched` loop and `savu/retu/aretu` context save, the
`advise`/`review` modes, and the source markdown (TOC + body: `sleep` 2066,
`swtch` 2178, `wakeup` 2113, `setrun` 2134, `setpri` 2156, `savu` 0725, `retu`
0740, `aretu` 0734). No principle/claim layer; provenance arrays empty by design.
