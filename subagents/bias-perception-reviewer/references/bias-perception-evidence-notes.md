---
name: bias-perception-evidence-notes
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P005
  - P006
  - P007
  - P008
  - P009
  - P010
  - P011
  - P012
  - P013
  - P014
  - P015
  - P016
  - P017
  - P018
  - P019
  - P020
  - P021
  - P022
  - P023
  - P024
  - P025
  - P026
  - P027
  - P028
  - P029
  - P030
  - P031
  - P032
  - P033
  - P034
  - P035
  - P036
  - P037
  - P038
  - P039
  - P040
  - P041
  - P042
  - P043
  - P044
  - P045
  - P046
  - P047
  - P048
  - P049
  - P050
  - P051
  - P052
  - P053
  - P054
  - P055
  - P056
  - P057
  - P058
  - P059
  - P060
  - P061
  - P062
  - P063
  - P064
  - P065
  - P066
  - P067
  - P068
  - P069
  - P070
  - P071
  - P072
  - P073
  - P074
  - P075
  - P076
  - P077
  - P078
  - P079
  - P080
  - P081
  - P082
  - P083
  - P084
  - P085
  - P086
  - P087
  - P088
  - P089
  - P090
  - P091
  - P092
  - P093
  - P094
  - P095
  - P096
  - P097
  - P098
  - P099
  - P100
  - P101
  - P102
  - P103
  - P104
  - P105
  - P106
  - P107
  - P108
  - P109
  - P110
  - P111
  - P112
  - P113
  - P114
  - P115
  - P116
  - P117
  - P118
  - P119
  - P120
  - P121
  - P122
  - P123
  - P124
  - P125
  - P126
  - P127
  - P128
  - P129
  - P130
  - P131
  - P132
  - P133
  - P134
  - P135
  - P136
  - P137
  - P138
  - P139
  - P140
  - P141
  - P142
  - P143
  - P144
  - P145
  - P146
  - P147
  - P148
  - P149
  - P150
  - P151
  - P152
  - P153
  - P154
  - P155
  - P156
  - P157
  - P158
  - P159
  - P160
  - P161
  - P162
  - P163
  - P164
  - P165
  - P166
  - P167
  - P168
  - P169
  - P170
  - P171
  - P172
  - P173
  - P174
  - P175
  - P176
  - P177
  - P178
  - P179
  - P180
  - P181
  - P182
  - P183
  - P184
  - P185
  - P186
  - P187
  - P188
  - P189
  - P190
  - P191
  - P192
  - P193
  - P194
  - P195
  - P196
  - P197
  - P198
  - P199
  - P200
  claims: []
  evidence: []
  source_anchors: []
  authored_from_digest: 48ff9b7fa0eadd8aed6f9b9d6a9fa7883957551ae3dac81b9673b1b416eed4cf
---

# Bias & Perception Evidence Notes

How the principles are grounded and how to keep findings faithful to the sources.

## Grounding chain

Each principle in `principles/principles.yaml` carries `derived_from_claims`; every claim resolves into `analysis/claims.jsonl`, and claims carry evidence in `evidence/evidence-records.yaml` and chunk anchors in `sources/anchors/*.anchors.jsonl`. A finding cites the principle ID; the chain behind it is auditable.

## Sources

- **Tradecraft Primer (CIA)** & **Psychology of Intelligence Analysis (Heuer)** — analytic tradecraft, mind-sets, and structured techniques (ACH, alternative futures).
- **Thinking, Fast and Slow (Kahneman)** — dual-process reasoning, heuristics and biases, prospect theory, framing, anchoring.
- **Superforecasting** & **Expert Political Judgment (Tetlock)** — calibration, foxes vs hedgehogs, track record, active open-mindedness.
- **Perception and Misperception (Jervis)** — attribution of intent, signals, deterrence vs spiral, cognitive consistency between actors.

## Faithfulness rule

No finding states a bias or its correction more strongly than its source supports. Claims about perception stay probabilistic (P108). When sources frame the same error differently, name the framing and its scope rather than assert a single universal law. See `reports/faithfulness-report.yaml` for the per-rule claim-strength check.

