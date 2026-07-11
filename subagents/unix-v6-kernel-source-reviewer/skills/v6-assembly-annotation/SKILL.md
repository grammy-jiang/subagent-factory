---
name: v6-assembly-annotation
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# v6 assembly annotation

## Purpose

Annotate a passage of PDP-11 assembly from the V6 kernel assembly files
(`m40.s`, `l40.s`) so a reader can follow what each instruction does in terms of
register roles, addressing modes, and kernel/user mode context. The hard parts
the commentary repeatedly flags are: the dual meaning of `r6` (kernel versus
user stack pointer), the dual register *sets* selected by the PSW mode bits, and
the compact addressing-mode notation the assembler uses.

## When to use

- A caller presents a fragment from `m40.s` (sheets 06..14) or `l40.s` and asks
  what it does instruction by instruction.
- A caller hits an addressing mode they cannot decode (`-(sp)`, `(r1)+`, `*$x`,
  `2(r5)`) or a `mov`/`jsr`/`mfpi`/`mtpi` they cannot place.
- A caller asks why an assembly routine touches the stack pointer or the
  segmentation/APR registers directly (e.g. inside `savu`, `retu`, `swtch`).

## Procedure

1. **Establish mode context first.** Determine whether the fragment runs in
   kernel or user mode. The PSW mode bits (14-15) select which physical `r6`
   (stack pointer) and which segmentation register set is active. State this
   before decoding operands: the same register name denotes different physical
   hardware depending on mode.
2. **Decode each operand by addressing mode** (commentary §2.5):
   - `rn` register; `(rn)` register-deferred; `(rn)+` autoincrement; `-(rn)`
     autodecrement; `X(rn)` index; `$x` immediate; a `*` prefix selects the
     deferred (indirect) variant. `pc`-relative and absolute forms are the
     `pc`-based (`r7`) special cases of index / deferred.
   - Resolve the effective address, then state the value moved or tested, not
     just the syntax.
3. **Map register roles** as the kernel uses them: `r5` as the C environment /
   frame pointer, `r6` as the stack pointer (per-mode), `r7` as the program
   counter; `r0`-`r1` as conventional return / scratch registers.
4. **Interpret control transfers** in kernel terms: `jsr`/`rts` for subroutine
   call/return (and what they push/pop), `rti`/`rtt` for return from interrupt
   or trap (both `pc` and PSW restored), and `trap`/`emt` as the system-call /
   fault entry path.
5. **Flag cross-mode data moves explicitly.** `mfpi`/`mtpi` move a word from /
   to the *previous* instruction (or data) space; whenever they appear, name
   which space (kernel vs user) is source and which is destination — the usual
   point of confusion.
6. **Tie the fragment back to its C caller.** Most `m40.s` routines exist to do
   what C cannot (manipulate the stack pointer, the PSW, or the APRs). State
   which higher-level routine calls it and what register state it expects on
   entry and guarantees on exit.
7. **Label any speculation.** Where the listing does not make intent explicit,
   say so rather than asserting hardware behaviour beyond the code.

## Inputs

- The assembly fragment, ideally with its `m40.s`/`l40.s` sheet or line range.
- Whether the caller already knows the surrounding mode context.

## Output

A line-by-line (or instruction-group) annotation giving, per step: addressing
mode, effective operand, register role, and mode context — opened with a
statement of kernel/user mode and closed with a tie-back to the C caller.
Speculative readings are labelled.

## References

- `references/pdp11-processor-handbook-reference.md` — instruction and
  addressing-mode lookup.
- `references/v6-source-file-index.md` — locate `m40.s` / `l40.s` by sheet.

## Provenance

Tier 0. Derived from the profile `always_on` rules on PDP-11/40 architecture,
addressing modes, and assembler conventions, the `advise`/`review` modes, and
the source markdown (addressing-mode discussion §2.5; `m40.s` sheets 06..14).
No principle/claim layer in this package; provenance arrays empty by design.
