# Provenance Ledger — mcp-protocol-advisor

Canonical source of truth: `subagents/mcp-protocol-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (632 claims),
`evidence/evidence-records.yaml` (620 records), `principles/principles.yaml` (253
principles, 220 high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic,
validator-checked layer. The LLM-authored layer (this profile, the faithfulness report, the
13 skills, 2 references, and the tests) is derived from those
principles and their backing claims, evidence, and anchors.

## Sources

The 20 sources are the pages of the Model Context Protocol specification (revisions 2024-11-05
through 2025-11-25), ingested as Markdown. All are `distillation-only`: content is paraphrased and
restructured, never quoted verbatim.

| source_id | title | year | rights_status |
|-----------|-------|------|---------------|
| `mcp-spec-overview-37bf1590` | Model Context Protocol Specification — Overview | 2025 | distillation-only |
| `mcp-spec-architectur-0b6ac42d` | Model Context Protocol Specification — Architecture | 2025 | distillation-only |
| `mcp-spec-basic-overv-a504a340` | Model Context Protocol Specification — Base Protocol Overview | 2025 | distillation-only |
| `mcp-spec-basic-lifec-88472000` | Model Context Protocol Specification — Lifecycle | 2025 | distillation-only |
| `mcp-spec-basic-trans-5a86d66a` | Model Context Protocol Specification — Transports | 2025 | distillation-only |
| `mcp-spec-util-cancel-a5220827` | Model Context Protocol Specification — Utilities: Cancellation | 2025 | distillation-only |
| `mcp-spec-util-ping-2702be9d` | Model Context Protocol Specification — Utilities: Ping | 2025 | distillation-only |
| `mcp-spec-util-progre-8f5b562e` | Model Context Protocol Specification — Utilities: Progress | 2025 | distillation-only |
| `mcp-spec-util-tasks-8df00bee` | Model Context Protocol Specification — Utilities: Tasks | 2025 | distillation-only |
| `mcp-spec-client-elic-01bfb448` | Model Context Protocol Specification — Client Features: Elicitation | 2025 | distillation-only |
| `mcp-spec-client-root-992d141a` | Model Context Protocol Specification — Client Features: Roots | 2025 | distillation-only |
| `mcp-spec-client-samp-3498fca5` | Model Context Protocol Specification — Client Features: Sampling | 2025 | distillation-only |
| `mcp-spec-server-over-ddb8b9b4` | Model Context Protocol Specification — Server Features Overview | 2025 | distillation-only |
| `mcp-spec-server-prom-a17e8901` | Model Context Protocol Specification — Server Features: Prompts | 2025 | distillation-only |
| `mcp-spec-server-reso-37de412b` | Model Context Protocol Specification — Server Features: Resources | 2025 | distillation-only |
| `mcp-spec-server-tool-8ed43301` | Model Context Protocol Specification — Server Features: Tools | 2025 | distillation-only |
| `mcp-spec-server-util-88cd5f33` | Model Context Protocol Specification — Server Utilities: Completion | 2025 | distillation-only |
| `mcp-spec-server-util-b287e6ef` | Model Context Protocol Specification — Server Utilities: Logging | 2025 | distillation-only |
| `mcp-spec-server-util-e59fbe4c` | Model Context Protocol Specification — Server Utilities: Pagination | 2025 | distillation-only |
| `mcp-spec-versioning-4f99907b` | Model Context Protocol Specification — Versioning and Revision History | 2025 | distillation-only |

## Authored-layer mapping

Each principle is assigned to exactly one skill by the specification page its backing claims come
from (majority source page).

| skill / reference | principles |
|-------------------|-----------|
| `skills/base-protocol-and-messages` | 25 (P001…P239) |
| `skills/architecture-and-trust-model` | 17 (P015…P167) |
| `skills/connection-lifecycle-and-capabilities` | 11 (P009…P197) |
| `skills/transports` | 25 (P032…P245) |
| `skills/cancellation-ping-and-progress` | 21 (P006…P208) |
| `skills/long-running-tasks` | 28 (P008…P253) |
| `skills/server-tools` | 12 (P014…P190) |
| `skills/server-resources-and-prompts` | 29 (P002…P250) |
| `skills/server-completion-logging-and-pagination` | 25 (P022…P252) |
| `skills/elicitation` | 21 (P019…P220) |
| `skills/sampling` | 17 (P003…P224) |
| `skills/roots` | 10 (P043…P247) |
| `skills/versioning-and-conformance` | 12 (P012…P238) |
| `references/mcp-protocol-principles-index` | all 253 |
| `references/mcp-conformance-evidence-notes` | high-confidence principles |

## Faithfulness

`reports/faithfulness-report.yaml` grades every load-bearing profile rule against the promoted
principles on the claim-strength scale. All findings are `WITHIN_SCOPE` (the profile narrows the
specification to conformance review; no rule is stronger than its evidence). `source_anchors` are
omitted from the report deliberately — provenance is carried in each note via principle + claim IDs.

## Version History

| version | date | change |
|---------|------|--------|
| 0.1.0 | 2026-07-05 | Initial authored layer over the map→reduce distilled spine (MCP specification, 20 pages, 253 principles). |
