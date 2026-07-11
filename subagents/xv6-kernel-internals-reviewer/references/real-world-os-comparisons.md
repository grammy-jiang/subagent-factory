---
name: real-world-os-comparisons
kind: reference
status: ready
provenance:
  principles:
  - pr-007
  claims:
  - cl-038
  source_anchors:
  - a-simple-unix-like-t-20260613000613-h0106
  - a-simple-unix-like-t-20260613000613-h0131
  - a-simple-unix-like-t-20260613000613-h0061
  - a-simple-unix-like-t-20260613000613-h0076
  - a-simple-unix-like-t-20260613000613-h0088
  - a-simple-unix-like-t-20260613000613-h0107
  - a-simple-unix-like-t-20260613000613-h0155
  authored_from_digest: 16a996faa0bf293b7ff6087fc2814f6ed54057267b39f154207be81276f21897
---

# Real-world OS comparisons

Where xv6 deliberately simplifies relative to production kernels (Linux, BSD, FreeBSD). Each row
states the xv6 choice, the production alternative as the book describes it, and the trade-off
accepted. Every comparison is framed as a teaching simplification — xv6 is never presented as
production-grade. All rows derive from the book's "Real world" sections; where the book is silent
on a production detail, this table is silent too.

## Simplification table

| Area | xv6 approach | Production alternative (per the book) | Trade-off / what xv6 omits |
|------|-------------|---------------------------------------|---------------------------|
| **Kernel structure** | Monolithic kernel | Also monolithic in Linux; microkernels (L4, Minix, QNX) organise OS functions as user-level servers and are common in embedded settings | xv6's monolith is simpler to follow; microkernels isolate subsystems but add IPC overhead (§2.7) |
| **Threads per process** | One kernel thread per process | Linux `clone` (a `fork` variant) supports multiple kernel threads per process; requires machinery to control what threads share | xv6 avoids that machinery; a single process cannot exploit multiple CPUs in parallel (§2.7) |
| **Virtual memory — demand and copy features** | Straight paging only; no demand paging from disk, no copy-on-write fork, no shared memory, no lazily-allocated pages, no auto-growing stacks, no memory-mapped files | Production kernels provide all of the above | xv6 keeps the VM code small and readable; gives up memory efficiency and on-demand features (§3.9) |
| **Physical-address protection and superpages** | Uses only page-level (`PTE_U`) protection; ignores RISC-V physical-address protection; no superpages | On large-memory machines superpages reduce page-table overhead; RISC-V physical-address protection is available | Simpler allocator; coarser, less efficient mappings on large-memory hardware (§3.9) |
| **Kernel mapped into user page tables** | Separate page tables; trampoline page + page-table switch on every trap; `sfence.vma` each way | Many kernels map the kernel into every user page table, avoiding the switch and allowing direct user-pointer dereference in kernel code | xv6 trades trap efficiency for a lower risk of security bugs from inadvertent user-pointer use and simpler address-space layout (§4.9) |
| **Timer interrupts in the kernel** | Device and timer interrupts enabled in the kernel; a timer interrupt forces `yield` even in a kernel thread | The book notes the kernel could be made simpler if device and timer interrupts only occurred in user code | xv6's choice time-slices kernel threads fairly but means kernel code may be suspended and resume on a different CPU, adding complexity (§4.9) |
| **Lock choice: spinlock vs. sleep-lock** (pr-007) | Two exposed lock types chosen by duration: spinlocks for short critical sections; sleep-locks for long-held sections (e.g., disk I/O in the file system) — sleep-locks yield the CPU and permit interrupts, whereas spinlocks busy-wait and disable interrupts | Production systems typically conceal lock primitives inside higher-level constructs such as synchronized queues; race-detector tooling is recommended | xv6 keeps both primitives visible for teaching. Choosing the wrong type has concrete consequences: holding a spinlock for a long operation wastes CPU; using a sleep-lock inside a spinlock critical section is illegal (§5.7 / §5.8) |
| **Lock-free and scalable locking** | Raw spinlocks and sleep-locks only | Many production systems use lock-free data structures and algorithms (e.g., a linked list requiring only one atomic insertion) to avoid cache-line-contention costs that grow orders of magnitude when many CPUs contend the same lock | xv6 avoids lock-free complexity deliberately; the book notes the added risk of instruction and memory reordering bugs (§5.8) |
| **POSIX threads (Pthreads)** | No user-thread library and no kernel support for it | Most OSes support Pthreads; the OS must ensure a blocking pthread does not stall other threads of the same process, and must propagate address-space changes to all CPUs running threads of that process | xv6 omits the required kernel support; user processes have one thread (§5.8) |
| **Scheduler policy** | Simple round-robin over all runnable processes | Production schedulers add priorities, fairness guarantees, and high-throughput goals; complex policies can produce unintended interactions such as priority inversion and convoy effects, requiring additional mechanisms | xv6's scheduler is easy to reason about but cannot express priority or prevent convoys (§6.9) |
| **Sleep/wakeup and lost-wakeup avoidance** | Explicit condition lock held across the sleep call; wakeup scans the entire process list for matching channel | FreeBSD's `msleep` uses the same lock approach; Plan 9 uses a callback under the scheduling lock; Linux uses per-waitqueue locks with an explicit wait queue rather than a channel scan | xv6's channel scan is O(n) in processes; the book notes that a per-condition wait list (as in Linux) is more efficient (§6.9) |
| **Process-list search** | Linear scan of the process table in `allocproc` and `wakeup` | Production kernels maintain an explicit free list for constant-time allocation | xv6 uses the linear scan for simplicity (§6.9) |
| **Filesystem logging** | Single fixed-location write-ahead log; whole-block logging even when only a few bytes change; synchronous log writes one block at a time; no concurrent commits during file-system calls | Real logging systems support concurrent commits, byte-granularity journalling, checksums, and multiple write modes (ordered, data); early Unix used a reboot-time scavenger (`fsck`) instead | xv6's log is easy to reason about but lower in performance and offers fewer durability modes; `fsck`-style recovery cannot guarantee atomicity for all crash scenarios (§7.15) |
| **Buffer cache** | Simple LRU eviction via a doubly-linked list; not integrated with the VM system | Production buffer caches use a hash table for lookups and a heap for LRU tracking; they are integrated with the VM system to support memory-mapped files | xv6's cache is simpler to follow; lacks mmap integration and is less efficient at scale (§7.15) |
| **Directory lookup** | Linear scan over all disk blocks in a directory | NTFS, HFS, and ZFS implement directories as on-disk balanced trees, giving logarithmic-time lookup | xv6 is reasonable for small directories; expensive for directories with many entries (§7.15) |
| **Disk-failure handling** | Panics on any disk-operation failure | Production systems on unreliable hardware handle failures more gracefully so that a single bad block does not affect the rest of the file system | Acceptable only when hardware redundancy makes failures rare; not safe on commodity disks (§7.15) |
| **System-call interface completeness** | Subset of POSIX; missing calls such as `lseek`; no networking, windowing, user-level threads, or most device drivers | Modern kernels provide a much larger set of system calls and kernel services; the Unix interface is standardised through POSIX | xv6 targets simplicity and clarity; it is not POSIX-compliant (§1.5) |

## How to use this table

1. Name the xv6 mechanism and the exact simplification or omission.
2. State the production alternative only as the book describes it — do not extend claims beyond the source.
3. Name the trade-off xv6 accepts (usually simplicity and readability versus performance, features, or safety).
4. Never describe an xv6 simplification as production-ready; flag the gap explicitly.
5. For any lock-choice row, apply pr-007: the correct type depends on operation duration — spinning for short sections, sleeping for long ones.

## Provenance

Distillation-only source (paraphrased; no verbatim quotation). All rows derived from the "Real
world" sections of *xv6: a simple, Unix-like teaching operating system* (Cox, Kaashoek, Morris):

- §1.5 Real world — system-call interface and POSIX gap
  (anchor `a-simple-unix-like-t-20260613000613-h0052`, section reached via §1.5 prose before h0052)
- §2.7 Real world — kernel structure, threads per process
  (anchor `a-simple-unix-like-t-20260613000613-h0061`)
- §3.9 Real world — paging features omitted, superpages, physical-address protection
  (anchor `a-simple-unix-like-t-20260613000613-h0076`)
- §4.9 Real world — trampoline / page-table switch, timer interrupts in kernel
  (anchor `a-simple-unix-like-t-20260613000613-h0088`)
- §5.7 Sleep locks — spinlock vs. sleep-lock selection criterion (pr-007 / cl-038)
  (anchor `a-simple-unix-like-t-20260613000613-h0106`)
- §5.8 Real world — lock concealment, race-detector tooling, lock-free structures, Pthreads
  (anchor `a-simple-unix-like-t-20260613000613-h0107`)
- §6.9 Real world — scheduling policy, sleep/wakeup variants, process-list scan
  (anchor `a-simple-unix-like-t-20260613000613-h0131`)
- §7.15 Real world — buffer cache, logging efficiency, directory lookup, disk failures
  (anchor `a-simple-unix-like-t-20260613000613-h0155`)
