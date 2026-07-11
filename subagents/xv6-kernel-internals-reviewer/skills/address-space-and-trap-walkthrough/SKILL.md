---
name: address-space-and-trap-walkthrough
kind: skill
status: ready
provenance:
  principles:
  - pr-001
  - pr-002
  - pr-003
  claims:
  - cl-011
  - cl-013
  - cl-020
  - cl-024
  - cl-027
  source_anchors:
  - a-simple-unix-like-t-20260613000613-h0056
  - a-simple-unix-like-t-20260613000613-h0059
  - a-simple-unix-like-t-20260613000613-h0070
  - a-simple-unix-like-t-20260613000613-h0082
  - a-simple-unix-like-t-20260613000613-h0085
  authored_from_digest: d2d2fce392373dda486d9f41a0cfa6ac42d8264aa37dee5ea89f21434e2eb3db
---

# Address space and trap walkthrough

## Purpose

Walk a reviewer or learner through how xv6 gives each process a private address space using
RISC-V page tables, and how control crosses the user/kernel boundary on a trap — naming the
registers involved (`satp`, `sepc`, `stvec`, `scause`) and showing where isolation is enforced
(page-table separation, the trampoline, and validation of user-supplied addresses via
`copyin`/`copyinstr`). Use it to explain a mechanism or to check that a change keeps the
boundary intact.

## When to use

- A learner is reading or modifying page-table or address-space code (`kvminit`, `walk`,
  `mappages`, `uvmalloc`, `exec`) and needs the mechanism explained.
- Someone must follow a trap from user space into the kernel and back, tracing which registers
  carry the state at each step.
- A reviewer must check that a change still validates user pointers and keeps user and kernel
  address spaces separate.
- **Does not apply** to kernel-only traps that never touch user page tables, or to the
  timer-interrupt machine-mode path handled before `uservec` is reached (pr-002 exemption).

## Procedure

### Step 1 — Establish the address space (pr-001, cl-011, cl-013)

Each process has its own page table (`p->pagetable`) in the format the RISC-V hardware reads
from `satp`. The virtual address space starts at 0 with the process text, followed by data, a
user stack, and an expandable heap, up toward `MAXVA`. The page table also serves as the
sole record of which physical pages belong to the process, which is why freeing user memory
requires walking the page table rather than a separate allocation list.

Process isolation rests on a triple: (a) kernel-controlled entry via `ecall` — the user cannot
jump to an arbitrary kernel address; (b) a private page table per process — one process cannot
name another's physical pages; and (c) time-sliced scheduling. Verify that a change under
review does not open a gap in any of the three legs.

### Step 2 — Explain Sv39 translation

xv6 uses Sv39: 39-bit virtual addresses translated through a three-level page table. The
hardware uses three consecutive 9-bit fields in the virtual address to index root, middle, and
leaf page-table pages. A missing PTE (`PTE_V` clear) at any level causes a page fault, which
allows large unmapped ranges to be represented without allocating intermediate pages.

Each leaf PTE carries a physical page number plus flag bits. Read these flags directly; do not
assume:

- `PTE_V` — entry is valid; otherwise a reference faults.
- `PTE_R` / `PTE_W` / `PTE_X` — read / write / execute permission.
- `PTE_U` — user mode may access; pages without this flag are supervisor-only and inaccessible
  to user code even if the virtual address is known.

### Step 3 — Show how isolation is enforced (pr-001, cl-011, cl-013)

Process isolation is maintained by:

- Each process seeing only its own mappings in its own page table.
- The trampoline page mapped at an identical virtual address in every address space (including
  the kernel) so that the trap handler can begin executing immediately after privilege is raised,
  before `satp` is switched. Without this identity of address, the first instruction after the
  privilege change would fetch from the wrong mapping.
- Guard pages placed below each user stack, mapped as invalid, so a stack overflow faults rather
  than silently overwriting a neighbour's memory.
- When a page-table mapping changes, xv6 issues `sfence.vma` to flush stale TLB entries on the
  current core before any code runs under the new mapping.

Verify that proposed changes preserve all three properties: per-process tables, trampoline
identity, and TLB invalidation discipline.

### Step 4 — Walk the trap entry path (pr-002, cl-020, cl-024)

A trap is triggered by an `ecall` instruction (system call), a hardware exception, or a device
interrupt. On any of these:

1. The hardware raises the privilege level to supervisor mode and jumps to the address in
   `stvec`, landing at `uservec` in the trampoline.
2. `sepc` is set by the hardware to the PC of the instruction that caused the trap (or the
   next instruction for `ecall`).
3. `scause` is set by the hardware to a code identifying the cause.
4. `uservec` saves all 32 user registers into the per-process trapframe (mapped in the address
   space alongside the trampoline) using scratch-space in `sscratch`. This happens before any
   register is overwritten.
5. `uservec` then loads the kernel page table into `satp` (issuing `sfence.vma`) and switches
   to the process's kernel stack.
6. Control transfers to `usertrap`, which reads `scause` to determine whether the cause is a
   system call, an exception, or a device interrupt, and dispatches accordingly.

The sequence must be traced in exactly this order when auditing the path; a change that reorders
the `satp` switch before the full register save would corrupt the trapframe.

### Step 5 — Walk the trap return path (pr-002, cl-020, cl-024)

To return to user code:

1. `usertrapret` sets up values the trampoline will need (user `satp`, trapframe address,
   return address) and calls `userret` in the trampoline.
2. `userret` restores all 32 user registers from the trapframe.
3. `userret` loads the user page table into `satp` (issuing `sfence.vma`) and executes `sret`.
4. `sret` lowers the privilege level and resumes execution at the address in `sepc`.

Note: xv6 deliberately keeps the kernel unmapped from user page tables. This requires a
page-table switch on every trap but removes entire classes of bugs that arise when user-mode
addresses accidentally alias kernel mappings.

This step applies only to the user-space trap path. Kernel-only traps (exceptions or interrupts
taken while already in supervisor mode) do not use `uservec`/`userret` and do not involve the
trampoline's page-table switching; they are handled separately.

### Step 6 — Check user-pointer validation (pr-003, cl-027)

Because user and kernel page tables are separate, a user-supplied virtual address is not
directly dereferenceable by the kernel. The correct pattern is:

- `copyin(dst, src_uaddr, len)` — translates `src_uaddr` through the user page table via
  `walkaddr`, checks that the resulting range falls within user memory, then copies bytes to
  the kernel destination.
- `copyinstr(dst, src_uaddr, max)` — same, but copies a null-terminated string with a length
  bound.
- `copyout(pagetable, dst_uaddr, src, len)` — writes from kernel memory into user space through
  the same translation.

Flag any kernel code that dereferences a user-supplied pointer directly without going through
one of these functions. Such code constitutes a privilege-escalation risk: the pointer could
name an arbitrary physical address the user has no right to read or modify.

`pr-003` applies to every syscall implementation that accepts a pointer argument and to any
kernel code that reads strings or buffers from user space. It does not apply to
kernel-to-kernel pointer passing within a single address space, or to pointers already
validated and copied in an outer call on the same path.

### Step 7 — Check `exec` boundary handling

`exec` builds a fresh page table, allocates memory per ELF segment with `uvmalloc`, and loads
each segment through `loadseg`/`walkaddr` into the process's page table — not the kernel's.
This separation prevents a crafted `ph.vaddr` or `ph.memsz` from writing into kernel memory.

An inaccessible page is placed just below the user stack so that oversized argument copies
cause `copyout` to fault. The old image is not freed until the new image is successfully built,
preserving the ability to return an error.

Flag any missing or overflow-prone address check in `exec`. The source notes explicitly that
xv6 may not validate all edge cases, and real kernels have a significant history of bugs in
exactly this class.

## Inputs

- The specific mechanism, function, or code path under discussion (e.g., `kvminit`, `walk`,
  `exec`, `copyin`, the `uservec`/`usertrap`/`usertrapret`/`userret` sequence) and the
  question asked or change proposed.

## Output

An explanation that names the registers and page-table structures involved and ties each step
to the isolation invariant it preserves — or, in review mode, a critique naming where a change
breaks page-table separation, skips `sfence.vma`, reorders the register-save/`satp`-switch
sequence, or trusts an unvalidated user address.

## References

- `references/xv6-subsystem-map.md` — canonical location of page-table and trap code.

## Provenance

Grounded in:

- pr-001 (cl-011, cl-013): process isolation triple — kernel-controlled `ecall` entry, private
  page table, time-sliced scheduling. Source: §2.2 "User mode, supervisor mode, and system
  calls"; §2.5 "Process overview".
- pr-002 (cl-020, cl-024): full user-space trap path — `uservec` saves to trapframe and
  switches page table/stack; `usertrap` handles cause; `usertrapret`/`userret` restores and
  executes `sret`; trampoline mapped identically in every address space. Kernel-only traps
  exempt. Source: §4.3 "Traps from user space".
- pr-003 (cl-027): validate/copy user pointers via `copyinstr`/`copyin`; never dereference
  directly. Source: §4.6 "Code: System call arguments"; §3.6 "Process address space".

Source: "xv6: a simple, Unix-like teaching operating system" (Cox, Kaashoek, Morris).
Rights: distillation-only — paraphrased throughout, no verbatim quotation.
