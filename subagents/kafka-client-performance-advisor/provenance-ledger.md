# Provenance Ledger — Kafka Client Performance Advisor

**Subagent slug:** `kafka-client-performance-advisor`
**Profile version:** 0.1.0
**Generated:** 2026-06-09

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| kafka-best-practices-20260608223304 | Kafka Best Practices | Yeva Byzek | 2020 | secondary | distillation-only | low | annual |

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `slug` | kafka-best-practices-20260608223304 | Q1 | Derived from role label; kebab-case role-based |
| `display_name` | kafka-best-practices-20260608223304 | Q1 | From paper title and structural section headers |
| `role` | kafka-best-practices-20260608223304 | Q1, Q2 | Synthesised from paper purpose statement (p.1) and three structural sections |
| `when_to_use[0]` | kafka-best-practices-20260608223304 | Q3 | New producer/consumer configuration before production |
| `when_to_use[1]` | kafka-best-practices-20260608223304 | Q3 | Throttle metrics (produce-throttle-time-avg, fetch-throttle-time-max) exceeding zero |
| `when_to_use[2]` | kafka-best-practices-20260608223304 | Q3 | Service-goal prioritisation and translation to parameters |
| `when_to_use[3]` | kafka-best-practices-20260608223304 | Q3 | Growing consumer lag (records-lag-max) remediation |
| `when_to_use[4]` | kafka-best-practices-20260608223304 | Q3 | Kafka Streams / ksqlDB topology, standby replicas, EOS |
| `when_not_to_use[0]` | kafka-best-practices-20260608223304 | Q4 | Inferred from scope statements; broker-side admin explicitly excluded |
| `when_not_to_use[1]` | kafka-best-practices-20260608223304 | Q4 | Inferred; security architecture deferred to separate Confluent docs |
| `when_not_to_use[2]` | kafka-best-practices-20260608223304 | Q4 | Inferred; business logic and schema design out of scope |
| `inputs.required[0]` | kafka-best-practices-20260608223304 | Q5 | Service goal required before tuning begins (p.20) |
| `inputs.required[1]` | kafka-best-practices-20260608223304 | Q5 | Current or proposed client configuration properties |
| `inputs.required[2]` | kafka-best-practices-20260608223304 | Q5 | Client type (Java / librdkafka) and cluster tier |
| `outputs.primary_format` | kafka-best-practices-20260608223304 | Q6 | Every optimisation section ends with a "Summary of Configurations" table |
| `modes[advise]` | kafka-best-practices-20260608223304 | Q9 | "To optimize for throughput… we generally recommend…" (pp. 22–36) |
| `modes[review]` | kafka-best-practices-20260608223304 | Q9 | "benchmark… starting with the default… familiarize yourself with the default values" (p.19) |
| `modes[validate]` | kafka-best-practices-20260608223304 | Q9 | "robust monitoring system in place… Ongoing monitoring… ensuring service goals are consistently met" (p.12) |
| `quality_bar[0]` | kafka-best-practices-20260608223304 | Q7 | Configuration summary tables use specific values (batch.size, linger.ms) not adjectives |
| `quality_bar[1]` | kafka-best-practices-20260608223304 | Q7 | Every optimisation section pairs gain with cost across goals |
| `quality_bar[2]` | kafka-best-practices-20260608223304 | Q7 | Monitoring prescription accompanies every recommendation (JMX + Metrics API) |
| `quality_bar[3]` | kafka-best-practices-20260608223304 | Q7 | Java vs. librdkafka parameter naming differences noted throughout |
| `quality_bar[4]` | kafka-best-practices-20260608223304 | Q7 | Benchmarking with production-representative data required (p.19) |
| `minimum_useful_output` | kafka-best-practices-20260608223304 | Q11 | Configuration summary boxes contain 4–7 named parameters |
| `forbidden_behaviours[0]` | kafka-best-practices-20260608223304 | Q10 | "avoid the temptation to discover and change other parameters… without understanding exactly how they impact the entire system" (p.19) |
| `forbidden_behaviours[1]` | kafka-best-practices-20260608223304 | Q10 | "We strongly recommend not using gzip because it's much more compute intensive" (p.23) |
| `forbidden_behaviours[2]` | kafka-best-practices-20260608223304 | Q10 | "you can't maximize all goals at the same time" (p.20) |
| `forbidden_behaviours[3]` | kafka-best-practices-20260608223304 | Q10 | Scope boundary inferred from paper's explicit focus on client configuration only |
| `handoff_rules[0]` | kafka-best-practices-20260608223304 | Q8 | "Next Steps — Develop, monitor, and tune your Kafka application" (p.37) |
| `handoff_rules[1]` | kafka-best-practices-20260608223304 | Q8 | "work with your administrator to get the appropriate access" (p.7) |
| `handoff_rules[2]` | kafka-best-practices-20260608223304 | Q8 | Inferred from "Next Steps" framing — production go/no-go after benchmark |
| `source_of_truth_policy.canonical_owner` | kafka-best-practices-20260608223304 | Q8, Q17 | Source pinned to CP 5.4/Kafka 2.4 (2020); Confluent docs supersede for current defaults |
| `source_of_truth_policy.precedence` | kafka-best-practices-20260608223304 | Q17, Q18 | Drift risk: defaults change per release; source is principles guide |
| `knowledge_partition.always_on` | kafka-best-practices-20260608223304 | Q12 | Ten always-on knowledge items distilled from Fundamentals and Optimizations sections |
| `knowledge_partition.skills` | kafka-best-practices-20260608223304 | Q13 | Six skill items extracted; moved out of profile body to avoid bloat |
| `knowledge_partition.references` | kafka-best-practices-20260608223304 | Q14 | Three reference items: config tables, JMX catalogue, decision tree |

---

## Evidence Gap Log

| Gap ID | Field(s) affected | Description | Resolution |
|--------|------------------|-------------|------------|
| EG-01 | `when_not_to_use` | Source has no explicit "do not use this guide for X" statement; exclusions inferred from scope statements and out-of-scope references | Inferred from broker-admin language and security deferral language; flagged as partial evidence |
| EG-02 | `handoff_rules` | No explicit "hand off to role Y" statement in source; handoff rules inferred from "work with your administrator" (p.7) and "Next Steps" (p.37) | Inferred and flagged in Q8 partial note |
| EG-03 | `mcp` | Confluent Cloud Metrics API runtime retrieval implied but source does not name a specific MCP tool | Listed as runtime retrieval requirement in Q15; mcp list left empty in profile |

---

## Conflict Log

_No conflicts recorded. Single source; no cross-source conflicts possible._

---

## Generated Artifacts

| Artifact | Type | Path | Notes |
|----------|------|------|-------|
| profile.yaml | canonical profile | `subagents/kafka-client-performance-advisor/profile.yaml` | |
| kafka-benchmarking-procedure | skill | `subagents/kafka-client-performance-advisor/skills/kafka-benchmarking-procedure/SKILL.md` | Not yet written; listed for future authoring |
| jmx-metric-collection | skill | `subagents/kafka-client-performance-advisor/skills/jmx-metric-collection/SKILL.md` | Not yet written |
| eos-configuration | skill | `subagents/kafka-client-performance-advisor/skills/eos-configuration/SKILL.md` | Not yet written |
| kafka-streams-topology-optimisation | skill | `subagents/kafka-client-performance-advisor/skills/kafka-streams-topology-optimisation/SKILL.md` | Not yet written |
| consumer-group-rebalancing | skill | `subagents/kafka-client-performance-advisor/skills/consumer-group-rebalancing/SKILL.md` | Not yet written |
| schema-registry-avro-wiring | skill | `subagents/kafka-client-performance-advisor/skills/schema-registry-avro-wiring/SKILL.md` | Not yet written |
| service-goal-configuration-tables | reference | `subagents/kafka-client-performance-advisor/references/service-goal-configuration-tables.md` | Not yet written |
| jmx-metric-catalogue | reference | `subagents/kafka-client-performance-advisor/references/jmx-metric-catalogue.md` | Not yet written |
| service-goal-decision-tree | reference | `subagents/kafka-client-performance-advisor/references/service-goal-decision-tree.md` | Not yet written |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-09 | Initial generation | kafka-best-practices-20260608223304 |
| 0.3.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Open Questions

- EG-03: Should the Confluent Cloud Metrics API be wired as an MCP tool in a future iteration when a tool schema is available?

---

## Notes

Source is dated 2020 (Confluent Platform 5.4 / Kafka 2.4). Parameter defaults, codec availability (zstd added Kafka 2.1), and EOS API changes (KIP-447, Kafka 2.5) may render specific numeric guidance outdated. Review annually against current Confluent documentation.
