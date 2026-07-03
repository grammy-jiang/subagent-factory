# Provenance Ledger — application-security-reviewer

Canonical source of truth: `subagents/application-security-reviewer/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` (501 claims),
`evidence/evidence-records.yaml` (323 records), `principles/principles.yaml` (50
principles, 25 high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic,
validator-checked layer. The LLM-authored layer (this profile, the faithfulness report, the seven
skills, two references, and the tests) is derived from those principles and their backing claims,
evidence, and anchors.

## Sources

| source_id | title | author | year | rights_status |
|-----------|-------|--------|------|---------------|
| `web-application-secu-3d98983c` | Web Application Security: Exploitation and Countermeasures for Modern Web Applications | Andrew Hoffman | 2020 | distillation-only |
| `securing-the-api-str-1a5b18f0` | Securing the API Stronghold: The Ultimate Guide to API Security | Nordic APIs | 2015 | distillation-only |

Both sources are `distillation-only`: content is paraphrased and restructured, never quoted
verbatim. The quote-scan passes over the ingested markdown; the prompt-injection scan findings are
benign (a `</user>` delimiter token appearing inside a security example) and recorded, not executed.

## Authored-layer mapping

| skill / reference | principles |
|-------------------|-----------|
| `skills/web-vulnerability-defense` | P001, P003, P009, P010, P013, P014, P015, P025, P030, P042, P045, P046, P047 |
| `skills/dependency-and-supply-chain-security` | P007, P008, P024, P038 |
| `skills/secure-development-lifecycle` | P016, P022, P023, P036, P048 |
| `skills/security-review-and-vulnerability-management` | P004, P031, P040, P041, P043 |
| `skills/reconnaissance-and-attack-surface-mapping` | P006, P012, P028, P039 |
| `skills/api-identity-and-access-management` | P002, P005, P011, P018, P021, P027, P029, P032, P034, P035, P044, P050 |
| `skills/api-design-and-lifecycle-governance` | P017, P019, P020, P026, P033, P037, P049 |
| `references/application-security-principles-index` | all 50 |
| `references/api-and-web-security-evidence-notes` | high-confidence principles |

## Faithfulness

`reports/faithfulness-report.yaml` grades every load-bearing profile rule against the promoted
principles on the claim-strength scale. All findings are `WITHIN_SCOPE` (the profile narrows the
sources to defensive review; no rule is stronger than its evidence). `source_anchors` are omitted
from the report deliberately — provenance is carried in each note via principle + claim IDs.

## Version History

| version | date | change |
|---------|------|--------|
| 0.1.0 | 2026-07-03 | Initial authored layer over the map→reduce distilled spine (2 sources, 50 principles). |
