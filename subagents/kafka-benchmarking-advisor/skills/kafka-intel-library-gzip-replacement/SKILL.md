---
name: kafka-intel-library-gzip-replacement
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Kafka Intel Library Gzip Replacement

## Purpose

Decide whether to swap native Java gzip in a Kafka pipeline for an Intel
gzip-compatible library — Intel ISA-L (via its IGZIP implementation) or Intel IPP
gzip — to raise compression throughput and cut producer-side latency on 3rd Gen
Intel Xeon hardware, while keeping gzip's compression ratio. Both are drop-in
replacements for the native Java gzip path.

## When to use

- An operator is using gzip compression (chosen for its high ratio / lowest P99
  latency among algorithms) and wants more throughput without abandoning gzip.
- A team is weighing ISA-L vs IPP vs native Java gzip.

## Procedure

1. **Confirm gzip is the right algorithm first.** Among compression methods, gzip
   gives the best P99 latency and highest compression ratio but the slowest
   compression speed / lowest throughput; LZ4, Snappy, and Zstd give higher
   throughput. Only pursue an Intel gzip library if the use case wants gzip's
   ratio/latency profile. If raw throughput dominates, consider LZ4/Zstd instead
   (see `kafka-benchmark-result-figures`).
2. **Confirm 3rd Gen Intel Xeon hardware.** The measured uplift is from Ice Lake
   bare-metal testing (Xeon Gold 6348). Do not extend the numbers to non-Intel
   CPUs.
3. **Pick the library by the priority you are optimising:**
   - **Intel ISA-L (IGZIP):** ~1.47x throughput and ~34% latency improvement vs
     native Java gzip. Choose when both throughput and latency matter most. ISA-L
     also covers RAID, erasure coding (Reed-Solomon), CRC, and crypto-hash
     functions.
   - **Intel IPP gzip:** ~1.15x throughput and ~8% latency improvement vs native
     Java gzip. A multithreaded Zlib-interface library (part of Intel oneAPI);
     the Intel-patched version of native Java gzip.
4. **Quantify against the native Java gzip baseline.** Always frame the uplift as
   a ratio against native Java gzip on matching hardware, not as a vague
   improvement. Cite the figure (ISA-L 1.47x / 34%; IPP 1.15x / 8%).
5. **Validate in the caller's environment.** The numbers come from the bare-metal
   config (Kafka 3.0.0, JDK 11.0.15, ISA-L 2.30, IPP 2021.4.0). Recommend the
   engineer benchmark the substitution on their own cluster before adopting.

## Inputs

- Current compression algorithm and whether gzip's ratio/latency profile is
  desired.
- Hardware generation (must be 3rd Gen Intel Xeon to claim the uplift).
- Optimisation priority: throughput, latency, or both.

## Output

A library recommendation (ISA-L or IPP) with its quantified throughput-ratio and
latency-improvement figure against native Java gzip, plus a note to validate on
the caller's hardware.

## References

- `kafka-benchmark-result-figures` — gzip vs Intel library figures (Fig 7, 8).
- `kafka-intel-open-source-contributions` — ISA-L and IPP descriptions.

## Provenance

Derived (Tier 0) from the `always_on` rule that ISA-L and IPP are drop-in gzip
replacements, the profile `quality_bar` ISA-L/IPP uplift requirement, and the
source's section 4.2 (Kafka Compression Optimizations on Intel Libraries,
figure 8) and section 5 library descriptions. No verbatim quotation.
