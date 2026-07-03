---
name: dependency-and-supply-chain-security
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P008
  - P024
  - P038
  claims:
  - C00391
  - C00392
  - C00488
  - C00489
  - C00317
  - C00318
  - C00179
  - C00180
  evidence:
  - E00232
  - E00233
  - E00316
  - E00317
  - E00179
  - E00180
  - E00120
  - E00121
  source_anchors:
  - 3d98983ce864-c0011
  - 3d98983ce864-c0017
  - 3d98983ce864-c0007
  - 1a5b18f0f07e-c0004
  - 1a5b18f0f07e-c0005
  authored_from_digest: eb4bff3769789fd5895f1844b1454ba443dfa9cfbab96e92120366598e37cfcb
---

# Dependency And Supply Chain Security

Treat the whole transitive dependency tree as untrusted, and scan and pin it. This skill packages 4
grounded principles the application-security-reviewer applies when this surface is in scope. Each
finding names the weakness, the attack it enables, the countermeasure, and the trade-off or residual
risk.

## When this applies

- Selecting and wiring a third-party or open source dependency into an application.
- Evaluating and pinning an application's third-party dependency tree.
- Reviewing server, framework, and dependency configuration for information disclosure.
- Applying patches or new versions of API dependencies.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope:
identify where untrusted data or an access decision enters, name the attack it enables, apply the
countermeasure, and state the trade-off or residual risk. Never weaken a defence below what the
source supports, and never present a single control as complete security.

1. **P007 (high confidence).** Integrate open source dependencies securely by isolating risky code (a decentralized server or constrained environment over embedding it in core code), choosing the integration method by size, dependency chain, and upstream activity, avoiding one-click installers that run setup scripts as admin, and scanning the full…
2. **P008 (high confidence).** Secure the whole dependency tree through automation and pinning, because third-, fourth-, and deeper-party dependencies cannot be manually reviewed and each unique dependency and version must be checked: model the tree and scan it automatically against a long-lived CVE database such as NIST NVD, isolate risky…
3. **P024 (high confidence).** Reduce version fingerprinting and keep dependencies patched, because insecurely configured default headers (X-Powered-By, Server, X-AspNet-Version) and default error or 404 pages reveal the software and version, letting an attacker cross-reference a known CVE; disable and remove identifying headers, replace default…
4. **P038 (medium confidence).** Review dependency updates before installation, compare them to known prior code, and reject update-then-review habits that transfer security responsibility to dependency maintainers.

## Anti-patterns to flag

- Trusting client-supplied data, or relying on a blacklist where a whitelist is possible.
- Leaving untrusted input un-parameterized, un-encoded, or rendered into a script/DOM sink.
- Presenting one control (a key, one flow, one header check) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P007, P008, P024, P038. Every cited claim, evidence record, and source anchor resolves
in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`,
`sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.

