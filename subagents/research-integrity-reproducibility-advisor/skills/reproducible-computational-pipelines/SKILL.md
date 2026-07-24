---
name: reproducible-computational-pipelines
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P022
  - P023
  - P030
  - P032
  - P026
  claims:
  - C00001
  - C00002
  - C00003
  - C00005
  - C00006
  - C00008
  - C00009
  - C00010
  - C00012
  - C00013
  - C00016
  - C00017
  - C00028
  - C00029
  - C00030
  - C00031
  evidence: []
  source_anchors: []
  authored_from_digest: c47d1c5ffadd522092ec92586514bdbd0121a394a2ea4887872ce6048585e810
---

# Reproducible Computational Pipelines

## Purpose

This skill guides building an analysis that another person — or the author's future self — can re-run and get the same result. It checks that data preparation is scripted rather than done by hand in a spreadsheet, that the whole computational environment and its software versions are captured (containers, semantic versioning), and that the project is modelled as a dependency tree built with a tool like Make or Snakemake so outputs rebuild when their prerequisites change.

## When to use

- An analysis is being built or reviewed and must be reproducible by a reviewer or collaborator later.
- Data is being cleaned or transformed by hand in a spreadsheet, producing a non-reproducible workflow.
- A project depends on many specific software or package versions and the environment must be captured so results do not silently change across machines.
- A multi-step analysis-to-manuscript pipeline needs a Make or Snakemake build and, where authored, its Makefile conventions checked.

## Procedure

1. Accept the upfront time cost of reproducibility because it is more than repaid (P002).
2. Do not manipulate or analyse data manually in spreadsheet software (P022).
3. Use containers to capture a whole computing environment for reproducibility (P023).
4. Capture the computational environment (P030).
5. Model a data-science project as a tree of dependencies and build it with a tool like Make or Snakemake that rebuilds an output whenever its prerequisites change (P032).
6. Follow Make authoring conventions (P026).

## Inputs

- The analysis workflow, its data-preparation steps, the software and environment it depends on, and any build or containerization already in place.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- Overlooking P002: Accept the upfront time cost of reproducibility because it is more than repaid.
- Overlooking P022: Do not manipulate or analyse data manually in spreadsheet software.
- Overlooking P023: Use containers to capture a whole computing environment for reproducibility.
- Overlooking P030: Capture the computational environment.
- Overlooking P032: Model a data-science project as a tree of dependencies and build it with a tool like Make or Snakemake that rebuilds an output whenever.
- Overlooking P026: Follow Make authoring conventions.

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P002, P022, P023, P030, P032, P026, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
