# Provenance Ledger — agent-skills-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, and `source_of_truth_policy` value
cites the promoted principle(s) it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`,
`outputs` — carry no inline tags, per repo convention.)

## Sources

Fifty-nine ingested primary and secondary **distillation-only** sources on Agent Skills, subagents,
MCP, evaluation, context engineering, and instruction files, spanning the Claude (Code + API), OpenAI
Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure
only, no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`; enforced by
`quote_scan`). The full source list with sha256 and rights lives in `profile.yaml` `sources[]` and
`source-pack.manifest.yaml`.

## Distillation

Spine: 150 promoted principles (P001-P150; 126 high-confidence) over
2059 atomic claims, with evidence records and chunk anchors. The 150 principles are
partitioned across 4 skills (each principle owned by exactly one skill); three references
index the authoring, deploying, and orchestrating slices.

| skill | principles | first ids |
|-------|-----------:|-----------|
| authoring-agent-skills | 43 | P001, P002, P003, P004, P006, P007… |
| evaluating-and-iterating-on-skills | 22 | P010, P012, P030, P033, P034, P035… |
| deploying-skills-across-platforms | 35 | P016, P018, P026, P027, P028, P036… |
| orchestrating-subagents-and-mcp | 50 | P005, P008, P009, P013, P023, P029… |

## Version History

- **0.3.0** (2026-07-25) — Fold-in of the official Anthropic *skill-creator* SKILL.md (59th source):
  its authoring loop (capture intent, interview, draft, evaluate, iterate), skill-writing guide, and
  description optimizer. The map->reduce rebuild re-clustered and renumbered the distilled spine
  (P001-P150; 2059 claims), so the LLM-authored layer was regenerated against
  it: the four skills, three references, faithfulness report, and the golden + one-per-principle
  behaviour tests re-grounded in the current principle ids; skill/reference `authored_from_digest`
  re-stamped; the profile's rule citations remapped, the 59th source added to `sources[]`, and the
  adapter re-exported. No prior profile decisions superseded.
- **0.2.1** (2026-07-25) — Added `router_description` to `profile.yaml`; adapter re-exported. No
  principle, rule, skill, or source changed.
- **0.2.0** (2026-07-25) — Fold-in of *new-rules-of-context-engineering-claude-5* (58th source); the
  distilled spine was re-clustered and the LLM-authored layer regenerated against it.
- **0.1.1** (2026-07-04) — PR #52 review fixes (citation format, self-check report); no behavioural
  change.
- **0.1.0** (2026-07-04) — Initial LLM-authored layer over the pre-built distilled spine.
