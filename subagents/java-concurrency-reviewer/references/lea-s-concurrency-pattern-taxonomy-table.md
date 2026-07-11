---
name: lea-s-concurrency-pattern-taxonomy-table
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Lea's Concurrency Pattern Taxonomy Table

A single compact table organizing the design patterns by the three problems they solve — exclusion
(keep state consistent), state-dependent action (act only when ready), and structure/flow
(organize the threads). It complements `concurrency-pattern-taxonomy.md` (which groups by
safe-without-locks / safe-under-locks / liveness); this table is the at-a-glance lookup by intent.

## Pattern table

| Set | Pattern | Intent | Mechanism | Apply when |
|-----|---------|--------|-----------|-----------|
| Exclusion | Immutability | No state to protect | Final fields, no mutation after construction | Value/config objects, snapshots |
| Exclusion | Confinement / `ThreadLocal` | No sharing to protect | Per-thread ownership | Per-thread context, non-shareable reusables |
| Exclusion | Fully synchronized object | Serialize all access | One lock, all methods synchronized | Small objects, simple invariants |
| Exclusion | Reduced scope / split sync | Lock less, contend less | Narrow blocks; separate locks per field | Coarse lock is a bottleneck |
| Exclusion | Optimistic methods | Avoid holding a lock | Read–compute–CAS–retry | High read contention, replace-value updates |
| State-dependent | Guarded suspension | Wait until ready | `while`-condition `wait` + `notifyAll` | Method must block for a state |
| State-dependent | Bounded buffer | Block on full/empty | `put`/`take` + `offer`/`poll` | Producer–consumer hand-off |
| State-dependent | Latches / barriers | Group rendezvous | Count-down / cyclic barrier | Parallel phased algorithms |
| Structure / flow | Thread-per-message | Start work now | New thread per request | Latency-bound, bounded volume |
| Structure / flow | Worker thread pool | Reuse threads | Bounded pool + queue | Throughput-bound, high-rate short tasks |
| Structure / flow | Resource ordering | Prevent deadlock | One global lock order | Method locks 2+ objects |
| Structure / flow | Open call | Prevent lockout | Release lock before outbound call | Synchronized call into another object |

## How to read it

- Start from the **problem** column (Set): consistency → Exclusion; "act only when ready" →
  State-dependent; "how are threads organized" → Structure/flow.
- Within a set, choose the cheapest pattern that holds: avoid sharing (immutability/confinement)
  before locking; lock narrowly before locking broadly; block correctly before spawning freely.
- Cross-reference the matching skill for the procedure and `concurrency-pattern-taxonomy.md` for the
  safety-vs-liveness grouping and caveats.

## Provenance

Tier 0. Derived from the profile `knowledge_partition` skills/references and `always_on` rules,
organized by problem type to mirror Lea's pattern structure; synthesized against the source (Doug
Lea, *Concurrent Programming in Java*, Addison-Wesley 1997, pattern organization). Complements
`concurrency-pattern-taxonomy.md`. No principle/claim layer at this tier; not drift-tracked.
Paraphrased — no verbatim quotation (`distillation-only` source).
