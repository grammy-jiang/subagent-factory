---
name: tool-access-and-supply-chain-security
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P004
  - P015
  - P050
  - P061
  - P048
  - P012
  - P016
  - P065
  - P049
  - P018
  - P017
  claims:
  - C00023
  - C00024
  - C00049
  - C00050
  - C00055
  - C00056
  - C00113
  - C00114
  - C00145
  - C00156
  - C00157
  - C00015
  - C00027
  - C00107
  - C00108
  - C00137
  - C00141
  - C00143
  - C00154
  - C00155
  - C00038
  - C00039
  - C00098
  - C00099
  - C00100
  - C00177
  - C00210
  - C00165
  - C00074
  - C00075
  - C00071
  - C00072
  - C00073
  - C00122
  - C00139
  - C00167
  - C00065
  - C00066
  - C00067
  - C00123
  - C00169
  - C00144
  - C00088
  - C00172
  - C00028
  - C00061
  - C00062
  - C00063
  - C00064
  - C00068
  - C00069
  - C00070
  - C00166
  - C00171
  evidence: []
  source_anchors: []
---

# Tool Access and Supply-Chain Security

## Purpose

Enforce structural least privilege over tools and verify the supply chain and untrusted content before the harness trusts them.

## When this applies

- validating or executing skills, tools, MCP components, or tool-using agents.
- untrusted content enters the harness.
- requests or responses pass through third-party routers.
- auditing AI application releases.
- agents use MCP tools, servers, or skills.
- configuring, building, auditing, installing, invoking, or delegating agent tools.
- designing L0 supply-chain controls.
- deploying data-classified agent workflows.
- mapping data to confidentiality tiers.
- validating skill scanners, control monitors, injection detectors, long-context defenses, or claims of adaptive robustness.
- the threat model includes adaptive attackers.
- claiming solved adversarial-control guarantees.
- the security question requires game-theoretic guarantees.
- threats can be distributed across multiple changes or sessions.
- choosing provenance or security controls.
- agents delegate work across principals or runtimes.
- assessing confidential LLM inference, TEE inference, or model-weight protection.
- building automated policy authoring for cryptographic wrappers or join-semilattice policy systems.
- converting behavioral goals into executable controls.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Secure skills and tools with pre-deployment analysis, runtime monitoring, and per-call checks for identity, semantic binding, permission scope, and implementation integrity. (P003)
2. Authenticate and integrity-check model responses, routers, tool binaries, skills, prompt chains, dependencies, and documentation before downstream execution trusts them. (P004)
3. Provision tools structurally with typed DAGs, signed manifests, minimal tool sets, and pattern-level removal of unneeded tools. (P015)
4. Verify the local-agent supply chain before trusting it, including CLIs, MCP servers, dependencies, model or skill packages, and parsed external tool output. (P050)
5. Decompose AI supply-chain controls across data, training, inference, and substrate layers, with verifiability, versioning, observability, and traceability for each. (P061)
6. Integrate enterprise data classifiers into agent encryption and audit decisions, and evaluate both tier-label quality and downstream leak rate. (P048)
7. Budget continuous red-teaming and payload-preserving adaptive attacks before claiming detector or prompt-injection robustness. (P012)
8. Model adaptive prompt-injection and control defense as repeated games before claiming equilibrium or solved adversarial-control guarantees. (P016)
9. Use watermarks for provenance, not as execution-security primitives. (P065)
10. Keep multi-hop compound attestation across heterogeneous delegation chains marked as a residual gap unless the chain proves identity and intent transitively. (P049)
11. Evaluate confidential inference with real accelerator measurements, attestation-loop latency, extraction resistance, and a separate prompt-injection threat model. (P018)
12. Target automated policy synthesis at typed monotone policy languages, and do not treat predicate, causal-rule, or program-spec synthesis as proof that policy-algebra synthesis is solved. (P017)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P003** (high) — Secure skills and tools with pre-deployment analysis, runtime monitoring, and per-call checks for identity, semantic binding, permission scope, and implementation integrity.
- **P004** (high) — Authenticate and integrity-check model responses, routers, tool binaries, skills, prompt chains, dependencies, and documentation before downstream execution trusts them.
- **P015** (high) — Provision tools structurally with typed DAGs, signed manifests, minimal tool sets, and pattern-level removal of unneeded tools.
- **P050** (medium) — Verify the local-agent supply chain before trusting it, including CLIs, MCP servers, dependencies, model or skill packages, and parsed external tool output.
- **P061** (high) — Decompose AI supply-chain controls across data, training, inference, and substrate layers, with verifiability, versioning, observability, and traceability for each.
- **P048** (medium) — Integrate enterprise data classifiers into agent encryption and audit decisions, and evaluate both tier-label quality and downstream leak rate.
- **P012** (high) — Budget continuous red-teaming and payload-preserving adaptive attacks before claiming detector or prompt-injection robustness.
- **P016** (high) — Model adaptive prompt-injection and control defense as repeated games before claiming equilibrium or solved adversarial-control guarantees.
- **P065** (medium) — Use watermarks for provenance, not as execution-security primitives.
- **P049** (medium) — Keep multi-hop compound attestation across heterogeneous delegation chains marked as a residual gap unless the chain proves identity and intent transitively.
- **P018** (medium) — Evaluate confidential inference with real accelerator measurements, attestation-loop latency, extraction resistance, and a separate prompt-injection threat model.
- **P017** (high) — Target automated policy synthesis at typed monotone policy languages, and do not treat predicate, causal-rule, or program-spec synthesis as proof that policy-algebra synthesis is solved.

