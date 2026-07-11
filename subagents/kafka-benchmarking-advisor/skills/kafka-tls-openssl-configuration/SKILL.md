---
name: kafka-tls-openssl-configuration
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka TLS / OpenSSL Configuration

## Purpose

Choose and configure the TLS crypto path for Kafka client–broker communication so
that AES-GCM encryption overhead is minimised on Intel hardware. TLS protects data
in transit but is CPU-intensive; the path you pick (JDK SSL vs OpenSSL, and which
hardware acceleration it can reach) decides how much of that overhead the CPU
actually pays. Note: Kafka has no encryption-at-rest — this skill is in-transit
TLS only.

## When to use

- A team is enabling TLS on Kafka and wants to limit the throughput/latency cost.
- A caller is choosing between JDK SSL and OpenSSL for broker/client TLS.
- An operator hits TLS 1.3 disconnections on an older Kafka/JDK combination.

## Procedure

1. **Establish the cipher and its cost.** Kafka TLS uses AES-GCM cipher suites.
   AES-GCM is pipelineable, so hardware implementations reach high speed at low
   latency — but enabling TLS still adds encryption overhead that must be
   budgeted against the latency SLA.
2. **Make sure the JDK can reach VAES acceleration.** AES-GCM is accelerated by
   OpenJDK 11.0.11+ via VAES / VPCLMULQDQ (AVX-512) on 3rd Gen Intel Xeon. If the
   cluster is on JDK 8, the JDK SSL path cannot use it — fix the JDK first (see
   `kafka-jdk-version-selection`).
3. **Consider OpenSSL over JDK SSL for the TLS path.** OpenSSL is widely deployed
   for Kafka client/broker TLS (Confluent adopts it broadly) and can outperform
   JDK SSL. Asynchronous OpenSSL is non-blocking and supports parallel-processing
   at the crypto level, enabling further optimisation.
4. **For maximum TLS throughput, evaluate the Intel QAT OpenSSL engine.** The
   QAT_Engine offloads crypto to dedicated hardware engines or separate logical
   cores and supports both hardware acceleration and optimised vectorised-software
   acceleration, boosting overall TLS performance.
5. **Watch the TLS 1.3 regression on older versions.** On Kafka 2.7 with JDK 11,
   TLS 1.3 did not support renegotiation, causing intermittent broker
   disconnections before read/write completed and harming P99 latency. The fix is
   tracked upstream as KAFKA-13418. Verify the caller's Kafka/JDK pairing against
   this before enabling TLS 1.3.
6. **Quantify the generational benefit, in-scenario.** On m6i (3rd Gen) vs m5
   (2nd Gen) with encryption ON and JDK 11, the source measured ~33% throughput
   and ~12% latency improvement — attributed to VAES crypto. Cite the matching
   scenario rather than a universal figure.

## Inputs

- TLS requirement and target TLS version.
- JDK version and CPU generation.
- SSL implementation in use or under evaluation (JDK SSL, OpenSSL, QAT engine).

## Output

A TLS configuration recommendation: SSL provider (JDK SSL / OpenSSL / QAT
engine), minimum JDK for acceleration, any TLS-1.3 regression caveat, and the
scenario-matched expected throughput/latency cost or saving.

## References

- `kafka-jdk-version-selection` — JDK floor for VAES acceleration.
- `kafka-intel-open-source-contributions` — OpenSSL/QAT, TLS regression, VAES.
- `kafka-benchmark-result-figures` — encryption-ON generational figures.

## Provenance

Derived (Tier 0) from the `always_on` rules on AES-GCM/TLS CPU cost and VAES, the
profile `when_to_use` OpenSSL/TLS entry, and the source's Crypto overview, the
Kafka Community TLS Regression note (KAFKA-13418), and the OpenSSL/QAT section 5
and 6 discussion. No verbatim quotation.
