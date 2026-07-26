---
name: reproducible-computational-pipelines
kind: skill
status: ready
description: Use when scripted data prep is replaced by hand spreadsheet copy-paste, when the computational environment (OS, package versions, semantic versioning) is not captured, when a project needs containers/a Dockerfile to snapshot its dependency stack, or when a multi-step analysis-to-manuscript build needs a Make/Snakemake dependency tree and Makefile conventions (tabs, .PHONY, all/clean targets, automatic variables) checked.
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

1. Accept the upfront time cost of reproducibility because it is more than repaid: a version-controlled reproducible pipeline makes a reviewer's late request fast to satisfy and the work easy to reuse, being reproducible does not oblige support for reuse beyond re-running the published analyses, the primary beneficiaries are usually the research team and the researcher's future self, and the required skills (data engineering, RSE, technical writing, project management) are themselves a barrier worth investing in (P002).
2. Do not manipulate or analyse data manually in spreadsheet software, including copy-paste, because that produces a non-reproducible workflow; instead use scripts or a tool like OpenRefine that records the steps, validate the data for consistency, completeness, and correctness before it enters the analysis, and for collaborative collection reuse a standard versioned spreadsheet design with a shared template, per-column entry standards, and one person answering questions (P022).
3. Use containers to capture a whole computing environment for reproducibility, because the dependency stack of even a moderate project is huge and a self-contained snapshot is easier than resolving dependencies by hand; containers are lighter than virtual machines and more robust than package managers or Binder since they reproduce the entire system, and are shared by writing a recipe (Dockerfile), building an image, and distributing the image for others to run (P023).
4. Capture the computational environment — operating system, software, package versions, hardware, configuration — so research can be reproduced, because the same valid code can give different results in different environments (for example 1/5 differs between Python 2 and Python 3) and an uncaptured environment harms the researcher, collaborators, and science; publish the entire analysis stack from data up, and record software versions with semantic versioning (MAJOR.MINOR.PATCH) (P030).
5. Model the project as a tree of dependencies and build it with a tool like Make or Snakemake that rebuilds an output whenever its prerequisites change, because the resulting build file is human- and machine-readable, easy to share and version-control, reduces cognitive load through conventional targets, and lets collaborators or readers recompute the results to increase trust (P032).
6. Follow Make authoring conventions when writing or reviewing a Makefile: indent recipes with tabs not spaces, combine dependent commands on one line since each line runs in its own subshell, name the first target `all` and provide a `clean` target, declare non-file targets as `.PHONY`, avoid repetition with automatic variables and pattern rules and functions like `wildcard` and `patsubst`, define UPPERCASE variables at the top, develop the directory structure and Makefile together, and avoid recursive nested Makefiles that hide the full dependency graph (P026).

## Inputs

- The analysis workflow, its data-preparation steps, the software and environment it depends on, and any build or containerization already in place.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- The team treats reproducibility work as a sunk cost to skip under deadline pressure, with no version-controlled pipeline to answer a reviewer's later request — invest the upfront time because it is repaid when the request or reuse comes (P002).
- Numbers are hand-copied from spreadsheet cells (or copy-pasted between sheets) straight into the manuscript, with no script or recorded steps and no validation pass before analysis — replace with a scripted transformation or a tool like OpenRefine that records the steps and validates the data first (P022).
- The analysis "works on my machine" with no Dockerfile or equivalent recipe, so the dependency stack can only be reconstructed by hand from memory — capture the whole environment in a container recipe and distribute the built image (P023).
- Software or package versions used for a result are unrecorded (no semantic-versioning tags, no environment manifest), so re-running the same code later or on another machine can silently produce a different answer — record the operating system, software, package versions, and configuration alongside the analysis (P030).
- The steps from raw data to final figure or manuscript exist only as an informal sequence of manually run scripts, with no dependency-aware build, so a changed input does not visibly trigger a rebuild of the outputs that depend on it — model the project as a dependency tree in Make or Snakemake (P032).
- A submitted or reviewed Makefile mixes tabs and spaces in recipes, has no `all` or `clean` target, lacks `.PHONY` declarations for non-file targets, or nests recursive sub-Makefiles that hide the true dependency graph — bring it in line with standard Make authoring conventions (P026).

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P002, P022, P023, P030, P032, P026, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
