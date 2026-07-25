# Provenance Ledger — mcp-security-advisor

Canonical source of truth: `subagents/mcp-security-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (1352 claims),
`evidence/evidence-records.yaml` (969 records), `principles/principles.yaml` (220 principles, 106
high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic, validator-checked
layer. The LLM-authored layer (this profile, the faithfulness report, the eleven skills, two
references, and the tests) is derived from those principles and their backing claims, evidence, and
anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `mcp-spec-basic-autho-b5eaaf20` | MCP Specification — Authorization | Anthropic / MCP | 2025 | distillation-only |
| `mcp-spec-basic-secur-d59e5c41` | MCP Specification — Security Best Practices | Anthropic / MCP | 2025 | distillation-only |
| `cosai-mcp-security-515304c3` | CoSAI — MCP Security | Coalition for Secure AI | 2025 | distillation-only |
| `nsa-csi-mcp-security-dcbba5b2` | NSA CSI — Securing the Model Context Protocol | NSA | 2025 | distillation-only |
| `owasp-mcp-top-10-fa0ccb38` | OWASP MCP Top 10 | OWASP | 2025 | distillation-only |
| `owasp-mcp-security-c-e6ab8dd9` | OWASP MCP Security Cheat Sheet | OWASP | 2025 | distillation-only |
| `owasp-ai-agent-secur-c82772e8` | OWASP AI Agent Security Cheat Sheet | OWASP | 2025 | distillation-only |
| `aaronparecki-fix-oau-8aab5281` | Let's Fix OAuth in MCP | Aaron Parecki | 2025 | distillation-only |
| `parecki-enterprise-r-73827be0` | Enterprise-Ready MCP | Aaron Parecki | 2025 | distillation-only |
| `parecki-mcp-auth-nov-c8cf335b` | MCP Authorization — Nov 2025 Spec | Aaron Parecki | 2025 | distillation-only |
| `vendor-workos-mcp-oa-0d5e0b52` | WorkOS — MCP OAuth Authorization | WorkOS | 2025 | distillation-only |
| `vendor-descope-mcp-a-ff3fcb8b` | Descope — MCP Authorization Spec | Descope | 2025 | distillation-only |
| `vendor-stytch-oauth-93eb31ae` | Stytch — OAuth for MCP | Stytch | 2025 | distillation-only |
| `vendor-auth0-mcp-aut-6ff87e35` | Auth0 — MCP Authorization | Auth0 | 2025 | distillation-only |
| `vendor-wiz-mcp-secur-38612cf3` | Wiz — MCP Security | Wiz | 2025 | distillation-only |
| `invariant-tool-poiso-cf795704` | Invariant Labs — MCP Tool Poisoning Attacks | Invariant Labs | 2025 | distillation-only |
| `invariant-whatsapp-m-357204ac` | Invariant Labs — WhatsApp MCP Exfiltration | Invariant Labs | 2025 | distillation-only |
| `trailofbits-line-jum-6954b218` | Trail of Bits — Line Jumping in MCP | Trail of Bits | 2025 | distillation-only |
| `simonwillison-lethal-867e7bf9` | The Lethal Trifecta for AI Agents | Simon Willison | 2025 | distillation-only |
| `unit42-mcp-prompt-in-b4bcb3ed` | Unit 42 — MCP Prompt Injection via Sampling | Palo Alto Unit 42 | 2025 | distillation-only |
| `arxiv-mcp-landscape-347696d0` | MCP Landscape, Security Threats, and Future Research (2503.23278) | arXiv | 2025 | distillation-only |
| `arxiv-mcp-sok-2512-0-457ef5c3` | SoK: MCP Security (2512.08290) | arXiv | 2025 | distillation-only |
| `arxiv-mcptox-2508-14-c5ec2b54` | MCPTox: A Benchmark for Tool Poisoning (2508.14925) | arXiv | 2025 | distillation-only |
| `arxiv-mcp-caller-ide-ceb67441` | MCP Caller Identity (2603.07473) | arXiv | 2026 | distillation-only |
| `measurement-study-mc-2c66587b` | A Measurement Study of the MCP Ecosystem | arXiv | 2025 | distillation-only |

All 25 sources are `distillation-only`: content is paraphrased and restructured, never quoted
verbatim. The quote-scan passes over the ingested markdown; the prompt-injection scan findings are
benign (security sources quoting injection strings such as “Ignore previous instructions” as
examples) and are recorded, not executed.

## Authored-layer mapping

| skill | scope | principles (head) |
|-------|-------|-------------------|
| `skills/mcp-oauth-authorization-model` | 45 principles | P001, P003, P006, P007, P013, P014, P018, P020 … |
| `skills/mcp-client-identity-and-registration` | 8 principles | P004, P054, P062, P065, P127, P191, P194, P206 |
| `skills/enterprise-mcp-identity-and-governance` | 10 principles | P011, P044, P079, P090, P107, P141, P142, P143 … |
| `skills/tool-poisoning-and-metadata-integrity` | 28 principles | P002, P005, P009, P010, P012, P037, P048, P050 … |
| `skills/indirect-prompt-injection-defense` | 26 principles | P024, P029, P033, P034, P043, P047, P057, P085 … |
| `skills/tool-boundary-and-least-privilege` | 9 principles | P025, P027, P028, P032, P111, P112, P156, P182 … |
| `skills/server-isolation-and-sandboxing` | 36 principles | P008, P017, P019, P022, P023, P026, P030, P038 … |
| `skills/supply-chain-and-server-provenance` | 11 principles | P041, P046, P055, P063, P083, P106, P120, P179 … |
| `skills/mcp-threat-modeling-and-deployment-patterns` | 23 principles | P016, P035, P049, P052, P053, P074, P092, P095 … |
| `skills/audit-logging-and-runtime-monitoring` | 15 principles | P015, P031, P039, P040, P060, P075, P081, P097 … |
| `skills/ecosystem-measurement-and-research-methodology` | 9 principles | P069, P117, P118, P119, P130, P186, P188, P189 … |
| `references/mcp-security-principles-index` | index | all 220 |
| `references/mcp-security-evidence-notes` | evidence | 106 high-confidence |

## Faithfulness

`reports/faithfulness-report.yaml` grades every load-bearing profile rule against the promoted
principles on the claim-strength scale. All findings are `WITHIN_SCOPE` (the profile narrows the
sources to defensive review; no rule is stronger than its evidence). `source_anchors` are omitted
deliberately — provenance is carried in each note via principle + claim IDs.

## Version History

- **0.1.3** (2026-07-25) — Restated the `router_description` out-of-scope clause by capability instead of naming sibling packages: generated subagents are independent of one another and the orchestrating session does the routing, so a routing string says what this agent does not cover rather than asserting which other package owns it. Also added that `router_description` in the first place (same day), for the routing-truncation reason above. Boundary content unchanged; adapter re-exported. Supersedes only same-day wording, not any principle or rule.

| version | date | change |
|---------|------|--------|
| 0.1.0 | 2026-07-05 | Initial authored layer over the map→reduce distilled spine (25 MCP-security sources, 220 principles). Fixed source metadata `source_type` (`md`→`markdown`) and one claim + one evidence `evidence_type` (`hypothetical_instance`→`case`). |
