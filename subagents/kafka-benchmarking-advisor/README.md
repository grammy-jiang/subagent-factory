# Kafka Infrastructure Benchmarking Advisor

**Slug:** `kafka-benchmarking-advisor`
**Version:** 0.1.0
**Status:** draft

## Purpose

This subagent provides evidence-backed guidance on Apache Kafka performance
optimisation and benchmarking specifically on Intel Xeon Scalable processor
hardware. It covers compression algorithm selection, JDK version impact on
TLS throughput, CPU generation trade-offs, Intel library substitutions for
gzip compression, and linear CPU scaling strategies.

All performance claims are derived from a 2022 Intel-authored benchmark guide
covering Kafka 2.8.1, 3.0, and 3.2 on m5, m6i, and i4i AWS instance families
and bare-metal 3rd Gen Xeon (Ice Lake) hardware.

## When to invoke

- Selecting between Intel Xeon processor generations for Kafka workloads
- Evaluating compression algorithms (gzip, Snappy, Zstd, LZ4) with quantified trade-offs
- Planning CPU linear scale-out on the i4i instance family
- Choosing between JDK 8 and JDK 11+ for clusters with TLS encryption
- Evaluating Intel ISA-L or Intel IPP as gzip replacements

## When NOT to invoke

- Non-Intel hardware (AMD, ARM) — source data does not apply
- Kafka encryption-at-rest design — explicitly out of scope per source
- Application-layer design (schema, topic modelling, consumer group logic)

## Required inputs

1. Target AWS instance family or bare-metal CPU generation
2. Encryption requirement (TLS on/off)
3. Compression method in use or under evaluation
4. JDK version currently deployed or planned
5. Primary workload KPI (max throughput MB/s, P99 latency ceiling ms, or both)

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `advise` | Deployment scenario with optimisation question | Prioritised configuration change list with quantified improvement and evidence |
| `compare` | Side-by-side comparison of two or more options | Head-to-head table with normalised throughput and latency ratios |
| `validate` | Benchmark test setup review | Methodology checklist with pass/fail assessment and remediation steps |

## Sources

| ID | Title | Rights | Year |
|----|-------|--------|------|
| kafka-optimization-b-20260608223929 | A Guide to Kafka Optimizations and Benchmarks | distillation-only | 2022 |

## Volatility

Source benchmark data is dated 2022. The following are likely to drift:
Kafka throughput characteristics per major release, JDK crypto acceleration
support, AWS instance availability and pricing, Intel QAT engine compatibility,
and 4th Gen Xeon (Sapphire Rapids) performance. Annual review is recommended.

## Package layout

```text
subagents/kafka-benchmarking-advisor/
  profile.yaml                        canonical profile
  provenance-ledger.md                distillation log and evidence gaps
  CHANGELOG.md                        version history
  README.md                           this file
  source-pack.manifest.yaml           source file registry
  interrogation-records.yaml          Q1-Q18 interrogation input
  sources/                            ingested source files
  tests/
    golden-tests.yaml                 routing and quality gate tests
  skills/                             (stub — not yet authored)
  references/                         (stub — not yet authored)
```
