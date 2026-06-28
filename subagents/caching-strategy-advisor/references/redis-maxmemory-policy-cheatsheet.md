---
name: redis-maxmemory-policy-cheatsheet
kind: reference
status: ready
provenance:
  principles:
  - P003
  claims:
  - C00041
  - C00042
  - C00043
  - C00044
  - C00045
  - C00050
  evidence:
  - E00019
  - E00020
  - E00021
  - E00022
  - E00023
  - E00024
  source_anchors:
  - 11ebbc818b96-c0001
  authored_from_digest: 2a28c7758ae390d9c5d46f2391dc8e4c98ac461462223c7997732d9f4a88f3d5
---

# Redis `maxmemory-policy` Cheatsheet

By default, when a Redis instance reaches its memory limit, further writes fail. Setting
`maxmemory-policy` enables automatic key eviction instead. The right policy depends on the
observed access-pattern distribution of the application; measurement or trial is often required
to identify the best fit (c026).

## Policy Reference Table

| Policy | Eviction scope | Algorithm | Best fit |
|---|---|---|---|
| `noeviction` | None — writes that need memory return errors | — | Permanent cache; working dataset fits entirely in memory |
| `allkeys-lru` | Any key | Least recently used (sampled approx.) | Recency-skewed workload: a smaller hot subset is accessed far more often than the rest |
| `allkeys-lfu` | Any key | Least frequently used (sampled approx.) | Frequency-skewed workload: the same items recur over long time windows |
| `volatile-lru` | Only keys with a TTL set | Least recently used (sampled approx.) | Mixed dataset: some keys must never be evicted; evictable keys carry explicit TTLs |
| `volatile-lfu` | Only keys with a TTL set | Least frequently used (sampled approx.) | Mixed dataset with long-window frequency skew; evictable keys carry explicit TTLs |
| `allkeys-random` | Any key | Random | Not recommended for production (see note below) |
| `volatile-random` | Only keys with a TTL set | Random | Not recommended for production (see note below) |
| `volatile-ttl` | Only keys with a TTL set | Shortest remaining TTL first | Eviction aligned with natural data expiry |

## TTL-Based Eviction: Per-Key EXPIRE

TTL eviction in Redis operates at the individual key level, not at the `maxmemory-policy`
level. Assign an expiration to a key with the `EXPIRE` command; Redis removes that key
automatically when the period elapses, regardless of whether the cache is full (c023). Common
use case: session management, where the TTL represents the idle-logout window and is refreshed
on each user interaction.

`volatile-*` policies use per-key TTL as the eligibility criterion: only keys that carry an
expiration are candidates for eviction. If no eligible key exists when memory is exhausted,
these policies fall back to `noeviction` behaviour and writes can fail. Use an `allkeys-*`
policy when every key must remain evictable (c029).

## Notes

**Approximation algorithms.** Redis LRU and LFU eviction are statistical approximations, not
exact global rankings. When a key must be evicted, Redis samples a small set of keys and
removes the least-recently-used or least-frequently-used candidate from that sample rather than
scanning the entire keyspace. This trades a small reduction in eviction accuracy for a
significant reduction in memory overhead. The sample size is tunable: increasing it improves
eviction accuracy at the cost of additional CPU work (c030).

**Random eviction.** Random policies are straightforward to implement and fast to execute, but
they are more likely to evict still-needed keys, leading to elevated miss rates. They are not
typically used in production; one of the algorithmic policies (LRU, LFU, or TTL-based) almost
always performs better in practice (c026).

**Policy choice is situation-dependent.** Neither LRU nor LFU is universally superior. The
appropriate selection depends on the access-distribution shape of the specific workload.
Analysing actual access patterns — or running a controlled trial — is the recommended approach
when the distribution is not known in advance (c026).

> Redis policy names and sampling parameters are version-specific. Verify exact option names
> and current defaults against [redis.io/docs](https://redis.io/docs) — the canonical
> upstream reference.

## Provenance

Principle P005 (eviction policy selection). Claims: c023 (per-key TTL/EXPIRE in Redis,
anchor h0033), c026 (eviction type comparison, situation-dependence, random not in production,
anchor h0036), c029 (Redis maxmemory-policy values and volatile-* scope, anchor h0039),
c030 (LRU/LFU as sampled approximations, anchor h0039). Source: Atchison, *Caching at Scale
With Redis* (2021), distillation-only — paraphrased throughout, no verbatim quotation.
