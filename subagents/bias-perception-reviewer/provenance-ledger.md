# Provenance Ledger — bias-perception-reviewer

Every profile field traces to the distilled spine of this package: promoted principles in
`principles/principles.yaml` (each `derived_from_claims` resolves into `analysis/claims.jsonl`),
their evidence in `evidence/evidence-records.yaml`, and chunk anchors in
`sources/anchors/*.anchors.jsonl`. No profile value is an orphan.

## Sources

| source_id | title | rights_status |
|-----------|-------|---------------|
| tradecraft-primer-6ec9d9fb | A Tradecraft Primer: Structured Analytic Techniques (CIA) | distillation-only |
| psychology-of-intell-3a2b4f82 | Psychology of Intelligence Analysis (Heuer) | distillation-only |
| thinking-fast-and-sl-d88ef771 | Thinking, Fast and Slow (Kahneman) | distillation-only |
| superforecasting-e3c7c0b4 | Superforecasting (Tetlock & Gardner) | distillation-only |
| expert-political-jud-5da0a790 | Expert Political Judgment (Tetlock) | distillation-only |
| perception-and-mispe-a445f294 | Perception and Misperception in International Politics (Jervis) | distillation-only |

All sources are `distillation-only`: distillation is permitted; verbatim quotation is not. The
verbatim `sources/original` and `sources/markdown` layers are withheld from any rights-clean export
per `.claude/rules/rights-and-quotation-policy.md`.

## Field → grounding

Profile rules are grounded in promoted principles, cited by ID in each rule. The load-bearing map:

| Profile field | Grounded in principles |
|---------------|------------------------|
| role | P001, P006, P049, P086, P100, P108, P128, P199 (bias review, calibration, perception, scope) |
| quality_bar[0] (vivid/anecdotal vs base rate; sample bias) | P001, P047, P062, P199 |
| quality_bar[1] (granular numeric probability; base-rate anchored) | P049, P067, P123, P191, P199 |
| quality_bar[2] (alternative hypotheses; structured technique) | P008, P010, P100, P141 |
| quality_bar[3] (motivated reasoning; slow-update vs strong prior) | P074, P076, P167, P193, P200 |
| quality_bar[4] (situational vs dispositional; centralized-actor; intent) | P013, P108, P109, P128 |
| forbidden_behaviours | P006, P052, P076, P086, P108 |
| knowledge_partition.always_on | the ten skills below, covering all 200 principles |

## Skill partition → principles

Each skill in `skills/` groups a disjoint set of principles; together they cover all 200. The exact
map is `.build/authoring/partition.json` (generated). Summary:

| Skill | Principles |
|-------|------------|
| dual-process-heuristics-and-cognitive-ease | P006 P018 P019 P022 P052 P056 P057 P064 P065 P066 P071 P072 P119 P140 P144 P145 P146 P178 P179 P182 P183 P186 |
| judgment-anchoring-and-base-rates | P008 P020 P025 P047 P082 P101 P102 P123 P143 P180 P199 |
| calibration-and-probabilistic-estimation | P049 P067 P120 P151 P190 P191 P198 P200 |
| forecasting-judgment-foxes-and-track-record | P073 P078 P083 P085 P086 P087 P103 P121 P122 P152 P153 P154 P155 P156 P187 P188 P192 P197 |
| mind-sets-and-structured-techniques | P009 P010 P100 P111 P112 P139 P142 P163 P165 P171 P184 P185 |
| motivated-reasoning-and-belief-perseverance | P014 P016 P021 P026 P027 P036 P041 P048 P070 P074 P075 P076 P077 P095 P107 P113 P114 P115 P135 P141 P167 P169 P173 P193 P194 |
| perception-attribution-of-intent-and-signaling | P004 P005 P007 P013 P017 P023 P024 P029 P032 P034 P035 P068 P069 P081 P091 P092 P096 P108 P109 P110 P125 P127 P128 P130 P133 P136 P138 P157 P158 P159 P164 P166 P168 P170 P174 P175 P176 |
| prospect-theory-framing-and-decision-weights | P040 P044 P046 P050 P053 P084 P104 P105 P116 P117 P118 P131 P147 P148 P149 P150 P181 P189 P196 |
| deterrence-spiral-and-strategic-interaction | P031 P033 P042 P045 P051 P054 P059 P060 P063 P079 P080 P088 P089 P090 P093 P094 P097 P106 P126 P129 P132 P134 P160 P161 P162 P177 |
| historical-analogy-learning-and-hindsight | P001 P002 P003 P011 P012 P015 P028 P030 P037 P038 P039 P043 P055 P058 P061 P062 P098 P099 P124 P137 P172 P195 |

## Distilled spine (deterministic, unchanged)

200 principles, 2,889 claims, 1,482 evidence records, 163 chunk anchors across the six sources above.
Built by the map→reduce pipeline; not edited by the authoring layer.

## Version history

Supersession rule (`.claude/rules/generated-artifact-policy.md`): profile decisions are never
silently overwritten. New versions append here.

- **1.0.0** — Initial release. LLM-authored layer (profile, faithfulness, skills, references, tests,
  adapter) built over the deterministic spine.

## Version History

- **1.0.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.
