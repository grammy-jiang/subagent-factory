---
name: k6-thresholds-and-checks
kind: skill
status: ready
provenance:
  principles:
  - k6-p001
  - k6-p002
  - k6-p003
  claims:
  - k6-c019
  - k6-c020
  - k6-c024
  - k6-c025
  - k6-c050
  evidence:
  - ev-k6-007
  - ev-k6-008
  - ev-k6-010
  - ev-k6-011
  - ev-k6-024
  source_anchors:
  - k6-guideline-20260612112658-h0022
  - k6-guideline-20260612112658-h0023
  - k6-guideline-20260612112658-c0024
  - k6-guideline-20260612112658-h0027
  - k6-guideline-20260612112658-h0028
  - k6-guideline-20260612112658-c0029
  - k6-guideline-20260612112658-h0031
  - k6-guideline-20260612112658-h0032
  authored_from_digest: c80aab3b8c5ebdcb8771418da99e11cb3fa9f697722a3717ca4614c3988abdfc
---

# k6 Thresholds and Checks

## Purpose

Guide correct use of the two k6 constructs that express pass/fail criteria and
response validation: **thresholds** and **checks**. These constructs are
frequently confused because both involve conditions on responses, but they differ
in a critical way — a threshold failure ends the test run with a failed status
(k6-p002), whereas a failed check is recorded but does not halt execution
(k6-p001). Keeping that distinction clear is the load-bearing purpose of this
skill (k6-p003).

## When to use

- A caller wants to make a k6 run return a non-zero exit code when performance
  targets are not met (a CI gate, an SLO check) — they need a threshold.
- A caller wants to assert that individual responses contain expected content or
  status codes during the run, without affecting whether the run passes — they
  need a check.
- A caller is unsure whether a failing condition will abort the test, or is
  conflating checks and thresholds when deciding which construct to use.
- A caller is writing an `options.thresholds` block or a `check()` call and
  needs the correct syntax or an explanation of its behaviour.

## Procedure

### Step 1 — Classify the caller's intent

Determine which question the caller is actually asking:

| Caller intent | Correct construct |
|---|---|
| "Fail the run if the system is too slow or error-prone" | **Threshold** |
| "Confirm each response looks correct" | **Check** |
| "Both — record response correctness AND gate the run" | Both, used together |

If the caller is confused about whether a failing condition will stop the test,
state the critical distinction up front: checks never halt execution; only an
unmet threshold causes a failed test status.

### Step 2a — For a threshold: tie a metric to a pass/fail condition

Thresholds are declared inside `options.thresholds`. Each key is a metric name;
each value is a list of condition strings. When the system under test does not
satisfy a condition, the test finishes with a failed status (k6-p002, anchor
h0027).

```js
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95th-percentile response time
    http_req_failed: ['rate<0.1'],    // request failure rate ceiling
  },
};
```

Key points grounded in the source (anchors h0027–h0032):

- `http_req_duration` measures the time from sending a request to receiving the
  response (anchor h0031). It is a Trend metric, so threshold expressions can
  use percentile syntax such as `p(95)<500`.
- `http_req_failed` counts requests that returned non-2xx or non-3xx status
  codes (anchor h0032). It is a Rate metric, so threshold expressions use
  `rate<…` form.
- Thresholds can target any combination of metrics. Source examples include:
  fewer than 1% of requests returning an error, 95% of requests responding
  within 200 ms, 99% within 400 ms, a specific endpoint always within 300 ms,
  or a condition on a custom metric (anchor h0027).
- The numeric targets in those examples are illustrative; threshold values are
  caller-chosen performance targets, not limits prescribed by the source.

### Step 2b — For a check: validate response conditions per VU iteration

Checks are placed inside the VU code (the default-exported function). Each
check is a label paired with a predicate that evaluates the response. A failed
check is recorded in the test output but **does not halt execution** — the run
continues regardless (k6-p001, anchor h0022).

```js
export default function () {
  const res = http.get('http://test.k6.io/');
  check(res, {
    'Response status is 200': (r) => r.status === 200,
  });
}
```

Checks also work against a browser `page` object (for example, asserting
visible text after a login flow), using the same `check(page, { … })` form
(anchor h0022, source example at c0024).

### Step 3 — State the halt-vs-no-halt distinction explicitly when relevant

Whenever the caller must choose between the two constructs, or is uncertain
whether a failure will abort the test, deliver the contrast directly:

- A **check** validates an individual response condition. Failure is noted in
  output but the test run continues. Checks do not affect the pass/fail status
  of the run.
- A **threshold** evaluates an aggregate metric condition. When the condition is
  not met the test ends with a failed status — this is what causes a non-zero
  exit code in CI (k6-p003, anchors h0022 and h0027).

### Step 4 — Present threshold values as caller targets, not prescribed limits

The source shows example threshold expressions to illustrate the syntax. Do not
present specific numbers (500 ms, rate 0.1, p(95), p(99)) as authoritative
limits. They are examples of the expression form; the caller sets values that
match their own SLOs and performance targets.

### Step 5 — Stay within documented behaviour

Do not invent threshold expression syntax, metric names, check semantics, or
executor interactions that the source does not cover. If a caller asks about
behaviour the source does not address (for example, aborting a run mid-test
via `abortOnFail`, or threshold behaviour across distributed runs), state the
gap rather than speculate.

## Inputs

- The caller's stated intent: gating the run on pass/fail criteria, validating
  individual response conditions, or both.
- Any metric name(s) the caller is targeting and any numeric target they have
  in mind.
- The fragment of the k6 script under discussion: an `options.thresholds` block,
  a `check()` call, or a description of the condition they want to express.

## Output

A response that does one or more of the following, matched to what the caller
asked:

- **Threshold guidance**: an `options.thresholds` entry tying the appropriate
  metric to the caller's pass/fail condition, with a note that an unmet
  threshold ends the run in a failed status.
- **Check guidance**: a `check()` call validating the response condition(s) the
  caller named, with a note that a failed check does not stop the run.
- **Contrast**: when the caller must choose, a side-by-side comparison of the
  halt-vs-no-halt difference and which construct fits their goal.

In all cases: code shows standard k6 API names from the source only; numeric
values in examples are presented as illustrative, not authoritative.

## References

- [k6-terminology-glossary](../../references/k6-terminology-glossary.md) —
  definitions of Check, Threshold, http_req_duration, http_req_failed, and
  related terms.

## Provenance

Grounded in principles k6-p001 (checks do not halt execution, derived from
claims k6-c019 and k6-c020, evidence ev-k6-007 and ev-k6-008, source anchor
k6-guideline-20260612112658-h0022), k6-p002 (thresholds define pass/fail and
end the test on failure, derived from claims k6-c024 and k6-c025, evidence
ev-k6-010 and ev-k6-011, source anchor k6-guideline-20260612112658-h0027), and
k6-p003 (checks vs thresholds distinction must not be conflated, derived from
claim k6-c050, evidence ev-k6-024, source anchors h0022 and h0027). Source
rights status is `distillation-only`: all prose is paraphrased; no verbatim
passages of three or more sentences are reproduced. Code in the Procedure
section reflects standard k6 API names drawn from source anchor c0024 and
c0029.
