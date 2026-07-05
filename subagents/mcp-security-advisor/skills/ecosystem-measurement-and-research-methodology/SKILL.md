---
name: ecosystem-measurement-and-research-methodology
kind: skill
status: ready
provenance:
  principles:
  - P069
  - P117
  - P118
  - P119
  - P130
  - P186
  - P188
  - P189
  - P218
  claims:
  - C00524
  - C00525
  - C01151
  - C01155
  - C01156
  - C01166
  - C01193
  - C01242
  - C01250
  - C01253
  - C01280
  - C01299
  - C01300
  - C01301
  - C01302
  - C01318
  evidence:
  - E00418
  - E00419
  - E00848
  - E00850
  - E00851
  - E00858
  - E00878
  - E00914
  - E00916
  - E00919
  - E00934
  - E00943
  - E00944
  - E00945
  - E00946
  - E00952
  source_anchors:
  - 2c66587b05e5-c0000
  - 2c66587b05e5-c0001
  - c5ec2b54074b-c0000
  - c5ec2b54074b-c0001
  - c8cf335ba0d6-c0000
  - ceb67441a627-c0000
  - ceb67441a627-c0001
  - ceb67441a627-c0002
  authored_from_digest: d03d412fbb8c0fcc38a38db33d57fe2b5a59e1b21df19fdade5356d62d47ee2e
---

# Ecosystem Measurement and Research Methodology

Read the MCP ecosystem critically — measured scale, maturity, entity resolution, benchmarking of defences, and attack-success metrics from empirical MCP security research.

This skill packages 9 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- judging ecosystem momentum or adoption trend.
- deduplicating or linking MCP projects across markets.
- designing a large-scale market crawl.
- building or auditing a crawler or dataset across multiple MCP markets.
- allocating limited detection effort or designing tool-call guards.
- defining metrics for a Tool-Poisoning evaluation.
- The MCP ecosystem has many independently operated clients and servers.
- The design target includes open ecosystem or enterprise-scale adoption.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P069 (high confidence).** Prioritize review of developer-facing MCP servers: they dominate the ecosystem, expose dense execution interfaces (over 50% insecure), and often aggregate multiple powerful capabilities, so a single authorization failure can escalate…
2. **P117 (high confidence).** Interpret MCP ecosystem growth cautiously: measured scale is smaller than raw counts suggest, MCP.so has plateaued, and new growth is driven largely by duplication (via MCP Market) rather than novel projects.
3. **P118 (high confidence).** Resolve cross-market MCP entities with multi-feature matching (GitHub URL as strong id, TF-IDF cosine text similarity, author and license, temporal activity) plus content hashing; auto-merge above a threshold and escalate borderline c…
4. **P119 (high confidence).** Crawl reproducibly and resiliently: rate-limited, robots-aware requests, time-versioned snapshots, rotating IPs, keyword variants, and semi-automated CAPTCHA handling with cookie or session reuse - these lifted coverage about 18% and…
5. **P130 (medium confidence).** Treat MCP authorization weakness as systemic — spanning functional categories, star ranges, and maturity, and stemming from flawed assumptions about execution context and caller identity rather than absent checks — and do not assess e…
6. **P186 (high confidence).** Measure a decentralized MCP ecosystem with per-registry adapters plus schema inference and canonicalization into a unified schema, because registries differ in data model and access method (HTML pages, JSON APIs, static catalogs).
7. **P188 (high confidence).** Prioritize defenses against parameter tampering: it is empirically the most effective paradigm (average ASR 46.7% vs 36.7% explicit and 26.7% implicit function hijacking), likely because the primary call still matches user intent and…
8. **P189 (high confidence).** When measuring TPA, define Attack Success narrowly — the agent calls a separate legitimate tool to complete the malicious action — compute ASR over valid outputs only, and record the four-way outcome taxonomy (Success / Ignored / Dire…
9. **P218 (medium confidence).** Do not design open MCP client identity around manual per-server OAuth registration; use an identity mechanism that can scale across independently operated clients and servers.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P069, P117, P118, P119, P130, P186, P188, P189, P218. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
