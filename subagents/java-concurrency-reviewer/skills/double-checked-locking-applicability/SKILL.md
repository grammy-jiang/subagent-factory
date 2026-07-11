---
name: double-checked-locking-applicability
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Double-Checked Locking Applicability

## Purpose

Double-checked locking (DCL) tries to avoid synchronizing on the common path by testing a field,
synchronizing only if it looks unset, and testing again inside the lock. It is notoriously
unsafe for general lazy initialization. This skill decides where DCL is actually safe — only for
monotonic or set-once values, and only with the right memory-visibility guarantee — and what to
use instead.

## When to use

- Code lazily initializes a shared field and uses a check–synchronize–recheck idiom to skip
  locking on the hot path.
- A reviewer must judge whether a DCL on a `singleton`/cache field is correct.
- A team wants to reduce synchronization on a frequently read, rarely written field.

## Procedure

1. **Identify the pattern.** DCL reads a field without a lock; if it appears unset, it enters a
   synchronized block and re-reads; if still unset, it constructs and assigns. Flag every such
   double-test on a shared field.
2. **Reject DCL for general lazy construction without a visibility guarantee.** Without the right
   memory-model support, a reader on the unlocked path can see a non-null reference to a
   partially constructed object: the reference is published before the constructor's writes are
   visible. This is the classic broken DCL.
3. **Allow DCL only for monotonic / set-once values, with the correct guarantee.** It is safe
   when the field transitions once (null → final value) and never back, AND the field carries the
   needed happens-before edge: declare it `volatile` (correct on J2SE 5.0+ memory model), or the
   value is immutable so a partially constructed view is impossible.
4. **Prefer alternatives that are correct by construction.** For a singleton, the
   initialization-on-demand holder idiom (a static nested class initialized by the classloader)
   gives lazy, thread-safe init with no explicit locking. For set-once references, an atomic
   compare-and-set publishes safely. Recommend these over hand-rolled DCL.
5. **Verify the value is truly write-once.** If the field can be reset or updated more than once,
   DCL is invalid regardless of `volatile`; require full synchronization or an optimistic
   compare-and-set instead.
6. **Confirm the target Java version.** On pre-J2SE-5.0 memory models, `volatile` did not provide
   the ordering DCL needs; treat DCL as unsafe there and use the holder idiom or plain
   synchronization.

## Inputs

- The field, whether it is set once or mutated repeatedly, whether the constructed object is
  immutable, the `volatile` modifier's presence, and the Java version.

## Output

A verdict: DCL safe (set-once + `volatile`/immutable on J2SE 5.0+) or unsafe (general lazy init,
non-`volatile`, resettable field, or old memory model), with the recommended correct alternative
(holder idiom, atomic set-once, or full synchronization).

## References

- `references/volatile-usage-rules.md` — what `volatile` does and does not guarantee.
- `references/concurrency-pattern-taxonomy.md` — lazy-initialization patterns.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` DCL entry (safe only for monotonic
or set-once variables, not general lazy init), the `always_on` `volatile` semantics and
memory-model rules, and the `quality_bar`/`forbidden_behaviours` constraints on `volatile`;
synthesized against the source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997,
initialization / memory-model material) with the J2SE 5.0 `volatile` correction noted. No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` source).
