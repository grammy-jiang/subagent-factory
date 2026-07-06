---
name: harness-engineering-principles-index
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
  claims: []
  evidence: []
  source_anchors: []
---

# Harness Engineering — Principles Index

The operational principles the advisor applies, distilled from the harness-engineering literature synthesis and the local-coding-agent engineering guide. Each maps to one of the nine harness skills. No rule is stronger than its source evidence; open problems are preserved as open.

| ID | Confidence | Skill | Principle |
|----|----|----|----|
| P001 | high | Context and Memory Engineering | For agentic project memory, store facts as schema-grounded, tool-retrievable records (causal or bi-temporal where applicable) instead of unverified natural-language / authoritative prose summaries. |
| P002 | high | Evaluation and Benchmark Integrity | Audit harness benchmarks for reward hacking and report fixed-model metadata, ablations, reliability, robustness, determinism, security, cost, rubric quality, chaos cases, and checkpoint scores. |
| P003 | high | Tool Access and Supply-Chain Security | Secure skills and tools with pre-deployment analysis, runtime monitoring, and per-call checks for identity, semantic binding, permission scope, and implementation integrity. |
| P004 | high | Tool Access and Supply-Chain Security | Authenticate and integrity-check model responses, routers, tool binaries, skills, prompt chains, dependencies, and documentation before downstream execution trusts them. |
| P005 | high | Harness Architecture and Scope | Design and evaluate AI agents as governed runtime harnesses, not as prompts or model weights in isolation. |
| P006 | high | Context and Memory Engineering | Treat persistent memory as governed state: separate mutable records from immutable history, gate writes, scope reads, monitor drift, and preserve provenance. |
| P007 | high | Context and Memory Engineering | Engineer context as a runtime resource with real-time budgets, staged compaction, selective routing, and structure-preserving document formats. |
| P008 | high | Verify-Before-Commit Gates | Gate state-changing actions with external, programmatic, formal, or executable verification before committing them. |
| P009 | high | Observability and Telemetry | Use cumulative session audits, multi-trace analysis, and trace-tree localization when harm or noncompliance can aggregate across turns or traces. |
| P010 | high | Runtime Governance and Policy Layers | Compose permissions and policies with deny-first precedence and monotonic narrowing so delegation never expands authority. |
| P011 | medium | Evaluation and Benchmark Integrity | Maintain local evaluations from realistic work: include hidden edge checks, fail-to-pass and pass-to-pass tests, manifest regressions, ambiguity cases, original prompts when privacy allows, hidden solutions, relevance checks, flaky-test exclusion, harness condition records, and rolling refresh. |
| P012 | high | Tool Access and Supply-Chain Security | Budget continuous red-teaming and payload-preserving adaptive attacks before claiming detector or prompt-injection robustness. |
| P013 | high | Observability and Telemetry | Capture cognitive, operational, and contextual telemetry at runtime, and design privacy controls when rich traces may expose sensitive data. |
| P014 | high | Verify-Before-Commit Gates | Harden learned or agentic verifiers with process monitors, maker-checker separation, explicit terminal states, real-execution benchmarks, and iterative verifier updates. |
| P015 | high | Tool Access and Supply-Chain Security | Provision tools structurally with typed DAGs, signed manifests, minimal tool sets, and pattern-level removal of unneeded tools. |
| P016 | high | Tool Access and Supply-Chain Security | Model adaptive prompt-injection and control defense as repeated games before claiming equilibrium or solved adversarial-control guarantees. |
| P017 | high | Tool Access and Supply-Chain Security | Target automated policy synthesis at typed monotone policy languages, and do not treat predicate, causal-rule, or program-spec synthesis as proof that policy-algebra synthesis is solved. |
| P018 | medium | Tool Access and Supply-Chain Security | Evaluate confidential inference with real accelerator measurements, attestation-loop latency, extraction resistance, and a separate prompt-injection threat model. |
| P019 | medium | Context and Memory Engineering | Promote lessons into durable memory only when they are structured, causal, tool-retrievable, triggered by concrete conditions, testable, rollbackable, owned, and durable across tasks. |
| P020 | medium | Repository Readiness and Agent Workflows | Define operating budgets and incident paths before agent work begins, including limits for turns, tokens, tools, time, network, commands, human escalation, compaction triggers, quarantine, revert, secret rotation, trace replay, and labels for local-policy thresholds. |
| P021 | high | Runtime Governance and Policy Layers | Keep authentication, authorization, audit, cryptography, and final security decisions in deterministic wrapper code rather than model reasoning. |
| P022 | high | Runtime Governance and Policy Layers | Implement runtime governance as a non-decomposable stack with policy evaluation, action interception, state tracking, audit logs, rollback, recovery, and staged capability rollout. |
| P023 | high | Multi-Agent Coordination and Governed Self-Evolution | Coordinate multi-agent systems with explicit routing, artifact coherence, controlled delegation, shared-state consistency, and compatibility checks. |
| P024 | high | Multi-Agent Coordination and Governed Self-Evolution | Constrain self-evolution and meta-harness search with formal guardrails, verified fallbacks, local contracts, compatibility checks, staged rollout, rollback, and attention to diminishing returns. |
| P025 | high | Evaluation and Benchmark Integrity | Search emerging research areas with expanded term atlases, direct identifier ingestion, coverage audits, and promotion of relevant exploratory shortlists. |
| P026 | medium | Runtime Governance and Policy Layers | Enforce structural least privilege through the tool graph: expose only needed capabilities, keep planning non-executing, scope adapters, and withhold commit authority until gates pass. |
| P027 | medium | Runtime Governance and Policy Layers | Encode agent policy in deterministic, versioned, verifiable layers instead of relying on the model to remember behavioral rules. |
| P028 | medium | Evaluation and Benchmark Integrity | Use multiple evaluation signals; do not rely solely on pass-at-one, public tests, model leaderboard rank, or agent self-rating. |
| P029 | high | Harness Architecture and Scope | Stage harness implementation with observability, supply-chain security, context, storage, governance, verification, and monitoring before advanced self-evolution. |
| P030 | high | Observability and Telemetry | Inspect execution behavior, not only final outputs, because successful-looking results can hide noncompliant trajectories. |
| P031 | high | Context and Memory Engineering | Do not claim dynamic memory selection is solved unless a meta-router actually routes among memory substrates by task capability. |
| P032 | high | Runtime Governance and Policy Layers | Evaluate permission systems on unauthorized-operation rate, scope-overstep rate, ask-user cost, usability, and adaptive escape rate. |
| P033 | high | Verify-Before-Commit Gates | Convert formal lifecycle, state, task, and component invariants into automated harness gates where those properties are expressible. |
| P034 | medium | Observability and Telemetry | Capture live telemetry sufficient for replay, including runtime metadata, plans, tool calls, tool results, verification events, context decisions, environment state, human decisions, and append-only session logs. |
| P035 | medium | Verify-Before-Commit Gates | Evolve harness behavior only as a measured experiment: vary one harness variable with the model fixed, use held-out tasks and regression checks, keep only improvements without new regressions, and preserve rollback. |
| P036 | medium | Harness Architecture and Scope | Weight rule confidence by domain evidence strength, and preserve partial/open gap status rather than overstating the synthesis. |
| P037 | medium | Harness Architecture and Scope | Treat the local coding-agent harness as part of the product: it must control visibility, tool authority, write scope, failure detection, memory, cost, auditability, and final acceptance. |
| P038 | medium | Repository Readiness and Agent Workflows | Bootstrap each repository with explicit runtime metadata and core manifests that define constraints, conventions, data classes, enforcement hooks, success criteria, scope, quality gates, and cost policy. |
| P039 | medium | Repository Readiness and Agent Workflows | Treat a repository as ready for local-agent editing only after sandboxing, inspectable policy, scoped writes, verification, audit trails, manifest review, AI-readiness scoring, and any needed readiness PR are complete. |
| P040 | medium | Evaluation and Benchmark Integrity | Test prompt-like artifacts as behavior specifications: state required and forbidden behavior with examples, add visible and hidden tests, semantic mutations, trace assertions, generated-file checks, refusal or clarification checks, regression runs, evidence, and rollback notes. |
| P041 | medium | Verify-Before-Commit Gates | When verification, budget, or supply-chain gates fail, treat the gate as authoritative: stop or block merge, compare evidence, fix faulty verifiers separately, checkpoint or split over-budget work, and require provenance-backed clean rebuilds for supply-chain alerts. |
| P042 | high | Observability and Telemetry | Track drift, parsing failures, repeated-output loops, safety conditions, trace differences, and replay evidence as distinct operational signals. |
| P043 | medium | Context and Memory Engineering | Preserve superseded memory records with provenance rather than deleting them when memory must handle temporal conflict. |
| P044 | medium | Verify-Before-Commit Gates | Use deterministic verification as the acceptance authority, with a minimum gate covering formatting or linting, tests, secret scanning, SAST, dependency scanning, and domain invariants. |
| P045 | medium | Verify-Before-Commit Gates | Evaluate harness changes by holding the model and runtime constant while varying manifests, tool scope, permissions, or verification gates. |
| P046 | medium | Verify-Before-Commit Gates | For high-risk changes, add domain-specific external guards such as state-machine invariants, schema compatibility checks, authorization tests, property checks, or formal safety properties. |
| P047 | medium | Harness Architecture and Scope | Use smaller control-plane models for routing, verification, monitoring, or memory routing only when the task is separable from creative reasoning and governance is preserved. |
| P048 | medium | Tool Access and Supply-Chain Security | Integrate enterprise data classifiers into agent encryption and audit decisions, and evaluate both tier-label quality and downstream leak rate. |
| P049 | medium | Tool Access and Supply-Chain Security | Keep multi-hop compound attestation across heterogeneous delegation chains marked as a residual gap unless the chain proves identity and intent transitively. |
| P050 | medium | Tool Access and Supply-Chain Security | Verify the local-agent supply chain before trusting it, including CLIs, MCP servers, dependencies, model or skill packages, and parsed external tool output. |
| P051 | medium | Context and Memory Engineering | Answer exact project-fact questions by querying validated memory records and re-promote only durable records into manifests or skills. |
| P052 | medium | Runtime Governance and Policy Layers | Require branch and review governance for agent work: agents use feature branches and agent-authored PRs require CI plus human review. |
| P053 | medium | Runtime Governance and Policy Layers | Run agents in a constrained sandbox that limits filesystem writes, network access, process resources, secret exposure, package installation, and protected branch writes. |
| P054 | medium | Runtime Governance and Policy Layers | Apply manifest precedence monotonically: durable hard constraints outrank project policy, project policy outranks runtime overlays, overlays outrank skills, and skills outrank session plans. |
| P055 | medium | Runtime Governance and Policy Layers | Keep skills and session plans operationally scoped: skills encode reusable procedures with observable outcomes, and plans record the current task contract before edits. |
| P056 | medium | Verify-Before-Commit Gates | Use DryRUN for change verification by recording intended behavior, expected files, representative cases, predicted effects, risks, and invariants before test results, then repairing or explaining mismatches before commit. |
| P057 | medium | Context and Memory Engineering | On memory writes, validate every required field, preserve source links, record unknowns and rejected options, and make the update reviewable like code. |
| P058 | medium | Context and Memory Engineering | Use cache and retrieval conservatively: cache only permitted stable material, prefer narrow symbol or file search, never cache secrets, and re-validate retrieved memory before edits. |
| P059 | medium | Repository Readiness and Agent Workflows | When an agent crosses scope or exposes sensitive data, stop and preserve evidence, revert only the offending agent changes, quarantine or rotate secrets as applicable, tighten controls, and add a regression or post-incident review. |
| P060 | high | Verify-Before-Commit Gates | Prefer external verification over unstructured self-feedback, allowing structured self-verification only when the source condition makes checking easier than generation. |
| P061 | high | Tool Access and Supply-Chain Security | Decompose AI supply-chain controls across data, training, inference, and substrate layers, with verifiability, versioning, observability, and traceability for each. |
| P062 | medium | Harness Architecture and Scope | Do not presume first-party harnesses are superior overall; compare them empirically across the relevant reliability and affordance axes. |
| P063 | medium | Multi-Agent Coordination and Governed Self-Evolution | Balance peer identity anonymization against accountability requirements in multi-agent systems. |
| P064 | medium | Observability and Telemetry | Use model-aware monitoring for heterogeneous model fleets because detectors may not generalize across model families. |
| P065 | medium | Tool Access and Supply-Chain Security | Use watermarks for provenance, not as execution-security primitives. |
| P066 | medium | Harness Architecture and Scope | Use a staged SME-developer-agent process that produces reusable requirements, grounding, tool, reasoning-policy, prompt-architecture, and evaluation artifacts for domain-specific agents. |
| P067 | medium | Verify-Before-Commit Gates | Add maintainability gates that can reject behavior-correct patches for poor locality, duplicated paths, mixed responsibilities, bad dependencies, unclear state ownership, or boundary-crossing side effects. |
| P068 | medium | Verify-Before-Commit Gates | Use the safe-refactor workflow when behavior must be preserved: characterize existing behavior, freeze interfaces, scope edit tools, run invariants and public-output checks, and reject unapproved behavior changes. |
| P069 | medium | Context and Memory Engineering | Use artifact ownership states in multi-agent workflows so agents know when they may edit, when they may only read, and when they must re-read stale state. |
| P070 | medium | Context and Memory Engineering | Compact context in stages by warning on budget pressure, retaining relevant ranges, pruning resolved dead ends, summarizing repeated traces, and checkpointing before hard-limit restarts. |
| P071 | medium | Repository Readiness and Agent Workflows | Use the spec-first workflow for high-impact production changes: check constraints, plan first, scope edits, verify, evaluate harness changes, and open a PR with trace evidence. |
| P072 | medium | Repository Readiness and Agent Workflows | Use the test-first workflow for bug fixes: reproduce the failure, constrain implementation and test edits, verify focused and neighboring tests, and promote only reviewed recurring fix patterns. |
| P073 | medium | Repository Readiness and Agent Workflows | Use the dependency-update workflow for package changes: inspect changelogs and advisories, update lockfiles in a sandbox, run tests and security/license scans, record transitive changes, and review postinstall scripts. |
| P074 | medium | Repository Readiness and Agent Workflows | Use the documentation-only workflow for docs tasks: state target files, preserve wiki-link syntax when present, avoid generated and unrelated artifacts, validate Markdown when tooling exists, and report changed documents. |
| P075 | medium | Observability and Telemetry | When an agent loops, stop immediately, preserve trace and diff, diagnose the missing tool, bad output, ambiguity, or stale context, restart from a compacted narrower context, and add a detector if recurrence shows a pattern. |

