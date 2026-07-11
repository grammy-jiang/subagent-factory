---
name: kafka-benchmark-hardware-tables
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka Benchmark Hardware Tables

Hardware configurations underpinning the source benchmark figures (Appendix A,
Tables 1.1–1.3). Use to confirm a caller's instance matches a tested config
before applying a figure, and to flag when it does not.

## Table 1.1 — AWS m5 vs m6i (gen-to-gen comparison)

| Attribute | m6i.4xlarge (3rd Gen) | m5.4xlarge (2nd Gen) |
|-----------|-----------------------|----------------------|
| CPU model | Xeon Platinum 8375C @ 2.90 GHz (Ice Lake) | Xeon Platinum 8259CL @ 2.50 GHz |
| Base / Max freq | 2.9 / 3.5 GHz | 2.5 / 3.5 GHz |
| All-core max | 3.5 GHz | 3.1 GHz |
| vCPU | 16 | 16 |
| Threads/core, cores/socket, sockets | 2, 8, 1 | 2, 8, 1 |
| Memory | 64 GB DDR4 3,200 MT/s | 64 GB DDR4 2,933 MT/s |
| Microcode | 0xd000331 | 0x500320a |
| NIC / Drive | 1x ENA / 1x 500 GB EBS | 1x ENA / 1x 500 GB EBS |

## Table 1.2 — AWS i4i family (CPU-scaling comparison)

| Attribute | i4i.xlarge | i4i.2xlarge | i4i.4xlarge |
|-----------|------------|-------------|-------------|
| CPU model | Xeon Platinum 8375C @ 2.90 GHz | same | same |
| vCPU | 4 | 8 | 16 |
| Cores/socket | 2 | 4 | 8 |
| Memory | 32 GB | 64 GB | 128 GB |
| Base / Max freq | 2.9 / 3.5 GHz | 2.9 / 3.5 GHz | 2.9 / 3.5 GHz |
| Drive | 1x 500 GB EBS | 1x 500 GB EBS | 1x 500 GB EBS + 1x 3.4 TB NVMe instance store |

All three i4i instances share the same CPU model and frequency; vCPU/cores/memory
scale linearly — the basis for the linear CPU-scaling result.

## Table 1.3 — Intel bare-metal 3rd Gen Xeon (ISA-L / IPP testing)

| Attribute | Value |
|-----------|-------|
| CPU model | Ice Lake — Xeon Gold 6348 @ 2.60 GHz |
| Sockets / total CPUs | 2 / 112 |
| HT, Turbo Boost | Yes, Yes |
| Memory | 1,024 GB DDR4 3,200 MT/s |
| Disk | NVMe 3.7 TB |
| OS / Kernel | CentOS Linux 7 (Core) / 5.13.0+ |
| Microcode / BIOS | 0xd0002a0 / 05.01.01 |

This bare-metal config (not the AWS instances) is the basis for the gzip-vs-Intel
library throughput/latency figures.

## Usage note

A figure is only valid for the instance row it was measured on. m5/m6i figures
come from Table 1.1; i4i-scaling figures from Table 1.2; ISA-L/IPP figures from
the Table 1.3 bare-metal box. Do not transfer a number across rows or to non-Intel
hardware.

## Provenance

Tier 0 — transcribed and condensed from the source Appendix A hardware tables
(Tables 1.1, 1.2, 1.3). Figures paraphrased into summary form; no verbatim
quotation.
