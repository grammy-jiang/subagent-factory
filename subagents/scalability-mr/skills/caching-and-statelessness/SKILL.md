---
name: caching-and-statelessness
kind: skill
status: ready
provenance:
  principles: [P003, P010, P031, P048, P046, P045, P047, P025, P005]
  claims: [C00088, C00089, C00154, C00155, C00085, C00419, C00355, C00331, C00375, C00079, C00018]
  evidence: [E00065, E00127, E00062, E00231, E00220, E00217, E00224, E00058, E00014]
  source_anchors: [67c60e378753-c0002, 67c60e378753-c0003, a6c7e769c072-c0003, a6c7e769c072-c0004]
---

# Cache in depth and keep services stateless

## Purpose

Cut load off the expensive tiers by caching at every layer and removing server-side state, so
requests can be served by any node and most responses never reach the origin.

## When to use

- A system has repetitive queries, computations, or servable content.
- Sessions are pinned to a server (affinity) or held in server memory, blocking horizontal cloning.
- A team is adding a constraint that an object hold state between user actions.

Do not invoke when the caller wants a specific cache product chosen or the caching layer coded
(out of scope — hand off).

## Procedure

1. **Strive for statelessness first (P010).** Prefer stateless services so any node can serve any
   request. If state is required, push it to the browser; otherwise use a distributed cache without
   affinity or replication. Remove session affinity that blocks scale-out.
2. **Cache in depth (P003).** Layer caches — CDN, page cache, application cache, object cache — and
   control them with HTTP headers (not meta tags). Monitor hit ratios; a cache you do not measure is
   a cache you cannot tune.
3. **Push per-user data to the user (P048).** Cache per-user data in the user's own cookie — a wildly
   scalable, user-centric cache — secured with encryption for confidentiality plus a digest for
   integrity.
4. **Offload origins with a reverse proxy (P046).** Serve previously seen content from a reverse-proxy
   cache and let it absorb slow-client TCP handling so expensive application servers move to the next
   job.
5. **Segregate static from dynamic (P045).** Most content is static; serve it from a lightweight,
   single-purpose server separated from dynamic content so each scales independently.
6. **Route to the nearest cluster (P047).** Optimize for network proximity, not geography; combine
   Anycast DNS (connectionless UDP) with unique per-node IPs to reach the nearest cluster — remember
   Anycast breaks TCP.
7. **Relax temporal constraints (P031).** Embrace eventual consistency (BASE) where strong
   consistency is not required, because CAP makes strong consistency expensive to scale.
8. **Do not duplicate work (P025, P005).** Never read-after-write to validate, act on returned error
   codes, cache data you will reuse soon, and trim the work the browser must do (fewer DNS lookups
   and page objects, balanced against the per-domain connection cap).
9. **State the trade-off.** Caching and eventual consistency buy throughput and origin offload at the
   cost of staleness and cache-invalidation complexity. Name the staleness the design accepts.

## Inputs

- The read/write mix, which data is reused and how fresh it must be, and where state currently lives.

## Output

A caching-and-state recommendation naming the layers to cache, the hit ratio to monitor, where state
moves, and the staleness/invalidation cost accepted.

## References

- [Availability and load-balancing patterns](../../references/availability-and-load-balancing-patterns.md)
- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P003/P010/P031/P048/P046/P045/P047/P025/P005** and their claims/evidence,
anchored in `sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
