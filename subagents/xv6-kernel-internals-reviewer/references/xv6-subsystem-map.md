---
name: xv6-subsystem-map
kind: reference
status: ready
provenance:
  principles:
  - pr-001
  - pr-002
  - pr-003
  - pr-004
  - pr-005
  - pr-006
  - pr-008
  - pr-009
  - pr-010
  - pr-011
  - pr-012
  claims:
  - cl-011
  - cl-013
  - cl-020
  - cl-024
  - cl-027
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
  - cl-050
  - cl-054
  - cl-056
  - cl-058
  - cl-060
  - cl-061
  - cl-065
  - cl-066
  source_anchors:
  - a-simple-unix-like-t-20260613000613-h0056
  - a-simple-unix-like-t-20260613000613-h0059
  - a-simple-unix-like-t-20260613000613-h0070
  - a-simple-unix-like-t-20260613000613-h0082
  - a-simple-unix-like-t-20260613000613-h0092
  - a-simple-unix-like-t-20260613000613-h0101
  - a-simple-unix-like-t-20260613000613-h0106
  - a-simple-unix-like-t-20260613000613-h0113
  - a-simple-unix-like-t-20260613000613-h0115
  - a-simple-unix-like-t-20260613000613-h0137
  - a-simple-unix-like-t-20260613000613-h0140
  - a-simple-unix-like-t-20260613000613-h0148
  authored_from_digest: 3265aa38a08c619e3ad4210d1bf19ac441e26b4e30b87522fc7bfdae05799c0d
---

# xv6 Subsystem Map

A lookup table from each xv6 kernel subsystem to the governing principle, key mechanism,
invariant to check, and source section. Use it to anchor a review judgement to a concrete
subsystem and principle rather than general OS folklore.

## Subsystem map

| Subsystem | Key mechanism | Invariant to check | Governing principles | Source section |
| --- | --- | --- | --- | --- |
| Process / kernel organization | `proc.c`: `p->state`, `p->pagetable`, `p->kstack`; ecall as the sole kernel-entry point | Each process has a private page table and a kernel stack isolated from user code; the isolation triple (ecall entry, private page table, time-sliced scheduling) must be intact | pr-001 (cl-011, cl-013) | §2.5 Process overview |
| Page tables / address space | `vm.c`: `walk`, `mappages`, `kvminit`, `uvmalloc`, `copyin`/`copyout`; Sv39 three-level page-table walk | PTE flags (`V/R/W/X/U`) are set correctly; TLB is flushed (`sfence.vma`) on every page-table change; guard pages remain unmapped | pr-001 | §3.6 Process address space |
| `exec` / program loading | `exec.c`: `loadseg`, `walkaddr`; ELF segment mapping into the process page table | ELF segments load into the process page table only; `vaddr + memsz` cannot overflow into kernel memory; the old image is freed only on success | pr-001, pr-003 | §3.6 Process address space |
| Traps / syscall entry-exit | `trampoline.S`, `trap.c`; RISC-V registers `stvec`, `sepc`, `scause`, `satp`; uservec → usertrap → usertrapret → userret sequence | Trap enters via the trampoline (mapped identically in every address space); switches to kernel stack and kernel page table before any user data is touched; user-pointer arguments are validated through `copyinstr`/`copyin`, never dereferenced directly | pr-002 (cl-020, cl-024), pr-003 (cl-027) | §2.2 User mode, supervisor mode, and system calls; §4.3 Traps from user space |
| Locking — spinlocks | `spinlock.c`: `acquire`/`release`; `amoswap` hardware atomic; `__sync_synchronize()` barriers; `push_off`/`pop_off` interrupt discipline | `push_off` called strictly before `lk->locked` is set; memory barriers present in both `acquire` and `release`; no spinlock held across a sleep or blocking call; shared data serialized by a lock that covers the complete multi-field invariant | pr-004 (cl-029, cl-032), pr-005 (cl-033, cl-034), pr-006 (cl-035, cl-036, cl-037, cl-038) | §5.1 Race conditions; §5.4 Deadlock and lock ordering |
| Locking — sleep-locks | `sleeplock.c`: `acquiresleep`/`releasesleep`; backed by a spinlock and a sleep call | Sleep-locks used only outside interrupt handlers and outside spinlock critical sections; spinlocks used only where the critical section is short enough to spin | pr-006, pr-007 (cl-038) | §5.7 Sleep locks |
| Sleep / wakeup | `proc.c`: `sleep`, `wakeup`; condition lock passed into `sleep` | Caller holds the condition lock when checking the condition and when calling `sleep` (atomically released on entry); `sleep` called inside a loop that re-tests the condition after waking | pr-008 (cl-043, cl-044, cl-045) | §6.5 Sleep and wakeup |
| Scheduling / context switch | `proc.c`: `swtch`, `scheduler`, `sched`, `yield`; per-CPU scheduler thread | `p->lock` is acquired in `yield` (before state change) and released in the scheduler (after stack switch), never in the same thread; a switched-out thread may resume on another CPU; known kill/sleep race: `kill` may set `p->killed` in the window between the victim's condition check and its `sleep` call | pr-009 (cl-040, cl-041, cl-048, cl-049) | §6.3 Code: Scheduling |
| Buffer cache | `bio.c`: `bget`, `bread`, `bwrite`, `brelse`; LRU recycle; `bcache.lock` plus per-buffer sleep-lock | At most one cached copy of any disk block; only one thread per buffer (locked by `bread`); LRU recycling releases the least-recently-used unlocked buffer | pr-004, pr-005 | §7.1 Overview (buffer-cache layer) |
| Logging / crash recovery | `log.c`: `begin_op`, `log_write`, `end_op`; write-ahead log; header block as commit point; recovery on boot | Every multi-block operation wrapped in `begin_op`/`end_op`; all writes go to the log first; the header count is written last as the commit record; recovery replays only a complete log; `log_write` absorption (multiple writes to the same block in one transaction coalesce) must not be bypassed | pr-011 (cl-054, cl-056, cl-065) | §7.4 Logging layer |
| Inode cache | `fs.c`: `ialloc`, `iget`, `ilock`, `iunlock`, `iput`, `readi`/`writei`; `icache.lock` (coarse) plus per-inode sleep-lock `ip->lock` (fine) | `icache.lock` guards cache membership and ref counts; `iget` increments ref before releasing `icache.lock` so the inode cannot be evicted between pointer acquisition and locking; `ilock` acquires the per-inode sleep-lock before touching fields; `nlink` count prevents disk deallocation while directory entries exist; xv6 does not recover orphaned inodes (`nlink==0`, `ref>0`) after a crash — known limitation | pr-010 (cl-050), pr-012 (cl-058, cl-060, cl-061, cl-066) | §7.8 Inode layer |
| Directories / pathnames | `fs.c`: `dirlookup`, `namex`; directory as a special inode of name-to-i-number entries | `namex` releases each component's inode lock before acquiring the next to avoid self-deadlock; directory lookup resolves through the inode and logging layers below it | pr-005, pr-010 | §7.1 Overview (directory and pathname layers) |
| File descriptors | `file.c`: `fileread`, `filewrite`; `ftable.lock`; reference count | Files, pipes, and devices share one uniform interface; reference count guards the lifetime of the underlying resource | pr-010 | §7.1 Overview (file-descriptor layer) |

## Lock-to-serialization index

| Lock | Serializes | Source section |
| --- | --- | --- |
| `kmem.lock` | Physical memory allocation (free list) | §2.5 Process overview |
| `p->lock` (per process) | Changes to a process's state fields across swtch boundary | §6.3 Code: Scheduling |
| `pid_lock` | Increment of `next_pid` | §5.1 Race conditions |
| `tickslock` | Operations on the ticks counter | §5.1 Race conditions |
| `cons.lock` | Console hardware access — prevents interleaved output | §5.4 Deadlock and lock ordering |
| `bcache.lock` | Allocation and recycling of block-buffer-cache entries | §7.1 Overview |
| `buf`'s `b->lock` (sleep-lock) | Operations on each individual block buffer | §5.7 Sleep locks |
| `log.lock` | Operations on the in-memory transaction log | §7.4 Logging layer |
| `icache.lock` | Allocation of inode-cache entries and ref-count changes | §7.8 Inode layer |
| `ip->lock` (per inode, sleep-lock) | Operations on each inode and its content | §7.8 Inode layer |
| `ftable.lock` | Allocation of a `struct file` in the global file table | §7.1 Overview |
| pipe's `pi->lock` | Operations on each pipe's buffer and state | §6.5 Sleep and wakeup |
| `vdisk_lock` | Disk hardware access and the queue of DMA descriptors | §5.1 Race conditions |

## Global lock ordering (filesystem path)

To avoid deadlock, xv6 acquires multiple locks in this consistent order when a single
operation needs more than one (pr-005, cl-033, cl-034):

> directory inode lock → child inode lock → buffer lock → `vdisk_lock` → `p->lock`

Any code path that acquires these locks in a different order is a deadlock candidate.

## Provenance

Tier 1. Derived by distillation from *xv6: a simple, Unix-like teaching operating system*
(Cox, Kaashoek, Morris, 2019) — distillation-only rights; all content paraphrased, no verbatim
quotation. Governing principles pr-001 through pr-012 are the evidence-backed distillation of
that source. Source anchors span: §2.2 User mode, supervisor mode, and system calls
(h0056); §2.5 Process overview (h0059); §3.6 Process address space (h0070); §4.3 Traps from
user space (h0082); §5.1 Race conditions (h0092); §5.4 Deadlock and lock ordering (h0101);
§5.7 Sleep locks (h0106); §6.3 Code: Scheduling (h0113); §6.5 Sleep and wakeup (h0115);
§7.1 Overview (h0137); §7.4 Logging layer (h0140); §7.8 Inode layer (h0148).
