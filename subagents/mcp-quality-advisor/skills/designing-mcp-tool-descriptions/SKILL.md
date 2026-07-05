---
name: designing-mcp-tool-descriptions
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P003
  - P017
  - P020
  - P021
  - P022
  - P023
  - P024
  - P028
  - P029
  - P030
  - P031
  - P032
  - P036
  - P038
  - P039
  - P040
  - P054
  - P055
  - P079
  - P080
  - P081
  - P083
  - P084
  - P100
  - P111
  - P113
  - P128
  - P133
  - P134
  - P137
  - P142
  - P177
  - P179
  - P187
  - P188
  - P189
  - P190
  - P191
  claims:
  - C00033
  - C01044
  - C01045
  - C01050
  - C01051
  - C01052
  - C01054
  - C00281
  - C00282
  - C00303
  - C00680
  - C00681
  - C00682
  - C00683
  - C00579
  - C00583
  - C00607
  - C00609
  evidence:
  - E00002
  - E00646
  - E00647
  - E00652
  - E00653
  - E00654
  - E00656
  - E00114
  - E00115
  - E00134
  - E00432
  - E00433
  - E00434
  - E00435
  - E00362
  source_anchors:
  - 46bbfd26b8df-c0001
  - eed3b927f923-c0000
  - 1a9237dbcad1-c0000
  - 4910b3c691ad-c0000
  - c983186538ad-c0000
  authored_from_digest: 81c0bbd0312f7da17e9916811614358703397eb444a161b3eddd3f5f2aa4e69e
---

# Skill: designing-mcp-tool-descriptions

## Purpose

Design and review the metadata surface of an MCP tool — its name, description, parameter schema, annotations, and examples — so a model reliably selects the right tool and builds valid arguments. The description trio is the primary and often only basis the model has for a call, so quality here sets the ceiling on tool use [P003], [P083], [P142].

## When to use

- You are authoring a new MCP tool or reviewing an existing tool's description and schema.
- A model picks the wrong tool, skips a step, or emits malformed/missing arguments.
- You are auditing a tool surface for description smells or missing components.

## Procedure

1. **Minimize and disambiguate the tool set.** Expose as few tools as you can: every name, description, schema, and annotation loads into context on connect and taxes reasoning before any prompt, and efficiency drops as selection complexity rises — consolidating many narrow tools into a few higher-level ones cuts tool-definition context sharply [P002]. Give each tool a unique, semantically meaningful name that is distinct within its namespace [P031].
2. **Treat name+description+schema as the selection lever.** Keep instructions simple and precise; expect that even small edits — tightening wording, merging similar tools — move evaluation results significantly, while inaccurate descriptions cause wrong-tool choices and bad arguments [P003], [P083]. Assume quality is poor by default and always review it, regardless of vendor or official origin [P079], [P080].
3. **Score against a component rubric, not a yes/no check.** Hold each component to its bar on a graded (5-point) scale, treating 3 as minimum viable [P081], [P038]: Purpose (function, behaviour, returns), Usage Guidelines (when to use and not use, disambiguation), Information Completeness (everything needed to build a valid call and read the result) [P054], [P187]. Always retain Purpose; select the minimal effective component set per domain-model pair [P030].
4. **Detect and fix the prevalent smells first.** Prioritise the most common description smells: Unstated Limitations (~90%), Missing Usage Guidance, then consistency and conciseness issues [P028], [P133]. For consistency, describe only behaviours the implementation actually has [P021]; for conciseness, maximise signal-to-noise and cut redundancy, hedge words, and clutter [P040], [P113].
5. **Ground examples and limitations in real executions.** Do not write Examples or full Limitations from the description alone — ground them in observed tool executions and, where possible, the tool's source code [P036], [P039], [P111]. Use input examples to teach conventions a schema cannot express: optional-field patterns, nested objects, formats [P024].
6. **Get arguments and optional fields right.** Validate parameters against each tool's constraints before invoking, and when building calls from form inputs omit optional fields with empty values unless the schema requires them [P100]. Diagnose argument faults with targeted metrics — hallucinated arg names, wrong values, missing required args [P137], [P128].
7. **Extend schemas for multimodal tools.** For vision and other multimodal tools, add explicit semantic-role, modality, and coordinate-system fields, and bring resizing, unit conversion, and schema coercion inside declared tool contracts — undocumented out-of-band handling is a recurring failure signature [P017], [P022], [P023], [P134], [P032].
8. **Make description authoring a first-class phase.** Treat description authoring as co-equal with implementation and testing; run rubric-based smell detection in review or CI, and expect a measurable payoff from a standards-compliant description among functionally equivalent tools [P055], [P029], [P084]. Prune lowest-value components (Examples, then Parameter Explanation) first under a tight budget [P190], [P189], [P020].

## Pitfalls / anti-patterns

- Assuming an official or vendor server's descriptions are good — study data shows they often are not [P080].
- Editing a description without measuring the effect; use execution-based metrics, not intuition [P037] (see mcp-evaluation-and-judge-reference).
- Dropping Purpose to save tokens — it is the one component to always retain [P030].

## Grounding

Principles: P002, P003, P017, P020, P021, P022, P023, P024, P028, P029, P030, P031, P032, P036, P038, P039, P040, P054, P055, P079, P080, P081, P083, P084, P100, P111, P113, P128, P133, P134, P137, P142, P177, P179, P187, P188, P189, P190, P191. Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.
