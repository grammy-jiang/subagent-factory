---
name: reproducibility-integrity-principles-index
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P005
  - P006
  - P007
  - P008
  - P009
  - P010
  - P011
  - P012
  - P013
  - P014
  - P015
  - P016
  - P017
  - P018
  - P019
  - P020
  - P021
  - P022
  - P023
  - P024
  - P025
  - P026
  - P027
  - P028
  - P029
  - P030
  - P031
  - P032
  - P033
  - P034
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00005
  - C00006
  - C00008
  - C00009
  - C00010
  - C00011
  - C00012
  - C00013
  - C00015
  - C00016
  - C00017
  - C00018
  evidence: []
  source_anchors: []
  authored_from_digest: 1d735ddd6a7def8f43091fdc5c73236edc75cd56babc83806bf57f6b34f1a0aa
---

# Reproducibility & Research-Integrity Principles Index

Package-wide index of every promoted principle, grouped by the skill that owns it. Each entry restates the principle's operative core; the full statement lives in `../principles/principles.yaml`.

## Research Data Management And Sharing

Skill: `research-data-management-and-sharing`

- **P001** — Address the real barriers to data sharing.
- **P017** — Manage outputs with a Data Management Plan, a living document covering roles and responsibilities, data types and sizes and metadata, storage and backup, post-project preservation, reuse.
- **P027** — Describe data so it can be understood and reused.
- **P033** — Provide rich PID metadata.

## Reproducible Computational Pipelines

Skill: `reproducible-computational-pipelines`

- **P002** — Accept the upfront time cost of reproducibility because it is more than repaid.
- **P022** — Do not manipulate or analyse data manually in spreadsheet software.
- **P023** — Use containers to capture a whole computing environment for reproducibility.
- **P030** — Capture the computational environment.
- **P032** — Model a data-science project as a tree of dependencies and build it with a tool like Make or Snakemake that rebuilds an output whenever its prerequisites change.
- **P026** — Follow Make authoring conventions.

## Version Control And Collaboration

Skill: `version-control-and-collaboration`

- **P019** — Use version control, the systematic recording of changes to files over time.
- **P029** — Commit well: make each commit an atomic single change, commit no generated files, stage the specific files by name rather than adding everything, and write a meaningful message with a roughly.
- **P031** — Keep the main branch always stable and only merge finished, tested work into it; when a merge conflict occurs.

## Research Software Engineering And Testing

Skill: `research-software-engineering-and-testing`

- **P005** — Manage research software with a Software Management Plan, a living document describing how the software is developed, documented, versioned, licensed, archived, and shared; treat even one-off.
- **P021** — Build a layered test suite with both positive tests.
- **P034** — Unit-test the smallest testable parts in isolation.
- **P016** — Build open hardware to be modular and extensible with documented interfaces so a community can grow around it, be honest with collaborators about the support they can expect, make the project.

## Open Source Projects And Licensing

Skill: `open-source-projects-and-licensing`

- **P018** — Run an open source project with the essential files.
- **P024** — Contribute well to another open source project.
- **P020** — Understand usage-restricting licences.
- **P025** — Choose a data licence deliberately.
- **P028** — License the parts of an ML or AI system separately.
- **P012** — Make research sufficiently open for exchange, scrutiny, and authorized follow-on use while withholding only information protected by valid secrecy, confidentiality, or intellectual-property duties.

## Research Integrity And Misconduct

Skill: `research-integrity-and-misconduct`

- **P006** — Classify possible misconduct under the applicable definition and evidence threshold, distinguishing fabrication, falsification, and plagiarism from honest error, negligence, and differences.
- **P008** — Never manipulate, select, process, visualize, interpret, or report data so that the apparent support exceeds what the observations warrant; examine design and measurement weaknesses as well.
- **P009** — Investigate data-integrity concerns by distinguishing invented research from manipulation of real research, preserving and inspecting original records, and using specialist reconstruction.
- **P003** — Act on a credible conduct concern through a calibrated path.
- **P010** — Begin human-subject or identifiable-private-data research only after appropriate review, with qualified operators and student supervision, and protect participants through risk minimization, informed.

## Authorship, Publication And Attribution

Skill: `authorship-publication-and-attribution`

- **P004** — Assign authorship only for substantive research contributions, order authors by contribution, disciplinary convention, or agreement, require each author to review and own the contributed part.
- **P007** — Choose publication units for coherence, completeness, and significant contribution; do not republish substantially the same findings or fragment a study merely to inflate output, while allowing.
- **P011** — Audit citations for bibliographic accuracy, relevance, and actual support, search the literature thoroughly, and read and cite original work where possible rather than relying only on later summaries.
- **P013** — Permit a full or secondary publication only when the prior dissemination is eligible, every similar report is disclosed and cross-cited, relevant materials are supplied, and all required editorial.
- **P015** — Detect plagiarism by substantive appropriation, not surface similarity.
- **P014** — Disclose potentially patentable inventions promptly through the applicable institutional process, identify all and only qualifying inventors, and reconcile jurisdiction-specific rules before.
