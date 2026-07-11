---
name: kafka-intel-open-source-contributions
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka Intel Open-Source Contributions

Catalogue of the Intel open-source contributions and libraries the source credits
for Kafka acceleration (section 5–6). Use to explain *why* a recommended JDK,
TLS, or compression-library change yields its measured benefit and where the
capability lives.

| Contribution / library | What it provides | Relevance to Kafka |
|------------------------|------------------|--------------------|
| **OpenJDK — VAES upstream/backport** | Intel contributed AVX-512 VAES crypto support to OpenJDK and backported crypto/hash acceleration from JDK 12+ into JDK 11 LTS (11.0.15), sponsored by the HotSpot compiler team. | Lets JDK 11.0.11+ accelerate AES-GCM; the basis for JDK-11-over-JDK-8 encryption gains. |
| **Kafka community — TLS regression (KAFKA-13418)** | Intel engineers found that TLS 1.3 on Kafka 2.7 with JDK 11 lacked renegotiation support, causing intermittent broker disconnections that hurt P99 latency; a fix was applied and upstreamed. | Caveat when enabling TLS 1.3 on older Kafka/JDK pairings. |
| **OpenSSL — SSL/TLS with AES** | Open-source SSL/TLS implementation broadly adopted for Kafka (e.g. Confluent); can outperform JDK SSL. Asynchronous OpenSSL is non-blocking, enabling parallel crypto processing. The Intel QAT engine (QAT_Engine) on OpenSSL offloads crypto to hardware engines or separate cores. | Alternative TLS path that can lower encryption overhead vs JDK SSL. |
| **Intel ISA-L (Storage Acceleration Library)** | Optimised low-level functions for storage: RAID, erasure coding (Reed-Solomon), CRC, crypto-hash, encryption, and compression. Its IGZIP implementation accelerates gzip; ISA-L Crypto does multi-buffer hashing with SIMD. | Drop-in gzip replacement: ~1.47x throughput, ~34% latency vs native Java gzip. |
| **Intel IPP Cryptography** | Secure, lightweight crypto building blocks optimised for Intel CPUs using SIMD/AVX. The multithreaded Zlib-interface "IPP gzip" is Intel's patched version of native Java gzip (part of Intel oneAPI). | Drop-in gzip replacement: ~1.15x throughput, ~8% latency vs native Java gzip. |

## Continued-innovation notes (forward-looking, section 6)

- JDK 18 adds optimised CRC32 and interleaved GCM functions, and 512-bit-wide
  vector array copy/clear, on Intel hardware.
- 4th Gen Intel Xeon adds the QAT accelerator engine for crypto and
  de/compression offload from the CPU.
- Intel Granulate is cited as a no-code-change workload-optimisation option
  (vendor claim — treat as such, not benchmarked here).

## Usage note

These are the mechanisms behind the figures, not separate performance claims.
Quantified uplift lives in `kafka-benchmark-result-figures`; cite a number from
there, and use this table only to name the contributing component.

## Provenance

Tier 0 — condensed from the source section 5 (Intel's Contributions on Open
Source Optimization) and section 6 (Continued Innovation). Descriptions
paraphrased; no verbatim quotation.
