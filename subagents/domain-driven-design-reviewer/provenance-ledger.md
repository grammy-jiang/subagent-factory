# Provenance Ledger — Domain-Driven Design Reviewer

**Subagent slug:** `domain-driven-design-reviewer`
**Profile version:** 0.1.0
**Generated:** 2026-06-09

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| domaindrivendesignqu-20260608144503 | Domain-Driven Design Quickly | Abel Avram & Floyd Marinescu | 2006 | Condensed summary of Evans 2004; supplementary authority | distillation-only | low | annual |

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `slug` | domaindrivendesignqu-20260608144503 | Q1 | kebab-case from display name; role-based |
| `display_name` | domaindrivendesignqu-20260608144503 | Q1 | Direct from q1_display_name |
| `role` | domaindrivendesignqu-20260608144503 | Q1, Q2 | Single sentence synthesised from q1_role and q2_job; paraphrased per distillation-only rights |
| `when_to_use` | domaindrivendesignqu-20260608144503 | Q3 | Five triggers drawn directly from q3_triggers; paraphrased |
| `when_not_to_use` | domaindrivendesignqu-20260608144503 | Q4 | Three exclusions from q4_exclusions; paraphrased |
| `inputs.required` | domaindrivendesignqu-20260608144503 | Q5 | Two items distilled from q5_required_input; evidence gap noted: source describes knowledge needs, not prescribed artefact formats |
| `outputs.primary_format` | domaindrivendesignqu-20260608144503 | Q6 | "structured review report" — canonical deliverable noun from q6_primary_deliverable |
| `outputs.modes` | domaindrivendesignqu-20260608144503 | Q9 | Five modes (review, advise, validate, patch-suggest, compare) all carrying source evidence from q9_modes |
| `quality_bar` | domaindrivendesignqu-20260608144503 | Q7 | Five checks rewritten as falsifiable statements from q7_quality_marks; paraphrased |
| `minimum_useful_output` | domaindrivendesignqu-20260608144503 | Q11 | Direct distillation of q11_minimum_output; paraphrased |
| `forbidden_behaviours` | domaindrivendesignqu-20260608144503 | Q10 | Four do-not rules from q10_refusals; paraphrased |
| `handoff_rules` | domaindrivendesignqu-20260608144503 | Q8 | Three rules from q8_handoff; canonical owner inferred from source emphasis on dev-plus-domain-expert collaboration (evidence gap noted in interrogation record) |
| `source_of_truth_policy.canonical_owner` | domaindrivendesignqu-20260608144503 | Q8, Q17 | Inferred from q8_handoff and q17_source_of_truth; primary authority is Evans 2004 per Q17 |
| `source_of_truth_policy.precedence` | domaindrivendesignqu-20260608144503 | Q17, Q18 | Evans 2004 as ultimate authority; platform-specific 2006 guidance marked non-normative per q18_volatile |
| `knowledge_partition.always_on` | domaindrivendesignqu-20260608144503 | Q12 | Seven items from q12_always_on; paraphrased |
| `knowledge_partition.skills` | domaindrivendesignqu-20260608144503 | Q13 | Six skill labels derived from q13_skills topics; procedure content moved to skills directory per bloat check |
| `knowledge_partition.references` | domaindrivendesignqu-20260608144503 | Q14 | Four reference labels from q14_references; static tables/checklists moved out of profile body per bloat check |
| `knowledge_partition.mcp` | domaindrivendesignqu-20260608144503 | Q15 | Empty — confirmed by interrogation; source predates MCP tooling |
| `knowledge_partition.caller_supplied` | domaindrivendesignqu-20260608144503 | Q16 | Four per-engagement runtime items from q16_caller_supplied; not placed in inputs.required because presence and form vary by engagement (per Q16 decision note) |

---

## Evidence Gaps Recorded

| Gap | Source QID | Resolution |
|-----|-----------|-----------|
| Q5: source describes knowledge needs, not prescribed artefact formats | Q5 | Inputs inferred from modeling process descriptions; flagged in interrogation evidence_gaps |
| Q8: source does not explicitly name a canonical owner role | Q8 | Inferred from repeated emphasis on developer-plus-domain-expert collaboration; flagged in interrogation evidence_gaps |
| Q15: source predates MCP tooling | Q15 | Filed as empty with confidence per interrogation record |

---

## Generated Artifacts

| Artifact | Type | Path | Notes |
|----------|------|------|-------|
| profile.yaml | canonical profile | `subagents/domain-driven-design-reviewer/profile.yaml` | |
| ubiquitous-language-session | skill | `subagents/domain-driven-design-reviewer/skills/ubiquitous-language-session/SKILL.md` | stub — content from Q13 |
| refactoring-toward-deeper-insight | skill | `subagents/domain-driven-design-reviewer/skills/refactoring-toward-deeper-insight/SKILL.md` | stub — content from Q13 |
| aggregate-design | skill | `subagents/domain-driven-design-reviewer/skills/aggregate-design/SKILL.md` | stub — content from Q13 |
| repository-and-factory-design | skill | `subagents/domain-driven-design-reviewer/skills/repository-and-factory-design/SKILL.md` | stub — content from Q13 |
| anticorruption-layer-design | skill | `subagents/domain-driven-design-reviewer/skills/anticorruption-layer-design/SKILL.md` | stub — content from Q13 |
| domain-distillation | skill | `subagents/domain-driven-design-reviewer/skills/domain-distillation/SKILL.md` | stub — content from Q13 |
| building-block-pattern-summaries | reference | `subagents/domain-driven-design-reviewer/references/building-block-pattern-summaries.md` | stub — content from Q14 |
| context-map-pattern-catalogue | reference | `subagents/domain-driven-design-reviewer/references/context-map-pattern-catalogue.md` | stub — content from Q14 |
| layered-architecture-layer-responsibilities | reference | `subagents/domain-driven-design-reviewer/references/layered-architecture-layer-responsibilities.md` | stub — content from Q14 |
| refactoring-checklist | reference | `subagents/domain-driven-design-reviewer/references/refactoring-checklist.md` | stub — content from Q14 |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-09 | Initial generation | domaindrivendesignqu-20260608144503 |
| 0.2.0 | 2026-06-11 | Skill and reference body authoring; status promoted to ready | domaindrivendesignqu-20260608144503 |
| 0.3.0 | 2026-06-13 | Full re-grounding supersession — Docling PDF re-conversion (see below) | domaindrivendesignqu-20260612231910 |
| 0.4.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Version 0.3.0 Supersession Record — 2026-06-13

### Trigger

The source PDF was re-converted using Docling, recovering 70 real section-heading anchors
(`#`-prefixed). The prior MarkItDown conversion produced 0 headings and an empty anchor
index, meaning every evidence record in the 0.1.0 / 0.2.0 packages grounded to nothing.
All evidence artifacts (evidence-records.yaml, analysis/claims.jsonl, principles/principles.yaml)
were rebuilt on the new Docling heading anchors under source ID
`domaindrivendesignqu-20260612231910`.

### What changed in this supersession

| Field | Change |
|-------|--------|
| `agent_version` | 0.2.0 → 0.3.0 |
| `source_id` | domaindrivendesignqu-20260608144503 → domaindrivendesignqu-20260612231910 |
| `tier` | (absent) → 1 |
| `quality_bar` | Re-grounded to P001–P013; principle IDs cited inline |
| `forbidden_behaviours` | Re-grounded to P002, P007, P011; Q10 / Q4 cited |
| `always_on` | All 7 items now carry principle ID references (P001–P013) |
| `when_to_use` | All 6 triggers carry principle IDs grounded in principles.yaml |
| `modes` | Replaced patch-suggest + compare with extract (justified by Q9); 4 modes total |
| `handoff_rules` | P001 citation added to language-change rule |
| `minimum_useful_output` | Added explicit requirement to cite principle references per finding |

### What was preserved

- Slug, display name, role, expert topic (no rename).
- All six skill names and four reference names in `knowledge_partition` (unchanged —
  principles.yaml operational_mapping references these exact names).
- Golden test IDs GT-001, GT-002, GT-003, NR-001, NR-002, MC-001 (unchanged —
  principles.yaml test_cases arrays reference these IDs).

### Multi-source conflict log

No conflicts: single source; 0.2.0 mode set (patch-suggest, compare) replaced because
interrogation Q9 (freshly written on Docling anchors) lists exactly four modes and
does not evidence compare or patch-suggest separately. The extract mode now replaces
both removed modes.

---

## Version 0.3.0 Distillation Log (delta only — full base in Version 0.1.0 log above)

| Field | Source IDs | QIDs / Principle IDs | Notes |
|-------|-----------|----------------------|-------|
| `tier` | domaindrivendesignqu-20260612231910 | principles-v1 present | Set to 1; principles.yaml with 13 principles present |
| `quality_bar` (revised) | domaindrivendesignqu-20260612231910 | Q7, P001–P006 | Added Service three-criteria test item (P006); principle IDs appended to all items |
| `forbidden_behaviours` (revised) | domaindrivendesignqu-20260612231910 | Q10, P002, P007, P011 | Added domain-knowledge invention and Aggregate root violation rules |
| `always_on` (revised) | domaindrivendesignqu-20260612231910 | Q12, P001–P013 | All 7 items carry P-IDs; wording paraphrased per distillation-only rights |
| `modes.extract` (new) | domaindrivendesignqu-20260612231910 | Q9, P010 | Replaces patch-suggest + compare; Q9 evidences implicit concept extraction |
| `when_to_use` (item 6, new) | domaindrivendesignqu-20260612231910 | Q3, P010, P013 | Refactoring-toward-deeper-insight trigger added |
| `source_id` (updated) | domaindrivendesignqu-20260612231910 | — | New Docling-derived source with 70 heading anchors |

---

## Open Questions

- Skills and references listed in knowledge_partition are stubs; procedure content from Q13/Q14 should be expanded into those files in the next authoring cycle.
- sha256 for source file is not yet recorded in the source registry — populate from source-pack manifest when available.
- Future review may benefit from cross-referencing Team Topologies and DDD Europe community output for context map and team-topology guidance (per Q18).

---

## Conflict Log

_No conflicts recorded at time of generation._
