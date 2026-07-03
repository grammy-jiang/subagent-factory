---
name: reconnaissance-and-attack-surface-mapping
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P012
  - P028
  - P039
  claims:
  - C00303
  - C00304
  - C00296
  - C00297
  - C00288
  - C00289
  - C00223
  - C00229
  evidence:
  - E00170
  - E00171
  - E00163
  - E00164
  - E00157
  - E00158
  - E00128
  - E00129
  source_anchors:
  - 3d98983ce864-c0006
  - 3d98983ce864-c0005
  - 3d98983ce864-c0001
  authored_from_digest: 4cf5244ed62ddc105da7bc3093a0f8d018c7e1d922ea324ce1e1dafff223f690
---

# Reconnaissance And Attack Surface Mapping

Map the attack surface from the attacker's perspective — only where authorised. This skill packages
4 grounded principles the application-security-reviewer applies when this surface is in scope. Each
finding names the weakness, the attack it enables, the countermeasure, and the trade-off or residual
risk.

## When this applies

- Enumerating and characterizing an application's API endpoints.
- Discovering an application's subdomains, infrastructure, and surface area.
- Searching for an application's exposed assets or assessing information leakage.
- Prioritizing which parts of an application to harden first.

## Procedure

Apply the principles below in order of the risk they carry, highest first. For each one in scope:
identify where untrusted data or an access decision enters, name the attack it enables, apply the
countermeasure, and state the trade-off or residual risk. Never weaken a defence below what the
source supports, and never present a single control as complete security.

1. **P006 (medium confidence).** Discover API endpoints and payloads methodically — probe HTTP verbs against known resources, try OPTIONS, reverse-engineer the authentication scheme and token, start from common endpoints (sign in/up, password reset), and shrink an unknown value's search space by learning its rules — but obtain explicit owner…
2. **P012 (medium confidence).** Use several reconnaissance techniques together because no single one is comprehensive, preferring cheap low-noise methods first (a zone-transfer attempt, then a dictionary of common subdomains) and treating noisy brute force as a last resort fired asynchronously, while paying special attention to less-scrutinized…
3. **P028 (medium confidence).** Assume sensitive data and infrastructure leak into public records over time — cached repositories, keys, internal URLs, PII — and proactively hunt for them using search-engine operators, web archives, social-media data APIs, and browser developer tools (including timing side-channels), both to find exposure and to…
4. **P039 (medium confidence).** Use the attacker's perspective — running the same reconnaissance against your own application — to find weak mechanisms and prioritize defenses, recognizing that routine defenses are easily bypassed and that some threats (such as malware hidden in valid software) are nearly impossible to detect after the fact.

## Anti-patterns to flag

- Trusting client-supplied data, or relying on a blacklist where a whitelist is possible.
- Leaving untrusted input un-parameterized, un-encoded, or rendered into a script/DOM sink.
- Presenting one control (a key, one flow, one header check) as complete security.
- Omitting the attack a control defends, its trade-off, or the residual risk.

## Grounding

Principles: P006, P012, P028, P039. Every cited claim, evidence record, and source anchor resolves
in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-records.yaml`,
`sources/anchors/`). Sources are distillation-only: paraphrased, never quoted.

