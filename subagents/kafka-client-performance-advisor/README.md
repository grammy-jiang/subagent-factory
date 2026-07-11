# kafka-client-performance-advisor

**Version:** 0.1.0
**Status:** draft
**Generated:** 2026-06-09

## Purpose

Advises development teams on Kafka client configuration parameters to achieve target service goals (throughput, latency, durability, availability). Covers producer and consumer settings, compression codec selection, batching, acknowledgment semantics, consumer-group design, and observability via JMX and the Confluent Cloud Metrics API.

## Operational modes

| Mode | When to use |
|------|-------------|
| `advise` | Caller states a service goal and asks for parameter recommendations |
| `review` | Caller provides an existing configuration and asks for a best-practice assessment |
| `validate` | Caller asks whether a deployed configuration is achieving its service goal using monitoring data |

## Required inputs

1. Target service goal(s): throughput, latency, durability, or availability
2. Current or proposed client configuration (producer and/or consumer properties)
3. Client type (Java or librdkafka) and cluster tier (Confluent Cloud Standard or Dedicated)

## Scope boundaries

**In scope:** Kafka client application configuration parameters and client-side monitoring.

**Out of scope:** Broker administration, ZooKeeper, cluster provisioning, Confluent Cloud infrastructure, security architecture, application business logic, and schema design.

## Sources

| Source ID | Title | Author | Year | Rights |
|-----------|-------|--------|------|--------|
| kafka-best-practices-20260608223304 | Kafka Best Practices | Yeva Byzek | 2020 | distillation-only |

Source is pinned to Confluent Platform 5.4 / Kafka 2.4 (2020). Cross-check specific parameter defaults and valid value ranges against current Confluent documentation before applying in production.

## Package layout

```
subagents/kafka-client-performance-advisor/
  profile.yaml                        canonical profile
  provenance-ledger.md                field-level distillation log
  CHANGELOG.md                        version history
  README.md                           this file
  source-pack.manifest.yaml           source inventory
  tests/golden-tests.yaml             routing and output tests
  sources/                            ingested source files
  skills/                             skill stubs (to be authored)
  references/                         reference stubs (to be authored)
```

## Validation

```bash
python -m tools.subagent_factory.cli selfcheck kafka-client-performance-advisor
```
