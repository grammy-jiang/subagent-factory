---
name: supply-chain-and-server-provenance
kind: skill
status: ready
provenance:
  principles:
  - P041
  - P046
  - P055
  - P063
  - P083
  - P106
  - P120
  - P179
  - P190
  - P198
  - P209
  claims:
  - C00199
  - C00200
  - C00309
  - C00310
  - C00415
  - C00418
  - C00876
  - C00877
  - C00889
  - C00890
  - C00913
  - C00914
  - C00940
  - C00941
  - C00958
  - C00959
  - C00973
  - C00974
  - C01282
  - C01288
  - C01324
  - C01336
  evidence:
  - E00166
  - E00167
  - E00254
  - E00255
  - E00353
  - E00354
  - E00693
  - E00694
  - E00703
  - E00704
  - E00722
  - E00723
  - E00745
  - E00746
  - E00761
  - E00762
  - E00776
  - E00777
  - E00935
  - E00938
  - E00955
  - E00963
  source_anchors:
  - 2c66587b05e5-c0000
  - 2c66587b05e5-c0001
  - 347696d03493-c0000
  - 347696d03493-c0001
  - 347696d03493-c0002
  - 347696d03493-c0003
  - 515304c317e3-c0001
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0000
  authored_from_digest: eb75f7045e8d2f127bfc0215612f50caad0cf1505d67022368aa2f2c1afe0199
---

# Supply Chain and Server Provenance

Secure the MCP software supply chain — verify server provenance with signatures and SBOMs, treat installers as privileged components, pin versions, and counter dependency monoculture and rug pulls.

This skill packages 11 grounded principles the mcp-security-advisor applies when this surface is in scope. Each finding names the weakness, the attack it enables, the control, and the trade-off or residual risk.

## When this applies

- Selecting MCP servers from community marketplaces, directories, registries, or repositories.
- MCP systems use SDKs, connectors, protocol servers, plugins, model tooling, build pipelines, container images, or package registries.
- Developing, building, packaging, publishing, installing, or distributing MCP servers and dependencies.
- Managing MCP package versions, auto-installers, updates, or server discovery.
- Distributing, selecting, installing, or dynamically resolving MCP servers by name.
- managing MCP servers across an organization over time.
- giving strategic guidance on adopting or investing in MCP.
- Before installing, updating, or connecting a new MCP server.
- assessing supply-chain exposure of MCP servers.
- Using one-click, natural-language, or community-provided tools to install MCP servers.
- Writing MCP guidance for developers, users, registry operators, or ecosystem maintainers.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope: identify where untrusted data, a token, or an authorization decision enters, name the attack it enables, apply the control, and state the trade-off or residual risk. Never weaken a defence below what the source and the MCP specification support, and never present a single control as complete MCP security.

1. **P041 (medium confidence).** Treat public MCP ecosystem maturity as uneven and verify community servers, marketplace listings, and directories for identity, availability, maintenance, documentation, curation, validation, and signing before trusting them.
2. **P046 (high confidence).** Secure the MCP software supply chain by requiring signed provenance for components, deployment SBOM and cryptographic inventories, pinned approved sources, dependency and code scanning, and sandboxed third-party plugins with constrain…
3. **P055 (medium confidence).** Secure MCP source, dependency, build, and release pipelines with controlled environments, reproducible builds, dependency records, signatures, checksums, attestations, version pinning, and strict dependency management.
4. **P063 (medium confidence).** Counter vulnerable-version redeployment with automated vulnerability detection, version freshness checks, standardized packaging, and a trusted MCP registry.
5. **P083 (medium confidence).** Prevent server impersonation by binding MCP namespaces to verified publishers, enforcing uniqueness, surfacing provenance, preferring trusted servers, and monitoring suspicious registration or update behavior.
6. **P106 (high confidence).** Govern the full MCP server lifecycle: mandatory code-signing and binary authorization before install, private vetted repositories with software-composition analysis, allow-lists with documented reviews, SBOM tracking, hash-pinned depe…
7. **P120 (high confidence).** Treat the MCP ecosystem as transitional - widely adopted in appearance but structurally fragile (over 50% low-value, supply-chain monocultures, uneven maintenance, slow client protocol migration) - and weight advice toward sustainabil…
8. **P179 (high confidence).** Handle MCP server installation as a supply-chain control point requiring trusted sources, code and tool-definition review, package-integrity checks, dependency scanning, and package-name verification.
9. **P190 (high confidence).** Treat dependency monoculture as systemic risk: Java servers concentrate on Spring (a single flaw like SpringShell can cascade), and over 93% of servers are JavaScript or Python, so a popular npm or PyPI vulnerability can cascade widel…
10. **P198 (medium confidence).** Treat MCP auto-installers as privileged supply-chain components that must show provenance, verify trusted signatures or checksums, reject mismatches, require confirmation, and isolate setup execution.
11. **P209 (medium confidence).** Assign MCP security duties by stakeholder: developers verify provenance and sign releases, users prefer trusted and sandboxed servers, and maintainers enforce version, integrity, and configuration checks.

## Anti-patterns to flag

- Trusting server-supplied tool metadata, descriptions, schemas, or outputs as instructions.
- Accepting or forwarding a mis-audienced or client-supplied token (confused deputy / pass-through).
- Presenting one control (a single OAuth flow, one approval, protocol defaults, sandboxing alone) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P041, P046, P055, P063, P083, P106, P120, P179, P190, P198, P209. Every cited claim, evidence record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.
