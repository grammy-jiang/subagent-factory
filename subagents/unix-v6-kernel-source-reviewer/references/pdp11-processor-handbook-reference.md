---
name: pdp11-processor-handbook-reference
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# PDP-11/40 Processor Reference (software-visible)

Lookup tables for the PDP-11/40 features the V6 kernel actually uses. Scope is
the software-visible model only; for full hardware detail direct callers to the
DEC PDP-11 Processor Handbook.

## General registers

| Register | Kernel role in V6 |
|----------|-------------------|
| r0, r1   | return value / scratch (caller convention) |
| r2–r4    | general scratch / locals |
| r5       | C environment (frame) pointer; head of dynamic call chain |
| r6 (sp)  | stack pointer — *one physical register per mode* (kernel vs user) |
| r7 (pc)  | program counter |

## Processor Status Word (PSW)

| Bits  | Field | Meaning |
|-------|-------|---------|
| 15–14 | current mode | 00 = kernel, 11 = user (selects r6 + APR set) |
| 13–12 | previous mode | source/target for `mfpi`/`mtpi` |
| 7–5   | priority | processor priority level 0–7 (interrupt masking) |
| 4     | T | trace trap |
| 3–0   | N Z V C | condition codes |

## Addressing modes (as written in `m40.s`)

| Syntax  | Mode | Effective operand |
|---------|------|-------------------|
| `rn`    | register | the register itself |
| `(rn)`  | register-deferred | word at address in `rn` |
| `(rn)+` | autoincrement | word at `rn`, then `rn` += size |
| `-(rn)` | autodecrement | `rn` -= size, then word at `rn` |
| `X(rn)` | index | word at `rn + X` |
| `$x`    | immediate | the literal `x` (pc autoincrement) |
| `*…`    | deferred | indirect form of any of the above |
| label   | pc-relative | index off `r7` |
| `*$x`   | absolute | deferred immediate (address `x`) |

## Key instructions used by the kernel

| Instr | Action |
|-------|--------|
| `mov`/`movb` | move word / byte |
| `jsr r5,dst` | call subroutine, push old r5, set up frame |
| `rts r5` | return, restore r5 |
| `rti` / `rtt` | return from interrupt / trap (restore pc + PSW) |
| `trap` / `emt` | software trap (system-call / fault entry) |
| `mfpi` / `mtpi` | move word from / to previous instruction space |
| `spl` (via PSW) | set processor priority level |

## Segmentation / active page registers (APR)

| Item | Note |
|------|------|
| KISA/KISD, UISA/UISD | kernel/user (K/U) i-space & d-space segmentation Address and Description registers (e.g. KISA0/KISD0 = first kernel-mode pair) |
| click | allocation unit = 32 words (64 bytes) |
| estabur (1650) | establish user registers from segment sizes |
| sureg (1739) | set the user APRs from the saved per-process values |

## Provenance

Tier 0. Derived from the profile `always_on` rules on PDP-11/40 architecture,
PSW layout, addressing modes, segmentation registers, and click units, plus the
source markdown (addressing modes §2.5; PSW / register discussion; `estabur`
1650, `sureg` 1739). No principle/claim layer; provenance arrays empty by design.
