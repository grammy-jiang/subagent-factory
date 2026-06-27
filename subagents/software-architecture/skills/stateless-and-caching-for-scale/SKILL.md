---
name: stateless-and-caching-for-scale
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P033
  - P027
  - P029
  - P032
  claims:
  - C02012
  - C02013
  - C02048
  - C02049
  - C01500
  - C01503
  - C02297
  - C02298
  evidence:
  - E00273
  - E00274
  - E00280
  - E00281
  - E00238
  - E00239
  - E00363
  - E00364
  source_anchors:
  - 760c81171459-c0034
  - 67c60e378753-c0000
  - 4bc1908bad03-c0000
  - a6c7e769c072-c0001
  authored_from_digest: 3a35395b3d2bfa5036dce631481aa1c5202ca8d94ce6998c8e13620b7f52a510
---

# Statelessness and caching for scale

## Purpose

Remove the two most common obstacles to horizontal scale: per-node state and repeated work.
Stateless services let any clone serve any request, which is the precondition for X-axis scale-out
and for surviving node failure; aggressive caching and computational reuse cut the load a system
must serve at all. Both are deliberate trade-offs, not free wins.

## When to use

- Application servers keep per-user session state locally, or requests are pinned to a node.
- A design wants to clone application servers but assumes sticky sessions.
- A system recomputes or re-serves the same results under load, or origin traffic is the bottleneck.

Do not invoke when the interaction is genuinely single-node with no scaling/failover goal, or when
correctness forbids any staleness at all.

## Procedure

1. **Find the state.** Locate per-request/per-session state held on a specific node. Local session
   state is what *forces* sticky routing; sticky routing assigns requests by something other than
   load, so it is not load balancing and it wastes capacity.
2. **Externalize state.** Move session/shared state to an external store so any node can serve any
   request. Confirm no remaining affinity prevents a clone from taking over on failure.
3. **Avoid the work before optimizing it.** The cheapest request is the one never served. Offload
   static and cacheable content to edge/CDN nodes that hold duplicate copies — get someone else to
   serve as many requests as possible.
4. **Reuse computation.** Where storing a result and looking it up later is cheaper than recomputing
   it, apply computational reuse (memoize/cache the result) at the appropriate layer.
5. **Name the freshness trade-off.** Every cache trades staleness for load reduction. State the
   invalidation/expiry policy and the staleness window the caller is accepting.
6. **Sequence it.** Statelessness first (it unlocks cloning), then caching/reuse (it reduces the
   load the clones share). Tie both back to the prioritized characteristics.

## Inputs

- Where state currently lives, the routing/affinity scheme, and which results or content are
  recomputed or re-served under load.

## Output

A review or recommendation that removes node affinity (stateless services + external state) and
applies edge/CDN offload and computational reuse, each with its staleness/invalidation trade-off
named.

## Provenance

Distilled from principle(s) **P010/P025/P011/P016/P028**, claims **C00532/C00533/C00568/C00569/C00235/C00621**, evidence **E00093/E00094/E00096/E00097/E00056/E00103**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
