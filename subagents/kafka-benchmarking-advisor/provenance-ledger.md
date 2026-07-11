# Provenance Ledger — Kafka Infrastructure Benchmarking Advisor

**Subagent slug:** `kafka-benchmarking-advisor`
**Profile version:** 0.1.0
**Generated:** 2026-06-09T00:00:00+00:00

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| kafka-optimization-b-20260608223929 | A Guide to Kafka Optimizations and Benchmarks | Debashis Paul, Roberto Baturoni | 2022 | Intel Corporation | distillation-only | high (software versions and instance families dated April–September 2022) | annual |

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `display_name` | kafka-optimization-b-20260608223929 | Q1 | Derived from interrogation Q1 display name |
| `role` | kafka-optimization-b-20260608223929 | Q1 | Paraphrased from Q1 role description |
| `when_to_use` (trigger 1) | kafka-optimization-b-20260608223929 | Q3 | Instance generation selection scenario; source sections 1.1–1.2 |
| `when_to_use` (trigger 2) | kafka-optimization-b-20260608223929 | Q3 | Compression algorithm evaluation; source sections 3.1–3.2 |
| `when_to_use` (trigger 3) | kafka-optimization-b-20260608223929 | Q3 | CPU linear scaling; source section 2 |
| `when_to_use` (trigger 4) | kafka-optimization-b-20260608223929 | Q3 | JDK 8 vs JDK 11 with TLS; source sections 1.2, 4.1 |
| `when_to_use` (trigger 5) | kafka-optimization-b-20260608223929 | Q3 | Intel library gzip replacement; source section 4.2 |
| `when_not_to_use` (exclusion 1) | kafka-optimization-b-20260608223929 | Q4 | Non-Intel hardware; source scope explicitly Intel Xeon only |
| `when_not_to_use` (exclusion 2) | kafka-optimization-b-20260608223929 | Q4 | Encryption-at-rest; verbatim source exclusion statement |
| `when_not_to_use` (exclusion 3) | kafka-optimization-b-20260608223929 | Q4 | Application-layer design; outside source scope |
| `inputs.required` | kafka-optimization-b-20260608223929 | Q5 | Five required inputs from Q5 |
| `outputs.primary_format` | kafka-optimization-b-20260608223929 | Q6 | Primary deliverable from Q6 |
| `modes.advise` | kafka-optimization-b-20260608223929 | Q9 | Evidence: 'Optimize Apache Kafka Streaming' section advisory verbs |
| `modes.compare` | kafka-optimization-b-20260608223929 | Q9 | Evidence: benchmark sections 1.1–4.2 head-to-head comparisons |
| `modes.validate` | kafka-optimization-b-20260608223929 | Q9 | Evidence: process/methodology section repeatable gating |
| `quality_bar` (all 5 items) | kafka-optimization-b-20260608223929 | Q7 | Directly from Q7 quality marks |
| `minimum_useful_output` | kafka-optimization-b-20260608223929 | Q11 | JDK 8 to 11 example from Q11 |
| `forbidden_behaviours` (all 4 items) | kafka-optimization-b-20260608223929 | Q10 | Directly from Q10 refusals |
| `handoff_rules` | kafka-optimization-b-20260608223929 | Q8 | Inferred from Q8 (see evidence gaps) |
| `source_of_truth_policy.precedence` | kafka-optimization-b-20260608223929 | Q17 | Directly from Q17 |
| `knowledge_partition.always_on` (all 7 items) | kafka-optimization-b-20260608223929 | Q12 | Directly from Q12 |
| `knowledge_partition.skills` (all 5 items) | kafka-optimization-b-20260608223929 | Q13 | Extracted from Q13 skill list |
| `knowledge_partition.references` (all 4 items) | kafka-optimization-b-20260608223929 | Q14 | Extracted from Q14 reference list |
| `sources[0].sha256` | kafka-optimization-b-20260608223929 | — | From source-pack.manifest.yaml |

---

## Evidence Gaps

The following gaps were recorded in the interrogation record and are logged here per the no-silent-resolution rule:

1. **Q8 partial — canonical owner identification:** The source does not name a specific role or team as the canonical decision owner. The value "infrastructure or platform engineer" is inferred from the document's intended audience ("enterprise" capacity planning context). This inference is flagged, not sourced.

2. **Q15 partial — MCP tool retrieval:** The source does not mention MCP tools or retrieval mechanisms. The three MCP entries (Kafka release notes, Intel library versions, AWS instance pricing) are gap-filled from logical requirements for keeping benchmark data current, not from source evidence.

---

## Generated Artifacts

| Artifact | Type | Path | Notes |
|----------|------|------|-------|
| profile.yaml | canonical profile | `subagents/kafka-benchmarking-advisor/profile.yaml` | |
| kafka-benchmarking-perf-test-procedure | skill | `subagents/kafka-benchmarking-advisor/skills/kafka-benchmarking-perf-test-procedure/SKILL.md` | Not yet written |
| kafka-tls-openssl-configuration | skill | `subagents/kafka-benchmarking-advisor/skills/kafka-tls-openssl-configuration/SKILL.md` | Not yet written |
| kafka-intel-library-gzip-replacement | skill | `subagents/kafka-benchmarking-advisor/skills/kafka-intel-library-gzip-replacement/SKILL.md` | Not yet written |
| kafka-kubernetes-anti-affinity-setup | skill | `subagents/kafka-benchmarking-advisor/skills/kafka-kubernetes-anti-affinity-setup/SKILL.md` | Not yet written |
| kafka-jdk-version-selection | skill | `subagents/kafka-benchmarking-advisor/skills/kafka-jdk-version-selection/SKILL.md` | Not yet written |
| kafka-benchmark-hardware-tables | reference | `subagents/kafka-benchmarking-advisor/references/kafka-benchmark-hardware-tables.md` | Not yet written |
| kafka-benchmark-software-tables | reference | `subagents/kafka-benchmarking-advisor/references/kafka-benchmark-software-tables.md` | Not yet written |
| kafka-benchmark-result-figures | reference | `subagents/kafka-benchmarking-advisor/references/kafka-benchmark-result-figures.md` | Not yet written |
| kafka-intel-open-source-contributions | reference | `subagents/kafka-benchmarking-advisor/references/kafka-intel-open-source-contributions.md` | Not yet written |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-09 | Initial generation | kafka-optimization-b-20260608223929 |
| 0.3.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Open Questions

1. Skills and reference files listed in knowledge_partition have not been written. They should be authored before the package is marked complete.
2. MCP entries in profile.yaml are empty arrays pending confirmation of runtime tool availability.

---

## Conflict Log

_No conflicts recorded at time of generation._
