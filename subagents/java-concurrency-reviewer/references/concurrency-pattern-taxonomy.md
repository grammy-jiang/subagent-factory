---
name: concurrency-pattern-taxonomy
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Concurrency Pattern Taxonomy

A selection map across the three families of design approach used by this reviewer: make state
**safe without locking** (immutability/confinement), make it **safe under locking**
(exclusion/synchronization), and keep threads **live** (coordination and liveness techniques).
Use it to name the applicable pattern for a finding or recommendation.

## Set 1 — Safety without locks (avoid sharing)

| Pattern | What it does | Use when | Caveat |
|---------|--------------|----------|--------|
| Immutability | State never changes after construction; always safe and live with no lock | Value objects, configuration, published snapshots | All fields effectively final; no escape during construction |
| Confinement / `ThreadLocal` | Each thread owns its own copy; no shared state to guard | Per-thread context, non-shareable reusable objects | Remove in pooled threads; never leak the instance |
| Copy / snapshot | Hand out a copy so readers never touch live state | Read-mostly exposure of mutable data | Copy cost; copy is stale once taken |

## Set 2 — Safety under locks (exclusion)

| Pattern | What it does | Use when | Caveat |
|---------|--------------|----------|--------|
| Fully synchronized object | Every method synchronized; one lock serializes all access | Small objects with simple invariants | Unsynchronized methods still run during the lock; contention bottleneck |
| Reduced lock scope / split synchronization | Lock only the shared access; separate locks for independent fields | Coarse lock is a bottleneck | Keep compound operations atomic; preserve cross-field invariants |
| Optimistic methods | Read–compute–commit via compare-and-set, retry on conflict | High read contention, set-once/replace updates | Bound retries (livelock); guard ABA |
| Double-checked locking | Skip the lock on the common path | Set-once/monotonic field, `volatile` (J2SE 5.0+) | Unsafe for general lazy init; prefer holder idiom |

## Set 3 — Liveness and coordination

| Pattern | What it does | Use when | Caveat |
|---------|--------------|----------|--------|
| Guarded suspension | Wait in a `while` loop until a precondition holds | Method must block for a state | Lock held; `notifyAll` on every state change |
| Bounded buffer / producer–consumer | Block on full/empty with `put`/`take` or fail-fast `offer`/`poll` | Hand-off between producers and consumers | Notify the opposite side; minimal critical section |
| Resource ordering | Acquire multiple locks in one global order | Method locks 2+ objects | Use a stable key (`identityHashCode`); tie-break |
| Open call | Release your lock before calling another object | Synchronized call into another object | Re-validate state after reacquiring |
| Latches / barriers | Count-based rendezvous for group phases | Parallel phased algorithms | Handle a missing party (timeout/broken) |
| Thread-per-message vs. worker pool | New thread per task vs. reused pool | Latency-bound vs. throughput-bound work | Bound the pool/queue; no fairness guarantee |

## How to use

- A **safety** finding (race, atomicity, visibility) → choose from Set 1 (eliminate sharing) before
  Set 2 (lock it); immutability/confinement is cheaper than correct locking.
- A **liveness** finding (deadlock, lockout, livelock, starvation) → Set 3: resource ordering for
  deadlock, open call for lockout, bounded retry for livelock, fairness/confinement for starvation.
- A **design/compare** question → name the specific pattern and the deciding property, never
  generic "use locks".

## Provenance

Tier 0. Derived from the profile `knowledge_partition` skills/references and `always_on` rules
(immutability, confinement, fully-synchronized objects, `volatile`, deadlock/liveness taxonomy,
Executor framework) and the `quality_bar` requirement that recommendations name a specific pattern;
synthesized against the source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997,
pattern organization). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
