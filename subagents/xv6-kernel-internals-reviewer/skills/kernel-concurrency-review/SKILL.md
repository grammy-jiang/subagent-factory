---
name: kernel-concurrency-review
kind: skill
status: ready
provenance:
  principles:
  - pr-004
  - pr-005
  - pr-006
  - pr-007
  - pr-008
  - pr-009
  claims:
  - cl-029
  - cl-032
  - cl-033
  - cl-034
  - cl-035
  - cl-036
  - cl-037
  - cl-038
  - cl-040
  - cl-041
  - cl-043
  - cl-044
  - cl-045
  - cl-048
  - cl-049
  source_anchors:
  - a-simple-unix-like-t-20260613000613-h0092
  - a-simple-unix-like-t-20260613000613-h0100
  - a-simple-unix-like-t-20260613000613-h0101
  - a-simple-unix-like-t-20260613000613-h0102
  - a-simple-unix-like-t-20260613000613-h0103
  - a-simple-unix-like-t-20260613000613-h0106
  - a-simple-unix-like-t-20260613000613-h0112
  - a-simple-unix-like-t-20260613000613-h0113
  - a-simple-unix-like-t-20260613000613-h0115
  - a-simple-unix-like-t-20260613000613-h0128
  - a-simple-unix-like-t-20260613000613-h0130
  - a-simple-unix-like-t-20260613000613-h0131
  authored_from_digest: 3fdad99062656c21ebde928a380dc05f7c1a1e3438bcd7520e80eac70be47d01
---

# Kernel concurrency review

## Purpose

Locate and judge concurrency defects in xv6-style kernel code against xv6's documented locking
discipline. Findings must name the precise invariant a piece of code upholds or breaks, not
assert from general folklore. The categories of defect are: races on shared multi-field data
(pr-004), lock-ordering violations that enable deadlock (pr-005), spinlock acquire/release
discipline violations — including missing barriers and interrupt-disable sequencing (pr-006),
wrong choice of spinlock versus sleep-lock (pr-007), lost-wakeup errors in sleep/wakeup patterns
(pr-008), and p->lock hand-off errors across the scheduler context switch (pr-009).

## When to use

- Kernel-style code touches data shared between threads on different CPUs, or between a thread
  and an interrupt handler, and you must check it is properly serialized.
- A change acquires more than one lock and you must confirm it honours the single global lock
  order so it cannot deadlock.
- Code implements or uses a sleep/wakeup (condition-variable) pattern and you must verify it
  cannot miss a wakeup.
- A reviewer must choose between, or check the use of, a spinlock and a sleep-lock.
- Code touches the yield/swtch/scheduler path or process kill/exit logic.

## Procedure

Work through every step in order. Steps are keyed to the principle that drives them.

### Step 1 — Identify shared state and its covering lock (pr-004, cl-029, cl-032)

For each data structure touched by the code under review:

1. Name the lock intended to serialize access (e.g., `kmem.lock` for the free list,
   `p->lock` for process state, `log.lock` for the transaction log, `bcache.lock` for buffer
   cache membership).
2. Determine what fields the lock's invariant spans. If the invariant requires two or more
   memory locations to be consistent simultaneously (e.g., `p->state` and `p->chan` are both
   part of the sleeping invariant), confirm that a single lock covers all of them — partial
   coverage allows a concurrent CPU to observe a transiently violated state.
3. Flag any shared field that is read or written without the covering lock held. Even a read of
   a single field can observe a torn intermediate value if a concurrent writer is updating a
   multi-field invariant.
4. Do not flag single-field atomic updates whose invariant is genuinely one variable; that is
   outside this principle's scope.

### Step 2 — Check lock ordering for deadlock (pr-005, cl-033, cl-034)

1. For every code path that holds two or more locks simultaneously, list them in acquisition
   order as they appear in the path.
2. Compare against the global ordering established by the rest of the kernel. In the xv6
   filesystem, for example, the order is: directory inode lock → new inode lock → buffer cache
   lock (`bcache.lock`) → disk lock (`vdisk_lock`) → process lock (`p->lock`). Any deviation
   is a potential deadlock.
3. Watch for structural hard cases:
   - The lock identity is not known until after a prior lock is held (pathname lookup,
     scanning the process table in `wait`/`exit`).
   - The same lock could be acquired twice — e.g., a pathname containing `.` causing the same
     directory to be locked in a recursive call.
   - The call graph obscures the simultaneous hold: lock A is taken, a helper is called, and
     the helper takes lock B; but elsewhere B is taken before A.
4. Flag any violation. This check applies only to paths that hold two or more locks; it does
   not apply to lock-free or RCU-based designs outside xv6's spinlock model.

### Step 3 — Check spinlock acquire/release discipline (pr-006, cl-035, cl-036, cl-037, cl-038)

Apply the following three-part check to every spinlock acquire/release pair:

**3a. Interrupt-disable sequencing (cl-035, cl-036)**

Confirm that `push_off` (which saves the interrupt enable state and disables interrupts) is
called strictly before `lk->locked` is set to 1. Reversing this order creates a window where
an interrupt fires on the core after the lock is marked held but before interrupts are disabled:
if the handler tries to acquire the same lock, the core deadlocks with itself. This applies to
spinlock acquire implementations; sleep-lock sections have different rules.

**3b. Memory barrier placement (cl-037)**

Confirm that a `__sync_synchronize()` full memory barrier appears in `acquire` (after the
atomic swap that sets `lk->locked`) and in `release` (before clearing `lk->locked`). These
barriers prevent the compiler and CPU from moving loads or stores across the lock boundary.
Without the acquire-side barrier, the compiler could hoist reads out of the critical section;
without the release-side barrier, it could sink writes past the unlock. Flag any spinlock
implementation where either barrier is absent. This check is scoped to spinlock sections; it
does not apply to sleep-lock critical sections.

**3c. No spinlock across sleep or blocking (cl-038)**

Confirm that no spinlock is held across any call that may yield the CPU — `sleep`, disk I/O
completion waits, `acquiresleep`, etc. A spinlock disables interrupts on the holding core;
yielding while interrupts are off corrupts the scheduler invariants and can make the system
unresponsive.

### Step 4 — Check spinlock vs sleep-lock choice (pr-007, cl-038)

1. For each critical section, assess duration. Spinlocks are appropriate for short sections
   (memory allocation, queue manipulation, a few instructions). If a section includes disk
   reads, network waits, or other operations that take on the order of milliseconds, a spinlock
   wastes CPU in a busy-wait loop and is wrong — use a sleep-lock.
2. Check where sleep-locks are used. A sleep-lock (`acquiresleep`/`releasesleep`) allows
   interrupts while held and may call `sleep` internally, so it can yield the CPU. Therefore:
   - Sleep-locks must not be acquired inside interrupt handlers (yields are forbidden there).
   - Sleep-locks must not be acquired while a spinlock is held (the spinlock disables
     interrupts and forbids yields; the sleep-lock would try to do both).
3. Flag a spinlock held across a long or blocking operation, and a sleep-lock used where
   interrupts or yields are forbidden. Very short critical sections where spinning is cheaper
   than a context switch are not a defect.

### Step 5 — Check sleep/wakeup for lost wakeups (pr-008, cl-043, cl-044, cl-045)

1. Locate the condition being waited on and the lock that guards it (the condition lock).
2. Verify that the caller holds the condition lock when it tests the condition. There must be
   no window between the test and the `sleep` call where the condition lock is not held —
   xv6's `sleep` atomically releases the condition lock and marks the process as sleeping, so
   the lock must be passed to `sleep` while it is still held.
3. Verify that the waker holds the condition lock when it modifies the condition and calls
   `wakeup`. This guarantees mutual exclusion between the check-and-sleep and the modify-and-
   wakeup, closing the lost-wakeup window.
4. Verify that `sleep` is called inside a loop that re-tests the condition after returning.
   A single wakeup can wake every process sleeping on the same channel; the others must
   re-test and sleep again. A straight `if` check instead of a `while` loop is a defect.
5. This check applies to producer/consumer patterns using `sleep` and `wakeup` — pipes, disk
   I/O, `wait`/`exit`, and similar. It does not apply to semaphore or futex primitives that
   provide their own lost-wakeup guarantee.

### Step 6 — Check the scheduler p->lock hand-off across swtch (pr-009, cl-040, cl-041, cl-048, cl-049)

1. Locate the yield → swtch → scheduler path. Confirm that `p->lock` is acquired in `yield`
   (or `sleep`) before the process state is changed to anything other than RUNNING, and is
   released in the scheduler thread after the stack has been switched — not in the same thread
   that acquired it. The lock must span the swtch boundary because the invariant it protects
   (process state consistent with the run queue and scheduler's view) is invalid in the
   transient window between state change and stack switch.
2. This hand-off is a deliberate asymmetry: the lock is not released by the same code that
   took it. Flag any implementation where `p->lock` is released before `swtch` in yield, or
   acquired again by the scheduler before the stack is switched.
3. Check the kill/sleep race (cl-048, cl-049). `kill` may set `p->killed` and call `wakeup`
   in the window after the victim process has checked its condition but before it has called
   `sleep`. This is a known structural race in xv6: flag code that calls `kill` without
   holding the victim's condition lock if correctness depends on the victim not missing the
   signal. Recognize that xv6 handles this by having the victim check `p->killed` on wakeup
   in its loop, not by closing the race entirely. This applies only to the yield/scheduler/
   swtch context-switch path; it does not apply to non-preemptive or cooperative-only
   schedulers without per-CPU scheduler threads.

### Step 7 — Recognise lock-like reference-count patterns

A reference count or state flag (such as `p->state`, or the reference counts in `file`,
`inode`, and `buf`) can act as a soft lock keeping an object alive while still in use. When
reviewing code that frees an object whose lock is embedded in it, confirm the free occurs only
after the last reference is gone. A thread blocked in `acquire` on an embedded lock inside a
freed object will malfunction when the lock is recycled or the memory is reused.

### Step 8 — State the verdict per invariant

For each finding, specify:

- The invariant at risk (serialization of a named structure, global lock order, interrupt-
  disable sequencing, barrier placement, held-condition-lock rule, or spin/sleep constraint).
- The code location (function, line, or call sequence) where the invariant is upheld or broken.
- The principle driving the finding (pr-004 through pr-009 as applicable).
- Whether the defect is a race, deadlock, self-deadlock, reordering hazard, lost wakeup, or
  misused lock type.

Do not mark code as correct without pointing to why each relevant invariant is satisfied. Do
not assert a defect from general intuition — every finding must trace to a named principle.

## Inputs

- The kernel code or proposed change under review, and which data it shares across threads,
  CPUs, or with interrupt handlers.
- Which lock is intended to protect each shared structure (or the absence of one).
- The code paths that hold two or more locks, if any.

## Output

A concurrency critique that, for each issue, names:

- The precise invariant at risk and the principle it derives from (pr-004 to pr-009).
- The code location (function name or call sequence) where the invariant is upheld or broken.
- The defect class: race (missing lock on a multi-field invariant), deadlock (out-of-order
  acquisition or self-deadlock), interrupt-deadlock (push_off not before locked flag set),
  reordering hazard (missing barrier), lost wakeup (condition lock gap or no re-test loop),
  wrong lock type (spinlock across a long operation or sleep-lock in a forbidden context), or
  scheduler hand-off violation (p->lock released before swtch boundary).

Never produce an unsupported "looks fine" verdict. If evidence is insufficient to assess an
invariant, say so explicitly.

## References

- `references/xv6-subsystem-map.md` — which lock guards which xv6 subsystem.
- `references/real-world-os-comparisons.md` — where xv6's locking is a teaching simplification
  versus production kernels.

## Provenance

Tier 1. Grounded in principles pr-004 through pr-009 and the underlying claims, distilled from
xv6: a simple, Unix-like teaching operating system (Cox, Kaashoek, Morris) — distillation-only,
no verbatim quotation.

Source sections used:

- §5.1 Race conditions (h0092) — multi-field invariant rationale backing pr-004/cl-029/cl-032
- §5.3 Code: Using locks (h0100) — lock introduction and invariant coverage
- §5.4 Deadlock and lock ordering (h0101) — global ordering requirement backing pr-005/cl-033/cl-034
- §5.5 Locks and interrupt handlers (h0102) — push_off sequencing backing pr-006/cl-035/cl-036
- §5.6 Instruction and memory ordering (h0103) — barrier placement backing pr-006/cl-037
- §5.7 Sleep locks (h0106) — sleep-lock vs spinlock choice backing pr-007/cl-038
- §6.2 Code: Context switching (h0112) — swtch and scheduler structure backing pr-009/cl-040
- §6.3 Code: Scheduling (h0113) — p->lock hand-off backing pr-009/cl-041
- §6.5 Sleep and wakeup (h0115) — lost-wakeup analysis backing pr-008/cl-043/cl-044
- §6.6 Code: Sleep and wakeup (h0128) — condition lock and loop pattern backing pr-008/cl-045
- §6.8 Code: Wait, exit, and kill (h0130) — kill/sleep race backing pr-009/cl-048/cl-049
- §6.9 Real world (h0131) — scope notes on xv6 simplifications
