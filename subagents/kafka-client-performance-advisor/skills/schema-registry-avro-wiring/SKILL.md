---
name: schema-registry-avro-wiring
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0134
  - kafka-best-practices-20260608223304-t0127
  - kafka-best-practices-20260608223304-t0074
---

# Schema Registry and Avro wiring

## Purpose

Wire a Kafka client to use Confluent Schema Registry with Avro serialization so message
schemas are versioned, governed, and evolved safely. The source recommends managed
Schema Registry plus Avro because it has seen recurring operational mistakes (bad
designs, inconsistent configuration) when teams self-manage their own registry — the
managed service removes that failure surface.

## When to use

- A client needs governed, versioned message schemas rather than ad-hoc payloads.
- Schemas must evolve under controlled compatibility rules.
- Standing up Avro serialization against Confluent Cloud Schema Registry.

## Procedure

1. **Prefer the managed registry.** Enable Confluent Cloud Schema Registry in the
   environment rather than self-hosting, to avoid the self-management mistakes the source
   warns about.
2. **Pick the subject name strategy.** The registry stores a versioned schema history
   keyed by a subject name strategy; choose the strategy deliberately, as it governs how
   schemas for a topic are grouped and resolved.
3. **Set the compatibility level** appropriate to how the schema will evolve, so the
   registry accepts only backward/forward-compatible changes as configured and rejects
   breaking ones at registration time.
4. **Configure the client to reach the registry.** Provide
   `schema.registry.url=<SR endpoint>`, and for authenticated registries set
   `basic.auth.credentials.source=USER_INFO` and
   `schema.registry.basic.auth.user.info=<SR API KEY>:<SR API SECRET>`.
5. **Use the Avro serializers/deserializers** that plug into the Kafka client to handle
   schema storage and retrieval transparently for Avro-format messages.
6. **Test schema compatibility in CI/CD.** Validate Avro and schema-compatibility
   alongside unit and integration tests (e.g. with a mock Schema Registry client) before
   deploying, so an incompatible schema is caught off the production path.

## Inputs

- Schema Registry endpoint and (if secured) API key/secret.
- The chosen subject name strategy and compatibility level.
- The Avro schema(s) for the topic's key and/or value.

## Output

A client configured for Avro serialization against the (managed) Schema Registry, with a
documented subject naming strategy and compatibility level, and a CI/CD compatibility
check.

## References

- `service-goal-configuration-tables` — sibling client configuration tables.

## Provenance

Tier 0. Grounded in the profile scope (client credential / Schema Registry configuration)
and the Schema Registry and Avro section of the Confluent source guide
(`kafka-best-practices-20260608223304`). Rights: distillation-only — paraphrased, no
verbatim quotation.
