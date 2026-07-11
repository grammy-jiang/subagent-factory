# Changelog — cloud-native-kubernetes-advisor

All notable changes to this subagent package are documented here.
Format follows Keep a Changelog conventions.

---

## [0.3.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.2.0 → 0.3.0.

## [0.2.0] — 2026-06-14

### Added

- Authored all 6 skill bodies and 6 reference bodies from package principles/claims/evidence
  (Step 8, author-skills). Each carries `authored-doc-v1` frontmatter with real principle/claim
  IDs and source anchors, plus a stamped `authored_from_digest` drift baseline.
- Skills: evaluating-managed-kubernetes-offerings (P001/P010), selecting-self-hosting-installers
  (P011), clusterless-and-faas-fit-analysis (P006/P007), container-image-build-practice (P004),
  deployment-strategy-selection (P009/P008), resilience-testing-guidance (P002/P003/P008/P011).
- References: managed-kubernetes-service-comparison, self-hosting-installer-comparison,
  production-readiness-checklist, kubernetes-control-plane-components,
  cloud-native-characteristics-reference, clusterless-container-services-reference.

### Changed

- Promoted package `status: draft → ready`.

### Notes

- Rights: distillation-only; quote-scan clean (no verbatim). validate_skill_authoring clean.

---

## [0.1.0] — 2026-06-14

### Added

- Initial profile derivation from interrogation records Q1–Q18.
- Source: Cloud Native DevOps with Kubernetes, 2nd Edition (cloud-native-devops-ed89eef5).
- 4 evidence-grounded modes: advise, compare, validate, produce.
- 11 principles grounded in evidence records EV001–EV020.
- 5-item quality_bar grounded in principles P001–P010.
- 5 forbidden_behaviours traceable to Q10 refusals and Q17/Q18 volatility evidence.
- 7 always_on knowledge items from Q12.
- 6 skill stubs and 6 reference stubs from Q13–Q14.
- policy/patch-policy.yaml (required for produce mode).
- tests/golden-tests.yaml with 4 tests (2 positive, 1 negative routing, 1 missing context).
- provenance-ledger.md with full distillation log.
- README.md.

### Notes

- Rights: distillation-only; no verbatim quotation.
- Managed service feature claims marked volatile; annual review cadence.
- MCP: none (no evidence of live data retrieval in source).
- Tier: 1 (principles.yaml present and grounding applied to quality_bar, forbidden_behaviours, and modes).
