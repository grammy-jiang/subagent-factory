# Provenance Ledger — Python Testing Advisor

**Subagent slug:** `python-testing-advisor`
**Profile version:** 0.3.0
**Generated:** 2026-07-03

This package distills three secondary sources into an evidence-backed testing
advisor. The distilled spine (claims, evidence records, principles, anchors) was
assembled by the map→reduce build; this ledger records how the LLM-authored layer
(profile, skills, references, tests, faithfulness report) was derived from it.

---

## Source Registry

| ID | Title | Authority | Rights | Volatility | Review cadence |
|----|-------|-----------|--------|------------|----------------|
| python-testing-with-44deffe9 | Python Testing with pytest (Okken) | secondary | distillation-only | low | annual |
| tdd-with-python-perc-e5bd744b | Test-Driven Development with Python (Percival) | secondary | distillation-only | low | annual |

---

## Distillation Log

Every profile field is grounded in the package's promoted principles
(`principles/principles.yaml`), which trace to `analysis/claims.jsonl` →
`evidence/evidence-records.yaml` → `sources/anchors/*.anchors.jsonl`.

| Field | Source IDs | Grounding principles | Notes |
|-------|-----------|----------------------|-------|
| `role` | both | P001, P056 | pytest usage + test-first workflow. |
| `when_to_use` | both | P011, P017, P018, P020, P039, P040, P041, P056, P059; P001, P014, P015; P012, P024, P032, P057, P060, P061; P038, P042, P043, P063 | Caller-observable triggers from principle `applies_when`. |
| `when_not_to_use` | both | scope boundary vs P003, P008, P027, P054 (deployment/infra) | Role-scoping decision: verify-with-tests, not build-infra. |
| `inputs.required` | both | P028, P058 | Code + pytest context (version, suite, conftest/ini). |
| `outputs.modes` | both | advise: P056; review: P025, P065; tdd-guide: P001, P015 | Three read-only advisory modes. |
| `quality_bar` | both | P001, P014, P032, P035, P036, P039, P041, P057, P061, P065 | Falsifiable checks citing principle ids. |
| `minimum_useful_output` | both | P056 | One actionable, cited recommendation or a missing-context statement. |
| `forbidden_behaviours` | both | P001, P017, P032, P036, P067 | Traceable do-not rules. |
| `handoff_rules` | both | P003, P008 | Defer infra/secrets to ops; feature design to caller. |
| `source_of_truth_policy` | both | — | Books govern; official docs supersede for versioned APIs. |
| `knowledge_partition.always_on` | both | P001, P017, P035, P036 | Small, stable, high-reuse rules kept in-prompt. |
| `knowledge_partition.skills` | both | pytest-test-authoring, tdd-workflow | Repeatable/branching procedures extracted to skills. |
| `knowledge_partition.references` | python-testing-with-44deffe9 | pytest-cli-and-config, pytest-plugin-catalog | Citation-bearing catalogs extracted to references. |

---

## Generated Artifacts

| Artifact | Type | Path |
|----------|------|------|
| profile.yaml | canonical profile | `subagents/python-testing-advisor/profile.yaml` |
| pytest-test-authoring | skill | `subagents/python-testing-advisor/skills/pytest-test-authoring/SKILL.md` |
| tdd-workflow | skill | `subagents/python-testing-advisor/skills/tdd-workflow/SKILL.md` |
| pytest-cli-and-config | reference | `subagents/python-testing-advisor/references/pytest-cli-and-config.md` |
| pytest-plugin-catalog | reference | `subagents/python-testing-advisor/references/pytest-plugin-catalog.md` |
| faithfulness-report.yaml | report | `subagents/python-testing-advisor/reports/faithfulness-report.yaml` |
| golden-tests.yaml | tests | `subagents/python-testing-advisor/tests/golden-tests.yaml` |
| principle-behaviour-tests.yaml | tests | `subagents/python-testing-advisor/tests/principle-behaviour-tests.yaml` |

---

## Version History

- **0.3.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

| Version | Date | Changes | Sources involved |
|---------|------|---------|------------------|
| 0.2.0 | 2026-07-03 | Regenerated the LLM-authored layer (profile, skills, references, tests, faithfulness) to match the merged principles from the map→reduce build. | python-testing-with-44deffe9, tdd-with-python-perc-e5bd744b |
| 0.3.0 | 2026-07-04 | Re-synced the LLM-authored layer to the rebuilt spine: fixed source metadata `source_type` to `markdown`, added the third governing source to the profile, extended `principle-behaviour-tests.yaml` to cover all 35 high-confidence principles, re-authored the stale skills/references, and re-exported the adapter invariant layer. | python-testing-with-44deffe9, tdd-with-python-perc-e5bd744b, testing-in-python-ro-8cdadfe3 |

---

## Open Questions

- The sources cover deployment and infrastructure (TDD book part 3); the advisor
  deliberately scopes those out via `when_not_to_use`/`handoff_rules`, advising only
  how to verify them with tests.

---

## Conflict Log

_No unresolved cross-source conflicts recorded. Where the two books overlap
(e.g. fixtures vs xUnit setup), the pytest book governs pytest mechanics and the
TDD book governs the red/green/refactor workflow, per `source_of_truth_policy`._
