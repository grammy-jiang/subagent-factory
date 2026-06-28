---
name: cache-performance-formula-sheet
kind: reference
status: ready
provenance:
  principles:
  - P001
  claims:
  - C00022
  - C00023
  - C00024
  - C00113
  - C00114
  - C00115
  - C00116
  - C00117
  - C00118
  - C00119
  evidence:
  - E00011
  - E00012
  - E00013
  - E00051
  - E00052
  - E00053
  - E00054
  - E00055
  - E00056
  - E00057
  source_anchors:
  - 11ebbc818b96-c0000
  - 11ebbc818b96-c0003
  authored_from_digest: 5bbaae67acf6099f960eeeef7a4a53b4e78da3cf9d4c848c69dd83949922bb9f
---

# Cache Performance Formula Sheet

Companion reference for the `cache-performance-break-even` skill. All formulas apply
to the cache-aside pattern. Substitute real or reliably estimated timings; never
fabricate values.

## Term definitions

| Symbol | Full name | Description |
|--------|-----------|-------------|
| `S` | `Service_Call_Time` | Latency of the backing operation when served without a cache hit (e.g. a database query, an external API call). Measured or estimated in consistent time units. |
| `C` | `Cache_Check` | Cost of a single cache lookup, regardless of outcome. Paid on every request — on a hit it is the only cost; on a miss it is incurred before the backing call. |
| `H` | Hit rate | Fraction of requests resolved from cache (0–1). Miss rate = `1 − H`. |

## Request-time model

A cache lookup is paid on every request.

```
On a cache hit:   Request_Time = C
On a cache miss:  Request_Time = C + S      (lookup fails, then backing call runs)
```

Weighted average request time with a cache at hit rate H:

```
Avg_With_Cache = H·C + (1−H)·(C + S)
               = C + (1−H)·S
```

Uncached baseline:

```
Avg_No_Cache = S
```

Net benefit per request (positive = cache helps):

```
Net_Benefit = S − (C + (1−H)·S)
            = H·S − C
```

## Break-even formula

The cache provides zero net benefit when `Net_Benefit = 0`:

```
H·S − C = 0
H_min = C / (S + C)          ← minimum viable hit rate
```

Equivalently expressed as:

```
H_min = Cache_Check / (Service_Call_Time + Cache_Check)
```

This is exact, not an approximation. The denominator is the full miss-path cost
(`S + C`), not `S` alone.

## Decision rule

| Observed or projected H | Verdict |
|-------------------------|---------|
| H > H_min | Cache reduces average latency — proceed |
| H = H_min | Cache breaks even — no latency gain, no loss |
| H < H_min | Cache degrades performance versus uncached baseline — do not deploy |

## Sensitivity relationship

The higher `S` is relative to `C`, the lower `H_min` becomes, and the larger the
latency reduction at any given hit rate above break-even. When `S` is large and `C`
is small, even a modest hit rate produces substantial average-latency improvement;
when `S ≈ C`, the break-even rate approaches 50% and the latency benefit at high hit
rates is limited.

In practical terms: caching an inexpensive backing call offers little reward, while
caching an expensive one can yield dramatic savings once hit rate exceeds a small
threshold.

## Worked example (illustrative values only)

```
S = 25 ms,  C = 1 ms
H_min = 1 / (25 + 1) = 1/26 ≈ 7.7%   # any hit rate above 7.7% is net-beneficial

At H = 0.90:  Avg = 1 + 0.10·25 = 3.5 ms   # ~86% lower than 25 ms uncached
```

```
S = 500 ms, C = 1 ms (same overhead, costlier backing call)
H_min = 1 / (500 + 1) ≈ 0.2%          # threshold is negligible

At H = 0.90:  Avg = 1 + 0.10·500 = 51 ms   # ~90% lower than 500 ms uncached
```

> These numbers are illustrative only. Replace `S` and `C` with measured or
> estimated values before drawing conclusions. Do not present illustrative figures
> as measured results.

## Usage notes

- Run the formula for each caching opportunity before committing to a design, and
  repeat after deployment using observed hit rate metrics.
- If actual `S` and `C` are unavailable, obtain estimates before applying the
  formula — fabricated values produce unreliable verdicts.
- The model covers average-case latency. It does not capture tail-latency effects,
  cache warm-up periods, or thundering-herd behaviour on cold starts.

## Provenance

Principle P009; evidence records e031 (c066 — miss-cost model, anchors h0114/c0115–c0116),
e032 (c067 — hit-cost model, anchors c0117–c0120), e033 (c068 — break-even derivation,
anchors c0125–c0126/c0136–c0137), e035 (c070 — higher-S sensitivity, anchors
c0151–c0152), e036 (c071 — calculate per opportunity, anchor h0153).
Source: Caching at Scale With Redis (Atchison 2021) — distillation-only; no verbatim
quotation.
