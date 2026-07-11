---
name: kafka-benchmark-software-tables
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
    - kafka-optimization-b-20260608223929-h0000
    - kafka-optimization-b-20260608223929-h0001
    - kafka-optimization-b-20260608223929-h0002
    - kafka-optimization-b-20260608223929-h0003
    - kafka-optimization-b-20260608223929-h0004
    - kafka-optimization-b-20260608223929-h0005
    - kafka-optimization-b-20260608223929-h0006
---

# Kafka Benchmark Software Tables

Software stack and Kafka/workload configuration constants behind the source
figures (Appendix A, Tables 2.1–2.4). Use to reproduce a test or to check that a
caller's setup matches the methodology.

## Common software stack

| Component | Version |
|-----------|---------|
| Kafka | 3.2 (2.8.1 and 3.0 also tested in specific cases) |
| ZooKeeper | 3.7.0 |
| Python | 3.10.x |
| OpenJDK | 11.0.15 (8u331 and 17.0.1 used in JDK-comparison cases) |
| OS | Ubuntu 20.04.4 / 22.04.1 LTS; CentOS 7 for bare-metal |

## Table 2.1 — m6i / m5 workload (encryption ON, Zstd/LZ4)

| Param | Value |
|-------|-------|
| REPLICATION_FACTOR | 1 |
| PARTITIONS / # producers / # consumers | twice the # of vCPUs |
| NUM_RECORDS | 5,000,000 |
| MESSAGES | 10,000,000 |
| ENCRYPTION | TRUE |
| RECORD_SIZE | 1,000 |
| COMPRESSION_TYPE | Zstd / LZ4 |
| BATCH_SIZE | 524,288 |
| LINGER_MS | 100 |
| CONSUMER_TIMEOUT | 600,000 |

## Table 2.2 — i4i family workload (JDK 11.0.15)

Same constants as Table 2.1 (REPLICATION_FACTOR 1; partitions/producers/consumers
= twice vCPUs; NUM_RECORDS 5,000,000; ENCRYPTION TRUE; RECORD_SIZE 1,000;
BATCH_SIZE 524,288; LINGER_MS 100). Used for the i4i CPU-scaling and JDK-8-vs-11
results.

## Table 2.3 — m6i compression comparison (encryption OFF, JDK 17.0.1)

| Param | Value |
|-------|-------|
| KAFKA | 2.8.1 |
| OPENJDK | 17.0.1 |
| REPLICATION_FACTOR | 1 |
| PARTITIONS / producers / consumers | twice the # of vCPUs |
| NUM_RECORDS | 3,000,000 |
| MESSAGES | 2,000,000 |
| ENCRYPTION | OFF |
| RECORD_SIZE | 1,000 |
| COMPRESSION_TYPE | gzip / Zstd / Snappy / LZ4 |
| BATCH_SIZE / LINGER_MS | Default |

## Table 2.4 — Bare-metal gzip vs Intel-library workload

| Param | Value |
|-------|-------|
| REPLICATION_FACTOR / PARTITIONS | 1 / 1 |
| # producers / consumers / brokers | 112 / 1 / 1 |
| NUM_RECORDS | 5,000,000 |
| MESSAGES | 10,000,000 |
| ENCRYPTION | No |
| RECORD_SIZE | 2048 |
| COMPRESSION_TYPE | Gzip / IPP Gzip |
| BATCH_SIZE / LINGER_MS | 524,288 / 100 ms |

## Usage note

The "twice the # of vCPUs" rule for partitions/producers/consumers is the scaling
knob — it must track the instance's vCPU count. Encryption, compression, record
size, and message count differ per table; quote the constant set that matches the
figure being cited.

## Provenance

Tier 0 — condensed from the source Appendix A software/workload/Kafka config
tables (Tables 2.1–2.4). Values paraphrased into summary tables; no verbatim
quotation.
