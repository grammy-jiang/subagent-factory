---
name: kafka-benchmark-result-figures
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka Benchmark Result Figures

The quantified results from the source (Figures 1–8). Every number is tied to a
specific scenario — instance, JDK, encryption setting, compression method. Cite
the matching row; never present a figure as a general rule. All are median of
three runs. Throughput: higher is better. P99 latency: lower is better.
Improvements are vs the stated baseline (normalised to 1.0).

## Gen-to-gen: m6i (3rd Gen) vs m5 (2nd Gen), JDK 11

| Fig | Scenario | Throughput | P99 latency |
|-----|----------|------------|-------------|
| 1 | Encryption OFF | ~30% improvement (1.30x) | ~3% (1.03 — roughly flat) |
| 2 | Encryption ON | ~33% improvement (1.33x) | ~12% improvement (0.88) |
| 3 | Zstd compression | ~35% improvement | ~12% improvement |
| 3 | LZ4 compression | ~30% improvement | ~36% improvement (0.64) |

The encryption-ON gain over m5 is attributed to Intel VAES crypto on 3rd Gen.

## CPU scaling: AWS i4i family, LZ4, JDK 11 (Fig 4)

| Instance | Throughput (vs i4i.xlarge = 1) | P99 latency |
|----------|-------------------------------|-------------|
| i4i.xlarge (4 vCPU) | 1.0 | 1.0 |
| i4i.2xlarge (8 vCPU) | ~1.91 | ~1.50 |
| i4i.4xlarge (16 vCPU) | ~3.86 | ~2.08 |

Throughput scales roughly linearly when producers, brokers, consumers, and
partitions scale with the instance.

## JDK across encryption (Fig 5, m5 baseline, no compression)

| Scenario | Throughput (vs m5 = 1) |
|----------|------------------------|
| JDK 8 — Encryption ON | m6i ~1.24 |
| JDK 11 — Encryption OFF | m6i ~1.30 |
| JDK 11 — Encryption ON | m6i ~1.33 |

Source summarises 3rd Gen as ~25–30% throughput improvement vs 2nd Gen.

## JDK 8 vs JDK 11 on i4i.4xlarge, encryption ON, Zstd (Fig 6)

| KPI | JDK 8 → JDK 11 |
|-----|----------------|
| Throughput | ~26% improvement (1.26x) |
| P99 latency | ~39% improvement (0.61) |

## Compression types on m6i.4xlarge, encryption OFF (Fig 7)

| Algorithm | Throughput (vs gzip=1) | P99 latency |
|-----------|------------------------|-------------|
| gzip | 1.0 | best (lowest) |
| snappy | ~1.48 | ~1.38 |
| zstd | ~1.48 | ~1.38 |
| lz4 | ~1.48 | ~1.08 |

gzip gives the best P99 latency and highest ratio but lowest throughput;
LZ4/Snappy/Zstd give higher throughput.

## gzip vs Intel libraries, bare-metal Ice Lake (Fig 8)

| Library | Throughput (vs Java gzip=1) | P99 latency |
|---------|-----------------------------|-------------|
| Java gzip | 1.0 | 1.0 |
| IPP gzip | ~1.15x | ~8% improvement (0.91) |
| ISA-L | ~1.47x | ~34% improvement (0.66) |

## Provenance

Tier 0 — figures transcribed from the source result charts (Figures 1–8,
section 1–4.2). All values are normalised ratios paraphrased from the charts; no
verbatim quotation. Source testing dates: 12 Apr–21 Sep 2022.
