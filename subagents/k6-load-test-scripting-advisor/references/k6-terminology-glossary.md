---
name: k6-terminology-glossary
kind: reference
status: ready
provenance:
  principles: []
  claims:
  - k6-c002
  - k6-c003
  - k6-c004
  - k6-c005
  - k6-c006
  - k6-c007
  - k6-c008
  - k6-c009
  - k6-c010
  - k6-c011
  - k6-c012
  - k6-c013
  - k6-c014
  - k6-c015
  - k6-c016
  - k6-c017
  - k6-c018
  - k6-c019
  - k6-c020
  - k6-c021
  - k6-c022
  - k6-c023
  - k6-c024
  - k6-c025
  - k6-c026
  - k6-c027
  - k6-c028
  - k6-c029
  - k6-c030
  - k6-c031
  - k6-c032
  - k6-c033
  - k6-c034
  - k6-c035
  - k6-c036
  - k6-c037
  - k6-c038
  - k6-c039
  - k6-c040
  - k6-c041
  - k6-c042
  - k6-c043
  - k6-c044
  - k6-c045
  - k6-c046
  - k6-c047
  - k6-c048
  - k6-c049
  - k6-c050
  source_anchors:
  - k6-guideline-20260612112658-h0001
  - k6-guideline-20260612112658-h0002
  - k6-guideline-20260612112658-h0003
  - k6-guideline-20260612112658-h0004
  - k6-guideline-20260612112658-h0005
  - k6-guideline-20260612112658-h0006
  - k6-guideline-20260612112658-h0008
  - k6-guideline-20260612112658-h0010
  - k6-guideline-20260612112658-h0012
  - k6-guideline-20260612112658-h0016
  - k6-guideline-20260612112658-h0020
  - k6-guideline-20260612112658-h0021
  - k6-guideline-20260612112658-h0022
  - k6-guideline-20260612112658-h0026
  - k6-guideline-20260612112658-h0027
  - k6-guideline-20260612112658-h0031
  - k6-guideline-20260612112658-h0032
  - k6-guideline-20260612112658-h0033
  - k6-guideline-20260612112658-h0037
  - k6-guideline-20260612112658-h0038
  - k6-guideline-20260612112658-h0040
  - k6-guideline-20260612112658-h0042
  - k6-guideline-20260612112658-h0044
  - k6-guideline-20260612112658-h0048
  - k6-guideline-20260612112658-h0049
  - k6-guideline-20260612112658-h0051
  - k6-guideline-20260612112658-h0054
  - k6-guideline-20260612112658-h0056
  - k6-guideline-20260612112658-h0057
  - k6-guideline-20260612112658-h0059
  - k6-guideline-20260612112658-h0060
  - k6-guideline-20260612112658-h0061
  authored_from_digest: 6e1f82187f0f3045d7c06c0b7e26671e35bce8970fd02612cbaa8a97fda98089
---

# k6 terminology glossary

A lookup table of the ~23 numbered terms the source cheat sheet defines, each with a
paraphrased definition and its source heading anchor. Definitions are derived from the
source; for complete behaviour the official k6 docs (k6.io) remain authoritative.
Where the cheat sheet uses informal wording that differs from the k6 docs (e.g. Trend
statistics), the technically correct k6 term is preferred and the discrepancy is noted.

## (1) Test Lifecycle

Source anchor: `k6-guideline-20260612112658-h0001`

Every k6 script passes through exactly four ordered stages:

| Stage | Anchor | What runs there |
|-------|--------|-----------------|
| Init | `h0002` | All `import` statements and module-level code execute once before the test starts. |
| Setup | `h0003` | Options and environment configuration are defined here — e.g. VU counts, iteration counts. |
| VU | `h0004` | The default-exported function runs repeatedly for each VU: HTTP calls, browser actions, and response validation. |
| Teardown | `h0005` | Final stage; cleanup and summary generation run here (e.g. `handleSummary` to produce an HTML report). |

## (2) Virtual User (VU)

Source anchor: `k6-guideline-20260612112658-h0006`

| Property | Value |
|----------|-------|
| Definition | A simulated concurrent user that interacts with the application; each VU repeatedly executes the test script for the duration of the test. |
| Option | `options.vus` |
| Type | Integer |
| Default | `1` |

## (3) Iterations

Source anchor: `k6-guideline-20260612112658-h0008`

| Property | Value |
|----------|-------|
| Definition | The number of times the scenario or action set is repeated across the test run. Setting `iterations: 10` causes the scenario to execute ten times in total. |
| Option | `options.iterations` |
| Type | Integer |
| Default | `1` |

## (4) Duration

Source anchor: `k6-guideline-20260612112658-h0010`

| Property | Value |
|----------|-------|
| Definition | The total wall-clock time for which VUs keep executing. Once elapsed, the run stops. |
| Option | `options.duration` |
| Type | Time string (seconds `s` or minutes `m`) |
| Example | `'30s'`, `'2m'` |

## (5) Stages

Source anchor: `k6-guideline-20260612112658-h0012`

| Property | Value |
|----------|-------|
| Definition | An array that divides the test into sequential phases, each with its own `duration` and `target` VU count, enabling realistic load patterns such as ramp-up, sustain, and ramp-down. |
| Option | `options.stages` |
| Type | Array of `{ duration, target }` objects |
| Note | `stages` is a shortcut for the `ramping-vus` executor (see term 23). |

## (6) Target

Source anchor: `k6-guideline-20260612112658-h0016`

The VU count a stage ramps toward over its `duration`. Setting `target: 0` in the final stage ramps all VUs down to zero, which is the standard teardown pattern.

| Field | Where it appears |
|-------|-----------------|
| `target` | `options.stages[].target` |

## (7) 90th Percentile (p90)

Source anchor: `k6-guideline-20260612112658-h0020`

The response time value below which 90 % of all measured requests complete. Lower values indicate better performance. In k6 threshold expressions: `p(90)<500` (milliseconds). The source cheat sheet labels this "90 Percentile"; the correct k6 docs notation is `p(90)`.

## (8) 95th Percentile (p95)

Source anchor: `k6-guideline-20260612112658-h0021`

The response time value below which 95 % of all measured requests complete. Lower values indicate better performance. In k6 threshold expressions: `p(95)<200`. The source cheat sheet labels this "95 Percentile"; the correct k6 docs notation is `p(95)`.

## (9) Checks

Source anchor: `k6-guideline-20260612112658-h0022`

| Property | Value |
|----------|-------|
| Definition | Boolean assertions on response properties (status code, body content, etc.) that confirm the system behaves correctly under load. |
| Failure behaviour | A failing check does NOT halt execution; the run continues and failures are counted in the summary. |
| API | `check(response, { 'label': (r) => r.status === 200 })` |

## (10) Metrics

Source anchor: `k6-guideline-20260612112658-h0026`

k6 collects measurements throughout a test run. There are four metric types:

| Type | What it tracks |
|------|---------------|
| Counter | Cumulative sum of all observed values. |
| Gauge | The minimum, maximum, and most recent observed value. |
| Rate | The proportion of non-zero values across all observations. |
| Trend | Statistical aggregates over all values: mean, median, and percentiles. (The source cheat sheet says "mode"; the k6 docs name this "median" / percentile — k6.io is authoritative.) |

Built-in metrics whose names begin with `http`, `iteration`, or `vu` are written to stdout automatically at the end of every run.

## (11) Thresholds

Source anchor: `k6-guideline-20260612112658-h0027`

| Property | Value |
|----------|-------|
| Definition | Predefined pass/fail criteria expressed as conditions on metric values. |
| Failure behaviour | When any threshold is unmet the test finishes with a **failed** exit status. |
| Option | `options.thresholds` |
| Example conditions | `'http_req_duration': ['p(95)<500']`, `'http_req_failed': ['rate<0.1']` |

Checks validate per-response conditions; thresholds determine the overall pass/fail of the run. They serve different purposes (claim k6-c050).

## `http_req_duration`

Source anchor: `k6-guideline-20260612112658-h0031`

A built-in Trend metric that records the total round-trip time of each HTTP request, measured from the moment the request is sent until the full response is received. Commonly used in threshold expressions such as `p(95)<500`.

## `http_req_failed`

Source anchor: `k6-guideline-20260612112658-h0032`

A built-in Rate metric that tracks the proportion of HTTP requests that returned a non-2xx or non-3xx status code. Used in threshold expressions such as `rate<0.1` (fewer than 10 % failures).

## (12) Status

Source anchor: `k6-guideline-20260612112658-h0033`

The HTTP status code returned in a response, accessible as `response.status`. Indicates whether the request succeeded (2xx/3xx) or failed (4xx/5xx). Commonly used inside `check()` assertions.

## (13) Error

Source anchor: `k6-guideline-20260612112658-h0037`

The error information captured when an HTTP request fails at the transport or protocol layer (not an HTTP error status), including the error message, stack trace, and supplementary detail. Accessible as `response.error`.

## (14) Error_Code

Source anchor: `k6-guideline-20260612112658-h0038`

A numeric identifier that categorises transport and protocol errors. When an HTTP error occurs, its code is stored in `response.error_code` and also attached as an `error_code` tag on associated metrics, enabling metric filtering by error category. Currently limited to HTTP errors; support for additional protocols may expand. Numeric ranges (from the source):

| Range | Category |
|-------|----------|
| 1000–1099 | General errors |
| 1100–1199 | DNS errors |
| 1200–1299 | TCP errors |
| 1300–1399 | TLS errors |
| 1400–1499 | HTTP 4xx errors |
| 1500–1599 | HTTP 5xx errors |
| 1600–1699 | HTTP/2 errors |

## (15) Scenario

Source anchor: `k6-guideline-20260612112658-h0040`

| Property | Value |
|----------|-------|
| Definition | A named user journey with its own VU count, iteration schedule, and executor configuration. |
| Parallelism | Multiple scenarios in a single script each run an independent JavaScript function, concurrently. |
| Option | `options.scenarios` |

## (16) Requests

Source anchor: `k6-guideline-20260612112658-h0042`

The aggregate count of HTTP requests executed by all VUs over the course of a test run. Tracked by the built-in `http_reqs` Counter metric.

## (17) Cookies

Source anchor: `k6-guideline-20260612112658-h0044`

Small data items sent with each HTTP request to maintain session state. k6 supports per-request cookie passing via the request options object (`http.get(url, { cookies: { key: 'value' } })`), enabling realistic simulation of authenticated or stateful user sessions.

## (18) Results Analysis

Source anchor: `k6-guideline-20260612112658-h0048`

The process of examining the metrics, logs, and data produced by a completed test run — response times, error rates, throughput, and percentile distributions — to identify performance bottlenecks and determine whether the system meets requirements.

## (19) Load Distribution

Source anchor: `k6-guideline-20260612112658-h0049`

How the total workload is allocated across VUs over time, including control over concurrent user counts and request rates at different points in the test. Configured through stages, scenarios, and executor-specific options.

## (20) Load Testing

Source anchor: `k6-guideline-20260612112658-h0051`

The practice of evaluating how well a system performs when many users access it simultaneously. k6 achieves this by scripting VU behaviour and running the script with a configured load shape (VU count, duration, stages).

## (21) Test Script

Source anchor: `k6-guideline-20260612112658-h0054`

The JavaScript file passed to `k6 run`. It defines what each VU does: which HTTP endpoints to call, which browser actions to take, and how to validate responses. The default-exported function is the VU body; named exports (`options`, `setup`, `teardown`, `handleSummary`) control lifecycle and reporting.

## (22) Ramping

Source anchor: `k6-guideline-20260612112658-h0056`

A load pattern strategy in which the VU count (and therefore request rate) is gradually increased or decreased over a specified time period, rather than jumping to full load instantly. This better approximates real-world traffic growth and avoids artificial spike artefacts.

## (23) Ramping VUs

Source anchor: `k6-guideline-20260612112658-h0057`

| Property | Value |
|----------|-------|
| Definition | The `ramping-vus` executor: runs a variable number of VUs for a set duration, with VU counts controlled per time interval via `stages`. |
| Shortcut | `options.stages` at the top level is equivalent to using `ramping-vus` with default settings. |
| Executor key config fields | `startVUs`, `stages` (array of `{ duration, target }`), `gracefulRampDown` |
| Where it appears | `options.scenarios.<name>.executor: 'ramping-vus'` |

## Run commands

Source anchors: `k6-guideline-20260612112658-h0059`, `k6-guideline-20260612112658-h0060`, `k6-guideline-20260612112658-h0061`

| Goal | Command |
|------|---------|
| Run an API/protocol test | `k6 run testName.js` (run from the directory containing the script) |
| Run a browser test | `K6_BROWSER_ENABLED=true k6 run testName.js` |

## Provenance

Source: `k6-guideline-20260612112658` (Anshita Bhasin, "Most commonly used terms in K6" cheat sheet). Rights status: `distillation-only` — all definitions are paraphrased; no verbatim prose passages reproduced. Code identifiers (`options.vus`, `http_req_duration`, etc.) are standard k6 API names and not copyrightable expression. Grounded to Docling-converted heading anchors `h0001`–`h0061`; claim IDs `k6-c002`–`k6-c050`. Where the cheat sheet wording diverges from k6.io documentation (Trend "mode" vs. "median/percentile"), the k6 docs terminology is preferred and the discrepancy is noted inline.
