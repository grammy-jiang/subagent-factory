---
name: tool-description-quality-rubric
kind: reference
status: ready
provenance:
  principles:
  - P028
  - P029
  - P030
  - P038
  - P081
  - P133
  - P177
  - P179
  - P187
  - P188
  - P189
  - P190
  - P191
  - P054
  - P055
  - P113
  - P036
  - P039
  - P020
  - P021
  - P024
  - P031
  - P040
  - P080
  - P083
  - P084
  - P142
  - P003
  claims:
  - C00342
  - C00343
  - C00344
  - C00345
  - C00346
  - C00347
  - C00394
  - C00395
  - C00396
  - C00397
  - C00398
  - C00399
  - C00366
  - C00367
  - C00370
  - C00371
  - C00377
  - C00380
  evidence:
  - E00164
  - E00165
  - E00166
  - E00167
  - E00168
  - E00169
  - E00208
  - E00209
  - E00210
  - E00211
  - E00212
  - E00213
  - E00186
  - E00187
  - E00188
  source_anchors:
  - 1a9237dbcad1-c0002
  - 1a9237dbcad1-c0005
  - 1a9237dbcad1-c0004
  authored_from_digest: 9c637b41cf2be4c9764e91e22aafb3c61bfb0144b3e6a23a1acbf9f66a83e8a9
---

# MCP Tool-Description Quality Rubric

A graded rubric for scoring an MCP tool description. Score each component on a 5-point scale with 3 as minimum viable; the description trio is the retrieval ceiling for tool use [P081], [P142], [P003]. Assume quality is poor by default and review every description [P080].

## Components to score (retain Purpose always)

- Purpose — the function, behaviour, and return data; never dropped, even under a tight budget [P030], [P187].
- Usage Guidelines — when to use and when not to use, plus disambiguation from sibling tools [P038].
- Information Completeness — everything the agent needs to build a valid call and interpret the result [P054].
- Examples — lowest-priority, safest to omit under constraints; ground them in real executions when present [P190], [P036].
- Parameter Explanation — prune before other components when tight, since the input schema already carries structure [P189].

## Smell checklist (fix the prevalent ones first)

- Unstated Limitations (~90% of descriptions) — state constraints and failure conditions [P028].
- Missing Usage Guidance — add when-to-use / when-not-to-use [P028], [P191].
- Inconsistency — describe only behaviours the implementation actually has [P021].
- Verbosity / low signal — maximise signal-to-noise; cut redundancy, hedge words (maybe, probably), and clutter [P040], [P113].
- Apply a well-defined analytic rubric rather than open-ended scoring; treat a smell as a risk signal, not a deterministic predictor [P177], [P133].

## Authoring practice

- Make description authoring a first-class phase, co-equal with implementation and testing [P055].
- Give each tool a unique, semantically meaningful name distinct within its namespace [P031].
- Ground Examples and Limitations in observed executions and source code, not the description alone [P039].
- Use input examples to teach conventions a schema cannot express — optional-field patterns, nested objects, formats [P024].
- Report and coverage-threshold decisions are reporting choices on a real-valued rubric score [P179].
- Expect a measurable payoff from a standards-compliant description among functionally equivalent tools [P084], [P020], [P029].

## Grounding

Principles: P028, P029, P030, P038, P081, P133, P177, P179, P187, P188, P189, P190, P191, P054, P055, P113, P036, P039, P020, P021, P024, P031, P040, P080, P083, P084, P142, P003. Sources are distillation-only; no verbatim source quotation.
