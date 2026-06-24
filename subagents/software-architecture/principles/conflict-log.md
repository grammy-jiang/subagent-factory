# Cross-source conflict log — software-architecture

Generated from `principle-graph.json` (Step 7). Cross-source `conflicts` edges are kept as **multi-truth**: both principles stay valid, scoped by the resolution. Never silently dropped.

- conflicts: 1 (resolved/scoped: 1, **OPEN: 0**)

## Resolved / scoped (multi-truth)

### P026 ↔ P013
- **P026:** Use Kafka transactions for exactly-once across Kafka-only chains, tying state-store writes to message sends, but do not expect them to cover external systems or to roll back after commit.
- **P013:** Do not build transactions across microservice boundaries; fix the service granularity instead, and use the saga pattern only sparingly for unavoidable cross-service coordination.
- **Resolution:** Scoped: P013 forbids application-level transactions across heterogeneous service boundaries; P026's exactly-once is confined to a Kafka-only message chain, so they do not actually contradict.

