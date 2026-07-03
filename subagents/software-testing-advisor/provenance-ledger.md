# Provenance Ledger — Software Testing Advisor

**Subagent slug:** `software-testing-advisor`
**Profile version:** 0.1.0
**Generated:** 2026-07-03

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility |
|----|-------|--------|------|-----------|--------|------------|
| intro-to-software-te-140e0638 | Introduction to Software Testing | Paul Ammann and Jeff Offutt | 2017 | secondary | distillation-only | low |
| xunit-test-patterns-11f28a21 | xUnit Test Patterns | Gerard Meszaros | 2007 | secondary | distillation-only | low |
| effective-software-t-a8da44b1 | Effective Software Testing | Mauricio Aniche | 2022 | secondary | distillation-only | low |
| growing-oo-software-ed2ddca7 | Growing Object-Oriented Software, Guided by Tests | Steve Freeman and Nat Pryce | 2009 | secondary | distillation-only | low |

---

## Distillation Log

The profile is derived from the package's distilled spine (`principles/principles.yaml`, 100
principles / 79 high-confidence, over `analysis/claims.jsonl` and `evidence/evidence-records.yaml`).
The spine was assembled deterministically by the map→reduce build and is **not** edited here; the
rows below record which principle clusters each profile field distills.

| Field | Source IDs | Principle IDs | Notes |
|-------|-----------|---------------|-------|
| `role` | all four | P001, P058, P066, P089, P022 | Advisor scope synthesized across the four works: doubles, coverage theory, systematic derivation, and smell repair. |
| `when_to_use` | all four | P001, P058, P066, P089, P022 | Caller-observable situations for test design and review. |
| `when_not_to_use` | — | — | Scope boundary: no code authoring, no framework config, defer TDD-cycle coaching. |
| `outputs.modes[advise]` | all four | P066, P089, P001 | Test-design recommendation from artifact model + criterion + doubles. |
| `outputs.modes[review]` | xunit-test-patterns-11f28a21, effective-software-t-a8da44b1 | P022, P026, P028 | Suite critique: smells, verification style, coverage gaps. |
| `outputs.modes[compare]` | intro-to-software-te-140e0638, xunit-test-patterns-11f28a21 | P083, P081, P039 | Contrast criteria / doubles / combination strategies by cost and strength. |
| `quality_bar[0]` | intro-to-software-te-140e0638, effective-software-t-a8da44b1 | P066, P089, P058 | Artifact modelling + named criterion. |
| `quality_bar[1]` | xunit-test-patterns-11f28a21, intro-to-software-te-140e0638 | P001, P007, P024 | Right double, substitutable dependency. |
| `quality_bar[2]` | intro-to-software-te-140e0638, effective-software-t-a8da44b1 | P083, P058, P060 | Subsumption + RIPR + contextual rigor. |
| `quality_bar[3]` | xunit-test-patterns-11f28a21 | P022, P028, P036 | Smell classification + targeted repair. |
| `quality_bar[4]` | effective-software-t-a8da44b1, intro-to-software-te-140e0638 | P063, P096 | No proof-of-absence-of-bugs over-claim. |
| `forbidden_behaviours` | all four | P063, P026, P075, P014, P050, P049, P021 | Scope + faithfulness guards. |
| `source_of_truth_policy` | all four | — | Developer owns the suite; each work is authority for its domain (precedence). |
| `knowledge_partition.always_on` | all four | P066, P058, P001, P007, P089, P022 | Rules the advisor always applies. |
| `knowledge_partition.skills` | see skill docs | — | selecting-test-doubles, designing-coverage-criteria, deriving-test-cases-systematically, refactoring-test-smells. |
| `knowledge_partition.references` | see reference docs | — | test-double-taxonomy, coverage-criteria-subsumption. |

---

## Generated Artifacts

| Artifact | Type | Path |
|----------|------|------|
| profile.yaml | canonical profile | `subagents/software-testing-advisor/profile.yaml` |
| selecting-test-doubles | skill | `subagents/software-testing-advisor/skills/selecting-test-doubles/SKILL.md` |
| designing-coverage-criteria | skill | `subagents/software-testing-advisor/skills/designing-coverage-criteria/SKILL.md` |
| deriving-test-cases-systematically | skill | `subagents/software-testing-advisor/skills/deriving-test-cases-systematically/SKILL.md` |
| refactoring-test-smells | skill | `subagents/software-testing-advisor/skills/refactoring-test-smells/SKILL.md` |
| test-double-taxonomy | reference | `subagents/software-testing-advisor/references/test-double-taxonomy.md` |
| coverage-criteria-subsumption | reference | `subagents/software-testing-advisor/references/coverage-criteria-subsumption.md` |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-07-03 | Initial LLM-authored layer over the map→reduce distilled spine | intro-to-software-te-140e0638, xunit-test-patterns-11f28a21, effective-software-t-a8da44b1, growing-oo-software-ed2ddca7 |

---

## Open Questions

_None at time of generation._

---

## Conflict Log

_No unresolved cross-source conflicts recorded. Overlapping guidance (e.g. state-vs-interaction
verification appears in both Meszaros and Aniche) is de-duplicated in the distilled spine; the
`precedence` policy assigns domain authority per source._
