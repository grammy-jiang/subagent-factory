# Provenance Ledger — MCP Quality Advisor

**Subagent slug:** `mcp-quality-advisor`
**Profile version:** 0.1.0
**Generated:** 2026-07-05

This package distills 29 primary and secondary sources on Model Context Protocol (MCP)
servers and tool interfaces — benchmarks, tool-description-quality audits, runtime-fault taxonomies,
conformance/validation frameworks, Python/TypeScript SDK testing guides, serverless-deployment
studies, and agent-evaluation research — into an evidence-backed advisor. The distilled spine —
`analysis/claims.jsonl` (C#####), `evidence/evidence-records.yaml` (E#####),
`principles/principles.yaml` (P001–P200), and `sources/anchors/*.anchors.jsonl`
(`<sha12>-cNNNN`) — was assembled by the map→reduce build and is **not modified** here. This ledger
records how the LLM-authored layer (profile, skills, references, tests, faithfulness report) was
derived from that spine.

---

## Source Registry

| ID | Title | Authority | Rights |
|----|-------|-----------|--------|
| mcp-universe-2508-14-46bbfd26 | mcp-universe-2508.14704 | secondary | distillation-only |
| livemcpbench-2508-01-eaca3d50 | livemcpbench-2508.01780 | secondary | distillation-only |
| mcp-atlas-2602-00933-b6b7517b | mcp-atlas-2602.00933 | secondary | distillation-only |
| demystifying-evals-f-ba55f4c0 | demystifying-evals-for-ai-agents | secondary | distillation-only |
| mcp-servers-evaluati-28f43d99 | mcp-servers-evaluation-report-2504.11094 | secondary | distillation-only |
| mcp-tool-description-1a9237db | mcp-tool-descriptions-are-smelly-2602.14878 | secondary | distillation-only |
| docs-to-descriptions-b348d1cb | docs-to-descriptions-smell-aware-2602.18914 | secondary | distillation-only |
| mcp-runtime-faults-t-22497acd | mcp-runtime-faults-taxonomy-2606.05339 | secondary | distillation-only |
| mcp-vision-systems-a-c9831865 | mcp-vision-systems-audit-2509.22814 | secondary | distillation-only |
| judge-reliability-ha-53171e80 | judge-reliability-harness-2603.05399 | secondary | distillation-only |
| github-mcp-offline-e-4910b3c6 | github-mcp-offline-evaluation | secondary | distillation-only |
| code-execution-with-c3493427 | code-execution-with-mcp | secondary | distillation-only |
| advanced-tool-use-5e5bb110 | advanced-tool-use | secondary | distillation-only |
| promcp-token-flows-l-dfe0874c | promcp-token-flows-latency | secondary | distillation-only |
| semantic-tool-discov-f73c30b5 | semantic-tool-discovery-vector-mcp | secondary | distillation-only |
| tool-attention-dynam-b0365df1 | tool-attention-dynamic-gating-lazy-schema | secondary | distillation-only |
| workflow-engine-mcp-2d3959ea | workflow-engine-mcp | secondary | distillation-only |
| faas-platforms-mcp-a-48702eca | faas-platforms-mcp-agentic | secondary | distillation-only |
| harness-mcp-server-r-eed3b927 | harness-mcp-server-redesign | secondary | distillation-only |
| speakeasy-reduce-tok-bbac4c57 | speakeasy-reduce-token-usage-100x | secondary | distillation-only |
| mcp-conformance-fram-a136f0ee | mcp-conformance-framework | secondary | distillation-only |
| mcp-inspector-docs-2eae1d32 | mcp-inspector-docs | secondary | distillation-only |
| mcp-inspector-repo-799a28bd | mcp-inspector-repo | secondary | distillation-only |
| mcp-debugging-guide-9a2be171 | mcp-debugging-guide | secondary | distillation-only |
| mcp-python-sdk-testi-1d5543a1 | mcp-python-sdk-testing | secondary | distillation-only |
| mcp-python-sdk-inmem-19746336 | mcp-python-sdk-inmemory-client | secondary | distillation-only |
| mcp-typescript-sdk-p-c3e4e099 | mcp-typescript-sdk-protocol | secondary | distillation-only |
| mcp-typescript-sdk-i-911ddde2 | mcp-typescript-sdk-inmemory-test | secondary | distillation-only |
| mcp-validation-redha-74c00514 | mcp-validation-redhat | secondary | distillation-only |

All sources are `distillation-only`: generated artifacts paraphrase and restructure; no verbatim
source quotation appears (verified by `quote_scan`).

---

## Authored-layer derivation

- **profile.yaml** — hand-derived from the 200 principles: `role`, scope, `quality_bar`,
  `forbidden_behaviours`, and mode triggers each cite the governing principle ids; `sources[]`
  mirrors the manifest source ids and sha256.
- **skills/** — five skills partition all 200 principles by theme; each `SKILL.md` frontmatter cites
  its principles plus the real claim/evidence/anchor ids they derive from.
- **references/** — three references (protocol-compliance checklist, tool-description rubric,
  evaluation & judge reference) ground the review/eval tables in the same principles.
- **tests/** — `principle-behaviour-tests.yaml` covers every principle (one `principle_id` entry
  each); `golden-tests.yaml` exercises the routing/mode surface.
- **reports/faithfulness-report.yaml** — every gradable profile rule graded against the principles;
  no rule exceeds its evidence.

## Principle → skill map

| Skill | # principles | span |
|-------|--------------|------|
| `designing-mcp-tool-descriptions` | 39 | P002–…P191 |
| `scaling-tool-discovery-and-context` | 45 | P001–…P186 |
| `verifying-mcp-protocol-compliance` | 59 | P005–…P196 |
| `evaluating-mcp-agents-and-judges` | 42 | P008–…P198 |
| `operating-mcp-on-serverless` | 15 | P044–…P200 |

---

## Version History

### 0.2.2 — 2026-07-25

- Restated the `router_description` out-of-scope clause by capability instead of naming sibling packages: generated subagents are independent of one another and the orchestrating session does the routing, so a routing string says what this agent does not cover rather than asserting which other package owns it. Also added that `router_description` in the first place (same day), for the routing-truncation reason above. Boundary content unchanged; adapter re-exported. Supersedes only same-day wording, not any principle or rule.

### 0.1.0 — 2026-07-05
- Initial authored layer over the map→reduce distilled spine (29 sources, 200 principles).
