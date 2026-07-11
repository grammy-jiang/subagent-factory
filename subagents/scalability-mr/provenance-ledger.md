# Provenance Ledger — scalability-mr

Canonical source of truth: `subagents/scalability-mr/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (524 claims),
`evidence/evidence-records.yaml`, `principles/principles.yaml` (50 principles), and
`sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked layer. The LLM-authored
layer (this profile, faithfulness report, skills, references, and tests) is derived from those
principles and their backing claims/evidence/anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `scalability-rules-67c60e37` | Scalability Rules: 50 Principles for Scaling Web Sites | Martin L. Abbott, Michael T. Fisher | 2011 | distillation-only |
| `scalable-internet-ar-a6c7e769` | Scalable Internet Architectures | Theo Schlossnagle | 2006 | distillation-only |

Both sources are `distillation-only`: content is paraphrased and restructured, never quoted
verbatim. The quote-scan and prompt-injection scans pass over the ingested markdown.

## Profile field → principle traceability

Every load-bearing profile rule traces to one or more promoted principles in
`principles/principles.yaml`, which in turn resolve into `derived_from_claims` in
`analysis/claims.jsonl` and their evidence records. The mapping is recorded per finding in
`reports/faithfulness-report.yaml` (the `note` of each finding names the backing principle and
claim IDs). No profile field value is an orphan.

- `role`, `quality_bar`, `forbidden_behaviours`, `knowledge_partition.always_on` — grounded in the
  50 principles (P001–P050), cited inline by principle ID.
- `knowledge_partition.skills` — eight skills, each grounded in a cluster of principles and their
  claims/evidence/anchors (see each `skills/<slug>/SKILL.md` frontmatter `provenance`).
- `knowledge_partition.references` — three references, grounded the same way.
- `sources[]` — the two source_ids and sha256 digests from `source-pack.manifest.yaml`.

## Version history

### 0.1.0 — 2026-06-21

Initial authored layer over the map→reduce distilled spine. Derived profile, faithfulness report,
eight skills, three references, and the behaviour/golden/principle test suites from the 50
principles. No supersession — first version.
