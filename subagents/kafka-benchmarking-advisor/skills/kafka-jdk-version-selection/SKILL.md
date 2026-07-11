---
name: kafka-jdk-version-selection
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka JDK Version Selection

## Purpose

Choose the JDK version for a Kafka cluster so that, when TLS encryption is
enabled, the workload benefits from Intel VAES crypto acceleration. The decision
turns almost entirely on one fact: JDK 8 has no crypto-acceleration support,
while OpenJDK 11.0.11 and later leverage VAES / VPCLMULQDQ from the Intel AVX-512
family for AES-GCM. Picking JDK 8 with encryption on leaves measured throughput
and latency on the table.

## When to use

- A platform engineer is choosing between JDK 8 and JDK 11+ for a TLS-enabled
  Kafka cluster on 3rd Gen Intel Xeon (Ice Lake) hardware.
- A team running JDK 8 with encryption asks what the upgrade is worth.

## Procedure

1. **Confirm encryption is in play.** The JDK choice only changes crypto
   acceleration. If TLS is off, the JDK crypto benefit does not apply and the
   recommendation is weaker — say so.
2. **Confirm the hardware is 3rd Gen Intel Xeon.** VAES/AES-NI acceleration is an
   Ice Lake capability; on non-Intel CPUs the source provides no evidence and the
   advice must not be extended (forbidden behaviour).
3. **Require JDK 11.0.11 or later for crypto acceleration.** JDK 8 cannot use the
   VAES crypto path; JDK 11.0.11+ can. Treat JDK 11.0.11 as the minimum to claim
   the benefit. The source benchmarked 11.0.15 and 17.0.1.
4. **Quantify the upgrade from the matching scenario, not in general.** Cite the
   source figure for the caller's instance and encryption setting. Example: on
   i4i.4xlarge with encryption ON, JDK 8 → JDK 11 gave ~26% throughput and ~39%
   P99-latency improvement. On m6i vs m5 with no compression, JDK 11+ instances
   showed ~25–30% throughput improvement against 2nd Gen. Do not state a single
   universal number.
5. **Flag version-range gaps.** If the caller's Kafka (tested range 2.8.1–3.2) or
   JDK falls outside the tested set (8, 11.0.15, 17.0.1), flag that the 2022 data
   may not hold and recommend checking current release notes before acting.
6. **Hand off the decision.** Recommend JDK 11.0.11+ for any TLS-enabled cluster
   on Ice Lake; leave the platform engineer to validate against their own
   environment and SLA.

## Inputs

- TLS encryption on/off.
- CPU generation (must be 3rd Gen Intel Xeon to claim the benefit).
- Current and candidate JDK versions; instance type for figure matching.

## Output

A JDK recommendation (e.g. "upgrade JDK 8 → JDK 11.0.11+") with the
scenario-matched expected throughput and P99-latency improvement, plus an
explicit note on any out-of-range version that weakens the source evidence.

## References

- `kafka-benchmark-result-figures` — JDK-across-encryption figures (Fig 5, 6).
- `kafka-intel-open-source-contributions` — OpenJDK VAES upstream/backport work.

## Provenance

Derived (Tier 0) from the `always_on` rule that JDK 11.0.11+ is required for Intel
VAES crypto acceleration, the profile `when_to_use` JDK entry, and the source's
section 3 (Kafka Encryption Performance Across Java Versions, figures 5–6) and the
AES-GCM/OpenJDK 11.0.11 discussion in the Crypto overview. No verbatim quotation.
