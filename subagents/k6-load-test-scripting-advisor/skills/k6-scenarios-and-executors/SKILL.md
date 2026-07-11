---
name: k6-scenarios-and-executors
kind: skill
status: ready
provenance:
  principles:
  - k6-p008
  claims:
  - k6-c036
  - k6-c037
  - k6-c046
  - k6-c047
  source_anchors:
  - k6-guideline-20260612112658-h0040
  - k6-guideline-20260612112658-h0056
  - k6-guideline-20260612112658-h0057
  authored_from_digest: d74845d26d67a5ce0de20c5e5205557d21f48714bc589d9964bcf7c8a9a7a84c
---

# k6 Scenarios and Executors

## Purpose

Guide the caller in configuring k6 scenarios — independently scheduled user journeys that
execute in parallel within a single test script — and in choosing the ramping-vus executor
when the number of virtual users must change gradually over time. The skill covers the
`options.scenarios` structure, the relationship between the ramping-vus executor and the
`stages` shortcut, and the boundary of what the cheat-sheet source documents.

## When to use

- The caller needs to run more than one user journey in the same k6 script and wants each
  journey to have its own VU count and iteration schedule.
- The caller wants to vary VU count over time within a scenario and is deciding between the
  top-level `stages` shortcut and the explicit `ramping-vus` executor block.
- The caller asks what a k6 scenario is, why scenarios run in parallel, or how the
  ramping-vus executor relates to the stages option.
- A single default scenario with fixed VUs is already in place and the caller is now adding
  a second journey that needs independent scheduling.

## Procedure

### Step 1 — Decide whether one scenario is sufficient

A single load pattern (fixed VUs for a duration, or a ramp expressed with the top-level
`stages` option) does not require the `scenarios` key. Reach for `scenarios` when two or
more user journeys need independent VU counts, iteration budgets, or execution schedules
within the same test run.

### Step 2 — Understand what a scenario is

A scenario represents a specific user journey or flow during a load test. It provides
detailed configuration options for virtual users and iteration schedules. Each named
scenario in `options.scenarios` executes its own JavaScript function independently and in
parallel with the other scenarios defined in the same script (source anchor
k6-guideline-20260612112658-h0040, claims k6-c036, k6-c037, principle k6-p008).

### Step 3 — Structure `options.scenarios`

Place each journey as a named key under `options.scenarios`. The key name is arbitrary;
choose something that describes the journey. A minimal two-scenario structure looks like:

```js
export const options = {
  scenarios: {
    browse:  { /* executor and schedule for the browsing journey */ },
    checkout: { /* executor and schedule for the checkout journey */ },
  },
};
```

Each scenario entry requires at least an `executor` field to select the execution model.
For executor parameters beyond what the cheat sheet documents, consult the k6.io docs.

### Step 4 — Choose the ramping-vus executor for gradual VU changes

When a scenario must vary its VU count over time — increasing to simulate a surge, then
decreasing — use the `ramping-vus` executor. The ramping-vus executor allows a flexible
number of VUs to perform iterations for a set duration, controlling VU behaviour across
different time periods. It is especially useful when VUs should gradually increase or
decrease within specific intervals (source anchor k6-guideline-20260612112658-h0057,
claim k6-c046, principle k6-p008).

```js
export const options = {
  scenarios: {
    ramp_up_journey: {
      executor: 'ramping-vus',
      stages: [
        { duration: '30s', target: 20 },
        { duration: '1m',  target: 20 },
        { duration: '30s', target: 0 },
      ],
    },
  },
};
```

The `stages` array here follows the same `{ duration, target }` semantics documented for
the top-level stages option: each stage ramps VU count toward `target` over its `duration`.

For additional ramping-vus parameters (such as `startVUs` or `gracefulRampDown`), see the
k6.io docs — those parameters are not covered in the cheat-sheet source.

### Step 5 — Use the top-level `stages` shortcut when a single ramp is enough

The `stages` option in the top-level `options` block is a convenience shortcut for the
ramping-vus executor (source anchor k6-guideline-20260612112658-h0057, claim k6-c047,
principle k6-p004). Prefer it when:

- Only one load shape is needed across the entire test, and
- The full `ramping-vus` executor block with its own named scenario is unnecessary.

Use the explicit `ramping-vus` executor block within `scenarios` when:

- Two or more independent journeys must run in parallel, or
- A specific named scenario needs its own ramping schedule separate from others.

### Step 6 — Stay within documented features

The cheat-sheet source documents:
- The scenario concept and parallel execution model (h0040).
- The concept of ramping — gradually increasing or decreasing VU load over time (h0056).
- The ramping-vus executor and the `stages` shortcut (h0057).

It does not document other executors (constant-vus, constant-arrival-rate, etc.),
distributed or cloud execution, custom JavaScript beyond the documented options, or
executor parameters beyond what is shown above. State this limit clearly if the caller
asks about undocumented features.

## Inputs

- The set of user journeys to model and whether they must run in parallel within one script.
- The desired VU-over-time shape for each journey (flat, ramp-up, ramp-down, or multi-phase).
- The relevant `options.scenarios` or executor fragment under discussion, if one exists.

## Output

A recommendation that:

1. Names the k6 constructs used (scenario, ramping-vus executor, stages shortcut).
2. Shows the matching `options.scenarios` structure — one named entry per independent
   journey, and for a gradual VU shape the `ramping-vus` executor with a `stages` array.
3. Notes where the cheat-sheet source ends and the k6.io docs are the appropriate next
   reference (for executor parameters not covered by the source).

## References

- [k6 terminology glossary](../../references/k6-terminology-glossary.md)
- [k6 options and stages configuration](../k6-options-and-stages-configuration/SKILL.md)
- k6.io docs: executors reference — for parameters such as `startVUs`, `gracefulRampDown`,
  and non-ramping executor types not covered by the cheat-sheet source.

## Provenance

Principle k6-p008 (scenarios configure distinct load patterns; each scenario executes an
independent JavaScript function in parallel; ramping-vus is the underlying mechanism for
gradual VU ramp-up or ramp-down). Derived from claims k6-c036 and k6-c037 (scenario
definition and parallel execution, ev-k6-018/ev-k6-019, source anchor
k6-guideline-20260612112658-h0040) and k6-c046 and k6-c047 (ramping-vus executor and
stages shortcut, ev-k6-022/ev-k6-023, source anchors k6-guideline-20260612112658-h0057).
The ramping concept is supported by source anchor k6-guideline-20260612112658-h0056.
Profile `always_on` rule: load shape in options object; scenarios entry in `when_to_use`.
Source rights status is `distillation-only`: all prose paraphrased; no verbatim quotation
of three or more consecutive sentences. Executor parameters not documented in the source
(such as `startVUs`, `gracefulRampDown`) are explicitly deferred to k6.io docs and not
treated as source-supported content.
