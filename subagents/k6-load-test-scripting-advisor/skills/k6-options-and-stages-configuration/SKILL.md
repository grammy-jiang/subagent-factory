---
name: k6-options-and-stages-configuration
kind: skill
status: ready
provenance:
  principles:
  - k6-p004
  claims:
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
  - k6-c047
  source_anchors:
  - k6-guideline-20260612112658-h0006
  - k6-guideline-20260612112658-h0008
  - k6-guideline-20260612112658-h0010
  - k6-guideline-20260612112658-h0012
  - k6-guideline-20260612112658-h0013
  - k6-guideline-20260612112658-c0014
  - k6-guideline-20260612112658-h0016
  - k6-guideline-20260612112658-h0017
  - k6-guideline-20260612112658-c0018
  - k6-guideline-20260612112658-h0057
  authored_from_digest: 9d9f4076ec4f9b61794cb0d480d3bfffda1f353dd092adbfd4503fe167a70614
---

# k6 options and stages configuration

## Purpose

Translate a desired load profile into the correct fields of a k6 `options`
object. This skill covers the four load-shape controls — `vus`, `iterations`,
`duration`, and `stages` (where each stage carries its own `duration` and
`target`) — and explains how they interact so that the active virtual-user
count is driven up, held steady, and ramped down over time as required by
the test design.

The primary grounding principle is k6-p004: stages move the VU count toward
a `target` value across each stage's `duration`, making the `stages` array
the correct mechanism for any load profile that changes in phases. `stages`
is also documented as a shortcut for the ramping-vus executor
(source anchor h0057).

## When to use

- An engineer is writing or reviewing a k6 `options` block and needs to know
  which field expresses a flat concurrency level, a fixed iteration count, a
  time-bounded run, or a multi-phase ramp.
- The caller is uncertain how `vus`, `iterations`, `duration`, and `stages`
  relate — for example, whether to set a flat `vus`/`duration` pair or a
  `stages` array.
- Someone needs to model a realistic load curve with distinct phases such as
  warm-up, steady state, and ramp-down, and must map each phase to a stage
  entry.

## Procedure

### Step 1 — Identify the intended load shape

Ask (or infer) which of the three basic shapes the caller needs:

| Shape | Characteristics | Fields to use |
|-------|----------------|---------------|
| Flat for a period | Fixed concurrency, time-bounded | `vus` + `duration` |
| Fixed-repeat | Run the scenario N times | `iterations` (optionally with `vus`) |
| Phased ramp | VU count rises, holds, or falls across distinct intervals | `stages` array |

If the caller provides only a rough description, clarify the shape before
recommending specific field values.

### Step 2 — Set `vus` for flat concurrency

`vus` is the number of virtual users running the default function
concurrently. Each VU represents one concurrent user executing the test
script (k6-c007, source h0006). It takes an integer value; the default is 1
(k6-c008).

Use `vus` when the desired concurrent-user count is constant throughout the
run:

```js
export const options = {
  vus: 10,
};
```

When `vus` is set without `duration` or `stages`, k6 runs one iteration per
VU and stops. Pair it with `duration` to keep VUs active for a fixed period.

### Step 3 — Set `iterations` for a fixed repeat count

`iterations` is the number of times the scenario or set of actions repeats
during the test (k6-c009, source h0008). It takes an integer value; the
default is 1. Setting it to 10 causes the scenario to execute 10 times in
total across all VUs (k6-c010).

```js
export const options = {
  vus: 5,
  iterations: 10,
};
```

Use `iterations` when the goal is "run the scenario exactly N times" rather
than "run for a given period". If both `vus` and `iterations` are set, k6
distributes the iterations across the available VUs.

### Step 4 — Set `duration` for a time-bounded run

`duration` is the total time for which a load test runs; it controls how
long the VUs continue executing the scenario (k6-c011, source h0010). The
value is a time string expressed in seconds or minutes, for example `'30s'`
or `'5m'` (k6-c012).

```js
export const options = {
  vus: 10,
  duration: '1m',
};
```

Pair `duration` with `vus` for a flat-concurrency, time-bounded run. Do not
combine `duration` with `stages`; when `stages` is present it controls the
run length implicitly through the sum of the stage durations.

### Step 5 — Build a `stages` array for a phased load profile

`stages` defines the different phases of a load test; each stage has its own
`duration` and `target` virtual-user count, enabling realistic patterns such
as gradual ramp-up, sustained load, and ramp-down (k6-c013, source h0012).
`stages` is also a shortcut for the underlying ramping-vus executor (k6-c047,
source h0057).

Each stage object requires exactly two fields:

- **`duration`** — how long this phase lasts, expressed as a time string.
- **`target`** — the VU count to ramp toward by the end of this phase
  (k6-c015, source h0016).

k6 interpolates the active VU count linearly from the previous stage's
endpoint to the current stage's `target` across the stage's `duration`.
Setting `target: 0` in the final stage ramps all VUs back to zero, which is
the standard ramp-down pattern (k6-c016, source h0017).

**Constructing the array** (k6-c014, sources h0013 + c0014):

```js
export const options = {
  stages: [
    { duration: '1m', target: 100 }, // ramp up to 100 VUs over 1 minute
    { duration: '2m', target: 200 }, // continue ramping to 200 VUs over 2 minutes
    { duration: '1m', target: 0 },   // ramp down to 0 VUs over 1 minute
  ],
};
```

Map the caller's described phases to stage entries in sequence. The total run
time is the sum of all stage durations; there is no separate top-level
`duration` field needed.

**Extended example with a sustain phase** (source c0018):

```js
export const options = {
  stages: [
    { duration: '3m', target: 10 },  // ramp up to 10 VUs
    { duration: '5m', target: 10 },  // hold at 10 VUs
    { duration: '10m', target: 35 }, // ramp further to 35 VUs
    { duration: '3m', target: 0 },   // ramp down to 0
  ],
};
```

A hold phase is expressed by repeating the same `target` value in consecutive
stages with different durations.

### Step 6 — Choose the right construct for the caller's goal

Apply this decision logic when a caller is uncertain which field to use:

- If the VU count should be constant for a fixed duration → `vus` + `duration`.
- If the goal is a precise number of script executions → `iterations` (+ `vus`
  if concurrency matters).
- If the load profile changes in phases (ramp-up, hold, ramp-down) →
  `stages` array.
- If the caller asks about fields not covered here (such as advanced executor
  parameters beyond what `stages` provides), say so rather than inventing
  option names or defaults. The source documents `vus`, `iterations`,
  `duration`, `stages`, and `target` only; do not introduce option names
  absent from the source.

## Inputs

- A description of the desired load profile or behaviour to express: flat,
  fixed-repeat, or a multi-phase ramp.
- The relevant fragment of the k6 `options` object under discussion, if any.
- The specific question being asked about how the fields relate or which
  construct to use.

## Output

A recommendation that:

1. Names each relevant k6 option (`vus`, `iterations`, `duration`, `stages`,
   `target`) using only documented meanings from the source.
2. Shows a matching `options`-object configuration with inline comments that
   label each phase.
3. For a phased load, provides a `stages` array whose entries correspond
   one-to-one to the phases the caller described.
4. Does not name or recommend option fields absent from the source
   (k6-guideline-20260612112658, anchors h0006–h0018 and h0057).

## References

- [k6 terminology glossary](../../references/k6-terminology-glossary.md)

## Provenance

Grounded in principle k6-p004 and its supporting claims k6-c013, k6-c014,
k6-c015, k6-c047 (stages ramp VUs toward target over duration; stages is a
shortcut for the ramping-vus executor). Additional claims k6-c007/c008
(VU definition and integer default), k6-c009/c010 (iterations definition and
default), k6-c011/c012 (duration and time-string format), and k6-c016
(target: 0 ramp-down pattern) provide the supporting context for vus,
iterations, and duration fields.

Evidence records: ev-k6-004 (h0012), ev-k6-005 (h0013 + c0014), ev-k6-006
(h0016), ev-k6-023 (h0057), ev-k6-002 (h0006), ev-k6-003 (h0008).

Source `k6-guideline-20260612112658` is `distillation-only`: all prose is
paraphrased; no verbatim passages of three or more sentences. Code blocks
use standard k6 option names only and are derived from the source examples
at anchors c0014 and c0018.
