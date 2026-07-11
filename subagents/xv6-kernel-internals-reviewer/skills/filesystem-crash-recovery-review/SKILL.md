---
name: filesystem-crash-recovery-review
kind: skill
status: ready
provenance:
  principles:
  - pr-010
  - pr-011
  - pr-012
  claims:
  - cl-050
  - cl-054
  - cl-056
  - cl-065
  - cl-058
  - cl-060
  - cl-061
  - cl-066
  source_anchors:
  - a-simple-unix-like-t-20260613000613-h0137
  - a-simple-unix-like-t-20260613000613-h0140
  - a-simple-unix-like-t-20260613000613-h0142
  - a-simple-unix-like-t-20260613000613-h0154
  - a-simple-unix-like-t-20260613000613-h0148
  - a-simple-unix-like-t-20260613000613-h0149
  - a-simple-unix-like-t-20260613000613-h0159
  authored_from_digest: 655c6d5af27e0124996c0ed4a3ba8938b9ee36ad31a58e1eda12c32acf2feee1
---

# Filesystem crash-recovery review

## Purpose

Explain or critique the xv6 filesystem as a stack of seven layers and verify that its
crash-recovery guarantee actually holds: a power failure mid-operation must leave on-disk
structures consistent because the logging layer commits a group of writes atomically. Every
durability or consistency claim must be traced to the specific layer that provides it, not
assumed to hold by default.

## When to use

- A reader needs the seven-layer xv6 filesystem design (disk, buffer cache, logging, inode,
  directory, pathname, file-descriptor) explained or mapped to concrete code and on-disk layout.
- A reviewer must judge whether a filesystem change preserves crash consistency — whether its
  disk writes are wrapped in a transaction that commits all-or-nothing.
- Someone must explain why a partially completed multi-block operation cannot leave the disk in
  a corrupt intermediate state.
- A reviewer must check inode cache concurrency: ref-count discipline, per-inode locking, and
  nlink protection.

## Procedure

### Step 1 — Place the change in the layer stack (pr-010, cl-050)

The filesystem is built from seven layers, each invoking only the one directly below it:

| Layer | Role |
|---|---|
| Disk | Raw sector read/write via the virtio driver |
| Buffer cache | One in-memory copy per block; serialises access |
| Logging | Write-ahead log; crash-atomicity for groups of writes |
| Inode | On-disk file metadata and content block pointers |
| Directory | Inode whose data are name-to-inumber mappings |
| Pathname | Recursive directory lookup for path strings |
| File-descriptor | Uniform interface over files, pipes, and devices |

Identify which layer the code under review lives in, because the invariant it must uphold
depends on the layer. Also locate it in the on-disk layout: block 0 (boot), block 1
(superblock — sizes, inode count, log location), then the log region, then inode blocks, then
the free-block bitmap, then data blocks. Flag any layer skip — code in the inode layer calling
disk primitives directly, for example, is an architectural violation.

### Step 2 — Check buffer-cache invariants

The buffer cache holds a fixed number of in-memory block copies. Its two jobs are: keeping at
most one cached copy of each block (so all paths share one consistent view), and serialising
access so only one kernel thread holds a given block at a time. `bread` returns a locked
buffer; `brelse` releases it and marks it most-recently-used.

Check these:
- Every read or write uses `bread`/`brelse`, holding the buffer across the entire use.
- No code assumes two separate `bread` calls for the same block return independent copies.
- The cache eviction path recycles only unlocked, unreferenced (`b->refcnt == 0`) buffers.

Flag any code that reads or writes a block without the buffer locked, or that holds a buffer
reference longer than necessary without eventually calling `brelse`.

### Step 3 — Check that writes go through a transaction (pr-011, cl-054, cl-056)

Every multi-block update that must survive a crash atomically must be bracketed by
`begin_op()` and `end_op()`, with all block modifications going through `log_write` rather
than `bwrite` directly.

What `log_write` does: it records the block's sector number, reserves the block a slot in the
in-memory log, and pins the buffer in the cache so it cannot be evicted before commit. Until
the transaction commits, the cached (modified) copy is the only record of the change — the
real disk block still holds the pre-transaction data.

Check these:
- Every operation that modifies more than one semantically related block is wrapped in
  `begin_op` / `end_op`.
- All block writes inside that bracket go through `log_write`, not `bwrite`.
- The total number of `log_write` calls the operation can issue does not exceed the budget
  declared at `begin_op` time (conservatively `MAXOPBLOCKS` per call).

Flag: any `bwrite` inside a transaction bracket (bypass of the log), any operation that
modifies disk state outside any transaction, any operation that may write more blocks than the
log can hold.

### Step 4 — Verify the commit/recovery argument (pr-011, cl-065)

The log occupies a fixed region named in the superblock. It has a header block — an array of
sector numbers plus a block count — followed by the logged block copies. The count field is
the commit point: zero means no committed transaction; non-zero means a complete committed
transaction of that many blocks.

The correct write order is:
1. Write all modified block data into the log's data region (logged copies on disk).
2. Write the header block with the real sector numbers and a non-zero count (this is the
   commit point — it must be a single disk write to be atomic at the hardware level).
3. Copy each logged block from the log region to its real home location (install).
4. Write a zero count to the header (clear the log).

Recovery after a crash: if the header count is non-zero, replay all logged blocks to their
home locations (idempotent — safe to repeat), then zero the count. If the count is zero,
skip. Either way the operation is atomic: a crash before the commit write leaves no committed
record; a crash after leaves a complete record that recovery can finish.

Check these:
- The header is written (commit) only after all logged block copies are safely on disk.
- Installation to real home locations happens only after the commit write.
- The log-clear write (zeroing the count) happens only after all installs are complete.

Flag any ordering that could let a partial write reach a real block before the commit record
is written, or that writes the header before the log's data region is flushed.

### Step 5 — Check log concurrency and absorption (pr-011, cl-054, cl-056)

`begin_op` waits until the system is not currently committing, and until enough unreserved log
space remains. The field `log.outstanding` both reserves space and prevents a commit from
starting while any operation is still writing. Each caller conservatively reserves
`MAXOPBLOCKS` blocks.

The absorption optimisation: if `log_write` is called for a block that already has a log slot
in the current transaction, it reuses that slot rather than allocating a new one. This means
a block written many times in one transaction uses only one log slot. Bypassing the cache
(writing through `bwrite` directly) defeats absorption and may cause the log to overflow.

Check these:
- `log.outstanding` is incremented in `begin_op` and decremented in `end_op` before the
  commit check.
- No path allows a commit to begin while `log.outstanding > 0`.
- No transaction writes more distinct blocks than the log region can hold.
- Absorption is not defeated by writing the same block outside `log_write`.

### Step 6 — Check inode-layer concurrency (pr-012, cl-058, cl-060, cl-061, cl-066)

The inode layer uses a two-level locking pattern. At the coarse level, `icache.lock` (a
spinlock) guards the in-memory inode cache: its membership, slot allocation, and the `ref`
count of each entry. At the fine level, each inode has its own sleep-lock (`ip->lock`) that
serialises access to that inode's fields and its on-disk content.

The correct sequence for obtaining an inode is:
1. Acquire `icache.lock`.
2. Find or allocate a cache slot; increment `ip->ref` before releasing `icache.lock` — this
   prevents the slot from being evicted in the window between pointer acquisition and locking.
3. Release `icache.lock`.
4. Call `ilock(ip)` to acquire the per-inode sleep-lock before reading or modifying any inode
   fields (type, size, addrs, nlink).

The `nlink` field on the disk inode counts how many directory entries point to the inode.
Deallocation (`iput` → `itrunc` → `ifree`) must only proceed when both `ip->ref == 0` (no
in-memory user) and `ip->nlink == 0` (no directory entry).

**Known limitation — orphaned inodes:** If a process holds the last reference to an inode
(`ref == 1, nlink == 0`) and a crash occurs before `iput` writes the inode to disk as free,
the inode's blocks remain allocated permanently after recovery. xv6 does not implement
orphan-inode recovery (unlike ext3/ext4, which maintain an orphan list in the superblock).
This is a documented design limitation, not a correctness bug in the logging layer, but
reviewers must disclose it when evaluating durability guarantees.

Check these:
- `iget` increments `ref` before releasing `icache.lock`.
- `ilock` is called before any field read or write on the returned inode.
- `iunlock` releases `ip->lock`; `iput` decrements `ref` (and conditionally `itrunc`/`ifree`
  when both `ref` and `nlink` drop to zero).
- `icache.lock` is not held when calling `ilock` (coarse lock released before fine lock
  is acquired long-term).
- `nlink` is decremented (in a transaction) before `iput` drops the last ref.
- Code that may create the ref=1/nlink=0 state and then crash is documented as subject to the
  orphan-inode limitation.

### Step 7 — Check upper-layer invariants

The directory layer stores name-to-inumber pairs inside an ordinary inode. The pathname layer
resolves slash-separated paths by iteratively looking up each component, releasing the current
directory's lock before acquiring the next to avoid self-deadlock on paths like `a/./..`. The
file-descriptor layer presents a uniform `struct file` abstraction over inodes, pipes, and
devices, with its own `ref` count protected by `ftable.lock`.

Check these:
- Directory modifications (adding or removing entries) are done inside a transaction and under
  `ilock` on the directory inode.
- Pathname resolution releases each component's inode lock before calling `ilock` on the
  next directory.
- File-descriptor creation (`filealloc`) and duplication (`filedup`) increment `f->ref` under
  `ftable.lock`; `fileclose` decrements it and calls `iput` only when `ref` reaches zero.

### Step 8 — State the verdict per layer invariant

For each finding, name:
1. The layer (buffer cache, logging, inode, directory, pathname, file-descriptor).
2. The specific invariant (single locked copy, writes inside transaction, commit-ordering,
   log-space budget, absorption not bypassed, two-level inode locking, nlink protection).
3. Whether the code upholds or violates it, and where.
4. If the orphan-inode limitation is relevant, state it explicitly rather than calling it a
   crash-recovery failure of the logging layer.

Never claim a write is durable without tracing it to a committed log entry.

## Inputs

- The filesystem code or change under review, with the layer it touches identified.
- Whether the disk writes must be crash-atomic (multi-block) or are single-block.
- Whether the code touches the inode cache (iget/ilock/iput/iunlock paths).

## Output

A layered review with one finding section per invariant category:
- **Layer placement** — correct layer or layer-skip violation.
- **Buffer-cache discipline** — bread/brelse pairing and single-copy guarantee.
- **Transaction discipline** — begin_op/end_op bracket, log_write usage, block budget.
- **Commit ordering** — log data before header; install after commit; clear after install.
- **Log concurrency** — outstanding counter, absorption, no commit during active ops.
- **Inode concurrency** — two-level locking, ref-before-release, nlink protection.
- **Orphan-inode exposure** — whether the change creates or worsens the known limitation.
- **Upper-layer invariants** — directory transaction discipline, pathname lock ordering,
  file-descriptor ref counting.

Each finding names the invariant, the code location, and the verdict (upheld / violated /
limitation disclosed). Never assume durability; trace it to the log.

## References

- `references/xv6-subsystem-map.md` — filesystem layer stack, on-disk layout, and lock table.
- xv6 source book, §7.1 Overview (seven-layer model and on-disk layout).
- xv6 source book, §7.4 Logging layer and §7.6 Code: logging (begin_op/end_op, log_write,
  commit sequence, recovery).
- xv6 source book, §7.8 Inode layer and §7.9 Code: Inodes (iget/ilock/iput, two-level
  locking, nlink, orphan limitation).
- xv6 source book, §7.14 Code: System calls (how syscalls compose the layers).
- xv6 source book, §8.1 Locking patterns (two-level cache locking discipline).

## Provenance

Grounded in pr-010 (cl-050): seven-layer filesystem model; each layer invokes only the one
below it (§7.1 Overview). Grounded in pr-011 (cl-054, cl-056, cl-065): write-ahead logging
atomicity via begin_op/end_op, log_write, commit-record ordering, replay-or-discard recovery,
and absorption not bypassed (§7.4 Logging layer; §7.6 Code: logging; §7.14 Code: System
calls). Grounded in pr-012 (cl-058, cl-060, cl-061, cl-066): inode-cache two-level locking
(icache.lock + per-inode sleep-lock), iget ref-before-release discipline, nlink protection,
and the documented orphan-inode limitation after crash (§7.8 Inode layer; §7.9 Code: Inodes;
§8.1 Locking patterns). Source: "xv6: a simple, Unix-like teaching operating system" (Cox,
Kaashoek, Morris) — distillation-only, paraphrased, no verbatim quotation.
