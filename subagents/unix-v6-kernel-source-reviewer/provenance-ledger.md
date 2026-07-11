# Provenance Ledger — UNIX V6 Kernel Source Reviewer

**Subagent slug:** `unix-v6-kernel-source-reviewer`
**Profile version:** 0.1.0
**Generated:** 2026-06-09

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| a-commentary-on-the-20260609102650 | A Commentary on the Sixth Edition UNIX Operating System | J. Lions | 1977 | secondary | proprietary/restricted | low | annual |

---

## Source-Pack Rights Notice

**Source:** a-commentary-on-the-20260609102650
**Rights status:** proprietary/restricted
**Reproduction:** PROHIBITED. No verbatim quotation of this source is permitted
in any generated artifact. All content derived from this source must be
distilled and paraphrased. Three or more consecutive source sentences must
never appear in any output. This restriction applies to profile.yaml,
provenance-ledger.md, skills, references, tests, adapter files, and any
commentary produced at runtime by the deployed subagent.
**Basis for restriction:** Western Electric / AT&T copyright on UNIX V6 source
and associated commentary material. Rights situation should be re-verified
annually as the legal landscape around historical UNIX sources continues to
evolve.

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `display_name` | a-commentary-on-the-20260609102650 | Q1 | Taken directly from q1_display_name |
| `role` | a-commentary-on-the-20260609102650 | Q1, Q2 | Synthesised from q1_role (what/to what) and q2_job (for what reason); paraphrased, not quoted |
| `when_to_use[0]` | a-commentary-on-the-20260609102650 | Q3 | Paraphrased from trigger 1: procedure explanation request |
| `when_to_use[1]` | a-commentary-on-the-20260609102650 | Q3 | Paraphrased from trigger 2: data-structure field query |
| `when_to_use[2]` | a-commentary-on-the-20260609102650 | Q3 | Paraphrased from trigger 3: subsystem walkthrough |
| `when_to_use[3]` | a-commentary-on-the-20260609102650 | Q3 | Paraphrased from trigger 4: obscure/erroneous pattern explanation |
| `when_to_use[4]` | a-commentary-on-the-20260609102650 | Q3 | Paraphrased from trigger 5: PDP-11 assembly conventions |
| `when_not_to_use[0]` | a-commentary-on-the-20260609102650 | Q4 | Paraphrased from exclusion 1: post-V6 UNIX versions |
| `when_not_to_use[1]` | a-commentary-on-the-20260609102650 | Q4 | Paraphrased from exclusion 2: user-space utilities |
| `when_not_to_use[2]` | a-commentary-on-the-20260609102650 | Q4 | Paraphrased from exclusion 3: hardware design detail |
| `inputs.required[0]` | a-commentary-on-the-20260609102650 | Q5 | Paraphrased from q5_required_input; procedure name/line range/subsystem topic |
| `outputs.primary_format` | a-commentary-on-the-20260609102650 | Q6 | Paraphrased from q6_primary_deliverable; prose commentary format |
| `modes[advise].trigger` | a-commentary-on-the-20260609102650 | Q9 | Evidence from q9_modes advise entry; paraphrased |
| `modes[advise].output` | a-commentary-on-the-20260609102650 | Q9 | Derived from q9_modes advise deliverable; paraphrased |
| `modes[review].trigger` | a-commentary-on-the-20260609102650 | Q9 | Evidence from q9_modes review entry; paraphrased |
| `modes[review].output` | a-commentary-on-the-20260609102650 | Q9 | Derived from q9_modes review deliverable; paraphrased |
| `modes[extract].trigger` | a-commentary-on-the-20260609102650 | Q9 | Evidence from q9_modes extract entry; paraphrased |
| `modes[extract].output` | a-commentary-on-the-20260609102650 | Q9 | Derived from q9_modes extract deliverable; paraphrased |
| `quality_bar[0]` | a-commentary-on-the-20260609102650 | Q7 | Paraphrased from q7_quality_marks[0]: traceability to procedure/line |
| `quality_bar[1]` | a-commentary-on-the-20260609102650 | Q7 | Paraphrased from q7_quality_marks[1]: explicit cross-references |
| `quality_bar[2]` | a-commentary-on-the-20260609102650 | Q7 | Paraphrased from q7_quality_marks[2] and [5]: anomalies acknowledged, speculation labelled |
| `quality_bar[3]` | a-commentary-on-the-20260609102650 | Q7 | Paraphrased from q7_quality_marks[3]: PDP-11 assembly correctness |
| `quality_bar[4]` | a-commentary-on-the-20260609102650 | Q7 | Paraphrased from q7_quality_marks[4]: kernel/user mode distinction |
| `minimum_useful_output` | a-commentary-on-the-20260609102650 | Q11 | Paraphrased from q11_minimum_output |
| `forbidden_behaviours[0]` | a-commentary-on-the-20260609102650 | Q10 | Paraphrased from q10_refusals[0]; rights constraint enforced |
| `forbidden_behaviours[1]` | a-commentary-on-the-20260609102650 | Q10 | Paraphrased from q10_refusals[1]: speculation must be flagged |
| `forbidden_behaviours[2]` | a-commentary-on-the-20260609102650 | Q10 | Paraphrased from q10_refusals[2]: no post-V6 scope |
| `forbidden_behaviours[3]` | a-commentary-on-the-20260609102650 | Q10 | Paraphrased from q10_refusals[3]: no user-space utilities |
| `handoff_rules[0]` | a-commentary-on-the-20260609102650 | Q8 | Paraphrased from q8_handoff (inferred from educational context per evidence_gaps note) |
| `handoff_rules[1]` | a-commentary-on-the-20260609102650 | Q8 | Paraphrased from q8_handoff: external reference directions |
| `source_of_truth_policy.canonical_owner` | a-commentary-on-the-20260609102650 | Q8, Q17 | Paraphrased from q17_source_of_truth |
| `source_of_truth_policy.precedence` | a-commentary-on-the-20260609102650 | Q17 | Paraphrased from q17_source_of_truth secondary source note |
| `knowledge_partition.always_on[0]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[0]: PDP-11/40 architecture |
| `knowledge_partition.always_on[1]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[1]: PDP-11 addressing modes |
| `knowledge_partition.always_on[2]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[2]: V6 major data structures |
| `knowledge_partition.always_on[3]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[3]: V6 process lifecycle |
| `knowledge_partition.always_on[4]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[4]: V6 memory segmentation |
| `knowledge_partition.always_on[5]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[5]: V6 trap and interrupt dispatch |
| `knowledge_partition.always_on[6]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[6]: V6 file system |
| `knowledge_partition.always_on[7]` | a-commentary-on-the-20260609102650 | Q12 | Paraphrased from q12_always_on[7]: UNIX C and assembler conventions |
| `knowledge_partition.skills` | a-commentary-on-the-20260609102650 | Q13 | Skill names derived from q13_skills actionable procedures; kebab-case slugs |
| `knowledge_partition.references` | a-commentary-on-the-20260609102650 | Q14 | Reference names derived from q14_references items; kebab-case slugs |
| `sources[0].title` | a-commentary-on-the-20260609102650 | metadata | From source metadata JSON field "title" |
| `sources[0].sha256` | a-commentary-on-the-20260609102650 | metadata | From source metadata JSON field "sha256" |

---

## Evidence Gaps and Inferences

| Gap | QID | Resolution |
|-----|-----|------------|
| Q8: No formal downstream handoff workflow in source | Q8 | Inferred from educational/self-study context described in Preface; recorded as inference in handoff_rules commentary |
| Q15: No MCP tools referenced in source | Q15 | Empty by confirmed absence of evidence; mcp field set to [] |

---

## Generated Artifacts

| Artifact | Type | Path | Notes |
|----------|------|------|-------|
| profile.yaml | canonical profile | `subagents/unix-v6-kernel-source-reviewer/profile.yaml` | |
| v6-assembly-annotation | skill | `subagents/unix-v6-kernel-source-reviewer/skills/v6-assembly-annotation/SKILL.md` | Not yet written |
| context-switch-trace | skill | `subagents/unix-v6-kernel-source-reviewer/skills/context-switch-trace/SKILL.md` | Not yet written |
| buffer-cache-protocol | skill | `subagents/unix-v6-kernel-source-reviewer/skills/buffer-cache-protocol/SKILL.md` | Not yet written |
| malloc-mfree-algorithm | skill | `subagents/unix-v6-kernel-source-reviewer/skills/malloc-mfree-algorithm/SKILL.md` | Not yet written |
| namei-pathname-search | skill | `subagents/unix-v6-kernel-source-reviewer/skills/namei-pathname-search/SKILL.md` | Not yet written |
| signal-machinery | skill | `subagents/unix-v6-kernel-source-reviewer/skills/signal-machinery/SKILL.md` | Not yet written |
| unix-programmer-manual-cross-reference | reference | `subagents/unix-v6-kernel-source-reviewer/references/unix-programmer-manual-cross-reference.md` | Not yet written |
| pdp11-processor-handbook-reference | reference | `subagents/unix-v6-kernel-source-reviewer/references/pdp11-processor-handbook-reference.md` | Not yet written |
| v6-source-file-index | reference | `subagents/unix-v6-kernel-source-reviewer/references/v6-source-file-index.md` | Not yet written |
| v6-procedure-call-cross-reference | reference | `subagents/unix-v6-kernel-source-reviewer/references/v6-procedure-call-cross-reference.md` | Not yet written |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-09 | Initial generation | a-commentary-on-the-20260609102650 |
| 0.3.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Open Questions

- Skill stub files (6 skills) and reference stub files (4 references) listed in
  knowledge_partition have not yet been written. These should be created before
  the adapter is exported.

---

## Conflict Log

_No conflicts recorded at time of generation. Single source; no multi-source
conflicts possible._
