---
name: k6-metrics-interpretation
kind: skill
status: ready
provenance:
  principles:
  - k6-p005
  - k6-p006
  - k6-p007
  claims:
  - k6-c022
  - k6-c027
  - k6-c029
  - k6-c030
  evidence:
  - ev-k6-009
  - ev-k6-012
  - ev-k6-014
  - ev-k6-015
  source_anchors:
  - k6-guideline-20260612112658-h0026
  - k6-guideline-20260612112658-h0028
  - k6-guideline-20260612112658-c0029
  - k6-guideline-20260612112658-h0031
  - k6-guideline-20260612112658-h0032
  authored_from_digest: 1ba29270a462bb9f38d1f2a7cd03108e6da542f66748167cdf0c554278bcb0c8
---

# k6 metrics interpretation

## Purpose

Interpret k6 metric output correctly by identifying the metric type (Counter,
Gauge, Rate, or Trend) that applies to a given measurement, and by reading the
semantics of the two built-in metrics most commonly referenced in threshold
examples: `http_req_duration` and `http_req_failed`. The four types determine
how k6 aggregates values; naming the wrong type misreads what a measurement
actually shows.

## When to use

- A caller is reading k6 terminal output and asks what a built-in metric means
  or how to interpret its value.
- The caller is choosing a metric for a threshold expression and needs to know
  whether it sums, tracks a range, tracks frequency, or computes statistics.
- The caller asks what p95 or p90 means in k6 results or why a percentile
  threshold was chosen as the SLO anchor.
- The caller is confused about whether `http_req_duration` or `http_req_failed`
  is the right metric for a pass/fail condition.

## Procedure

### Step 1 — Identify what is being measured

Determine from the caller's description which of the four types governs the
measurement:

| Type    | How k6 aggregates it                             | Fits measurements like                        |
|---------|--------------------------------------------------|-----------------------------------------------|
| Counter | Sums all values over the run                     | Total request count, byte totals              |
| Gauge   | Tracks the smallest, largest, and latest values  | A value that fluctuates (e.g., active VUs)    |
| Rate    | Tracks how often a non-zero value occurs         | Error proportion, check-pass proportion       |
| Trend   | Computes mean, median, and percentiles           | Response-time distributions                   |

Source: anchor h0026 — the section on Metrics lists all four types with these
definitions. (k6-p007, ev-k6-009)

### Step 2 — Choose the type by the analytical question

Map the caller's question to the correct type before naming a metric:

- "How many in total?" → Counter.
- "What is the current / minimum / maximum?" → Gauge.
- "How often does this happen?" → Rate.
- "What is the p95 / mean / median?" → Trend.

This avoids matching by metric name alone, which can mislead.

### Step 3 — Interpret the two built-in metrics most commonly used in thresholds

**`http_req_duration`** (anchor h0031, ev-k6-014, k6-p005): measures the total
duration of an HTTP request — from the moment the request is sent until the
response is fully received. Use this metric when expressing a response-time
threshold. Because it aggregates a distribution of values, it supports
percentile conditions.

**`http_req_failed`** (anchor h0032, ev-k6-015, k6-p005): counts HTTP requests
that returned a non-2xx or non-3xx status code. Use this metric when expressing
an error-rate threshold. It is a Rate-type metric and supports frequency
conditions such as `rate<0.1`.

Both metrics are k6 built-ins and appear in the threshold example at anchor
c0029: `http_req_duration: ['p(95)<500']` and `http_req_failed: ['rate<0.1']`.

### Step 4 — Interpret percentile values (p95 and p90)

When a caller encounters `p(95)` in threshold syntax or output (anchor h0028,
ev-k6-012, k6-p006):

- p95 is the 95th percentile response time — the value below which 95 percent
  of all sampled requests fell during the test.
- p90 is the analogous value at the 90th percentile.
- Lower values indicate better performance.
- The convention of anchoring HTTP response-time SLOs to p95 comes from its
  use in the source's threshold example; the exact numeric limit is
  caller-chosen, not a source mandate.

Do not state that p95 is "the industry standard" or otherwise stronger than
what the source documents. The source shows it as a commonly used example, not
a prescribed universal target.

### Step 5 — Map a threshold condition to the right metric type

A threshold condition must be compatible with the metric type:

- Trend metrics support percentile conditions — e.g., `p(95)<500`.
- Rate metrics support frequency conditions — e.g., `rate<0.1`.
- Counter metrics support sum conditions — e.g., `count<1000`.
- Gauge metrics support min/max/value conditions.

When the caller's condition and metric type are mismatched, name the mismatch
and suggest the type that fits the condition.

### Step 6 — Built-in metrics coverage and limits

All metric names beginning with `http`, `iteration`, or `vu` are k6 built-ins,
written to stdout at the end of a test (anchor h0026). The source instructs
callers to consult the k6 Metrics reference for the full list. Do not invent
metric names or semantics not documented in this cheat sheet — if a metric is
not covered, say so and direct the caller to the official k6 docs.

## Inputs

- The measurement or metric name the caller is trying to interpret, or the
  threshold expression under discussion.
- Optional: a fragment of k6 terminal output showing the metric and its value.

## Output

A response that:

1. Names the metric type (Counter / Gauge / Rate / Trend) applicable to the
   measurement and explains what that type aggregates.
2. For `http_req_duration` or `http_req_failed`, states the precise k6 semantic
   (total request time from send to receipt; non-2xx/non-3xx count
   respectively).
3. For percentile values, states what p95 or p90 represents numerically and
   notes that the threshold number is caller-chosen, not a mandated limit.
4. When the caller is choosing between metric types, contrasts the candidates
   so the correct one can be selected for the threshold condition in question.

## References

- [k6 terminology glossary](../../references/k6-terminology-glossary.md)
- [k6 thresholds and checks](../k6-thresholds-and-checks/SKILL.md)
- Source anchor h0026 — Metrics section (four types and built-in metric list)
- Source anchor h0028 and c0029 — Threshold example with `http_req_duration`
  and `http_req_failed`
- Source anchor h0031 — `http_req_duration` definition
- Source anchor h0032 — `http_req_failed` definition

## Provenance

Grounded in principles k6-p005, k6-p006, k6-p007 from
`subagents/k6-load-test-scripting-advisor/principles/principles.yaml`, and the
following evidence records from
`subagents/k6-load-test-scripting-advisor/evidence/evidence-records.yaml`:
ev-k6-009 (k6-c022, anchor h0026), ev-k6-012 (k6-c027, anchors h0028 and
c0029), ev-k6-014 (k6-c029, anchor h0031), ev-k6-015 (k6-c030, anchor h0032).
All grounding is from source
`subagents/k6-load-test-scripting-advisor/sources/markdown/k6-guideline-20260612112658.md`,
rights status `distillation-only`; all prose is paraphrased, no verbatim
passage of three or more sentences.
